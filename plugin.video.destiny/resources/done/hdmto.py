# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 01-14-2019 by JewBMX in Scrubs.

import re,urllib,urlparse
from resources.lib.modules import cleantitle,client,proxy,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdm.to']
        self.base_link = 'https://hdm.to'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = cleantitle.geturl(title)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            scraper = cfscrape.create_scraper()
            url = '%s/%s/' % (self.base_link,url)
            r = scraper.get(url).content
            try:
                match = re.compile('<iframe.+?src="(.+?)"').findall(r)
                for url in match:
                    sources.append({'source': 'openload.co','quality': '1080p','language': 'en','url': url,'direct': False,'debridonly': False}) 
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url

