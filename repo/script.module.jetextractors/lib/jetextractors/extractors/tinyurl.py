
import requests, re

from ..models.Extractor import Extractor
from ..models.Link import Link
from ..util import hunter
from urllib.parse import unquote


class Tinyurl(Extractor):
    def __init__(self) -> None:
        self.domains = ["streamcheck.link"]
        self.shortener = True
    
    def get_link(self, url):
        r = requests.get(url).text
        link = re.findall(r"window.location.href = '(.+?)'", r)[0]
        return Link(link)
    