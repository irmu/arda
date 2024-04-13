import requests, re

from ..models.Extractor import Extractor
from .plytv import PlyTv

class Embedstream(Extractor):
    def __init__(self) -> None:
        self.domains = ["embedstream.me"]
        self.name = "Embedstream"

    def embedstream(self, id):
        r_embedstream = requests.get("https://embedstream.me/" + id).text
        zmid = re.compile(r'zmid = "(.+?)"').findall(r_embedstream)[0]
        game_cat = re.findall(r'gameCat="(.+?)"', r_embedstream)[0]
        return PlyTv().plytv_sdembed(game_cat, zmid, "https://embedstream.me/")

    def get_link(self, url):
        return self.embedstream(url.replace("https://embedstream.me/", ""))