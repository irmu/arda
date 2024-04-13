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


class Apkskip(Extractor):
    def __init__(self) -> None:
        self.domains = ["apkship.xyz"]
        self.name = "Apkskip"
        self.short_name = "APK"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        for game in soup.find_all("li"):
            href = game.find("a").get("href")
            title = game.find("a").text.strip()
            games.append(Game(title=title, links=[Link(address=href)]))
        return games
    
    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        link = iframes[0]
        # if "premium" in link.address:
        #     link.license_url = f"|Referer=https://claplivehdplay.ru/&Origin=https://claplivehdplay.ru"
        #     link.is_ffmpegdirect = True
        if "mono.m3u8" in link.address:
            return Daddylive().get_link(link.address)
        if "voodc" in link.address:
            return Voodc().get_link(link.address)
        if "freesportstime" in link.address:
            del link.headers["Referer"]
        return link