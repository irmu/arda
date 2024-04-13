import re, requests, time

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from .embedstream import Embedstream
from bs4 import BeautifulSoup
from ..icons import icons
from datetime import datetime, timedelta



class Playoffsstream(Extractor):
    def __init__(self) -> None:
        self.domains = ["playoffsstream.com", "playoffsstream.live"]
        self.name = "Playoffsstream"
        self.short_name = "PS"

    def get_link(self, url):
        r_href = requests.get(url).text
        re_embedstream = re.compile(r"embedstream\.me\/(.+?)['\"]").findall(r_href)
        m3u8 = Link()
        if len(re_embedstream) > 0:
            m3u8.address = Embedstream().embedstream(re_embedstream[0])
        elif "/mlb/" in m3u8.address:
            mlb_auth = requests.get("https://magnetic.website/keys/mlb.txt", headers={"User-Agent": "Kodi"}).text
            re_m3u8 = re.compile(r'var .+? = "(.+?)";', re.DOTALL).findall(r_href)
            if len(re_m3u8) > 0:
                m3u8_name = str(re_m3u8[0]).split("/")[-1]
                bitrate_url = str(re_m3u8[0]).replace(m3u8_name, "").strip()
                url_response = requests.get(re_m3u8[0]).text
                bitrates = re.compile(r"\n[^#].*?\.m3u8\n").findall(url_response)
                bitrate = bitrates[-1].replace("complete", "slide")
                m3u8 = Link(bitrate_url + bitrate.strip("\n"), headers={"Cookie", "Authorization=" + mlb_auth})
        elif "nhl.com/" in r_href:
            re_m3u8 = re.compile(r'"(https://.+?nhl\.com.+?\.m3u8)"').findall(r_href)[0]
        return m3u8

    def get_games(self):
        games = []
        base_url = "http://playoffsstream.com"
        r = requests.get(base_url).text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.navbar-nav > li.nav-item > a.nav-link")
        for category in categories:
            league = category.text.strip()
            href = base_url + category.get("href")
            r_league = requests.get(href).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            for game in soup_league.find_all("a", class_="btn-block"):
                try:
                    href = base_url + game.get("href")
                    title = game.find("div", class_="mt-0").getText().strip()
                    time_str = game.find("div", class_="text-center").getText().strip()
                    icon = icons[league.lower()]
                    utc_time = None
                    if time_str != "":
                        utc_time = datetime(*(time.strptime(time_str, "%Y-%m-%d %H:%M ET")[:6])) + timedelta(hours=4)
                    games.append(Game(title=title, links=[Link(href)], icon=icon, league=league, starttime=utc_time))
                except:
                    continue
        return games