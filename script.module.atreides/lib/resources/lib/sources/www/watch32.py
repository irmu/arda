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

from resources.lib.modules import cleantitle, client, control, dom_parser2, jsunpack, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['watch32hd.co']
        self.base_link = 'https://watch32hd.co'
        self.search_link = '/results?q=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Watch32 - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['title']

            hdlr = data['year']

            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', title)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            timer = control.Time(start=True)

            r = client.request(url)

            posts = client.parseDOM(r, 'div', attrs={'class': 'video_title'})

            items = []

            for post in posts:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('Watch32 - Timeout Reached')
                    break

                try:
                    data = dom_parser2.parse_dom(post, 'a', req=['href', 'title'])[0]
                    t = data.content
                    y = re.findall('\((\d{4})\)', data.attrs['title'])[0]
                    qual = data.attrs['title'].split('-')[1]
                    link = data.attrs['href']

                    if not cleantitle.get(t) == cleantitle.get(title):
                        raise Exception()
                    if not y == hdlr:
                        raise Exception()

                    items += [(link, qual)]

                except Exception:
                    pass
            for item in items:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('Watch32 - Timeout Reached')
                    break

                try:
                    r = client.request(item[0]) if item[0].startswith('http') else client.request(urlparse.urljoin(self.base_link, item[0]))

                    qual = client.parseDOM(r, 'h1')[0]
                    # quality = source_utils.get_release_quality(item[1], qual)[0]

                    url = re.findall('''frame_url\s*=\s*["']([^']+)['"]\;''', r, re.DOTALL)[0]
                    url = url if url.startswith('http') else urlparse.urljoin('https://', url)

                    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}

                    postID = url.split('/embed/')[1]
                    post_link = 'https://vidlink.org/embed/update_views'
                    payload = {'postID': postID}
                    headers = ua
                    headers['X-Requested-With'] = 'XMLHttpRequest'
                    headers['Referer'] = url

                    ihtml = client.request(post_link, post=payload, headers=headers)
                    linkcode = jsunpack.unpack(ihtml).replace('\\', '')
                    try:
                        extra_link = re.findall(r'var oploadID="(.+?)"', linkcode)[0]
                        oload = 'https://openload.co/embed/' + extra_link
                        sources.append({'source': 'openload.co', 'quality': '1080p', 'language': 'en', 'url': oload, 'direct': False, 'debridonly': False})

                    except Exception:
                        pass

                    give_me = re.findall(r'var file1="(.+?)"', linkcode)[0]
                    stream_link = give_me.split('/pl/')[0]
                    headers = {'Referer': 'https://vidlink.org/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
                    r = client.request(give_me, headers=headers)

                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('Watch32 - Timeout Reached')
                        break

                    my_links = re.findall(r'[A-Z]{10}=\d+x(\d+)\W[A-Z]+=\"\w+\"\s+\/(.+?)\.', r)
                    for quality_bitches, link in my_links:

                        if '1080' in quality_bitches:
                            quality = '1080p'
                        elif '720' in quality_bitches:
                            quality = '720p'
                        elif '480' in quality_bitches:
                            quality = 'SD'
                        elif '360' in quality_bitches:
                            quality = 'SD'
                        else:
                            quality = 'SD'

                        final = stream_link + '/' + link + '.m3u8'
                        sources.append({'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': final, 'direct': True, 'debridonly': False})

                except Exception:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Watch32 - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
