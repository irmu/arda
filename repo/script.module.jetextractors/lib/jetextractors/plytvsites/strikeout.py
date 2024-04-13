import requests, re, json, datetime, time
from bs4 import BeautifulSoup
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from .plytv import PlyTv
from concurrent.futures import ThreadPoolExecutor

class Strikeout(Extractor):
    domains = ["strikeout.im"]
    name = "Strikeout"

    def get_games(self):
        slugs = []
        def __get_games(sport_href):
            sport = sport_href[1]
            sport_href = sport_href[0]
            games = []
            r_sport = requests.get(f"https://{self.domains[0]}{sport_href}").text
            soup_sport = BeautifulSoup(r_sport, "html.parser")
            site_config = json.loads(re.findall(r"const siteConfig = (.+?);", r_sport)[0])
            for game in soup_sport.select("a.btn-primary"):
                game_id = game.get("aria-controls")
                game_slug = site_config["slugs"][game_id]
                if game_slug in slugs:
                    continue
                else:
                    slugs.append(game_slug)
                game_title = game.get("title")
                game_links = [Link(address=f"https://{self.domains[0]}/{sport_href[1:]}/{i+1}/{game_slug}-stream", name=f"{link['player']} - Link {i+1}") for i, link in enumerate(site_config["links"][game_id])]
                game_spans = game.find_all("span")
                if len(game_spans) > 1:
                    game_time = datetime.datetime(*(time.strptime(game_spans[-1].get("content"), "%Y-%m-%dT%H:%M")[:6])) - datetime.timedelta(hours=1)
                else:
                    game_time = None
                games.append(Game(title=game_title, links=game_links, league=sport, starttime=game_time))
            return games

        games = []
        hrefs = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        for sport_page in soup.select("div.col-xxl-2"):
            sport = sport_page.text
            sport_href = sport_page.select_one("a").get("href")
            if not sport_href.startswith("/"):
                continue
            hrefs.append((sport_href, sport))
        
        with ThreadPoolExecutor() as executor:
            results = executor.map(__get_games, hrefs)
            for result in results:
                games.extend(result)
            
        return games
    
    def get_link(self, url):
        r = requests.get(url).text
        zmid = re.findall(r'zmid = "(.+?)"', r)[0]
        game_cat = re.findall(r'gameCat="(.+?)"', r)[0]
        return PlyTv().plytv_sdembed(game_cat, zmid, url)