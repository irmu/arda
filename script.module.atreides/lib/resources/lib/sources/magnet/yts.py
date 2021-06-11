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


import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cfscrape, cleantitle, client, control, debrid, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['magnet']
        self.domains = ['yts.lt']
        self.base_link = 'https://yts.lt/'
        self.search_link = '/browse-movies/%s/all/all/0/latest'
        self.scraper = cfscrape.create_scraper()
        self.min_seeders = int(control.setting('torrent.min.seeders'))

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status(True) is False:
            return

        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('YTSAM - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s %s' % (data['title'], data['year'])

            url = self.search_link % urllib.quote(query)
            url = urlparse.urljoin(self.base_link, url)

            timer = control.Time(start=True)

            html = self.scraper.get(url).content
            if html is None:
                log_utils.log('YTS - Website Timed Out')
                return sources
            try:
                results = client.parseDOM(html, 'div', attrs={'class': 'row'})[2]
            except Exception:
                return sources

            items = re.findall('class="browse-movie-bottom">(.+?)</div>\s</div>', results, re.DOTALL)
            if items is None:
                return sources

            for entry in items:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('YTSAM - Timeout Reached')
                    break

                try:
                    try:
                        link, name = re.findall('<a href="(.+?)" class="browse-movie-title">(.+?)</a>', entry, re.DOTALL)[0]
                        name = client.replaceHTMLCodes(name)
                        if not cleantitle.get(data['title']) in cleantitle.get(name):
                            continue
                    except Exception:
                        continue
                    y = entry[-4:]
                    if not y == data['year']:
                        continue

                    response = self.scraper.get(link).content
                    try:
                        entries = client.parseDOM(response, 'div', attrs={'class': 'modal-torrent'})
                        for torrent in entries:
                            # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                            if timer.elapsed() > sc_timeout:
                                log_utils.log('YTSAM - Timeout Reached')
                                break

                            link, name = re.findall('href="magnet:(.+?)" class="magnet-download download-torrent magnet" title="(.+?)"', torrent, re.DOTALL)[0]
                            link = 'magnet:%s' % link
                            link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                            quality, info = source_utils.get_release_quality(name, name)
                            try:
                                size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', torrent)[-1]
                                div = 1 if size.endswith(('GB', 'GiB')) else 1024
                                size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                                size = '%.2f GB' % size
                                info.append(size)
                            except Exception:
                                pass
                            info = ' | '.join(info)
                            sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en',
                                            'url': link, 'info': info, 'direct': False, 'debridonly': True})
                    except Exception:
                        continue
                except Exception:
                    failure = traceback.format_exc()
                    log_utils.log('YTSAM - Exception: \n' + str(failure))
                    continue

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('YTSAM - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
