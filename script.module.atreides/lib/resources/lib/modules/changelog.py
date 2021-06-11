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

import urllib2
import base64
import os

import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs

addon_id = xbmcaddon.Addon().getAddonInfo('id')


def get():
    newsfile = base64.b64decode(b'aHR0cDovL2F0cmVpZGVzLmhlbGlvaG9zdC5vcmcvcGx1Z2luLnZpZGVvLmF0cmVpZGVzL3doYXRzbmV3LnR4dA')
    changelog = base64.b64decode(b'aHR0cDovL2F0cmVpZGVzLmhlbGlvaG9zdC5vcmcvcGx1Z2luLnZpZGVvLmF0cmVpZGVzL2NoYW5nZWxvZy50eHQ')
    try:
        if 'file' in changelog:
            temp = xbmc.translatePath(('special://home/addons/%s' % (addon_id)))
            changelog = os.path.join(temp, changelog.replace('file://', '')).decode('utf-8')
        message = open_atreides_url(newsfile)
        changelog_file = open_atreides_url(changelog)

        if message is None or changelog_file is None:
            return

        message = message.replace('$version$', str(xbmcaddon.Addon().getAddonInfo('version')))
        if '$changelog$' in message:
            message = message.replace('$changelog$', changelog_file)
        xbmcgui.Dialog().textviewer('[B][COLOR springgreen]Latest Updates and Information[/COLOR][/B]', message)
    except Exception:
        return


def open_atreides_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'klopp')
    try:
        response = urllib2.urlopen(req)
        text = response.read()
        response.close()
        return text
    except Exception:
        return None


# FIXME: Left in as placeholder, as may define custom skinned message window down the road
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            quit()
            return
        except Exception:
            pass
