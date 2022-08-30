# coding: utf-8
# Name:        play.py
# Author:      Mancuniancol
# Created on:  28.11.2016
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html
"""
Play a link from torrent or magnet
"""
from contextlib import closing
import time,logging,xbmc,xbmcgui
from urllib import quote_plus
from storage import Storage
import logger,urllib2
from urlparse import urlparse
import socket,json,xbmcaddon
from browser import get_links
from urllib import quote_plus, unquote_plus, urlencode
Addon = xbmcaddon.Addon()
MAGNETIC_SERVICE_HOST = "127.0.0.1"
MAGNETIC_SERVICE_PORT = 5005
def end_busy():
    """
    End Busy icon
    """
    xbmc.executebuiltin("Dialog.Close(busydialog)")
def start_busy():
    """
    Start Busy icon
    """
    xbmc.executebuiltin("ActivateWindow(busydialog)")

def close_dialog():
    """
    Close Ok Dialog
    """
    xbmc.executebuiltin('Dialog.Close(okdialog, true)')

def play(uri, payload=None, item=None):
    """
    Play a magnet or torrent
    :param item:
    :param payload:
    :param uri: magnet or torrent to be played
    :type uri: str
    """
    
    plugin_p = Addon.getSetting('players')
    if plugin_p=='0':
      plugin = 'Quasar'
    elif plugin_p=='1':
      plugin = 'Pulsar'
    elif plugin_p=='2':
      plugin = 'KmediaTorrent'
    elif plugin_p=='3':
      plugin = 'Torrenter'
    elif plugin_p=='4':
      plugin = 'YATP'
    elif plugin_p=='5':
      plugin = 'XBMCtorrent'
    elif plugin_p=='6':
      plugin = 'KODIPOPCORN'
    list_players = ['Quasar', 'Pulsar', 'KmediaTorrent', 'Torrenter', 'YATP', 'XBMCtorrent','KODIPOPCORN']
    if plugin not in list_players:
        close_dialog()
        selection = xbmcgui.Dialog().select("Torrent Player", list_players)
        if selection == -1:
            return

        plugin = list_players[selection]

    filename = get_links(uri)
    if not filename.startswith('magnet'):
        filename = "http://%s:%s?uri=%s" % (str(MAGNETIC_SERVICE_HOST), str(MAGNETIC_SERVICE_PORT),
                                            quote_plus(filename))
    uri_string = quote_plus(filename)
    logging.warning('Filename: %s' % filename)
    if plugin == 'Quasar':
        link = 'plugin://plugin.video.quasar/play?uri=%s' % uri_string

    elif plugin == 'Pulsar':
        link = 'plugin://plugin.video.pulsar/play?uri=%s' % uri_string

    elif plugin == 'KmediaTorrent':
        link = 'plugin://plugin.video.kmediatorrent/play/%s' % uri_string

    elif plugin == "Torrenter":
        link = 'plugin://plugin.video.torrenter/?action=playSTRM&url=' + uri_string

    elif plugin == "YATP":
        link = 'plugin://plugin.video.yatp/?action=play&torrent=' + uri_string
    elif plugin == "KODIPOPCORN":
        link='plugin://plugin.video.kodipopcorntime/?endpoint=player&amp;720psize=1331439862&amp;1080psize=2566242959&amp;720p='+uri_string+'&amp;mediaType=movies'
    else:
        link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string
    
    
    # Remove the dialog
    close_dialog()

    # save link
    if payload and item:
        labels = Storage.open('labels', ttl=60 * 24 * 30)
        item['link'] = link
        labels[payload] = item
        labels.close()
    
    # Play the link
    magnetizer_storage = Storage.open("magnetizer")
    if 'info' in magnetizer_storage:
        info = magnetizer_storage['info']
        info['FileName'] = filename
        info['Path'] = filename
        list_item = xbmcgui.ListItem(info["Title"])
        list_item.setInfo('video', info)
        list_item.setProperty("IsPlayable", "true")
        close_dialog()
        xbmc.Player().play(link, list_item, False)
        # player.setSubtitles(MainURL + srt)

    else:
        xbmc.executebuiltin("PlayMedia(%s)" % link)
    close_dialog()


# noinspection PyTypeChecker
def search(info=None):
    close_dialog()

    # Request data
    operation = info.get('search', '')
    query = info.get('title', '')
    title = quote_plus(query)
    imdb_id = info.get('imdb_id', '')
    payload = ''
    if operation == 'general':
        payload = '?search=general&imdb_id=%s&title=%s' % (imdb_id, title)

    elif operation == "movie":
        year = info.get('year', '')
        payload = '?search=movie&imdb_id=%s&title=%s&year=%s' % (imdb_id, title, year)

    elif operation == "episode":
        season = info.get('season', '')
        episode = info.get('episode', '')
        absolute_number = info.get('absolute_number', '')
        payload = '?search=episode&imdb_id=%s&title=%s&season=%s&episode=%s&absolute_number=%s' % (
            imdb_id, title, season, episode, absolute_number)

    elif operation == "season":
        season = info.get('season', '')
        payload = '?search=episode&imdb_id=%s&title=%s&season=%s' % (imdb_id, title, season)

    # Check if there is previous selection
    labels = Storage.open('labels', ttl=60 * 24 * 30)
    if payload in labels:
        end_busy()
        label = '%s \n %s ' % (labels[payload]["name"], labels[payload]["parser"])
        if xbmcgui.Dialog().yesno('[COLOR FFFFD800][B]magnetic[/B][/COLOR]', "Do you want to use the previous selection?", label):
            resume_point_storage = Storage().open("resume_point", ttl=43200)
            info_video1, resume_point = resume_point_storage.get(xbmc.getInfoLabel("ListItem.Label"), ({}, 0))
            logging.warning(info_video1)
            logging.warning(resume_point)
            resume_point_storage.close()
            link = labels[payload]['link']
            logging.warning(link)
            labels.close()
            result = -1
            if resume_point > 0:
                result = xbmcgui.Dialog().contextmenu(
                    ["Resume from %s" % time.strftime('%H:%M:%S', time.gmtime(resume_point)),
                     "Play from the beginning"])

            list_item = xbmcgui.ListItem(title)
            list_item.setProperty("IsPlayable", "true")
            xbmc.Player().play(link, list_item, False)
            if result != 0:
                return

            logging.warning("Starting Playing")
            while xbmcgui.getCurrentWindowDialogId() > 0 and not xbmc.Player().isPlaying():
                xbmc.sleep(100)

            logging.warning("Seeking: %s" % resume_point)
            xbmc.Player().seekTime(resume_point)
            return

    # Continue
    start_busy()
    labels.close()
    magnetic_url = "http://%s:%s" % (str(MAGNETIC_SERVICE_HOST), str(MAGNETIC_SERVICE_PORT))
    url = magnetic_url + payload
    logging.warning(url)
    results = dict()
    socket.setdefaulttimeout(120)
    try:
        req = urllib2.Request(url, None)
        with closing(urllib2.urlopen(req, timeout=120)) as response:
            results = json.loads(response.read())

    except Exception as e:
        logger.error("Error trying to search %s: %s" % (url, repr(e)))

    # we got the magnets
    items = results.get('magnets', [])
   
    end_busy()
    if len(items)> 0:

    

        check_played(items)
        #window = DialogSelect("DialogSelectResults.xml",
        #                      ADDON_PATH,
        #                      "Default",
        #                      title=string(32074) % (len(items), query),
        #                      items=items)
        #close_dialog()
        #window.doModal()
        #selection = window.ret
        
        #del window
        #if selection > -1:
        #    played = Storage.open('played', ttl=60 * 24 * 30)
        #    key = 'info_hash' if len(items[selection]['info_hash']) > 0 else 'uri'
        #    played[items[selection][key]] = 'x'
        #    played.close()
        #    play(items[selection]['uri'], payload, items[selection])
        #    logging.warning('selection')
        #    logging.warning(items[selection]['uri'])
        #    logging.warning(payload)
        #    logging.warning(items[selection])
    return items

def check_played(items=None):
    played = Storage.open('played', ttl=60 * 24 * 30)
    for item in items:
        key = 'info_hash' if len(item['info_hash']) > 0 else 'uri'
        if item[key] in played:
            item['played'] = 'true'

        else:
            item['played'] = 'false'

    played.close()
