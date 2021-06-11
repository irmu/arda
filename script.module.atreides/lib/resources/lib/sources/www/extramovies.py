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
2019/07/06: Scraper updated.
'''

import base64
import re
import traceback
import urllib
import urlparse
import requests

from resources.lib.modules import cfscrape, cleantitle, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 0
        self.source = ['www']
        self.domains = ['extramovies.trade', 'extramovies.host', 'extramovies.guru']
        self.base_link = 'http://extramovies.wiki'
        self.search_link = '/?s=%s'
        self.User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ExtraMovie - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ExtraMovie - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ExtraMovie - Exception: \n' + str(failure))
            return

    def filter_host(self, host):
        if host not in ['openload.co', 'yourupload.com', 'streamango.com', 'rapidvideo.com', 'uptobox.com', 'clicknupload.org']:
            return False
        return True

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            hostDict = hostDict + hostprDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query(title)))
            headers = {'User-Agent': self.User_Agent}

            timer = control.Time(start=True)

            if 'tvshowtitle' in data:
                scraper = cfscrape.create_scraper()
                html = scraper.get(url, headers=headers).content

                match = re.compile('class="post-item.+?href="(.+?)" title="(.+?)"', re.DOTALL).findall(html)
                for url, item_name in match:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('ExtraMovies - Timeout Reached')
                        break

                    if cleantitle.getsearch(title).lower() in cleantitle.getsearch(item_name).lower():
                        season_url = '%02d' % int(data['season'])
                        episode_url = '%02d' % int(data['episode'])
                        sea_epi = 'S%sE%s' % (season_url, episode_url)

                        result = scraper.get(url, headers=headers, timeout=5).content
                        Regex = re.compile('href="(.+?)"', re.DOTALL).findall(result)
                        for ep_url in Regex:
                            if sea_epi in ep_url:
                                quality = source_utils.check_sd_url(ep_url)
                                sources.append({'source': 'CDN', 'quality': quality, 'language': 'en', 'url': ep_url, 'direct': False, 'debridonly': False})
            else:
                html = requests.get(url, headers=headers).content
                match = re.compile('<div class="thumbnail".+?href="(.+?)" title="(.+?)"', re.DOTALL).findall(html)

                for url, item_name in match:
                    if cleantitle.getsearch(title).lower() in cleantitle.getsearch(item_name).lower():
                        quality = source_utils.check_sd_url(url)

                        result = requests.get(url, headers=headers, timeout=10).content
                        Regex = re.compile('href="/download.php.+?link=(.+?)"', re.DOTALL).findall(result)

                        for link in Regex:
                            if 'server=' not in link:
                                try:
                                    link = base64.b64decode(link)
                                except Exception:
                                    pass
                                valid, host = source_utils.is_host_valid(link, hostDict)
                                if not valid or not self.filter_host(host):
                                    continue
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('ExtraMovie - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
