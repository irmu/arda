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
2019/07/06: Domain and one host domain change
2020/01/12: Update for node links, thx to shell
'''

import json
import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cleantitle, client, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['gowatchseries.io', 'gowatchseries.co']
        self.base_link = 'https://gowatchseries.tv'
        self.search_link = '/ajax-search.html?keyword=%s&id=-1'
        self.search_link2 = '/search.html?keyword=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoWatchSeries - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoWatchSeries - Exception: \n' + str(failure))
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
            log_utils.log('GoWatchSeries - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            if not str(url).startswith('http'):

                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
                season, episode = '', ''
                if 'season' in data:
                    season = data['season']
                if 'episode' in data:
                    episode = data['episode']
                year = data['year']

                r = client.request(self.base_link, output='extended', timeout='10')
                cookie = r[4]
                headers = r[3]
                # result = r[0]
                headers['Cookie'] = cookie

                query = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.getsearch(title)))

                timer = control.Time(start=True)

                r = client.request(query, headers=headers, XHR=True)
                r = json.loads(r)['content']
                r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a'))

                if 'tvshowtitle' in data:
                    cltitle = cleantitle.get(title+'season'+season)
                    cltitle2 = cleantitle.get(title+'season%02d' % int(season))
                    r = [i for i in r if cltitle == cleantitle.get(i[1]) or cltitle2 == cleantitle.get(i[1])]
                    vurl = '%s%s-episode-%s' % (self.base_link, str(r[0][0]).replace('/info', ''), episode)
                    vurl2 = None
                else:
                    cltitle = cleantitle.getsearch(title)
                    cltitle2 = cleantitle.getsearch('%s (%s)' % (title, year))
                    r = [i for i in r if cltitle2 == cleantitle.getsearch(i[1]) or cltitle == cleantitle.getsearch(i[1])]
                    vurl = '%s%s-episode-0' % (self.base_link, str(r[0][0]).replace('/info', ''))
                    vurl2 = '%s%s-episode-1' % (self.base_link, str(r[0][0]).replace('/info', ''))

                r = client.request(vurl, headers=headers)
                headers['Referer'] = vurl

                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('GoWatchSeries - Timeout Reached')
                    return sources

                slinks = client.parseDOM(r, 'div', attrs={'class': 'anime_muti_link'})
                slinks = client.parseDOM(slinks, 'li', ret='data-video')
                if len(slinks) == 0 and vurl2 is not None:
                    r = client.request(vurl2, headers=headers)
                    headers['Referer'] = vurl2
                    slinks = client.parseDOM(r, 'div', attrs={'class': 'anime_muti_link'})
                    slinks = client.parseDOM(slinks, 'li', ret='data-video')

                for slink in slinks:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('GoWatchSeries - Timeout Reached')
                        break

                    try:
                        if 'vidnode.net/streaming.php' in slink:
                            vc_headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
                                'Referer': 'https:{0}'.format(slink)
                            }
                            r = client.request('https:{0}'.format(slink), headers=vc_headers)
                            clinks = re.compile('''window\.urlVideo = ['"](.+?)['"]''').findall(r)[0]
                            r = client.request(clinks, headers=vc_headers)
                            regex = re.compile('[A-Z]{10}=\d+x(\d+)\s+\/(.+?)\.', re.DOTALL).findall(r)
                            for quality, links in regex:
                                quality = source_utils.check_sd_url(quality)
                                stream_link = clinks.split('hls/')[0]
                                final = '{0}{1}.m3u8'.format(stream_link, links)
                                sources.append({'source': 'cdn', 'quality': quality, 'language': 'en', 'url': final+'|Referer=https:{0}'.format(slink), 'direct': True, 'debridonly': False})
                        else:
                            # if 'vidnode.net/load.php' in slink:
                            #     continue
                            valid, hoster = source_utils.is_host_valid(slink, hostDict)
                            if any(x in hoster for x in ['openload', 'streamango', 'streamcherry', 'rapidvideo', 'verystream', 'vidnode']):
                                continue
                            if valid:
                                sources.append({'source': hoster, 'quality': 'SD', 'language': 'en', 'url': slink, 'direct': False, 'debridonly': False})
                    except Exception:
                        pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('GoWatchSeries - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
