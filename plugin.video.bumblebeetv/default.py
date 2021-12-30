# -*- coding: utf-8 -*-

"""
	Bumblebee Tv
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
"""

### Imports ###
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs,base64,os,re,requests,json,urllib,urllib2
import __builtin__
from resources.lib import tools
import resolveurl as RESOLVE

skin_used 			= xbmc.getSkinDir()
addon_id 			= xbmcaddon.Addon().getAddonInfo('id')
ownAddon            = xbmcaddon.Addon(id=addon_id)
tmdb_api_key        = ownAddon.getSetting('tmdb_api_key')
addon_name 			= xbmcaddon.Addon().getAddonInfo('name')
home_folder 		= xbmc.translatePath('special://home/')
addon_folder 		= os.path.join(home_folder, 'addons')
art_path 			= os.path.join(addon_folder, addon_id)
resources_path		= os.path.join(art_path, 'resources')
other_art_path		= os.path.join(resources_path, 'art')
user_data_folder 	= os.path.join(home_folder, 'userdata')
addon_data_folder 	= os.path.join(user_data_folder, 'addon_data')
addon_icon 			= os.path.join(art_path,'icon.png')
addon_fanart 		= os.path.join(art_path,'fanart.jpg')
content_type    	= "movies"

def start():
	tools.addDir("[COLOR=orange]Bumblebee Movies[/COLOR]","bumblebee_movies",1,os.path.join(other_art_path,'bumblebee.png'),os.path.join(other_art_path,'bumblebeeback.jpg'),"Bumblebee Movies")
	tools.addDir("[COLOR=orange]Bumblebee Comedy[/COLOR]","bumblebee_comedy",2,os.path.join(other_art_path,'bumblebee.png'),os.path.join(other_art_path,'bumblebeeback.jpg'),"Bumblebee Comedy")
	tools.addDir("[COLOR=orange]Bumblebee Lifestyle[/COLOR]","bumblebee_lifestyle",3,os.path.join(other_art_path,'bumblebee.png'),os.path.join(other_art_path,'bumblebeeback.jpg'),"Bumblebee Lifestyle")
	tools.addDir("[COLOR=orange]Bumblebee News[/COLOR]","bumblebee_news",4,os.path.join(other_art_path,'bumblebee.png'),os.path.join(other_art_path,'bumblebeeback.jpg'),"Bumblebee News")
	tools.addDir("[COLOR=orange]Bumblebee Gaming[/COLOR]","bumblebee_gaming",5,os.path.join(other_art_path,'bumblebee.png'),os.path.join(other_art_path,'bumblebeeback.jpg'),"Bumblebee Gaming")

def urlsolver(url):
	host = RESOLVE.HostedMediaFile(url)
	ValidUrl = host.valid_url()
	if ValidUrl == True :
		resolver = RESOLVE.resolve(url)
	elif ValidUrl == False:
		from resources.lib import genesisresolvers
		resolved=genesisresolvers.get(url).result
		if resolved :
			if isinstance(resolved,list):
				for k in resolved:
					quality = setting('quality')
					if k['quality'] == 'HD'  :
						resolver = k['url']
						break
					elif k['quality'] == 'SD' :
						resolver = k['url']
					elif k['quality'] == '10080p' and setting('10080pquality') == 'true' :
						resolver = k['url']
						break
			else:
				resolver = resolved
	return resolver

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

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None


try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass

	### Modes ###
if mode==None or url==None or len(url)<1:
	start()
elif mode==1:
	tools.bumblebee_movies(url)
elif mode==2:
	tools.bumblebee_comedy(url)
elif mode==3:
	tools.bumblebee_lifestyle(url)
elif mode==4:
	tools.bumblebee_news(url)
elif mode==5:
	tools.bumblebee_gaming(url)
elif mode==6:
	tools.bumblebee_movies_section(url)
elif mode==7:
	tools.bumblebee_lifestle_section(url)
elif mode==90:
	html = requests.get(url).content
	match = re.compile('"url":"(.+?)"',re.DOTALL).findall(html)
	liz = xbmcgui.ListItem(name, path=match[0])
	infoLabels={"title": name}
	liz.setInfo(type="video", infoLabels=infoLabels)
	liz.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
elif mode==91:
	link = "https://www.youtube.com/watch?v=%s"%(url)
	link = urlsolver(link)
	liz = xbmcgui.ListItem(name, path=link)
	infoLabels={"title": name}
	liz.setInfo(type="video", infoLabels=infoLabels)
	liz.setProperty('IsPlayable', 'true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

xbmcplugin.endOfDirectory(int(sys.argv[1]))