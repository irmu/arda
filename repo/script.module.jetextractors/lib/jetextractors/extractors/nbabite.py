import requests, re, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

from ..models.Extractor import Extractor
from urllib.parse import urlparse

from ..models.Game import Game
from ..models.Link import Link
from ..util import sportscentral_streams

class NBABite(Extractor):
    def __init__(self) -> None:
        self.domains = ["nbabite.com", "nflbite.com", "nhlbite.com", "mlbbite.net", "live1.formula1stream.cc", "mmabite.app", "tonight.boxingstreams.cc", "wwestreams.cc"]
        self.name = "NBAbite"
        self.short_name = "NBAB"

    def get_games(self):
        def __get_games(site):
            games = []
            try:
                r = requests.get("https://" + site).text
                soup = BeautifulSoup(r, "html.parser")
                if soup.select_one("div.justify-between > strong"):
                    date = datetime(*(time.strptime(soup.select_one("div.justify-between > strong").text.strip(), "%a %d %b %Y")[:6]))
                else:
                    date = datetime.now()
                other_sites = soup.select("a.other-site") + soup.select("a.rounded-xl")
                league = ""
                for other_site in other_sites:
                    if urlparse(other_site.get("href")).netloc.replace("www.", "") == site:
                        league = (other_site.select_one("div.site-name") or other_site).text.strip().replace(" Streams", "").replace("Bite", "")
                if "mlb" in site:
                    for competition in soup.select("div.competition"):
                        team_names = [team.text.strip() for team in competition.select("span.name")]
                        title = f"{team_names[0]} vs. {team_names[1]}"
                        href = competition.select_one("a").get("href")
                        games.append(Game(title=title, league=f"MLB", links=[Link(address=href, is_links=True)]))
                else:
                    for game in soup.select("div.col-md-6"):
                        team_names = [team.text for team in game.select("div.team-name")]
                        title = "%s vs %s" % (team_names[0], team_names[1])
                        status = game.select_one("div.status")
                        game_time = None
                        # if "live-indicator" not in status.attrs["class"] and ":" in status.text:
                        #     split = status.text.split(":")
                        #     hour = int(split[0])
                        #     minute = int(split[1])
                        #     game_time = date.replace(hour=hour, minute=minute) + timedelta(hours=4)
                        # else:
                        #     title = "[COLORyellow]%s[/COLOR] - %s" % (status.text, title)
                        score = game.select("div.score")
                        if len(score) > 0 and score[0].text:
                            scores = [i.text for i in score]
                            title =  "%s [COLORyellow](%s-%s)[/COLOR]" % (title, scores[0], scores[1])
                        icon = game.select_one("img").get("src")
                        href = game.select_one("a").get("href")
                        games.append(Game(title=title, icon=icon, starttime=game_time, league=league, links=[Link(address=href, is_links=True)]))
                    for game in soup.select("div.grid-cols-1.gap-3 > div.col-span-1"):
                        team_names = [team.text for team in game.select("strong")]
                        if len(team_names) > 1:
                            title = "%s vs %s" % (team_names[0], team_names[1])
                            score = game.select("b")
                        else:
                            title = game.select_one("h5").text
                            score = []
                        
                        if len(score) > 0 and score[0].text:
                            scores = [i.text for i in score]
                            title =  "%s [COLORyellow](%s-%s)[/COLOR]" % (title, scores[0], scores[1])
                        icon = game.select_one("img").get("src")
                        href = "https://" + site + game.select_one("a").get("href")
                        games.append(Game(title=title, icon=icon, league=league, links=[Link(address=href, is_links=True)]))
            except:
                pass

            return games
        
        games = []
        with ThreadPoolExecutor() as executor:
            results = executor.map(__get_games, self.domains)
            for result in results:
                games.extend(result)
        
        return games

    def get_links(self, url):
        r = requests.get(url).text
        match_id = re.findall(r"var streamsMatchId = (.+?);", r)[0]
        match_sport = re.findall(r"var streamsSport = ['\"](.+?)['\"]", r)[0]
        return sportscentral_streams.get_streams(match_id, match_sport, self.domains[0])


