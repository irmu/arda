from typing import List
import requests, re, random
from bs4 import BeautifulSoup
from dateutil import parser, tz
from datetime import timedelta, datetime
from unidecode import unidecode
import unicodedata
import html
from ..util import find_iframes
import xbmc
from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import m3u8_src

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
headers = {"User-Agent":user_agent, "referrer": 'daddylive.me', "Connection":'keep-alive', 'Accept':'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'}

class Aesport(Extractor):
    def __init__(self) -> None:
        self.domains = ["aesport.tv"]        
        self.categories = ["fixture", "live-tv"]
        self.name = "Aesport"
        # self.short_name = ""

    def get_games(self):
        games = []
        
        for category in self.categories:           
            if category == "fixture":  # games   
                # set schedule to show next x days
                now = datetime.now()   
                sched_start = now.replace(hour=6, minute=0, second=0, microsecond=0)
                schedule_days = 3
                sched_end = sched_start + timedelta(days=schedule_days)
                timeout= int(sched_end.timestamp())
                category_url = f"https://{self.domains[0]}/{category}/all.html"        
                r = requests.get(category_url, headers=headers)                                   
                soup = BeautifulSoup(r.text, "html.parser")       
                fixtures = soup.findAll('div', class_='d-flex justify-content-between fixture-page-item active')       
  
                for fixture in fixtures :    
                               
                    regex1 = 'class=\"time-format\".+?data-time=\"(.+?)\"' 
                    schedule = re.compile(regex1).findall(str(fixture))
                    sched_time = int(int(schedule[0])/1000) 
                                      
                    sched_date = datetime.fromtimestamp(int(sched_time))
                    utc_date = sched_date-timedelta(hours=1)
                    
                    comp = fixture.find('div', class_='mt-1 tournament').text.strip()
                    team1 = fixture.find('span', class_='name-team name-team-left').text.strip()
                    team2 = fixture.find('span', class_='name-team name-team-right').text.strip()
                    link = fixture.find('a', class_='btn-watch active').get("href").strip()
                
                    comp = fix_text(comp)
                    team1 = fix_text(team1)
                    team2 = fix_text(team2)
                
                    if int(sched_time) <= int(timeout) :    
                        category ='scheduled'    
                    else :      
                        category ='future'    
                    
                    title = f'{team1} vs {team2}'
                    href = link
                    icon = 'https://i.imgur.com/OG7lCPM.png' 
                    league = comp
                    sched_time = parser.parse(str(sched_date)).replace(tzinfo=tz.gettz("Europe/London"))
                    utc_time = parser.parse(str(utc_date)).replace(tzinfo=tz.gettz("UTC"))                   
                    combined_title = f"{title}"
                    
                    if category == 'scheduled' :                 
                        games.append(Game(league=f"[COLORdeepskyblue]{league}" ,title=combined_title, links=[Link(address=href, is_links=True)], starttime=utc_time, icon=icon))
                                                                    
            else : # channels
                category_url = f"https://{self.domains[0]}/{category}.html"            
                r = requests.get(category_url, headers=headers)                                   
                soup = BeautifulSoup(r.text, "html.parser")       
                target = soup.findAll('div', class_='section-focus') 
                for t in target :                   
                    channels_content= t.findAll('div', class_='content')
                    channels = channels_content[0].find_all("a")
                    for channel in channels :                      
                        title = channel.select_one("div.channel-name").text.strip(),                            
                        href = channel.get("href")
                        thumb = channel.select_one("img.hide").get("src"),
                        league = "Channel" 
                        utc_time = None
                        combined_title = str(title[0])  
                        icon = str(thumb[0])  

                        games.append(Game(league=f"[COLORorange]{league}" ,title=combined_title, links=[Link(address=href, is_links=True)], starttime=utc_time, icon=icon))
                                   
        return games

    def get_links(self, url: str):
        links = []
        if not "live-tv" in url :  # games     
            pass
            result = m3u8_src.scan_page(url)
            if result :
                result = f"{result}|Referer=https://{self.domains[0]}/&User-Agent={user_agent}"                
                links.append(Link(result, headers={"Referer": "https://aesport.tv/", "User-Agent": user_agent}))
        else : # channels    
            result = m3u8_src.scan_page(url)
            if result :
                result = f"{result}|Referer=https://{self.domains[0]}/&User-Agent={user_agent}"                
                links.append(Link(result, headers={"Referer": "https://aesport.tv/", "User-Agent": user_agent}))                                
        return links

    def get_link(self, url: str): 
        result = m3u8_src.scan_page(url)
        if result :
            result = f"{result}|Referer=https://{self.domains[0]}/&User-Agent={user_agent}"                                
            link = Link(result, headers={"Referer": "https://aesport.tv/", "User-Agent": user_agent})                
        return link
                
def fix_text(new_text) :
    new_text = unicodedata.normalize('NFD', new_text).encode('ascii', 'ignore').decode("utf-8")
    new_text= html.unescape(new_text)
    return str(new_text)         
        
        
        
