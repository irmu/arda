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
2019/06/23: Readded with my own tweaks and enhancements. Pulled from other Covenant/Placenta forks.
2019/11/03: Increased pages for searches. Fuck it
2019/11/04: Note to self----Stop doing function calls like self.base_link() in the god damn init. Slows
            the start of scrapers since ALL scrapers (regardless of settings), run and the init executes
            before filtering out www, magnet, etc. BAD DOG, BAD DOG. Dumbass
2019/11/08: Moved base_link calls down to sources. Let's see how this goes, Mmmmkay?
2019/12/28: Base updates - Thx to other scrapers. Too lazy to work on them lately.
'''

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cache, cfscrape, cleantitle, client, control, debrid, log_utils, source_utils, workers
from resources.lib.modules import dom_parser2 as dom

class source:
    def __init__(self):
        self.priority = 1
        self.source = ['magnet']
        self.domains = ['1337x.to', 'x1337x.ws', '1337x.st', 'x1337x.eu', '1337x.is', '1337x.unblocked.win']
        self._base_link = None

    @property
    def base_link(self):
        if self._base_link is None:
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
            log_utils.log('1337x - Exception: \n' + str(failure))
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
            log_utils.log('1337x - Exception: \n' + str(failure))
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
            log_utils.log('1337x - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            self._sources = []
            self.items = []

            if url is None:
                return self._sources

            if self._base_link is None:
                self.base_link = cache.get(self.__get_base_url, 240, 'https://%s' % self.domains[0])

            self.tvsearch = '%s/sort-category-search/%s/TV/seeders/desc/%s/' % (self.base_link, '%s', '%s')
            self.moviesearch = '%s/sort-category-search/%s/Movies/size/desc/%s/' % (self.base_link, '%s', '%s')

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
            urls = []
            if 'tvshowtitle' in data:
                urls.append(self.tvsearch % (urllib.quote(query), '1'))
                urls.append(self.tvsearch % (urllib.quote(query), '2'))
                urls.append(self.tvsearch % (urllib.quote(query), '3'))
            else:
                urls.append(self.moviesearch % (urllib.quote(query), '1'))
                urls.append(self.moviesearch % (urllib.quote(query), '2'))
                urls.append(self.moviesearch % (urllib.quote(query), '3'))
            threads = []

            self.timer = control.Time(start=True)

            for url in urls:
                threads.append(workers.Thread(self._get_items, url, sc_timeout))
            [i.start() for i in threads]
            [i.join() for i in threads]

            self.hostDict = hostDict + hostprDict
            threads2 = []
            for i in self.items:
                threads2.append(workers.Thread(self._get_sources, i, sc_timeout))
            [i.start() for i in threads2]
            [i.join() for i in threads2]

            return self._sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('1337x - Exception: \n' + str(failure))
            return self._sources

    def _get_items(self, url, sc_timeout):
        try:
            scraper = cfscrape.create_scraper()
            r = scraper.get(url).content
            posts = client.parseDOM(r, 'tbody')[0]
            posts = client.parseDOM(posts, 'tr')
            for post in posts:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if self.timer.elapsed() > sc_timeout:
                    log_utils.log('1337x - Timeout Reached')
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
            failure = traceback.format_exc()
            log_utils.log('1337x - Exception: \n' + str(failure))
            return self.items

    def _get_sources(self, item, sc_timeout):
        try:
            # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
            if self.timer.elapsed() > sc_timeout:
                log_utils.log('1337x - Timeout Reached')
                return

            scraper = cfscrape.create_scraper()
            name = item[0]
            quality, info = source_utils.get_release_quality(item[1], name)
            info.append(item[2])
            info = ' | '.join(info)
            data = scraper.get(item[1]).content
            data = client.parseDOM(data, 'a', ret='href')
            url = [i for i in data if 'magnet:' in i][0]
            url = url.split('&tr')[0]

            self._sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
        except Exception:
            pass

    def __get_base_url(self, fallback):
        try:
            for domain in self.domains:
                try:
                    url = 'https://%s' % domain
                    result = client.request(url, timeout='10')
                    search_n = re.findall('<input type="submit" title="(.+?)"', result, re.DOTALL)[0]
                    if search_n and 'Pirate Search' in search_n:
                        return url
                except Exception:
                    pass
        except Exception:
            pass

        return fallback

    def resolve(self, url):
        return url
