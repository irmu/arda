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
import urllib
import urlparse

from resources.lib.modules import cfscrape, cleantitle, client, control, debrid, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.domains = ['scene-rls.com', 'scene-rls.net']
        self.base_link = 'http://scene-rls.net'
        self.search_link = '/?s=%s&submit=Find'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SceneRls - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SceneRls - Exception: \n' + str(failure))
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
            log_utils.log('SceneRls - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        try:
            sources = []

            if url is None:
                return sources

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = '%sS%02dE%02d' % (data['year'], int(data['season']), int(
                data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s %s S%02dE%02d' % (
                data['tvshowtitle'],
                data['year'],
                int(data['season']),
                int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
                data['title'],
                data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            try:
                url = self.search_link % urllib.quote_plus(query)
                url = urlparse.urljoin(self.base_link, url)

                timer = control.Time(start=True)

                r = self.scraper.get(url).content

                posts = client.parseDOM(r, 'div', attrs={'class': 'post'})

                items = []
                dupes = []

                for post in posts:
                    # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                    if timer.elapsed() > sc_timeout:
                        log_utils.log('SceneRLS - Timeout Reached')
                        break

                    try:
                        t = client.parseDOM(post, 'a')[0]
                        t = re.sub('<.+?>|</.+?>', '', t)

                        x = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', t)
                        if not cleantitle.get(title) in cleantitle.get(x):
                            raise Exception()
                        y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', t)[-1].upper()
                        if not y == hdlr:
                            raise Exception()

                        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', t.upper())
                        fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                        fmt = [i.lower() for i in fmt]
                        # if not any(i in ['1080p', '720p'] for i in fmt): raise Exception()

                        if len(dupes) > 2:
                            raise Exception()
                        dupes += [x]

                        u = client.parseDOM(post, 'a', ret='href')[0]

                        r = self.scraper.get(u).content
                        u = client.parseDOM(r, 'a', ret='href')
                        u = [(i.strip('/').split('/')[-1], i) for i in u]
                        items += u
                    except Exception:
                        pass
            except Exception:
                pass

            for item in items:
                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name)

                    if not cleantitle.get(t) == cleantitle.get(title):
                        raise Exception()

                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()

                    if not y == hdlr:
                        raise Exception()

                    quality, info = source_utils.get_release_quality(name, item[1])

                    url = item[1]
                    if any(x in url for x in ['.rar', '.zip', '.iso']):
                        raise Exception()
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    if host not in hostDict:
                        raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    sources.append({'source': host, 'quality': quality, 'language': 'en',
                                    'url': url, 'info': info, 'direct': False, 'debridonly': True})
                except Exception:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('SceneRls - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
