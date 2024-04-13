import re, requests, time

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from .plytv_sdembed import PlyTv
from bs4 import BeautifulSoup
from datetime import datetime
from ..icons import icons

class Buffstreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["buffstreams.tv"]
        self.name = "Buffstreams"
        self.short_name = "BUFF"

    def get_zmid(self, url):
        r_game = requests.get(url).text
        zmid = re.compile(r'zmid = "(.+?)"').findall(r_game)[0]
        return zmid

    def get_link(self, url):
        r = requests.get(url).text
        plytv = PlyTv()
        if "zmid" in r:
            zmid = re.compile(r'zmid = "(.+?)"').findall(r)[0]
            url = plytv.plytv_sdembed(zmid, url)
        else:
            v_vpp = re.compile(r'v_vpp="(.+?)"').findall(r)[0]
            v_vid = re.compile(r'v_vid="(.+?)"').findall(r)[0]
            v_vpv = re.compile(r'v_vpv="(.+?)"').findall(r)[0]
            url = plytv.plytv_sdembed("https://www.tvply.me/hdembed?p=%s&id=%s&v=%s" % (v_vpp, v_vid, v_vpv), url)
        return Link(address=url)

    def get_games(self):
        games = []
        base_url = "https://buffstreams.tv"
        r_home = requests.get(base_url).text
        soup_home = BeautifulSoup(r_home, "html.parser")
        for button in soup_home.find_all("div", {"class": "col-lg-3"}):
            href = base_url + button.find("a").get("href")
            category = href.replace("https://buffstreams.tv/watch-", "")
            r_category = requests.get(href).text
            soup_category = BeautifulSoup(r_category, "html.parser")
            for game in soup_category.find_all("a", {"class": "card"}):
                try:
                    game_href = base_url + game.get("href")
                    title = game.find_all("span")[-1].text
                    game_time = datetime(*(time.strptime(game.find_all("span")[-1].get("content"), "%Y-%m-%dT%H:%M")[:6])) if game.find_all("span")[-2].get("content") != None else ""
                    league = category
                    games.append(Game(title=title, links=[Link(address=game_href)], icon=icons[league.lower()], league=league.capitalize(), starttime=game_time))
                except Exception as e:
                    continue
        return games