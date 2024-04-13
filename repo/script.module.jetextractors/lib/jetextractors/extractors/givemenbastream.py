import requests, re

from ..models.Extractor import Extractor
from ..models.Link import Link
from ..util.hunter import hunter
from ..util.m3u8_src import scan_page

class GiveMeNBAStreams(Extractor):
    def __init__(self) -> None:
        self.domains = ["givemereddit.eu","official.givemeredditstream.cc","givemenbastreams.com", "givemenflstreams.com"]

    def get_link(self, url):
        r = requests.get(url).text
        re_iframe = re.findall(r'iframe class=\"embed-responsive-item\" src=\"(.+?)\"', r)
        if len(re_iframe) != 0:
            r = requests.get(re_iframe[0], headers={"User-Agent": self.user_agent, "Referer": url}).text
        re_hunter = re.findall(r'decodeURIComponent\(escape\(r\)\)}\("(.+?)",(.+?),"(.+?)",(.+?),(.+?),(.+?)\)', r)[0]
        deobfus = hunter(re_hunter[0], int(re_hunter[1]), re_hunter[2], int(re_hunter[3]), int(re_hunter[4]), int(re_hunter[5]))
        m3u8 = scan_page(url, deobfus)
        m3u8.headers["User-Agent"] = self.user_agent
        return m3u8