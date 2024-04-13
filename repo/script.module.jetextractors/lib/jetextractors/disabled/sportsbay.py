import requests, time, re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from . import daddylive, wstream

class SportsBay(Extractor):
    def __init__(self) -> None:
        self.domains = ["sportsbay.sx"]
        self.name = "SportsBay"
        self.short_name = "SB"

    # def get_games(self):
    #     games = []
    #     current_date = datetime.now()
    #     i = 1
    #     while (len(games) == 0 or (games[-1]["time"] - timedelta(hours=3)).day <= current_date.day) and i < 10:
    #         r = requests.get(f"https://{domain[0]}/page/{i}").text
    #         soup = BeautifulSoup(r, "html.parser")
            
    #         for game in soup.select("tr"):
    #             try:
    #                 if "date" in game.attrs["class"]: continue
    #                 game_title = game.select_one("a.summary").text
    #                 game_time = datetime(*(time.strptime(game.select_one("span.value-title").get("title"), "%Y-%m-%dT%H:%M+00:00")[:6]))
    #                 league = game.select_one("td.type").select_one("img").get("alt")
    #                 game_id = game.get("id")
    #                 game_icon = "https:" + game.select_one("td.type").select_one("img").get("src")
    #                 game_description = game.select_one("a.description").text.strip()
    #                 try: teams = [re.findall(r"List (.+?) events", team.get("title"))[0] for team in game.select("a.team")]
    #                 except: teams = []
    #                 games.append({
    #                     "title": game_title,
    #                     "links": [
    #                         f"https://freefeds.com/stream/{game_id}.html",
    #                         f"https://freefeds.com/stream/2/{game_id}.html",
    #                         f"https://freefeds.com/stream/3/{game_id}.html"
    #                     ],
    #                     "icon": game_icon,
    #                     "league": f"{league} ({game_description})",
    #                     "time": game_time,
    #                     "teams": teams
    #                 })
    #             except:
    #                 continue
    #         if len(games) == 0: break
    #         i += 1
    #     return games

    def get_link(self, url):
        r = requests.get(url).text
        embed = re.findall(r'<iframe+?src="(.+?)"', r)[0]
        if "daddylive" in embed:
            return daddylive.Daddylive().get_link(embed)
        else:
            r_casptv = requests.get(embed).text
            rowsports = re.findall(r'iframe.+?src="(.+?)"', r_casptv)[0]
            r_rowsports = requests.get(rowsports).text
            if "fid" in r_rowsports:
                fid = re.findall(r'fid="(.+?)"', r_rowsports)[0]
                r_pkcast = requests.get(f"https://www.pkcast123.me/footy.php?player=desktop&live={fid}&vw=740&vh=416", headers={"Referer": "https://1rowsports.com"}).text
                m3u8 = "".join(eval(re.findall(r"return\((\[.+?\])", r_pkcast)[0])).replace("\\", "")
                return Link(address=m3u8, headers={"Referer": "https://www.pkcast123.me/"})
            elif "wigistream" in r_rowsports:
                wigi = re.findall(r'<iframe src="(.+?)"', r_rowsports)[0]
                return wstream.Wstream().get_link(wigi + "|Referer=" + rowsports)

    def get_links(self, url):
        r = requests.get(url).text
        re_videos = re.findall(r"\"title\":\"(.+?)\".+?\"code\":\"(.+?)\"", r)
        links = [Link(video[1], name=video[0]) for video in re_videos]
        return links

    def get_games(self):
        games = []
        current_date = datetime.now()
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        
        for game in soup.select("tr"):
            try:
                if "date" in game.attrs["class"]: continue
                game_title = game.select_one("a.summary").text
                game_time = game.select_one("span.value-title").text.split(":")
                game_time = current_date.replace(hour=int(game_time[0]), minute=int(game_time[1])) + timedelta(hours=5)
                league = game.select_one("a.description").text.strip()
                game_icon = "https:" + game.select_one("img").get("src")
                game_description = game.select_one("a.description").text.strip()
                game_href = re.findall(r"location\.href='(.+?)';", game.get("onclick"))[0]
                games.append(Game(title=game_title, links=[Link(address=f"https://{self.domains[0]}{game_href}", is_links=True)], icon=game_icon, league=f"{league} ({game_description})", starttime=game_time))
            except:
                continue
        return games

