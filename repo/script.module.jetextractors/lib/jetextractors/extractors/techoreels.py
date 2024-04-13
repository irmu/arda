import requests, re
from ..models.Extractor import Extractor
from ..models.Link import Link

class Techoreels(Extractor):
    def __init__(self) -> None:
        self.domains = ["techclips.net", "techoreels.com"]

    def __find_link(self, url, servers, serv_eval):
        for serv in servers:
            stream = eval(serv_eval)
            r_stream = requests.get(stream, headers={"Referer": url, "User-Agent": self.user_agent})
            if r_stream.status_code == 200:
                return Link(address=stream, headers={"Referer": url, "User-Agent": self.user_agent})

    def get_link(self, url):
        r = requests.get(url).text
        servers = re.findall(r'var servs = (\[.+?\]);', r)
        if len(servers) > 0:
            servers = eval(servers[0])
            serv_eval = re.findall(r"source: (.+?),", r)[0]
            return self.__find_link(url, servers, serv_eval)
        else:
            iframe = re.findall(r'iframe src="(.+?)"', r)[0]
            r_iframe = requests.get(iframe).text
            servers = eval(re.findall(r'var servs = (\[.+?\]);', r_iframe)[0])
            serv_eval = re.findall(r"source: (.+?),", r_iframe)[0]
            return self.__find_link(url, servers, serv_eval)