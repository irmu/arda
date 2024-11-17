import requests, re
from bs4 import BeautifulSoup
from dateutil.parser import parse

from ..models import *
from ..util.m3u8_src import scan_page

class Crackstream(JetExtractor):
    def __init__(self) -> None:
        self.domains = ["crackstreams.dev"]
        self.name = "Crackstreams"
        self.short_name = "CS"

    
    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = []
        if self.progress_init(progress, items):
            return items
        r = requests.get(f"http://{self.domains[0]}", timeout=self.timeout).text
        soup = BeautifulSoup(r, "html.parser")
        categories = soup.select("ul#primary-menu > li > a")[1:]
        for category in categories:
            if self.progress_update(progress):
                return items
            league = category.text.replace(" streams", "")
            league_href = category.get("href")
            r_league = requests.get(league_href, timeout=self.timeout).text
            soup_league = BeautifulSoup(r_league, "html.parser")
            for post in soup_league.select("article.post"):
                a = post.select_one("a")
                href = a.get("href")
                title = a.text.strip()
                time = post.select_one("div.entry-content").text.strip()
                if "Stream" in time:
                    continue
                utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time)
                    except:
                        pass
                items.append(JetItem(title=title, links=[JetLink(address=href)], icon="-", league=league, starttime=utc_time))
        return items
    

    def get_link(self, url: JetLink) -> JetLink:
        m3u8 = ""
        video_html = requests.get(url.address).text
        video = BeautifulSoup(video_html, "html.parser")
        if len(video.find_all("iframe")) > 0:
            iframe = video.find("iframe").get("src")
            r_iframe = requests.get(iframe).text
            m3u8 = JetLink(address=re.compile(r"source: ['\"](.+?)['\"]").findall(r_iframe)[0].replace(".m3u8", ".m3u8?&Connection=keep-alive"))
        else:
            m3u8 = scan_page(url.address, video_html)
        return m3u8
