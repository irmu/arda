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


class Sol(Extractor):
    def __init__(self) -> None:
        
        self.domains = ["bestsolaris.com/category/"]
        self.name = "Sol"
        self.short_name = "MS"


    def get_games(self):
        games = []
        leagues = ["nba","mlb","nhl","mma","boxing","cfb","motor-sports"]#,"mma","boxing","nfl","cfb","motor-sports"
        
        for league in leagues:
            r = requests.get(f"https://{self.domains[0]}"+league+"streams").text
            soup = BeautifulSoup(r, "html.parser")
                # leagues1= league.replace("streams","").replace("-","").replace("get","").replace("/1/","").replace("/","").replace("4","").replace("live","").replace("collegebasketball","ncaab")
                
                
                
            for game in soup.find_all("li", {"class": "f1-podium--item"}):
                href = game.find("a").get("href")
                
                # href = game.get("href")
                        # if href.startswith("/"):
                        #     href = f"https://{self.domains[0]}{href}"
                title = game.find("span",{"class": "f1-podium--driver f1--xs MacBaslik"}).text.strip()
                
                
                
                time = game.find("span",{"class": "f1-podium--time f1-label f1-bg--gray2 misc--label text-semi-bold MacBaslikSagTarih"}).text.strip()
                # title = title +"\n" +time  
                
                utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time) + timedelta(hours=5)
                    except:
                        try:
                            utc_time = datetime.strptime(time, "%H:%M %p ET - %m/%d/%Y") + timedelta(hours=5)
                        except:
                            pass
                games.append(Game(icon=icons[league.lower()] if league.lower() in icons else None,league=league.upper(),title=title, links=[Link(address=href)], starttime=utc_time ))
        return games
                
        
            




    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]

        
        return iframes[0]