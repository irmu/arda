import requests, re, base64,json
from bs4 import BeautifulSoup
from dateutil.parser import parse
from urllib.parse import urlparse
from datetime import timedelta, datetime

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.m3u8_src import scan_page
from ..util import jsunpack, find_iframes
from ..icons import icons

class Methstreams(Extractor):
    def __init__(self) -> None:
        
        self.domains = ["v1.methstreams.me"]
        self.name = "Methstreams"
        self.short_name = "MS"

    # def __init__(self) -> None:
    #     url = ''
    #     response = requests.get(url)
    #     config_data = json.loads(response.content)
    #     self.domains = config_data['Methstreams']
    #     self.name = "Methstreams"

    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        return iframes[0]
        
    # def get_link(self, url):
    #     m3u8 = ""
    #     video_html = requests.get(url).text
    #     video = BeautifulSoup(video_html, "html.parser")
    #     if len(video.find_all("iframe")) > 0:
    #         iframe = video.find("iframe").get("src")
    #         r_iframe = requests.get(iframe).text
    #         atob = re.findall(r'window.atob\("(.+?)"\)', r_iframe)[0]
    #         m3u8 = Link(address=base64.b64decode(atob).decode("utf-8"), headers={"User-Agent": self.user_agent, "Referer": iframe})
    #     else:
    #         m3u8 = scan_page(url, video_html)
    #     if m3u8 != None:
    #         m3u8.is_ffmpegdirect = True     
    #     return m3u8

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.navbar-nav > li > a")
        for category in categories:
            league = category.text.replace(" Streams", "")
            league_href = category.get('href')
            r_league = requests.get(league_href).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            league_games = soup_league.find_all("a", {"class": "btn-block"})
            for body in league_games:
                href = body.get("href")
                if href.startswith("/"):
                    href = f"https://{self.domains[0]}{href}"
                title = body.find("h4").text.strip()
                time = body.find("p").text
                utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time) + timedelta(hours=4)
                    except:
                        try:
                            utc_time = datetime.strptime(time, "%H:%M %p ET - %m/%d/%Y") + timedelta(hours=4)
                        except:
                            pass
                games.append(Game(icon=icons[league.lower()] if league.lower() in icons else None,
                  title=title, links=[Link(address=href)],  league=league, starttime=utc_time))
        return games
