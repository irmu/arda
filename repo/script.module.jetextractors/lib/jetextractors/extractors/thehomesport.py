from typing import List
import requests, re, datetime
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class TheHomeSport(Extractor):
    def __init__(self) -> None:
        self.domains = ["thehomesport.com", "embedme.top"]
        self.name = "TheHomeSport"

    def get_games(self):
        games = []
        r = requests.get(f"https://{self.domains[0]}").text
        events = re.findall(r'category:"(?P<category>.+?)",title:"(?P<title>.+?)",href:"(?P<href>.+?)",date:new Date\((?P<date>.+?)\),popular:(?P<popular>.+?)}', r)
        sports = re.findall(r'id:"(.+?)",name:"(.+?)",href:"(.+?)",meta:"(.+?)",sub:(.+?)}', r)
        sports_map = {}
        for sport in sports:
            sports_map[sport[0]] = sport[1]
        sports_map["american-football"] = "American Football"
        for event in events:
            if event[0] not in sports_map:
                print(event[0])
                continue
            category = sports_map[event[0]]
            title = event[1]
            href = event[2]
            date = event[3]
            popular = event[4]
            games.append(Game(title, league=category, links=[Link(f"https://{self.domains[0]}{href}", is_links=True)], starttime=datetime.datetime.fromtimestamp(int(date) / 1000) if date != "NaN" else None))
        return games
    
    def get_links(self, url: str):
        r = requests.get(url)
        r.encoding = "utf8"
        streams = re.findall(r'stream:"(.+?)",streamNo:(.+?),hd:(.+?),language:"(.+?)"', r.text)
        links = [Link(f"https://{self.domains[1]}{stream[0].replace('/watch/', '/embed/')}", name=f"Stream {stream[1]} - {stream[3]}") for stream in streams]
        return links

    def get_link(self, url):
        r = requests.get(url).text
        info = re.findall(r'i="(.+?)",s="(.+?)",l=\["(.+?)"\],h="(.+?)"', r)[0]
            
        return Link(f"https://{info[2]}.{info[3]}/js/{info[0]}/{info[1]}/playlist.m3u8", headers={"Referer": url}, is_ffmpegdirect=True)