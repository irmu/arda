
import requests, re, base64
from bs4 import BeautifulSoup
from ..models import *
from ..icons import icons

class HDStreams(JetExtractor):
    def __init__(self) -> None:
        self.domains = ["www1.ihdstreams.xyz", "live.ihdstreams.xyz"]
        self.name = "HDStreams"


    def get_items(self, params: Optional[dict] = None, progress: Optional[JetExtractorProgress] = None) -> List[JetItem]:
        items = []
        if self.progress_init(progress, items):
            return items
        r = requests.get(f"https://{self.domains[0]}", timeout=self.timeout).text
        soup = BeautifulSoup(r, "html.parser")

        navbar = soup.find("nav")
        hrefs = navbar.find_all("a", class_="block")
        for sport in hrefs:
            if self.progress_update(progress):
                return items
            
            sport_href = sport.get("href")
            sport_name = sport.text.replace("STREAMS", "").replace("STREAM", "").replace("Streams", "").lower()
            sport_url = f"https://{self.domains[0]}{sport_href}"

            r = requests.get(sport_url, timeout=self.timeout).text
            re_iframe = re.findall(r'iframe.+?src="(.+?)"', r)[0]
            r = requests.get(re_iframe, headers={"Referer": sport_url}, timeout=self.timeout).text
            soup = BeautifulSoup(r, "html.parser")

            for game in soup.find_all("a", class_="w-full"):
                name = game.h3.get_text(strip=True)
                if not name:
                    continue
                href = game.get("href")
                items.append(JetItem(icon=icons[sport_name] if sport_name in icons else None,title=name, league=sport_name.upper(), links=[JetLink(href)]))
        return items

    
    def get_link(self, url: JetLink) -> JetLink:
        r = requests.get(url.address).text
        re_iframe = re.findall(r'iframe.+?src="(.+?)"', r)[0]
        
        r_iframe = requests.get(re_iframe, headers={"Referer": url.address}).text 
        re_iframe2 = re.findall(r'iframe.+?src="(.+?)"', r_iframe)[0].replace("embed.php", "channel.php").replace("Embed.php", "channel.php")

        if re_iframe2.startswith("//"):
            re_iframe2 = "https:" + re_iframe2
        r_iframe2 = requests.get(re_iframe2, headers={"Referer": re_iframe}).text 

        re_atob = re.findall(r"window.atob\('(.+?)'\)", r_iframe2)[0]
        link = base64.b64decode(re_atob).decode("ascii")
        if link.startswith("//"):
            link = "https:" + link
        return JetLink(link, headers={"Referer": re_iframe2, "User-Agent": self.user_agent})


