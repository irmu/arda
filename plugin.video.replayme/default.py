import xbmcaddon,os,requests,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,resolveurl,liveresolver


AddonTitle     = "REPLAYME"
addon_id       = 'plugin.video.replayme'
art            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
addon_fanart   = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))
icon           = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
baseurl        = 'http://bit.ly/REPLYSNEW2'

def INDEX():
        url=baseurl
        link=open_url(url)
        match= re.compile('<item>(.+?)</item>').findall(link)
        for item in match:
            try:
                if '<folder>'in item:
                                data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                for name,url,iconimage,fanart in data:
                                        addDir(name,url,2,iconimage,fanart)
                else:
                                links=re.compile('<link>(.+?)</link>').findall(item)
                                if len(links)==1:
                                        data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                                        lcount=len(match)
                                        for name,url,iconimage,fanart in data:
                                                addLink(name,url,4,iconimage,fanart)
                                elif len(links)>1:
                                        name=re.compile('<title>(.+?)</title>').findall(item)[0]
                                        iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                                        fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                                        addLink(name,url2,7,iconimage,fanart)
            except:pass
    
def GETPLAYLIST(name,url,iconimage,fanart):
        link=open_url(url)
        match= re.compile('<item>(.+?)</item>').findall(link)
        count=len(match)
        for item in match:
            try:
                if '<folder>'in item: FOLDER(item)
                else:GETPLAYLISTCONTENT(item,url)
            except:pass
            

def GETPLAYLISTCONTENT(item,url):
        links=re.compile('<link>(.+?)</link>').findall(item)
        data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
        if len(links)==1:
                data=re.compile('<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
                for name,url,iconimage,fanart in data:
                        addLink(name,url,4,iconimage,fanart)
        elif len(links)>1:
                name=re.compile('<title>(.+?)</title>').findall(item)[0]
                iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(item)[0]
                fanart=re.compile('<fanart>(.+?)</fanart>').findall(item)[0]
                addLink(name,url,7,iconimage,fanart)

def FOLDER(item):
        data=re.compile('<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>').findall(item)
        for name,url,iconimage,fanart in data:
                addDir(name,url,2,iconimage,fanart)

def PLAYLINKS(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def CHECKLINKS(name,url,iconimage):
        try:
                if resolveurl.HostedMediaFile(url).valid_url():
                        url = resolveurl.HostedMediaFile(url).resolve()
                        PLAYLINKS(name,url,iconimage)
                elif liveresolver.isValid(url)==True:
                        url=liveresolver.resolve(url)
                        PLAYLINKS(name,url,iconimage)
                else:PLAYLINKS(name,url,iconimage)
        except:
                notification(addtags('[COLOR red]REPLAYME[/COLOR]'),'Stream Unavailable', '3000', icon)

def GETMULTI(name,url,iconimage):
    streamurl=[]
    streamname=[]
    streamicon=[]
    link=open_url(url)
    urls=re.compile('<title>'+re.escape(name)+'</title>(.+?)</item>',re.DOTALL).findall(link)[0]
    iconimage=re.compile('<thumbnail>(.+?)</thumbnail>').findall(urls)[0]
    links=[]
    if '<link>' in urls:
                nlinks=re.compile('<link>(.+?)</link>').findall(urls)
                for nlink in nlinks:
                        links.append(nlink)
    i=1
    for sturl in links:
                sturl2=sturl
                if '(' in sturl:
                        sturl=sturl.split('(')[0]
                        caption=str(sturl2.split('(')[1].replace(')',''))
                        streamurl.append(sturl)
                        streamname.append(caption)
                else:
                        domain=sturl.split('/')[2].replace('www.','')                        
                        streamurl.append( sturl )
                        streamname.append('Link '+str(i)+ ' | ' +domain)
                i=i+1
    dialog = xbmcgui.Dialog()
    select = dialog.select(name,streamname)
    if select < 0:quit()
    else:
        url = streamurl[select]
        CHECKLINKS(name,url,iconimage)

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")

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

def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    link=link.replace('\n','').replace('\r','').replace('<fanart></fanart>','<fanart>x</fanart>').replace('<thumbnail></thumbnail>','<thumbnail>x</thumbnail>')
    return link  

def addItem(name,url,mode,iconimage,fanart,description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def addDir(name,url,mode,iconimage,fanart):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
          
def resolve(name,url):
    if '.m3u8' in url or '.mp4' in url:
        xbmc.Player().play(url, xbmcgui.ListItem(name))

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None; fanart=None; description=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
try: description=urllib.unquote_plus(["description"])
except: pass

if mode==None or url==None or len(url)<1:INDEX()
elif mode==2: GETPLAYLIST(name,url,iconimage,fanart)
elif mode==3: GETPLAYLISTCONTENT(name,url,iconimage,fanart)
elif mode==4: CHECKLINKS(name,url,iconimage)
elif mode==5: PLAYLINKS(name,url,iconimage)
elif mode==7: GETMULTI(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

