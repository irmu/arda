import requests, time
from datetime import datetime, timedelta
from urllib.parse import urlparse

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"



class Sportsurge(Extractor):
    def __init__(self) -> None:
        self.domains = ["sportsurge.net", "api.sportsurge.net"]
        self.name = "Sportsurge"
        self.short_name = "SS"
        self.ignore = ["streameast.live","dudestream.com","sportsbuzz.co","freesport.info","nbatvsport.com","tvsportslive.fr","sportinglive.co","bilasport.xyz","dubzstreams.com","freesportsforall.ml","bestnhl.com","soccerjumbotvs.me"]

    def __scrape_group(self, id, icon, category):
        games = []
        group_root = requests.get("https://%s/groups/list?parent=%s" % (self.domains[1], id)).json()
        if len(group_root["groups"]) == 0:
            event_list = requests.get("https://%s/events/list?group=%s" % (self.domains[1], id)).json()
            for event in event_list["events"]:
                game_time = ""
                if "description" in event and event["description"] != None and "ET" in event["description"]:
                    try:
                        event["description"] = event["description"][:event["description"].index(" |")]
                        date = datetime(*(time.strptime(event["description"], "%I:%M %p ET")[:6]))
                        game_time = datetime.now().replace(hour=date.hour, minute=date.minute) + timedelta(hours=4)
                    except Exception as e:
                        pass
                games.append(Game(title=event["name"], icon=icon, starttime=game_time, league=category, links=[Link("https://api.sportsurge.net/streams/list?event=" + str(event["id"]), is_links=True)]))
        else:
            for group in group_root["groups"]:
                games += self.__scrape_group(group["id"], icon, category)
        
        return games

    def get_games(self):
        games = []
        r = requests.get("https://%s/groups/list?parent=0" % self.domains[1], headers={"User-Agent": user_agent, "Referer": "https://" + self.domains[0]})
        root = r.json()
        for group in root["groups"]:
            category = group["name"]
            icon = "https://%s%s%s" % (self.domains[0], "/" if not group["imageurl"].startswith("/") else "", group["imageurl"]) if not group["imageurl"].startswith("http") else group["imageurl"]
            games += self.__scrape_group(group["id"], icon, category)
        return games

    def get_links(self, url):
        links = []
        stream_list = requests.get(url).json()
        for stream in stream_list["streams"]:
            stream_domain = urlparse(stream["url"]).netloc.replace("www.", "")
            if stream_domain not in self.ignore: 
                try: links.append(Link(stream["url"], name="%s %s%i@%ikbps" % (stream["name"], stream["resolution"], stream["framerate"], stream["bitrate"])))
                except: links.append(Link(stream["url"]))
        return links
