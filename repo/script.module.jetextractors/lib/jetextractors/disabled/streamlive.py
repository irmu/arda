import requests, re

from ..models.Extractor import Extractor
from ..models.Link import Link

class Streamlive(Extractor):
    def __init__(self) -> None:
        self.domains = ["streamlive.to"]
        self.name = "Streamlive"
        self.short_name = "SL"

    def get_link(self, url):
        r = requests.get(url, headers={"User-Agent": self.user_agent}).text
        vars = re.findall("var\s*([^\s=]+)\s*=\s*(\[[^\]]+\])\s*;", r)
        var_map = {}
        for v in vars: var_map[v[0]] = "".join(eval(v[1]))
        ids = re.findall('id\s*=\s*([^<]+)>([^<]+)', r)
        id_map = {}
        for i in ids: id_map[i[0]] = i[1]
        info = re.findall('(\[[^\]]+\]).join.+? \+\s*([a-zA-Z]+).join.+?\+.+?document.getElementById\([\"\']([^\"\']+)', r)[0]
        server = "https:" + "".join(eval(info[0])).replace('\\/','/')
        m3u8 = server + var_map[info[1]] + id_map[info[2]]
        return Link(m3u8, headers={"Referer": url})
