import requests, re

from ..models.Link import Link
from ..models.Extractor import Extractor
from .weakspell import Weakspell
from .vecdn import VeCDN

class Cricfree(Extractor):
    def __init__(self) -> None:
        self.domains = ["cricfree.live"]

    def get_link(self, url):
        r = requests.get(url).text
        iframe = re.findall(r'iframe src="(.+?)"', r)[0].replace("https://cricfree.live/live/embed", "https://cricplay2.xyz")
        r_iframe = requests.get(iframe).text
        if "castfree" in r_iframe:
            return VeCDN().get_link(iframe)
        else:
            re_link = re.findall(r'iframe src="(.+?)"', r_iframe)[0]
            if "weakstream" in re_link:
                return Weakspell().get_link(re_link)
            else:
                return VeCDN().get_link(re_link)