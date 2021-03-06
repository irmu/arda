# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2019/4/16: Updated to use CFScrape - Still using single request
2019/5/12: Fixed search
'''

import re
import traceback
import urllib
import urlparse
import xbmcgui

from resources.lib.modules import cfscrape, cleantitle, client, control, debrid, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['myvideolinks.net', 'iwantmyshow.tk', 'new.myvideolinks.net']
        self.base_link = 'http://myvideolinks.net'
        self.search_link = '/mv1/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyVideoLink - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyVideoLink - Exception: \n' + str(failure))
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
            log_utils.log('MyVideoLink - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            scraper = cfscrape.create_scraper()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'],
                int(data['season']),
                int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
                data['title'],
                data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % urllib.quote_plus(query)

            timer = control.Time(start=True)

            r = scraper.get(url).content

            r = client.parseDOM(r, 'h2')
            z = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            r = [
                (i[0],
                 i[1],
                 re.sub('(\.|\(|\[|\s)(\d{4}|3D)(\.|\)|\]|\s|)(.+|)', '', i[1]),
                 re.findall('[\.|\(|\[|\s](\d{4}|)([\.|\)|\]|\s|].+)', i[1])) for i in z]
            r = [(i[0], i[1], i[2], i[3][0][0], i[3][0][1]) for i in r if i[3]]
            r = [(i[0], i[1], i[2], i[3], re.split('\.|\(|\)|\[|\]|\s|\-', i[4])) for i in r]
            r = [i for i in r if cleantitle.get(title) == cleantitle.get(i[2]) and data['year'] == i[3]]
            r = [i for i in r if not any(x in i[4]
                                         for x in ['HDCAM', 'CAM', 'DVDR', 'DVDRip', 'DVDSCR', 'HDTS', 'TS', '3D'])]
            r = [i for i in r if '1080p' in i[4]][:1] + [i for i in r if '720p' in i[4]][:1]

            if 'tvshowtitle' in data:
                posts = [(i[1], i[0]) for i in z]
            else:
                posts = [(i[1], i[0]) for i in z]

            hostDict = hostprDict + hostDict

            items = []

            for post in posts:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('MyVideoLink - Timeout Reached')
                    break

                try:
                    t = post[0]

                    u = scraper.get(post[1]).content
                    u = re.findall('\'(http.+?)\'', u) + re.findall('\"(http.+?)\"', u)
                    u = [i for i in u if '/embed/' not in i]
                    u = [i for i in u if 'youtube' not in i]

                    items += [(t, i) for i in u]
                except Exception:
                    pass

            for item in items:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('MyVideoLink - Timeout Reached')
                    break

                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)

                    if not cleantitle.get(t) == cleantitle.get(title):
                        raise Exception()

                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()

                    if not y == hdlr:
                        raise Exception()

                    fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', name.upper())
                    fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                    fmt = [i.lower() for i in fmt]

                    if any(i.endswith(('subs', 'sub', 'dubbed', 'dub')) for i in fmt):
                        raise Exception()
                    if any(i in ['extras'] for i in fmt):
                        raise Exception()

                    if '1080p' in fmt:
                        quality = '1080p'
                    elif '720p' in fmt:
                        quality = 'HD'
                    else:
                        quality = 'SD'
                    if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt):
                        quality = 'SCR'
                    elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt):
                        quality = 'CAM'

                    info = []

                    if '3d' in fmt:
                        info.append('3D')

                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', item[2])[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        size = '%.2f GB' % size
                        info.append(size)
                    except Exception:
                        pass

                    if any(i in ['hevc', 'h265', 'x265'] for i in fmt):
                        info.append('HEVC')

                    info = ' | '.join(info)

                    url = item[1]
                    if any(x in url for x in ['.rar', '.zip', '.iso']):
                        raise Exception()
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if host not in hostDict:
                        raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'language': 'en',
                                    'url': url, 'info': info, 'direct': False, 'debridonly': debrid.status()})
                except Exception:
                    pass

            check = [i for i in sources if not i['quality'] == 'CAM']
            if check:
                sources = check

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyVideoLink - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
