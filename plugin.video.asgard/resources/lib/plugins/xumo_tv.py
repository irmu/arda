# -*- coding: utf-8 -*-
"""
    Xumotv plugin
    Copyright (C) 2020, TonyH

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    -------------------------------------------------------------

    Usage Examples:

    Xumo tv channels

    <dir>
    <title>Xumo Tv channels</title>
    <xumo>tv_channels</xumo>
    </dir>

    <dir>
    <title>Xumo On Demand</title>
    <xumo>demand</xumo>
    </dir>

    --------------------------------------------------------------

"""


import requests,re,os,xbmc,xbmcaddon,xbmcgui,json,xbmcplugin
import base64,pickle,koding,time,sqlite3
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode

CACHE_TIME = 86400  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')

class Xumo_Tv(Plugin):
    name = "xumo_tv"

    def process_item(self, item_xml):
        if "<xumo>" in item_xml:
            item = JenItem(item_xml)
            if "tv_channels" in item.get("xumo", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_xumo_tvchannels",
                    'url': item.get("xumo", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "tv_link" in item.get("xumo", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_xumo_tvchannels_link",
                    'url': item.get("xumo", ""),
                    'folder': False,
                    'imdb': "0",
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
            elif "demand" in item.get("xumo", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_xumo_on_demand",
                    'url': item.get("xumo", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "onitems" in item.get("xumo", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_xumo_on_demand_menu",
                    'url': item.get("xumo", ""),
                    'folder': True,
                    'imdb': "0",
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
            elif "dem_link" in item.get("xumo", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_xumo_on_demand_links",
                    'url': item.get("xumo", ""),
                    'folder': False,
                    'imdb': "0",
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


@route(mode='open_xumo_tvchannels')
def open_channels():
    pins = "PLugin_xumo_tvchannels"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:  
        xml = ""
        User_Agent = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
        headers = {'User-Agent': User_Agent}
        base_api = "https://valencia-app-mds.xumo.com/v2/"
        url = 'http://www.xumo.tv'
        response = requests.get(url).text
        match = json.loads(re.compile('__JOBS_REHYDRATE_STATE__=(.+?);</script>',re.DOTALL).findall(response)[0])
        geoId = match["jobs"]["1"]["data"]["geoId"]
        chanId = match["jobs"]["1"]["data"]["channelListId"]
        Chan = (base_api+('channels/list/%s.json?sort=hybrid&geoId=%s')%(chanId, geoId))
        response = requests.get(Chan, headers=headers).text
        res = json.loads(response)
        item = res['channel']['item']
        items = sorted(list(item), key=lambda item: item['title'])
        link = ""
        for c in items:
            title = c['title'].encode('utf-8')
            check = xumo_bad(title)
            if check == False:
                summary = c['description'].encode('utf-8')
                chid   = c['guid']['value'].encode('utf-8')
                icon = 'https://image.xumo.com/v1/channels/channel/%s/512x512.png?type=color_onBlack'%chid
                fanart = "https://image.xumo.com/v1/channels/channel/%s/248x140.png?type=channelTile"% chid
                data = "%s|%s|%s"%(chid,title,icon)
                xml += "<item>"\
                     "<title>%s</title>"\
                     "<meta>"\
                     "<content>movie</content>"\
                     "<imdb></imdb>"\
                     "<title></title>"\
                     "<year></year>"\
                     "<thumbnail>%s</thumbnail>"\
                     "<fanart>%s</fanart>"\
                     "<summary>%s</summary>"\
                     "</meta>"\
                     "<xumo>tv_link|%s</xumo>"\
                     "</item>" % (title,icon,fanart,summary,data)            
                                                                                     
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)    

@route(mode='open_xumo_tvchannels_link', args=["url"])
def open_channel_link(url):
    koding.Show_Busy(status=True)
    chid = url.split("|")[1]
    name = url.split("|")[2]
    image = url.split("|")[3]
    User_Agent = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
    headers = {'User-Agent': User_Agent}
    base_api = "https://valencia-app-mds.xumo.com/v2/"
    on_url = base_api+"channels/channel/%s/onnow.json?f=title&f=descriptions#descriptions"%(chid)
    response = requests.get(on_url, headers=headers).text
    res = json.loads(response)
    assets = res['id']
    meta_url = base_api+"assets/asset/%s.json?f=title&f=providers&f=descriptions&f=runtime&f=availableSince"%(assets)
    response = requests.get(meta_url, headers=headers).text
    res = json.loads(response)
    try:
        link = res['providers'][0]['sources'][0]['uri']
    except:
        link = "none"
    koding.Show_Busy(status=False )
    info = xbmcgui.ListItem(name, thumbnailImage=image)
    xbmc.Player().play(link,info) 

@route(mode='open_xumo_on_demand', args=["url"])
def open_on_demand(url):
    pins = "PLugin_xumo_ondemand"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else: 
        xml = ""
        User_Agent = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
        headers = {'User-Agent': User_Agent}
        base_api = "https://valencia-app-mds.xumo.com/v2/"
        url = 'http://www.xumo.tv'
        response = requests.get(url).text
        match = json.loads(re.compile('__JOBS_REHYDRATE_STATE__=(.+?);</script>',re.DOTALL).findall(response)[0])
        geoId = match["jobs"]["1"]["data"]["geoId"]
        chanId = match["jobs"]["1"]["data"]["channelListId"]
        Chan = (base_api+('channels/list/%s.json?sort=hybrid&geoId=%s')%(chanId, geoId))
        response = requests.get(Chan, headers=headers).text
        res = json.loads(response)
        item = res['channel']['item']
        #items = sorted(list(item), key=lambda item: item['title'])
        for c in item:
            title = c['title'].encode('utf-8')
            num = c['number']
            chid = c['guid']['value']
            icon = 'https://image.xumo.com/v1/channels/channel/%s/512x512.png?type=color_onBlack'%chid
            fanart = "https://image.xumo.com/v1/channels/channel/%s/248x140.png?type=channelTile"% chid
            summary = c['description'].encode('utf-8')
            xml += "<item>"\
                 "<title>%s</title>"\
                 "<meta>"\
                 "<content>movie</content>"\
                 "<imdb></imdb>"\
                 "<title></title>"\
                 "<year></year>"\
                 "<thumbnail>%s</thumbnail>"\
                 "<fanart>%s</fanart>"\
                 "<summary>%s</summary>"\
                 "</meta>"\
                 "<xumo>onitems|%s</xumo>"\
                 "</item>" % (title,icon,fanart,summary,chid)

        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_xumo_on_demand_menu', args=["url"])
def open_on_demand_menu(url):
    pins = "PLugin_xumo_ondemand_"+url
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else: 
        xml = ""
        chid = url.split("|")[-1]
        User_Agent = "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)"
        headers = {'User-Agent': User_Agent}
        base_api = "https://valencia-app-mds.xumo.com/v2/"
        lineup_url = base_api+"channels/channel/%s/broadcast.json?hour=22"%chid
        response = requests.get(lineup_url, headers=headers).text
        res = json.loads(response)
        assets = res['assets']
        for a in assets:
            start = a['timestamps']['start']
            end = a['timestamps']['end']
            vodid = a['id']
            meta_url = base_api+"assets/asset/%s.json?f=title&f=providers&f=descriptions&f=runtime&f=availableSince"%(vodid)
            response = requests.get(meta_url, headers=headers).text
            res = json.loads(response)
            show_title = res['title'].encode('utf-8')
            summary = show_title.encode('utf-8')
            try:
                summary = res['descriptions']['large'].encode('utf-8')
            except:
                pass
            try:
                summary = res['descriptions']['medium'].encode('utf-8')
            except:
                pass
            try:
                summary = res['descriptions']['small'].encode('utf-8')
            except:
                pass
            logoid = res['id']
            icon = "https://image.xumo.com/v1/assets/asset/%s/600x340.jpg"% logoid
            try:
                link = res['providers'][0]['sources'][0]['uri']
            except:
                link = "none"
            data = "%s|%s|%s"%(link,show_title,icon)
            xml += "<item>"\
                 "<title>%s</title>"\
                 "<meta>"\
                 "<content>movie</content>"\
                 "<imdb></imdb>"\
                 "<title></title>"\
                 "<year></year>"\
                 "<thumbnail>%s</thumbnail>"\
                 "<fanart></fanart>"\
                 "<summary>%s</summary>"\
                 "</meta>"\
                 "<xumo>dem_link|%s</xumo>"\
                 "</item>" % (show_title,icon,summary,data)

        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_xumo_on_demand_links', args=["url"])
def open_demand_link(url):
    link = url.split("|")[1]
    name = url.split("|")[2]
    image = url.split("|")[3]
    info = xbmcgui.ListItem(name, thumbnailImage=image)
    xbmc.Player().play(link,info) 



def xumo_bad(name):
    missing = ["ACC Digital Network","Above Average","Adventure Sports Network","Ameba",
    "America's Funniest Home Videos","Architectural Digest","Billboard","Bloomberg Television",
    "CBC NEWS","CHIVE TV","CNET","CollegeHumor","Condé Nast Traveler","Cooking Light",
    "CoolSchool","Copa90","Cycle World","FBE","FOX Sports","Family Feud","Field & Stream",
    "Food52","Football Daily","Fox Deportes","Funny or Die","Futurism","GQ","GameSpot",
    "Glamour","Got Talent Global","Great Big Story","HISTORY","Hard Knocks Fighting Championship",
    "Just For Laughs","Just For Laughs Gags","Kid Genius","MMAjunkie","MOTORVISION.TV",
    "Mashable","Motorcyclist","NEW K.ID","Newsy","Nitro Circus","Nosey","NowThis",
    "Outside TV+","PBS Digital","People Are Awesome","People Magazine","PeopleTV",
    "Popular Science","Real Nosey","Refinery29","Rowan and Martin's Laugh-In",
    "SYFY WIRE","Saveur","Southern Living","Sports Illustrated","TIME Magazine",
    "TMZ","TODAY","The Hollywood Reporter","The Inertia","The New Yorker","The Pet Collective",
    "The Preview Channel","This Is Happening","Titanic Channel","Toon Goggles","USA TODAY News",
    "USA Today SportsWire","Uzoo","Vanity Fair","Vogue","Wochit","World Surf League",
    "Young Hollywood","ZooMoo","batteryPOP","comicbook","eScapes"]
    if name in missing:
        return True
    else:
        return False

def fetch_from_db2(url):
    koding.reset_db()
    url2 = clean_url(url)
    match = koding.Get_All_From_Table(url2)
    if match:
        match = match[0]
        if not match["value"]:
            return None   
        match_item = match["value"]
        try:
                result = pickle.loads(base64.b64decode(match_item))
        except:
                return None
        created_time = match["created"]
        test_time = float(created_time) + CACHE_TIME 
        print test_time
        if float(created_time) + CACHE_TIME <= time.time():
            koding.Remove_Table(url2)
            db = sqlite3.connect('%s' % (database_loc))        
            cursor = db.cursor()
            db.execute("vacuum")
            db.commit()
            db.close()
            display_list2(result, "video", url2)
        else:
            pass                     
        return result
    else:
        return []


def remove_non_ascii(text):
    return unidecode(text)
        
