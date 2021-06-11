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
Note: Any scraper with it's own worker threads may give false positives in Thread Monitor as hanged, due to thread pausing while the workers do their thing.
2019/07/07: Initial import to Atreides from other Covenant/Placenta Forks
'''

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cleantitle, client, control, debrid, dom_parser2, log_utils, source_utils, workers


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['www.mkvhub.com']
        self.base_link = 'https://www.mkvhub.com/'
        self.search_link = '/search/%s/feed/rss2/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MKVHub - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MKVHub - Exception: \n' + str(failure))
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
            log_utils.log('MKVHub - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            self._sources = []

            if url is None:
                return self._sources

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                    if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            self.timer = control.Time(start=True)

            r = client.request(url)
            posts = client.parseDOM(r, 'item')

            items = []
            for post in posts:
                try:
                    t = re.findall('<title>(.+?)</title>', post, re.IGNORECASE)[0]
                    name = t.split(hdlr)[0].replace('(', '')
                    if not cleantitle.get(name) == cleantitle.get(title):
                        continue

                    try:
                        y = re.findall(r'(?:\.|\(|\[|\s*|)(S\d+E\d+|S\d+)(?:\.|\)|\]|\s*|)', t, re.I)[-1].upper()
                    except Exception:
                        y = re.findall(r'(?:\.|\(|\[|\s*|)(\d{4})(?:\.|\)|\]|\s*|)', t, re.I)[-1]

                    if not y == hdlr:
                        continue

                    urls = [(client.parseDOM(post, 'a', ret='href', attrs={'class': 'dbuttn watch'})[0],
                             client.parseDOM(post, 'a', ret='href', attrs={'class': 'dbuttn blue'})[0],
                             client.parseDOM(post, 'a', ret='href', attrs={'class': 'dbuttn magnet'})[0])]
                    try:
                        size = re.findall(
                            '((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', post)[0]
                        div = 1 if size.endswith(('GB', 'GiB', 'Gb')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                        size = '%.2f GB' % size
                    except Exception:
                        size = '0'
                    items += [(t, urls, size)]
                except Exception:
                    pass

            datos = []
            for title, urls, size in items:
                try:
                    name = client.replaceHTMLCodes(title)
                    quality, info = source_utils.get_release_quality(name, name)
                    info.append(size)
                    info = ' | '.join(info)
                    datos.append((urls[0], quality, info))
                except Exception:
                    pass

            threads = []
            for i in datos:
                threads.append(workers.Thread(self._get_sources, i[0], i[1], i[2], hostDict, sc_timeout))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self._sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MKVHub - Exception: \n' + str(failure))
            return self._sources

    def _get_sources(self, urls, quality, info, hostDict, sc_timeout):
        try:
            for url in urls:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if self.timer.elapsed() > sc_timeout:
                    log_utils.log('2DDL - Timeout Reached')
                    return self._sources

                r = client.request(url)
                if 'linkprotector' in url:
                    p_link = dom_parser2.parse_dom(r, 'link', {'rel': 'canonical'},  req='href')[0]
                    p_link = p_link.attrs['href']
                    input_name = client.parseDOM(r, 'input', ret='name')[0]
                    input_value = client.parseDOM(r, 'input', ret='value')[0]
                    post = {input_name: input_value}
                    p_data = client.request(p_link, post=post)
                    links = client.parseDOM(p_data, 'a', ret='href', attrs={'target': '_blank'})
                    for i in links:
                        valid, host = source_utils.is_host_valid(i, hostDict)
                        if not valid:
                            continue
                        self._sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': i, 'info': info, 'direct': False, 'debridonly': debrid.status()})
                elif 'torrent' in url:
                    if debrid.status(True) is False:
                        continue

                    data = client.parseDOM(r, 'a', ret='href')
                    url = [i for i in data if 'magnet:' in i][0]
                    url = url.split('&tr')[0]
                    self._sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
        except Exception:
            pass

    def resolve(self, url):
        return url
