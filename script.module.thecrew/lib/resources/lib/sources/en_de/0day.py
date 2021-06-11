# -*- coding: utf-8 -*-

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import re
import urllib
import urlparse
import traceback

from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['0dayreleases.com']
        self.base_link = 'https://0daywarez.biz'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
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
            return

    def sources(self, url, hostDict, hostprDict):

        try:
            sources = []

            if url is None:
                return sources

            if debrid.status() is False:
                raise Exception()

            hostDict = hostprDict + hostDict

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']


            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            scraper = cfscrape.create_scraper()

            r = scraper.get(url).content
            
            posts = client.parseDOM(r, 'h2', attrs={'class': 'entry-title'})
            posts = client.parseDOM(posts, 'a', ret='href')

            items = []

            for post in posts:
                try:
                    r = scraper.get(post).content
                    u = client.parseDOM(r, "div", attrs={"class": "entry-content"})
                    for s in u:
                        t = re.search('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', s)
                        t = t.groups()[0] if t else '0'
                        u = client.parseDOM(s, 'a', ret='href')
                        u = [(i.strip('/').split('/')[-1], i, t) for i in u]
                        items += u
                except Exception:
                    pass

            info = []

            for item in items:
                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name, flags=re.I)

                    if not cleantitle.get(t) == cleantitle.get(title):
                        raise Exception()

                    quality, info = source_utils.get_release_quality(name, item[1])
                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', item[2])[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                        size = '%.2f GB' % size
                        info.append(size)
                    except Exception:
                        pass
                    info = ' | '.join(info)

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

                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                except Exception:
                    pass

            return sources
        except Exception:
            return sources

    def resolve(self, url):
        return url
