
import requests, re, time, json, datetime,base64
import xbmcgui
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes

from ..icons import icons




class Mgame(Extractor):
  
    def __init__(self) -> None:

        self.domains = ["mrgamingstreams.com/247-tv"]
        self.name = "Mgame"
        self.leagues = ["nhl","nba","mlb","nfl","soccer","fighting","motorsports","24-7"]
        
        
    

    def get_games(self):
        games = []
        
        
        
        for league in self.leagues:
            try:
                r = requests.get(f"http://mrgamingstreams.com/{league}").text
                soup = BeautifulSoup(r, "html.parser")

            
                game = soup.select("td.schedulefont2")
                for i in range(0, len(game), 3):
                    time = game[i].text.strip()
                    league_event=league.upper().replace("/","")
                    title = game[i + 1].text.strip()
                    
                    if league_event == "NBA":
                        title = f"{time}   [/COLOR] [COLORaqua]NBA: [/COLOR]{title}"
                    elif league_event == "MLB":
                        title = f"{time}   [COLORorange]MLB: [/COLOR]{title}"
                    elif league_event == "NHL":
                        title = f"{time}   [COLORyellow]NHL: [/COLOR]{title}"
                    elif league_event == "NFL":
                        title = f"{time}   [COLORlime]NFL: [/COLOR]{title}"

                    elif league_event == "SOCCER":
                        title = f"{time}   [COLORmagenta]SOCCER: [/COLOR]{title}"
                    elif league_event == "FIGHTING":
                        title = f"{time}   [COLORturquoise]FIGHTING: [/COLOR]{title}"
                    elif league_event == "MOTORSPORTS":
                        title = f"{time}   [COLORwheat]MOTORSPORTS: [/COLOR]{title}"    



                    hrefs = game[i + 2].find('a')['href'] if game[i + 2].find('a') else None
                    href = f"http://mrgamingstreams.com{hrefs}"
                    
                

                    
                    games.append(Game(icon=icons[league.lower()] if league.lower() in icons else None,title=title,links=[Link(href)]))
            except:
                continue    
        r = requests.get(f"https://{self.domains[0]}").text
        soup = BeautifulSoup(r, "html.parser")
        
        game_divs = soup.find_all('div', class_='txt247list')

        
        

        for game_div in game_divs:
            try:
                
                links = game_div.find_all('a')
                for link in links:
                    title = link.find('li').text
                    if re.search(r'\*$', title):
                        hrefs = link['href']
                        href = f"https://{self.domains[0]}".replace("247-tv","")+ hrefs
                        games.append(Game(icon=icons[league.lower()] if league.lower() in icons else None,title=title,links=[Link(href)]))
                    
                        
            
                    # games.append(Game(title,links=[Link(href)]))
            except:
                continue        
                

        return games

    def get_link(self, url):
        
    
        
        # iframes = []
        
        
        iframes = [Link(u) if not isinstance(u, Link) else u for u in find_iframes.find_iframes(url, "", [], [])]
        links = [link for link in iframes if "m3u8" in link.address]
        # return iframes[0]
        return links[0]
    
    
        
    
    
    
    
    
    
