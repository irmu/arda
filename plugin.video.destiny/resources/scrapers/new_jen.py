import koding,logging,PTN,json
import koding.router as router
import xbmc,xbmcgui,xbmcplugin,xbmcaddon
from addall import addNolink,addDir3,addLink
import __builtin__

addon_id   = xbmcaddon.Addon().getAddonInfo('id')
ownAddon   = xbmcaddon.Addon(id=addon_id)
__builtin__.tvdb_api_key = ownAddon.getSetting('tvdb_api_key')
__builtin__.tmdb_api_key = ownAddon.getSetting('tmdb_api_key')
__builtin__.trakt_client_id = ownAddon.getSetting('trakt_api_client_id')
__builtin__.trakt_client_secret = ownAddon.getSetting('trakt_api_client_secret')
__builtin__.search_db_location = ownAddon.getSetting('search_db_location')

__builtin__.login_url = ownAddon.getSetting('login_url')
__builtin__.login_verified = ownAddon.getSetting('login_verified')
__builtin__.user_var = ownAddon.getSetting('user_var')
__builtin__.pwd_var = ownAddon.getSetting('pwd_var')
__builtin__.session_length = ownAddon.getSetting('session_length')

from koding import route
from resources.lib.util.xml import JenList, display_list, fetch_from_db, display_data, clean_url
from resources.lib.plugins import *

from resources.lib.plugin import run_hook

def get_list(url,icon,fan):
    """display jen list"""
    pins = url
    Pins = clean_url(url)
    Items = fetch_from_db(Pins)
    
    if Items:
        
        display_data(Items)
        
        return True
    else:               
        global content_type
        jen_list = JenList(url)
        if not jen_list:
            koding.dolog(_("returned empty for ") + url)
        try:
            items = jen_list.get_list()
        except:
            logging.warning('Destiny JEN')
            from jen import check_jen_categroys
            check_jen_categroys(url,icon,fan)
            return '0'
        content = jen_list.get_content_type()
        
        if items == []:
            return False
        if content:
            content_type = content
        #logging.warning(items)
        display_list(items, content_type, pins)
        return True
        logging.warning(content_type)
        for it in items:
            
            if it['folder']==True:
                 plot=it.get('plot',' ')
                 if plot==None:
                    plot=' '
                 
                 
                 addDir3(it['label'],it['url'],141,it['icon'],it['fanart'],plot,data=it['year'],original_title=it['label'],id=it['imdb'],heb_name=it['mode'],show_original_year=it['year'])
            else:
                plot=it.get('plot',' ')
                if plot==None:
                    plot=' '
                info=(PTN.parse(it['label']))
                video_data={}
                
                video_data['title']=info['title'].replace('=',' ').replace('[B]','').replace('[/B]','').replace('silver','').replace('deepskyblue','').replace('[','').replace(']','').replace('/COLOR','').replace('COLOR','').replace('4k','').replace('4K','').strip().replace('(','.').replace(')','.').replace(' ','.').replace('..','.')
                year=''
                if 'year' in info:
                    year=info['year']
                    video_data['year']=info['year']
                else:
                   year=it['year']
                   video_data['year']=year
                   
                video_data['plot']=plot
                logging.warning(it['label'])
                addLink(it['label'],it['url'],5,False,iconimage=it['icon'],fanart=it['fanart'],description=plot,data=year,original_title=it['label'],id=it['imdb'],video_info=json.dumps(video_data))
                
        return True

