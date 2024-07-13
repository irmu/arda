import requests, re, base64,json
from bs4 import BeautifulSoup
from dateutil.parser import parse
from urllib.parse import urlparse
from datetime import timedelta, datetime

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.m3u8_src import scan_page
from ..util import jsunpack, find_iframes
from ..icons import icons
from .daddylive import Daddylive
from .voodc import Voodc
from .givemereddit import GiveMeReddit


class Elixx(Extractor):
    def __init__(self) -> None:
        self.domains = ["www.elixx.xyz"]
        self.name = "Elixx"
        self.short_name = "ELI"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}/schedule.html").text
        soup = BeautifulSoup(r, "html.parser")
        for button in soup.select("button.accordion"):
            title = button.text
            panel = button.next_sibling.next_sibling
            links = [Link(link.get("href"), name=link.text) for link in panel.select("a")]
            games.append(Game(title, links))
        return games
    
    def get_link(self, url: str) -> Link:
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        link = next(filter(lambda x: "m3u8" in x.address, iframes))
        link.headers["Origin"] = "https://" + urlparse(link.headers["Referer"]).netloc
        return link