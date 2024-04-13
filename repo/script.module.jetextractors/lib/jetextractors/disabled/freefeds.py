import requests, re, time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import m3u8_src
from . import sling, telerium
from urllib.parse import quote

class Freefeds(Extractor):
    def __init__(self) -> None:
        self.domains = ["freefeds.com"]
        self.name = "Freefeds"
        self.short_name = "FF"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        for tab in soup.select("div"):
            if "id" not in tab.attrs or not tab.attrs["id"].startswith("tab"): continue
            sport = tab.select_one("h3").text.replace(" schedule", "")
            date = datetime.now()
            date_ahead = date + timedelta(days=2)
            for child in tab.contents:
                if child == "\n": continue
                elif child.name == "h3":
                    if child.text.endswith("schedule"): continue
                    else: 
                        date = datetime(*(time.strptime(child.text, "%A, %B %d, %Y")[:6]))
                elif child.name == "div":
                    title = child.select_one("h4").text.strip()
                    title_split = title.split(" - ")
                    time_split = title_split[0].split(":")
                    game_time = date.replace(hour=int(time_split[0]), minute=int(time_split[1])) + timedelta(hours=4)
                    if game_time > date_ahead: continue
                    game_title = title_split[1].replace("'", "").replace('"', "")
                    league = title_split[2]
                    links = []
                    for link in child.select("input.sm"):
                        if link.attrs["value"].startswith("http") and "/video/" not in link.attrs["value"]: links.append(Link(address=link.attrs["value"]))
                    games.append(Game(title=game_title, links=links, league="%s/%s" % (sport, league), starttime=game_time))
        return games

    def get_link(self, url):
        r = requests.get(url, headers={"User-Agent": self.user_agent, "Referer": "https://" + self.domains[0]}).text
        scan = m3u8_src.scan_page(url, r)
        if scan: return scan
        if "chNo=" in r:
            r_chno = re.findall(r"chNo=(.+?);", r)[0]
            r_sling = requests.get("https://cbd46b77.cdn.cms.movetv.com/cms/publish3/domain/summary/ums/1.json", headers={"User-Agent": self.user_agent}).json()
            mpd_url, license_url, _, start_time = sling.Sling().get_playlist(r_sling["channels"][1]["qvt_url"])
            mpd_url = mpd_url.replace(re.findall(r"(clipslist\/.+?)\/", mpd_url)[0], "clipslist/" + r_chno)
            return Link(address=mpd_url, is_widevine=True, license_url=license_url)
        if ".mpd?" in r:
            src = re.findall(r"var src = \"(.+?)\";", r)[0]
            payload = '{"channel_id": "6f6788bea06243da873b8b3450b4aaa0", "env": "production", "message": [D{SSM}], "user_id": "fcdda172-0060-11eb-b722-0a599a2ac821"}'
            license_key = '%s|Content-Type=text/plain&User-Agent=%s|%s|' % ("https://p-drmwv.movetv.com/widevine/proxy", self.user_agent, quote(payload))
            return Link(address=src, is_widevine=True)
        if "teleriumtv.com" in r:
            re_telerium = re.findall(r"src=\"(https:\/\/teleriumtv\.com\/embed\/.+?)\"", r)[0]
            return telerium.Telerium().get_link(re_telerium)
