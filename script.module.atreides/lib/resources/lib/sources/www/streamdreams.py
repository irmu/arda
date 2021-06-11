# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @shellc0de wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2019/5/28: Fixed. Site changed the search again
'''

import re
import urlparse
import requests
import traceback

from resources.lib.modules import cleantitle, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['streamdreams.org']
        self.base_link = 'https://streamdreams.org'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search.replace(':', ' ').replace(' ', '+'))
            headers = {'Referer': url, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            r = requests.get(url, headers=headers).content
            Yourmouth = re.compile('<div class="thumbnail  same-height big-title-thumb".+?href="(.+?)"\stitle="(.+?)"', re.DOTALL).findall(r)
            for Mynuts, Mycock, in Yourmouth:
                if cleantitle.get(title) in cleantitle.get(Mycock):
                    if year in str(Mycock):
                        return Mynuts
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('StreamDreams - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            search = cleantitle.getsearch(tvshowtitle)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search.replace(':', ' ').replace(' ', '+'))
            headers = {'Referer': url, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            r = requests.get(url, headers=headers).content
            Yourmouth = re.compile('<div class="thumbnail  same-height big-title-thumb".+?href="(.+?)"\stitle="(.+?)"', re.DOTALL).findall(r)
            for Mynuts, Mycock, in Yourmouth:
                if cleantitle.get(tvshowtitle) in cleantitle.get(Mycock):
                    if year in str(Mycock):
                        return Mynuts
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('StreamDreams - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + '?session=%s&episode=%s' % (season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('StreamDreams - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []
            if url is None:
                return sources

            hostDict = hostprDict + hostDict
            headers = {'Referer': url, 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}

            timer = control.Time(start=True)

            r = requests.get(url, headers=headers).content
            links = re.compile("data-href='(.+?)'\s+data", re.DOTALL).findall(r)
            for link in links:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('StreamDreams - Timeout Reached')
                    break

                if 'BDRip' in link:
                    quality = '720p'
                elif 'HD' in link:
                    quality = '720p'
                else:
                    quality = 'SD'

                info = source_utils.get_release_quality(url)
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].split('.')[0].title()
                valid, host = source_utils.is_host_valid(link, hostDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('StreamDreams - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
