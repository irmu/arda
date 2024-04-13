import requests, datetime, time
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Streameast(Extractor):
    def __init__(self) -> None:
        self.domains = ["v1.streameast.top"]
        self.name = "Streameast"

    def get_games(self):
        games = []

        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")

        for league in soup.select("ul.navbar-nav > li.nav-item > a.nav-link"):
            r_league = requests.get(league.get("href")).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            for competition in soup_league.select("div.top-tournament"):
                if (league_name := competition.select_one("span.league-name")) == None:
                    continue
                league_name = league_name.text
                for game in competition.select("li"):
                    block = game.find("a")
                    href = block.get("href")
                    if "d-block" in block.attrs["class"]:
                        name = " - ".join(map(lambda x: x.strip(), block.next.replace("\n", "").strip().split("-")))
                    else:
                        name = block.get("title")
                    if (score_elem := block.find("span", class_="competition-cell-score")) != None:
                        name += f" ({score_elem.text.strip()})"
                    utc_time = None
                    if (time_elem := block.find("time")) != None:
                        utc_time = datetime.datetime(*(time.strptime(time_elem.get("datetime"), "%Y-%m-%d %H:%M:%S")[:6])) + datetime.timedelta(hours=7)
                    games.append(Game(name, links=[Link(href, is_links=True)], league=league_name, starttime=utc_time))
        return games

    def get_links(self, url: str):
        r = requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        links = [Link(button.get("datatype")) for button in soup.select("button.embed-link")]
        return links
    