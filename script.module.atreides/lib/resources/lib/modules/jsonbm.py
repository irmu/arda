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

import json
import os
import sys
import traceback

import xbmc
import xbmcplugin

from resources.lib.modules import control, log_utils

HOME = xbmc.translatePath('special://home/')
FILENAME = os.path.join(HOME, 'userdata/addon_data/plugin.video.atreides/bookmarks.json')

defaults = {'Channels': {},
            'Documentaries': {},
            'Radio': {}
            }


class jsonBookmarks(object):
    def __init__(self):
        if not os.path.exists(FILENAME):
            f = open(FILENAME, 'w')
            temp = json.dumps(defaults)
            f.write(temp)
            f.close()
            self.bookmarks = json.loads(temp)
        else:
            with open(FILENAME) as json_file:
                self.bookmarks = json.load(json_file)

    def add_channel(self, dbase):
        temp = dbase.decode('base64').split('|')
        name = temp[0]
        chan_id = temp[1]
        action = temp[2]
        icon = temp[3]
        url = temp[4]
        try:
            if action in self.bookmarks['Channels']:
                if chan_id not in self.bookmarks['Channels'][action]:
                    self.bookmarks['Channels'][action][chan_id] = {'name': name, 'id': chan_id, 'action': action, 'icon': icon, 'url': url}
                    self.save()
                    control.refresh()
            else:
                self.bookmarks['Channels'][action] = {}
                self.bookmarks['Channels'][action][chan_id] = {}
                self.bookmarks['Channels'][action][chan_id] = {'name': name, 'id': chan_id, 'action': action, 'icon': icon, 'url': url}
                self.save()
                control.refresh()
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Bookmarks - Add Channel Exception: \n' + str(failure))

    def rem_channel(self, dbase):
        temp = dbase.decode('base64').split('|')
        chan_id = temp[1]
        action = temp[2]
        try:
            del self.bookmarks['Channels'][action][chan_id]
            self.save()
            control.refresh()
        except Exception:
            from resources.lib.dialogs import ok
            ok.load('Bookmarks Error', '[B]Error removing channel.[/B]')
            failure = traceback.format_exc()
            log_utils.log('Remove Channel Bookmark - Exception: \n' + str(failure))
            return

    def show_channels(self):
        items = []
        for action in self.bookmarks['Channels'].keys():
            for entry in self.bookmarks['Channels'][action].keys():
                try:
                    channel = self.bookmarks['Channels'][action][entry]
                    item = control.item(label=channel['name'])
                    item.setProperty("IsPlayable", "true")
                    item.setArt({"thumb": channel['icon'], "icon": channel['icon']})
                    item.setInfo(type="video", infoLabels={"Title": channel['name'], "mediatype": "video"})
                    url = '%s?action=%s&url=%s' % (sys.argv[0], channel['action'], channel['url'])

                    cm = self.build_cm('Channels', name=channel['name'], id=channel['id'], action=channel['action'], icon=channel['icon'], url=channel['url'])
                    item.addContextMenuItems(cm)

                    try:
                        item.setContentLookup(False)
                    except AttributeError:
                        pass
                    items.append((url, item, False))
                except Exception:
                    from resources.lib.dialogs import ok
                    ok.load('Bookmarks Error', '[B]Error loading bookmarks.[/B]')
                    failure = traceback.format_exc()
                    log_utils.log('Show Channel Bookmarks - Exception: \n' + str(failure))
                    return
        control.addItems(int(sys.argv[1]), items)
        self.endDirectory('files', xbmcplugin.SORT_METHOD_LABEL)

    def add_radio(self, dbase):
        temp = dbase.decode('base64').split('|')
        name = temp[0]
        station_id = temp[1]
        action = temp[2]
        icon = temp[3]
        url = temp[4]
        try:
            if action in self.bookmarks['Radio']:
                if station_id not in self.bookmarks['Radio'][action]:
                    self.bookmarks['Radio'][action][station_id] = {'name': name, 'id': station_id, 'action': action, 'icon': icon, 'url': url}
                    self.save()
                    control.refresh()
            else:
                self.bookmarks['Radio'][action] = {}
                self.bookmarks['Radio'][action][station_id] = {}
                self.bookmarks['Radio'][action][station_id] = {'name': name, 'id': station_id, 'action': action, 'icon': icon, 'url': url}
                self.save()
                control.refresh()
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Bookmarks - Add Radio Exception: \n' + str(failure))

    def rem_radio(self, dbase):
        temp = dbase.decode('base64').split('|')
        station_id = temp[1]
        action = temp[2]
        try:
            del self.bookmarks['Radio'][action][station_id]
            self.save()
            control.refresh()
        except Exception:
            from resources.lib.dialogs import ok
            ok.load('Bookmarks Error', '[B]Error removing radio station.[/B]')
            failure = traceback.format_exc()
            log_utils.log('Remove Radio Bookmark - Exception: \n' + str(failure))
            return

    def show_radio(self):
        items = []
        for action in self.bookmarks['Radio'].keys():
            for entry in self.bookmarks['Radio'][action].keys():
                try:
                    station = self.bookmarks['Radio'][action][entry]
                    item = control.item(label=station['name'])
                    item.setProperty("IsPlayable", "true")
                    item.setArt({"thumb": station['icon'], "icon": station['icon']})
                    url = '%s?action=%s&url=%s' % (sys.argv[0], station['action'], station['url'])

                    cm = self.build_cm('Radio', name=station['name'], id=station['id'], action=station['action'], icon=station['icon'], url=station['url'])
                    item.addContextMenuItems(cm)

                    try:
                        item.setContentLookup(False)
                    except AttributeError:
                        pass
                    items.append((url, item, False))
                except Exception:
                    from resources.lib.dialogs import ok
                    ok.load('Bookmarks Error', '[B]Error loading bookmarks.[/B]')
                    failure = traceback.format_exc()
                    log_utils.log('Show Radio Bookmarks - Exception: \n' + str(failure))
                    return
        control.addItems(int(sys.argv[1]), items)
        self.endDirectory('files', xbmcplugin.SORT_METHOD_LABEL)

    def save(self):
        with open(FILENAME, 'w') as json_file:
            json.dump(self.bookmarks, json_file, sort_keys=True, indent=4)
            json_file.close()

    def build_cm(self, bmtype, **kwargs):
        try:
            cm = []
            name = kwargs.get('name')
            action = kwargs.get('action')
            icon = kwargs.get('icon')
            url = kwargs.get('url')
            if bmtype == 'Channels':
                chan_id = kwargs.get('id')
                dbase = name + '|' + chan_id + '|' + action + '|' + icon + '|' + url
                if action in self.bookmarks[bmtype]:
                    if chan_id in self.bookmarks[bmtype][action]:
                        cm.append(('Remove Bookmark', 'RunPlugin(%s?action=%s&url=%s)' % (sys.argv[0], 'remove_channel', dbase.encode('base64'))))
                    else:
                        cm.append(('Add Bookmark', 'RunPlugin(%s?action=%s&url=%s)' % (sys.argv[0], 'add_channel', dbase.encode('base64'))))
                else:
                    cm.append(('Add Bookmark', 'RunPlugin(%s?action=%s&url=%s)' % (sys.argv[0], 'add_channel', dbase.encode('base64'))))
            elif bmtype == 'Radio':
                station_id = kwargs.get('id')
                dbase = name + '|' + station_id + '|' + action + '|' + icon + '|' + url
                if action in self.bookmarks[bmtype]:
                    if station_id in self.bookmarks[bmtype][action]:
                        cm.append(('Remove Bookmark', 'RunPlugin(%s?action=%s&url=%s)' % (sys.argv[0], 'remove_radio', dbase.encode('base64'))))
                    else:
                        cm.append(('Add Bookmark', 'RunPlugin(%s?action=%s&url=%s)' % (sys.argv[0], 'add_radio', dbase.encode('base64'))))
                else:
                    cm.append(('Add Bookmark', 'RunPlugin(%s?action=%s&url=%s)' % (sys.argv[0], 'add_radio', dbase.encode('base64'))))
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Bookmarks - Context Exception: \n' + str(failure))

        return cm

    def endDirectory(self, contentType='addons', sortMethod=control.xDirSort.NoSort):
        control.content(int(sys.argv[1]), contentType)
        control.sortMethod(int(sys.argv[1]), sortMethod)
        control.directory(int(sys.argv[1]), cacheToDisc=True)