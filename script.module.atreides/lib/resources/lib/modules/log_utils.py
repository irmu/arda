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

import cProfile
import json
import os
import pstats
import re
import requests
import StringIO
import time
from datetime import datetime

import pyqrcode
import xbmc
import xbmcvfs
import xbmcgui

from resources.lib.dialogs import themecontrol
from resources.lib.modules import control
from xbmc import (LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO,  # @UnusedImport
                  LOGNONE, LOGNOTICE, LOGSEVERE, LOGWARNING)

name = control.addonInfo('name')
aid = control.addonInfo('id')
version = control.addonInfo('version')
# Using color coding, for color formatted log viewers like Assassin's Tools
DEBUGPREFIX = '[COLOR red][ ATREIDES DEBUG ][/COLOR]'
LOG_PATH = xbmc.translatePath('special://logpath/')
HOME_PATH = xbmc.translatePath('special://home/')
PROFILE = control.profile

def log(msg, level=LOGNOTICE):
    debug_enabled = control.setting('addon_debug')
    debug_log = control.setting('debug.location')

    print DEBUGPREFIX + ' Debug Enabled?: ' + str(debug_enabled)
    print DEBUGPREFIX + ' Debug Log?: ' + str(debug_log)

    if not control.setting('addon_debug') == 'true':
        return

    try:
        if isinstance(msg, unicode):
            msg = '%s (ENCODED)' % (msg.encode('utf-8'))

        if not control.setting('debug.location') == '0':
            log_file = os.path.join(LOG_PATH, 'atreides.log')
            if not os.path.exists(log_file):
                f = open(log_file, 'w')
                f.close()
            with open(log_file, 'a') as f:
                line = '[%s %s] %s: %s' % (datetime.now().date(), str(datetime.now().time())[:8], DEBUGPREFIX, msg)
                f.write(line.rstrip('\r\n')+'\n')
        else:
            print('%s: %s' % (DEBUGPREFIX, msg))
    except Exception as e:
        try:
            xbmc.log('Logging Failure: %s' % (e), level)
        except Exception:
            pass


def cleanLog(content):
    replaces = (('//.+?:.+?@', '//USER:PASSWORD@'),('<user>.+?</user>', '<user>USER</user>'),('<pass>.+?</pass>', '<pass>PASSWORD</pass>'),)
    for pattern, repl in replaces:
        content = re.sub(pattern, repl, content)
        return content


def readLog(path):
    try:
        lf = xbmcvfs.File(path)
        sz = lf.size()
        if sz > 1000000:
            log('file is too large')
            return 'File is too large'
        content = lf.read()
        lf.close()
        if content:
            return content
        else:
            log('file is empty')
            return 'File is Empty'
    except:
        log('unable to read file')
        return 'Unable to read file'


def highlightText(msg):
    msg = cleanLog(msg)
    msg = msg.replace('\n', '[NL]')
    matches = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(msg)
    for item in matches:
        string = '-->Python callback/script returned the following error<--%s-->End of Python script error report<--' % item
        msg    = msg.replace(string, '[COLOR red]%s[/COLOR]' % string)
    msg = msg.replace('WARNING', '[COLOR yellow]WARNING[/COLOR]').replace('ERROR', '[COLOR red]ERROR[/COLOR]').replace('[NL]', '\n').replace(': EXCEPTION Thrown (PythonToCppException) :', '[COLOR red]: EXCEPTION Thrown (PythonToCppException) :[/COLOR]')
    msg = msg.replace('\\\\', '\\').replace(HOME_PATH, '')
    return msg


def uploadLog(data):
    url = 'https://paste.kodi.tv/'

    session = requests.Session()
    UserAgent = '%s: %s' % (aid, version)
    try:
        response = session.post(url + 'documents', data=data, headers={'User-Agent': UserAgent})
        if 'key' in response.json():
            result = url + response.json()['key']
            return True, result
        elif 'message' in response.json():
            log('upload failed, paste may be too large')
            return False, response.json()['message']
        else:
            log('error: %s' % response.text)
            return False, 'Error posting the logfile.'
    except:
        log('unable to retrieve the paste url')
        return False, 'Failed to retrieve the paste url'


def showResult(message, url=None):
    if url:
        imagefile = os.path.join(xbmc.translatePath(PROFILE),'%s.png' % str(url.split('/')[-1]))
        qrIMG = pyqrcode.create(url)
        qrIMG.png(imagefile, scale=10)
        qr = QRCode("LogViewer_QR.xml", themecontrol.skinModule(), themecontrol.skinTheme(), '1080i', image=imagefile, text=message)
        qr.doModal()
        del qr
        xbmcvfs.delete(imagefile)
    else:
        from resources.lib.dialogs import ok
        ok.OK_Dialog('Upload Complete', message)


class QRCode(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.colors = themecontrol.ThemeColors()

        self.image = kwargs["image"]
        self.text = kwargs["text"]

    def onInit(self):
        self.imagecontrol = 501
        self.textbox = 502
        self.okbutton = 503
        self.showdialog()

    def showdialog(self):
        self.setProperty('dhtext', self.colors.dh_color)

        self.getControl(self.imagecontrol).setImage(self.image)
        self.getControl(self.textbox).setText(self.text)
        self.setFocus(self.getControl(self.okbutton))

    def onClick(self, controlId):
        if (controlId == self.okbutton):
            self.close()


class Profiler(object):
    def __init__(self, file_path, sort_by='time', builtins=False):
        self._profiler = cProfile.Profile(builtins=builtins)
        self.file_path = file_path
        self.sort_by = sort_by

    def profile(self, f):
        def method_profile_on(*args, **kwargs):
            try:
                self._profiler.enable()
                result = self._profiler.runcall(f, *args, **kwargs)
                self._profiler.disable()
                return result
            except Exception as e:
                log('Profiler Error: %s' % (e), LOGWARNING)
                return f(*args, **kwargs)

        def method_profile_off(*args, **kwargs):
            return f(*args, **kwargs)

        if _is_debugging():
            return method_profile_on
        else:
            return method_profile_off

    def __del__(self):
        self.dump_stats()

    def dump_stats(self):
        if self._profiler is not None:
            s = StringIO.StringIO()
            params = (self.sort_by,) if isinstance(self.sort_by, basestring) else self.sort_by
            ps = pstats.Stats(self._profiler, stream=s).sort_stats(*params)
            ps.print_stats()
            if self.file_path is not None:
                with open(self.file_path, 'w') as f:
                    f.write(s.getvalue())


def trace(method):
    def method_trace_on(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        log('{name!r} time: {time:2.4f}s args: |{args!r}| kwargs: |{kwargs!r}|'.format(
            name=method.__name__, time=end - start, args=args, kwargs=kwargs), LOGDEBUG)
        return result

    def method_trace_off(*args, **kwargs):
        return method(*args, **kwargs)

    if _is_debugging():
        return method_trace_on
    else:
        return method_trace_off


def _is_debugging():
    command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Settings.getSettings',
               'params': {'filter': {'section': 'system', 'category': 'logging'}}}
    js_data = execute_jsonrpc(command)
    for item in js_data.get('result', {}).get('settings', {}):
        if item['id'] == 'debug.showloginfo':
            return item['value']

    return False


def execute_jsonrpc(command):
    if not isinstance(command, basestring):
        command = json.dumps(command)
    response = control.jsonrpc(command)
    return json.loads(response)
