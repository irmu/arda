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
import urllib
import urlparse
import traceback

from resources.lib.modules import client, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['openlist']
        self.domains = ['dl8.heyserver.in']
        self.base_link = 'http://dl8.heyserver.in'
        self.search_link = '/serial/%s/%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = urllib.quote(tvshowtitle)
            url = {'tvshowtitle': title}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DL8heySERVER - Exception: \n' + str(failure))
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
            log_utils.log('DL8heySERVER - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            hldr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            season = 'S%02d/' % int(data['season'])
            title = data['tvshowtitle']

            url = urlparse.urljoin(self.base_link, self.search_link % (title, season))
            url = url.replace('%20', '.')
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            results = client.request(url, headers=headers)
            if results is None:
                return sources

            results = re.compile('<a href="(.+?)"').findall(results)
            for dirlink in results:
                if dirlink.startswith('.') or dirlink.startswith('?'):
                    continue
                sublink = urlparse.urljoin(url, dirlink)

                if dirlink.endswith('/'):
                    subhtml = client.request(sublink, headers=headers)
                    subres = re.compile('<a href="(.+?)"').findall(subhtml)
                    for link in subres:
                        if link.startswith('.') or link.startswith('?'):
                            continue
                        if hldr in link:
                            link = urlparse.urljoin(sublink, link)
                            quality = source_utils.check_sd_url(link)
                            sources.append({'source': 'Direct', 'quality': quality, 'language': 'en',
                                            'url': link, 'direct': True, 'debridonly': False})
                else:
                    if hldr in dirlink:
                        link = urlparse.urljoin(sublink, dirlink)
                        quality = source_utils.check_sd_url(link)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en',
                                        'url': link, 'direct': True, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('DL8heySERVER - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
