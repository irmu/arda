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
2019/11/03: Initial Import to addon. Pulled from Oath/Scrubs
'''

import re
import urllib
import urlparse

from resources.lib.modules import cache, cfscrape, cleantitle, client, control, debrid, log_utils, source_utils, workers
from resources.lib.modules import dom_parser2 as dom


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['magnet']
        self.domains = ['limetorrents.info', 'limetorrents.co', 'limetor.com']
        self._base_link = None
        self.scraper = cfscrape.create_scraper()
        self.tvsearch = '/search/tv/{0}/'
        self.moviesearch = '/search/movies/{0}/'

    @property
    def base_link(self):
        if not self._base_link:
            self._base_link = cache.get(self.__get_base_url, 120, 'https://%s' % self.domains[0])
        return self._base_link

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status(True) is False:
            return

        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('LimeTorrents - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status(True) is False:
            return

        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('LimeTorrents - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status(True) is False:
            return

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
            log_utils.log('LimeTorrents - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            self._sources = []
            self.items = []
            if url is None:
                return self._sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])
                                        ) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (
                data['tvshowtitle'],
                int(data['season']),
                int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
                data['title'],
                data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            if 'tvshowtitle' in data:
                url = self.tvsearch.format(urllib.quote(query))
                url = urlparse.urljoin(self.base_link, url)
            else:
                url = self.moviesearch.format(urllib.quote(query))
                url = urlparse.urljoin(self.base_link, url)

            self.timer = control.Time(start=True)

            self._get_items(url, sc_timeout)
            self.hostDict = hostDict + hostprDict
            threads = []
            for i in self.items:
                threads.append(workers.Thread(self._get_sources, i, sc_timeout))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self._sources
        except Exception:
            return self._sources

    def _get_items(self, url, sc_timeout):
        try:
            r = self.scraper.get(url).content
            posts = client.parseDOM(r, 'table', attrs={'class': 'table2'})[0]
            posts = client.parseDOM(posts, 'tr')
            log_utils.log("Post Count: " + str(len(posts)))
            for post in posts:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if self.timer.elapsed() > sc_timeout:
                    log_utils.log('LimeTorrents - Timeout Reached')
                    return self.items

                data = dom.parse_dom(post, 'a', req='href')[1]
                link = urlparse.urljoin(self.base_link, data.attrs['href'])
                name = data.content

                t = name.split(self.hdlr)[0]
                if not cleantitle.get(re.sub('(|)', '', t)) == cleantitle.get(self.title):
                    continue

                try:
                    y = re.findall('[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                except Exception:
                    y = re.findall('[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
                if not y == self.hdlr:
                    continue

                try:
                    size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                    div = 1 if size.endswith('GB') else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                    size = '[B]%.2f GB[/B]' % size
                except Exception:
                    size = '0'
                self.items.append((name, link, size))
            return self.items
        except Exception:
            return self.items

    def _get_sources(self, item, sc_timeout):
        # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
        if self.timer.elapsed() > sc_timeout:
            log_utils.log('1337x - Timeout Reached')
            return self.items

        try:
            name = item[0]
            quality, info = source_utils.get_release_quality(name, name)
            info.append(item[2])
            info = ' | '.join(info)
            data = self.scraper.get(item[1]).content
            url = re.search('''href=["'](magnet:\?[^"']+)''', data).groups()[0]
            self._sources.append(
                {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False,
                 'debridonly': True})
        except Exception:
            pass

    def resolve(self, url):
        return url

    def __get_base_url(self, fallback):
        try:
            for domain in self.domains:
                try:
                    url = 'https://%s' % domain
                    result = self.scraper.get(url).content
                    result = re.findall('<title>(.+?)</title>', result, re.DOTALL)[0]
                    if result and 'LimeTorrents' in result:
                        return url
                except Exception:
                    pass
        except Exception:
            pass
        return fallback
