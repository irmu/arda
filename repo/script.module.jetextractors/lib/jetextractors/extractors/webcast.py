
import requests, re, datetime
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes
from ..icons import icons

class Webcast(Extractor):
    def __init__(self) -> None:
        self.domains = ["nbacast.com", "mlbwebcast.com","nhlwebcast.com","nflwebcast.com"]
        self.name = "Webcast"

    def get_games(self):
        games = []

        for domain in self.domains:
            r = requests.get(f"https://{domain}").text
            soup = BeautifulSoup(r, "html.parser")

            for game in soup.select("tr.singele_match_date "):
                if "mdatetitle" in game.attrs["class"]:
                    continue
                name = " ".join(game.select_one("td.teamvs").text.strip().replace("  ", " ").split(" ")[:3])
                if domain == "nbacast.com":
                    sport = "NBA"
                    name = f"[COLORaqua]{sport}: [/COLOR]" + name
                elif domain == "mlbwebcast.com":
                    sport = "MLB"
                    name = f"[COLORorange]{sport}: [/COLOR]" + name
                    
                elif domain == "nhlwebcast.com":
                    sport = "NHL"
                    name = f"[COLORyellow]{sport}: [/COLOR]" + name
                elif domain == "nflwebcast.com":
                    sport = "NFL"
                    name = f"[COLORlime]{sport}: [/COLOR]" + name    
                game_time = game.select_one("td.matchtime").text.strip().split(":")
                game_icon = game.select_one("img").get("src")
                hour = int(game_time[0])
                minute = int(game_time[1])
                utc_time = datetime.datetime.now().replace(hour=hour, minute=minute) + datetime.timedelta(hours=17)
                href = game.find("a").get("href")
                games.append(Game(title=name, starttime=utc_time, icon=icons[sport.lower()] if sport.lower() in icons else None, links=[Link(href, is_links=True)]))

        return games


    def get_links(self, url):
        
            
        regex_patterns = {
            "mlbwebcast.com": r"<a class=\"btn .+\" href=\"(https://mlbwebcast.com/stream/.+)\" target",
            "nhlwebcast.com": r"<a class=\"btn .+\" href=\"(https://nhlwebcast\.com/live/.+)\" target",
            "nbacast.com": r"<a class=\"btn .+\" href=\"(https://nbacast\.com/live/.+)\" target",
            "nflwebcast.com": r"<a class=\"btn .+\" href=\"(https://nflwebcast\.com/live/.+)\" target"
        }

        r = requests.get(url).text
        re_links = []

        for domain, pattern in regex_patterns.items():
            if domain in url:
                re_links += re.findall(pattern, r)
        # elif url == "nbacast.com":
        #     re_links = re.findall(r"<a class=\"btn .+\" href=\"(https://nbacast\.com/live/.+)\" target", r)
        # elif url == "nflwebcast.com":
        #     re_links = re.findall(r"<a class=\"btn .+\" href=\"(https://nflwebcast\.com/live/.+)\" target", r)    
        iframes = []
        for link in re_links:
            iframes += [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(link, "", [], [])]
        for iframe in iframes:
            iframe.is_direct = True
            if "Referer" in iframe.headers and "bdnewszh.com" in iframe.headers["Referer"]:
                iframe.headers["Referer"] = "https://bdnewszh.com/"
        links = [link for link in iframes if "m3u8" in link.address]
        if len(links) >= 2:
            links[1].name = "Home"
            links[0].name = "Away"
        return links


