import requests
from bs4 import BeautifulSoup as bs
from typing import List
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link


class NhlVideo(Extractor):
    domains = ["inhlvideo.com"]
    name = "NhlVideo"

    def get_games(self) -> List[Game]:
        games = []
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(base_url, headers=headers, timeout=10).text
        soup = (bs(r, 'html.parser'))
        matches = soup.find_all(class_='excerpt')
        for match in matches:
            title = match.header.text
            link = match.a['href']
            thumbnail = match.img['src']
            games.append(Game(title, links=[Link(link, is_links=True)], icon=thumbnail))
        games.append(Game("[COLORyellow]Page 2[/COLOR]", page=2))
        return games
    
    def get_games_page(self, page) -> List[Game]:
        games = []
        base_url = f"https://{self.domains[0]}"
        url = f"{base_url}/page/{page}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url, headers=headers, timeout=10).text
        soup = (bs(r, 'html.parser'))
        matches = soup.find_all(class_='excerpt')
        for match in matches:
            title = match.header.text
            link = match.a['href']
            thumbnail = match.img['src']
            games.append(Game(title, links=[Link(link, is_links=True)], icon=thumbnail))
        games.append(Game(f"[COLORyellow]Page {int(page) + 1}[/COLOR]", page=int(page) + 1))
        return games
    
    def get_links(self, url: str) -> List[Link]:
        links = []
        title = ''
        link = ''
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url, headers=headers, timeout=10).text
        soup = bs(r, 'html.parser')
        for article in soup.find('article').find_all('a'):
            link = article['href']
            title = link.split('/')[2]
            links.append(Link(link, name=title, is_resolveurl=True))
        return links