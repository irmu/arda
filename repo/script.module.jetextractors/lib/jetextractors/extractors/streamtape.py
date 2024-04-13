import requests
import datetime
import re
from bs4 import BeautifulSoup
from base64 import b64decode
from typing import List
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link

class Streamtape(Extractor):
    domains = ["streamtape.com"]
    name = "Streamtape"

    def get_link(self, url):
        r = requests.get(url, headers={"User-Agent": self.user_agent, "Referer": url}).text
        script = re.findall(r"getElementById\('norobotlink'\)\.innerHTML = (.+?);<", r)[0]
        substrs = re.findall(r"\.substring\((.+?)\)", script)
        script = script[:script.index(".", 36)]
        for s in substrs:
            script = script + f"[{s}:]"
        link = "https:" + eval(script)
        return Link(link, headers={"User-Agent": self.user_agent})

