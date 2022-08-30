# -*- coding: utf-8 -*-

import sys
import os
import re
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import json
import xbmcvfs
import time
from datetime import datetime, timedelta
from calendar import timegm as TGM
import requests
PY2 = sys.version_info[0] == 2
if PY2:
	from urllib import urlencode, quote, unquote, unquote_plus  # Python 2.X
	from urllib2 import urlopen  # Python 2.X
	TRANS_PATH, LOG_MESSAGE, INPUT_APP = xbmc.translatePath, xbmc.LOGNOTICE, 'inputstreamaddon' # Stand: 05.12.20 / Python 2.X
else:
	from urllib.parse import urlencode, quote, unquote, unquote_plus  # Python 3.X
	from urllib.request import urlopen  # Python 3.X
	TRANS_PATH, LOG_MESSAGE, INPUT_APP = xbmcvfs.translatePath, xbmc.LOGINFO, 'inputstream' # Stand: 05.12.20  / Python 3.X
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from .provider import Client


global debuging
HOST_AND_PATH                 = sys.argv[0]
ADDON_HANDLE                  = int(sys.argv[1])
dialog                                      = xbmcgui.Dialog()
addon                                     = xbmcaddon.Addon()
addon_id                                = addon.getAddonInfo('id')
addon_name                         = addon.getAddonInfo('name')
addon_version                      = addon.getAddonInfo('version')
addonPath                             = TRANS_PATH(addon.getAddonInfo('path')).encode('utf-8').decode('utf-8')
dataPath                                = TRANS_PATH(addon.getAddonInfo('profile')).encode('utf-8').decode('utf-8')
searchHackFile                     = os.path.join(dataPath, 'searchString')
defaultFanart                        = (os.path.join(addonPath, 'fanart.jpg') if PY2 else os.path.join(addonPath, 'resources', 'media', 'fanart.jpg'))
icon                                         = (os.path.join(addonPath, 'icon.png') if PY2 else os.path.join(addonPath, 'resources', 'media', 'icon.png'))
artpic                                      = os.path.join(addonPath, 'resources', 'media', '').encode('utf-8').decode('utf-8')
evepic                                     = os.path.join(addonPath, 'resources', 'media', 'events', '').encode('utf-8').decode('utf-8')
thepic                                     = os.path.join(addonPath, 'resources', 'media', 'themes', '').encode('utf-8').decode('utf-8')
COUNTRY                               = {0: 'de', 1: 'fr'}[int(addon.getSetting('language'))]
enableINPUTSTREAM          = addon.getSetting('useInputstream') == 'true'
prefSTREAM                           = addon.getSetting('prefer_stream')
LIMIT_NUMBER                    = int(addon.getSetting('entry_limitation'))
useThumbAsFanart              = addon.getSetting('useThumbAsFanart') == 'true'
enableADJUSTMENT            = addon.getSetting('show_settings') == 'true'
DEB_LEVEL                            = (LOG_MESSAGE if addon.getSetting('enableDebug') == 'true' else xbmc.LOGDEBUG)
BASE_URL                              = "https://www.arte.tv/"
API_URL                                 = "https://api-cdn.arte.tv/api/emac/v3/"+COUNTRY+"/web/"
OPA_token                             = "AOwImM4EGZ2gjYjRGZzEzYxMTNxMWOjJDO4gDO3UWN3UmN5IjNzAzMlRmMwEWM2I2NhFWN1kjYkJjZ1cjY1czN reraeB"
EMAC_token                          = "wYxYGNiBjNwQjZzIjMhRDOllDMwEjM2MDN3MjY4U2M1ATYkVWOkZTM5QzM4YzN2ITM0E2MxgDO1EjN5kjZmZWM reraeB"
PLAY_token                           = "QMjZTOkF2NwQDZlFTOmJDOiFGN1QGM4EjY5QWOhBzN4YzM4YGMiRTNjZjZyImMjFWZlRWZ3Q2Y1MmYyYDZyYzM reraeB"
traversing                              = Client(Client.CONFIG_ARTE)

xbmcplugin.setContent(ADDON_HANDLE, 'movies')

def py2_enc(s, nom='utf-8', ign='ignore'):
	if PY2:
		if not isinstance(s, basestring):
			s = str(s)
		s = s.encode(nom, ign) if isinstance(s, unicode) else s
	return s

def py2_uni(s, nom='utf-8', ign='ignore'):
	if PY2 and isinstance(s, str):
		s = unicode(s, nom, ign)
	return s

def py3_dec(d, nom='utf-8', ign='ignore'):
	if not PY2 and isinstance(d, bytes):
		d = d.decode(nom, ign)
	return d

def translation(id):
	return py2_enc(addon.getLocalizedString(id))

def failing(content):
	log(content, xbmc.LOGERROR)

def debug_MS(content):
	log(content, DEB_LEVEL)

def log(msg, level=LOG_MESSAGE): # kompatibel mit Python-2 und Python-3
	msg = py2_enc(msg)
	return xbmc.log('[{0} v.{1}]{2}'.format(addon_id, addon_version, msg), level)

def get_userAgent():
	base = 'Mozilla/5.0 {0} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
	if xbmc.getCondVisibility('System.Platform.Android'):
		if 'arm' in os.uname()[4]: return base.format('(X11; CrOS armv7l 7647.78.0)') # ARM based Linux
		return base.format('(X11; Linux x86_64)') # x86 Linux
	elif xbmc.getCondVisibility('System.Platform.Windows'):
		return base.format('(Windows NT 10.0; WOW64)') # Windows
	elif xbmc.getCondVisibility('System.Platform.IOS'):
		return base.format('(iPhone; CPU iPhone OS 10_3 like Mac OS X)') # iOS iPhone/iPad
	elif xbmc.getCondVisibility('System.Platform.Darwin'):
		return base.format('(Macintosh; Intel Mac OS X 10_10_1)') # Mac OSX
	return base.format('(X11; Linux x86_64)') # x86 Linux

def _header(REFERRER=None, USERTOKEN=None):
	header = {}
	header['Connection'] = 'keep-alive'
	header['Cache-Control'] = 'no-cache'
	header['User-Agent'] = get_userAgent()
	header['DNT'] = '1'
	header['Upgrade-Insecure-Requests'] = '1'
	header['Accept-Encoding'] = 'gzip'
	header['Accept-Language'] = 'en-US,en;q=0.8,de;q=0.7'
	if REFERRER:
		header['Referer'] = REFERRER
	if USERTOKEN:
		header['Authorization'] = USERTOKEN[::-1]
	return header

def getUrl(url, method='GET', REF=None, AUTH=None, headers=None, cookies=None, allow_redirects=False, verify=True, stream=None, data=None, json=None):
	simple = requests.Session()
	debug_MS("(common.getUrl) === URL that wanted : {0} ===".format(url))
	ANSWER = None
	simple.headers.update(_header(REF, AUTH))
	try:
		if method in ['GET', 'LOAD']:
			response = simple.get(url, headers=headers, allow_redirects=allow_redirects, verify=verify, stream=stream, timeout=30)
		elif method == 'POST':
			response = simple.post(url, headers=headers, allow_redirects=allow_redirects, verify=verify, data=data, json=json, timeout=30)
		ANSWER = response.json() if method in ['GET', 'POST'] else py2_enc(response.text)
		debug_MS("(common.getUrl) === send url-HEADERS : {0} ===".format(str(simple.headers)))
	except requests.exceptions.RequestException as e:
		failing("(common.getUrl) ERROR - ERROR - ERROR : ##### url: {0} === error: {1} #####".format(url, str(e)))
		dialog.notification(translation(30521).format('URL'), translation(30523).format(str(e)), icon, 10000)
		return sys.exit(0)
	return ANSWER

def ADDON_operate(IDD):
	js_query = xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "id":1, "method":"Addons.GetAddonDetails", "params":{{"addonid":"{}", "properties":["enabled"]}}}}'.format(IDD))
	if '"enabled":false' in js_query:
		try:
			xbmc.executeJSONRPC('{{"jsonrpc":"2.0", "id":1, "method":"Addons.SetAddonEnabled", "params":{{"addonid":"{}", "enabled":true}}}}'.format(IDD))
			failing("(common.ADDON_operate) ERROR - ERROR - ERROR :\n##### Das benötigte Addon : *{0}* ist NICHT aktiviert !!! #####\n##### Es wird jetzt versucht die Aktivierung durchzuführen !!! #####".format(IDD))
		except: pass
	if '"error":' in js_query:
		dialog.ok(addon_id, translation(30501).format(IDD))
		failing("(common.ADDON_operate) ERROR - ERROR - ERROR :\n##### Das benötigte Addon : *{0}* ist NICHT installiert !!! #####".format(IDD))
		return False
	if '"enabled":true' in js_query:
		return True

def get_Local_DT(info):
	fixed_format = '%Y{0}%m{0}%dT%H{1}%M{1}%S'.format('-', ':') # 2019-06-13T13:30:00Z
	utcDT = datetime(*(time.strptime(info, fixed_format)[0:6]))
	try:
		localDT = datetime.fromtimestamp(TGM(utcDT.timetuple()))
		assert utcDT.resolution >= timedelta(microseconds=1)
		localDT = localDT.replace(microsecond=utcDT.microsecond)
	except (ValueError, OverflowError): # ERROR on Android 32bit Systems = cannot convert unix timestamp over year 2038
		localDT = datetime.fromtimestamp(0) + timedelta(seconds=TGM(utcDT.timetuple()))
		localDT = localDT - timedelta(hours=datetime.timetuple(localDT).tm_isdst)
	return localDT

def get_Description(info):
	if 'fullDescription' in info and info['fullDescription'] and len(info['fullDescription']) > 10:
		return cleaning(info['fullDescription'])
	elif 'description' in info and info['description'] and len(info['description']) > 10:
		return cleaning(info['description'])
	elif 'shortDescription' in info and info['shortDescription'] and len(info['shortDescription']) > 10:
		return cleaning(info['shortDescription'])
	return ""

def get_Picture(elem_id, resources, elem_type):
	if elem_type in resources and resources[elem_type] is not None and 'blurUrl' in resources[elem_type] and resources[elem_type]['blurUrl']:
		return resources[elem_type]['resolutions'][-1]['url']
	return None

def getSorting():
	method = [xbmcplugin.SORT_METHOD_UNSORTED, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE, xbmcplugin.SORT_METHOD_DATE, xbmcplugin.SORT_METHOD_DURATION]
	return method

def cleaning(text):
	if text is not None:
		text = py2_enc(text).strip()
	return text

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split('&')
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

params = parameters_string_to_dict(sys.argv[2])
name = unquote_plus(params.get('name', ''))
url = unquote_plus(params.get('url', ''))
mode = unquote_plus(params.get('mode', 'root'))
image = unquote_plus(params.get('image', ''))
page = unquote_plus(params.get('page', '1'))
phrase = unquote_plus(params.get('phrase', 'standard'))
extras = unquote_plus(params.get('extras', 'standard'))
