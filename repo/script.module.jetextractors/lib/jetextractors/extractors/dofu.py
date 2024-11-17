import requests, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from ..models import *
from ..util import find_iframes
from ..icons import icons
from .voodc import Voodc
from .givemenbastream import GiveMeNBAStreams
from .sportea import Sportea


class Dofu(JetExtractor):
    def __init__(self) -> None:
        self.domains = ["dofusports.xyz"]
        self.name = "Dofu"
    

    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = []
        if self.progress_init(progress, items):
            return items
        
        r = requests.get(f"http://{self.domains[0]}", timeout=self.timeout).text
        soup = BeautifulSoup(r, "html.parser")
        for category in soup.select('table'):
            league = category.select_one("th").text.split()[0]
            # print(f"--- {league} ---")
            for game in category.select("tbody > tr"):
                td = game.select("td")
                date = td[0].text
                
                date_time = datetime(*(time.strptime(date, "%B %d, %Y %H:%M")[:6])) - timedelta(hours=8)
                
                name = td[1].text
                href = game.find("a").get("href")
                sport = league
                

                    
                items.append(JetItem(icon=icons[league.lower()] if league.lower() in icons else None,
                  title=name,
                  league=sport,
                  starttime=date_time,
                  links=[JetLink(href)]))

        return items

    def get_link(self, url: JetLink) -> JetLink:
        iframes = [JetLink(u) if not isinstance(u, JetLink) else u for u in find_iframes.find_iframes(url.address, "", [], [])]
        link = iframes[0]
        if "giveme" in link.address:
            return GiveMeNBAStreams().get_link(link)
        if "voodc" in link.address:
            return Voodc().get_link(link)
        if "sportea" in link.address:
            return Sportea().get_link(link)
        if "freesportstime" in link.address:
            del link.headers["Referer"]
        return iframes[0]
    
