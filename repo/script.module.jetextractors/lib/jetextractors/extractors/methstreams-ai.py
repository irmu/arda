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

class Methstreamsai(Extractor):
    def __init__(self) -> None:
        
        self.domains = ["meth-streams.ai"]
        self.name = "Methstreamsai"
        self.short_name = "MSAI"

    

    def get_link(self, url):
        r = requests.get(url).text
        atob = base64.b64decode(re.findall(r"window.atob\('(.+?)'\)", r)[0]).decode("ascii")
        return Link(atob, headers={"Referer": url})
        
   

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.navbar-nav > li > a")
        for category in categories:
            league = category.text.replace(" streams", "")
            league_href = category.get('href')
            r_league = requests.get(league_href).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            league_games = soup_league.find_all("a", {"class": "btn-block"})
            for body in league_games:
                href = body.get("href")
                if href.startswith("/"):
                    href = f"https://{self.domains[0]}{href}"
                title = body.find("h4").text.strip()
                time = body.find("p").text
                utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time) + timedelta(hours=4)
                    except:
                        try:
                            utc_time = datetime.strptime(time, "%H:%M %p ET - %m/%d/%Y") + timedelta(hours=4)
                        except:
                            pass
                games.append(Game(icon=icons[league.lower()] if league.lower() in icons else None,
                  title=title, links=[Link(address=href)],  league=league, starttime=utc_time))
        return games
