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
2019/5/28: Re-add with new url. Credit to host505 for the url
2019/5/30: magnetdl came back i guess...
'''
import re
import traceback
import urllib
import urlparse

from resources.lib.modules import cleantitle, client, control, debrid, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['magnet']
        self.domains = ['magnetdl.com']
        self.base_link = 'https://torrentquest.com'
        self.search_link = '/%s/%s'
        self.min_seeders = int(control.setting('torrent.min.seeders'))

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status(True) is False:
            return

        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('TorrentQuest - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status(True) is False:
            return

        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('TorrentQuest - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status(True) is False:
            return

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
            log_utils.log('TorrentQuest - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        sources = []
        try:
            if debrid.status() is False:
                raise Exception()

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            stype = 'TV' if 'tvshowtitle' in data else 'Movie'
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'],
                int(data['season']),
                int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
                data['title'],
                data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|<|>|\|)', ' ', query)

            '''
            Have to clean the titles up completely, as they remove characters like : and so on, and replace spaces with dashes
            '''
            url = urlparse.urljoin(self.base_link, self.search_link % (query[0].lower(), cleantitle.geturl(query)))

            timer = control.Time(start=True)

            html = client.request(url)
            html = html.replace('&nbsp;', ' ')
            try:
                results = client.parseDOM(html, 'tbody')[0]
            except Exception:
                return sources

            rows = re.findall('<tr>(.+?)</tr>', results, re.DOTALL)
            if rows is None:
                return sources

            for entry in rows:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('TorrentQuest - Timeout Reached')
                    break

                try:
                    '''
                    Test category. If it fails, no need to parse this line.
                    '''
                    try:
                        if stype == 'TV':
                            verify = re.findall('<td class="t5">(.+?)</td>', entry, re.DOTALL)[0]
                        else:
                            verify = re.findall('<td class="t2">(.+?)</td>', entry, re.DOTALL)[0]
                    except Exception:
                        continue
                    try:
                        name = re.findall('<td class="n">(.+?)</td>', entry, re.DOTALL)[0]
                        name = re.findall('title="(.+?)"', name, re.DOTALL)[0]
                        name = client.replaceHTMLCodes(name)
                        if not cleantitle.get(title) in cleantitle.get(name):
                            continue
                    except Exception:
                        continue
                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()
                    if not y == hdlr:
                        continue

                    try:
                        seeders = int(re.findall('<td class="s">(.+?)</td>', entry, re.DOTALL)[0])
                    except Exception:
                        continue
                    if self.min_seeders > seeders:
                        continue

                    try:
                        link = 'magnet:%s' % (re.findall('href="magnet:(.+?)"', entry, re.DOTALL)[0])
                        link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                    except Exception:
                        continue

                    quality, info = source_utils.get_release_quality(name, name)

                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', entry)[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                        size = '%.2f GB' % size
                        info.append(size)
                    except Exception:
                        pass

                    info = ' | '.join(info)
                    sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en',
                                    'url': link, 'info': info, 'direct': False, 'debridonly': True})
                except Exception:
                    continue

            check = [i for i in sources if not i['quality'] == 'CAM']
            if check:
                sources = check

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('TorrentQuest - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
