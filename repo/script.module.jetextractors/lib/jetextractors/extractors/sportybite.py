
import requests, re, time, json, datetime
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack

class SportyBite(Extractor):
    def __init__(self) -> None:
        self.domains = ["sons-stream.com"]
        self.name = "SportyBite"
    
    league_dict = {
        9: "F1",
        10: "NBA",
        34: "MLB",
        46: "NHL"
    }

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")

        current_date = datetime.datetime.now()
        for game in soup.select("tbody > tr"):
            if "class" not in game.attrs:
                split = game.text.split("-")
                current_date = datetime.datetime(year=int(split[0]), month=int(split[1]), day=int(split[2]))
                continue
            cells = game.select("td")
            hours = cells[0].text.split(":")
            icon = cells[1].select_one("img").get("src")
            league_id = int(icon.split("/")[-1].split(".")[0])
            title = cells[2].text

            links = []
            if ((link := cells[3].select_one("a")) != None):
                links.append(Link(f"https://{self.domains[0]}/tvon.php?hd={link.get('data-stream')}"))
            if ((link := cells[4].select_one("a")) != None):
                links.append(Link(f"https://{self.domains[0]}/tvon.php?hd={link.get('data-stream')}"))

            games.append(Game(title, league=self.league_dict.get(league_id, None), icon=icon, links=links))

        for channel in soup.select("div.channels"):
            name = channel.text.strip()
            href = channel.find("a").get("href")
            games.append(Game(name, links=[Link(href)]))

        return games

    def get_link(self, url):
        r = requests.get(url).text
        fid = re.findall(r'fid="(.+?)"', r)[0]
        embed_url = "https://anarchy-stream.com/dhonka3.php?player=desktop&live=" + fid
        r_embed = requests.get(embed_url, headers={"Referer": url}).text
        m3u8 = "".join(eval(re.findall(r"return\((\[.+?\])", r_embed)[0])).replace("\\", "").replace("////", "//")
        return Link(m3u8, headers={"Referer": embed_url, "User-Agent": self.user_agent})
