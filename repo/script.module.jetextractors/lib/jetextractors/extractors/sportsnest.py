
import requests, re, base64
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes

class SportsNest(Extractor):
    def __init__(self) -> None:
        self.domains = ["sportsnest.co"]
        self.name = "SportsNest"

    # def get_games(self):
    #     return self.get_games_page(1)
    
    # def get_games_page(self, page):
    #     page = int(page)
    #     games = []
    #     r = requests.get(f"https://{self.domains[0]}/page/{page}/?s=soccer").text
    #     soup = BeautifulSoup(r, "html.parser")

    #     for game in soup.find_all("a",class_="link"):#, class_="et4"): # Loop through each <a> element
    #         name = game.text
    #         if not name:
    #             continue
    #         href = game.get("href")
    #         games.append(Game(name,links=[Link(href)]))
    #     games.append(Game(f"Page {page + 1}", page=page + 1))
    #     return games
    
    def get_games_in_range(self, start_page, end_page):
        all_games = []

        for page in range(start_page, end_page + 1):
            games_on_page = self.get_games_page(page)
            if not games_on_page:
                break

            all_games.extend(games_on_page)

        return all_games

        
    def get_games(self):
        return self.get_games_in_range(1, 7)
    
    def get_games_page(self, page):
        page = int(page)
        games = []
        r = requests.get(f"https://{self.domains[0]}/page/{page}/?s=soccer").text
        soup = BeautifulSoup(r, "html.parser")

        for game in soup.find_all("a",class_="link"):#, class_="et4"): # Loop through each <a> element
            name = game.text
            if not name:
                continue
            href = game.get("href")
            games.append(Game(name,links=[Link(href)]))
        games.append(Game(f"Page {page + 1}", page=page + 1))
        return games

    def get_link(self, url):
        s = requests.Session()
        s.post(f"https://{self.domains[0]}/wp-content/plugins/litespeed-cache/guest.vary.php")
        r = s.get(url).text
        b64 = re.findall(r"src=\"data:text/javascript;base64,(.+?)\"", r)
        for b in b64:
            decoded = base64.b64decode(b).decode("utf-8")
            re_css = re.findall(r"src:'(.+?)'", decoded)
            if re_css:
                return Link(re_css[0], headers={"Referer": url})


