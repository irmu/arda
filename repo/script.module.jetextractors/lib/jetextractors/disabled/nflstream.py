import requests, re, time
from bs4 import BeautifulSoup

from ..models.Game import Game
from ..models.Link import Link

from ..models.Extractor import Extractor
from .plytv_sdembed import PlyTv
from datetime import datetime, timedelta
from ..icons import icons



class NFLStream(Extractor):
    def __init__(self) -> None:
        self.domains = ["nflstream.io", "nbastream.nu", "nhlstream.nu", "mlbstream.me", "tennisstreams.me", "rugbystreams.me", "socceronline.me", "boxingstreams.me", "ufcstream.me", "f1stream.me", "motogpstream.me", "cricstream.me"]
        self.name = "NFLStream"
        self.short_name = "NS"
    
    def get_zmid(self, url):
        r_game = requests.get(url).text
        if "zmid" in r_game:
            zmid = re.compile(r'zmid = "(.+?)",').findall(r_game)[0]
        else:
            zmid = re.compile(r'"(https:\/\/www\.tvply\.me\/.+?)"').findall(r_game)[0]
        return zmid

    def get_link(self, url):
        r_game = requests.get(url).text
        plytv = PlyTv()
        if "zmid" in r_game:
            zmid = re.compile(r'zmid = "(.+?)"').findall(r_game)[0]
            url = plytv.plytv_sdembed(zmid, url)
        elif "v_vid" in r_game:
            v_vpp = re.compile(r'v_vpp="(.+?)"').findall(r_game)[0]
            v_vid = re.compile(r'v_vid="(.+?)"').findall(r_game)[0]
            v_vpv = re.compile(r'v_vpv="(.+?)"').findall(r_game)[0]
            url = plytv.plytv_sdembed("https://www.tvply.me/hdembed?p=%s&id=%s&v=%s" % (v_vpp, v_vid, v_vpv), url)
        return url

    def get_games(self):
        games = []
        r_home = requests.get("https://nflstream.io").text
        soup_home = BeautifulSoup(r_home, "html.parser")
        for button in soup_home.find_all("a", {"class": "nav-link"}):
            try:
                base_url = "https://nflstream.io"
                href = "https:" + button.get("href")
                league = button.text[1:]
                if not href.startswith("https://nflstream.io"):
                    base_url = href
                if href.startswith("https://nbastream.nu"):
                    base_url = "https://nbastream.nu" # Fixes NCAAM
                
                r_games = requests.get(href).text
                soup_games = BeautifulSoup(r_games, "html.parser")
                for game in soup_games.find_all("a", {"class": "btn-secondary"}):
                    try:
                        game_href = base_url + game.get("href")
                        title = game.get("title")
                        game_time = datetime(*(time.strptime(game.find_all("span")[-1].get("content"), "%Y-%m-%dT%H:%M")[:6])) - timedelta(hours=1) if game.find_all("span")[-1].get("content") != None else None
                        games.append(Game(title=title, links=[Link(address=game_href)], icon=icons[league.lower()], league=league, starttime=game_time))
                    except:
                        continue
            except:
                continue
        return games