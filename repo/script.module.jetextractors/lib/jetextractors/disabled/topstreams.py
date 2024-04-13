import re, requests, math, json
from random import random
from bs4 import BeautifulSoup
import dateutil

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Topstreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["topstreams.info"]
        self.name = "Topstreams"
        self.short_name = "TS"

    def get_link(self, url):
        page_data = requests.get(url).text
        server = re.findall(r'-1\';\s*var server=\'([^\']*)', page_data)[0]
        key = self.get_key(page_data)
        return Link("http://%s/%s.m8" % (server, key))

    def get_key(self, page_data):
        alledges = json.loads(re.compile(r"var alledges=({.+?});").findall(page_data)[0])
        edges = {}
        for vkey in alledges:
            if vkey != "primary" and int(alledges[vkey]) < 1000:
                edges[vkey] = alledges[vkey]

        if len(edges.keys()) == 0:
            for vkey in alledges:
                if vkey != "primary":
                    edges[vkey] = alledges[vkey]

        edgeslength = len(edges.keys()) - 1
        randomIndex = int(math.floor(random() * edgeslength))
        key = list(edges.keys())[randomIndex]
        return key

    def get_games(self):
        games = []
        base_url = "http://topstreams.info"
        r_home = requests.get(base_url).text
        soup_home = BeautifulSoup(r_home, "html.parser")
        for game in soup_home.select("div.item.upcoming"):
            try:
                title = game.select_one("div.home div.name").get_text() + " vs. " + game.select_one("div.away div.name").get_text()
                icon = game.select_one("div.away img.teamlogo").get("src")
                time = dateutil.parser.parse(re.compile(r"moment\('(.+?)'\)").findall(str(game))[0])
                href = game.select_one("div.list a.item").get("href")
                games.append(Game(title=title, links=[Link(href)], icon=icon, starttime=time))
            except:
                continue
        return games