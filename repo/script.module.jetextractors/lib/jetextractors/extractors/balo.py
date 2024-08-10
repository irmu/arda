import requests, re, json
from bs4 import BeautifulSoup
from dateutil.parser import parse
from urllib.parse import urlparse, parse_qs, quote
from datetime import timedelta, datetime
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util.m3u8_src import scan_page
from ..util import jsunpack, find_iframes
from typing import List


class Balo(Extractor):
    def __init__(self) -> None:
        self.domains = ["balo.live", "cdn-rum.n2olabs.pro"]
        self.name = "Balo"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, 'html.parser')

        for sport in soup.select("div.list-match-sport-live-stream"):
            sport_title = sport.select_one("h3.title").text
            for game in sport.select("a.item-match"):
                if (t := game.select_one("div.txt-name")) is not None:
                    title = t.text.strip()
                else:
                    teams = game.select("div.txt-team-name")
                    title = f"{teams[0].text.strip()} vs {teams[1].text.strip()}"
                href = game.get("href")
                utc_time = datetime.fromtimestamp(int(game.select_one("span.txt_time").get("data-timestamp")))
                league = game.select_one("div.league-name > span").text
                games.append(Game(title, links=[Link(href, is_links=True)], starttime=utc_time, league=f"{sport_title} ({league})"))
        
        for item in soup.select('div.league-item.channel-item'):
            title = item['data-title']
            icon = item.select_one('div.league-logo img')['src']
            href = item.get('data-link', '')
            link = Link(parse_qs(urlparse(href).query)["m3u8"][0], headers={"Referer": f"https://{urlparse(href).netloc}/"}) if "m3u8" in href else Link(href)
            games.append(Game(title, links=[link], icon=icon))
        return games
    
    def get_links(self, url: str):
        r = requests.get(url).text
        match_info = json.loads(re.findall(r'var matchInfo = (.+?);', r)[0])
        me = requests.post(f"https://{self.domains[0]}/me").json()
        token = me["token_livestream"].split(".")
        link_format = f"https://{self.domains[1]}/stream.m3u8?url={{}}&token={token[0]}&is_vip={token[1]}&verify={quote(token[2])}"
        links = []
        for link in match_info["links"]:
            links.append(Link(link_format.format(quote(link["stream_link"], safe="")), unquote=False, is_ffmpegdirect=True, headers={"Referer": f"https://{urlparse(link['iframe_link']).netloc}/"}, name=link["display_name"], is_direct=True))
            # links.append(Link(link_format.format(link["stream_link"].replace("index.m3u8", f"chunks.m3u8?token={token[0]}&is_vip={token[1]}&verify={token[2]}")), headers={"Referer": f"https://{urlparse(link['iframe_link']).netloc}/"}, name=link["display_name"], is_direct=True))
        return links
    
    def get_link(self, url: str):
        if "/live-sport/" in url:
            return self.get_links(url)[0]
        else:
            tv_id = parse_qs(urlparse(url).query)["tv"][0]
            r = requests.get(url).text
            soup = BeautifulSoup(r, 'html.parser')
            tv = soup.select_one(f'div[data-slug="{tv_id}"]')
            href = tv.get("data-link")
            link = Link(parse_qs(urlparse(href).query)["m3u8"][0], is_ffmpegdirect=True, headers={"Referer": f"https://{urlparse(href).netloc}/"}) if "m3u8" in href else Link(href)
            return link

