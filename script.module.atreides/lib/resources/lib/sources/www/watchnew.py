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
2019/6/16: fixed by Shellc0de.
'''

import re
import urllib
import urlparse
import traceback

from resources.lib.modules import cleantitle, cfscrape, client, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['watchnewmovienet.com']
        self.base_link = 'http://watchnewmovienet.com'
        self.search_link = '/search/%s/feed/rss2/'
        self.cfscrape = cfscrape.create_scraper()
        self.shell_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'Referer': self.base_link
        }

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchNEW - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchNEW - Exception: \n' + str(failure))
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
            log_utils.log('WatchNEW - Exception: \n' + str(failure))
            return

    def searchShow(self, title, season):
        try:
            sea = '%s season %d' % (title, int(season))
            query = self.search_link % urllib.quote_plus(cleantitle.getsearch(sea))
            url = urlparse.urljoin(self.base_link, query)
            r = self.cfscrape.get(url, headers=self.shell_headers).content
            r = client.parseDOM(r, 'item')
            r = [(client.parseDOM(i, 'title')[0], i) for i in r if i]
            r = [i[1] for i in r if sea.lower() in i[0].replace('  ', ' ').lower()]
            links = re.findall('''<h4>(EP\d+)</h4>.+?src="(.+?)"''', r[0], re.I | re.DOTALL)
            links = [(i[0], i[1].lstrip()) for i in links if i]
            return links
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchNEW - Exception: \n' + str(failure))
            return

    def searchMovie(self, title, year):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.getsearch(title+' '+year))
            url = urlparse.urljoin(self.base_link, query)
            r = self.cfscrape.get(url, headers=self.shell_headers).content
            r = client.parseDOM(r, 'item')
            r = [(client.parseDOM(i, 'title')[0], i) for i in r if i]
            r = [i[1] for i in r if cleantitle.get(title) in cleantitle.get(i[0]) and year in i[0]]
            return r[0]
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchNEW - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            try:
                if 'tvshowtitle' in data:
                    epi = 'EP%d' % int(data['episode'])
                    links = self.searchShow(data['tvshowtitle'], data['season'])
                    url = [i[1] for i in links if epi.lower() == i[0].lower()]
                else:

                    url = self.searchMovie(data['title'], data['year'])

                    try:
                        url = re.findall('''src=['"]\s*(.+?)['"]''', url, re.DOTALL)
                    except Exception:
                        url = re.compile('<iframe id="advanced_iframe.+?src="(.+?)"', re.DOTALL).findall(url)
            except Exception:
                pass

            timer = control.Time(start=True)

            for u in url:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('WatchNew - Timeout Reached')
                    break

                u = u.lstrip()
                if 'watchnewmovienet' in u:
                    continue
                # vidnode section not tested. havent found a vidnode link on the site yet.
                elif 'vidnode' in u:
                    headers = {'Host': 'vidnode.net',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                               'Upgrade-Insecure-Requests': '1',
                               'Accept-Language': 'en-US,en;q=0.9'}
                    r = client.request(u, headers=headers)
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('WatchNew - Timeout Reached')
                        break

                    links = re.findall('''\{file:\s*['"]([^'"]+).*?label:\s*['"](\d+\s*P)['"]''', r, re.DOTALL | re.I)
                    for u, qual in links:
                        quality, info = source_utils.get_release_quality(qual, u)
                        url = u
                        sources.append({'source': 'cdn', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                else:
                    '''
                    entervideo link gets processed here. Our resolver will handle the link, least for now. Makes no since to chase
                    the direct link when they pussy foot around and mis-label the quality of their links which are all pretty
                    much SD.
                    '''
                    host = u.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].lower()
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': u, 'direct': False, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchNEW - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
