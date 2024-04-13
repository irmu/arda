import requests
from bs4 import BeautifulSoup as bs
from typing import List
import xbmc
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link


class FullRaces(Extractor):
    domains = ["fullraces.com"]
    name = "Fullraces"

    def get_games(self) -> List[Game]:
        games = []
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(base_url, headers=headers, timeout=10).text
        soup = (bs(r, 'html.parser'))
        matches = soup.find_all(class_='short_item')
        for match in matches:
            name = match.h3.a.text
            link = f"{base_url}{match.a['href']}"
            icon = f"{base_url}{match.a.img['src']}"
            games.append(Game(name, links=[Link(link, is_links=True)], icon=icon))
        games.append(Game("[COLORyellow]Page 2[/COLOR]", page=2))
        return games
    
    def get_games_page(self, page) -> List[Game]:
        games = []
        int_page = 1
        base_url = f"https://{self.domains[0]}"
        if not str.isdecimal(page):
            splitted = page.split('/')
            if len(splitted) > 1:
                int_page = int(splitted[-1])
                page = splitted[0]
            url = f'{base_url}/{page}?page{int_page}'
        else:
            url = f"{base_url}?page{page}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url, headers=headers, timeout=10).text
        soup = (bs(r, 'html.parser'))
        matches = soup.find_all(class_='short_item')
        for match in matches:
            name = match.h3.a.text
            link = f"{base_url}{match.a['href']}"
            icon = f"{base_url}{match.a.img['src']}"
            games.append(Game(name, links=[Link(link, is_links=True)], icon=icon))
        if not str.isdecimal(page):
            games.append(Game(f"[COLORyellow]Page {int(int_page) + 1}[/COLOR]", page=f'{page}/{int(int_page) + 1}'))
        else:
            games.append(Game(f"[COLORyellow]Page {int(page) + 1}[/COLOR]", page=int(page) + 1))
        return games
    
    def get_links(self, url: str) -> List[Link]:
        xbmc.log('Fullraces get_links started', xbmc.LOGINFO)
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
        for button in soup.find_all(class_='su-button'):
            link = button['href']
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