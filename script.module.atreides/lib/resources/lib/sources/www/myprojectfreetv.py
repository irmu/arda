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

from resources.lib.modules import cleantitle, client, control, log_utils, proxy


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['my-project-free.tv']
        self.base_link = 'https://www8.project-free-tv.ag/'
        self.search_link = '/episode/%s-season-%s-episode-%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(tvshowtitle)
            url = clean_title
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyProjectFreeTV - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = url
            url = self.base_link + self.search_link % (tvshowtitle, int(season), int(episode))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyProjectFreeTV - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            timer = control.Time(start=True)

            r = client.request(url)
            try:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('MyProjectFreeTV - Timeout Reached')
                    return sources

                data = re.compile("callvalue\('.+?','.+?','(.+?)://(.+?)/(.+?)'\)", re.DOTALL).findall(r)
                for http, host, url in data:
                    url = '%s://%s/%s' % (http, host, url)
                    sources.append({
                        'source': host,
                        'quality': 'SD',
                        'language': 'en',
                        'url': url,
                        'direct': False,
                        'debridonly': False
                    })
            except Exception:
                pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyProjectFreeTV - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
