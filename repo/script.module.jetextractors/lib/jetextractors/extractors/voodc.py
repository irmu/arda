import requests, re
from bs4 import BeautifulSoup
from ..util import jsunpack

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Voodc(Extractor):
    def __init__(self) -> None:
        self.domains = ["voodc.com"]
        self.name = "Voodc"
        self.short_name = "TP"
        self.user_agent = "Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"

    def get_link(self, url):
        r = requests.get(url, headers={"User-Agent": self.user_agent}).text
        script = "https:" + re.findall(r'" src="(.+?)"', r)[0]
        split = script.split("/")
        embed_url = f"https://voodc.com/player/d/{split[-1]}/{split[-2]}"
        r = requests.get(embed_url, headers={"User-Agent": self.user_agent}).text
        re_m3u8 = re.findall(r'"file": \'(.+?)\'',  r)
        if len(re_m3u8) > 0:
            m3u8 = re_m3u8[0]
        else:
            fid = re.findall(r"fid='(.+?)'", r)[0]
            r_player = requests.get(f"https://player.mycraft.click/{fid}").text
            re_packed = re.findall(r"(}\(.+)", r_player)[0]
            jameiei = jsunpack.unpack(re_packed)
            m3u8 = "".join(map(lambda x: chr(int(x)), re.findall(r"\[(.+)\]", jameiei)[0].split(",")))
        return Link(m3u8, headers={"User-Agent": self.user_agent})