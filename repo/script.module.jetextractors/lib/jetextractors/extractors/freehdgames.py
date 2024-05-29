import requests, re, base64
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta, datetime

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.m3u8_src import scan_page
from ..util import jsunpack, find_iframes
from ..icons import icons

class Freehdgames(Extractor):
    def __init__(self) -> None:
        self.domains = ["gamehdlive.online"]
        self.name = "Freehdgames"
        self.short_name = "HG"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        for game in soup.select("a"):
            href = game.get("href")
            if "ch" not in href or not href.endswith(".php"):
                continue
            league = game.previous.previous.text
            sport = league.replace(" —","")
            link_name = game.text
            game_time = game.previous.previous.previous.previous.text
            name = (game_time + " " + game.previous.text).strip()
            if not name or "Watch Free Games" in name:
                continue
            games.append(Game(icon=icons[sport.lower()] if sport.lower() in icons else None,
                  title=name, league=sport, links=[Link(href, name=link_name)]))
        return games

    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        return iframes[0]









    
