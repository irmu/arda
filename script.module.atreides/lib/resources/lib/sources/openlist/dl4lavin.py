# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import client, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['openlist']
        self.domains = ['dl4.lavinmovie.net']
        self.base_link = 'http://dl4.lavinmovie.net/'
        self.search_link = '/movie/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = '%s.%s' % (title, year)
            title = urllib.quote_plus(title).replace('+', '.')
            url = {'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DL4.LAVINMOVIE - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            year = data['year']
            url = self.base_link + self.search_link % (year)

            timer = control.Time(start=True)

            html = client.request(url, headers=headers)
            if html is None:
                return sources

            # this method guarantees only results matching our formatted title get pulled out of the html
            regex_string = r'<tr><td class="link"><a href="{0}(.+?)"'.format(title)
            results = re.compile(regex_string).findall(html)
            for link in results:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('DL4Lavin - Timeout Reached')
                    break

                if 'Trailer' in link:
                    continue
                if 'Dubbed' in link:
                    continue
                url = self.base_link + self.search_link % year + title + link

                quality = source_utils.check_sd_url(url)
                sources.append({'source': 'Direct', 'quality': quality, 'language': 'en',
                                'url': url, 'direct': True, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DL4.LAVINMOVIE - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
