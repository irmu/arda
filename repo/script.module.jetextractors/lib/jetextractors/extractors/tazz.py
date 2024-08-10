import requests, re, time, json, datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Tazz(Extractor):
    def __init__(self) -> None:
        self.domains = ["tazz.tv", "full.realiptvs.com", "minum.realiptvs.com", "api.tazz.tv"]
        self.name = "Tazz"

    def get_games(self):
        uuids = {
            "Channels": ("a68c1287", None),
            "Soccer": ("53662bee", "8b84f073"),
            "Tennis": ("b8cbdefa", "b870c9a2"),
            "NFL": ("2090c62e", "d4d986e8"),
            "Basketball": ("b45797c0", "ebd43f84"),
            "Volleyball": ("63e95c34", "96230538"),
            "Handball": ("b8e3b0c2", "9c869ed1"),
            "Water Polo": ("5970fbd8", "8cca17c7"),
            "NBA": ("104a40f5", "7281de84"),
            "NHL": ("e21e0c55", "4f452860"),
            "MLB": ("bdcbe0d4", "248a0280"),
            "CFL": ("764e328f", "688fd539"),
            "F1": ("2a6592f5", "7bcf26a6"),
            "Boxing": ("ed41106a", "f415efb9"),
            "MMA": ("87caf79d", "3f7a342d"),
            "NCAAF": ("0a48805d", "68689ed4"),
            "NCAAB": ("7316f32d", "d3a02a28"),
            "Golf": ("95917238", "48d45d90"),
            "Rugby": ("d79a1631", "19f13fe4"),
            "Motorsports": ("ec2cdc35", "f7302e8f"),
            "Tour de France": ("5d9a63a9", "fe4ebb36"),
            "Athletics": ("0b2811ef", "f523679a"),
            "Ice Hockey": ("275decc4", "a8aa164c"),
            "Horse Racing": ("a6253c14", "ffadbd5c"),
            "Euroleague": ("8062aaac", "88241a03"),
        }

        def __get_games(info):
            games = []
            category = info[0]
            uuid = info[1]

            r = requests.post(f"https://api.{self.domains[0]}/leagues/streams", params={"timestamp": int(time.time() * 1000)}, files={"league_uuid": (None, uuid[0])}).json()
            for item in r:
                if item["stream"] == "!":
                    continue
                name = item["name"].replace("_tazz", "")
                href = re.findall(r'iframe src="(.+?)"', item["stream"])[0].replace("full", "minum").replace("premium", "tazzfree")
                img = f"https://assets.{self.domains[0]}/{item['icon']}"
                games.append(Game(name, links=[Link(href)], icon=img, league=category))
            
            if uuid[1] is not None:
                r_events = requests.get(f"https://api.{self.domains[0]}/events/v3/sorted-and-published", params={"timestamp": int(time.time() * 1000), "days": 6, "sport_uuid": uuid[1]}).json()
                for event in r_events:
                    if not event:
                        continue
                    event = json.loads(event)
                    name = event["title"]
                    event_uuid = event["uuid"]
                    href = f"https://api.{self.domains[0]}/events/streams|{event_uuid}"
                    starttime = datetime.datetime.fromtimestamp(event["start_time"]) + datetime.timedelta(hours=7)
                    home = json.loads(event["participantHome"])
                    away = json.loads(event["participantAway"])
                    name = f"{away['name']} @ {home['name']}"
                    games.append(Game(name, links=[Link(href, is_links=True)], league=category, starttime=starttime))
            
            return games

        games = []
        with ThreadPoolExecutor() as executor:
            results = executor.map(__get_games, uuids.items())
            for result in results:
                games.extend(result)

        return games

    def get_link(self, url):
        r = requests.get(url, headers={"User-Agent": self.user_agent, "Referer": f"https://{self.domains[0]}/"}).text
        m3u8 = re.findall(r'file:[\'"](.+?)[\'"]', r)[0]
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
                        if not link.get("name", "").endswith("_tazz"):
                            continue
                        if "iframe" in stream:
                            stream = re.findall(r'iframe.+?src="(.+?)"', stream)[0]
                        stream = stream.replace("full", "minum").replace("premium", "tazzfree")
                        links.append(Link(stream, name=f"{urlparse(stream).netloc}: {link['name']}/{link.get('tvlist_title', link.get('description'))}"))
            except:
                pass
        return links