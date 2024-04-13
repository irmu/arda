from datetime import datetime, timedelta

from ..util import m3u8_src
from ..models.Extractor import Extractor
from ..models.Link import Link
from ..models.Game import Game
from . import embedstream, nbastreams, vecdn, cloudstream
import requests, re
from dateutil.parser import parse
from bs4 import BeautifulSoup

class FreeStreamsLive(Extractor):
    def __init__(self) -> None:
        self.name = "FreeStreamsLive"
        self.domains = [".+freestreams-live1.com"]
        self.domains_regex = True
    
    def get_links(self, url):
        r = requests.get(url).text
        iframe = re.findall(r'iframe loading="lazy".+src="(.+?)"', r)[0]
        if "embedstream" in iframe:
            return [embedstream.Embedstream().get_link(iframe)]
        elif "freestreams" in iframe:
            return nbastreams.NBAStreams().get_links(iframe)
        elif "nba-streams" in iframe or self.domains[0] in iframe:
            return nbastreams.NBAStreams().get_links(iframe)
        elif "vecdn.pw" in iframe or "castfree.me" in iframe:
            return [vecdn.VeCDN().get_link(iframe)]
        elif "casadelfutbol.net" in iframe:
            r = requests.get(iframe).text
            iframe = re.findall(r'<iframe.+?src="(.+?)"', r)[0]
            return [cloudstream.CloudStream().get_link(iframe)]
        else:
            return [Link(url)]
    
    def get_link(self, url):
        try:
            return nbastreams.NBAStreams().get_link(url)
        except:
            r = requests.get(url).text
            iframe = re.findall(r'iframe loading="lazy".+src="(.+?)"', r)[0]
            if "http://cricfree.live/live/embed" in iframe:
                iframe = iframe.replace("http://cricfree.live/live/embed", "http://cricplay2.xyz")
            elif "showsport.xyz" in iframe:
                r = requests.get(iframe).text
                if "window.atob" in r:
                    return m3u8_src.scan_page(iframe, r)
                else:
                    iframe = re.findall(r'iframe src="(.+?)"', r)[0].replace("http://cricfree.live/live/embed", "http://cricplay2.xyz")
            if iframe.startswith("//"):
                iframe = "http:" + iframe
            if "casadelfutbol.net" in iframe:
                r = requests.get(iframe).text
                iframe = re.findall(r'<iframe.+?src="(.+?)"', r)[0]
                return cloudstream.CloudStream().get_link(iframe)
            else:
                return vecdn.VeCDN().get_link(iframe)
    
    def get_games(self):
        games = []
        leagues = ["Home", "Football", "MMA", "Boxing", "Tennis", "Motorsports", "Rugby", "Euroleague", "WWE / AEW", "AFL", "CFL"]
        r = requests.get("https://" + self.domains[0].replace(".+", "sc.")).text
        soup = BeautifulSoup(r, "html.parser")
        leagues_lower = [league.lower() for league in leagues]
        for tab in soup.select("ul#menu-primary-menu > li"):
            tab_league = tab.text.strip()
            if tab_league.lower() in leagues_lower:
                tab_href = tab.select_one("a").get("href")
                r_tab = requests.get(tab_href).text
                soup_tab = BeautifulSoup(r_tab, "html.parser")
                if soup_tab.select_one("table") is not None:
                    game_date = re.findall(r'<h2 class="elementor-heading-title elementor-size-large">(.+?)<\/h2>', r)[0].split(", ")[-1]
                    soup_tab = soup_tab.select_one("table")
                    for game in soup_tab.select("tr")[1:]:
                        game_time = game.select_one("td.matchtime").text.strip() if game.select_one("td.matchtime") != None else datetime.now().strftime("%H:%M")
                        game_icon = game.select_one("img").get("src")
                        game_name = game.select_one("td.event-title").text.strip().replace("\n", " ")
                        if "LINK" in game_name: game_name = game_name.split("LINK")[0]
                        game_utc = parse(f"{game_date} {game_time}") + timedelta(days=1)
                        games.append(Game(title=game_name, links=[Link(address=href.get("href"), is_links=True, name=href.text) for href in game.select("a")], icon=game_icon, league=tab_league.capitalize(), starttime=game_utc))
                else:
                    game_date = soup_tab.select_one("h2.elementor-heading-title").text.split(", ")[-1]
                    for game in soup_tab.select("section.elementor-section"):
                        try:
                            try: game_time = game.select_one("p").text.strip().replace("ET", "")
                            except: game_time = None
                            try: game_icon = game.select_one("img").get("src")
                            except: game_icon = None
                            if game.select_one("span.name") != None:
                                game_name = game.select_one("span.name").text
                            else:
                                try: game_name = game.select_one("h2").text
                                except: continue
                            game_name = game_name.replace("\n", "")
                            if "GMT" in game_name: continue
                            if game_time != None and game_time != "": game_utc = parse(f"{game_date} {game_time}") + timedelta(hours=5)
                            else: game_utc = None
                            href = [Link(address=href.get("href"), is_links=True, name=href.text) for href in game.select("a")]
                            if len(href) == 0: continue
                            games.append(Game(title=game_name, links=href, icon=game_icon, league=tab_league.capitalize(), starttime=game_utc))
                        except:
                            continue
        return games