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
import time
import sys
import traceback
import urllib
import urlparse

from resources.lib.modules import client, control, log_utils, source_utils

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()


class jsonMenu(object):
    def __init__(self):
        # Default root locations, if none is set by the indexer
        self.menu_file = None
        self.local_root = os.path.join(control.addonPath, 'menu')
        self.remote_root = 'SaHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3RoZXJlYWxhdHJlaWRlcy9ob3VzZWF0cmVpZGVzL21hc3Rlci9wbHVnaW4udmlkZW8uYXRyZWlkZXMvbWVudS8='[1:].decode('base64')
        self.menu = None

        self.precheck = control.setting('menu.links.resolve')
        self.debugcheck = control.setting('menu_links')

        self.agent = 'hQXRyZWlkZXMgSlNPTiBNZW51'[1:].decode('base64')

    def load(self, menu_file, refresh=False):
        menu_file = menu_file + '.json'
        try:
            self.menu_file = os.path.join(self.local_root, menu_file)
            fileref = control.openFile(self.menu_file)
            content = fileref.read()
            fileref.close()
            self.menu = json.loads(content)
            '''
            Now lets handle the versioning side of things
            '''
            try:
                lastCheck = self.menu["menu_file"]["checked"]
            except Exception:
                lastCheck = '1'
            lastCheck = int(float(lastCheck))
            if time.time() < lastCheck:
                return

            '''
            Time check done, so let's check online for a newer version
            '''
            try:
                version = self.menu["menu_file"][0]["version"]
            except Exception:
                version = '0'
            version = int(float(version))

            try:
                header = {'User-Agent': self.agent}
                url = urlparse.urljoin(self.remote_root, menu_file)
                response = client.request(url, headers=header)
                remote_menu = json.loads(response)

                try:
                    remote_version = remote_menu["menu_file"][0]["version"]
                except Exception:
                    remote_version = '0'
                remote_version = int(float(remote_version))
                if remote_version > version:
                    self.menu = remote_menu
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('jsonMenu - Open Remote Exception: \n' + str(failure))

            lastCheck = time.time() + (60 * 60 * 24)
            self.menu["menu_file"][0]["checked"] = str(lastCheck)
            self.save()
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('jsonMenu - Open Local Exception: \n' + str(failure))

    def save(self):
        with open(self.menu_file, 'w') as json_file:
            json.dump(self.menu, json_file, indent=4)
            json_file.close()

    def process(self, menu_section):
        for item in self.menu[menu_section]:
            isFolder = True
            try:
                '''
                First things first, let's see if this is an entry with on/off settings and if we should display it.
                '''
                try:
                    toggle = item.get('toggle', None)
                    if toggle is not None:
                        is_enabled = control.setting(toggle).strip()
                        if (is_enabled == '' or is_enabled == 'false'):
                            continue
                except Exception:
                    pass

                '''
                Language file support can be done this way
                '''
                title = item.get('title', 'No Title Given')
                try:
                    title = control.lang(int(title)).encode('utf-8')
                except Exception:
                    pass

                link = item.get('action', None)
                if link is None:
                    '''
                    This is something without an action like direct link or nolink.
                    '''
                    link = item.get('link', None)
                    if link is None:
                        link = item.get('plugin', None)
                    else:
                        isFolder = False
                try:
                    url = item.get('url', None)
                    link = '%s&url=%s' % (link, url) if url is not None else link
                except Exception:
                    pass
                try:
                    listid = item.get('list_id', None)
                    listtype = item.get('list_type', None)
                    link = '%s&listid=%s&listtype=%s' % (link, listid, listtype) if listid is not None else link
                except Exception:
                    pass
                try:
                    menu_file = item.get('menu_file', None)
                    menu_section = item.get('menu_section', None)
                    link = '%s&menu_file=%s&menu_section=%s&menu_title=%s' % (link, menu_file, menu_section, title) if menu_file is not None else link
                    if menu_file is not None:
                        isFolder = True
                except Exception:
                    pass

                try:
                    menu_sort = item.get('menu_sort', None)
                    link = '%s&menu_sort=%s' % (link, menu_sort) if menu_sort is not None else link
                except Exception:
                    pass

                try:
                    query = item.get('query', None)
                    link = '%s&query=%s' % (link, query) if query is not None else link
                except Exception:
                    pass

                if item.get('nolink', None) is not None:
                    link = "sectionItem"
                    isAction = False
                    isFolder = False
                else:
                    isAction = True

                self.addDirectoryItem(title, link, item['thumbnail'], item['thumbnail'], isAction=isAction, isFolder=isFolder)
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('Process Menu - Failed to Build: \n' + str(failure))

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        isPlayable = False
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        if query.startswith('http'):
            '''
            This is a direct play link. Need to add support for it.
            '''
            if ((self.precheck == '' or self.precheck == 'false') and (self.debugcheck == '' or self.debugcheck == 'false')):
                url = '%s?action=playSimple&title=%s&url=%s' % (sysaddon, urllib.quote_plus(name), urllib.quote_plus(query))
            else:
                source = source_utils.uResolve(query)
                if source is None and self.precheck == 'true':
                    return
                url = '%s?action=playSimple&title=%s&url=%s&resolved=true' % (sysaddon,  urllib.quote_plus(name), urllib.quote_plus(source))
            isPlayable = True
        elif query.startswith('plugin'):
            url = query
        else:
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
        if isPlayable:
            item.setInfo(type="video", infoLabels={"Title": name})
            item.setProperty("IsPlayable", "true")
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
