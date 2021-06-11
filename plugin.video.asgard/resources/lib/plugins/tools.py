# -*- coding: utf-8 -*-
"""
    tools.py --- Jen Plugin for accessing various tools
    Copyright (C) 2018: MuadDib, Jen
    Version 2.1.2

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------


    Overview:
        Drop this PY in the plugins folder, and use whatever tools below you want.

    Changelog:
        2020-04-19
			- Updated the PAIR_LIST
				- removed Openload, Streamango & Streamcherry
				- added UptoBox (requires a VPN to pair from USA!)
        2019-07-29
            - Updated base64 decoding to work with padded strings
            - Added a multi-step protection process for accessing an Adult menu (see XML Explanations below)
                - added <adultpass></adultpass> tags
                - added requirement to enable "Enable Adult Menus" option in addon settings before menu is visible
                - requires password to access menu after it becomes visible
                - works with both Local and Remote XML locations
                
        2019-07-25
            - Added option to authorize ResolveURL with Premiumize.me debrid service (see Usage Examples below)
            - Added option to authorize ResolveURL with LinkSnappy debrid service (see Usage Examples below)
            - Added option to clear Resolver Function Cache for ResolveURL and/or URLResolver (see Usage Examples below)
            - Categorized and added Usage Examples
            
        2018.11.17
            - Updated the PAIR_LIST (replaced the_video_me with vevio; replaced vid_up_me with vidup, replaced vshare with videoshare)
                - updated URL for openload and vidup
            - Added AUTH_LIST to authorize ResolveURL with RealDebrid or AllDebrid
                - added <authwith> tags
                - can use "authlist" to display both debrid services, or specific entry from AUTH_LIST to authorize only that service
            - Added customizable settings for 2 COLORS for the Header & list of Items displayed in the Pair/Authorize/Function Cache windows

        2018.7.14
            - Updated password code to cache a session for X amt of time
            - Adjust the timer via the SESSION_HOURS in settings.xml (or in code)

        2018.6.23
            - Updated link for pairing The Video Me

        2018.6.14
            - Fix for pairing on Mac OSX

        2018.6.8
            - Added Streamango and Streamcherry pairing sites
            - Added <passreq> tag to password protect submenus

        2018.5.25
            - Added <pairwith> tags
                - Can use pairlist to show all sites, or specific entry from PAIR_LIST to load that site from menu
            - Added <trailer> tag support to load your custom YT trailer (via plugin url) for non-imdb items

        2018.5.1a
            - Added <mode> and <modeurl> tags (used together in same item)

        2018.5.1
            - Initial Release

    XML Explanations:
        Tags:
            <heading></heading> - Displays the entry as normal, but performs no action (not a directory or "item")
            <mysettings>0/0</mysettings> - Opens settings dialog to the specified Tab and section (0 indexed)
            <pairwith></pairwith> - Used for pairing with supported sites (flashx, uptobox, vevio, vidup, videoshare)
            <authwith></authwith> - Used for authorizing Debrid services (realdebrid, alldebrid, premiumize, linksnappy)
            <funccache></funccache> - Used for clearing resolver function cache (resolveurl, urlresolver)
            <passreq></passreq> - Used to password protect submenus. Format is base64 encoded string formatted like this:  Password|link_to_xml
            <trailer>plugin://plugin.video.youtube/play/?video_id=ChA0qNHV1D4</trailer> - Adds Trailer option for this movie in the context menu when Metadata is DISABLED in your addon
            <adultpass></adultpass> - Used to password protect an Adult menu similar to <passreq> above.  Format is:  Password|link_to_xml  (all base64 encoded)
                                    - If the Adult menu contains the word "adult" in ANY part of its name (lowercase, uppercase or both), the menu will NOT be displayed unless the "Enable Adult Menus" option is enabled in addon settings (requires latest settings.xml & xml.py files).
                                    - If the Adult menu does NOT contain the word "adult" in ANY part of its name, you will get a "This menu is not enabled!" message when trying to access it.
                                    - In either case, once the "Enable Adult Menus" option is enabled in addon settings, you will be required to enter a password in order to access the menu.


    *** COLORS ***
        Set your desired colors for the COLOR1 & COLOR2 variables within "" on lines 238 & 239 below.
        COLOR1 is for all Headers & COLOR2 is for the Items list, displayed in the Pair/Authorize/Function Cache window.
        The color values must be lowercase alphanumeric (example: red, limegreen) or anycase of Hex (example: ffff0000, FF00FF00).
        If the color variables are left blank, they will display as the default color set within the skin you're using.

    -------------------------------------------------------------

    Usage Examples:

	### Headings ###

        * Displays the entry as normal, but performs no action (not a directory or "item")
        <item>
            <title>[COLOR dodgerblue]Don't forget to folow me on twitter @tantrumdev ![/COLOR]</title>
            <heading></heading>
        </item>

	### Settings ###

        * Open the Settings for the addon on the Customization tab
        <item>
            <title>JEN: Customization</title>
            <mysettings>0/0</mysettings>
        </item>

        * Open the Settings for the addon on the Cache tab

        <item>
            <title>JEN: Cache</title>
            <mysettings>1/0</mysettings>
        </item>

	### Pairing ###

        * Gives option to pair device with any of the supported pairing sites
        <item>
            <title>Pair With Sites</title>
            <pairwith>pairlist</pairwith>
        </item>

        * Opens UptoBox site to pair device with.  A VPN is required to pair with UptoBox from the USA !!!
        <item>
            <title>Pair UptoBox</title>
            <pairwith>uptobox</pairwith>
        </item>
		* To paith with a site other than "uptobox", use "flashx", "vevio", "vidup" or "videoshare"

	### Authorizing ###

        * Gives option to authorize ResolveURL with any/all supported Debrid Services
        <item>
            <title>Authorize Debrid Services</title>
            <authwith>authlist</authwith>
        </item>

        * Displays code to authorize ResolveURL with RealDebrid, waits 20 seconds, then displays the RealDebrid site to enter the code in
        <item>
            <title>Authorize RealDebrid</title>
            <authwith>realdebrid</authwith>
        </item>

        * Displays code to authorize ResolveURL with AllDebrid, waits 20 seconds, then displays the AllDebrid site to enter the code in
        <item>
            <title>Authorize AllDebrid</title>
            <authwith>alldebrid</authwith>
        </item>

        * Displays code to authorize ResolveURL with Premiumize.me, waits 20 seconds, then displays the Premiumize.me site to enter the code in
        <item>
            <title>Authorize Premiumize</title>
            <authwith>premiumize</authwith>
        </item>

        * Displays prompt for LinkSnappy account details (Username, Password) to authorize ResolveURL with LinkSnappy
        <item>
            <title>Authorize LinkSnappy</title>
            <authwith>linksnappy</authwith>
        </item>

	### Function Cache ###

        * Gives option to clear function cache any/all supported Resolvers
        <item>
            <title>Clear Resolver Function Cache</title>
            <funccache>funclist</funccache>
        </item>

        * Clears function cache for ResolveURL
        <item>
            <title>Clear ResolveURL Function Cache</title>
            <funccache>resolveurl</funccache>
        </item>

        * Clears function cache for URLResolver
        <item>
            <title>Clear URLResolver Function Cache</title>
            <funccache>urlresolver</funccache>
        </item>

	### Password Protection ###

        * Password protects a menu for which its corresponding xml is a Local file.  Everything between the <passreq></passreq> tags MUST be Base64 Encoded!
        <item>
            <title>Password Protected Local File</title>
            <passreq>ThisIsThePassword|file://submenu.xml</passreq>
        </item>

        * Password protects a menu for which its corresponding xml is a Remote file  Everything between the <passreq></passreq> tags MUST be Base64 Encoded!
        <item>
            <title>Password Protected Remote File</title>
            <passreq>ThisIsThePassword|http://www.example.com/submenu.xml</passreq>
        </item>

	### Adult Protection ###
        
        * Password protects Adult menu for which its corresponding xml is a Local file.  Everything between the <adultpass></adultpass> tags MUST be Base64 Encoded!
        <item>
            <title>ADULT_Time</title>
            <adultpass>ThisIsThePassword|file://adultmenu.xml</adultpass>
        </item>

        * Password protects Adult menu for which its corresponding xml is a Remote file.  Everything between the <adultpass></adultpass> tags MUST be Base64 Encoded!
        <item>
            <title>Myadult Area</title>
            <adultpass>ThisIsThePassword|http://www.example.com/adultmenu.xml</adultpass>
        </item>

	### Trailer ###

        * Adds the Trailer option for a specific movie to the context menu when Metadata is DISABLED in your addon
        <item>
            <title>Dune (1984)</title>
            <trailer>plugin://plugin.video.youtube/play/?video_id=ChA0qNHV1D4</trailer>
        </item>

	### Custom Modes ###

        * Sets a specific Mode for the menu item, to utilize Jen modes not normally accessible. Setting modeurl passes a custom built url= variable to go with it
        <item>
            <title>Custom Mode</title>
            <mode>Whatever</mode>
            <modeurl>query=Iwant</modeurl>
        </item>

"""

import collections,requests,re,os,time,traceback,webbrowser
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
import base64
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

COLOR1 = ""
COLOR2 = ""

addon_id = xbmcaddon.Addon().getAddonInfo('id')
this_addon   = xbmcaddon.Addon(id=addon_id)
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
addon_path   = xbmcaddon.Addon().getAddonInfo('path')


PAIR_LIST = [ ("flashx", "https://www.flashx.tv/?op=login&redirect=https://www.flashx.tv/pairing.php"),
              ("uptobox", "https://uptobox.com/pin"),
              ("vevio", "https://vev.io/pair"),
              ("vidup", "https://vidup.io/pair"),
              ("videoshare", "http://vshare.eu/pair") ]


AUTH_LIST = [ ("realdebrid", "http://real-debrid.com/device"),
              ("alldebrid", "https://alldebrid.com/pin"),
              ("premiumize", "https://www.premiumize.me/device"),
              ("linksnappy", "https://linksnappy.com") ]


FUNC_LIST = [ ("resolveurl", "script.module.resolveurl"),
              ("urlresolver", "script.module.urlresolver") ]


class JenTools(Plugin):
    name = "jentools"
    priority = 200

    def process_item(self, item_xml):
        result_item = None
        if "<heading>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "HEADING",
                'url': item.get("heading", ""),
                'folder': False,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item
        elif "<mysettings>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "MYSETTINGS",
                'url': item.get("mysettings", ""),
                'folder': False,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item
        elif "<passreq>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "PASSREQ",
                'url': item.get("passreq", ""),
                'folder': True,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item
        elif "<mode>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': item.get("mode", ""),
                'url': item.get("modeurl", ""),
                'folder': True,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item
        elif "<pairwith>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "PAIRWITH",
                'url': item.get("pairwith", ""),
                'folder': False,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item
        elif "<authwith>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "AUTHWITH",
                'url': item.get("authwith", ""),
                'folder': False,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item
        elif "<trailer>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "PAIRWITH",
                'url': item.get("pairwith", ""),
                'folder': False,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["info"]["trailer"] = item.get("trailer", None)
            return result_item
        elif "<funccache>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "FUNCCACHE",
                'url': item.get("funccache", ""),
                'folder': False,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item
        elif "<adultpass>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "ADULTREQ",
                'url': item.get("adultpass", ""),
                'folder': True,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            return result_item


@route(mode='HEADING')
def heading_handler():
    try:
        quit()
    except:
        pass


@route(mode="MYSETTINGS", args=["url"])
def mysettings_handler(query):
    try:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % addon_id)
        c, f = query.split('/')
        xbmc.executebuiltin('SetFocus(%i)' % (int(c) + 100))
        xbmc.executebuiltin('SetFocus(%i)' % (int(f) + 200))
    except:
        return


@route(mode="PASSREQ", args=["url"])
def password_handler(url):
    pins = ""
    prot_xml = ''
    sep_list = base64.b64decode(url + '=' * (-len(url) % 4)).split('|')
    dec_pass = sep_list[0]
    xml_loc = sep_list[1]

    SESSION_HOURS = this_addon.getSetting('SESSION_HOURS')
    if SESSION_HOURS == '':
        SESSION_HOURS = '1'
    expires_at = this_addon.getSetting('PASS_EXPIRES_AT')
    if time.time() > expires_at or expires_at == '':
        input = ''
        if not COLOR1 == "":
            enterpass = "[COLOR %s]Are you worthy?[/COLOR]" % COLOR1
        else:
            enterpass = "Are you worthy?"
        keyboard = xbmc.Keyboard(input, enterpass)
        keyboard.doModal()
        if keyboard.isConfirmed():
            input = keyboard.getText()
        if input == dec_pass:
            expires_at = time.time() + 60 * 60 * int(SESSION_HOURS)
            this_addon.setSetting("PASS_EXPIRES_AT", str(expires_at))
            if 'http' in xml_loc:
                prot_xml = requests.get(xml_loc).content
            else:
                import xbmcvfs
                xml_loc = xml_loc.replace('file://', '')
                xml_file = xbmcvfs.File(os.path.join(addon_path, "xml", xml_loc))
                prot_xml = xml_file.read()
                xml_file.close()
        else:
            if not COLOR2 == "":
                passfail = "[COLOR %s]Wrong Answer...You are not worthy![/COLOR]" % COLOR2
            else:
                passfail = "Wrong Answer...You are not worthy!"
            prot_xml += "<item>"\
                    "    <title>%s</title>"\
                    "    <thumbnail>https://nsx.np.dl.playstation.net/nsx/material/c/ce432e00ce97a461b9a8c01ce78538f4fa6610fe-1107562.png</thumbnail>"\
                    "</item>" % passfail
    else:
        if 'http' in xml_loc:
            prot_xml = requests.get(xml_loc).content
        else:
            import xbmcvfs
            xml_loc = xml_loc.replace('file://', '')
            xml_file = xbmcvfs.File(os.path.join(addon_path, "xml", xml_loc))
            prot_xml = xml_file.read()
            xml_file.close()

    jenlist = JenList(prot_xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode="PAIRWITH", args=["url"])
def pairing_handler(url):
    try:
        site = ''
        if 'pairlist' in url:
            names = []
            for item in PAIR_LIST:
                the_title = '[COLOR %s]Pair with [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, item[0].capitalize())
                names.append(the_title)
            selected = xbmcgui.Dialog().select('[COLOR %s]Select Site To Pair Device With[/COLOR]' % COLOR2, names)

            if selected ==  -1:
                return

            # If you add [COLOR] etc to the title stuff in names loop above, this will strip all of that out and make it usable here
            pair_item = re.sub('\[.*?]','',names[selected]).replace('Pair with ', '').lower()
            for item in PAIR_LIST:
                if str(item[0]) == pair_item:
                    site = item[1]
                    break
        else:
            for item in PAIR_LIST:
                if str(item[0]) == url:
                    site = item[1]
                    break

        check_os = platform()
        if check_os == 'android':
            open_site = xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' % (site))
        elif check_os == 'osx':
           os.system("open " + site)
        else:
            open_site = webbrowser.open(site)
    except Exception:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('Exception',str(failure))
        pass


@route(mode="AUTHWITH", args=["url"])
def authorizing_handler(url):
    try:
        site = ''
        if 'authlist' in url:
            names = []
            for item in AUTH_LIST:
                the_title = '[COLOR %s]Authorize with [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, item[0].capitalize())
                names.append(the_title)
            selected = xbmcgui.Dialog().select('[COLOR %s]Select Debrid Service To Authorize With[/COLOR]' % COLOR2, names)

            if selected ==  -1:
                return

            # If you add [COLOR] etc to the title stuff in names loop above, this will strip all of that out and make it usable here
            auth_item = re.sub('\[.*?]','',names[selected]).replace('Authorize with ', '').lower()
            for item in AUTH_LIST:
                if str(item[0]) == auth_item:
                    site = item[1]
                    break
        else:
            for item in AUTH_LIST:
                if str(item[0]) == url:
                    site = item[1]
                    break
        if str(item[0]) == "realdebrid":
            auth_mode = "auth_rd"
        elif str(item[0]) == "alldebrid":
            auth_mode = "auth_ad"
        elif str(item[0]) == "premiumize":
            auth_mode = "auth_pm"
        else:
            auth_mode = "auth_ls"
        xbmc.executebuiltin("RunPlugin(plugin://script.module.resolveurl/?mode=%s)" % auth_mode)
        if not auth_mode == "auth_ls":
            time.sleep(20)
            check_os = platform()
            if check_os == 'android':
                open_site = xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' % (site))
            elif check_os == 'osx':
               os.system("open " + site)
            else:
                open_site = webbrowser.open(site)
    except Exception:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('Exception',str(failure))
        pass


@route(mode="FUNCCACHE", args=["url"])
def funccache_handler(url):
    try:
        plugin = ''
        if 'funclist' in url:
            names = []
            for item in FUNC_LIST:
                the_title = '[COLOR %s]Clear [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, item[0].capitalize())
                names.append(the_title)
            selected = xbmcgui.Dialog().select('[COLOR %s]Select Resolver To Clear Function Cache For[/COLOR]' % COLOR2, names)

            if selected ==  -1:
                return

            # If you add [COLOR] etc to the title stuff in names loop above, this will strip all of that out and make it usable here
            rslvr_item = re.sub('\[.*?]','',names[selected]).replace('Clear ', '').lower()
            for item in FUNC_LIST:
                if str(item[0]) == rslvr_item:
                    plugin = item[1]
                    break
        else:
            for item in FUNC_LIST:
                if str(item[0]) == url:
                    plugin = item[1]
                    break
        if xbmc.getCondVisibility('System.HasAddon(%s)' % plugin):
            xbmc.executebuiltin('RunPlugin(plugin://%s/?mode=reset_cache)' % plugin)
        else:
            xbmcgui.Dialog().notification("[COLOR %s]Clear %s Function Cache[/COLOR]" % (plugin, COLOR1), "[COLOR %s]%s not found![/COLOR]" % (plugin, COLOR2))

    except Exception:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('Exception',str(failure))
        pass


@route(mode="ADULTREQ", args=["url"])
def adultpass_handler(url):
    pins = ""
    adult_xml = ''
    try:
        adult_setting = this_addon.getSetting('adult_menu')
        if adult_setting == None or adult_setting == '':
            adult_setting = 'false'
            xbmcaddon.Addon().setSetting('adult_menu', str(adult_setting))
        if adult_setting == 'false':
            if not COLOR1 == "":
                adultenable = "[COLOR %s]This menu is not enabled![/COLOR]" % COLOR2
            else:
                adultenable = "This menu is not enabled!"
            adult_xml += "<item>"\
                    "    <title>%s</title>"\
                    "    <thumbnail>https://nsx.np.dl.playstation.net/nsx/material/c/ce432e00ce97a461b9a8c01ce78538f4fa6610fe-1107562.png</thumbnail>"\
                    "</item>" % adultenable
            jenlist = JenList(adult_xml)
            display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
            return
    except:
        return
    sep_list = base64.b64decode(url + '=' * (-len(url) % 4)).split('|')
    dec_pass = sep_list[0]
    xml_loc = sep_list[1]
    SESSION_HOURS = this_addon.getSetting('SESSION_HOURS')
    if SESSION_HOURS == '':
        SESSION_HOURS = '1'
    expires_at = this_addon.getSetting('ADULTPASS_EXPIRES_AT')
    if time.time() > expires_at or expires_at == '':
        input = ''
        if not COLOR1 == "":
            enterpass = "[COLOR %s]Are You Old Enough To Be Naughty?[/COLOR]" % COLOR1
        else:
            enterpass = "Are You Old Enough To Be Naughty?"
        keyboard = xbmc.Keyboard(input, enterpass)
        keyboard.doModal()
        if keyboard.isConfirmed():
            input = keyboard.getText()
        if input == dec_pass:
            expires_at = time.time() + 60 * 60 * int(SESSION_HOURS)
            this_addon.setSetting("ADULTPASS_EXPIRES_AT", str(expires_at))
            if 'http' in xml_loc:
                adult_xml = requests.get(xml_loc).content
            else:
                import xbmcvfs
                xml_loc = xml_loc.replace('file://', '')
                xml_file = xbmcvfs.File(os.path.join(addon_path, "xml", xml_loc))
                adult_xml = xml_file.read()
                xml_file.close()
        else:
            if not COLOR2 == "":
                passfail = "[COLOR %s]Wrong Answer...No Naughty Time for YOU![/COLOR]" % COLOR2
            else:
                passfail = "Wrong Answer...No Naughty Time for YOU!"
            adult_xml += "<item>"\
                    "    <title>%s</title>"\
                    "    <thumbnail>https://nsx.np.dl.playstation.net/nsx/material/c/ce432e00ce97a461b9a8c01ce78538f4fa6610fe-1107562.png</thumbnail>"\
                    "</item>" % passfail
    else:
        if 'http' in xml_loc:
            adult_xml = requests.get(xml_loc).content
        else:
            import xbmcvfs
            xml_loc = xml_loc.replace('file://', '')
            xml_file = xbmcvfs.File(os.path.join(addon_path, "xml", xml_loc))
            adult_xml = xml_file.read()
            xml_file.close()

    jenlist = JenList(adult_xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def platform():
    if xbmc.getCondVisibility('system.platform.android'):   return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):   return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'): return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):     return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):    return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):     return 'ios'