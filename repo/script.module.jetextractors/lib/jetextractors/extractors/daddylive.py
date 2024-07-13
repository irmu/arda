import requests, re, base64
from bs4 import BeautifulSoup
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from urllib.parse import urlparse

from dateutil import parser
from datetime import datetime, timedelta

from ..models.Extractor import Extractor
from ..models.Game import Game
from ..models.Link import Link
from ..util import jsunpack, find_iframes, hunter
from ..util import m3u8_src
from . import wstream, nbastreams


 

class Daddylive(Extractor):
    def __init__(self) -> None:
        self.domains = ["dlhd.so", "1.dlhd.sx","dlhd.sx", "d.daddylivehd.sx", "daddylive.sx", "daddylivehd.com"]
        self.name = "Daddylive"
        

        # self.short_name = "TP"

    def get_games(self):
        games = []
        unique_hrefs = set()
        count = 0
        duplicate_count = 0
        r = requests.get(f"https://{self.domains[0]}/schedule/schedule-generated.json").json()

        for header, events in r.items():
            for event_type, event_list in events.items():
                for event in event_list:
                    title = event.get("event", "")
                    starttime = event.get("time", "")
                    league = event_type
                    channels = event.get("channels", [])
                    try:
                        utc_time = self.parse_header(header, starttime) - timedelta(hours=1)
                    except:
                        try:
                            utc_time = datetime.now().replace(hour=int(starttime.split(":")[0]), minute=int(starttime.split(":")[1])) - timedelta(hours=1)
                        except:
                            utc_time = datetime.now()
                    
                    
                    games.append(Game(
                        title,
                        [Link(f"https://{self.domains[0]}/stream/stream-{channel['channel_id']}.php", name=channel["channel_name"]) for channel in channels],
                        league=league,
                        starttime=utc_time
                    ))
            
            r_channels = requests.get(f"https://{self.domains[0]}/24-7-channels.php")
            # if r_channels.status_code == 200:
            soup_channels = BeautifulSoup(r_channels.text, "html.parser")
            # channel = soup_channels.find_all('a')
            A_link = soup_channels.find_all('a')[:2]
            
            b_link = soup_channels.find_all('a')[8:]
            links = A_link+ b_link
            for link in links:
                
                title = link.text
                if '18+' in title:
                    del title
                    continue
                
                href = f"https://{self.domains[0]}{link['href']}"
                if href in unique_hrefs:
                    duplicate_count += 1
                    continue
                unique_hrefs.add(href)
                count += 1
                games.append(Game(title,links=[Link(href)],league= "[COLORorange]24/7")) 
            return games

    def get_link(self, url):
        m3u8 = ""
        if "/embed/" not in url and "/channels/" not in url and "/stream/" not in url and "/cast/" not in url and "/batman/" not in url and "/extra/" not in url:
            raise Exception("Invalid URL")
        r = requests.get(url).text
        m3u8 = None
        
        if "wigistream.to" in r:
            re_embed = re.compile(r'src="(https:\/\/wigistream\.to\/embed\/.+?)"').findall(r)[0]
        elif "wstream.to" in r:
            re_embed = re.compile(r'src="(https:\/\/wstream\.to\/embed\/.+?)"').findall(r)[0]
        elif "eplayer.click" in r:
            re_embed = re.compile(r"<iframe src=\"(https:\/\/.+?)\"").findall(r)[0]
            r_embed = requests.get(re_embed, headers={"Referer": url}).text
            m3u8 = nbastreams.NBAStreams().process_page(r_embed, re_embed)
        elif "castmax.net" in r:
            embed_id = re.compile(r"id='(.+?)'").findall(r)[0]
            re_embed = "https://castmax.net/embed/%s.html" % embed_id 
        elif "jazzy.to" in r:
            re_embed = re.findall(r'src="(https:\/\/jazzy\.to.+?)"', r)[0]
            m3u8 = m3u8_src.scan_page(re_embed, headers={"Referer": url})
        elif "streamservicehd" in r:
            re_embed = re.findall(r'src="(https:\/\/streamservicehd.+?)"', r)[0]
            m3u8 = m3u8_src.scan_page(re_embed, headers={"Referer": url})
        elif "topuplist" in r:
            re_embed = re.findall(r'src="(https:\/\/topuplist\.click.+?)"', r)[0]
            r_embed = requests.get(re_embed).text
            fid = re.findall(r"fid='(.+?)';", r_embed)[0]
            embed_url = "https://jewelavid.com/embed2.php?player=desktop&live=" + fid
            r_embed = requests.get(embed_url, headers={"User-Agent": self.user_agent, "Referer": "https://1l1l.to/"}).text
            eval_url = ("".join(eval(re.findall(r"return\s?\((\[.+?\])", r_embed)[0]))).replace("\\", "").replace("////", "//")
            m3u8 = Link(eval_url, headers={"User-Agent": self.user_agent, "Referer": embed_url})
        if m3u8 == None:
            try:
                m3u8 = wstream.Wstream().get_link(re_embed + f"|Referer=https://{self.domains[0]}")
            except:
                m3u8 = nbastreams.NBAStreams().process_page(r, url)
        # if "webhdrunns.onlinehdhls.ru" in m3u8.address: # Temp fix 10-12-22, 12-19-22
            # m3u8.address = m3u8.address.split("?")[0] + "?Connection=keep-alive"
        if m3u8 is not None:
            # m3u8.license_url = f"|Referer=https://weblivehdplay.ru&Origin=https://weblivehdplay.ru"
            # netloc = urlparse(m3u8.address).netloc
            # m3u8.license_url = f"|Origin=https://{netloc}"
            if "id=" in m3u8.address:
                r = requests.get(m3u8.address).text
                re_hunter = re.findall(r'decodeURIComponent\(escape\(r\)\)}\("(.+?)",(.+?),"(.+?)",(.+?),(.+?),(.+?)\)', r)[0]
                deobfus = hunter.hunter(re_hunter[0], int(re_hunter[1]), re_hunter[2], int(re_hunter[3]), int(re_hunter[4]), int(re_hunter[5]))
                source = re.findall(r"var encodedSource = '(.+?)'", deobfus)[0]
                m3u8 = Link(base64.b64decode(source).decode("utf-8"), headers={"Referer": "https://qqwebplay.xyz/", "User-Agent": self.user_agent})
                
           
            m3u8.is_ddl = True
                    
                    
                        
            
                    # m3u8.is_mpd = True
            # if "Referer" in m3u8.headers and "lewblivehdplay.ru" in m3u8.headers["Referer"]:
            #     m3u8.headers["Origin"] = m3u8.headers["Referer"]
                

        return m3u8
   
            

    def show_ffmpeg_dialog(self):
        dialog = xbmcgui.Dialog()
        ret = dialog.contextmenu(['ffmpeg', 'HLS', 'NONE',"MPD"])

        return ret
    
    def parse_header(self, header, time):
        timestamp = parser.parse(header[:header.index("-")] + " " + time)
        timestamp = timestamp.replace(year=2023) # daddylive is dumb
        return timestamp
            

    