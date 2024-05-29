import requests, re
from bs4 import BeautifulSoup
import requests, re, datetime,json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from datetime import datetime
from urllib.parse import urlparse
from dateutil.parser import parse

date = datetime.now()

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes
from typing import List
from .daddylive import Daddylive
from .voodc import Voodc
from .givemereddit import GiveMeReddit
from .weakspell import Weakspell
from .vecdn import VeCDN
url1 = "hd.cricfree.io"
class Cric_Test(Extractor):
    def __init__(self) -> None:
        self.domains = ["hd.cricfree.io/"]
        self.name = "Cric_Test"

    def get_games(self) -> List[Game]:
        games = []
        r = requests.get(f"https://{self.domains[0]}")
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            game_rows = soup.find_all('tr', class_='info-open')
            link_rows = soup.find_all('tr', class_='info')

            for row, link_row in zip(game_rows, link_rows):
                time = row.find('td', class_='time').text.strip()
                # utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time) + timedelta(hours=23)
                    except:
                        # try:
                        #     utc_time = datetime.strptime(time, "%H:%M %p ET - %m/%d/%Y") + timedelta(hours=0)
                        # except:
                            pass
                title = row.find('td', class_='event').text.strip()
                league = row.find('td', class_='competition').text.strip()
                # league = league+" | "+time+" - "
                href = row.find('td', class_='event').find('a')['href']
                links = [a['href'] for a in link_row.find_all('a')]
                games.append(Game(league=league,starttime=utc_time,title=title,links=[Link(link) for link in links]))

        r_channels = requests.get(f"https://cricfree.live/live/sky-sports-main-event")
        if r_channels.status_code == 200:
            soup_channels = BeautifulSoup(r_channels.text, "html.parser")
            channel = soup_channels.find('ul', class_='nav-sidebar')
            if channel:
                channels_links = channel.find_all('a')
                for link in channels_links:
                    
                    title = link['title']
                    
                    href = link['href']
                    
                    games.append(Game(league="Channel",title=title ,links=[Link(href)]))

        return games

        

       
    

        

    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        link = iframes[0]
        
        if "index.m3u8" in link.address:
            return Voodc().get_link(link.address)
        return iframes[0]