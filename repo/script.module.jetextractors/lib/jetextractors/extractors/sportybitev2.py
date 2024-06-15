
import requests, re, time, json, datetime
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack

class SportyBitev2(Extractor):
  
    def __init__(self) -> None:
        self.domains = ["streamhd-pro.com"]
        self.name = "SportyBitev2"
    

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")

        for game in soup.select("tbody > tr"):
            if "class" in game.attrs and "date-separator" in game.attrs["class"]:
                continue
            league = game.select_one("td.hidden-xs").text
            hours = game.select_one("td.dt").text
            name = game.select_one("td.event-title").text
            # game_time = game.select_one("td.et3").text.split(":")
            # hour = int(game_time[0])
            # minute = int(game_time[1])
            # utc_time = datetime.datetime.now().replace(hour=hour, minute=minute) + datetime.timedelta(hours=23)
            
            if not name:
                continue
            href = game.find("a").get("href")
            icon = game.find("img").get("src")
            games.append(Game(name, league=league, icon=icon, links=[Link(href)]))

        for channel in soup.select("div.channels"):
            name = channel.text.strip()
            href = channel.find("a").get("href")
            games.append(Game(name, links=[Link(href)]))

        return games

    def get_link(self, url):
        r = requests.get(url).text
        embeds = re.findall(r'embeds.+src="(.+?)"', r)[0]
        if embeds.startswith("//"):
            embeds = "https:" + embeds
        r_embeds = requests.get(embeds, headers={"Referer": url}).text
        fid = re.findall(r'fid="(.+?)"', r_embeds)[0]
        embed_url = "https://b4ucast.com/dhonka.php?player=desktop&live=" + fid
        r_embed = requests.get(embed_url, headers={"Referer": embeds}).text
        m3u8 = "".join(eval(re.findall(r"return\((\[.+?\])", r_embed)[0])).replace("\\", "").replace("////", "//")
        return Link(m3u8, headers={"Referer": embed_url, "User-Agent": self.user_agent})
