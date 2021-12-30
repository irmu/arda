# -*- coding: utf-8 -*-

import os,re,sys,xbmc,xbmcaddon,json,base64,urllib,urlparse,requests,shutil,xbmcplugin,xbmcgui,socket,urllib2
from xbmcplugin import addDirectoryItem, endOfDirectory


addon_id            = xbmcaddon.Addon().getAddonInfo('id')
addon_name          = xbmcaddon.Addon().getAddonInfo('name')
home_folder         = xbmc.translatePath('special://home/')
addon_folder        = os.path.join(home_folder, 'addons')
art_path            = os.path.join(addon_folder, addon_id)
resources_path      = os.path.join(art_path, 'resources')
lib_path            = os.path.join(resources_path, 'lib')
other_art_path      = os.path.join(resources_path, 'art')
ownAddon            = xbmcaddon.Addon(id=addon_id)
tmdb_api_key        = ownAddon.getSetting('tmdb_api_key')
skin_used           = xbmc.getSkinDir()
addon_icon          = os.path.join(art_path,'icon.png')
addon_fanart        = os.path.join(art_path,'fanart.jpg')
bee_icon            = os.path.join(other_art_path,'bumblebee.png')
bee_fanart          = os.path.join(other_art_path,'bumblebeeback.jpg')
content_type        = "movies"


def addDir(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description,})
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    if skin_used == 'skin.xonfluence':
        xbmc.executebuiltin('Container.SetViewMode(515)') # "MediaListView2" view
    elif skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(515)') # "MediaListView2" view
    elif skin_used == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(512)') # "Info-wall" view. 
    elif skin_used == 'skin.aeon.embuary':
        xbmc.executebuiltin('Container.SetViewMode(59)') # "Big-List" view.
    else:
        xbmc.executebuiltin('Container.SetViewMode(50)') # "Default-View for all" view.
    return ok
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addDirVid(name,url,mode,iconimage,fanart,description):
    ok=True
    liz = xbmcgui.ListItem(label=name, thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanart)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description,})
    liz.setProperty('IsPlayable', 'true')
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
    is_folder = False
    if skin_used == 'skin.xonfluence':
        xbmc.executebuiltin('Container.SetViewMode(515)') # "MediaListView2" view
    elif skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(515)') # "MediaListView2" view
    elif skin_used == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(512)') # "Info-wall" view. 
    elif skin_used == 'skin.aeon.embuary':
        xbmc.executebuiltin('Container.SetViewMode(59)') # "Big-List" view.
    else:
        xbmc.executebuiltin('Container.SetViewMode(50)') # "Default-View for all" view.
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)        
    return ok
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def bumblebee_movies(url):
    url = "https://api.unreel.me/api/assets/5bf58f136589a879828fda86/discover?__site=bumblebeetv&__source=web&onlyEnabledChannels=true"
    payload = {}
    headers = {
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'Sec-Fetch-Dest': 'empty',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
      'Origin': 'https://www.bumblebee.tv',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Referer': 'https://www.bumblebee.tv/pages/discover/d/movies',
      'Accept-Language': 'en-US,en;q=0.9',
      'If-None-Match': 'W/"4094-UpIKg3zWM7oNK9pSz7QSLGoydvg"'
    }
    response = requests.request("GET", url, headers=headers, data = payload).text
    data = json.loads(response)
    res = json.dumps(data, indent=2)
    channels = data['channels']
    for c in channels:
        name = c['name']
        sid = c['channelId']
        addDir(name,sid,6,bee_icon,bee_fanart,name) 

def bumblebee_movies_section(url):
    url2 = "https://api.unreel.me/v2/sites/bumblebeetv/channels/%s/movies?__site=bumblebeetv&__source=web&page=0&pageSize=80"%(url)
    payload = {}
    headers = {
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'Sec-Fetch-Dest': 'empty',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
      'Origin': 'https://www.bumblebee.tv',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Referer': 'https://www.bumblebee.tv/pages/discover/d/movies',
      'Accept-Language': 'en-US,en;q=0.9',
      'If-None-Match': 'W/"1407-IZfI6nafgZqtpLA8qYuUsOR8zqA"'
    }
    response = requests.request("GET", url2, headers=headers, data = payload).text
    data = json.loads(response)
    res = json.dumps(data, indent=2)
    items = data['items']
    for i in items:
        uid = i['uid']
        icon = i['movieData']['background']
        fanart = i['movieData']['poster']
        name = i['title'].encode('utf-8')
        summary = i['description'].encode('utf-8')
        link = "https://api.unreel.me/v2/sites/bumblebeetv/videos/%s/play-url?__site=bumblebeetv&__source=web&embed=false&protocol=https&tv=false"%uid
        addDirVid(name,link,90,icon,fanart,summary)      

def bumblebee_comedy(url):
    url = "https://api.unreel.me/api/assets/5716946b468119dd7a5ffb16/discover?__site=bumblebeetv&__source=web&onlyEnabledChannels=true"
    payload = {}
    headers = {
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'Sec-Fetch-Dest': 'empty',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
      'Origin': 'https://www.bumblebee.tv',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Referer': 'https://www.bumblebee.tv/pages/discover/d/movies',
      'Accept-Language': 'en-US,en;q=0.9',
      'If-None-Match': 'W/"4094-UpIKg3zWM7oNK9pSz7QSLGoydvg"'
    }
    response = requests.request("GET", url, headers=headers, data = payload).text
    data = json.loads(response)
    res = json.dumps(data, indent=2)
    channels = data['channels']
    for c in channels:
        name = c['name']
        sid = c['channelId']
        addDir(name,sid,7,bee_icon,bee_fanart,name)     


def bumblebee_lifestyle(url):
    url = "https://api.unreel.me/api/assets/5957c7e78f69b52a9861e7b1/discover?__site=bumblebeetv&__source=web&onlyEnabledChannels=true"
    payload = {}
    headers = {
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'Sec-Fetch-Dest': 'empty',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
      'Origin': 'https://www.bumblebee.tv',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Referer': 'https://www.bumblebee.tv/pages/discover/d/movies',
      'Accept-Language': 'en-US,en;q=0.9',
      'If-None-Match': 'W/"4094-UpIKg3zWM7oNK9pSz7QSLGoydvg"'
    }
    response = requests.request("GET", url, headers=headers, data = payload).text
    data = json.loads(response)
    res = json.dumps(data, indent=2)
    channels = data['channels']
    for c in channels:
        name = c['name']
        sid = c['channelId']
        addDir(name,sid,7,bee_icon,bee_fanart,name)    

def bumblebee_lifestle_section(url):
    url2 = "https://api.unreel.me/v2/sites/bumblebeetv/channels/%s/videos?__site=bumblebeetv&__source=web&page=0&pageSize=80"%(url)
    print url2
    payload = {}
    headers = {
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'Sec-Fetch-Dest': 'empty',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
      'Origin': 'https://www.bumblebee.tv',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Referer': 'https://www.bumblebee.tv/pages/discover/d/movies',
      'Accept-Language': 'en-US,en;q=0.9',
      'If-None-Match': 'W/"1407-IZfI6nafgZqtpLA8qYuUsOR8zqA"'
    }
    response = requests.request("GET", url2, headers=headers, data = payload).text
    data = json.loads(response)
    res = json.dumps(data, indent=2)
    items = data['items']
    for i in items:
        uid = i['uid']
        try:
            icon = i['metadata']['thumbnails']['maxres']
        except:
            icon = i['metadata']['thumbnails']['medium']
        #fanart = i['movieData']['poster']
        name = i['title'].encode('utf-8')
        summary = i['description'].encode('utf-8')
        otherId = i['id']
        sid = re.compile("uid: '(.+?)'.+?source: '(.+?)'",re.DOTALL).findall(otherId)
        for url, source in sid:
            if source == "Youtube":
                addDirVid(name,url,91,icon,icon,summary)
            else:
                link = "https://api.unreel.me/v2/sites/bumblebeetv/videos/%s/play-url?__site=bumblebeetv&__source=web&embed=false&protocol=https&tv=false"%uid
                addDirVid(name,link,90,icon,icon,summary) 

def bumblebee_news(url):
    url = "https://api.unreel.me/api/assets/5957c7895a65402a7db46ff7/discover?__site=bumblebeetv&__source=web&onlyEnabledChannels=true"
    payload = {}
    headers = {
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'Sec-Fetch-Dest': 'empty',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
      'Origin': 'https://www.bumblebee.tv',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Referer': 'https://www.bumblebee.tv/pages/discover/d/movies',
      'Accept-Language': 'en-US,en;q=0.9',
      'If-None-Match': 'W/"4094-UpIKg3zWM7oNK9pSz7QSLGoydvg"'
    }
    response = requests.request("GET", url, headers=headers, data = payload).text
    data = json.loads(response)
    res = json.dumps(data, indent=2)
    channels = data['channels']
    for c in channels:
        name = c['name']
        sid = c['channelId']
        addDir(name,sid,7,bee_icon,bee_fanart,name)    

def bumblebee_gaming(url):
    url = "https://api.unreel.me/api/assets/5957c7ff4d807055dc65fb98/discover?__site=bumblebeetv&__source=web&onlyEnabledChannels=true"
    payload = {}
    headers = {
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'Sec-Fetch-Dest': 'empty',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
      'Origin': 'https://www.bumblebee.tv',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Referer': 'https://www.bumblebee.tv/pages/discover/d/movies',
      'Accept-Language': 'en-US,en;q=0.9',
      'If-None-Match': 'W/"4094-UpIKg3zWM7oNK9pSz7QSLGoydvg"'
    }
    response = requests.request("GET", url, headers=headers, data = payload).text
    data = json.loads(response)
    res = json.dumps(data, indent=2)
    channels = data['channels']
    for c in channels:
        name = c['name']
        sid = c['channelId']
        addDir(name,sid,7,bee_icon,bee_fanart,name) 