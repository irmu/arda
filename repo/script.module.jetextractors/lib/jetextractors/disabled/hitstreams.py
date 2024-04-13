import requests, re
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Hitstreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["hitstreams.live", "ww.hitstreams.live"]
        self.name = "Hitstreams"
        self.short_name = "HS"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul.navbar-nav > li > a")
        for category in categories:
            league = category.text.replace(" Streams", "")
            league_href = category.get("href")
            if league_href.startswith("/"):
                league_href = f"https://{self.domains[0]}" + league_href
            r_league = requests.get(league_href).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            for body in soup_league.select("div.btn-block"):
                href = f"https://{self.domains[0]}/" + body.select_one("a").get("href")
                title = body.find("h4").text.strip()
                if body.find("h5") != None:
                    game_league = body.find("h5").text.strip()
                    if game_league == "No League":
                        game_league = league
                else:
                    game_league = league
                icon = (f"https://{self.domains[0]}/" + body.find("img").get("src").replace(" ", "%20")) if body.find("img") != None else ""
                games.append(Game(title=title, links=[Link(address=href)], icon=icon, league=game_league))
        return games
    
    def get_link(self, url):
        r = requests.get(url).text
        re_iframe = re.findall(r'iframe.+?src="(.+?)"', r)[0]
        r_iframe = requests.get(re_iframe, headers={"Referer": url}).text
        fid = re.findall(r'fid="(.+?)";', r_iframe)[0]
        embed_url = "https://lovesomecommunity.com/embedcr.php?player=desktop&live=" + fid
        r_embed = requests.get(embed_url, headers={"User-Agent": self.user_agent, "Referer": re_iframe}).text
        eval_url = ("".join(eval(re.findall(r"return\((\[.+?\])", r_embed)[0]))).replace("\\", "").replace("////", "//")
        return Link(eval_url, headers={"User-Agent": self.user_agent, "Referer": embed_url})