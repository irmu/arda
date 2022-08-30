from jen import JenItem
import xbmc,xbmcaddon,os
Addon = xbmcaddon.Addon()
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")

def get_context_items(item):
    return item
class IMDB:
    
    def __init__(self, item_xml,icon,fanart):
            self.icon=icon
            self.fanart=fanart
            self.item_xml=item_xml
            self.result=self.process_item()
    def process_item(self):
        if "<imdburl>" in self.item_xml:
            item = JenItem(self.item_xml)
            if "movies/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbmovies",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "tvshows/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbseries",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "season/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbseason",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "episode/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbepisode",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "theepisodeTwo/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbepisodeTwo",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "years/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbyears",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "yearstv/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbyearstv",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "list/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdblists",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "actors/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbactors",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "name/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbactorspage",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "www.imdb.com" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbNextPage",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "genres/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbgenres",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "genrestv/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbgenrestv",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "chart/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbchart",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "charttv/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "imdbcharttv",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "searchmovies" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "searchmovies",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "searchseries" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "searchseries",
                    'url': item.get("imdburl", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item

class TMDB:
    name = "tmdb"
    def __init__(self, item_xml,icon,fanart):
            self.icon=icon
            self.fanart=fanart
            self.item_xml=item_xml
            self.result=self.process_item()
    def process_item(self):
        if "<tmdb>" in self.item_xml:
            item = JenItem(self.item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", self.icon),
                'fanart': item.get("fanart", self.fanart),
                'mode': "tmdb",
                'url': item.get("tmdb", ""),
                'folder': True,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "tmdb_tv_show" in self.item_xml:
            item = JenItem(self.item_xml)
            url = item.get("link", ")").replace("tmdb_tv_show(", "")[:-1]
            result_item = {
                'label': item["title"],
                'icon': item["thumbnail"],
                'fanart': item.get("fanart", self.fanart),
                'mode': "tmdb_tv_show",
                'url': "tmdb_id" + url,
                'folder': True,
                'content': "tvshows",
                'season': "0",
                'episode': "0",
                'info': {},
                "imdb": item.get("imdb", "0"),
                'year': item.get("year", ""),
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "tmdb_season(" in self.item_xml:
            item = JenItem(self.item_xml)
            url = item.get("link", ")").replace("tmdb_season(", "")[:-1]
            season = url.split(",")[1]
            result_item = {
                'label': item["title"],
                'icon': item["thumbnail"],
                'fanart': item.get("fanart", self.fanart),
                'mode': "tmdb_season",
                'url': "tmdb_id" + url,
                'folder': True,
                'content': "seasons",
                'season': str(season),
                'episode': "0",
                'info': {},
                "imdb": item.get("imdb", "0"),
                'year': item.get("year", ""),
                'context': {},
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
            
class Trakt:
    def __init__(self, item_xml,icon,fanart):
            self.icon=icon
            self.fanart=fanart
            self.item_xml=item_xml
            self.result=self.process_item()

    def process_item(self):
        #self.item_xml = remove_non_ascii(self.item_xml)
        if "<trakt>" in self.item_xml:
            item = JenItem(self.item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", self.icon),
                'fanart': item.get("fanart", self.fanart),
                'mode': "trakt",
                'url': item.get("trakt", ""),
                'folder': True,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "trakt_tv_show(" in self.item_xml:
            item = JenItem(self.item_xml)
            url = item.get("link", ")").replace("trakt_tv_show(", "")[:-1]
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", self.icon),
                'fanart': item.get("fanart", self.fanart),
                'mode': "trakt_tv_show",
                'url': "trakt_id" + url,
                'folder': True,
                'imdb': item.get("imdb", ""),
                'content': "tvshows",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': item.get("year", ""),
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "trakt_season(" in self.item_xml:
            item = JenItem(self.item_xml)
            url = item.get("link", ")").replace("trakt_season(", "")[:-1]
            season = url.split(",")[1]
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", self.icon),
                'fanart': item.get("fanart", self.fanart),
                'mode': "trakt_season",
                'url': "trakt_id" + url,
                'folder': True,
                'imdb': item.get("imdb", ""),
                'content': "seasons",
                'season': str(season),
                'episode': "0",
                'info': {},
                'year': item.get("year", ""),
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "trakt_list(" in self.item_xml:
            item = JenItem(self.item_xml)
            url = item.get("link", ")").replace("trakt_list(", "")[:-1]
            user_id, list_id = url.split(",")
            list_url = "https://api.trakt.tv/users/%s/lists/%s/items/" % (
                user_id, list_id)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", self.icon),
                'fanart': item.get("fanart", self.fanart),
                'mode': "trakt",
                'url': list_url,
                'folder': True,
                'imdb': item.get("imdb", ""),
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': item.get("year", ""),
                'context': {},
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item

        return False
        
        
        
class TVMAZE:
    def __init__(self, item_xml,icon,fanart):
            
            self.item_xml=item_xml
            self.icon=icon
            self.fanart=fanart
            self.result=self.process_item()

    def process_item(self):
        if "<tvmaze>" in self.item_xml:
            item = JenItem(self.item_xml)
            if "country/" in item.get("tvmaze", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "country",
                    'url': item.get("tvmaze", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "network/" in item.get("tvmaze", ""):
                item = JenItem(self.item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "network",
                    'url': item.get("tvmaze", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item    
            elif "show/" in item.get("tvmaze", ""):
                item = JenItem(self.item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "show",
                    'url': item.get("tvmaze", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "tvshows",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item 
            elif "season/" in item.get("tvmaze", ""):
                item = JenItem(self.item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "season",
                    'url': item.get("tvmaze", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "seasons",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': {},
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item                 
            elif "web_channel/" in item.get("tvmaze", ""):
                item = JenItem(self.item_xml)
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", self.icon),
                    'fanart': item.get("fanart", self.fanart),
                    'mode': "web_channel",
                    'url': item.get("tvmaze", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item 