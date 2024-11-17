import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import timedelta, datetime
from ..models import *
from ..util import find_iframes
from ..icons import icons


class Sol(JetExtractor):
    def __init__(self) -> None:
        self.domains = ["bestsolaris.com"]
        self.name = "Sol"
        self.short_name = "MS"


    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = []
        if self.progress_init(progress, items):
            return items
        
        leagues = ["nba", "mlb", "nhl", "mma", "boxing", "cfb", "motor-sports"]#,"mma","boxing","nfl","cfb","motor-sports"
        for league in leagues:
            if self.progress_update(progress, league):
                return items
            
            r = requests.get(f"https://{self.domains[0]}/category/"+league+"streams", timeout=self.timeout).text
            soup = BeautifulSoup(r, "html.parser")
            for game in soup.find_all("li", {"class": "f1-podium--item"}):
                href = game.find("a").get("href")
                title = game.find("span",{"class": "f1-podium--driver f1--xs MacBaslik"}).text.strip()
                time = game.find("span",{"class": "f1-podium--time f1-label f1-bg--gray2 misc--label text-semi-bold MacBaslikSagTarih"}).text.strip()
                utc_time = None
                if time != "":
                    try:
                        utc_time = parse(time) + timedelta(hours=5)
                    except:
                        try:
                            utc_time = datetime.strptime(time, "%H:%M %p ET - %m/%d/%Y") + timedelta(hours=5)
                        except:
                            pass
                items.append(JetItem(icon=icons[league.lower()] if league.lower() in icons else None,league=league.upper(),title=title, links=[JetLink(address=href)], starttime=utc_time ))
        return items
                
        
    def get_link(self, url: JetLink) -> JetLink:
        iframes = [JetLink(u) if not isinstance(u, JetLink) else u for u in find_iframes.find_iframes(url.address, "", [], [])]
        return iframes[0]