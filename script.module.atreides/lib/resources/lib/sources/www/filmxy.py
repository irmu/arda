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
2019/10/04: Re-added this site, thx to shellc0de's work to keep it going. His notes retained below
'''

# 1/22/19 Fixed. Search was changed. Found a way around that.
# 5/24/19 Removed filter function, as its not needed anymore. Updated/tweaked regex
# to pull both iframes. Added some quality checking from source_utils.
# 6/12/19. fixed added cfscrape
# 7/8/19 FIXED! even though site has a captcha on the search link url now, was able to bypass
# it with a set of headers lol. Seems like site is mis-configured or captcha is not set up properly.
# SO IF UR READING THIS.....PLEASE KEEP THIS FIX PRIVATE. I really like this site, i don't need it
# copy n pasted everywhere, cause we will all be fucked with no links again
# 7/13/19 fixed again, had to use my backup fix. They closed the loophole i found. However now,
# we search thru their json file by first letter of the search title. Which ive never done before, but
# got her done. Enjoy the links, and please keep this fix private or just ask. This scraper is on its last leg.
# 7/23/19 fixed again. can't use the json file to search atm, but found another way using basically
# the same method previously, which i've never seen done before.
# 8/31/19 fixed. added .lower() to search title cause was switched to a lower case letter. also cf was turned on.
# 9/6/19 improved. started scraping the download links. Only the 1080's for now. May add the 720p's too next time.
# 10/11/19 fixed freeze up. site completly changed up html in movie scrape and also in link_bin (download links)

import re
import traceback
import urlparse

from resources.lib.modules import cfscrape, cleantitle, client, control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['filmxy.me', 'filmxy.one', 'filmxy.ws', 'filmxy.live']
        self.base_link = 'https://www.filmxy.nl'
        # self.json_search = 'https://static.filmxy.live/json/%s.json'
        self.list_search = '/movie-list/%s/'
        self.shellscrape = cfscrape.CloudflareScraper()
        self.shell_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Referer': self.base_link
        }

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search = cleantitle.getsearch(title.lower())
            url = urlparse.urljoin(self.base_link, self.list_search)
            url = url % (search[0])
            r = self.shellscrape.get(url, headers=self.shell_headers).content
            movie_scrape = re.compile('<a href="(.+?)"\srel="bookmark"\stitle="Permanent\sLink\sto\s(.+?\))').findall(r)
            # href=(.+?)rel=bookmark title="Permanent Link to (.+?)" target=
            for movie_url, movie_title in movie_scrape:
                # final_url = 'https://www.filmxy.live/?p=' + num_string
                if cleantitle.get(title) in cleantitle.get(movie_title):
                    if year in str(movie_title):
                        return movie_url
            return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FilmXY - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources
            # log_utils.log('Filmxy - Sources - url: ' + str(url))
            # PLEASE KEEP THIS FIX PRIVATE, THANKS.
            # cust_headers = {
            #     'Host': 'www.filmxy.live',
            #     'Connection': 'keep-alive',
            #     'Origin': 'https://www.filmxy.live',
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            #     'Accept': '*/*',
            #     'Referer': 'https://www.filmxy.live/',
            #     'Accept-Encoding': 'gzip, deflate',
            #     'Accept-Language': 'en-US,en;q=0.9'
            # }

            timer = control.Time(start=True)

            r = self.shellscrape.get(url, headers=self.shell_headers).content
            streams = re.compile('data-player="&lt;[A-Za-z]{6}\s[A-Za-z]{3}=&quot;(.+?)&quot;', re.DOTALL).findall(r)

            try:
                link_bin = re.compile('<div id="tab-download".+?<a href="(.+?)"', re.DOTALL).findall(r)[0]
                link_bin = link_bin.rstrip()
                r = self.shellscrape.get(link_bin, headers=self.shell_headers).content

                dlinks1080 = client.parseDOM(r, 'div', attrs={'class': 'link-panel row'})[1]
                dlinks1080 = client.parseDOM(dlinks1080, 'a', ret='href')

                for links in dlinks1080:
                    if any(x in links for x in ['mirrorace', 'sendit']):
                        continue
                    host = links.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].lower()
                    sources.append({'source': host, 'quality': '1080p', 'language': 'en',
                                    'url': links, 'direct': False, 'debridonly': False})
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('300MBFilms - Timeout Reached')
                        break
            except Exception:
                pass

            for link in streams:
                quality = source_utils.check_sd_url(link)
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].lower()
                '''
                Now source_utils can't strip quality on some of these links. It will drop them
                down to SD. So i say we try this.
                '''
                if quality == 'SD':
                    quality = 'HD'
                sources.append({'source': host, 'quality': quality, 'language': 'en',
                                'url': link, 'direct': False, 'debridonly': False})
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('300MBFilms - Timeout Reached')
                    break
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FilmXY - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
