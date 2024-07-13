import requests, re
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.m3u8_src import scan_page
import xbmcgui

class Crackstream(Extractor):
    def __init__(self) -> None:
        self.domains = ["crackstreams.dev"]
        self.name = "Crackstreams"
        self.short_name = "CS"
    
    def get_link(self, url):
        m3u8 = ""
        video_html = requests.get(url).text
        video = BeautifulSoup(video_html, "html.parser")
        if len(video.find_all("iframe")) > 0:
            iframe = video.find("iframe").get("src")
            r_iframe = requests.get(iframe).text
            m3u8 = Link(address=re.compile(r"source: ['\"](.+?)['\"]").findall(r_iframe)[0].replace(".m3u8", ".m3u8?&Connection=keep-alive"))
        else:
            m3u8 = scan_page(url, video_html)
        # if "hdstreamss" in m3u8.address:
        #     m3u8.headers = {"Referer": "http://hdstreamss.club/"}
        # else:
        #     m3u8.headers = {"Referer": "http://crackstreams.biz/"}
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
        games = []
        r = requests.get(f"http://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul#primary-menu > li > a")[1:]
        for category in categories:
            league = category.text.replace(" streams", "")
            league_href = category.get("href")
            r_league = requests.get(league_href).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            for post in soup_league.select("article.post"):
                a = post.select_one("a")
                href = a.get("href")
                title = a.text.strip()
                time = post.select_one("div.entry-content").text.strip()
                if "Stream" in time:
                    continue
                utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time)
                    except:
                        pass
                games.append(Game(title=title, links=[Link(address=href)], icon="-", league=league, starttime=utc_time))
        return games
