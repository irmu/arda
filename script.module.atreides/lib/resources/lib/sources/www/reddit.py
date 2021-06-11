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

from resources.lib.modules import cleantitle, client, control, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['reddit.com']
        self.base_link = 'https://www.reddit.com/user/nbatman/m/streaming2/search?q=%s&restrict_sr=on'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            title = title.replace('-', '+')
            query = '%s+%s' % (title, year)
            url = self.base_link % query
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Reddit - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            timer = control.Time(start=True)

            r = client.request(url)
            try:
                match = re.compile(
                    'class="search-title may-blank" >(.+?)</a>.+?<span class="search-result-icon search-result-icon-external"></span><a href="(.+?)://(.+?)/(.+?)" class="search-link may-blank" >').findall(r)
                for info, http, host, ext in match:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('Reddit - Timeout Reached')
                        break

                    if '2160' in info:
                        quality = '4K'
                    elif '1080' in info:
                        quality = '1080p'
                    elif '720' in info:
                        quality = 'HD'
                    elif '480' in info:
                        quality = 'SD'
                    else:
                        quality = 'SD'

                    url = '%s://%s/%s' % (http, host, ext)
                    if 'google' in host:
                        host = 'GDrive'
                    if 'Google' in host:
                        host = 'GDrive'
                    if 'GOOGLE' in host:
                        host = 'GDrive'

                    sources.append({
                        'source': host,
                        'quality': quality,
                        'language': 'en',
                        'url': url,
                        'info': info,
                        'direct': False,
                        'debridonly': False
                    })
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('Reddit - Exception: \n' + str(failure))
                return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Reddit - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
