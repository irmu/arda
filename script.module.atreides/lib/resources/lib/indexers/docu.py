# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import os
import re
import requests
import sys
import traceback
import urllib
import urlparse

import xbmc
import xbmcplugin

from random import randint
from resources.lib.dialogs import notification
from resources.lib.modules import cache, client, control, jsonmenu, log_utils, source_utils, utils

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()


unreg_items = {'myspace', 'nfb.ca', 'snagfilms', 'dotsub', 'en.musicplayon.com', 'vkontakte.ru', 'veehd.com',
               'liveleak.com', 'imdb.com', 'disclose.tv', 'videoweed.es', 'putlocker', 'vid.ag', 'vice.com'}
"""
Examples for unreg_items, to look into future support or if requested to fix by adding to/fixing in resolveurl

Docu Heaven - thevideobee: Music - Amy
Docu Heaven - snagfiles: Music - Jimi Hendrix the Uncut Story
Docu Heaven - dotsub: Music - The Man in the Mirror
Docu Heaven - en.musicplayon.com: Music - Prince: The Glory Years
Docu Heaven - vkontakte.ru: Music - Paul Kalkbrenner: A live documentary
Docu Heaven - veehd.com: The Abandoned Marsh
Docu Heaven - liveleak.com: Lost Nuke
Docu Heaven - imdb.com: Eceti Ranch
Docu Heaven - disclose.tv: The Revelation of the Pyramids
Docu Heaven - videoweed.es: EP2/4 Wonders of the Universe
Docu Heaven - putlocker: EP 1/6 The Private Life of Plants
Docu Heaven - vid.ag: Jim: The James Foley Story
Docu Heaven - vice.com: Our Rising Oceans

"""


class documentary:
    def __init__(self):
        pass

    def root(self):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load('documentary')
        rootMenu.process('documentaries_root')
        self.endDirectory(category='Documentaries')

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        if 'http' not in thumb:
            thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []

        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, contentType='addons', sortMethod=control.xDirSort.NoSort, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
        if sortMethod is not control.xDirSort.NoSort:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=True)


class topdocs:
    def __init__(self):
        self.base_link = 'https://topdocumentaryfilms.com/'
        self.cat_link = '%swatch-online/' % (self.base_link)
        self.items = []

    def get(self, url=None):
        if url is None:
            self.root()
        else:
            self.items = self.docu_list(url)
            control.addItems(syshandle, self.items)
            self.endDirectory('videos', category='Top Documentaries')

    def root(self):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load('documentary')
        rootMenu.process('topdoc_root')
        self.endDirectory(category='Top Documentaries')

    def docu_list(self, url):
        self.items = []
        try:

            html = client.request(url)
            cat_list = client.parseDOM(html, 'article', attrs={'class': 'module'})

            for content in cat_list:
                docu_info = re.findall('<h2>(.+?)</h2>', content)[0]

                docu_url = re.findall('href="(.+?)"', docu_info)[0]

                docu_title = re.findall('href=".+?">(.+?)</a>', docu_info)[0].strip()
                docu_title = utils.convert(docu_title).encode('utf-8')

                docu_plot = re.findall('<p>(.+?)</p>', content)[0]
                docu_plot = utils.convert(docu_plot).encode('utf-8')

                try:
                    docu_icon = re.findall('img data-src="(.+?)"', content)[0]
                except Exception:
                    docu_icon = client.parseDOM(content, 'img', ret='src')[0]

                item = control.item(label=docu_title)
                item.setProperty("IsPlayable", "true")
                item.setArt({"thumb": docu_icon, "icon": docu_icon})
                item.setInfo(type="video", infoLabels={"Title": docu_title, "mediatype": "video", 'plot': docu_plot, 'mediatype': 'video', 'plotoutline': docu_plot})
                try:
                    item.setContentLookup(False)
                except AttributeError:
                    pass
                url = '%s?action=docuTDNavigator&docuPlay=%s' % (sysaddon, docu_url)
                self.items.append((url, item, False))
            try:
                navi_content = client.parseDOM(html, 'div', attrs={'class': 'pagination module'})[0]
                links = client.parseDOM(navi_content, 'a', ret='href')
                link = links[(len(links)-1)]
                next_url = '%s?action=docuTDNavigator&docuCat=%s' % (sysaddon, link)

                item = control.item(label=control.lang(32053).encode('utf-8'))
                item.setArt({"thumb": control.addonNext(), "icon": control.addonNext()})
                self.items.append((next_url, item, True))
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('Top Docs: Docu_List: Exception in Nav - ' + str(failure))
                pass
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Top Docs: Docu_List: Exception in List - ' + str(failure))
            pass
        return self.items

    def docu_play(self, url):
        try:
            docu_page = client.request(url)
            docu_item = client.parseDOM(docu_page, 'meta', attrs={'itemprop': 'embedUrl'}, ret='content')[0]
            if 'http:' not in docu_item and 'https:' not in docu_item:
                docu_item = 'https:' + docu_item
            url = docu_item

            try:
                docu_title = re.findall('meta property="og:title" content="(.+?)"', docu_page)[0]
            except Exception:
                docu_title = re.findall('<title>(.+?)</title>', docu_page)[0]

            try:
                docu_icon = re.findall('meta property="og:image" content="(.+?)"', docu_page)[0]
            except Exception:
                docu_icon = control.addonIcon()

            if 'youtube' in url:
                if 'list=' not in url:
                    video_id = client.parseDOM(docu_page, 'div', attrs={'class': 'youtube-player'}, ret='data-id')[0]
                    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
                else:
                    playlist_id = url.split('list=')[1]
                    url = 'plugin://plugin.video.youtube/play/?playlist_id=%s&play=1' % playlist_id
            else:
                url = source_utils.uResolve(url)
                if url is None:
                    log_utils.log('Top Documentary Films: Unable to resolve url: ' + str(url))
                    notification.infoDialog(msg='Invalid Host - Report To Developer: ' + str(url))
                    return

            li = control.item(docu_title, path=url)
            li.setArt({"thumb": docu_icon, "icon": docu_icon})
            li.setInfo(type="video", infoLabels={"Title": docu_title})
            li.setProperty('IsPlayable', 'true')

            control.resolve(handle=int(sys.argv[1]), succeeded=True, listitem=li)
        except Exception as e:
            log_utils.log('docu_play: Exception - ' + str(e))
            pass

    def sort_key(self, elem):
        if elem[0] == "auto":
            return 1
        else:
            return int(elem[0].split("@")[0])

    # Code originally written by gujal, as part of the DailyMotion Addon in the official Kodi Repo. Modified to fit the needs here.
    def getDailyMotionStream(self, id):
        headers = {'User-Agent': 'Android'}
        cookie = {'Cookie': "lang=en_US; ff=off"}
        r = requests.get("http://www.dailymotion.com/player/metadata/video/"+id, headers=headers, cookies=cookie)
        content = r.json()
        if content.get('error') is not None:
            Error = (content['error']['title'])
            xbmc.executebuiltin('XBMC.Notification(Info:,' + Error + ' ,5000)')
            return
        else:
            cc = content['qualities']

            cc = cc.items()

            cc = sorted(cc, key=self.sort_key, reverse=True)
            m_url = ''
            other_playable_url = []

            for source, json_source in cc:
                source = source.split("@")[0]
                for item in json_source:

                    m_url = item.get('url', None)

                    if m_url:
                        if source == "auto":
                            continue

                        elif int(source) <= 2:
                            if 'video' in item.get('type', None):
                                return m_url

                        elif '.mnft' in m_url:
                            continue
                        other_playable_url.append(m_url)

            if len(other_playable_url) > 0:  # probably not needed, only for last resort
                for m_url in other_playable_url:

                    if '.m3u8?auth' in m_url:
                        rr = requests.get(m_url, cookies=r.cookies.get_dict(), headers=headers)
                        if rr.headers.get('set-cookie'):
                            print 'adding cookie to url'
                            strurl = re.findall(
                                '(http.+)', rr.text)[0].split('#cell')[0]+'|Cookie='+rr.headers['set-cookie']
                        else:
                            strurl = re.findall('(http.+)', rr.text)[0].split('#cell')[0]
                        return strurl

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        if 'http' not in thumb:
            thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []

        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, contentType='addons', sortMethod=control.xDirSort.NoSort, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
        if sortMethod is not control.xDirSort.NoSort:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=True)

    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                item = control.item(label=name)

                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


class docuheaven:
    def __init__(self):
        self.base_link = 'https://documentaryheaven.com/'
        self.cat_link = '%swatch-online/' % (self.base_link)
        self.items = []

    def get(self, url=None):
        if url is None:
            self.root()
        else:
            self.items = self.docu_list(url)
            control.addItems(syshandle, self.items)
            self.endDirectory('videos', category='Documentary Heaven')

    def root(self):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load('documentary')
        rootMenu.process('docuh_root')
        self.endDirectory(category='Documentary Heaven')

    def docu_list(self, url):
        try:
            self.items = []

            url = urlparse.urljoin(self.base_link, url)

            html = client.request(url)
            cat_list = client.parseDOM(html, 'article')

            for content in cat_list:
                try:
                    docu_info = re.findall('<h2>(.+?)</h2>', content)[0]

                    docu_url = re.findall('href="(.+?)"', docu_info)[0]

                    docu_title = re.findall('href=".+?">(.+?)</a>', docu_info)[0].strip()
                    docu_title = utils.convert(docu_title).encode('utf-8')

                    try:
                        docu_plot = re.findall('<p>(.*?)</p>', content)[0]
                    except Exception:
                        docu_plot = client.parseDOM(content, 'p')[0]
                    docu_plot = utils.convert(docu_plot).encode('utf-8')

                    try:
                        docu_icon = re.findall('img data-src="(.+?)"', content)[0]
                    except Exception:
                        docu_icon = client.parseDOM(content, 'img', ret='src')[0]

                    item = control.item(label=docu_title)
                    item.setProperty("IsPlayable", "true")
                    item.setArt({"thumb": docu_icon, "icon": docu_icon})
                    item.setInfo(type="video", infoLabels={"Title": docu_title, "mediatype": "video", 'plot': docu_plot, 'mediatype': 'video', 'plotoutline': docu_plot})
                    try:
                        item.setContentLookup(False)
                    except AttributeError:
                        pass
                    url = '%s?action=docuDHNavigator&docuPlay=%s' % (sysaddon, docu_url)
                    self.items.append((url, item, False))
                except Exception:
                    failure = traceback.format_exc()
                    log_utils.log('Documentary Heaven: Exception in Loop - ' + str(failure))
            try:
                navi_content = client.parseDOM(html, 'div', attrs={'class': 'numeric-nav'})[0]
                if 'next page' in navi_content.lower():
                    links = client.parseDOM(navi_content, 'a', ret='href')
                    link = links[(len(links)-1)]
                    next_url = '%s?action=docuDHNavigator&docuCat=%s' % (sysaddon, link)

                    item = control.item(label=control.lang(32053).encode('utf-8'))
                    item.setArt({"thumb": control.addonNext(), "icon": control.addonNext()})
                    self.items.append((next_url, item, True))
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('Documentary Heaven: Exception in Nav - ' + str(failure))
                pass
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Documentary Heaven: Exception in List - ' + str(failure))
            pass

        return self.items

    def docu_play(self, url):
        try:
            docu_page = client.request(url)
            docu_item = client.parseDOM(docu_page, 'div', attrs={'class': 'video'})[0]
            url = client.parseDOM(docu_item, 'iframe', ret='src')[0]

            try:
                docu_title = re.findall('meta property="og:title" content="(.+?)"', docu_page)[0]
            except Exception:
                docu_title = re.findall('<title>(.+?)</title>', docu_page)[0]

            try:
                docu_icon = re.findall('meta property="og:image" content="(.+?)"', docu_page)[0]
            except Exception:
                docu_icon = control.addonIcon()

            if 'youtube' in url:
                if 'list=' not in url:
                    video_id = url.split('embed/')[-1]
                    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
                else:
                    playlist_id = url.split("=")[-1]
                    url = 'plugin://plugin.video.youtube/play/?playlist_id=%s&play=1' % playlist_id
            elif 'archive.org/embed' in url:
                archive_page = client.request(url)
                video_element = client.parseDOM(archive_page, 'source', ret='src')[0]
                url = urlparse.urljoin('https://archive.org/', video_element)
            else:
                url = source_utils.uResolve(url)
                if url is None:
                    log_utils.log('Documentary Heaven: Unable to resolve url: ' + str(url))
                    notification.infoDialog(msg='Invalid Host - Report To Developer: ' + str(url))
                    return

            li = control.item(docu_title, path=url)
            li.setArt({"thumb": docu_icon, "icon": docu_icon})
            li.setInfo(type="video", infoLabels={"Title": docu_title})
            li.setProperty('IsPlayable', 'true')

            control.resolve(handle=int(sys.argv[1]), succeeded=True, listitem=li)
        except Exception as e:
            log_utils.log('docu_play: Exception - ' + str(e))
            pass

    def sort_key(self, elem):
        if elem[0] == "auto":
            return 1
        else:
            return int(elem[0].split("@")[0])

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        if 'http' not in thumb:
            thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []

        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, contentType='addons', sortMethod=control.xDirSort.NoSort, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
        if sortMethod is not control.xDirSort.NoSort:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=True)

    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                item = control.item(label=name)

                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass

        self.endDirectory(sortMethod=control.xDirSort.NoSort)
