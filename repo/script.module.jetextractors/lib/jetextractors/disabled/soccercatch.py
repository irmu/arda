import requests
import datetime
import re
from bs4 import BeautifulSoup as bs
from base64 import b64decode
from typing import List
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from xbmcgui import Dialog


class SoccerCatch(Extractor):
    domains = ["soccercatch.com"]
    name = "SoccerCatch"

    def get_games(self) -> List[Game]:
        dates = self.get_dates()
        games = [Game(title=date[0], page=date[1]) for date in dates]
        return games
    
    def get_games_page(self, date) -> List[Game]:
        games = []
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.post(f"{base_url}/api/matches/date?date={date}", headers=headers).text
        soup = (bs(r, 'html.parser'))
        matches = soup.find_all('a', class_='match-list-content')
        for match in matches:
            url = f"{base_url}{match['href']}"
            home = match.find(class_='match-list-home')
            away = match.find(class_='match-list-away')
            home_name = home.img['alt']
            home_icon = home.img['src']
            away_name = away.img['alt']
            name = f'{home_name} vs {away_name}'
            games.append(Game(name, links=[Link(url, is_links=True)], icon=home_icon))
        return games
    
    def get_links(self, url: str) -> List[Link]:
        links = []
        base_url = f"https://{self.domains[0]}"
        headers = {"User-Agent": self.user_agent, "Referer": base_url}
        r = requests.get(url, headers=headers).text
        soup = bs(r, 'html.parser')
        highlights = soup.find_all(class_='iframe-responsive')
        url = re.findall(' src="(.+?)"| src=\'(.+?)\'', str(highlights))
        
        highlight_links = []
        for url1, url2 in url:
            if url1 != '':
                highlight_links.append(url1)
            if url2 != '':
                highlight_links.append(url2)
        if highlight_links:
            for link in highlight_links:
                if 'youtube' in link:
                    yt_id = link.split('/')[-1]
                    yt_link = f'plugin://plugin.video.youtube/play/?video_id={yt_id}'
                    links.append(Link(yt_link, name='Highlights - YouTube'))
        
        links2 = []
        fullmatch = soup.find_all(class_='hidden-link')
        for match in fullmatch:
            link = re.findall('data-url="(.+?)"', str(match))[0]
            link = b64decode(link).decode('utf-8').rstrip('.html')
            if 'payskip.org' in link:
                continue
            if link in str(links2):
                continue
            host = link.split('/')[2]
            title = match.text.replace('Main Player - ', '')
            title = title.replace('Alternative Player - ', '')
            title = title.replace('Official - ', '')
            title = title.replace('Fast Direct Link - ', '')
            title = f'{title} - {host}'
            links2.append([title, link])
        if links2:
            for title, link in links2:
                links.append(Link(link, name=title, is_resolveurl=True))
        return links
    
    def get_dates(self):
        dates = []
        d = datetime.date(2021,1,18)
        while d <= datetime.date.today():
            dates.append([datetime.datetime.strftime(d,'%A, %B %d, %Y'), datetime.datetime.strftime(d,'%d-%m-%Y')])
            d += datetime.timedelta(days=1)
        return list(reversed(dates))