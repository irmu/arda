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
2019/11/03: Domain updates
2019/11/08: Moved base_link calls down to sources. Let's see how this goes, Mmmmkay?
'''

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cache, cfscrape, cleantitle, client, control, debrid, log_utils, source_utils, workers


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['magnet']
        self.domains = ['torrentdownloads.me', 'torrentdownloads.info']
        self._base_link = None
        self.search = '%s/rss.xml?new=1&type=search&cid={0}&search={1}'
        self.scraper = cfscrape.create_scraper()

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
            log_utils.log('TorrentsDL - Exception: \n' + str(failure))
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
            log_utils.log('TorrentsDL - Exception: \n' + str(failure))
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
            log_utils.log('TorrentsDL - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            self._sources = []
            if url is None:
                return self._sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])
                                        ) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            self.search = self.search % (self.base_link)
            if 'tvshowtitle' in data:
                url = self.search.format('8', urllib.quote(query))
            else:
                url = self.search.format('4', urllib.quote(query))
            self.hostDict = hostDict + hostprDict

            self.timer = control.Time(start=True)

            html = self.scraper.get(url).content
            if html is None:
                log_utils.log('TorrentsDL - Website Timed Out')
                return self._sources

            threads = []
            for i in re.findall(r'<item>(.+?)</item>', html, re.DOTALL):
                threads.append(workers.Thread(self._get_items, i, sc_timeout))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self._sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('TorrentsDL - Exception: \n' + str(failure))
            return self._sources

    def _get_items(self, r, sc_timeout):
        try:
            # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
            if self.timer.elapsed() > sc_timeout:
                log_utils.log('TorrentsDL - Timeout Reached')
                return self.items
            size = re.search(r'<size>([\d]+)</size>', r).groups()[0]
            seeders = re.search(r'<seeders>([\d]+)</seeders>', r).groups()[0]
            _hash = re.search(r'<info_hash>([a-zA-Z0-9]+)</info_hash>', r).groups()[0]
            name = re.search(r'<title>(.+?)</title>', r).groups()[0]
            url = 'magnet:?xt=urn:btih:%s&dn=%s' % (_hash.upper(), urllib.quote_plus(name))
            t = name.split(self.hdlr)[0]
            try:
                y = re.findall(r'[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
            except BaseException:
                y = re.findall(r'[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
            try:
                div = 1000 ** 3
                size = float(size) / div
                size = '%.2f GB' % size
            except BaseException:
                size = '0'
            quality, info = source_utils.get_release_quality(name, name)
            info.append(size)
            info = ' | '.join(info)
            if not seeders == '0':
                if cleantitle.get(re.sub('(|)', '', t)) == cleantitle.get(self.title):
                    if y == self.hdlr:
                        self._sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en',
                                              'url': url, 'info': info, 'direct': False, 'debridonly': True})
        except BaseException:
            pass

    def __get_base_url(self, fallback):
        try:
            for domain in self.domains:
                try:
                    url = 'https://%s' % domain
                    result = client.request(url, timeout='10')
                    search_n = re.findall('alt="Torrent Downloads"', result, re.DOTALL)[0]
                    if search_n:
                        return url
                except Exception:
                    pass
        except Exception:
            pass

        return fallback

    def resolve(self, url):
        return url
