import requests, re, time, json, datetime
from urllib.parse import urlparse

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Zuzz(Extractor):
    def __init__(self) -> None:
        self.domains = ["zuzz.tv", "vip.realtvs.tv", "api.zuzz.tv"]
        self.name = "Zuzz"

    def get_games(self):
        games = []
        uuids = {
            "Channels": ("8d615535", None),
            "NFL": ("e889a4fb", "d4d986e8"),
            "MLB": ("bdcbe0d4", "39c497e9"),
            "NBA": ("104a40f5", "7281de84"),
            "NHL": ("e21e0c55", "4f452860"),
            "Boxing": ("ed41106a", "f415efb9"),
            "MMA": ("4c295b23", "3f7a342d"),
            "F1": ("2a6592f5", "7bcf26a6"),
        }

        for category, uuid in uuids.items():
            r = requests.post(f"https://api.{self.domains[0]}/leagues/streams", params={"timestamp": int(time.time() * 1000)}, files={"league_uuid": (None, uuid[0])}).json()
            for item in r:
                if item["stream"] == "!":
                    continue
                name = item["name"]
                href = re.findall(r'iframe src="(.+?)"', item["stream"])[0]
                img = f"https://assets.{self.domains[0]}/{item['icon']}"
                games.append(Game(name, links=[Link(href)], icon=img, league=category))
            
            if uuid[1] is not None:
                r_events = requests.get(f"https://api.{self.domains[0]}/events/v3/sorted-and-published", params={"timestamp": int(time.time() * 1000), "days": 6, "sport_uuid": uuid[1]}).json()
                for event in r_events:
                    event = json.loads(event)
                    name = event["title"]
                    event_uuid = event["uuid"]
                    href = f"https://api.zuzz.tv/events/streams|{event_uuid}"
                    starttime = datetime.datetime.fromtimestamp(event["start_time"]) + datetime.timedelta(hours=7)
                    home = json.loads(event["participantHome"])
                    away = json.loads(event["participantAway"])
                    name = f"{away['name']} @ {home['name']}"
                    games.append(Game(name, links=[Link(href, is_links=True)], league=category, starttime=starttime))
        return games

    def get_link(self, url):
        r = requests.get(url, headers={"User-Agent": self.user_agent, "Referer": f"https://{self.domains[0]}/"}).text
        m3u8 = re.findall(r'file: [\'"](.+?)[\'"]', r)[0]
        return Link(m3u8, headers={"User-Agent": self.user_agent, "Referer": url})
    
    def get_links(self, url):
        links = []
        split = url.split("|")
        uuid = split[1]
        url = split[0]
        r = requests.post(url, params={"timestamp": int(time.time() * 1000)}, files={"event_uuid": (None, uuid)}).json()
        for collection in r:
            try:
                for site in collection["collection"].values():
                    for link in site:
                        stream = link["stream"]
                        if "iframe" in stream:
                            stream = re.findall(r'iframe.+?src="(.+?)"', stream)[0]
                        links.append(Link(stream, name=f"{urlparse(stream).netloc}: {link['name']}/{link.get('tvlist_title', link.get('description'))}"))
            except:
                pass
        return links