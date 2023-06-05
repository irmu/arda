# -*- coding: utf-8 -*-
#------------------------------------------------------------
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import re
import urllib
import urllib2
from addon.common.addon import Addon



base_url= 'http://www.bnwmovies.com'
addon_id = 'plugin.video.classicbnwmoviesghost'
addon = Addon(addon_id, sys.argv)
local = xbmcaddon.Addon(id=addon_id)
icon = local.getAddonInfo('icon')
fanart = local.getAddonInfo('fanart')
artwork = xbmc.translatePath(os.path.join('special://home', 'addons', addon_id, 'resources', 'art/'))



def CATEGORIES():
    addDir('Year', 'none', 'year', artwork + 'year.png')
    addDir('Action', '/genre/action', 'index', artwork + 'action.png')
    addDir('Adventure', '/genre/adventure', 'index', artwork + 'adventure.png')
    addDir('Classic', '/classic-movies', 'index', artwork + 'classic.png')
    addDir('Comedy', '/genre/comedy', 'index', artwork + 'comedy.png')
    addDir('Drama', '/genre/drama', 'index', artwork + 'drama.png')
    addDir('Horror', '/genre/horror', 'index', artwork + 'horror.png')
    addDir('Mystery', '/genre/mystery', 'index', artwork + 'mystery.png')
    addDir('Romance', '/genre/romance', 'index', artwork + 'romance.png')
    addDir('Sci-fi', '/genre/sci-fi', 'index', artwork + 'sci-fi.png')
    addDir('Thriller', '/genre/thriller', 'index', artwork + 'thriller.png')
    addDir('Western', '/genre/western', 'index', artwork + 'western.png')
    addDir('War', '/genre/war', 'index', artwork + 'war.png')



def year():
    addDir('10s', '/decade/10s', 'index', artwork + 'action.png')
    addDir('20s', '/decade/20s', 'index', artwork + 'action.png')
    addDir('30s', '/decade/30s', 'index', artwork + 'action.png')
    addDir('40s', '/decade/40s', 'index', artwork + 'action.png')
    addDir('50s', '/decade/50s', 'index', artwork + 'action.png')
    addDir('60s', '/decade/60s', 'index', artwork + 'action.png')



def read_file(path):
    if path.startswith('http://') or path.startswith('https://'):
        req = urllib2.Request(path)
        import random
        user_agent = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.75 Safari/537.1')
        req.add_header('User-Agent', random.choice(user_agent))
        temp_file = urllib2.urlopen(req)
    elif os.path.isfile(path):
        temp_file = open(path, 'r')
    else:
        return ''
    contents = temp_file.read()
    temp_file.close()
    return contents



def index(url):
    next_page = ''
    link = read_file(base_url + url)
    match = re.findall('<div class="cat.+"><a href="([^"]+)".+?src="([^"]+)".+?>.+?>([^<]+)<', link)
    np = re.findall('current.>.+?<.+?title=".+?".+?href=".+?com([^"]+)">.+?<', link)
    if len(np) > 0:
        next_page = np[0]
        addDir('[COLOR red]Next Page >>[/COLOR]', next_page, 'index', artwork + 'next.png')
        for url, thumb, name in match:
            addDir(name, url, 'video_link', thumb)



def video_link(url):
    link = read_file(url)
    match = re.findall('<video.+\s.+<source src="([^"]+)"', link)
    for url in match:
        liz = xbmcgui.ListItem(name);
        xbmc.Player().play(url, liz, False)
        sys.exit()



def addDir(name, url, mode, thumb):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)
    liz.setProperty('fanart_image', fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok



mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
# year = addon.queries.get('year', '')
# season = addon.queries.get('season', '')
# episode = addon.queries.get('episode', '')
# show = addon.queries.get('show', '')
# types = addon.queries.get('types', '')


print "Mode is: "+str(mode)
print "URL is: "+str(url)
print "Name is: "+str(name)
print "Thumb is: "+str(thumb)
# print "Year is: "+str(year)
# print "Season is: "+str(season)
# print "Episode is: "+str(episode)
# print "Show is: "+str(show)
# print "Type is: "+str(types)


if mode=='CATEGORIES' or mode==None or url==None or len(url)<1:
        print ""+url
        CATEGORIES()
        
elif mode=='index':
        print ""+url
        index(url)

elif mode == 'year':
        print ""+url
        year()

elif mode=='video_link':
        print ""+url
        video_link(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
