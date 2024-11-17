import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from ..models import *
from ..util import find_iframes


class Elixx(JetExtractor):
    def __init__(self) -> None:
        self.domains = ["www.elixx.xyz"]
        self.name = "Elixx"
        self.short_name = "ELI"


    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = []
        if self.progress_init(progress, items):
            return items
        
        r = requests.get(f"https://{self.domains[0]}/schedule.html", timeout=self.timeout).text
        soup = BeautifulSoup(r, "html.parser")
        for button in soup.select("button.accordion"):
            title = button.text
            panel = button.next_sibling.next_sibling
            links = [JetLink(link.get("href"), name=link.text) for link in panel.select("a")]
            items.append(JetItem(title, links))
        return items
    
    
    def get_link(self, url: JetLink) -> JetLink:
        iframes = [JetLink(u) if not isinstance(u, JetLink) else u for u in find_iframes.find_iframes(url.address, "", [], [])]
        link = next(filter(lambda x: "m3u8" in x.address, iframes))
        link.headers["Origin"] = "https://" + urlparse(link.headers["Referer"]).netloc
        return link