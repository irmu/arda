import requests, re
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import m3u8_src

class Sportea(Extractor):
    def __init__(self) -> None:
        self.domains = ["s1.sportea.link"]
        self.name = "Sportea"

    def get_games(self):
        games = []

        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        for table in soup.select("div.p-4 > div.row"):
            league = table.select_one("h5").text.upper()
            for game in table.select("tbody > tr"):
                data = game.select("td")
                time = data[1].text
                title = data[2].text.split("\n")[0].strip()
                href = "https:" + data[-1].select_one("a").get("href")
                games.append(Game(title, links=[Link(href)], league=league))
        return games

    def get_link(self, url):
        return m3u8_src.scan_page(url.replace("embed.php", "channel.php"), headers={"Referer": url})