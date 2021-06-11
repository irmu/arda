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
2019/6/5: Adjusted to pull more links
'''

import re
import traceback
import urlparse

from resources.lib.modules import cleantitle, client, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['watch-series.ru']
        self.base_link = 'https://watch-series.live'
        self.search_link = '/series/%s-season-%s-episode-%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchSeriesRU - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = url
            url = self.base_link + self.search_link % (tvshowtitle, season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchSeriesRU - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        sources = []
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

            timer = control.Time(start=True)

            r = client.request(url, headers=headers)
            match = re.compile('data-video="(.+?)">').findall(r)
            for url in match:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('WatchSeriesRU - Timeout Reached')
                    break

                if 'vidcloud' in url:
                    url = urlparse.urljoin('https:', url)
                    r = client.request(url, headers=headers)
                    regex = re.compile("file: '(.+?)'").findall(r)
                    for direct_links in regex:
                        sources.append({'source': 'cdn', 'quality': 'SD', 'language': 'en', 'url': direct_links, 'direct': False, 'debridonly': False})

                else:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchSeriesRU - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
