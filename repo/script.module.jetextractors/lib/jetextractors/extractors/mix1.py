
import requests, re, datetime
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes

class MixSports1(Extractor):
    def __init__(self) -> None:
        self.domains = ["methstreams.me/","streameast.top","bestsolaris.com","topstreams.me","givemeredditstreams.me","nbastreams.org","thesportsurge.net","rojadirecta.io","rnbastreams.net","vipboxs.net/","thebuffstreams.com","streameast.stream","hesgoals.to","rainostream4u.online","worldstreams.watch",
                        ]
        #"dofusports.xyz/"
        self.name = "MixSports1"

    # def get_games(self):
    #     games = []
    #     r = requests.get(f"https://{self.domains[0]}").text
    #     soup = BeautifulSoup(r, "html.parser")

    #     for game in soup.select("ul.f1-podium li.f1-podium--item"):
    #         name = game.select_one("span.d-md-inline").text
    #         live = game.select("span",style_="color: #e10600;font-weight:bold;")[-1].text
    #         sport = game.select_one("span",class_="f1-podium--rank f1-bold--xs",stlyle_="min-width: 35px;width: unset;").text 
          
    #         if not name:
    #             continue
    #         href = game.find("a").get("href")
    #         games.append(Game(sport+ "[COLORyellow] | [/COLOR]"+name + "   "+"[COLORred]"+ live+"[/COLOR]",links=[Link(href)]))
    #     return games

    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        return iframes[0]


