
import requests, re, datetime, base64
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes
from ..icons import icons



class Pawa(Extractor):
    def __init__(self) -> None:
        self.domains = ["pawastreams.info/","ww2.pawastreams.top"]#ww2.pawastreams.top
        self.name = "Pawa"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")

        for category in soup.select("h2.elementor-heading-title"):
            sport = category.text.replace(" Streams", "")
            sport_href = category.select_one("a")
            if sport_href == None:
                continue
            sport_href = sport_href.get("href")
            r_sport = requests.get(sport_href).text
            soup_sport = BeautifulSoup(r_sport, "html.parser")
            for game in soup_sport.select("h3.elementor-post__title"):
                name = game.select_one("a").text
                if not name:
                    continue
                href = game.find("a").get("href")
                games.append(Game(icon=icons[sport.lower()] if sport.lower() in icons else None,
                  title="[COLORyellow] | [/COLOR]"+name + "   "+"[COLORred][/COLOR]",links=[Link(href)], league=sport))
        
        return games

    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], []) if self.domains[0] not in str(u)]
        return iframes[0]


