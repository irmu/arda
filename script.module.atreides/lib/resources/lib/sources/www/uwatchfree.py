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
2019/4/17: fix by SC
'''

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cfscrape, client, control, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['uwatchfree.sx']
        self.base_link = 'https://www.uwatchfree.sx'
        self.search_link = '/?s=%s&submit=Search'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('UWatchFree - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        sources = []
        hostDict = hostprDict + hostDict
        try:
            if url is None:
                return
            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            imdb = urldata['imdb']
            title = urldata['title']
            year = urldata['year']

            search = imdb.lower()
            url = urlparse.urljoin(self.base_link, self.search_link % (search.replace(' ', '+')))

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}

            timer = control.Time(start=True)

            request = self.scraper.get(url).content

            regex = re.compile('<h2\s+\w{5}="\w{5}-\w{5}"><\w\shref=(.+?)\stitle="(.+?)"', re.DOTALL).findall(request)
            for Aurora, Atreides in regex:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('UWatchFree - Timeout Reached')
                    break

                if title.lower() in Atreides.lower():
                    if year in str(Atreides):
                        if 'hindi' in Atreides.lower():
                            continue
                        r = client.request(Aurora, headers=headers)

                        links = re.compile(
                            '<h2\s+c\w{4}\W"d\w{7}-l\w{4}"><a\s\w{4}=(.+?)\s[a-z]{6}\W', re.DOTALL).findall(r)

                        for link in links:
                            sources.append({'source': 'Direct', 'quality': '720p', 'language': 'en',
                                            'url': link, 'direct': True, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('UWatchFree - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
