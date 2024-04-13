import requests, re
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Template(Extractor):
    def __init__(self) -> None:
        self.domains = ["example.com"]
        # self.name = "Template"
        # self.short_name = "TP"

    def get_games(self):
        games = []
        return games

    def get_link(self, url):
        return Link()