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

'''
2019/5/12: Moved news control timer to news dialog
'''

import os
import sys
import time
import traceback

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from resources.lib.dialogs import notification
from resources.lib.modules import changelog, control, jsonmenu, log_utils, trakt

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()
traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
    ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
    HOMEPATH = xbmc.translatePath('special://home/')
    ADDONSPATH = os.path.join(HOMEPATH, 'addons')
    THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)

    def root(self):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load('main')

        for item in rootMenu.menu['main_menu']:
            try:
                '''
                First things first, let's see if this is an entry with on/off settings and if we should display it.
                '''
                try:
                    toggle = item.get('toggle', None)
                    if toggle is not None:
                        if self.getMenuEnabled(toggle) is False:
                            continue
                except Exception:
                    pass

                '''
                Language file support can be done this way
                '''
                title = item.get('title', 'No Title Given')
                tcheck = title
                try:
                    title = control.lang(int(title)).encode('utf-8')
                except Exception:
                    pass

                '''
                Check to see if is a My Lists entry and skip if not enabled
                '''
                try:
                    if tcheck == '32003' or tcheck == '32004':
                        if control.setting('lists.widget') == '0':
                            continue
                except Exception:
                    pass

                '''
                Check to see if is New Movies and skip if not enabled
                '''
                try:
                    if tcheck == '32005':
                        theSetting = control.setting('movie.widget')
                        if theSetting == '0':
                            continue
                        if theSetting == '1':
                            title = title + " (" + control.lang(32321).encode('utf-8') + ")"
                        elif theSetting == '2':
                            title = title + " (" + control.lang(32322).encode('utf-8') + ")"
                        elif theSetting == '3':
                            title = title + " (" + control.lang(32323).encode('utf-8') + ")"
                        elif theSetting == '4':
                            title = title + " (" + control.lang(32324).encode('utf-8') + ")"
                        elif theSetting == '5':
                            title = title + " (" + control.lang(32580).encode('utf-8') + ")"
                except Exception:
                    pass

                '''
                Check to see if is New Episodes entry and skip if not enabled
                '''
                try:
                    if tcheck == '32006':
                        if (traktIndicators is True and control.setting('tv.widget.alt') == '0') or (traktIndicators is False and control.setting('tv.widget') == '0'):
                            continue
                except Exception:
                    pass

                '''
                Check to see if is Downloads entry and skip if not enabled
                '''
                try:
                    if tcheck == '32009':
                        downloads = True if control.setting('downloads') == 'true' and(
                            len(control.listDir(control.setting('movie.download.path'))[0]) > 0
                            or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
                        if downloads is False:
                            continue
                except Exception:
                    pass

                icon = item['thumbnail']
                link = item.get('action', None)

                try:
                    menu_file = item.get('menu_file', None)
                    menu_section = item.get('menu_section', None)
                    link = '%s&menu_file=%s&menu_section=%s' % (link, menu_file, menu_section) if menu_file is not None else link
                except Exception:
                    pass

                try:
                    link = '%s&menu_title=%s' % (link, title)
                except Exception:
                    pass

                try:
                    menu_sort = item.get('menu_sort', None)
                    link = '%s&menu_sort=%s' % (link, menu_sort) if menu_sort is not None else link
                except Exception:
                    pass

                self.addDirectoryItem(title, link, icon, icon)
            except Exception:
                pass

        self.endDirectory()

        newsUpdate = control.setting('NewsUpdate')
        if newsUpdate == '':
            newsUpdate = 1
        else:
            newsUpdate = int(float(newsUpdate))
        if time.time() < newsUpdate:
            return
        newsUpdate = time.time() + (60*60*24*7)
        control.setSetting('NewsUpdate', str(newsUpdate))

        from resources.lib.dialogs import news
        news.load()

    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'):
            return False
        return True

    def movies(self, lite=False):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load('movies')

        for item in rootMenu.menu['movie_menu']:
            try:
                '''
                First things first, let's see if this is an entry with on/off settings and if we should display it.
                '''
                try:
                    toggle = item.get('toggle', None)
                    if toggle is not None:
                        if self.getMenuEnabled(toggle) is False:
                            continue
                except Exception:
                    pass

                '''
                Language file support can be done this way
                '''
                title = item.get('title', 'No Title Given')
                tcheck = title
                try:
                    title = control.lang(int(title)).encode('utf-8')
                except Exception:
                    pass

                '''
                Check to see if is a My Lists entry and skip if not enabled
                '''
                try:
                    if tcheck == '32003':
                        if control.setting('lists.widget') == '0' and lite is True:
                            continue
                except Exception:
                    pass

                '''
                Check to see if is Lite shit and skip as required
                '''
                try:
                    if (tcheck == '32028' or tcheck == '32010') and lite is True:
                        continue
                except Exception:
                    pass

                icon = item['thumbnail']
                link = item.get('action', None)

                try:
                    url = item.get('url', None)
                    link = '%s&url=%s' % (link, url) if url is not None else link
                except Exception:
                    pass
                try:
                    menu_file = item.get('menu_file', None)
                    menu_section = item.get('menu_section', None)
                    link = '%s&menu_file=%s&menu_section=%s' % (link, menu_file, menu_section) if menu_file is not None else link
                except Exception:
                    pass

                try:
                    link = '%s&menu_title=%s' % (link, title)
                except Exception:
                    pass

                self.addDirectoryItem(title, link, icon, icon)
            except Exception:
                pass

        self.endDirectory(category=control.lang(32001).encode('utf-8'))

    def mymovies(self, lite=False):
        self.accountCheck()

        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load('movies')

        for item in rootMenu.menu['mymovies_menu']:
            try:
                '''
                First things first, let's see if this is an entry with on/off settings and if we should display it.
                '''
                try:
                    toggle = item.get('toggle', None)
                    if toggle is not None:
                        if self.getMenuEnabled(toggle) is False:
                            continue
                except Exception:
                    pass

                '''
                Language file support can be done this way
                '''
                title = item.get('title', 'No Title Given')
                tcheck = title
                try:
                    title = control.lang(int(title)).encode('utf-8')
                except Exception:
                    pass

                requires_trakt = item.get('req_trakt', None)
                requires_imdb = item.get('req_imdb', None)
                try:
                    if requires_trakt == '1':
                        if traktCredentials is False:
                            continue
                        if item.get('trakt_indicator', None) == '1' and traktIndicators is False:
                            continue
                        title = "Trakt " + title
                    elif requires_imdb == '1':
                        if imdbCredentials is False:
                            continue
                        title = "IMDB " + title
                except Exception:
                    pass

                try:
                    if (tcheck == '32028' or tcheck == '32010' or tcheck == '32031') and lite is True:
                        continue
                except Exception:
                    pass

                icon = item['thumbnail']
                link = item.get('action', None)

                try:
                    url = item.get('url', None)
                    link = '%s&url=%s' % (link, url) if url is not None else link
                except Exception:
                    pass
                try:
                    menu_file = item.get('menu_file', None)
                    menu_section = item.get('menu_section', None)
                    link = '%s&menu_file=%s&menu_section=%s' % (link, menu_file, menu_section) if menu_file is not None else link
                except Exception:
                    pass

                if item.get('queue', None) == '1':
                    queue = True
                else:
                    queue = False

                context = item.get('context', None)
                if context is not None:
                    context = context.split('|', 1)
                    context = (int(context[0]), context[1])

                self.addDirectoryItem(title, link, icon, icon, queue=queue, context=context)
            except Exception:
                pass

        self.endDirectory(category=control.lang(32003).encode('utf-8'))

    def tvshows(self, lite=False):
        if self.getMenuEnabled('navi.tvReviews') is True:
            self.addDirectoryItem(32623, 'tvReviews', 'reviews.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvGenres') is True:
            self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvNetworks') is True:
            self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvLanguages') is True:
            self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvCertificates') is True:
            self.addDirectoryItem(32015, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvTrending') is True:
            self.addDirectoryItem(32017, 'tvshows&url=trending', 'people-watching.png',
                                  'DefaultRecentlyAddedEpisodes.png')
        if self.getMenuEnabled('navi.tvPopular') is True:
            self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvRating') is True:
            self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvViews') is True:
            self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAiring') is True:
            self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvActive') is True:
            self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvPremier') is True:
            self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tvAdded') is True:
            self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png',
                                  'DefaultRecentlyAddedEpisodes.png', queue=True)
        if self.getMenuEnabled('navi.tvCalendar') is True:
            self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite is False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory(category=control.lang(32002).encode('utf-8'))

    def mytvshows(self, lite=False):
        self.accountCheck()

        if traktCredentials is True and imdbCredentials is True:
            self.addDirectoryItem(
                32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png',
                context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(
                32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png',
                context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

        elif traktCredentials is True:
            self.addDirectoryItem(
                32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png',
                context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(
                32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png',
                context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

        elif imdbCredentials is True:
            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')

        if traktCredentials is True:
            self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

        elif imdbCredentials is True:
            self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

        if traktIndicators is True:
            self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
            self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png',
                                  'DefaultRecentlyAddedEpisodes.png', queue=True)
            self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png',
                                  'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

        if traktCredentials is True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

        if lite is False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32028, 'tvPerson', 'people-search.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory(category=control.lang(32004).encode('utf-8'))

    def jsonMenu(self, menufile, menusection, menuContent='addons', menuSort=control.xDirSort.NoSort, menuCategory=None):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load(menufile)
        rootMenu.process(menusection)
        self.endDirectory(contentType=menuContent, sortMethod=menuSort, category=menuCategory)

    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(
            32559, control.setting('library.movie'),
            'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

        self.endDirectory(category='Library')

    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory(category=control.lang(32009).encode('utf-8'))

    def views(self):
        try:
            control.idle()

            items = [(control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'),
                     (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes')]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1:
                return

            content = items[select][1]

            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels={'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except Exception:
            return

    def accountCheck(self):
        if traktCredentials is False and imdbCredentials is False:
            control.idle()
            notification.infoDialog(msg=control.lang(32042).encode('utf-8'), style='WARNING')
            sys.exit()

    def infoCheck(self, version):
        try:
            notification.infoDialog(msg=control.lang(32074).encode('utf-8'), timer=5000)
            return '1'
        except Exception:
            return '1'

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        if 'http' not in thumb:
            thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []
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
