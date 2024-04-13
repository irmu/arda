import requests, re, base64, time, random
from datetime import datetime, timedelta
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Link import Link
from ..models.Game import Game

class Onestream(Extractor):
    def __init__(self) -> None:
        self.domains = ["1stream.eu"]
        self.name = "1stream"

    def get_games(self):
        games = []
        base_url = f"http://{self.domains[0]}"
        r = requests.get(base_url).text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.navbar-nav > li > a")
        for category in categories:
            try:
                league = category.text.replace(" streams", "").replace(" Streams", "")
                href = category.get("href")
                r_category = requests.get(base_url + href).text
                soup = BeautifulSoup(r_category, "html.parser")
                for game in soup.find_all("a", class_="btn-block"):
                    try:
                        url = game.get("href")
                        icon = game.find("img").get("src")
                        title = game.find("h4").text.strip()
                        time_str = game.find("p").text.strip()
                        utc_time = datetime(*(time.strptime(time_str, "%a %d %b %Y %H:%M %p EST")[:6])) + timedelta(hours=5)
                        games.append(Game(title=title, links=[Link(address=url)], icon=icon, league=league, starttime=utc_time))
                    except:
                        continue

            except:
                continue
        return games

    def get_link(self, url):
        r = requests.get(url).text
        link = base64.b64decode(re.findall(r'window.atob\("(.+?)"\)', r)[0]).decode("utf-8")
        return Link(link, headers={"Referer": f"https://{self.domains[0]}/", "Origin": f"https://{self.domains[0]}"})