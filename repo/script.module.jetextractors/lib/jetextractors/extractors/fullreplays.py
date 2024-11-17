# Whoever wrote this: do NOT call xbmc or resolveurl functions in Jetextractors
import sys
import xbmcgui
from bs4 import BeautifulSoup as bs
from requests.sessions import Session
from ..models import *

class FullReplays(JetExtractor):
    domains = ["www.fullreplays.com"]
    name = "FullReplays"
    
    def __init__(self):
        self.base_url = f"https://{self.domains[0]}"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        self.headers = {
            'User-Agent': self.user_agent,
            'Referer': self.base_url
        }
        self.session = Session()
        self.session.headers = self.headers

    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = [JetItem("Links may take several seconds to populate!", links=[])]
        if self.progress_init(progress, items):
            return items
        
        if params is None:
            page = self.base_url
        else:
            page = params["page"]
        response = self.session.get(page).text
        soup = (bs(response, 'html.parser'))
        row = soup.find(class_='row vlog-posts row-eq-height')
        for article in row.find_all('article'):
            title = article.h2.text
            link = article.a['href']
            thumbnail = article.a.img['src']
            items.append(JetItem(title, links=[JetLink(link, links=True)], icon=thumbnail))
        pagination = soup.find(class_='next page-numbers')
        if pagination:
            next_page = pagination['href']
            items.append(JetItem("[COLORyellow]Next Page[/COLOR]", links=[], params={"page": next_page}))
        return items
    
    
    def get_links(self, url: JetLink) -> List[JetLink]:
        links = []
        response = self.session.get(url.address).text
        soup = bs(response, 'html.parser')
        sources = soup.find_all(class_='frc-sources-wrap')
        for source in sources:
            host = source.find(class_='frc-vid-label').text.lower()
            for button in source.find_all(class_='vlog-button'):               
                title = f'{button.text.strip()} - {host.capitalize()}'
                # link = button['data-sc']
                try :
                    link = button['data-sc']
                except :
                    continue
                    
                if 'hoolights.com' in link:
                    continue                   
                if 'youtube.com' in link:
                    continue
                    
                links.append([title, link])
        if links:
            link = self.get_multilink(links)
            if not link:
                sys.exit()
            title, link = link
            if 'fviplions' in link:
                from resolveurl.plugins.filelions import FileLionsResolver
                splitted = link.split('/')
                link = FileLionsResolver().get_media_url(splitted[2], splitted[-1])
                if not link:
                    sys.exit()
                
                return [JetLink(link, name=title, direct=True)]
            if 'tapenoads' in link or 'tapeantiads' in link:
               from resolveurl.plugins.streamtape import StreamTapeResolver
               resolver = StreamTapeResolver()
               splitted = link.split('/')
               link = resolver.get_media_url(splitted[2], splitted[4])
               if not link:
                   sys.exit()
               return [JetLink(link, name=title, direct=True)]
            return [JetLink(link, name=title, resolveurl=True)]
    
    def get_multilink(self, lists):
        if len(lists) == 1:
            return lists[0]
        labels = [i[0] for i in lists]
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Choose a Link', labels)
        if ret == -1:
           return ''
        return lists[ret]
        