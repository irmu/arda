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
2019/04/17: Readded this one, fix by SC
2019/07/06: Minor code updates
2019/11/04: Domain update
'''

import re
import urlparse
import traceback

from resources.lib.modules import client, cleantitle, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['coolmoviezone.online', 'coolmoviezone.co']
        self.base_link = 'https://coolmoviezone.cc'
        self.search_link = '/%s-%s'
        # self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CoolMovieZone - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        hostDict = hostprDict + hostDict
        try:
            sources = []
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

            timer = control.Time(start=True)

            r = client.request(url, headers=headers)
            if r is None:
                return sources
            match = re.findall('<td align="center"><strong><a href="(.+?)"', r, re.DOTALL)
            for url in match:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('CoolMovieZone - Timeout Reached')
                    break

                quality = source_utils.check_sd_url(url)
                valid, host = source_utils.is_host_valid(url, hostDict)
                if not valid:
                    continue
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CoolMovieZone - Exception: \n' + str(failure))
            return
        return sources

    def resolve(self, url):
        return url
