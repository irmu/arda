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


import sys

from resources.lib.modules import control, log_utils, youtube_menu

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()

# initializes as Kids Corner, functions can override based on action and subid.
class yt_index:
    def __init__(self):
        self.action = 'kidscorner'
        self.base_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIveXRtZW51cy9raWRzbmF0aW9uLw=='.decode('base64')
        self.mainmenu = 'JXNrbm1haW4udHh0'.decode('base64') % (self.base_url)
        self.submenu = 'JXMvJXMudHh0'.decode('base64')
        self.default_icon = 'JXMvaWNvbnMvaWNvbi5wbmc='.decode('base64')
        self.default_fanart = 'JXMvaWNvbnMvZmFuYXJ0LmpwZw=='.decode('base64')

    def init_vars(self, action):
        try:
            if action == 'fitness':
                self.action = 'fitness'
                self.base_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIveXRtZW51cy9maXRuZXNzem9uZS8='.decode('base64')
                self.mainmenu = 'JXNmem1haW4udHh0'.decode('base64') % (self.base_url)
            elif action == 'tvReviews':
                self.action = 'tvReviews'
                self.base_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9hdHJlaWRlc2V4dHJhcy9tYXN0ZXIveXRtZW51cy90aGVjcml0aWNzLw=='.decode('base64')
                self.mainmenu = 'JXN0ZWxldmlzaW9uLnR4dA=='.decode('base64') % (self.base_url)
            self.submenu = self.submenu % (self.base_url, '%s')
            self.default_icon = self.default_icon % (self.base_url)
            self.default_fanart = self.default_fanart % (self.base_url)
        except Exception:
            pass

    def root(self, action):
        try:
            self.init_vars(action)
            menuItems = youtube_menu.youtube_menu().processMenuFile(self.mainmenu)
            for name, section, searchid, subid, playlistid, channelid, videoid, iconimage, fanart, description in menuItems:
                if not subid == 'false':  # Means this item points to a submenu
                    youtube_menu.youtube_menu().addMenuItem(name, self.action, subid, iconimage, fanart, description, True)
                elif not searchid == 'false':  # Means this is a search term
                    youtube_menu.youtube_menu().addSearchItem(name, searchid, iconimage, fanart)
                elif not videoid == 'false':  # Means this is a video id entry
                    youtube_menu.youtube_menu().addVideoItem(name, videoid, iconimage, fanart)
                elif not channelid == 'false':  # Means this is a channel id entry
                    youtube_menu.youtube_menu().addChannelItem(name, channelid, iconimage, fanart)
                elif not playlistid == 'false':  # Means this is a playlist id entry
                    youtube_menu.youtube_menu().addPlaylistItem(name, playlistid, iconimage, fanart)
                elif not section == 'false':  # Means this is a section placeholder/info line
                    youtube_menu.youtube_menu().addSectionItem(name, self.default_icon, self.default_fanart)
            self.endDirectory()
        except Exception:
            pass

    def get(self, action, subid):
        try:
            self.init_vars(action)
            thisMenuFile = self.submenu % (subid)
            menuItems = youtube_menu.youtube_menu().processMenuFile(thisMenuFile)
            for name, section, searchid, subid, playlistid, channelid, videoid, iconimage, fanart, description in menuItems:
                if not subid == 'false':  # Means this item points to a submenu
                    youtube_menu.youtube_menu().addMenuItem(name, self.action, subid, iconimage, fanart, description, True)
                elif not searchid == 'false':  # Means this is a search term
                    youtube_menu.youtube_menu().addSearchItem(name, searchid, iconimage, fanart)
                elif not videoid == 'false':  # Means this is a video id entry
                    youtube_menu.youtube_menu().addVideoItem(name, videoid, iconimage, fanart)
                elif not channelid == 'false':  # Means this is a channel id entry
                    youtube_menu.youtube_menu().addChannelItem(name, channelid, iconimage, fanart)
                elif not playlistid == 'false':  # Means this is a playlist id entry
                    youtube_menu.youtube_menu().addPlaylistItem(name, playlistid, iconimage, fanart)
                elif not section == 'false':  # Means this is a section placeholder/info line
                    youtube_menu.youtube_menu().addSectionItem(name, self.default_icon, self.default_fanart)
            self.endDirectory()
        except Exception:
            pass

    def endDirectory(self, contentType='addons', sortMethod=control.xDirSort.NoSort, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
        if sortMethod is not control.xDirSort.NoSort:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=True)
