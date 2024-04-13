import requests, re, base64
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta, datetime

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.m3u8_src import scan_page
from ..util import jsunpack, find_iframes, hunter



from ..util.hunter import hunter
from ..util.m3u8_src import scan_page

class GiveMeReddit(Extractor):
    def __init__(self) -> None:
        self.domains = ["givemeredditstreams.xyz", "givemereddit.eu","official.givemeredditstream.cc","givemenbastreams.com", "givemenflstreams.com"]
        self.name = "Give Me"


    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")

        for league in soup.select("a.nav-link")[1:]:
            league_name = league.text
            print("\n" + league_name)
            r_league = requests.get(f"https://{self.domains[0]}{league.get('href')}").text
            soup_league = BeautifulSoup(r_league, "html.parser")
            for game in soup_league.select("a.matches"):
                href = game.get("href")
                if href.startswith("/"):
                    href = f"https://{self.domains[0]}" + href
                title = game.get("aria-label")
                if title == None:
                    if league_name == "MLB":
                        teams = game.select("span.team-name")
                        title = f"{teams[0].text} vs {teams[1].text}"
                    else:
                        title = game.text.strip()
                        print(title)
                icon = game.select_one("img")
                if icon != None:
                    icon = icon.get("src")
                
                games.append(Game(title, links=[Link(href)], league=league_name, icon=icon))
        return games


    def get_link(self, url):
        r = requests.get(url).text
        re_iframe = re.findall(r'iframe class=\"embed-responsive-item\" src=\"(.+?)\"', r)
        if len(re_iframe) != 0:
            r = requests.get(re_iframe[0], headers={"User-Agent": self.user_agent, "Referer": url}).text
        re_hunter = re.findall(r'decodeURIComponent\(escape\(r\)\)}\("(.+?)",(.+?),"(.+?)",(.+?),(.+?),(.+?)\)', r)[0]
        deobfus = hunter(re_hunter[0], int(re_hunter[1]), re_hunter[2], int(re_hunter[3]), int(re_hunter[4]), int(re_hunter[5]))
        m3u8 = scan_page(url, deobfus)
        m3u8.headers["User-Agent"] = self.user_agent
        if len(re_iframe) != 0:
            m3u8.headers["Referer"] = re_iframe[0]
        return m3u8