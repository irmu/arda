import requests, re
from bs4 import BeautifulSoup
from ..models import *
from ..util import m3u8_src

class Sportea(JetExtractor):
    def __init__(self) -> None:
        self.domains = ["s1.sportea.link"]
        self.name = "Sportea"

    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = []

        r = requests.get(f"https://{self.domains[0]}", timeout=self.timeout).text
        soup = BeautifulSoup(r, "html.parser")
        for table in soup.select("div.p-4 > div.row"):
            league = table.select_one("h5").text.upper()
            for game in table.select("tbody > tr"):
                data = game.select("td")
                time = data[1].text
                title = data[2].text.split("\n")[0].strip()
                href = "https:" + data[-1].select_one("a").get("href")
                items.append(JetItem(title, links=[JetLink(href)], league=league))
        return items

    def get_link(self, url: JetLink) -> JetLink:
        m3u8 = m3u8_src.scan_page(url.address.replace("embed.php", "channel.php"), headers={"Referer": url.address})
        return JetLink(m3u8.address, headers={"Referer": f"https://{self.domains[0]}/"})