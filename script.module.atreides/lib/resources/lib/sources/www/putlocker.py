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

'''
2019/4/17: Readded this one, fix by SC
2019/5/13: Removed cfscrape, not needed atm. Using a client req seems consistent after testing
'''

import re
import traceback

from resources.lib.modules import client, control, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['putlockers.movie', 'putlockerr.is']
        self.base_link = 'https://putlockerr.is'
        self.search_link = '/embed/%s/'
        # self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + '/%s-%s/' % (season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}

            timer = control.Time(start=True)

            r = client.request(url, headers=headers)
            try:
                match = re.compile('<iframe src="(.+?)://(.+?)/(.+?)"').findall(r)
                for http, host, url in match:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('PutLocker - Timeout Reached')
                        break

                    url = '%s://%s/%s' % (http, host, url)
                    sources.append({'source': host, 'quality': 'HD', 'language': 'en',
                                    'url': url, 'direct': False, 'debridonly': False})
            except Exception:
                return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
