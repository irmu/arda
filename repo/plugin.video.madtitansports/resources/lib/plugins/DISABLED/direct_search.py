###########################################
#     GIVE CREDIT WHERE CREDIT IS DUE     #
#                                         #
#          T4ILS AND JETJET               #
###########################################




import json, sys, time, operator, os
from ..util.dialogs import link_dialog
from xbmcvfs import translatePath
from concurrent.futures import ThreadPoolExecutor
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
from resources.lib.plugin import Plugin
from datetime import datetime, timedelta
import calendar, inputstreamhelper
from sportjetextractors import extractors, extractor
from resources.lib.plugin import run_hook
import urllib.parse

import operator, traceback

CACHE_TIME = 0  # change to wanted cache time in seconds
SEARCH_INCLUDE = ["Direct_CH"]

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')

class DirectSearch(Plugin):
    name = "direct_search"
    priority = 100

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
        @plugin.route(f"/{self.name}/search/<path:query>")
        def search(query):
            if query == "*":
                query = xbmcgui.Dialog().input("Search game")
                if query == "": return
            games = []
            empty_date = datetime(year=2030, month=12, day=31)
            with ThreadPoolExecutor(max_workers=128) as executor:
                running_tasks = []
                for module in extractors.__all__:
                    if hasattr(module, "site_name") and hasattr(module, "get_games") and not module.site_name.endswith("Highlights") and module.site_name in SEARCH_INCLUDE:
                        running_tasks.append(executor.submit(lambda: [module.site_name, module.get_games()]))
                for running_task in running_tasks:
                    try:
                        site_name = running_task.result()[0]
                        site_games = running_task.result()[1]
                        for game in site_games:
                            if query.lower() not in game["title"].lower() and query.lower() not in game["league"].lower(): continue
                            jen_data = {
                                "title": "[COLORdodgerblue]%s[COLORwhite] |[B][I] %s[/B][/I]\n  [COLORred]%s | %s[/COLOR]" % (game["league"].replace("'", ""), game["title"], site_name, format_time(game["time"])),
                                "thumbnail": game["icon"],
                                "fanart": game["icon"],
                                "summary": game["title"],
                                "sportjetextractors": game["links"],
                                "time": game["time"].timestamp() if game["time"] != "" else empty_date.timestamp(),
                                "type": "item"
                            }
                            games.append(jen_data)
                    except Exception as e:
                        continue
            
            games = sorted(games, key=lambda x: x["time"])
            games = [run_hook("process_item", item) for item in games]
            games = [run_hook("get_metadata", item, return_item_on_failure=True) for item in games]
            run_hook("display_list", games)



def format_time(date):
    return utc_to_local(date).strftime("%m/%d %I:%M %p") if date != "" else ""

# https://stackoverflow.com/questions/4563272/convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-standard-lib
def utc_to_local(utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


