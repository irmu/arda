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
from ..icons import icons

class StreamBTW(Extractor):
    def __init__(self) -> None:
        self.domains = ["streambtw.com"]
        self.name = "StreamBTW"
        self.short_name = "CS"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        
        for game_area in soup.select("div.single-timeline-area"):
            game_titles = [title.text.strip() for title in game_area.select("h6")]
            hrefs = [link.get("href") for link in game_area.select("a")]
            sport = [title.text.strip() for title in game_area.select("p")]
            
            for title,sport, href in zip(game_titles,sport, hrefs):
             games.append(Game(icon=icons[sport.lower()] if sport.lower() in icons else None,league=sport.upper(),title=title, links=[Link(href)]))




        return games

    def get_link(self, url):
            iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
            iframes[0].headers["Origin"] = f"https://{self.domains[0]}"
            iframes[0].headers["User-Agent"] = self.user_agent
            return iframes[0]