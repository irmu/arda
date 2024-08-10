from typing import List
import requests, re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class AeSport(Extractor):
    def __init__(self) -> None:
        self.domains = ["aesport.tv"]
        self.name = "AeSport"

    def get_games(self):
        games = []

        # Games
        r = requests.get(f"https://{self.domains[0]}/fixture/all.html").text
        soup = BeautifulSoup(r, "html.parser")
        max_date = datetime.now() + timedelta(days=5)
        for game in soup.select("div.fixture-page-item"):
            team_left = game.select_one("span.name-team-left").text
            team_right = game.select_one("span.name-team-right").text
            title = f"{team_left} vs {team_right}"
            league = game.select_one("div.tournament").text.strip()
            utc_time = datetime.fromtimestamp(int(game.select_one(".time-format").get("data-time")) // 1000) + timedelta(hours=7)
            if utc_time > max_date:
                break
            href = game.select_one("a").get("href")
            games.append(Game(title, links=[Link(href, is_links=True)], league=league, starttime=utc_time))

        # Live TV
        r = requests.get(f"https://{self.domains[0]}/live-tv.html").text
        soup = BeautifulSoup(r, "html.parser")
        for section in soup.select("div.live-tv"):
            section_title = section.select_one("div.head-bar > div.left").text.strip()
            for channel in section.select("div.content > a"):
                href = channel.get("href")
                icon = channel.select_one("img.hide").get("src")
                title = channel.select_one("div.channel-name").text.strip()
                games.append(Game(title, links=[Link(href, is_links=True)], league=section_title, icon=icon))

        return games
    
    def get_links(self, url: str) -> List[Link]:
        links = []
        r = requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        flag = False
        for link in soup.select("a.link-channel"):
            l = clean_url(link.get("data-url"))
            # links.append(Link(l, name=link.text.strip(), headers={"Referer": f"https://{self.domains[0]}/", "User-Agent": self.user_agent}, is_direct=True))
            #if "$vipcdn.live" in l:
                #flag = True
            #else :
            links.append(Link(l, name=link.text.strip(), headers={"Referer": f"https://{self.domains[0]}/", "User-Agent": self.user_agent}, is_ffmpegdirect=True))
        """if flag:
            re_link = re.findall(r"var link = '(.+?)'", r)
            if re_link:
                links.append(Link(re_link[0], name=link.text.strip(), headers={"Referer": f"https://{self.domains[0]}/", "Origin": f"https://{self.domains[0]}", "User-Agent": self.user_agent}, is_direct=True))"""
        return links

def clean_url(url: str) -> str:
    return url.replace('https://live-tv.vipcdn.live', 'https://liveus1.score806.cc')