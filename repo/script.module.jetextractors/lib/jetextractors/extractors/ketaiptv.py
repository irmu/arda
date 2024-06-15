import requests, re
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import m3u8_src

class KetaIPTV(Extractor):
    def __init__(self) -> None:
        self.domains = ["ketaiptv.me"]
        self.name = "KetaIPTV"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}/search.php?search=+").text
        soup = BeautifulSoup(r, "html.parser")
        
        for item in soup.select("li.channel-item"):
            title = item.text.strip()
            if "PORN" in title.upper() or "XXX" in title.upper() or "18+" in title.upper() or "X4" in title or "VERIFIED" in title:
                continue
            
            img = item.select_one("img")
            img = img.get("src") if img else ""
            
            link = item.select("a")[-1].get("href")
            
            games.append(Game(title, [Link(link)], icon=img))
    
    
        games.sort(key=lambda game: game.title)
        
        return games

    def get_link(self, url):
        return m3u8_src.scan_page(url)