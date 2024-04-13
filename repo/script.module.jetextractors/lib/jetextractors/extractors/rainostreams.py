import requests, re, datetime, time
from dateutil import parser
from ..util.m3u8_src import scan_page

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..icons import icons

class Rainostreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["epllive.net", "bdnewszh.com", "embed4u.xyz"]
        self.name = "Rainostreams"
        self.short_name = "RS"

    def get_link(self, url):
        if "epllive" in url:
            if "?sport" in url:
                url = url.split("?sport")[2]
            url = url.replace("https", "http")
            if "/embed" not in url:
                url = url.replace(self.domains[0], f"{self.domains[2]}/embed") + ".php"
        m3u8 = scan_page(url, headers={"User-Agent": self.user_agent, "Referer": f"http://{self.domains[2]}/"})
        if m3u8 != None:
            headers = {
                "Origin": f"http://{self.domains[2]}",
                "Referer": f"http://{self.domains[2]}/",
                "User-Agent": self.user_agent
            }
            if requests.head(m3u8.address, headers=headers).status_code == 401:
                headers = {
                    "Origin": f"https://{self.domains[2]}",
                    "Referer": f"https://{self.domains[2]}/",
                    "User-Agent": self.user_agent
                }
            m3u8.is_hls = True
            m3u8.headers = headers
        return m3u8

    def get_games(self):
        games = []
        leagues = ["nba", "soccer", "ncaaf", "rugby", "racing", "cricket", "mma"]
        for league in leagues:
            try:
                r = requests.get(f"https://streamsapi.xyz/api/{league}").json()
                for event in r["events"]:
                    game_title = event["title"]
                    game_time = event["kickOff"]
                    utc_time = datetime.datetime(*(time.strptime(game_time, "%Y-%m-%dT%H:%M:%S.000Z")[:6]))
                    if event["stream"] != "":
                        link = Link(f"https://{self.domains[2]}/embed/{league}/{event['stream']}.php")
                    else:
                        link = Link(f"https://{self.domains[2]}/embed/{league}/{game_title.split()[-1].lower()}.php")
                    games.append(Game(icon=icons[league.lower()] if league.lower() in icons else None,
                  title=game_title,
                        links=[link],
                        starttime=utc_time,
                        league=league.upper()
                    ))
            except:
                continue
        
        leagues = ["nfl", "mlb"]
        for league in leagues:
            try:
                r = requests.get(f"https://streamsapi.xyz/api/{league}/schedule").json()
                for event in r["results"]:
                    game_title = f"{event['home']['name']}"# vs. {event['away']['name']}
                    utc_time = datetime.datetime.fromtimestamp(int(event["time"])) - datetime.timedelta(hours=17)
                    link = Link(f"https://{self.domains[2]}/embed/{league}/{game_title.split()[-1].lower()}.php")
                    games.append(Game(
                        title=game_title,
                        links=[link],
                        starttime=utc_time,
                        league=league.upper()
                    ))
            except:
                continue
        
        return games