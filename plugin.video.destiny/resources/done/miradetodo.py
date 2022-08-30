# -*- coding: utf-8 -*-

'''
    DooFree Add-on
    Copyright (C) 2017 Mpie
'''


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['miradetodo.net']
        self.base_link = 'https://miradetodo.net'
        self.gk_url = self.base_link + '/stream/plugins/gkpluginsphp.php'
        self.search_link = '/?s=%s'
        self.episode_link = '/episodio/%s-%sx%s'
        self.tvshow_link = '/series/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            t = 'http://www.imdb.com/title/%s' % imdb
            t = client.request(t, headers={'Accept-Language': 'es-AR'})
            t = client.parseDOM(t, 'title')[0]
            t = re.sub('(?:\(|\s)\d{4}.+', '', t).strip().encode('utf-8')

            q = self.search_link % urllib.quote_plus(t)
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q)

            r = client.parseDOM(r, 'div', attrs = {'class': 'item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'class': 'tt'}), client.parseDOM(i, 'span', attrs = {'class': 'year'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [i[0] for i in r if cleantitle.get(t) == cleantitle.get(i[1]) and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            t = cleantitle.geturl(tvshowtitle)

            q = self.tvshow_link % t
            q = urlparse.urljoin(self.base_link, q)
            r = client.request(q, output='geturl')

            if not r:
                t = 'http://www.imdb.com/title/%s' % imdb
                t = client.request(t, headers={'Accept-Language': 'es-AR'})
                t = client.parseDOM(t, 'title')[0]
                t = re.sub('(?:\(|\s)\(TV Series.+', '', t).strip().encode('utf-8')

                q = self.search_link % urllib.quote_plus(t)
                q = urlparse.urljoin(self.base_link, q)

                r = client.request(q)

                r = client.parseDOM(r, 'div', attrs = {'class': 'item'})
                r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'span', attrs = {'class': 'tt'}), client.parseDOM(r, 'span', attrs = {'class': 'year'}))
                r = [(i[0], re.sub('(?:\(|\s)\('+year+'.+', '', i[1]).strip().encode('utf-8'), i[2]) for i in r if len(i[0]) > 0 and '/series/' in i[0] and len(i[1]) > 0 and len(i[2]) > 0]
                r = [i[0] for i in r if year == i[2]][0]

            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'url': r}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            show = data['url'].split('/')[4]
            r = urlparse.urljoin(self.base_link, self.episode_link % (show, season, episode))
            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            pass

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            r = urlparse.urljoin(self.base_link, url)

            result = client.request(r)

            f = client.parseDOM(result, 'div', attrs = {'class': 'movieplay'})

            if not f:
                f = client.parseDOM(result, 'div', attrs={'class': 'embed2'})
                f = client.parseDOM(f, 'div')

            f = client.parseDOM(f, 'iframe', ret='data-lazy-src')

            for u in f:
                try:
                    html = client.request(u)
                    fragment = client.parseDOM(html, 'nav', attrs={'class': 'nav'})

                    # movies
                    if fragment:
                        stream_url = client.parseDOM(fragment[0], 'a', ret='href')

                        for stream in stream_url:
                            if 'streamango' in stream:
                                html = client.request(stream)
                                url = client.parseDOM(html, 'iframe', ret='src')[0]
                                sources.append({'source': 'Streamango', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                            if 'ol.php' in stream:
                                html = client.request(stream)
                                url = client.parseDOM(html, 'iframe', ret='src')[0]
                                url = url.replace('embed', 'f')
                                sources.append({'source': 'Openload', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                            if 'cdnvi' in stream:
                                html = client.request(stream)
                                url = client.parseDOM(html, 'iframe', ret='src')[0]
                                sources.append({'source': 'Rapidvideo', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                            if 'your.php' in stream:
                                html = client.request(stream)
                                url = client.parseDOM(html, 'iframe', ret='src')[0]
                                sources.append({'source': 'Yourupload', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                            if 'fastplay.php' in stream:
                                html = client.request(stream)
                                url = client.parseDOM(html, 'iframe', ret='src')[0]
                                sources.append({'source': 'Fastplay', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    # series
                    else:
                        if 'streamango' in u:
                            html = client.request(u)
                            url = client.parseDOM(html, 'iframe', ret='src')[0]
                            sources.append({'source': 'Streamango', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                        if 'ol.php' in u:
                            html = client.request(u)
                            url = client.parseDOM(html, 'iframe', ret='src')[0]
                            url = url.replace('embed', 'f')
                            sources.append({'source': 'Openload', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                        if 'cdnvi' in u:
                            html = client.request(u)
                            url = client.parseDOM(html, 'iframe', ret='src')[0]
                            sources.append({'source': 'Rapidvideo', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                        if 'your.php' in u:
                            html = client.request(u)
                            url = client.parseDOM(html, 'iframe', ret='src')[0]
                            sources.append({'source': 'Yourupload', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                        if 'fastplay.php' in u:
                            html = client.request(u)
                            url = client.parseDOM(html, 'iframe', ret='src')[0]
                            sources.append({'source': 'Fastplay', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __get_amazon_links(self, html):
        sources = {}
        match = re.search('AmazonPlayer.*?file\s*:\s*"([^"]+)', html, re.DOTALL)
        if match:
            html = self._http_get(match.group(1), allow_redirect=False, method='HEAD', cache_limit=0)
            if html.startswith('http'):
                sources = {html: {'quality': QUALITIES.HD720, 'direct': True}}
        return sources

    def __get_gk_links2(self, html):
        sources = {}
        match = re.search('proxy\.link=([^"&]+)', html)
        if match:
            proxy_link = match.group(1)
            proxy_link = proxy_link.split('*', 1)[-1]
            if len(proxy_link) <= 224:
                vid_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY1, proxy_link)
            else:
                vid_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY2, proxy_link)

            if scraper_utils.get_direct_hostname(self, vid_url) == 'gvideo':
                for source in self._parse_gdocs(vid_url):
                    sources[source] = {'quality': scraper_utils.gv_get_quality(source), 'direct': True}
        return sources

    def __get_gk_links(self, html):
        sources = {}
        match = re.search('{link\s*:\s*"([^"]+)', html)
        if match:
            iframe_url = match.group(1)
            data = {'link': iframe_url}
            headers = {'Referer': iframe_url}
            html = self._http_get(self.gk_url, data=data, headers=headers, cache_limit=.5)
            js_data = scraper_utils.parse_json(html, self.gk_url)
            links = js_data.get('link', [])
            if isinstance(links, basestring):
                links = [{'link': links}]

            for link in links:
                stream_url = link['link']
                if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                    direct = True
                elif 'label' in link:
                    quality = scraper_utils.height_get_quality(link['label'])
                    direct = True
                else:
                    quality = QUALITIES.HIGH
                    direct = False
                sources[stream_url] = {'quality': quality, 'direct': direct}
        return sources


