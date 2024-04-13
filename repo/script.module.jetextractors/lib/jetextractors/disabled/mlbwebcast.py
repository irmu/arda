
import requests, re, datetime
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes

class MLBWebCast(Extractor):
    def __init__(self) -> None:
        self.domains = ["mlbwebcast.com"]
        self.name = "MLBwebCast"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        for game in soup.select("tr.singele_match_date "):
            if "mdatetitle" in game.attrs["class"]:
                 continue
            name = " ".join(game.select_one("td.teamvs").text.strip().replace("  ", " ").split(" ")[:3])
            game_time = game.select_one("td.matchtime").text.strip().split(":")
            game_icon = game.select_one("img").get("src")
            hour = int(game_time[0])
            minute = int(game_time[1])
            utc_time = datetime.datetime.now().replace(hour=hour, minute=minute) + datetime.timedelta(hours=4)
            href = game.find("a").get("href")
            games.append(Game(name, starttime=utc_time, icon=game_icon, links=[Link(href, is_links=True)]))
        return games

    def get_links(self, url):
        r = requests.get(url).text
        re_links = re.findall(r"<a class=\"btn .+\" href=\"(https://mlbwebcast\.com/stream/.+)\" target", r)
        iframes = []
        for link in re_links:
            iframes += [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(link, "", [], [])]
        for iframe in iframes:
            iframe.is_direct = True
            if "Referer" in iframe.headers and "bdnewszh.com" in iframe.headers["Referer"]:
                iframe.headers["Referer"] = "https://bdnewszh.com/"
        links = [link for link in iframes if "m3u8" in link.address]
        if len(links) >= 2:
            links[0].name = "Home"
            links[1].name = "Away"
        return links


