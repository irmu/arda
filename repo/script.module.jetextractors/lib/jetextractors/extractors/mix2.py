
import requests, re, time, json, datetime,base64
from bs4 import BeautifulSoup

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes
from ..util.hunter import hunter
from ..util.m3u8_src import scan_page
from ..util import m3u8_src
from .voodc import Voodc
from .givemereddit import GiveMeReddit
from urllib.parse import urlparse, quote

class Mix2(Extractor):
  
    def __init__(self) -> None:
        self.domains = ["yyyyy.xyz"]
        # self.name = "Mix2"
        
    

    

    def get_link(self, url):
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        link = iframes[0]
        if "giveme" in link.address:
            return GiveMeReddit().get_link(link.address)
        if "voodc" in link.address:
            return Voodc().get_link(link.address)
        if "freesportstime" in link.address:
            del link.headers["Referer"]
        return iframes[0]
