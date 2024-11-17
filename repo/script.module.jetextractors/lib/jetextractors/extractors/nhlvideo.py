import requests
from bs4 import BeautifulSoup as bs
import xbmc
from ..models import *


class NhlVideo(JetExtractor):
    domains = ["inhlvideo.com"]
    name = "NhlVideo"

    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = []
        if self.progress_init(progress, items):
            return items
        
        base_url = f"https://{self.domains[0]}"
        if params is not None:
            base_url += f"/page/{params['page']}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(base_url, headers=headers, timeout=self.timeout).text
        soup = (bs(r, 'html.parser'))
        matches = soup.find_all(class_='excerpt')
        for match in matches:
            if self.progress_update(progress, match.h2.text):
                return items
            xbmc.sleep(250)
            title = match.h2.text
            link = match.a['href']
            thumbnail = match.img['data-src']
            items.append(JetItem(title, links=[JetLink(link, links=True)], icon=thumbnail))
        
        if params is not None:
            next_page = int(params['page']) + 1
        else:
            next_page = 2
        items.append(JetItem(f"[COLORyellow]Page {next_page}[/COLOR]", links=[], params={"page": next_page}))
        return items
    
    
    def get_links(self, url: JetLink) -> List[JetLink]:
        links = []
        title = ''
        link = ''
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url.address, headers=headers, timeout=10).text
        soup = bs(r, 'html.parser')
        for article in soup.find(class_='article-content').find_all('p'):
            a = article.find('a')
            if a:
                link = article.a['href'].replace(f'https://{self.domains[0]}/goto/', '')
                #link = f'{link}$$https://{self.domains[0]}'
                title = link.split('/')[2]
                links.append(JetLink(link, name=title, resolveurl=True))
        links.reverse()
        return links