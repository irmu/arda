import requests, re
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..icons import icons

class Azulito(Extractor):
    def __init__(self) -> None:
        self.domains = ["fabtech.work/category/"]
        self.name = "Azulito"
        self.short_name = "AZ"

    def get_link(self, url):
        r = requests.get(url).text
        m3u8 = re.findall(r"source src=\"(.+?)\"", r)[0]
        
        return Link(address=m3u8.replace(".m3u8", ".m3u8?&Connection=keep-alive"), headers={"Referer": url}, is_ffmpegdirect=True)
    
       

    def get_games(self):
        games = []
        leagues = ["nba/","ncaa/","soccer/","nfl/","boxing/"]
        for league in leagues:
            sport = league.replace("/","")
            r = requests.get("https://" + self.domains[0]+league).text
            soup = BeautifulSoup(r, "html.parser")
            for game in soup.select("h3"):
                title = game.text
                href = game.select_one("a").get("href")
                # icon = game.select_one("img").get("src")
                # try: league = game.select_one("a.entry-category").text.replace(" Streams", "")
                # except: league = None
                games.append(Game(icon=icons[sport.lower()] if sport.lower() in icons else None,league=sport.upper(),title=title, links=[Link(address=href)]))
        return games
