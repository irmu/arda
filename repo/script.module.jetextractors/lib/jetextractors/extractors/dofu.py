
import requests, re, time, json, datetime,base64
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes
from ..icons import icons

from .voodc import Voodc
from .givemenbastream import GiveMeNBAStreams


class Dofu(Extractor):
  
    def __init__(self) -> None:
        self.domains = ["dofusports.xyz"]
        self.name = "Dofu"
        
    NBA = "[COLORyellow]NBA[/COLOR]"

    def get_games(self):
        games = []
        r = requests.get(f"http://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")

        for category in soup.select('table'):
            league = category.select_one("th").text.split()[0]
            # print(f"--- {league} ---")
            for game in category.select("tbody > tr"):
                td = game.select("td")
                date = td[0].text
                
                date_time = datetime.strptime(date, "%B %d, %Y %H:%M")
                adjusted_date_time = date_time - timedelta(hours=8)
                time_part = adjusted_date_time.strftime("%I:%M %p").lstrip('0')
                
                name = td[1].text
                href = game.find("a").get("href")
                sport = league
                
                if sport == "NBA":
                    sport = "[COLORaqua]NBA: [/COLOR]"
                elif sport == "MLB":
                    sport = "[COLORorange]MLB: [/COLOR]"
                elif sport == "NHL":
                    sport = "[COLORyellow]NHL: [/COLOR]"
                elif sport == "NFL":
                    sport = "[COLORlime]NFL: [/COLOR]" 

                elif sport == "CFB":
                    sport = "[COLORpurple]CFB: [/COLOR]"
                

                    
                games.append(Game(icon=icons[league.lower()] if league.lower() in icons else None,
                  title=adjusted_date_time.strftime("%m/%d %#I:%M %p").lstrip('0') + " " + sport + " " + name,
                  links=[Link(href)]))

        return games

    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        link = iframes[0]
        if "giveme" in link.address:
            return GiveMeNBAStreams().get_link(link.address)
        if "voodc" in link.address:
            return Voodc().get_link(link.address)
        if "freesportstime" in link.address:
            del link.headers["Referer"]
        return iframes[0]
    
