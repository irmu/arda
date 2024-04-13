import requests, re, dateutil.parser
from bs4 import BeautifulSoup
from datetime import timedelta
import xbmcgui

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Sixstream(Extractor):
    def __init__(self) -> None:
        self.domains = ["v.markkystreams.com", "6streams.tv"]
        self.name = "6stream"
        self.short_name = "6S"

    def get_link(self, url):
        r = requests.get(url).text
        m3u8 = Link(address=re.compile(r'source: "(.+?)"').findall(r)[0].replace(".m3u8", ".m3u8?&Connection=keep-alive"), headers={"Referer": url, "User-Agent": self.user_agent}, is_hls=True)
        if m3u8 is not None:
            # m3u8.license_url = f"|Referer=https://weblivehdplay.ru&Origin=https://weblivehdplay.ru"
            ret = self.show_ffmpeg_dialog()
            if ret != -1:
                if ret == 0:
                    m3u8.is_ffmpegdirect = True
                elif ret == 1:
                    m3u8.is_hls = True
                elif ret == 2:
                    m3u8.is_hls = False
        return m3u8
    def show_ffmpeg_dialog(self):
        dialog = xbmcgui.Dialog()
        ret = dialog.contextmenu(['ffmpeg', 'HLS', 'NONE'])

        return ret
        # return m3u8

    def get_games(self):
        games = []
        r = requests.get("https://" + self.domains[0]).text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.nav > li.menu-item > a")
        categories = categories[:int(len(categories) / 2)] # Remove bottom nav buttons
        for category in categories:
            try:
                if "Streams" not in category.text:
                    continue
                league = category.text.replace(" Streams", "")
                href = category.get("href")
                r_league = requests.get(href).text
                soup_league = BeautifulSoup(r_league, "html.parser")
                for game in soup_league.find_all("figure"):
                    try:
                        icon = game.get("data-original")
                        sibling = game.next_sibling
                        title = sibling.select_one("h2.entry-title > a").get("title")
                        game_href = game.find("a").get("href")
                        utc_time = None
                        if title.lower().endswith("et"): # this is dumb
                            time = " ".join(title.split(" ")[::-1][:3][::-1])
                            utc_time = dateutil.parser.parse(time.upper()) + timedelta(hours=4)
                            title = title.replace(time, "").strip()

                        games.append(Game(title=title, icon=icon, league=league, starttime=utc_time, links=[Link(address=game_href)]))
                    except:
                        continue
            except:
                continue
        return games