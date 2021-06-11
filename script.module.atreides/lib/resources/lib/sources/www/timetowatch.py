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
2019/07/06: Initial
'''

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cfscrape, cleantitle, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['timetowatch.video']
        self.base_link = 'https://www.timetowatch.video'
        self.search_link = '/?s=%s&3mh1=#'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = title.replace('\'', '').replace(',', '').replace('-', '').replace(':', '')
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('TimeToWatch - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url == None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']
            year = data['year']

            query = title.lower()
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            timer = control.Time(start=True)

            r = self.scraper.get(url).content
            match = re.findall('<div data-movie-id=.+?href="(.+?)".+?oldtitle="(.+?)".+?div class="jt-info".+?release-year/(.+?)/', r, re.DOTALL)
            items = []

            for url, name, r_year in match:
                name = name.replace('&#8230', ' ').replace('&#038', ' ').replace('&#8217', ' ').replace('...', ' ')
                if cleantitle.get(name).lower() in cleantitle.get(title).lower():
                    if r_year in year:
                        items += [(name, url)]

            hostDict = hostprDict + hostDict

            for item in items:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('TimeToWatch - Timeout Reached')
                    break

                url = item[1]
                html = self.scraper.get(url).content

                try:
                    links = re.findall('id="linkplayer.+?href="(.+?)"', html, re.DOTALL)
                    for link in links:
                        quality, info = source_utils.get_release_quality(link, url)
                        valid, host = source_utils.is_host_valid(link, hostDict)
                        if not valid:
                            continue
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
                except Exception:
                    pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('TimeToWatch - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
