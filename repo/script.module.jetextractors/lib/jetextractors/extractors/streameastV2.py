
import requests, re, base64
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes
from ..icons import icons

class StreamEastV2(Extractor):
    def __init__(self) -> None:
        self.domains = ["the.streameast.app"]
        self.name = "StreamEastV2"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}/v2").text
        soup = BeautifulSoup(r, "html.parser")

        for game in soup.select("li.f1-podium--item"):  #ul.f1-podium li.f1-podium--item
            name = game.select_one("span.d-md-inline").text
            live = game.select("span",style_="color: #e10600;font-weight:bold;")[-1].text
            sport = game.select_one("span",class_="f1-podium--rank f1-bold--xs",stlyle_="min-width: 35px;width: unset;").text 
          
            if not name:
                continue
            href = game.find("a").get("href")
            games.append(Game(icon=icons[sport.lower()] if sport.lower() in icons else None,title=sport+ "[COLORyellow] | [/COLOR]"+name + "   "+"[COLORred]"+ live+"[/COLOR]",links=[Link(href)]))
        return games

    def get_link(self, url):
        r = requests.get(url).text
        atob = base64.b64decode(re.findall(r"window.atob\('(.+?)'\)", r)[0]).decode("ascii")
        return Link(atob, headers={"Referer": url})


