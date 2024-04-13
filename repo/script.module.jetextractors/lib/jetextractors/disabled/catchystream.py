import requests, re, base64
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta, datetime

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.m3u8_src import scan_page
from ..util import jsunpack, find_iframes
from ..util.hunter import hunter

class Catchystreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["catchystream.com"]
        self.name = "Catchystream"
        self.short_name = "CS"
        
    

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        # categories = soup.select("ul.navbar-nav > li > a")
        # for category in categories:
        #     league = category.text.replace(" streams", "")
        #     league_href = category.get('href')
        #     r_league = requests.get(league_href).text
        #     soup_league = BeautifulSoup(r_league, "html.parser")
        #     league_games = soup_league.find_all("a", {"class": "btn-block"})
        for game in soup.select("div.card-body"):
            name = game.select_one("div.timeline-title").text
            live = game.select_one("div.timeline-local-time").text 
            sport = game.select_one("div.timeline-league").text 
          
            # if not name:
            #     continue
            href = game.find("a").get("href")
            href1= "https://"+self.domains[0]+"/"+ href
            games.append(Game(sport+ "[COLORyellow] | [/COLOR]"+name + "   "+"[COLORred]"+ live+"[/COLOR]",links=[Link(href1)]))
        return games

    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        return iframes[0]
    

        
