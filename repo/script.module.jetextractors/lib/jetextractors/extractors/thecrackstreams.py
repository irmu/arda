import requests, re, base64
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta, datetime

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.m3u8_src import scan_page
from ..util import jsunpack, find_iframes

class Thecrackstreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["v2.thecrackstreams.live"]
        self.name = "Thecrackstreams"
        self.short_name = "TC"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")

        for element in soup.select_one("div.col-md-8").children:
            if element.name == "div":
                league = element.text.strip()
            elif element.name == "a":
                href = element.get("href")
                icon = element.select_one("img").get("src")
                name = element.select_one("h4").text.strip()
                try:
                    game_time = element.select_one("p").text.strip()
                    utc_time = datetime.strptime(game_time, "%a %d %b %Y %H:%M %p EST") + timedelta(hours=5)
                except:
                    utc_time = None
                games.append(Game(name, icon=icon, league=league, starttime=utc_time, links=[Link(href)]))
        return games

    def get_link(self, url):
        r = requests.get(url).text
        atob = base64.b64decode(re.findall(r"window.atob\('(.+?)'\)", r)[0]).decode("ascii")
        return Link(atob, headers={"Referer": url})









    
