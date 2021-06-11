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
        self.domains = ['dl3.f2m.io']
        self.base_link = 'http://dl3.f2m.io/'
        self.search_link = 'serial/%s/%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = urllib.quote(tvshowtitle)
            url = {'tvshowtitle': title}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DL3F2M.IO - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['season'], url['episode'] = season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DL3F2M.IO - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            hldr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            season = 'S%02d/' % int(data['season'])
            title = data['tvshowtitle']

            '''
            Check for season directory, no need for extra checks. Path is there or it's not
            '''
            url = urlparse.urljoin(self.base_link, self.search_link % (title, season))

            timer = control.Time(start=True)

            results = client.request(url, headers=headers)
            if results is None:
                return sources

            results = re.compile('<a href="(.+?)"').findall(results)
            for link in results:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('DL3F2M - Timeout Reached')
                    break

                if link.startswith('.') or link.startswith('?'):
                    continue
                if hldr in link:
                    link = urlparse.urljoin(url, link)
                    quality = source_utils.check_sd_url(link)
                    sources.append({'source': 'Direct', 'quality': quality, 'language': 'en',
                                    'url': link, 'direct': True, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DL3F2M.IO - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
