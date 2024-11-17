



import requests,json
from bs4 import BeautifulSoup
from ..models import *
from ..util import find_iframes
from ..icons import icons
from urllib.parse import urlparse, quote
import xbmc
import os


class Weakspell(JetExtractor):
    def __init__(self) -> None:
        self.domains = ["methstreams.to"]
        self.name = "Weakspell/LiveOnScore"
        self.short_name = "CS"
    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = []
        if self.progress_init(progress, items):
            return items
        r = requests.get(f"https://{self.domains[0]}", timeout=self.timeout).text
        soup = BeautifulSoup(r, "html.parser")
        
        for extra in soup.select("div.col-xs-12"):
            game_items = extra.select("li.styled-list-item")
            for item in game_items:
                title = item.select_one("span.title_name").text.strip()
                href = item.find("a")["href"]
                sport = item.select_one("span.cat-name").text.strip()
                items.append(JetItem(icon=icons[sport.lower()] if sport.lower() in icons else None, league=sport.upper(), title=title, links=[JetLink(href)]))
        return items
    
    def get_link(self, url: JetLink) -> JetLink:
        base_url = "http://" + urlparse(url.address).netloc
        r_game = requests.get(url.address).text
        re_vidgstream = re.compile(r'var vidgstream = "(.+?)";').findall(r_game)[0]
        r_hls = requests.get(base_url + "/gethls.php?idgstream=%s" % quote(re_vidgstream, safe=""), headers={"User-Agent": self.user_agent, "Referer": url.address, "X-Requested-With": "XMLHttpRequest"}).text
        json_hls = json.loads(r_hls)
        m3u8 = json_hls["rawUrl"]
        if m3u8 is None:
            raise "no link found"
        else:
            m3u8 = JetLink(address=m3u8.replace(".m3u8", ".m3u8?&Connection=keep-alive"), headers={"Referer": url.address})
        return m3u8

    