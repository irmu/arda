import requests
from bs4 import BeautifulSoup as bs
from typing import List
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class MlbLive(Extractor):
    domains = ["mlblive.net"]
    name = "MlbLive"

    def get_games(self) -> List[Game]:
        games = []
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(base_url, headers=headers).text
        soup = (bs(r, 'html.parser'))
        matches = soup.find_all(class_='short_item block_elem')
        for match in matches:
            name = match.h3.a.text.replace('Full Game Replay ', '').rstrip(' NHL')
            link = f"{base_url}{match.a['href']}"
            icon = f"{base_url}{match.a.img['src']}"
            games.append(Game(name, links=[Link(link, is_links=True)], icon=icon))
        games.append(Game("[COLORyellow]Page 2[/COLOR]", page=2))
        return games
    
    def get_games_page(self, page) -> List[Game]:
        games = []
        base_url = f"https://{self.domains[0]}"
        url = f"{base_url}?page{page}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url, headers=headers).text
        soup = (bs(r, 'html.parser'))
        matches = soup.find_all(class_='short_item block_elem')
        for match in matches:
            name = match.h3.a.text.replace('Full Game Replay ', '').rstrip(' NHL')
            link = f"{base_url}{match.a['href']}"
            icon = f"{base_url}{match.a.img['src']}"
            games.append(Game(name, links=[Link(link, is_links=True)], icon=icon))
        games.append(Game(f"[COLORyellow]Page {int(page) + 1}[/COLOR]", page=int(page) + 1))
        return games
    
    def get_links(self, url: str) -> List[Link]:
        links = []
        title = ''
        link = ''
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url, headers=headers).text
        soup = bs(r, 'html.parser')
        iframes = soup.find_all('iframe')
        for iframe in iframes:
            link = iframe['src']
            if link.startswith('//'):
                link = f'https:{link}'
            if 'youtube' in link:
                yt_id = link.split('/')[-1]
                link = f'plugin://plugin.video.youtube/play/?video_id={yt_id}'
                title = 'Highlights'
            else:
                title = link.split('/')[2]
            links.append(Link(link, name=title, is_resolveurl=True))
        return links