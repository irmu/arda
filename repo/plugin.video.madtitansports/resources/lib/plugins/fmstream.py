from resources.lib.plugin import Plugin, run_hook
import xbmcgui
from bs4 import BeautifulSoup
import urllib
import requests, re

def recursive_replace(string: str, repl: str, new: str):
    while repl in string:
        string = string.replace(repl, new)
    return string

def parse_station(station):
    profiles=['', 'LC', 'HE', 'HE2', 'AAC Main']
    protocols=['http', 'https', 'mms', 'mmsh', 'rtsp', 'rtmp']

    res = {}
    if not station:
        return {"code": -1}
    res["link"] = station[0]
    res["bitrate"] = station[2]
    res["code"] = station[6]
    if len(station) > 7:
        res["protocol"] = protocols[station[7]]
    else:
        res["protocol"] = "http"
    if type(station[1]) == str:
        if station[1].isnumeric():
            res["codec"] = profiles[int(station[1])]
        else:
            res["codec"] = station[1]
    else:
        res["codec"] = res["protocol"]
    return res

class Fmstream(Plugin):
    name = "fmstream"

    def process_item(self, item):
        if self.name in item:
            link = item.get(self.name, "")
            thumbnail = item.get("thumbnail", "")
            fanart = item.get("fanart", "")
            icon = item.get("icon", "")
            if link.startswith("search"):
                item["is_dir"] = True
                item["link"] = f"{self.name}/{link}"
                list_item = xbmcgui.ListItem(item.get("title", item.get("name", "")), offscreen=True)
                list_item.setArt({"thumb": thumbnail, "fanart": fanart})
                item["list_item"] = list_item
                return item
    
    def routes(self, plugin):
        @plugin.route(f"/{self.name}/search/<query>")
        def search(query):
            query = urllib.parse.unquote_plus(query)
            if query == "*":
                query = xbmcgui.Dialog().input("Enter query")
                if query == "": return
            r = requests.get("http://fmstream.org/index.php?s=" + query).text.replace("\r", "").replace("\n", "").replace("\\/", "/")
            r = recursive_replace(r, ",,", ",0,")
            data = list(map(lambda x: [parse_station(station) for station in x], eval(re.findall(r"data=(.+?\]);", r)[0])))
            soup = BeautifulSoup(r, "html.parser")
            stations = soup.select("div.stnblock")
            jen_list = []
            for station in stations:
                try:
                    title = station.select_one("h3").text
                    code = int(re.findall(r"tf\((.+?),", station.select_one("div.fvb").get("onclick"))[0])
                    station_data = next((filter(lambda x: x[0]["code"] == code, data)))
                    description = []
                    if station.select_one("span.desc"):
                        description.append("[B]" + station.select_one("span.desc").text + "[/B]")
                    if station.select_one("span.slo"):
                        description.append("[I]" + station.select_one("span.slo").text + "[/I]")
                    if station.select_one("span.loc"):
                        description.append("Location: " + station.select_one("span.loc").text)
                    if station.select_one("span.frq"):
                        description.append("Frequency: " + ", ".join([frq.text for frq in station.select("span.frq")]))
                    jen_data = {
                        "title": title,
                        "link": [f"{link['protocol']}://{link['link']}({link['codec']} B{link['bitrate']})" for link in station_data],
                        "type": "item",
                        "summary": "\n".join(description)
                    }
                    jen_list.append(jen_data)
                except:
                    continue
            
            jen_list = [run_hook("process_item", item) for item in jen_list]
            jen_list = [run_hook("get_metadata", item, return_item_on_failure=True) for item in jen_list]
            run_hook("display_list", jen_list)