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
2019/07/17: Optimized things a bit and reogranized cleanup locations in function
'''

import re
import traceback
import urllib
import urlparse

from resources.lib.modules import client, control, debrid, dom_parser2, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['ultrahdindir.com']
        self.base_link = 'https://ultrahdindir.com/'
        self.post_link = '/index.php?do=search'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('UltraHD - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title'].replace(':', '').lower()
            year = data['year']

            query = '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = urlparse.urljoin(self.base_link, self.post_link)

            post = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s' % urllib.quote_plus(query)

            timer = control.Time(start=True)

            r = client.request(url, post=post)

            r = client.parseDOM(r, 'div', attrs={'class': 'box-out margin'})
            r = [(dom_parser2.parse_dom(i, 'div', attrs={'class': 'news-title'})) for i in r if data['imdb'] in i]
            r = [(dom_parser2.parse_dom(i[0], 'a', req='href')) for i in r if i]
            r = [(i[0].attrs['href'], i[0].content) for i in r if i]

            hostDict = hostprDict + hostDict

            for item in r:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('UltraHDInDir - Timeout Reached')
                    break

                try:
                    name = item[0]
                    s = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', name)
                    s = s[0] if s else '0'
                    data = client.request(item[0])
                    data = dom_parser2.parse_dom(data, 'div', attrs={'id': 'r-content'})
                    data = re.findall('\s*<b><a href="(.+?)".+?</a></b>', data[0].content, re.DOTALL)
                    for url in data:
                        # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                        if timer.elapsed() > sc_timeout:
                            log_utils.log('UltraHDInDir - Timeout Reached')
                            break

                        url = client.replaceHTMLCodes(url)
                        url = url.encode('utf-8')

                        if 'turbobit' not in url:
                            continue
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if not valid:
                            continue

                        try:
                            qual = client.request(url)
                            quals = re.findall('span class="file-title" id="file-title">(.+?)</span', qual)
                            for quals in quals:
                                quality = source_utils.check_sd_url(quals)

                            info = []
                            if '3D' in name or '.3D.' in quals:
                                info.append('3D')
                                quality = '1080p'
                            if any(i in ['hevc', 'h265', 'x265'] for i in quals):
                                info.append('HEVC')

                            info = ' | '.join(info)

                            sources.append({'source': host, 'quality': quality, 'language': 'en',
                                            'url': url, 'info': info, 'direct': True, 'debridonly': False})

                        except Exception:
                            pass
                except Exception:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('UltraHD - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
