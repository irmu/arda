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
2019/06/12: Adjusted regex in links to remove the trailer link that was sneaking in.
2019/07/06: Added valid host check since already pulled
'''

import re
import urlparse
import requests
import traceback

from resources.lib.modules import cleantitle, control, source_utils, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['iwannawatch.is']
        self.base_link = 'https://www.iwannawatch.is'
        self.search_link = '/%s-%s-full-movie/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('IwannaWatch - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []
            hostDict = hostprDict + hostDict

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

            timer = control.Time(start=True)

            r = requests.get(url, headers=headers).content
            quality_check = re.compile('class="quality">(.+?)<').findall(r)

            for quality in quality_check:
                if 'HD' in quality:
                    quality = '720p'
                else:
                    quality = 'SD'

            links = re.compile('li class=.+?data-target="\W[A-Za-z]+\d"\sdata-href="(.+?)"').findall(r)
            for url in links:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('IWannaWatch - Timeout Reached')
                    break

                valid, host = source_utils.is_host_valid(url, hostDict)
                if not valid:
                    continue
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('IwannaWatch - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
