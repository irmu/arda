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
2019/07/17: Added with my own tweaks and enhancements. Pulled from other Covenant/Placenta forks.
'''

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import client, control, debrid, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['magnet']
        self.domains = ['yifyddl.movie']
        self.base_link = 'https://yifyddl.movie/'
        self.search_link = '/movie/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status(True) is False:
            return

        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('YifiDDL - Exception: \n' + str(failure))
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
            url = urlparse.urljoin(self.base_link, url).replace('%20', '-')

            timer = control.Time(start=True)

            html = client.request(url)
            if html is None:
                return sources

            try:
                results = client.parseDOM(html, 'div', attrs={'class': 'ava1'})
                if results is None:
                    return sources
            except:
                return sources

            for torrent in results:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('YifiDDL - Timeout Reached')
                    return sources

                link = re.findall('a data-torrent-id=".+?" href="(magnet:.+?)" class=".+?" title="(.+?)"', torrent, re.DOTALL)
                for link, name in link:
                    link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                    if link in str(sources):
                        continue

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

                    sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': True})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('YifiDDL - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
