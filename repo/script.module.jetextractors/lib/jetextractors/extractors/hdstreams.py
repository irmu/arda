
import requests, re, datetime, base64
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack
from ..icons import icons

class HDStreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["www1.ihdstreams.xyz", "live.ihdstreams.xyz"]
        self.name = "HDStreams"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")

        navbar = soup.find("nav")
        hrefs = navbar.find_all("a", class_="block")
        for sport in hrefs:
            sport_href = sport.get("href")
            sport_name = sport.text.replace("STREAMS", "").replace("STREAM", "").replace("Streams", "").lower()
            sport_url = f"https://{self.domains[0]}{sport_href}"
            # sport = sport_name

            r = requests.get(sport_url).text
            re_iframe = re.findall(r'iframe.+?src="(.+?)"', r)[0]
            r = requests.get(re_iframe, headers={"Referer": sport_url}).text
            soup = BeautifulSoup(r, "html.parser")
            # sport = sport_name.lower()
            for game in soup.find_all("a", class_="w-full"):
                name = game.h3.get_text(strip=True)
                if not name:
                    continue
                href = game.get("href")
                games.append(Game(icon=icons[sport_name] if sport_name in icons else None,title=name, league=sport_name.upper(), links=[Link(href)]))
        return games

    def get_link(self, url):
        r = requests.get(url).text
        re_iframe = re.findall(r'iframe.+?src="(.+?)"', r)[0]
        
        r_iframe = requests.get(re_iframe, headers={"Referer": url}).text 
        re_iframe2 = re.findall(r'iframe.+?src="(.+?)"', r_iframe)[0]

        if re_iframe2.startswith("//"):
            re_iframe2 = "https:" + re_iframe2
        r_iframe2 = requests.get(re_iframe2, headers={"Referer": re_iframe}).text 

        re_atob = re.findall(r"window.atob\('(.+?)'\)", r_iframe2)[0]
        link = base64.b64decode(re_atob).decode("ascii")
        if link.startswith("//"):
            link = "https:" + link
        return Link(link, headers={"Referer": re_iframe2, "User-Agent": self.user_agent})


