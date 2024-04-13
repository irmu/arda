from typing import List
import xbmcgui
import requests, re, json, time
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote
from ..models.Extractor import Extractor
from ..models.Link import Link
from ..models.Game import Game

class Weakspell(Extractor):
    def __init__(self) -> None:
        self.name = "Weakspell/LiveOnScore"
        self.short_name = "WS"
        self.domains = ["weakspell.to", "sporteks.net", "liveonscore.tv", "wpstream.tv"]

    def get_link(self, url: str) -> Link:
        base_url = "http://" + urlparse(url).netloc
        r_game = requests.get(url).text
        re_vidgstream = re.compile(r'var vidgstream = "(.+?)";').findall(r_game)[0]
        if base_url == "http://liveonscore.tv":
            re_gethlsUrl = re.compile(r'gethlsUrl\(vidgstream, (.+?), (.+?)\);').findall(r_game)[0]
            r_hls = requests.get(base_url + "/gethls.php?idgstream=%s&serverid=%s&cid=%s" % (quote(re_vidgstream, safe=""), re_gethlsUrl[0], re_gethlsUrl[1]), headers={"User-Agent": self.user_agent, "Referer": url, "X-Requested-With": "XMLHttpRequest"}).text
        else:
            r_hls = requests.get(base_url + "/gethls.php?idgstream=%s" % quote(re_vidgstream, safe=""), headers={"User-Agent": self.user_agent, "Referer": url, "X-Requested-With": "XMLHttpRequest"}).text
        json_hls = json.loads(r_hls)
        m3u8 = json_hls["rawUrl"]
        if m3u8 == None:
            raise "no link found"
        else:
            m3u8 = Link(address=m3u8.replace(".m3u8", ".m3u8?&Connection=keep-alive"), headers={"Referer": url})
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

    def get_games(self):
        games: List[Game] = []
        r = requests.get(f"http://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.navbar-nav > li > a")
        for category in categories:
            try:
                league = category.text.replace(" Streams", "")
                href = category.get("href")
                r_category = requests.get(href).text
                soup = BeautifulSoup(r_category, "html.parser")
                for game in soup.find_all("a", class_="btn-block"):
                    try:
                        url = game.get("href")
                        icon = game.find("img").get("src")
                        title = game.find("h4").text.strip()
                        time_str = game.find("p").text.strip()
                        utc_time = None
                        if time_str != "":
                            if "LIVE" in time_str:
                                utc_time = datetime.now(timezone.utc)
                            else:
                                utc_time = datetime(*(time.strptime(time_str, "%a %d %b %Y %I:%M %p EST")[:6])) + timedelta(hours=5)
                        games.append(Game(title=title, links=[Link(address=url)], icon=icon, league=league, starttime=utc_time))
                    except Exception as e:
                        continue
            except:
                continue
        return games