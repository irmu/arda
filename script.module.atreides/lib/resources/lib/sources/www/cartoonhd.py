# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with
# this stuff. If we meet some day, and you think this stuff is worth it,
# you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2019/07/08: Minor tweaks
2019/07/18: Rewrote search portion to use the API for more accuracy. Need to find resolver for viduplayer.com embed links to make it pull ALL links properly
2019/10/04: Added some additional resolving per updates from shellc0de
'''

import base64
import json
import re
import time
import traceback
import urllib
import urlparse

import xbmc

from resources.lib.modules import cache, cfscrape, cleantitle, client, control, directstream, jsunpack, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 0
        self.source = ['www']
        self.domains = ['cartoonhd.cz', 'www1.cartoonhd.it', 'www1.cartoonhd.care']
        self._base_link = None
        self.search_link = 'https://api.cartoonhd.cz/api/v1/0A6ru35yevokjaqbb3'
        self.search_set = "MmTkOQzKUxltDSrwSNEWnmqCs"
        '''
        Next two are referenced. They are in the headers, but currently never change and combine to equal the search url last item.
        If they start changing it up, will look at pulling them out of the header to append to the search link.
        '''
        self.search_slk = "0A6ru35y"
        self.search_key = "evokjaqbb3"

    @property
    def base_link(self):
        if not self._base_link:
            self._base_link = cache.get(self.__get_base_url, 120, 'https://%s' % self.domains[0])
        return self._base_link

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CartoonHD - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CartoonHD - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CartoonHD - Exception: \n' + str(failure))
            return

    def searchShow(self, title, season, episode, year):
        try:
            chkurl = urlparse.urljoin(self.base_link, '/tv-shows')
            data = client.request(chkurl, headers={})

            try:
                tok = re.findall("var\s*tok\s*=\s*'(.+?)'", data)[0]
            except Exception:
                log_utils.log('CartoonHD: Unable to retrieve token')
                return

            params = {
                "q": cleantitle.geturl(title),
                "limit": 100,
                "timestamp": int(time.time() * 1000),
                "verifiedCheck": tok,
                "set": self.search_set,
                "rt": self.search_set,
                "sl": self.search_key
                }

            results = client.request(self.search_link, referer=chkurl, post=params)
            for entry in json.loads(results):
                if "show" not in entry["meta"].lower():
                    continue
                if str(year) != str(entry["year"]):
                    continue
                if cleantitle.get(title) == cleantitle.get(entry["title"]):
                    return urlparse.urljoin(self.base_link, entry["permalink"])
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CartoonHD - Exception: \n' + str(failure))
            return

    def searchMovie(self, title, year):
        try:
            chkurl = urlparse.urljoin(self.base_link, '/films')
            data = client.request(chkurl, headers={})
            try:
                tok = re.findall("var\s*tok\s*=\s*'(.+?)'", data)[0]
            except Exception:
                log_utils.log('CartoonHD: Unable to retrieve token')
                return

            params = {
                "q": cleantitle.geturl(title),
                "limit": 100,
                "timestamp": int(time.time() * 1000),
                "verifiedCheck": tok,
                "set": self.search_set,
                "rt": self.search_set,
                "sl": self.search_key
                }

            results = client.request(self.search_link, referer=chkurl, post=params)
            for entry in json.loads(results):
                if "movie" not in entry["meta"].lower():
                    continue
                if str(year) != str(entry["year"]):
                    continue
                if cleantitle.get(title) == cleantitle.get(entry["title"]):
                    return urlparse.urljoin(self.base_link, entry["permalink"])
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CartoonHD - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            hostDict = hostDict + hostprDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            imdb = data['imdb']

            timer = control.Time(start=True)

            if 'tvshowtitle' in data:
                url = self.searchShow(title, int(data['season']), int(data['episode']), data['year'])
                url = url + '/season/%s/episode/%s' % (data['season'], data['episode'])
            else:
                url = self.searchMovie(title, data['year'])

            r = client.request(url, output='extended', timeout='10')

            if not imdb in r[0]:
                log_utils.log('CartoonHD - IMDB Not Found')
                return sources

            cookie = r[4]
            headers = r[3]
            result = r[0]
            try:
                r = re.findall('(https:.*?redirector.*?)[\'\"]', result)
                for i in r:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('CartoonHD - Timeout Reached')
                        break

                    try:
                        sources.append({'source': 'gvideo', 'quality': directstream.googletag(
                            i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                    except Exception:
                        pass
            except Exception:
                pass

            try:
                auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except Exception:
                auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)
            headers['Authorization'] = auth
            headers['Referer'] = url
            u = '/ajax/vsozrflxcw.php'

            self.base_link = client.request(self.base_link, headers=headers, output='geturl')
            u = urlparse.urljoin(self.base_link, u)
            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'
            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())
            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]
            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]
            post = {'action': action, 'idEl': idEl, 'token': token, 'nopop': '', 'elid': elid}
            post = urllib.urlencode(post)
            cookie += ';%s=%s' % (idEl, elid)
            headers['Cookie'] = cookie

            r = client.request(u, post=post, headers=headers, cookie=cookie, XHR=True)
            r = str(json.loads(r))

            if len(r) > 0:
                r = re.findall('\'(http.+?)\'', r) + re.findall('\"(http.+?)\"', r)
                for i in r:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('CartoonHD - Timeout Reached')
                        break

                    try:
                        if 'google' in i:
                            quality = 'SD'
                            if 'googleapis' in i:
                                try:
                                    quality = source_utils.check_sd_url(i)
                                except Exception:
                                    pass
                            if 'googleusercontent' in i:
                                i = directstream.googleproxy(i)
                                try:
                                    quality = directstream.googletag(i)[0]['quality']
                                except Exception:
                                    pass
                            sources.append({'source': 'gvideo', 'quality': quality, 'language': 'en',
                                            'url': i, 'direct': True, 'debridonly': False})
                        elif 'llnwi.net' in i or 'vidcdn.pro' in i:
                            try:
                                quality = source_utils.check_sd_url(i)
                                sources.append({'source': 'CDN', 'quality': quality, 'language': 'en',
                                                'url': i, 'direct': True, 'debridonly': False})
                            except Exception:
                                pass
                        # tested with Brightburn 2019 and Yellowstone S02E04
                        elif 'vidnode.net/streaming.php' in i:
                            try:
                                vc_headers = {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                                    'Referer': i
                                }
                                r = client.request(i, headers=vc_headers)
                                clinks = re.compile('''sources:\[\{file: ['"](.+?)['"]''').findall(r)[1]
                                r = client.request(clinks, headers=vc_headers)
                                regex = re.compile('[A-Z]{4}="(.+?)"\s+\w+\.\w(.+?)\.', re.DOTALL).findall(r)
                                for quality, links in regex:
                                    quality = source_utils.check_sd_url(quality)
                                    stream_link = clinks.rstrip('.m3u8')
                                    final = '{0}{1}.m3u8'.format(stream_link, links)
                                    sources.append({'source': 'cdn', 'quality': quality, 'language': 'en',
                                                    'url': final+'|Referer='+i, 'direct': True, 'debridonly': False})
                            except Exception:
                                pass
                        # tested with Captain Marvel 2019
                        elif 'viduplayer' in i:
                            try:
                                vp_headers = {
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                                    'Referer': i
                                }
                                result = client.request(i, headers=vp_headers)
                                for x in re.findall('(eval\s*\(function.*?)</script>', result, re.DOTALL):
                                    try:
                                        result += jsunpack.unpack(x).replace('\\', '')
                                    except Exception:
                                        pass
                                result = jsunpack.unpack(result)
                                result = unicode(result, 'utf-8')
                                links = re.findall('''['"]?file['"]?\s*:\s*['"]([^'"]+)['"][^}]*['"]?label['"]?\s*:\s*['"]([^'"]*)''', result, re.DOTALL)
                                for direct_links, qual in links:
                                    quality = source_utils.check_sd_url(qual)
                                    sources.append({'source': 'vidu', 'quality': quality, 'language': 'en',
                                                    'url': direct_links, 'direct': True, 'debridonly': False})
                            except Exception:
                                pass
                        else:
                            if 'vidnode.net/load.php' in i:
                                continue
                            valid, hoster = source_utils.is_host_valid(i, hostDict)
                            if not valid:
                                continue
                            sources.append({'source': hoster, 'quality': '720p', 'language': 'en',
                                            'url': i, 'direct': False, 'debridonly': False})
                    except Exception:
                        pass
            return sources
        except:
            return sources

    def __get_base_url(self, fallback):
        try:
            for domain in self.domains:
                try:
                    url = 'https://%s' % domain
                    result = client.request(url, limit=1, timeout='5')
                    result = re.findall('<meta property="og:site_name" content="(.+?)" />', result, re.DOTALL)[0]
                    if result and 'Cartoon HD' in result:
                        return url
                except:
                    pass
        except:
            pass
        return fallback

    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url
