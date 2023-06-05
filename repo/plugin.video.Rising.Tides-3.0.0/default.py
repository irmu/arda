import urllib,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,traceback,os,time,_Edit,re,requests,base64,sys,xbmc,random,string,hashlib,resolveurl
from bs4 import BeautifulSoup
from xml.etree.ElementTree import ElementTree
import urllib.parse
import urllib.request

try:
    import json
except:
    import simplejson as json
  
resolve_url=[]
g_ignoreSetResolved=[]

class NoRedirection(urllib.request.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response


AddonID   = 'plugin.video.Rising.Tides'
addon = _Edit.addon
addon_version = addon.getAddonInfo('version')
profile = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
fanart = xbmcvfs.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))        
icon = xbmcvfs.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
artpath = xbmcvfs.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/art/'))
thumbpath = xbmcvfs.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/thumbs/'))
dialog1 = xbmcgui.Dialog()      
selfAddon = xbmcaddon.Addon(id=AddonID)
home = xbmcvfs.translatePath(addon.getAddonInfo('path'))
favorites = os.path.join(profile, 'favorites')
history = os.path.join(profile, 'history')
REV = os.path.join(profile, 'list_revision')
icon = os.path.join(home, 'icon.png')
FANART = os.path.join(home, 'fanart.jpg')
source_file = os.path.join(profile, 'source_file')
functions_dir = profile
debug = 'true' #addon.getSetting('debug')
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else: FAV = []
if os.path.exists(source_file)==True:
    SOURCES = open(source_file).read()
else: SOURCES = []


def addon_log(string):
    if debug == 'true':
        xbmc.log("[addon.live.RisingTides Lists-%s]: %s" %(addon_version, string))

class SafeString(str):
    def title(self):
        return self

    def capitalize(self):
        return self

def OPEN_URL(url):
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = requests.get(url)
    link=response.text
    return link

def scrape():
    html = OPEN_URL('https://soccerhighlightshd.com/')
    r='<a alt="(.+?)" .+? data-src="(.+?)" .+? href="(.+?)">'
    match = re.compile ( r , re.DOTALL).findall (html)
    for name,image,url in match:
        addDir1('[B][COLOR white]%s[/COLOR][/B]'%name,url,34,image,FANART,'')

def HIGHLIGHTS_LINKS(name,url):
    xbmc.log('GETLINKS: %s'%url)
    links=OPEN_URL(url)
    links= links.split("<div style='width:100%;height:0px;position:relative;padding-bottom:56.250%;margin-bottom:30px'>")
    xbmc.log('LINK LEN: %s'%len(links))
    for link in links:
        r = '<iframe src="(.+?)"'
        match = re.compile(r,re.DOTALL).findall(link)
        for url in match:
            if'veuclips' in url:
                url=url.replace('goal91','player')
                addDir1(name,url,36,'','','' )
            if'ok.ru' in url:
                addDir1(name,url,65,'','','' )
            else:
                addDir1(name,url,36,'','','' )

def PLAYLINKS(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setArt({'icon':iconimage,'thumb':iconimage})

        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def CHECKLINKS(name,url,iconimage):
        if resolveurl.HostedMediaFile(url).valid_url():
            url = resolveurl.HostedMediaFile(url).resolve()     
            PLAYLINKS(name,url,iconimage)
        elif liveresolver.isValid(url)==True:
            url=liveresolver.resolve(url)
            PLAYLINKS(name,url,iconimage)
        else:
            PLAYLINKS(name,url,iconimage)
       
def PLAYSTREAM(name,url,iconimage):
        link=resolveurl.resolve(str(url))
        resolve(name,link)
        if (xbmc.Player().isPlaying() == 0):
            quit()
        else:
            return
    
def resolve(name,url):
    if 'm3u8' in url or 'mp4' in url:
        xbmc.Player().play(url,xbmcgui.ListItem(name))

def makeRequest(url, headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
            req = requests.get(url,headers=headers)
            data = req.text
            data = data.replace("<link>.<link>","<link>http://Ignoreme</link>")
            data = data.replace("<link","<url").replace("</link","</url")
            return data
        except Exception as e:
            addon_log('URL: '+url)
            if hasattr(e, 'code'):
                addon_log('We failed with error code - %s.' % e.code)
                xbmc.executebuiltin("XBMC.Notification(RisingTides,We failed with error code - "+str(e.code)+",10000,"+icon+")")
            elif hasattr(e, 'reason'):
                addon_log('We failed to reach a server.')
                addon_log('Reason: %s' %e.reason)
                xbmc.executebuiltin("XBMC.Notification(RisingTides,We failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")

               
def SKindex():
    addon_log("SKindex")
    addDir('[COLOR pink][B]F[/B][/COLOR][COLOR white][B]ootball[/B][/COLOR] [COLOR red][B]H[/B][/COLOR][COLOR white][B]ighlights[/B][/COLOR]','Football Highlights',33,'https://i.imgur.com/koR9cKd.jpg' ,  FANART,'','','','')
    getData(_Edit.MainBase,'')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def play(url,name,pdialogue=None):
        from resources.root import resolvers
        import xbmcgui
        
        url = url.strip()

        url = resolvers.resolve(url)

        if url.endswith('m3u8'):
            from resources.root import iptv
            iptv.listm3u(url)
        else:
            liz = xbmcgui.ListItem(name)
            liz.setArt({'icon':iconimage,'thumb':iconimage})

            liz.setInfo(type='Video', infoLabels={'Title':name})
            liz.setProperty("IsPlayable","true")
            liz.setPath(url)
            
            if url.endswith('.ts'):
                url = 'plugin://plugin.video.f4mTester/?url='+urllib.parse.quote_plus(url)+'&amp;streamtype=SIMPLE'
            elif url.endswith('.m3u8'):
                url = 'plugin://plugin.video.f4mTester/?url='+urllib.parse.quote_plus(url)+'&amp;streamtype=HLS'
            elif url.endswith('.f4m'):
                url = 'plugin://plugin.video.f4mTester/?url='+urllib.parse.quote_plus(url)

            '''
            elif '.mpegts' in i.string:                                         
                f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.parse.quote_plus(i.string)+'&amp;streamtype=TSDOWNLOADER'
            '''
            if url.lower().startswith('plugin') and 'youtube' not in  url.lower():
                from resources.modules import CustomPlayer
                xbmc.executebuiltin('XBMC.PlayMedia('+url+')') 
                player = CustomPlayer.MyXBMCPlayer()
                if (xbmc.Player().isPlaying() == 0):
                    quit()
                try:
                   
                        if player.urlplayed:
                            print('yes played')
                            return
                        if time.time()-beforestart>4: return False
                except: pass

                print('returning now')
                return False

            from resources.modules import  CustomPlayer
            import time

            player = CustomPlayer.MyXBMCPlayer()
            player.pdialogue=pdialogue
            start = time.time() 
            print('going to play')
            import time
            beforestart=time.time()
            player.play( url, liz)
            if (xbmc.Player().isPlaying() == 0):
                quit()
            try:
                while player.is_active:
                    xbmc.sleep(400)
                   
                    if player.urlplayed:
                        print('yes played')
                        return
                    if time.time()-beforestart>4: return False
            except: pass
            print('not played',url)
            xbmc.Player().stop()
            return

def regex_from_to(text, from_string, to_string, excluding=True):
    import re,string
    if excluding:
        try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
        except: r = ''
    else:
        try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
        except: r = ''
    return r

def regex_get_all(text, start_with, end_with):
    import re,string
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

logfile    = xbmcvfs.translatePath(os.path.join('special://home/addons/plugin.video.Rising.Tides', 'log.txt'))


def getSources():
        if os.path.exists(favorites) == True:
            addDir('Favorites','url',4,os.path.join(home, 'resources', 'favorite.png'),FANART,'','','','')
        if addon.getSetting("browse_xml_database") == "true":
            addDir('XML Database','http://xbmcplus.xb.funpic.de/www-data/filesystem/',15,icon,FANART,'','','','')
        if addon.getSetting("browse_community") == "true":
            addDir('Community Files','community_files',16,icon,FANART,'','','','')
        if os.path.exists(history) == True:
            addDir('Search History','history',25,os.path.join(home, 'resources', 'favorite.png'),FANART,'','','','')
        if addon.getSetting("searchyt") == "true":
            addDir('Search:Youtube','youtube',25,icon,FANART,'','','','')
        if addon.getSetting("searchDM") == "true":
            addDir('Search:dailymotion','dmotion',25,icon,FANART,'','','','')
        if addon.getSetting("PulsarM") == "true":
            addDir('Pulsar:IMDB','IMDBidplay',27,icon,FANART,'','','','')            
        if os.path.exists(source_file)==True:
            sources = json.loads(open(source_file,"r").read())
            if len(sources) > 1:
                for i in sources:
                    if isinstance(i, list):
                        addDir(i[0].encode('utf-8'),i[1].encode('utf-8'),1,icon,FANART,'','','','','source')
                    else:
                        thumb = icon
                        fanart = FANART
                        desc = ''
                        date = ''
                        credits = ''
                        genre = ''
                        if i.has_key('thumbnail'):
                            thumb = i['thumbnail']
                        if i.has_key('fanart'):
                            fanart = i['fanart']
                        if i.has_key('description'):
                            desc = i['description']
                        if i.has_key('date'):
                            date = i['date']
                        if i.has_key('genre'):
                            genre = i['genre']
                        if i.has_key('credits'):
                            credits = i['credits']
                        addDir(i['title'].encode('utf-8'),i['url'].encode('utf-8'),1,thumb,fanart,desc,genre,date,credits,'source')

            else:
                if len(sources) == 1:
                    if isinstance(sources[0], list):
                        getData(sources[0][1].encode('utf-8'),FANART)
                    else:
                        getData(sources[0]['url'], sources[0]['fanart'])

def getSoup(url,data=None):
        if url != None :
            if url.startswith('http://') or url.startswith('https://'):
                data = makeRequest(url)
                if re.search("#EXTM3U",data) or 'm3u' in url: 
                    print('found m3u data',data)
                    return data
                
        elif data == None:
            if xbmcvfs.exists(url):
                if url.startswith("smb://") or url.startswith("nfs://"):
                    copy = xbmcvfs.copy(url, os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    if copy:
                        data = open(os.path.join(profile, 'temp', 'sorce_temp.txt'), "r").read()
                        xbmcvfs.delete(os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    else:
                        addon_log("failed to copy from smb:")
                else:
                    data = open(url, 'r').read()
                    if re.match("#EXTM3U",data)or 'm3u' in url: 
                        return data
            else:
                addon_log("Soup Data not found!")
                return
        return BeautifulSoup(data)

def getData(url,fanart):
    SetViewLayout = "List"
     
    soup = getSoup(url)
    
    if isinstance(soup,BeautifulSoup):
        if len(soup('layoutype')) > 0:
            SetViewLayout = "Thumbnail"         

        if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:

                linkedUrl=''
                lcount=0
                try:
                    linkedUrl =  channel('externallink')[0].string
                    lcount=len(channel('externallink'))
                except: pass
                if lcount>1: linkedUrl=''

                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = ''

                try:
                    if not channel('fanart'):
                        if addon.getSetting('use_thumb') == "true":
                            fanArt = thumbnail
                        else:
                            fanArt = fanart
                    else:
                        fanArt = channel('fanart')[0].string
                    if fanArt == None:
                        raise
                except:
                    fanArt = fanart

                try:
                    desc = channel('info')[0].string
                    if desc == None:
                        raise
                except:
                    desc = ''

                try:
                    genre = channel('genre')[0].string
                    if genre == None:
                        raise
                except:
                    genre = ''

                try:
                    date = channel('date')[0].string
                    if date == None:
                        raise
                except:
                    date = ''

                try:
                    credits = channel('credits')[0].string
                    if credits == None:
                        raise
                except:
                    credits = ''

                try:
                    if linkedUrl=='':
                        addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                    else:
                        addDir(name.encode('utf-8'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                except:
                    addon_log('There was a problem adding directory from getData(): '+name.encode('utf-8', 'ignore'))
        else:
            addon_log('No Channels: getItems')
            getItems(soup('item'),fanart)
    else:
        parse_m3u(soup)

    if SetViewLayout == "Thumbnail":
       SetViewThumbnail()

def parse_m3u(data):
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(content)
    total = len(match)
    print( 'total m3u links',total)
    for other,channel_name,stream_url in match:
        if 'tvg-logo' in other:
            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
            if thumbnail:
                if thumbnail.startswith('http'):
                    thumbnail = thumbnail
                
                elif not addon.getSetting('logo-folderPath') == "":
                    logo_url = addon.getSetting('logo-folderPath')
                    thumbnail = logo_url + thumbnail

                else:
                    thumbnail = thumbnail            
        else:
            thumbnail = ''
        if 'type' in other:
            mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
            if mode_type == 'yt-dl':
                stream_url = stream_url +"&mode=18"
            elif mode_type == 'regex':
                url = stream_url.split('&regexs=')
                regexs = parse_regex(getSoup('',data=url[1]))
                
                addLink(url[0], channel_name,thumbnail,'','','','','',None,regexs,total)
                continue
        addLink(stream_url, channel_name,thumbnail,'','','','','',None,'',total)
        
    xbmc.executebuiltin("Container.SetViewMode(50)")
    
def getChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('channel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('item')
        try:
            fanArt = channel_list('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not channel('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                pass
            try:
                desc = channel('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = channel('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = channel('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            try:
                credits = channel('credits')[0].string
                if credits == None:
                    raise
            except:
                credits = ''

            try:
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc,genre,credits,date)
            except:
                addon_log('There was a problem adding directory - '+name.encode('utf-8', 'ignore'))
        getItems(items,fanArt)

def getSubChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('subchannel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('subitem')
        getItems(items,fanart)

def GetSublinks(name,url,iconimage,fanart):
    xbmc.log('I GOT HERE###############')
    List=[]; ListU=[]; c=0
    all_videos = regex_get_all(url, 'sublink:', '#')
    for a in all_videos:
        if 'LISTSOURCE:' in a:
            vurl = regex_from_to(a, 'LISTSOURCE:', '::')
            linename = regex_from_to(a, 'LISTNAME:', '::')
        else:
            vurl = a.replace('sublink:','').replace('#','')
            linename = name
        if len(vurl) > 10:
            c=c+1; List.append(linename); ListU.append(vurl)
 
    if c==1:
        try:
            liz=xbmcgui.ListItem(name); liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setArt({'icon':iconimage,'thumb':iconimage})
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=ListU[0],listitem=liz)
            xbmc.Player().play(urlsolver(ListU[0]), liz)
        except:
            pass
    else:
         dialog=xbmcgui.Dialog()
         rNo=dialog.select('Select A Source', List)
         if rNo>=0:
             rName=name
             rURL=str(ListU[rNo])
             try:
                 xbmc.Player().play(urlsolver(rURL), xbmcgui.ListItem(rName))
             except:
                 xbmc.Player().play(rURL, xbmcgui.ListItem(rName))
               
def Search_m3u(data,Searchkey):
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(content)
    total = len(match)
    print('total m3u links',total)
    for other,channel_name,stream_url in match:
        if 'tvg-logo' in other:
            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
            if thumbnail:
                if thumbnail.startswith('http'):
                    thumbnail = thumbnail
                
                elif not addon.getSetting('logo-folderPath') == "":
                    logo_url = addon.getSetting('logo-folderPath')
                    thumbnail = logo_url + thumbnail

                else:
                    thumbnail = thumbnail            
        else:
            thumbnail = ''
        if 'type' in other:
            mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
            if mode_type == 'yt-dl':
                stream_url = stream_url +"&mode=18"
            elif mode_type == 'regex':
                url = stream_url.split('&regexs=')
                regexs = parse_regex(getSoup('',data=url[1]))
                
                addLink(url[0], channel_name,thumbnail,'','','','','',None,regexs,total)
                continue
        addLink(stream_url, channel_name,thumbnail,'','','','','',None,'',total)

def FindFirstPattern(text,pattern):
    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result
    
def getItems(items,fanart):
        total = len(items)
        addon_log('Total Items: %s' %total)
        for item in items:
            isXMLSource=False
            isJsonrpc = False
            try:
                name = item('title')[0].string
                
                if name is None:
                    name = 'unknown?'
            except:
                addon_log('Name Error')
                name = ''


            try:
                if item('epg'):
                    if item.epg_url:
                        addon_log('Get EPG Regex')
                        epg_url = item.epg_url.string
                        epg_regex = item.epg_regex.string
                        epg_name = get_epg(epg_url, epg_regex)
                        if epg_name:
                            name += ' - ' + epg_name
                    elif item('epg')[0].string > 1:
                        name += getepg(item('epg')[0].string)
                else:
                    pass
            except:
                addon_log('EPG Error')
            try:
                url = []
                if len(item('url')) >0:
                    for i in item('url'):
                        if not i.string == None:
                            url.append(i.string)

                if len(item('inputstream')) >0:
                    for i in item('inputstream'):
                        print("item inputstream ",item)
                        if not i.string == None:
                            url.append(i.string)
                    print("item url ",url)

                elif len(item('sportsdevil')) >0:
                    for i in item('sportsdevil'):
                        if not i.string == None:
                            sportsdevil = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +i.string
                            referer = item('referer')[0].string
                            if referer:
                                sportsdevil = sportsdevil + '%26referer=' +referer
                            url.append(sportsdevil)

                elif len(item('p2p')) >0:
                    for i in item('p2p'):
                        if not i.string == None:
                            if 'sop://' in i:
                                sop = 'plugin://plugin.video.p2p-streams/?url='+i.string +'&amp;mode=2&amp;' + 'name='+name 
                                url.append(sop) 
                            else:
                                p2p='plugin://plugin.video.p2p-streams/?url='+i.string +'&amp;mode=1&amp;' + 'name='+name 
                                url.append(p2p)
                elif len(item('vaughn')) >0:
                    for i in item('vaughn'):
                        if not i.string == None:
                            vaughn = 'plugin://plugin.stream.vaughnlive.tv/?mode=PlayLiveStream&amp;channel='+i.string
                            url.append(vaughn)
                elif len(item('ilive')) >0:
                    for i in item('ilive'):
                        if not i.string == None:
                            if not 'http' in i.string:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url=http://www.streamlive.to/view/'+i.string+'&amp;link=99&amp;mode=iLivePlay'
                            else:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url='+i.string+'&amp;link=99&amp;mode=iLivePlay'
                elif len(item('yt-dl')) >0:
                    for i in item('yt-dl'):
                        if not i.string == None:
                            ytdl = i.string + '&mode=18'
                            url.append(ytdl)
                elif len(item('utube')) >0:
                    for i in item('utube'):
                        if not i.string == None:
                            if len(i.string) == 11:
                                utube = 'plugin://plugin.video.youtube/play/?video_id='+ i.string 
                            elif i.string.startswith('PL') and not '&order=' in i.string :
                                utube = 'plugin://plugin.video.youtube/play/?&order=default&playlist_id=' + i.string
                            else:
                                utube = 'plugin://plugin.video.youtube/play/?playlist_id=' + i.string 
                    url.append(utube)
                elif len(item('imdb')) >0:
                    for i in item('imdb'):
                        if not i.string == None:
                            if addon.getSetting('genesisorpulsar') == '0':
                                imdb = 'plugin://plugin.video.genesis/?action=play&imdb='+i.string
                            else:
                                imdb = 'plugin://plugin.video.pulsar/movie/tt'+i.string+'/play'
                            url.append(imdb)                      
                elif len(item('f4m')) >0:
                        for i in item('f4m'):
                            if not i.string == None:
                                if '.f4m' in i.string:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.parse.quote_plus(i.string)
                                elif '.m3u8' in i.string:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.parse.quote_plus(i.string)+'&amp;streamtype=HLS'
                                    
                                else:
                                    f4m = 'plugin://plugin.video.f4mTester/?url='+urllib.parse.quote_plus(i.string)+'&amp;streamtype=SIMPLE'
                        url.append(f4m)
                elif len(item('ftv')) >0:
                    for i in item('ftv'):
                        if not i.string == None:
                            ftv = 'plugin://plugin.video.F.T.V/?name='+urllib.parse.quote(name) +'&url=' +i.string +'&mode=125&ch_fanart=na'
                        url.append(ftv)                        
                if len(url) < 1:
                    raise
            except Exception as e:
                addon_log('Error <link> element, Passing:'+name)#.decode(encoding='UTF-8'))#encode('utf-8', 'ignore'))
                continue
                
            isXMLSource=False

            try:
                isXMLSource = item('externallink')[0].string
            except: pass
            
            if isXMLSource:
                ext_url=[isXMLSource]
                isXMLSource=True
            else:
                isXMLSource=False
            try:
                isJsonrpc = item('jsonrpc')[0].string
            except: pass
            if isJsonrpc:
                ext_url=[isJsonrpc]
                isJsonrpc=True
            else:
                isJsonrpc=False            
            try:
                thumbnail = item('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not item('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                    else:
                        fanArt = fanart
                else:
                    fanArt = item('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                fanArt = fanart
            try:
                desc = item('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = item('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = item('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            regexs = None
            if item('regex'):
                try:
                    reg_item = item('regex')
                    regexs = parse_regex(reg_item)
                except:
                    pass            
           
            try:
                if len(url) > 1:
                    
                    alt = 0
                    playlist = []
                    for i in url:
                        if addon.getSetting('ask_playlist_items') == 'true':
                            if regexs:
                                playlist.append(i+'&regexs='+regexs)
                            elif  any(x in i for x in resolve_url) and  i.startswith('http'):
                                playlist.append(i+'&mode=19')                            
                        else:
                            playlist.append(i)
                    if addon.getSetting('add_playlist') == "false":                    
                            for i in url:
                                alt += 1
                                addLink(i,'%s) %s' %(alt, name.encode('utf-8', 'ignore')),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)                            
                    else:
                        addLink('', name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)
                else:
                    if isXMLSource:
                        addDir(name.encode('utf-8'),ext_url[0].encode('utf-8'),1,thumbnail,fanart,desc,genre,date,None,'source')
                    elif isJsonrpc:
                        addDir(name.encode('utf-8'),ext_url[0],53,thumbnail,fanart,desc,genre,date,None,'source')
                    elif url[0].find('sublink') > 0:
                        addDir(name.encode('utf-8'),url[0],30,thumbnail,fanart,'','','','')
                    else: 
                        addLink(url[0],name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
            except:
                addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))
        print('FINISH GET ITEMS *****')      

def parse_regex(reg_item):
                try:
                    regexs = {}
                    for i in reg_item:
                        regexs[i('name')[0].string] = {}
                        try:
                            regexs[i('name')[0].string]['expre'] = i('expres')[0].string
                            if not regexs[i('name')[0].string]['expre']:
                                regexs[i('name')[0].string]['expre']=''
                        except:
                            addon_log("Regex: -- No Referer --")
                        regexs[i('name')[0].string]['page'] = i('page')[0].string
                        try:
                            regexs[i('name')[0].string]['refer'] = i('referer')[0].string
                        except:
                            addon_log("Regex: -- No Referer --")
                        try:
                            regexs[i('name')[0].string]['connection'] = i('connection')[0].string
                        except:
                            addon_log("Regex: -- No connection --")

                        try:
                            regexs[i('name')[0].string]['notplayable'] = i('notplayable')[0].string
                        except:
                            addon_log("Regex: -- No notplayable --")
                            
                        try:
                            regexs[i('name')[0].string]['noredirect'] = i('noredirect')[0].string
                        except:
                            addon_log("Regex: -- No noredirect --")
                        try:
                            regexs[i('name')[0].string]['origin'] = i('origin')[0].string
                        except:
                            addon_log("Regex: -- No origin --")
                        try:
                            regexs[i('name')[0].string]['includeheaders'] = i('includeheaders')[0].string
                        except:
                            addon_log("Regex: -- No includeheaders --")                            
                            
                        try:
                            regexs[i('name')[0].string]['x-req'] = i('x-req')[0].string
                        except:
                            addon_log("Regex: -- No x-req --")
                        try:
                            regexs[i('name')[0].string]['x-forward'] = i('x-forward')[0].string
                        except:
                            addon_log("Regex: -- No x-forward --")

                        try:
                            regexs[i('name')[0].string]['agent'] = i('agent')[0].string
                        except:
                            addon_log("Regex: -- No User Agent --")
                        try:
                            regexs[i('name')[0].string]['post'] = i('post')[0].string
                        except:
                            addon_log("Regex: -- Not a post")
                        try:
                            regexs[i('name')[0].string]['rawpost'] = i('rawpost')[0].string
                        except:
                            addon_log("Regex: -- Not a rawpost")
                        try:
                            regexs[i('name')[0].string]['htmlunescape'] = i('htmlunescape')[0].string
                        except:
                            addon_log("Regex: -- Not a htmlunescape")


                        try:
                            regexs[i('name')[0].string]['readcookieonly'] = i('readcookieonly')[0].string
                        except:
                            addon_log("Regex: -- Not a readCookieOnly")
                        try:
                            regexs[i('name')[0].string]['cookiejar'] = i('cookiejar')[0].string
                            if not regexs[i('name')[0].string]['cookiejar']:
                                regexs[i('name')[0].string]['cookiejar']=''
                        except:
                            addon_log("Regex: -- Not a cookieJar")                          
                        try:
                            regexs[i('name')[0].string]['setcookie'] = i('setcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a setcookie")
                        try:
                            regexs[i('name')[0].string]['appendcookie'] = i('appendcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a appendcookie")
                                                    
                        try:
                            regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        except:
                            addon_log("Regex: -- no ignorecache")
                    regexs = urllib.parse.quote(repr(regexs))
                    return regexs
                except:
                    regexs = None
                    addon_log('regex Error: '+name.encode('utf-8', 'ignore'))

def getRegexParsed(regexs, url,cookieJar=None,forCookieJarOnly=False,recursiveCall=False,cachedPages={}, rawPost=False, cookie_jar_file=None):
        if not recursiveCall:
            regexs = eval(urllib.parse.unquote(regexs))
        doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
        setresolved=True        
        for k in doRegexs:
            if k in regexs:
                m = regexs[k]
                cookieJarParam=False


                if  'cookiejar' in m:
                    cookieJarParam=m['cookiejar']
                    if  '$doregex' in cookieJarParam:
                        cookieJar=getRegexParsed(regexs, m['cookiejar'],cookieJar,True, True,cachedPages)
                        cookieJarParam=True
                    else:
                        cookieJarParam=True
                if cookieJarParam:
                    if cookieJar==None:
                        cookie_jar_file=None
                        if 'open[' in m['cookiejar']:
                            cookie_jar_file=m['cookiejar'].split('open[')[1].split(']')[0]
                            
                        cookieJar=getCookieJar(cookie_jar_file)
                        if cookie_jar_file:
                            saveCookieJar(cookieJar,cookie_jar_file)
                    elif 'save[' in m['cookiejar']:
                        cookie_jar_file=m['cookiejar'].split('save[')[1].split(']')[0]
                        complete_path=os.path.join(profile,cookie_jar_file)
                        print('complete_path',complete_path)
                        saveCookieJar(cookieJar,cookie_jar_file)
                if  m['page'] and '$doregex' in m['page']:
                    m['page']=getRegexParsed(regexs, m['page'],cookieJar,recursiveCall=True,cachedPages=cachedPages)

                if 'setcookie' in m and m['setcookie'] and '$doregex' in m['setcookie']:
                    m['setcookie']=getRegexParsed(regexs, m['setcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                if 'appendcookie' in m and m['appendcookie'] and '$doregex' in m['appendcookie']:
                    m['appendcookie']=getRegexParsed(regexs, m['appendcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)

                 
                if  'post' in m and '$doregex' in m['post']:
                    m['post']=getRegexParsed(regexs, m['post'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                    print('post is now',m['post'])

                if  'rawpost' in m and '$doregex' in m['rawpost']:
                    m['rawpost']=getRegexParsed(regexs, m['rawpost'],cookieJar,recursiveCall=True,cachedPages=cachedPages,rawPost=True)  
                if 'rawpost' in m and '$epoctime$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime$',getEpocTime())
  
                if 'rawpost' in m and '$epoctime2$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime2$',getEpocTime2())
                link=''
                if m['page'] and m['page'] in cachedPages and not 'ignorecache' in m and forCookieJarOnly==False :
                    link = cachedPages[m['page']]
                else:
                    if m['page'] and  not m['page']=='' and  m['page'].startswith('http'):
                        
                        if '$epoctime$' in m['page']:
                            m['page']=m['page'].replace('$epoctime$',getEpocTime())
                        if '$epoctime2$' in m['page']:
                            m['page']=m['page'].replace('$epoctime2$',getEpocTime2())
                        page_split=m['page'].split('|')
                        pageUrl=page_split[0]
                        header_in_page=None
                        if len(page_split)>1:
                            header_in_page=page_split[1]
                            
                        req = urllib.request.Request(pageUrl)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                        if 'refer' in m:
                            req.add_header('Referer', m['refer'])
                        if 'agent' in m:
                            req.add_header('User-agent', m['agent'])
                        if 'x-req' in m:
                            req.add_header('X-Requested-With', m['x-req'])
                        if 'x-forward' in m:
                            req.add_header('X-Forwarded-For', m['x-forward'])
                        if 'setcookie' in m:
                            print('adding cookie',m['setcookie'])
                            req.add_header('Cookie', m['setcookie'])
                        if 'appendcookie' in m:
                            print('appending cookie to cookiejar',m['appendcookie'])
                            cookiestoApend=m['appendcookie']
                            cookiestoApend=cookiestoApend.split(';')
                            for h in cookiestoApend:
                                n,v=h.split('=')
                                w,n= n.split(':')
                                ck = cookielib.Cookie(version=0, name=n, value=v, port=None, port_specified=False, domain=w, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                                cookieJar.set_cookie(ck)
                        if 'origin' in m:
                            req.add_header('Origin', m['origin'])
                        if header_in_page:
                            header_in_page=header_in_page.split('&')
                            for h in header_in_page:
                                n,v=h.split('=')
                                req.add_header(n,v)


                        if not cookieJar==None:
                            cookie_handler = urllib.request.HTTPCookieProcessor(cookieJar)
                            opener = urllib.request.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                            opener = urllib.request.install_opener(opener)
                            if 'noredirect' in m:
                                opener2 = urllib.request.build_opener(NoRedirection)
                                opener = urllib.request.install_opener(opener2)
                                
                        if 'connection' in m:
                            print('..........................connection//////.',m['connection'])
                            from keepalive import HTTPHandler
                            keepalive_handler = HTTPHandler()
                            opener = urllib.request.build_opener(keepalive_handler)
                            urllib.request.install_opener(opener)
                        post=None

                        if 'post' in m:
                            postData=m['post']
                            if '$LiveStreamRecaptcha' in postData:
                                (captcha_challenge,catpcha_word)=processRecaptcha(m['page'])
                                if captcha_challenge:
                                    postData+='recaptcha_challenge_field:'+captcha_challenge+',recaptcha_response_field:'+catpcha_word
                            splitpost=postData.split(',');
                            post={}
                            for p in splitpost:
                                n=p.split(':')[0];
                                v=p.split(':')[1];
                                post[n]=v
                            post = urllib.urlencode(post)

                        if 'rawpost' in m:
                            post=m['rawpost']
                            if '$LiveStreamRecaptcha' in post:
                                (captcha_challenge,catpcha_word)=processRecaptcha(m['page'])
                                if captcha_challenge:
                                   post+='&recaptcha_challenge_field='+captcha_challenge+'&recaptcha_response_field='+catpcha_word
                        if post:
                            response = urllib.request.urlopen(req,post)
                        else:
                            response = urllib.request.urlopen(req)

                        link = response.read()
                        link=javascriptUnEscape(link)
                        if 'includeheaders' in m:
                            link+=str(response.headers.get('Set-Cookie'))

                        response.close()
                        cachedPages[m['page']] = link                        
                        if forCookieJarOnly:
                            return cookieJar
                        
                    elif m['page'] and  not m['page'].startswith('http'):
                        if m['page'].startswith('$pyFunction:'):
                            val=doEval(m['page'].split('$pyFunction:')[1],'',cookieJar )
                            if forCookieJarOnly:
                                return cookieJar
                            link=val
                        else:
                            link=m['page']
                if '$pyFunction:playmedia(' in m['expre'] or 'ActivateWindow'  in m['expre']   or  any(x in url for x in g_ignoreSetResolved):
                    setresolved=False
                if  '$doregex' in m['expre']:
                    m['expre']=getRegexParsed(regexs, m['expre'],cookieJar,recursiveCall=True,cachedPages=cachedPages)

                if not m['expre']=='':
                    if '$LiveStreamCaptcha' in m['expre']:
                        val=askCaptcha(m,link,cookieJar)
                        url = url.replace("$doregex[" + k + "]", val.encode('utf-8'))
                    elif m['expre'].startswith('$pyFunction:'):
                        val=doEval(m['expre'].split('$pyFunction:')[1],link,cookieJar )
                        if 'ActivateWindow' in m['expre']: return 

                        url = url.replace("$doregex[" + k + "]", val)
                    else:
                        if not link=='':
                            reg = re.compile(m['expre'].encode('utf-8')).search(link)
                            val=''
                            try:
                                val=reg.group(1).strip()
                            except: traceback.print_exc()
                        else:
                            val=m['expre']
                        if rawPost:
                            print('rawpost')
                            val=urllib.parse.quote_plus(val)
                        if 'htmlunescape' in m:
                            import HTMLParser
                            val=HTMLParser.HTMLParser().unescape(val)                     
                        url = url.replace("$doregex[" + k + "]", str(val))#.encode('utf-8'))
                else:           
                    url = url.replace("$doregex[" + k + "]",'')
        if '$epoctime$' in url:
            url=url.replace('$epoctime$',getEpocTime())
        if '$epoctime2$' in url:
            url=url.replace('$epoctime2$',getEpocTime2())

        if '$GUID$' in url:
            import uuid
            url=url.replace('$GUID$',str(uuid.uuid1()).upper())
        if '$get_cookies$' in url:
            url=url.replace('$get_cookies$',getCookiesString(cookieJar))   

        if recursiveCall:
            return url
        url = url.split('|')[0].replace('b\'','').replace('\'','')+'|'+url.split('|')[1].replace('&','&amp;')
        if url=="": 
            return
        else:
            return str(url),setresolved

def playmedia(media_url):
    try:
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), path=media_url )
        listitem.setArt({'icon':"DefaultVideo.png",'thumb':xbmc.getInfoImage( "ListItem.Thumb") })
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    return ''

  
def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):
    cookie_handler = urllib.parse.HTTPCookieProcessor(cookieJar)
    opener = urllib.parse.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    req = urllib.parse.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link

 
def playmedia(media_url):
    try:
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), path=media_url )
        listitem.setArt({'icon':"DefaultVideo.png",'thumb':xbmc.getInfoImage( "ListItem.Thumb") })
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    return ''

 
def javascriptUnEscape(data):
    js=re.findall('unescape\(\'(.*?)\'',data.decode('utf-8'))
    print('js',js)
    if (not js==None) and len(js)>0:
        for j in js:
            data=data.replace(j ,urllib.parse.unquote(j))
    return data
iid=0

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param

def urlsolver(url):
    if addon.getSetting('Updatecommonresolvers') == 'true':
        l = os.path.join(home,'resolverers.py')
        if xbmcvfs.exists(l):
            os.remove(l)

        genesis_url = 'https://raw.githubusercontent.com/lambda81/lambda-addons/master/plugin.video.genesis/commonresolvers.py'
        th= urllib.request.urlretrieve(genesis_url,l)
        addon.setSetting('Updatecommonresolvers', 'false')
    try:
        import resolverers
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(RisingTides,Please enable Update Commonresolvers to Play in Settings. - ,10000)")

    resolved=resolverers.get(url).result
    if url == resolved or resolved is None:
        xbmc.executebuiltin("XBMC.Notification(RisingTides,Using resolveurl module.. - ,5000)")
        import resolveurl
        host = resolveurl.HostedMediaFile(url)
        if host:
            resolver = resolveurl.resolve(url)
            resolved = resolver
    if resolved :
        if isinstance(resolved,list):
            for k in resolved:
                quality = addon.getSetting('quality')
                if k['quality'] == 'HD'  :
                    resolver = k['url']
                    break
                elif k['quality'] == 'SD' :
                    resolver = k['url']
                elif k['quality'] == '1080p' and addon.getSetting('1080pquality') == 'true' :
                    resolver = k['url']
                    break
        else:
            resolver = resolved
    return resolver


def play_playlist(name, mu_playlist):
        import urlparse
        if addon.getSetting('ask_playlist_items') == 'true':
            names = []
            for i in mu_playlist:
                d_name=urlparse.urlparse(i).netloc
                if d_name == '':
                    names.append(name)
                else:
                    names.append(d_name)
            dialog = xbmcgui.Dialog()
            index = dialog.select('Choose a video source', names)
            if index >= 0:
                if "&mode=19" in mu_playlist[index]:
                    xbmc.Player().play(urlsolver(mu_playlist[index].replace('&mode=19','')))
                elif "$doregex" in mu_playlist[index] :

                    sepate = mu_playlist[index].split('&regexs=')

                    url,setresolved = getRegexParsed(sepate[1], sepate[0])
                    xbmc.Player().play(url)
                else:
                    url = mu_playlist[index]
                    xbmc.Player().play(url)
        else:
            playlist = xbmc.PlayList(1)
            playlist.clear()
            item = 0
            for i in mu_playlist:
                item += 1
                info = xbmcgui.ListItem('%s) %s' %(str(item),name))
                playlist.add(i, info)
                xbmc.executebuiltin('playlist.playoffset(video,0)')


def addDir(name,url,mode,iconimage,fanart,description,genre,date,credits,showcontext=False):
        
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&iconimage="+urllib.parse.quote_plus(iconimage)+"&fanart="+urllib.parse.quote_plus(fanart)
        ok=True
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name)
        liz.setArt({"icon":iconimage, "thumb":iconimage})
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date, "credits": credits })
        liz.setProperty("Fanart_Image", fanart)
        if showcontext:
            contextMenu = []
            if showcontext == 'source':
                if name.decode(encoding='UTF-8') in str(SOURCES):
                    contextMenu.append(('Remove from Sources','XBMC.RunPlugin(%s?mode=8&name=%s)' %(sys.argv[0], urllib.parse.quote_plus(name))))
            elif showcontext == 'download':
                contextMenu.append(('Download','XBMC.RunPlugin(%s?url=%s&mode=9&name=%s)'
                                    %(sys.argv[0], urllib.parse.quote_plus(url), urllib.parse.quote_plus(name))))
            elif showcontext == 'fav':
                contextMenu.append(('Remove from Add-on Favorites','XBMC.RunPlugin(%s?mode=6&name=%s)'
                                    %(sys.argv[0], urllib.parse.quote_plus(name))))
                                    
            if not name in FAV:
                contextMenu.append(('Add to Add-on Favorites','XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.parse.quote_plus(name), urllib.parse.quote_plus(url), urllib.parse.quote_plus(iconimage), urllib.parse.quote_plus(fanart), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return ok

def addDir1(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&iconimage="+urllib.parse.quote_plus(iconimage)+"&description="+urllib.parse.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name)
    liz.setArt({"icon":"DefaultFolder.png", "thumb":iconimage})

    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
    liz.setProperty('fanart_image', fanart)
    if mode==102 or mode==9999:
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
    xbmcplugin.endOfDirectory

def addDir2(name,url,mode,iconimage,fanart,channelid=''):
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&channelid="+str(channelid)+"&iconimage="+urllib.parse.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setArt({"icon":"DefaultFolder.png", "thumb":iconimage})

        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': channelid } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def sendJSON( command):
    data = ''
    try:
        data = xbmc.executeJSONRPC(uni(command))
    except UnicodeEncodeError:
        data = xbmc.executeJSONRPC(ascii(command))

    return uni(data)

def SetViewThumbnail():
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')
    elif skin_used == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(511)') 
    else:
        xbmc.executebuiltin('Container.SetViewMode(500)')
    
def pluginquerybyJSON(url):
    json_query = uni('{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":["thumbnail","title","year","dateadded","fanart","rating","season","episode","studio"]},"id":1}') %url

    json_folder_detail = json.loads(sendJSON(json_query))
    for i in json_folder_detail['result']['files'] :
        url = i['file']
        name = removeNonAscii(i['label'])
        thumbnail = removeNonAscii(i['thumbnail'])
        try:
            fanart = removeNonAscii(i['fanart'])
        except Exception:
            fanart = ''
        try:
            date = i['year']
        except Exception:
            date = ''
        try:
            episode = i['episode']
            season = i['season']
            if episode == -1 or season == -1:
                description = ''
            else:
                description = '[COLOR yellow] S' + str(season)+'[/COLOR][COLOR hotpink] E' + str(episode) +'[/COLOR]'
        except Exception:
            description = ''
        try:
            studio = i['studio']
            if studio:
                description += '\n Studio:[COLOR steelblue] ' + studio[0] + '[/COLOR]'
        except Exception:
            studio = ''

        if i['filetype'] == 'file':
            addLink(url,name,thumbnail,fanart,description,'',date,'',None,'',total=len(json_folder_detail['result']['files']))
        else:
            addDir(name,url,53,thumbnail,fanart,description,'',date,'')

def addLink(url,name,iconimage,fanart,description,genre,date,showcontext,playlist,regexs,total,setCookie=""):
        contextMenu =[]
        try:
            name = name.encode('utf-8')
        except: pass
        ok = True
       
        if regexs: 
            mode = '17'
           
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.parse.quote_plus(url), urllib.parse.quote_plus(name))))           
        elif  any(x in url for x in resolve_url) and  url.startswith('http'):
            mode = '19'
          
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.parse.quote_plus(url), urllib.parse.quote_plus(name))))           
        elif url.endswith('&mode=18'):
            url=url.replace('&mode=18','')
            mode = '18' 
          
            contextMenu.append(('[COLOR white]!!Download!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=23&name=%s)'
                                    %(sys.argv[0], urllib.parse.quote_plus(url), urllib.parse.quote_plus(name)))) 
            if addon.getSetting('dlaudioonly') == 'true':
                contextMenu.append(('!!Download [COLOR seablue]Audio!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=24&name=%s)'
                                        %(sys.argv[0], urllib.parse.quote_plus(url), urllib.parse.quote_plus(name))))                                     
        elif url.startswith('magnet:?xt=') or '.torrent' in url:
          
            if '&' in url and not '&amp;' in url :
                url = url.replace('&','&amp;')
            url = 'plugin://plugin.video.pulsar/play?uri=' + url
            mode = '12'
                     
        else: 
            mode = '12'
      
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.parse.quote_plus(url), urllib.parse.quote_plus(name))))           
        u=sys.argv[0]+"?"
        play_list = False
      
        if playlist:
            if addon.getSetting('add_playlist') == "false":
                u += "url="+urllib.parse.quote_plus(url)+"&mode="+mode
            else:
                u += "mode=13&name=%s&playlist=%s" %(urllib.parse.quote_plus(name), urllib.parse.quote_plus(str(playlist).replace(',','||')))
                name = name + '[COLOR magenta] (' + str(len(playlist)) + ' items )[/COLOR]'
                play_list = True
        else:
            u += "url="+urllib.parse.quote_plus(url)+"&mode="+mode
        if regexs:
            u += "&regexs="+regexs
        if not setCookie == '':
            u += "&setCookie="+urllib.parse.quote_plus(setCookie)
  
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name)
        liz.setArt({"icon":"DefaultFolder.png", "thumb":iconimage})

        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date })
        liz.setProperty("Fanart_Image", fanart)
        
        if (not play_list) and not any(x in url for x in g_ignoreSetResolved):
            if regexs:
                if '$pyFunction:playmedia(' not in urllib.parse.unquote_plus(regexs) and 'notplayable' not in urllib.parse.unquote_plus(regexs)  :
                    liz.setProperty('IsPlayable', 'true')
            else:
                liz.setProperty('IsPlayable', 'true')
        else:
            addon_log( 'NOT setting isplayable'+url)
       
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(
                    ('Remove from Add-on Favorites','XBMC.RunPlugin(%s?mode=6&name=%s)'
                     %(sys.argv[0], urllib.parse.quote_plus(name)))
                     )
            elif not name in FAV:
                fav_params = (
                    '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
                    %(sys.argv[0], urllib.parse.quote_plus(name), urllib.parse.quote_plus(url), urllib.parse.quote_plus(iconimage), urllib.parse.quote_plus(fanart))
                    )
                if playlist:
                    fav_params += 'playlist='+urllib.parse.quote_plus(str(playlist).replace(',','||'))
                if regexs:
                    fav_params += "&regexs="+regexs
                contextMenu.append(('Add to Add-on Favorites','XBMC.RunPlugin(%s)' %fav_params))
            liz.addContextMenuItems(contextMenu)
       
        if not playlist is None:
            if addon.getSetting('add_playlist') == "false":
                playlist_name = name.split(') ')[1]
                contextMenu_ = [
                    ('Play '+playlist_name+' PlayList','XBMC.RunPlugin(%s?mode=13&name=%s&playlist=%s)'
                     %(sys.argv[0], urllib.parse.quote_plus(playlist_name), urllib.parse.quote_plus(str(playlist).replace(',','||'))))
                     ]
                liz.addContextMenuItems(contextMenu_)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,totalItems=total)
        return ok

def playsetresolved2(url, name, iconimage, setresolved=True):
    print("playsetresolved2 entry ")
    reg=None
    if url is None:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return


    if setresolved:
        setres = True
        if '$$LSDirect$$' in url:
            url = url.replace('$$LSDirect$$', '')
            setres = False
        if reg and 'notplayable' in reg:
            setres = False

        liz = xbmcgui.ListItem(name)
        liz.setArt({'thumb': iconimage,
                    'icon': iconimage})
        liz.setInfo(type='Video', infoLabels={'Title': name, 'mediatype': 'video'})
        liz.setProperty("IsPlayable", "true")
        if True :
            url = url.replace('&mode=20', '')
            if '$$lic' in url:
                url, lic = url.split('$$lic=')
                lic = urllib.parse.unquote_plus(lic)
                if '{SSM}' not in lic:
                    lic += '||R{SSM}|'
                liz.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
                liz.setProperty('inputstream.adaptive.license_key', lic)

            if '|' in url:
                url, strhdr = url.split('|')
                liz.setProperty('inputstream.adaptive.stream_headers', strhdr)

            if '.m3u8' in url:
                liz.setProperty('inputstream', 'inputstream.adaptive')
                liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
                liz.setMimeType('application/vnd.apple.mpegstream_url')
                liz.setContentLookup(False)
                print("playsetresolved2 m3u8 in url ",url)

            elif '.mpd' in url or 'format=mpd' in url:
                liz.setProperty('inputstream', 'inputstream.adaptive')
                liz.setProperty('inputstream.adaptive.manifest_type', 'mpd')
                liz.setMimeType('application/dash+xml')
                liz.setContentLookup(False)

            elif '.ism' in url:
                liz.setProperty('inputstream', 'inputstream.adaptive')
                liz.setProperty('inputstream.adaptive.manifest_type', 'ism')
                liz.setMimeType('application/vnd.ms-sstr+xml')
                liz.setContentLookup(False)

        liz.setPath(url)
        if not setres:
            xbmc.Player().play(url)
        else:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

    else:
        xbmc.executebuiltin('RunPlugin(' + url + ')')

def playsetresolved(url,name,iconimage,setresolved=True):
    if setresolved:
        liz = xbmcgui.ListItem(name)
        liz.setArt({"thumb":iconimage})

        liz.setInfo(type='Video', infoLabels={'Title':name})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
        #xbmc.Player().play(url, liz)
    else:
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')      

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
    pass

params=get_params()

url=None
name=None
mode=None
playlist=None
iconimage=None
fanart=FANART
playlist=None
fav_mode=None
regexs=None

try:
    url=urllib.parse.unquote_plus(params["url"])#.decode('utf-8')
except:
    pass
try:
    name=urllib.parse.unquote_plus(params["name"])
except:
    pass
try:
    iconimage=urllib.parse.unquote_plus(params["iconimage"])
except:
    pass
try:
    fanart=urllib.parse.unquote_plus(params["fanart"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    playlist=eval(urllib.parse.unquote_plus(params["playlist"]).replace('||',','))
except:
    pass
try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    regexs=params["regexs"]
except:
    pass
try:        
    channelid=urllib.parse.unquote_plus(params["channelid"])      
except:     
    pass

addon_log("Mode: "+str(mode))
if not url is None:
    addon_log("URL: "+str(url.encode('utf-8')))
addon_log("Name: "+str(name))

if mode==None:
    addon_log("Index")
    SKindex()   

elif mode==1:
    addon_log("getData mode1")
    getData(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==2:
    addon_log("getChannelItems mode2")
    getChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==3:
    getSubChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


elif mode==4:
    addon_log("geturl mode4")
    get(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==10:
    play(url,name)

elif mode==11:
    addSource(url)

elif mode==12:
    import six
    addon_log("setResolvedUrl mode12")
    item = xbmcgui.ListItem(name)
    if '$$lic' in url:
        url, lic = url.split('$$lic=')
        lic = urllib.parse.unquote_plus(lic)
        if '{SSM}' not in lic:
            lic += '||R{SSM}|'
        item.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
        item.setProperty('inputstream.adaptive.license_key', lic)
    if '|' in url:
        url, strhdr = url.split('|')
        item.setProperty('inputstream.adaptive.stream_headers', strhdr)
        item.setPath(url)
    if '.m3u8' in url:
        if six.PY2:
            item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        else:
            item.setProperty('inputstream', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        item.setMimeType('application/vnd.apple.mpegstream_url')
        item.setContentLookup(False)

    elif '.mpd' in url or 'format=mpd' in url:
        if six.PY2:
            item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        else:
            item.setProperty('inputstream', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
        item.setMimeType('application/dash+xml')
        item.setContentLookup(False)

    elif '.ism' in url:
        if six.PY2:
            item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        else:
            item.setProperty('inputstream', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'ism')
        item.setMimeType('application/vnd.ms-sstr+xml')
        item.setContentLookup(False)
    item.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

elif mode==13:
    addon_log("play_playlist")
    play_playlist(name, playlist)

elif mode==17:
    addon_log("getRegexParsed")
    url,setresolved = getRegexParsed(regexs, url)
    if url:
        playsetresolved2(url,name,iconimage,setresolved) #???????????????????????????????????????????
    else:
        xbmc.executebuiltin("XBMC.Notification(RisingTides ,Failed to extract regex. - "+"this"+",4000,"+icon+")")
    
elif mode==27:
    addon_log("Using IMDB id to play in Pulsar")
    pulsarIMDB=search(url)
    xbmc.Player().play(pulsarIMDB)

elif mode==30:
    GetSublinks(name,url,iconimage,fanart)

elif mode==33:
    scrape()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==34:
    HIGHLIGHTS_LINKS(name,url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==36:
    PLAYSTREAM(name,url,iconimage)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==40:
    SearchChannels()
    SetViewThumbnail()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==53:
    addon_log("Requesting JSON-RPC Items")
    pluginquerybyJSON(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==65:
    CHECKLINKS(name,url,iconimage)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==9999:
    import xbmcgui,xbmcplugin
    from resources.root import resolvers
    url = resolvers.resolve(url)
    liz = xbmcgui.ListItem(name)
    liz.setArt({"icon":iconimage, "thumb":iconimage})

    liz.setInfo(type='Video', infoLabels='')
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)