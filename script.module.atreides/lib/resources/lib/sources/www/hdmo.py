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
2019/6/16: Initial scraper by sc
'''

import re
import urlparse
import traceback
import requests

from resources.lib.modules import cleantitle, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['hdmo.tv']
        self.base_link = 'https://hdmo.tv'
        self.search_link = '/?s=%s'
        self.ajax_link = '/wp-admin/admin-ajax.php'
        self.shellscraper = requests.Session()
        self.shell_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'Referer': self.base_link
        }

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search.replace(':', ' ').replace(' ', '+'))
            r = self.shellscraper.get(url, headers=self.shell_headers).content
            movie_scrape = re.compile('<div class="title".+?href="(.+?)">(.+?)</a>.+?class="year">(.+?)</span>', re.DOTALL).findall(r)
            for movie_url, movie_title, movie_year in movie_scrape:
                if cleantitle.get(title) in cleantitle.get(movie_title):
                    if year in str(movie_year):
                        return movie_url
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('HDMO - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            search = cleantitle.getsearch(tvshowtitle)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url % (search.replace(':', ' ').replace(' ', '+'))
            r = self.shellscraper.get(url, headers=self.shell_headers).content
            tv_scrape = re.compile('<div class="title".+?href="(.+?)">(.+?)</a>.+?class="year">(.+?)</span>', re.DOTALL).findall(r)
            for tv_url, tv_title, tv_year in tv_scrape:
                if cleantitle.get(tvshowtitle) in cleantitle.get(tv_title):
                    if year in str(tv_year):
                        return tv_url
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('HDMO - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url[:-1]
            url = url.replace('/tvshows/', '/episodes/')
            url = url + '-%sx%s' % (season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('HDMO - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            timer = control.Time(start=True)

            r = self.shellscraper.get(url, headers=self.shell_headers).content
            regex = re.compile("data-type='(.+?)' data-post='(.+?)' data-nume='(\d+)'><i class='icon-play3'></i><span class='title'>(.+?)</span>", re.DOTALL).findall(r)
            for data_type, post, nume, quality in regex:

                cust_headers = {
                    'Host': 'hdmo.tv',
                    'Accept': '*/*',
                    'Origin': 'https://hdmo.tv',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                    'Referer': url,
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9'
                }

                post_link = urlparse.urljoin(self.base_link, self.ajax_link)
                payload = {'action': 'doo_player_ajax', 'post': post, 'nume': nume, 'type': data_type}
                suck_my_nuts = self.shellscraper.post(post_link, headers=cust_headers, data=payload)

                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('HDMO - Timeout Reached')
                    return sources

                copy_n_paste_bitches = suck_my_nuts.content
                links = re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(copy_n_paste_bitches)
                for link in links:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('HDMO - Timeout Reached')
                        break

                    '''
                    Testing this out still. Not sure if it will stay 1080p or change it to 720p.
                    '''
                    if 'HD' in quality:
                        quality = '1080p'
                    elif 'CAM' in quality:
                        quality = 'CAM'
                    else:
                        quality = 'SD'

                    valid, host = source_utils.is_host_valid(link, hostDict)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('HDMO - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
