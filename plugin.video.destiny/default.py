# -*- coding: utf-8 -*-
import xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys,logging,time,random
from os import listdir
from os.path import isfile, join
Addon = xbmcaddon.Addon()
import pyxbmct
import requests,json
import xbmcvfs
import koding
import socket
import  threading
global done_nextup 
global all_data_imdb
global susb_data,susb_data_next
global all_s_in
global stop_window
global stop_try_play,global_result
global playing_text,mag_start_time_new
global now_playing_server,stop_all,close_on_error
global wait_for_subs
global in_next_ep
in_next_ep=0
wait_for_subs=0
close_on_error=0

global done1,done1_1,close_sources_now,once_fast_play
once_fast_play=0
close_sources_now=0
done1_1=0
done1=0
stop_all=0

now_playing_server=''
mag_start_time_new=0
global_result=''
playing_text=''
stop_try_play=False
stop_window=False
all_s_in=({},0,'','','')
all_data_imdb=[]
done_nextup=0
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
libDir = os.path.join(addonPath, 'resources', 'lib')
sys.path.append( libDir)
libDir = os.path.join(addonPath, 'resources', 'lib2')
sys.path.append( libDir)
libDir = os.path.join(addonPath, 'resources', 'plugins')
sys.path.append( libDir)
libDir = os.path.join(addonPath, 'resources', 'solvers')
sys.path.append( libDir)
libDir = os.path.join(addonPath, 'resources', 'solvers','resolver')

sys.path.append( libDir)
libDir = os.path.join(addonPath, 'resources', 'solvers','torrentool')

sys.path.append( libDir)

done_dir = os.path.join(addonPath, 'resources', 'done')
sys.path.append( done_dir)

sys.path.append( libDir)
rd_dir = os.path.join(addonPath, 'resources', 'done','rd')
sys.path.append( rd_dir)

mag_dir = os.path.join(addonPath, 'resources', 'done','magnet')
sys.path.append( mag_dir)

libDir = os.path.join(addonPath, 'resources', 'scrapers')
sys.path.append( libDir)

m3_dir = os.path.join(addonPath, 'resources', 'm3u8')


BASE_LOGO=os.path.join(addonPath, 'resources', 'logos/')
tmdb_data_dir = os.path.join(addonPath, 'resources', 'tmdb_data')
debug_mode=False
if Addon.getSetting("debugmode")=='true':
  debug_mode=True


lan=xbmc.getInfoLabel('System.Language')


from general import res_q,clean_name,check_link,server_data,replaceHTMLCodes,domain_s,similar,cloudflare_request,fix_q,call_trakt,post_trakt,reset_trakt,cloudflare_request,base_header
import cache as  cache
import PTN as PTN

__PLUGIN_PATH__ = Addon.getAddonInfo('path')

from globals import *
from tmdb import *
from addall import addNolink,addDir3,addLink

DESIMG=os.path.join(addonPath,'fanart.jpg')

socket.setdefaulttimeout(40.0)



global imdb_global,search_done,silent_mode,close_all,list_index,all_links_sources
all_links_sources={}
search_done=0

list_index=999
silent_mode=False



if debug_mode==False:
  reload(sys)  
  sys.setdefaultencoding('utf8')
 
imdb_global=' '

rd_sources=Addon.getSetting("rdsource")
allow_debrid = rd_sources == "true" 
ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108
def TextBox_help(title, msg):
    class TextBoxes(xbmcgui.WindowXMLDialog):
        def onInit(self):
            
            self.title      = 101
            self.msg        = 102
            self.scrollbar  = 103
            self.okbutton   = 201
            self.imagecontrol=202
            self.y=0
            self.showdialog()

        def showdialog(self):
            import random
            self.getControl(self.title).setLabel(title)
            self.getControl(self.msg).setText(msg)
            self.getControl(self.imagecontrol).setImage("https://wallpaperstock.net/wallpapers/thumbs1/36550hd.jpg")
            self.setFocusId(self.scrollbar)
            all_op=['fJ9rUzIMcZQ','HgzGwKwLmgM','RNoPdAq666g','9f06QZCVUHg','s6TtwR2Dbjg','yt7tUJIK9FU','NJsa6-y4sDs','Nq8TasNsgKw','0pibtxAO00I','jkPl0e8DlKc','WQnAxOQxQIU']
            random.shuffle(all_op)
            from youtube_ext import get_youtube_link2
            if all_op[0]!=None:
              try:
                f_play= get_youtube_link2('https://www.youtube.com/watch?v='+all_op[0]).replace(' ','%20')
                xbmc.Player().play(f_play,windowed=True)
            
              except Exception as e:
                    pass
            
            xbmc.executebuiltin("Dialog.Close(busydialog)")
        def onClick(self, controlId):
            if (controlId == self.okbutton):
                xbmc.Player().stop()
                self.close()
        
        def onAction(self, action):
            if   action == ACTION_PREVIOUS_MENU: 
                xbmc.Player().stop()
                self.close()
            elif action == ACTION_NAV_BACK: 
                    xbmc.Player().stop()
                    self.close()
            
            
    tb = TextBoxes( "Textbox.xml" , Addon.getAddonInfo('path'), 'DefaultSkin', title=title, msg=msg)
    tb.doModal()
    del tb
    
# You can add \n to do line breaks
CONTACT        = 'test'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'https://ballzbeatz.com/wp-content/uploads/2018/01/Destiny-Destiny-Logo-Silhouette-Decal-768x768.jpg'
CONTACTFANART  = 'http://'
ADDONTITLE     = 'Destiny' 
COLOR1         = 'gold'
COLOR2         = 'white'
COLOR3         = 'red'
COLOR3         = 'blue'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required 
THEME4         = '[COLOR '+COLOR1+']%s[/COLOR] [COLOR '+COLOR2+']:[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7
ACTION_MOVE_UP = 3
ACTION_MOVE_DOWN = 4
ACTION_STEP_BACK = 21
ACTION_NAV_BACK = 92
ACTION_MOUSE_RIGHT_CLICK = 101
ACTION_MOUSE_MOVE = 107
ACTION_BACKSPACE = 110
KEY_BUTTON_BACK = 275 

def contact(title='',msg=""):
	class MyWindow(xbmcgui.WindowXMLDialog):
		def __init__(self, *args, **kwargs):
			self.title = THEME3 % kwargs["title"]
			self.image = kwargs["image"]
			self.fanart = kwargs["fanart"]
			self.msg = THEME2 % kwargs["msg"]

		def onInit(self):
			self.fanartimage = 101
			self.titlebox = 102
			self.imagecontrol = 103
			self.textbox = 104
			self.scrollcontrol = 105
			self.button = 199
			self.showdialog()

		def showdialog(self):
			self.getControl(self.imagecontrol).setImage(self.image)
			self.getControl(self.fanartimage).setImage(self.fanart)
			self.getControl(self.fanartimage).setColorDiffuse('9FFFFFFF')
			self.getControl(self.textbox).setText(self.msg)
			self.getControl(self.titlebox).setLabel(self.title)
            
	
		
            
			self.setFocusId(self.button)
			
		def onAction(self,action):
			if   action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

	cw = MyWindow( "Contact.xml" , Addon.getAddonInfo('path'), 'DefaultSkin', title=title, fanart=CONTACTFANART, image=CONTACTICON, msg=msg)
	cw.doModal()
	del cw
FILENAME='contextmenu.xml'
ACTION_BACK          = 92
ACTION_PARENT_DIR    = 9
ACTION_PREVIOUS_MENU = 10
ACTION_CONTEXT_MENU  = 117
ACTION_C_KEY         = 122

ACTION_LEFT  = 1
ACTION_RIGHT = 2
ACTION_UP    = 3
ACTION_DOWN  = 4

class ContextMenu(xbmcgui.WindowXMLDialog):

    def __new__(cls, addonID, menu,icon,fan,txt):
        FILENAME='contextmenu.xml'
        return super(ContextMenu, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID, menu,icon,fan,txt):
        super(ContextMenu, self).__init__()
        self.menu = menu
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.icon=icon
        self.fan=fan
        self.text=txt
    def onInit(self):
        line   = 38
        spacer = 20
        delta  = 0 

        nItem = len(self.menu)
        if nItem > 16:
            nItem = 16
            delta = 1
        self.getControl(self.imagecontrol).setImage(self.icon)
        self.getControl(self.bimagecontrol).setImage(self.fan)
        self.getControl(self.txtcontrol).setText(self.text)
        height = (line+spacer) + (nItem*line)
        height=1100
        self.getControl(5001).setHeight(height)
            
        self.list = self.getControl(3000)
        self.list.setHeight(height)

        newY = 360 - (height/2)

        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)

        self.params    = None
        self.paramList = []
        #txt='[COLOR deepskyblue]'+name.replace('-',' ').replace('%20',' ').strip()+'[/COLOR]\nServer: '+server+' Subs: '+str(pre_n)+'  Quality:[COLOR gold] ◄'+q+'► [/COLOR]Provider: [COLOR lightblue]'+supplay+'[/COLOR] Size:[COLOR coral]'+size+'[/COLOR]$$$$$$$'+link
        #import textwrap
        for item in self.menu:
            self.paramList.append(item[6])
            
            if len(item[0])>60:
            #    item[0]="\n".join(textwrap.wrap(item[0],60))
                 item[0]=item[0][0:60]+'\n'+item[0][60:len(item[0])]
            add_rd=''
            logging.warning('rd status:')
         
            if item[7]:
                add_rd='[COLOR gold]RD- [/COLOR]'
            title =add_rd+'[COLOR deepskyblue][B]'+item[0] +'[/B][/COLOR]'
            if len(item[1].strip())<2:
                item[1]='--'
            if len(item[2].strip())<2:
                item[2]='--'
            if len(item[3].strip())<2:
                item[3]='--'
            if len(item[4])<2:
                item[4]='--'
            if len(item[5])<2:
                item[5]='--'
            server=item[1]
            pre_n='[COLOR khaki]'+item[2]+'[/COLOR]'
            q=item[3]
            supplay='[COLOR lightblue]'+item[4]+'[/COLOR]'
            size='[COLOR coral]'+item[5]+'[/COLOR]'
            link=item[6]
            
            
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('server', server)
            liz.setProperty('pre',pre_n)
            liz.setProperty('Quality', q)
            liz.setProperty('supply', supplay)
            liz.setProperty('size', size)
            
            self.list.addItem(liz)

        self.setFocus(self.list)

           
    def onAction(self, action):  
        actionId = action.getId()

        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = 888
            xbmc.sleep(100)
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            self.params = 888
            return self.close()


    def onClick(self, controlId):
        if controlId != 3001:
            index = self.list.getSelectedPosition()        
            try:    self.params = index
            except: self.params = None

        self.close()
        

    def onFocus(self, controlId):
        pass
def get_trailer_f(id,tv_movie):
    import random
    try:
        html_t='99'
        logging.warning('Get Trailer')
        if tv_movie=='movie':
          url_t='http://api.themoviedb.org/3/movie/%s/videos?api_key=1248868d7003f60f2386595db98455ef&language=en'%id
        else:
          url_t='http://api.themoviedb.org/3/tv/%s/videos?api_key=1248868d7003f60f2386595db98455ef&language=en'%id
        html_t=requests.get(url_t).json()
        if len(html_t['results'])==0:
            if tv_movie=='movie':
              url_t='http://api.themoviedb.org/3/movie/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id
            else:
              url_t='http://api.themoviedb.org/3/tv/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id
            html_t=requests.get(url_t).json()
        else:
            logging.warning(html_t)
        if len(html_t['results'])>0:
            vid_num=random.randint(0,len(html_t['results'])-1)
        else:
          return 0
        video_id=(html_t['results'][vid_num]['key'])
        #from pytube import YouTube
        #playback_url = YouTube(domain_s+'www.youtube.com/watch?v='+video_id).streams.first().download()
        playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
        from youtube_ext import get_youtube_link2
        if video_id!=None:
          try:
            return get_youtube_link2('https://www.youtube.com/watch?v='+video_id).replace(' ','%20')
          except Exception as e:
            logging.warning(e)
            return ''
        else:
            return ''
        return playback_url
    except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Line:'+str(lineno)+' E:'+str(e))).encode('utf-8'))
        logging.warning('ERROR IN Trailer :'+str(lineno))
        logging.warning('inline:'+line)
        logging.warning(e)
        logging.warning(html_t)
        logging.warning('BAD Trailer play')
        return ''
class ContextMenu_new(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID, menu,icon,fan,txt):
        FILENAME='contextmenu_new.xml'
        return super(ContextMenu_new, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID, menu,icon,fan,txt):
        super(ContextMenu_new, self).__init__()
        self.menu = menu
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.icon=icon
        self.fan=fan
        self.text=txt
    
    def onInit(self):
        line   = 38
        spacer = 20
        delta  = 0 

        nItem = len(self.menu)
        if nItem > 16:
            nItem = 16
            delta = 1
        self.getControl(self.imagecontrol).setImage(self.icon)
        self.getControl(self.bimagecontrol).setImage(self.fan)
        self.getControl(self.txtcontrol).setText(self.text)
        height = (line+spacer) + (nItem*line)
        height=1100
        self.getControl(5001).setHeight(height)
            
        self.list = self.getControl(3000)
        self.list.setHeight(height)

        newY = 360 - (height/2)

        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)
        
       
        
        self.params    = None
        self.paramList = []
        #txt='[COLOR deepskyblue]'+name.replace('-',' ').replace('%20',' ').strip()+'[/COLOR]\nServer: '+server+' Subs: '+str(pre_n)+'  Quality:[COLOR gold] ◄'+q+'► [/COLOR]Provider: [COLOR lightblue]'+supplay+'[/COLOR] Size:[COLOR coral]'+size+'[/COLOR]$$$$$$$'+link
        #import textwrap
        for item in self.menu:
            self.paramList.append(item[6])
            '''
            info=(PTN.parse(item[0]))
            if 'excess' in info:
                if len(info['excess'])>0:
                    item[0]='.'.join(info['excess'])
            '''
            
                
            if len(item[0])>45 and '►►►' not in item[0]:
            #    item[0]="\n".join(textwrap.wrap(item[0],60))
                 item[0]=item[0][0:45]+'\n'+item[0][45:len(item[0])]
            title ='[COLOR deepskyblue][B]'+item[0] +'[/B][/COLOR]'
            if len(item[1].strip())<2:
                item[1]='--'
            if len(item[2].strip())<2:
                item[2]='--'
            if len(item[3].strip())<2:
                item[3]='--'
            if len(item[4])<2:
                item[4]='--'
            if len(item[5])<2:
                item[5]='--'
            server=item[1]
            pre_n='[COLOR khaki]'+item[2]+'[/COLOR]'
            q=item[3]
            supplay='[COLOR lightblue]'+item[4]+'[/COLOR]'
            size='[COLOR coral]'+item[5]+'[/COLOR]'
            link=item[6]
            
            if item[7]==True or ('magnet' in server and allow_debrid):
                supplay='[COLOR gold]RD - '+supplay+'[/COLOR]'
          
            if '►►►' in item[0]:
                
                title=''
                supplay=item[0]
           
            
                
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('server', server)
            liz.setProperty('pre',pre_n)
            liz.setProperty('Quality', q)
            liz.setProperty('supply', supplay)
            liz.setProperty('size', size)
            
            if '►►►' not in item[0]:
                liz.setProperty('server_v','100')
            if item[7]==True or ('magnet' in server and allow_debrid):
                liz.setProperty('rd', '100')
            if 'magnet' in server or 'torrent' in server.lower():
                liz.setProperty('magnet', '100')
            self.list.addItem(liz)

        self.setFocus(self.list)

           
    def onAction(self, action):  
        actionId = action.getId()

        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = 888
            xbmc.sleep(100)
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            self.params = 888
            return self.close()


    def onClick(self, controlId):
        if controlId != 3001:
            index = self.list.getSelectedPosition()        
            try:    self.params = index
            except: self.params = None
        else:
            self.params = 888
        self.close()
        

    def onFocus(self, controlId):
        pass
class ContextMenu_new2(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID, menu,icon,fan,txt):
        FILENAME='contextmenu_new2.xml'
        return super(ContextMenu_new2, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID, menu,icon,fan,txt):
        global playing_text
        super(ContextMenu_new2, self).__init__()
        self.menu = menu
        self.auto_play=0
        self.params    = 666666
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.icon=icon
        self.fan=fan
        self.text=txt
        playing_text=''
        self.tick=60
        self.done=0
        self.story_gone=0
        self.count_p=0
        self.keep_play=''
        self.tick=60
        self.s_t_point=0
        self.start_time=time.time()
    def background_work(self):
        global playing_text,mag_start_time_new,now_playing_server,done1
        tick=0
        tick2=0
        changed=1
        vidtime=0
        while(1):
            all_t=[]
            for thread in threading.enumerate():
                if ('tick_time' in thread.getName()) or ('background_task' in thread.getName()) or ('get_similer' in thread.getName()) or ('MainThread' in thread.getName()) or ('sources_s' in thread.getName()):
                    continue
                
                if (thread.isAlive()):
                    all_t.append( thread.getName())
            self.getControl(606).setLabel(','.join(all_t))
            if  xbmc.getCondVisibility('Window.IsActive(busydialog)'):
                self.getControl(102).setVisible(True)
                if tick2==1:
                    self.getControl(505).setVisible(True)
                    tick2=0
                else:
                    self.getControl(505).setVisible(False)
                    tick2=1
            else:
                self.getControl(102).setVisible(False)
                self.getControl(505).setVisible(False)
            if len(playing_text)>0 or  self.story_gone==1 :
                changed=1
                vidtime=0
                if xbmc.Player().isPlaying():
                    vidtime = xbmc.Player().getTime()
                
                t=time.strftime("%H:%M:%S", time.gmtime(vidtime))
                
                if len(playing_text)==0:
                    playing_text=self.keep_play
                try:
                    self.keep_play=playing_text
                    self.getControl(self.txtcontrol).setText(t+'\n'+playing_text.split('$$$$')[0]+'\n'+now_playing_server.split('$$$$')[0]+'\n'+now_playing_server.split('$$$$')[1])
                    if vidtime == 0:
                        if tick==1:
                            self.getControl(303).setVisible(True)
                            tick=0
                        else:
                            self.getControl(303).setVisible(False)
                            tick=1
                except Exception as e:
                    logging.warning('Skin ERR:'+str(e))
                    self.params = 888
                    self.done=1
                    logging.warning('Close:4')
                    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                    done1_1=3
                    self.close()
                    pass
            
            elif changed==1:
                changed=0
                
                self.getControl(303).setVisible(False)
                self.getControl(self.txtcontrol).setText(self.text)
            
            if self.done==1:
                break
            if xbmc.Player().isPlaying():
                self.tick=60
                self.count_p+=1
                self.st_time=0
                
                vidtime = xbmc.Player().getTime()
                if self.s_t_point==0:
                    
                    
                    if vidtime > 0:
                        self.getControl(3000).setVisible(False)
                        self.getControl(self.imagecontrol).setVisible(False)
                        self.getControl(505).setVisible(False)
                        self.getControl(909).setPosition(1310, 40)
                        self.getControl(2).setPosition(1310, 100)
                        self.s_t_point=1
                        self.getControl(303).setVisible(False)
                        self.story_gone=1
                        logging.warning('Change seek Time:'+str(mag_start_time_new))
                        try:
                            if int(float(mag_start_time_new))>0:
                                xbmc.Player().seekTime(int(float(mag_start_time_new)))
                        except:
                            pass
                
                if vidtime > 0:
                    playing_text=''
     
                try:
                    value_d=(vidtime-(int(float(mag_start_time_new)))) 
                except:
                    value_d=vidtime
                play_time=int(Addon.getSetting("play_full_time"))
                if value_d> play_time and self.s_t_point>0 :
                    self.params = 888
                    self.done=1
                    logging.warning('Close:1')
                    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                    done1_1=3
                    self.close()
              
                if self.count_p>(play_time+30) :
                   if Addon.getSetting("play_first")!='true':
                   
                    self.params = 888
                    self.done=1
                    logging.warning('Close:3')
                    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                    done1_1=3
                    self.close()
            else:
                self.count_p=0
                self.s_t_point=0
                self.getControl(3000).setVisible(True)
         
                #self.getControl(505).setVisible(True)
                self.getControl(self.imagecontrol).setVisible(True)
                self.story_gone=0
                self.getControl(2).setPosition(1310, 700)
                self.getControl(909).setPosition(1310, 10)
            xbmc.sleep(1000)
    def tick_time(self):
        global done1_1
        while(self.tick)>0:
            self.getControl(self.tick_label).setLabel(str(self.tick))
            self.tick-=1
            if self.params == 888: 
                break
            xbmc.sleep(1000)
        if self.params != 888:
            self.params = 888
            self.done=1
            logging.warning('Close:93')
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            done1_1=3
            self.close()
    def onInit(self):
        xbmc.Player().stop()
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        
        thread=[]
        thread.append(Thread(self.background_work))
        thread[len(thread)-1].setName('background_task')
        thread.append(Thread(self.tick_time))
        thread[len(thread)-1].setName('tick_time')
        thread[0].start()
        thread[1].start()
        
        line   = 38
        spacer = 20
        delta  = 0 
        
        nItem = len(self.menu)
        if nItem > 16:
            nItem = 16
            delta = 1
        self.getControl(self.imagecontrol).setImage(self.icon)
        self.getControl(self.bimagecontrol).setImage(self.fan)
        if len(playing_text)==0:
            self.getControl(self.txtcontrol).setText(self.text)
        height = (line+spacer) + (nItem*line)
        height=1100
        self.getControl(5001).setHeight(height)
            
        self.list = self.getControl(3000)
        self.list.setHeight(height)

        newY = 360 - (height/2)

        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)
        
       
        
        
        self.paramList = []
        #txt='[COLOR deepskyblue]'+name.replace('-',' ').replace('%20',' ').strip()+'[/COLOR]\nServer: '+server+' Subs: '+str(pre_n)+'  Quality:[COLOR gold] ◄'+q+'► [/COLOR]Provider: [COLOR lightblue]'+supplay+'[/COLOR] Size:[COLOR coral]'+size+'[/COLOR]$$$$$$$'+link
        #import textwrap
        all_liz_items=[]
        count=0
        dbcur.execute("SELECT * FROM historylinks")
        all_his_links_pre = dbcur.fetchall()
        all_his_links=[]
        for link,status,option in all_his_links_pre:
            all_his_links.append(link)
        logging.warning('Loading')
        for item in self.menu:
            
            self.getControl(202).setLabel(str(((count*100)/len(self.menu))) + '% Please wait ')
            count+=1
            self.paramList.append(item[6])
            '''
            info=(PTN.parse(item[0]))
            if 'excess' in info:
                if len(info['excess'])>0:
                    item[0]='.'.join(info['excess'])
            '''
            golden=False
            if 'Cached ' in item[0]:
                golden=True
            o_title=item[0].replace('Cached ','')
            
            item[0]=item[0].replace('magnet','').replace('torrent','').replace('Cached ','')
            if len(item[0])>45 and '►►►' not in item[0]:
            #    item[0]="\n".join(textwrap.wrap(item[0],60))
                 item[0]=item[0][0:45]+'\n'+item[0][45:len(item[0])]
            title ='[COLOR deepskyblue][B]'+item[0] +'[/B][/COLOR]'
            if len(item[1].strip())<2:
                item[1]='--'
            if len(item[2].strip())<2:
                item[2]=''
            if len(item[3].strip())<2:
                item[3]='--'
            if len(item[4])<2:
                item[4]='--'
            if len(item[5])<2:
                item[5]='--'
            server=item[1]
            pre_n='[COLOR khaki]'+item[2]+'[/COLOR]'
            q=item[3]
            supplay='[COLOR lightblue]'+item[4].replace('P-0/','')+'[/COLOR]'
            size='[COLOR coral]'+item[5]+'[/COLOR]'
            link=item[6]
            
            if item[7]==True or ('magnet' in o_title and allow_debrid):
                supplay='[COLOR gold]RD - '+supplay+'[/COLOR]'
          
            if '►►►' in item[0]:
                
                title=''
                supplay=item[0]
           
            
            if q=='2160':
                q='4k'
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('server', server)
            liz.setProperty('pre',pre_n)
            liz.setProperty('Quality', q)
            liz.setProperty('supply', supplay)
            liz.setProperty('size', size)
            
            if item[6].encode('base64') in all_his_links:
                liz.setProperty('history','100')
            if '►►►' not in item[0]:
                liz.setProperty('server_v','100')
            if item[7]==True or (('magnet' in o_title or 'torrent' in supplay.lower()) and allow_debrid):
                liz.setProperty('rd', '100')
            if golden:
                liz.setProperty('magnet', '200')
            
            elif 'magnet' in o_title or 'torrent' in supplay.lower():
        
               liz.setProperty('magnet', '100')
            all_liz_items.append(liz)
        logging.warning(' Done Loading')
        self.getControl(202).setLabel('')
        self.list.addItems(all_liz_items)

        self.setFocus(self.list)

    def played(self):
        self.params =7777
    def onAction(self, action):  
        global done1_1
        actionId = action.getId()
        self.tick=60
        logging.warning('ACtion:'+ str(actionId))
        if actionId in [ACTION_LEFT,ACTION_RIGHT ,ACTION_UP,ACTION_DOWN ]:
            self.getControl(3000).setVisible(True)
           
            
            #self.getControl(505).setVisible(True)
            self.getControl(self.imagecontrol).setVisible(True)
            self.getControl(1005).setVisible(False)
            self.story_gone=0
            self.getControl(2).setPosition(1310, 700)
            self.getControl(909).setPosition(1310, 10)
            
            
        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            logging.warning('Close:5')
            self.params = 888
            xbmc.sleep(100)
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            self.done=1
            logging.warning('action1 CLosing')
            done1_1=3
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK,ACTION_NAV_BACK]:
            self.params = 888
            logging.warning('Close:6')
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            self.done=1
            logging.warning('action2 CLosing')
            done1_1=3
            return self.close()

    def wait_for_close(self):
        global done1
        timer=0
        while(done1!=1):
                if timer>10:
                    break
                timer+=1
                self.params = 888
                self.done=1
                xbmc.sleep(200) 
        if timer>10:
            done1_1=3
            self.close()
    def onClick(self, controlId):
        global playing_text,done1
        self.tick=60
        if controlId != 3001:
            '''
            self.getControl(3000).setVisible(False)
            self.getControl(102).setVisible(False)
            self.getControl(505).setVisible(False)
            self.getControl(909).setPosition(1310, 40)
            self.getControl(2).setPosition(1310, 100)
            self.getControl(self.imagecontrol).setVisible(False)
            self.getControl(303).setVisible(False)
            self.story_gone=1
            '''
            index = self.list.getSelectedPosition()        
            try:    self.params = index
            except: self.params = None
            playing_text=''
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
           
            return self.params
        else:
            logging.warning('Close:7')
            self.params = 888
            self.done=1
            #while(done1==0):
            #    self.params = 888
            #    self.done=1
            #    xbmc.sleep(100) 
            thread=[]
            thread.append(Thread(self.wait_for_close))
            thread[len(thread)-1].setName('closing_task')
            thread[0].start()
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            logging.warning('Clicked CLosing')
            #self.close()
        
    def close_now(self):
        global done1_1
        logging.warning('Close:8')
        self.params = 888
        self.done=1
        xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
        xbmc.sleep(1000)
        logging.warning('Close now CLosing')
        done1_1=3
        self.close()
    def onFocus(self, controlId):
        pass
        
class sources_search(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID,id,tv_movie,name):
        FILENAME='sources_s.xml'
        return super(sources_search, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID,fan,tv_movie,name):
        super(sources_search, self).__init__()
       
        self.onint=False
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.close_tsk=0
        self.tv_movie=tv_movie
        self.id=id
        self.name=name
        self.progress=32
        self.progress2=33
        self.label=34
        self.label2=35
        self.label3=36
        self.label4=37
        
        self.progress3=40
        self.progress4=43
        self.label5=38
        self.label6=41
        self.label7=39
        self.label8=42
        
        self.label9=44
        self.label10=45
        self.label11=46
        self.label12=47
        self.label13=48
        self.label14=49
        self.label15=50
        
        self.image_movie=51
        self.label_movie=52
        self.txt_movie=53
        
        self.label16=54
        self.progress5=55
        
        self.label17=56
        self.all_ids_done=0
        self.label18=57
        self.label19=58
        self.label20=59
        
        self.label21=60
        self.progress6=61
        self.label22=62
        self.timer_close=0
        self.all_ids=[]
        xbmc.Player().stop()
        Thread(target=self.background_task).start()
        Thread(target=self.get_similer).start()
    def get_similer(self):
        while self.onint==False:
            xbmc.sleep(100)
        if len(id)>1 and '%' not in id :
            self.getControl(self.label22).setLabel('Getting similar')
            url=domain_s+'api.themoviedb.org/3/%s/%s/recommendations?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1'%(self.tv_movie,self.id.replace('\n',''))
            self.html=get_html(url)
            logging.warning(url)
            all_data_int=[]
            self.all_ids=[]
            self.all_ids_done=0
            for items in self.html['results']:
                
                if self.tv_movie=='movie':
                    title=items['title']
                else:
                    title=items['name']
                self.all_ids.append((items['id'],title))
                rating=''
                if items['vote_average']!=None:
                    rating='[COLOR khaki]'+str(items['vote_average'])+'[/COLOR]'
                all_data_int.append((title,items['backdrop_path'],'Rating-(' + rating+')\n'+items['overview']))
            self.all_ids_done=1
            all_was=[]
            while(1):
                count=0
                while all_data_int[0][1] in all_was:
                    random.shuffle(all_data_int)
                    count+=1
                    if count>15:
                        break
                if all_data_int[0][1]!=None:
                    all_was.append(all_data_int[0][1])
                    self.getControl(self.image_movie).setImage(domain_s+'image.tmdb.org/t/p/original/'+all_data_int[0][1])
                    self.getControl(self.label_movie).setLabel(all_data_int[0][0])
                    self.getControl(self.txt_movie).setText(all_data_int[0][2])
                xbmc.sleep(10000)
                if self.close_tsk>0:
                    break
    def background_task(self):
        global all_s_in
        
        start_time=time.time()
        if fav_status=='true' and Addon.getSetting("fav_search_time_en"):
           max_time=int(Addon.getSetting("fav_search_time"))
        else:
           max_time=int(Addon.getSetting("time_s"))
        counter_close=0
        while(1):
            if self.onint:
              try:
                elapsed_time = time.time() - start_time
                #self.getControl(self.label17).setLabel('Hellpw')
                if self.timer_close==1:
                   self.getControl(self.label17).setLabel('Closing please Wait...')
                else:
                    self.getControl(self.label17).setLabel(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
                #prect=int(100*(elapsed_time/max_time))
                #self.getControl(self.progress6).setPercent(prect)
                #self.getControl(self.label21).setLabel(str(prect)+'%')
                    
                count_hebrew=0
                count_magnet=0
                count_regular=0
                if len(all_s_in[0])>0:
                    txt=[]
                    txt2=[]
                    
                    for names in all_s_in[0]:
                        if names=='magnet':
                            continue
                        if len(all_s_in[0][names]['links'])>0:
                            color='lightgreen'
                            txt.append('[COLOR %s]'%color+names+' - '+str(len(all_s_in[0][names]['links']))+'[/COLOR]')
                        else:
                            color='red'
                            txt2.append('[COLOR %s]'%color+names+' - '+str(len(all_s_in[0][names]['links']))+'[/COLOR]')
                        
                        
                        if 'magnet' in names:
                            count_magnet=count_magnet+len(all_s_in[0][names]['links'])
                        else:
                            count_regular=count_regular+len(all_s_in[0][names]['links'])
                        
                    self.getControl(self.txtcontrol).setText('\n'.join(txt)+'\n'+'\n'.join(txt2))
                if count_regular>0:
                    self.getControl(self.label18).setLabel(str(count_regular))
                if count_magnet>0:
                    self.getControl(self.label19).setLabel(str(count_magnet))
                if count_hebrew>0:
                    self.getControl(self.label20).setLabel(str(count_hebrew))
                
                if all_s_in[3]==1:
                    self.getControl(self.progress).setPercent(all_s_in[1])
                    self.getControl(self.label3).setLabel(str(all_s_in[1])+'%')
                    self.getControl(self.label).setLabel('Collecting Files:'+all_s_in[2])
                elif all_s_in[3]==2:
                    self.getControl(self.progress2).setPercent(all_s_in[1])
                    self.getControl(self.label4).setLabel(str(all_s_in[1])+'%')
                    self.getControl(self.label2).setLabel('Sources: '+all_s_in[2])
                    
                    
                    self.getControl(self.progress).setPercent(100)
                    self.getControl(self.label3).setLabel('100%')
                    self.getControl(self.label).setLabel('Collecting Files: Done')
                elif all_s_in[3]==3:
                    
                    
                    #self.getControl(self.progress5).setPercent(all_s_in[1])
                    #self.getControl(self.label16).setLabel(str(all_s_in[1])+'%')
                  
                    
                    
                    self.getControl(self.progress2).setPercent(100)
                    self.getControl(self.label4).setLabel('100%')
                    self.getControl(self.label2).setLabel('Sources: Done')
                    
                if len(all_s_in[4])>0:
                    regex="4K: (.+?) 1080: (.+?) 720: (.+?) 480: (.+?) Rest: (.+?)  T: (.+?) '"
                    match=re.compile(regex).findall(all_s_in[4])
                    for res4k,res1080,res720,res480,resuk,total in match:
                        self.getControl(self.label9).setLabel(res4k)
                        self.getControl(self.label10).setLabel(res1080)
                        self.getControl(self.label11).setLabel(res720)
                        self.getControl(self.label12).setLabel(res480)
                        self.getControl(self.label13).setLabel(resuk)
                        self.getControl(self.label14).setLabel(subs)
                        self.getControl(self.label15).setLabel(total)
                avg=0
                counter=0
                for i in range(0,8):
                    prec=float(xbmc.getInfoLabel('System.CoreUsage(%s)'%str(i)))
                    if prec>0:
                        avg+=int(prec)
                        counter+=1
                avg_f=int(float(avg/counter))
                try:
                    self.getControl(self.progress3).setPercent(int(xbmc.getInfoLabel('System.CpuUsage').replace('%','')))
                except:
                    self.getControl(self.progress3).setPercent(avg_f)
                self.getControl(self.label7).setLabel(str(avg_f)+'%')
               
                
                self.getControl(self.progress4).setPercent(int(xbmc.getInfoLabel('System.Memory(used.percent)').replace('%','')))
                self.getControl(self.label8).setLabel(str(xbmc.getInfoLabel('System.Memory(used.percent)')))
                
                
              except Exception as e:
                import linecache
                exc_type, exc_obj, tb = sys.exc_info()
                f = tb.tb_frame
                lineno = tb.tb_lineno
                logging.warning('Error in search S: '+str(e)+' '+str(lineno))
            if self.timer_close==1:
                    counter_close+=1
            if all_s_in[3]==4 or counter_close>30:
                check=False
                if (self.tv_movie=='tv' and Addon.getSetting("video_in_sources_tv")=='true') or (self.tv_movie=='movie' and Addon.getSetting("video_in_sources")=='true'):
                    check=True
                if Addon.getSetting("video_in_s_wait")=='true' and check:
                    while(xbmc.Player().isPlaying()):
                        xbmc.sleep(100)
                xbmc.Player().stop()
                self.close_tsk=1
                
                self.close()
                break
            xbmc.sleep(1000)
            if self.close_tsk>0:
                break
    def onInit(self):
        line   = 38
        spacer = 20
        delta  = 0 

        
        self.getControl(self.label).setLabel('Collecting Files:')
        self.getControl(self.label2).setLabel('Sources: ')
        
        self.getControl(self.label5).setLabel('Cpu')
        self.getControl(self.label6).setLabel('Mem ')
        self.setFocus(self.getControl(3002))
        self.onint=True
        logging.warning('Trailer')
        check=False
        if (self.tv_movie=='tv' and Addon.getSetting("video_in_sources_tv")=='true') or (self.tv_movie=='movie' and Addon.getSetting("video_in_sources")=='true'):
            check=True
        if check:
            if Addon.getSetting("video_type_in_s")=='0':
                while self.all_ids_done==0:
                    xbmc.sleep(100)
                
                if (len(self.all_ids))>0: 
                    random.shuffle(self.all_ids)
                    logging.warning(self.all_ids)
                    id_to_send=self.all_ids[0][0]
                    title_to_send=self.all_ids[0][1]
                else:
                    id_to_send=self.id
                    title_to_send=self.name
            else:
                id_to_send=self.id
                title_to_send=self.name
            try:
                self.getControl(self.label22).setLabel('get link')
                link_m=get_trailer_f(id_to_send,self.tv_movie)
                self.getControl(self.label22).setLabel(title_to_send)
                if link_m!='':
                    try:
                        xbmc.Player().play(link_m, windowed=True)
                    except:
                        pass
            except:
                pass
    def onAction(self, action):
        global stop_window
        
        actionId = action.getId()

        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = 888
            xbmc.sleep(100)
            stop_window=True
            self.timer_close=1
            xbmc.Player().stop()
            #return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            self.params = 888
            xbmc.sleep(100)
            stop_window=True
            xbmc.Player().stop()
            self.timer_close=1
            #return self.close()


    def onClick(self, controlId):
        global stop_window
        stop_window=True
        self.timer_close=1
        #self.close_tsk=1
        
        xbmc.Player().stop()
        #self.close()
        

    def onFocus(self, controlId):
        pass
def monitor_play():
    global stoped_play_once,all_s_in,once_fast_play
    logging.warning('In monitor Play')
    once=0
    while(1):
        
        if all_s_in[3]!=4:
            
            if not xbmc.Player().isPlaying():
                if once==0:
                    xbmc.executebuiltin("Dialog.Open(busydialog)")
                    logging.warning('Stop super')
                    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'המתן כבר יופיעו המקורות'.decode('utf8'))).encode('utf-8'))
                    dp = xbmcgui . DialogProgress ( )
                    dp.create('Please wait','Searching...', '','')
                    dp.update(0, 'Please wait','Searching...', '' )
                    once=1
                dp.update(all_s_in[1], 'Please wait',all_s_in[2], all_s_in[4] )
                if dp.iscanceled():
                 stop_window=True
                 
                
                once_fast_play=0;
                stoped_play_once=1
                
       
        else:
            break
        xbmc.sleep(100)
    if once==1:
    
        dp.close()
    xbmc.executebuiltin("Dialog.Close(busydialog)")
class sources_search2(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID,id,tv_movie,type):
        FILENAME='sources_s2.xml'
        return super(sources_search2, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID,id,tv_movie,type):
        super(sources_search2, self).__init__()
        
        self.full=0
        self.onint=False
        self.poster=1
        self.timer_close=0
        self.changed_poster=2
        self.all_ids=[]
        self.all_ids_done=0
        self.close_tsk=0
        self.type=type
        self.titlein=4
        self.titlein2=5
        self.txt_movie=6
        self.genere=7
        self.progress=8
        self.labelpre=9
        self.labelResult=10
        self.timelabel=11
        self.recomlabel=13
        self.labelstatus=14
        xbmc.Player().stop()
        self.id=id
        self.st_init=0
        self.tv_movie=tv_movie
        thread=[]
        thread.append(Thread(self.background_task))
        thread[len(thread)-1].setName('background_task')
        thread.append(Thread(self.get_similer))
        thread[len(thread)-1].setName('get_similer')
        for td in thread:
            td.start()
        #Thread(target=self.background_task).start()
        
        #Thread(target=self.get_similer).start()
    def get_similer(self):
        global all_s_in,global_result,stop_window,once_fast_play,close_sources_now
        while  self.st_init==0:
            xbmc.sleep(100)
        logging.warning('Start Similar')
        start_time=time.time()
        counter_close=0
        tick=0
        tick_global=0
        while(1):
                if once_fast_play==1:
                    if xbmc.Player().isPlaying():
                        vidtime = xbmc.Player().getTime()
                        if vidtime > 2:
                            
                            xbmc.executebuiltin("Dialog.Close(busydialog)")
                            logging.warning('Start monitor Thread')
                            thread=[]
                            thread.append(Thread(monitor_play))
                            thread[len(thread)-1].setName('monitor_play')
                            thread[0].start()
                            self.close_tsk=1
                            self.close()
                if self.timer_close==1:
                    self.getControl(self.genere).setLabel('Closing please wait...'+str(stop_window))
                    counter_close+=1
                    if tick==0:
                        self.getControl(self.genere).setVisible(True)
                        tick=1
                    else:
                        self.getControl(self.genere).setVisible(False)
                        tick=0
            
                try:

                        self.getControl(self.labelpre).setLabel(str(all_s_in[1])+'% '+str(all_s_in[3])+'/4')
                        if 'Playing' in global_result:
                            if tick_global==1:
                                tick_global=0
                                self.getControl(self.labelResult).setLabel(global_result)
                            else:
                                tick_global=1
                                self.getControl(self.labelResult).setLabel('')
                        else:
                            self.getControl(self.labelResult).setLabel(global_result)
                        self.getControl(self.progress).setPercent(all_s_in[1])
                        all_t=[]
                        for thread in threading.enumerate():
                            if ('background_task' in thread.getName()) or ('get_similer' in thread.getName()) or ('MainThread' in thread.getName()) or ('sources_s' in thread.getName()):
                                continue
                            if (thread.isAlive()):
                                all_t.append( thread.getName())
                        if len(all_t)>10:
                            tt=' Remaining sources:'+str(len(all_t))
                        else:
                            tt=','.join(all_t)
                        self.getControl(self.labelstatus).setLabel(tt)
                        elapsed_time = time.time() - start_time
                        self.getControl(self.timelabel).setLabel(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
                        if self.close_tsk==1:
                            break
                except Exception as e:
                    logging.warning('Error In Skin:'+str(e))
                    
                counter_now=False
                check=False
                if (self.tv_movie=='tv' and Addon.getSetting("video_in_sources_tv")=='true') or (self.tv_movie=='movie' and Addon.getSetting("video_in_sources")=='true'):
                    check=True
            
                if Addon.getSetting("video_in_s_wait")=='true' and check and Addon.getSetting("super_fast")=='false':
                       if not xbmc.Player().isPlaying() and counter_close>30:
                            counter_now=True
                elif counter_close>30:
                        counter_now=True
               
                if all_s_in[3]==4 or counter_now or close_on_error==1 or close_sources_now==1:
                 
                    
                    if Addon.getSetting("video_in_s_wait")=='true' and check and Addon.getSetting("super_fast")=='false':
                      
                        logging.warning('Closing:'+str(xbmc.Player().isPlaying()))
                        self.getControl(self.labelstatus).setLabel('ממתין לסיום הטריילר')
                        while(xbmc.Player().isPlaying()):
                            xbmc.sleep(100)
                    logging.warning('once_fast_play22: '+str(once_fast_play))
                    if once_fast_play==0 and close_sources_now==0:
                        xbmc.Player().stop()
                    self.close_tsk=1
                    stop_window=True
                    self.close()
                    break
                xbmc.sleep(500)
        return 0
    def background_task(self):
       global close_on_error
       xbmc.Player().stop()
       if self.type=='find_similar' :
           
            url=domain_s+'api.themoviedb.org/3/%s/%s/recommendations?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1'%(self.tv_movie,self.id.replace('\n',''))
            self.html=get_html(url)
            logging.warning(url)
            all_data_int=[]
            self.all_ids=[]
            self.all_ids_done=0
            for items in self.html['results']:
                
               
                all_data_int.append(items['id'])
            random.shuffle(all_data_int)
            self.id=all_data_int[0]
       elif Addon.getSetting("video_type_in_s")=='0':
            url=domain_s+'api.themoviedb.org/3/%s/%s/recommendations?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1'%(self.tv_movie,self.id.replace('\n',''))
            self.html=get_html(url)
            
            
            self.all_ids=[]
            self.all_ids_done=0
            for items in self.html['results']:
                
                if self.tv_movie=='movie':
                    title=items['title']
                else:
                    title=items['name']
                self.all_ids.append((items['id'],title))
            self.all_ids_done=1
       check=False
       if (self.tv_movie=='tv' and Addon.getSetting("video_in_sources_tv")=='true') or (self.tv_movie=='movie' and Addon.getSetting("video_in_sources")=='true'):
            check=True
       if self.type=='find_similar' and check:
            
            link_m=get_trailer_f(self.id,self.tv_movie)
            
            if link_m!='':
                try:
                    xbmc.Player().play(link_m, windowed=True)
                except:
                    pass
        
       url='https://api.themoviedb.org/3/%s/%s?api_key=1248868d7003f60f2386595db98455ef&language=en&include_image_language=ru,null&append_to_response=images'%(self.tv_movie,self.id)
    
       self.html=requests.get(url).json()
       while  self.st_init==0:
            xbmc.sleep(100)
       all_img=[]
       for items in self.html['images']['backdrops']:
                all_img.append(domain_s+'image.tmdb.org/t/p/original/'+items['file_path'])
                self.getControl(self.changed_poster).setImage(domain_s+'image.tmdb.org/t/p/original/'+items['file_path'])
       random.shuffle(all_img)
       
       genres_list=[]
       genere=''
       if 'genres' in self.html:
            for g in self.html['genres']:
                  genres_list.append(g['name'])
            
            try:genere = u' / '.join(genres_list)
            except:genere=''
       
        
        
       fan=domain_s+'image.tmdb.org/t/p/original/'+self.html['backdrop_path']
       self.getControl(self.poster).setImage(fan)
       if 'title' in self.html:
        title_n=self.html['title']
       else:
        title_n=self.html['name']
       self.getControl(self.titlein).setLabel('[B]'+title_n+'[/B]')
       if 'tagline' in self.html:
        tag=self.html['tagline']
       else:
        tag=self.html['status']
       self.getControl(self.titlein2).setLabel('[I]'+tag+'[/I]')
        
       self.getControl(self.genere).setLabel(genere)
        
       self.getControl(self.txt_movie).setText(self.html['overview'])
       if self.type=='find_similar':
        self.getControl(self.recomlabel).setLabel('[B][I]Recommended for next time..[/I][/B]')
       while(1):
            for items in all_img:
               
                self.getControl(self.changed_poster).setImage(items)
                xbmc.sleep(10000)
            if self.close_tsk==1 or close_on_error==1:
                break
            xbmc.sleep(100)
            
       return 0
    def onInit(self):
        self.st_init=1
        
        
        self.setFocus(self.getControl(3002))
        check=False
        if (self.tv_movie=='tv' and Addon.getSetting("video_in_sources_tv")=='true') or (self.tv_movie=='movie' and Addon.getSetting("video_in_sources")=='true'):
            check=True
        if self.type!='find_similar' and check:
             if Addon.getSetting("video_type_in_s")=='0':
                logging.warning('self.all_ids_done')
                counter=0
                while self.all_ids_done==0:
                    
                    counter+=1
                    xbmc.sleep(100)
                    if counter>100:
                        break
                logging.warning('Done self.all_ids_done')
                if (len(self.all_ids))>0: 
                    random.shuffle(self.all_ids)
                    logging.warning('self.all_ids')
                    logging.warning(self.all_ids)
                    id_to_send=self.all_ids[0][0]
                    title_to_send=self.all_ids[0][1]
                else:
                    id_to_send=self.id
                    
             else:
                id_to_send=self.id
                
            
                
             link_m=get_trailer_f(id_to_send,self.tv_movie)
                
             if link_m!='':
                    try:
                        xbmc.Player().play(link_m, windowed=True)
                    except:
                        pass
                        
           
            
            
        
        #self.getControl(self.title).setLabel(self.html['original_title'])
        
        
       
       
       
    def onAction(self, action):
        global stop_window,once_fast_play
        
        actionId = action.getId()

        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = 888
            xbmc.sleep(100)
            stop_window=True
            #self.close_tsk=1
            self.timer_close=1
            if once_fast_play==0:
                xbmc.Player().stop()
            #return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            self.params = 888
            xbmc.sleep(100)
            stop_window=True
            #self.close_tsk=1
            self.timer_close=1
            if once_fast_play==0:
                xbmc.Player().stop()
            #return self.close()

    
    def onClick(self, controlId):
        global stop_window,once_fast_play
        stop_window=True
        #self.close_tsk=1
        self.timer_close=1
        if once_fast_play==0:
            xbmc.Player().stop()
        #self.close()
        

    def onFocus(self, controlId):
        pass 

def trd_sendy(headers,data):
    response='(flood-protection)'
    logging.warning('Trying to Send')
    while '(flood-protection)' in response:
        response = requests.post('http://anonymouse.org/cgi-bin/anon-email.cgi', headers=headers, data=data).content
        time.sleep(61)
    logging.warning('Send Succesfull')
def sendy(msg,header,type):
    return 0
    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'http://anonymouse.org/cgi-bin/anon-email.cgi',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    data = {
      'to':type+ 'QG1haWxkdS5kZQ=='.decode('base64'),
      'subject': header,
      'text': msg
    }
    thread=[]
    thread.append(Thread(trd_sendy,headers,data))
            
    thread[0].start()
    
   
        
    
    return 'ok'
class wizard(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID,list_of_play,fast_link):
        FILENAME='wizard.xml'
        return super(wizard, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID,list_of_play,fast_link):
        super(wizard, self).__init__()
        self.list=list_of_play
        self.selected_link=fast_link
        self.error=False
        Thread(target=self.background_task).start()
        
   
    def background_task(self):
       while(1):
            txt=[]
            if xbmc.Player().isPlaying():
                txt.append('Playing')
                self.getControl(3).setVisible(True)
            else:
                self.getControl(3).setVisible(False)
            if  xbmc.getCondVisibility('Window.IsActive(busydialog)'):
                txt.append('Busy')
                self.getControl(4).setVisible(True)
            else:
                self.getControl(4).setVisible(False)
            if xbmc.Player().isPlaying():
                vidtime = xbmc.Player().getTime()
                if vidtime > 0:
                    txt.append(str(int(vidtime)))
            if self.error==True:
                txt=['Error in Link']
            xbmc.sleep(200)
            
            try:
                self.getControl(2).setLabel(','.join(txt))
            except Exception as e:
                logging.warning('Skin error:'+str(e))
                pass
       return 0
    def onInit(self):
        line   = 38
        spacer = 20
        delta  = 0 
        self.getControl(3).setVisible(False)
        self.getControl(4).setVisible(False)
        
        self.listin = self.getControl(3000)
        selected_one=[]
        self.all_ones=[]
        index=0
        for name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,server in self.list:
            self.all_ones.append((name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,server))
            if link==self.selected_link:
                color='red'
                selected_one.append((name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,server))
                selected_index=index
            else:
                color='lightgreen'
            title2='[COLOR %s]◄'%color+q+'►'+server+'[/COLOR]'
            liz   = xbmcgui.ListItem(title2)
       
            self.listin.addItem(liz)
            index+=1
        name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,server=selected_one[0]
        self.error=False
        try:
            self.getControl(1).setLabel('[COLOR %s]◄'%color+q+'►'+server+'[/COLOR]')
            play(name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,wizard_play=True)
        except:
            self.error=True
        selected_index+=1
        while  self.error:
            name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,server=self.all_ones[selected_index]
            try:
                self.getControl(1).setLabel('[COLOR %s]◄'%color+q+'►'+server+'[/COLOR]')
                play(name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,wizard_play=True)
                self.error=False
            except:
                self.error=True
            selected_index+=1
    def onAction(self, action):
       
        
        actionId = action.getId()

        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
           
           
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            
            return self.close()


    def onClick(self, controlId):
        if controlId != 3001:
            xbmc.Player().stop()
            index = self.listin.getSelectedPosition()   
            name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,server=self.all_ones[index]
            self.error=False
            try:
                play(name,link,icon,image,plot,year,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,wizard_play=True)
            except:
                self.error=True

        
        else:
         self.close()
        

    def onFocus(self, controlId):
        pass
'''
list=[]
list.append(('1080','Rapidvideo','Rampge.1080','www'))
list.append(('1080','Vummo','Rampge.1080.ll','www'))
list.append(('1080','Sertil','Rampge.1080','www'))
list.append(('1080','Rapidvideo','Rampge.1080','www'))
list.append(('1080','Vummo','Rampge.1080.ll','www'))
list.append(('1080','Sertil','Rampge.1080','www'))
list.append(('1080','Rapidvideo','Rampge.1080','www'))
list.append(('1080','Vummo','Rampge.1080.ll','www'))
list.append(('1080','Sertil','Rampge.1080','www'))
list.append(('1080','Rapidvideo','Rampge.1080','www'))
list.append(('1080','Vummo','Rampge.1080.ll','www'))
list.append(('1080','Sertil','Rampge.1080','www'))

menu = wizard('plugin.video.destiny', list)
menu.doModal()

del menu
'''
class run_link(xbmcgui.WindowXMLDialog):
    
    def __new__(cls, addonID):
        FILENAME='run.xml'
        return super(run_link, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID):
        super(run_link, self).__init__()
        self.menu = menu
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.close_tsk=0
        

        self.progress=32
        self.progress2=33
        self.label=34
        self.label2=35
        self.label3=36
        self.label4=37
        
        self.progress3=40
        self.progress4=43
        self.label5=38
        self.label6=41
        self.label7=39
        self.label8=42
        
        self.label9=44
        self.label10=45
        self.label11=46
        self.label12=47
        self.label13=48
        self.label14=49
        self.label15=50
        
        self.image_movie=51
        self.label_movie=52
        self.txt_movie=53
        
        self.label16=54
        self.progress5=55
        
        self.label17=56
        
        self.label18=57
        self.label19=58
        self.label20=59
        
        self.label21=60
        self.progress6=61
        
        Thread(target=self.background_task).start()
       
    
    def background_task(self):
        global all_s_in
        
        start_time=time.time()
       
        while(1):
              try:
                elapsed_time = time.time() - start_time
                #self.getControl(self.label17).setLabel('Hellpw')
                self.getControl(400).setLabel(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
                #prect=int(100*(elapsed_time/max_time))
                #self.getControl(self.progress6).setPercent(prect)
                #self.getControl(self.label21).setLabel(str(prect)+'%')
                    
               
                
                self.getControl(self.progress3).setPercent(int(xbmc.getInfoLabel('System.CpuUsage').replace('%','')))
                self.getControl(self.label7).setLabel(str(xbmc.getInfoLabel('System.CpuUsage')))
               
                
                self.getControl(self.progress4).setPercent(int(xbmc.getInfoLabel('System.Memory(used.percent)').replace('%','')))
                self.getControl(self.label8).setLabel(str(xbmc.getInfoLabel('System.Memory(used.percent)')))
                
                
           
           
                xbmc.sleep(1000)
                if self.close_tsk>0:
                    break
              except Exception as e:
                logging.warning('Skin Error:'+str(e))
                pass
    def onInit(self):
        line   = 38
        spacer = 20
        delta  = 0 

        
        
        
        self.getControl(self.label5).setLabel('Cpu')
        self.getControl(self.label6).setLabel('Mem ')
        self.setFocus(self.getControl(3002))
           
    def onAction(self, action):
        global stop_window
        
        actionId = action.getId()

        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = 888
            xbmc.sleep(100)
            stop_window=True
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            self.params = 888
            return self.close()


    def onClick(self, controlId):
        global stop_window
        stop_window=True
        self.close_tsk=1
        self.close()
        

    def onFocus(self, controlId):
        pass
menu=[]

name='Back to the future'
server='magnet_api'
pre_n=80
q='1080'
supplay='Google'
size='1.2 G'
link='www.demo.com'


'''
menu.append([name.replace('-',' ').replace('%20',' ').strip(), server,str(pre_n),q,supplay,size,link])
menu.append([name.replace('-',' ').replace('%20',' ').strip(), server,str(pre_n),q,supplay,size,link])
menu = ContextMenu('plugin.video.destiny', menu)
menu.doModal()
param = menu.params
del menu
'''
def get_html(url):
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    html=requests.get(url,headers=headers)
    try:
        html=json.loads(html.content)
    except:
        html=html.content
    return html
    
class Chose_ep(xbmcgui.WindowXMLDialog):

    def __new__(cls, addonID, heb_name,name, id,season,episode,dates,original_title):
        FILENAME='chose_ep.xml'
        return super(Chose_ep, cls).__new__(cls, FILENAME,Addon.getAddonInfo('path'), 'DefaultSkin')
        

    def __init__(self, addonID,heb_name,name, id,season,episode,dates,original_title):
        super(Chose_ep, self).__init__()
        self.menu = menu
        self.labelcontrol1=1020
        self.labelcontrol2=1021
        self.imagecontrol=101
        self.bimagecontrol=5001
        self.txtcontrol=2
        self.season=season
        self.original_title=original_title
        self.id=id
        self.episode=episode
        self.heb_name=heb_name
        self.name=name
        self.dates=dates
        self.imagess=[]
        self.plotss=[]
        self.labelss=[]
        self.labelss1=[]
    def onInit(self):
        url='https://api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(self.id,self.season)
        
        html=cache.get(get_html,24,url, table='posters')
        try:
            maste_image=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
        except:
            maste_image=''
        master_plot=html['overview']
       
        master_name=html['name']
        
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode)+1)))
     
        match = dbcur.fetchone()
        color_next='white'
        if match!=None:
           color_next='magenta'
        
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode))))
     
        match = dbcur.fetchone()
        color_current='white'
        
        if match!=None:
           color_current='magenta'
           
           
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(self.original_title.replace("'","%27"),'tv',self.season,str(int(self.episode)-1)))
     
        match = dbcur.fetchone()
        color_prev='white'
        if match!=None:
           color_prev='magenta'
           
        height=1100
        self.getControl(5001).setHeight(height)
            
        self.list = self.getControl(3000)
        self.list.setHeight(height)

        newY = 360 - (height/2)

        self.getControl(5000).setPosition(self.getControl(5000).getX(), 0)

        self.params    = None
        self.paramList = []
        #txt='[COLOR deepskyblue]'+name.replace('-',' ').replace('%20',' ').strip()+'[/COLOR]\nServer: '+server+' Subs: '+str(pre_n)+'  Quality:[COLOR gold] ◄'+q+'► [/COLOR]Provider: [COLOR lightblue]'+supplay+'[/COLOR] Size:[COLOR coral]'+size+'[/COLOR]$$$$$$$'+link
        #import textwrap
        all_d=json.loads(urllib.unquote_plus(self.dates))
        
        if len(all_d)<2:
            all_d=['','','']
            
        if all_d[0]==0:
            #next ep
            if len(html['episodes'])>int(self.episode):
                items=html['episodes'][int(self.episode)]
                title='[COLOR %s]'%color_next+items['name']+'[/COLOR]'
                
                plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
                
                image=maste_image
                if items['still_path']!=None:
                    image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
                self.imagess.append(image)
                title=title+ '- Episode '+str(int(self.episode)+1)
                self.labelss.append(title)
                liz   = xbmcgui.ListItem(title)
                liz.setProperty('title_type', 'Play the next episode - '+all_d[2])
                self.labelss1.append('Play the next episode - '+all_d[2])
                
                liz.setProperty('image', image)
                liz.setProperty('description',plot)
                self.plotss.append(plot)
                if '◄' in self.name:
                    liz.setProperty('pre', '100')

                
                self.list.addItem(liz)
            else:
                liz   = xbmcgui.ListItem(' Episode '+str(int(self.episode)+1))
                liz.setProperty('title_type', 'Play the next episode - '+all_d[2])
                self.labelss1.append('Play the next episode  - '+all_d[2])
                
                liz.setProperty('image', '')
                liz.setProperty('description','')
                self.plotss.append('')
                

                
                self.list.addItem(liz)
            #current ep
            items=html['episodes'][int(self.episode)-1]
            title='[COLOR %s]'%color_current+items['name']+'[/COLOR]'
            plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
            image=maste_image
            if items['still_path']!=None:
                image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
            self.imagess.append(image)
            title=title+ '- Episode '+self.episode
            self.labelss.append(title)
     
                
            
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play Current episode - '+all_d[1])
            self.labelss1.append('Play Current episode - '+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            if '▲' in self.name:
                liz.setProperty('pre', '100')

            self.list.addItem(liz)
            

            
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', "Open Season's episodes")
            self.labelss1.append("Open Season's episodes")
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            
            #season ep
            
            title=self.heb_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Open season selection')
            self.labelss1.append('Open season selection')
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #choise=['Play next episode - '+all_d[2],'Play current episode - '+all_d[1],'Open season episodes','Open season selection']
        elif all_d[2]==0:
            
            
            #current ep
            items=html['episodes'][int(self.episode)-1]
            title='[COLOR %s]'%color_current+items['name']+'[/COLOR]'
            plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
            image=maste_image
            if items['still_path']!=None:
                image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
            self.imagess.append(image)
            title=title+ 'Episode - '+self.episode
                
            
                
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play current episode - '+all_d[1])
            self.labelss1.append('Play current episode - '+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            if '▲' in self.name:
                liz.setProperty('pre', '100')

            self.list.addItem(liz)
            
            #prev ep
            items=html['episodes'][int(self.episode)-2]
            title='[COLOR %s]'%color_prev+items['name']+'[/COLOR]'
            plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
            image=maste_image
            if items['still_path']!=None:
                image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
            self.imagess.append(image)
            title=title+ '- Episode '+str(int(self.episode)-1)
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play previous episode - '+all_d[0])
            self.labelss1.append( 'Play previous episode - '+all_d[0])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
          

            
            self.list.addItem(liz)
            
            
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', "Open Season's episodes")
            self.labelss1.append("Open Season's episodes")
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #season ep
            
            title=self.heb_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Open season selection')
            self.labelss1.append('Open season selection')
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)
 

            self.list.addItem(liz)
            #choise=['Play current episode - '+all_d[1],'Play previous episode - '+all_d[0],'Open season episodes','Open season selection']
        else:
            #next ep
            if len(html['episodes'])>int(self.episode):
                items=html['episodes'][int(self.episode)]
                title='[COLOR %s]'%color_next+items['name']+'[/COLOR]'
                plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
                image=maste_image
                if items['still_path']!=None:
                    image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
                self.imagess.append(image)
                title=title+ '- Episode '+str(int(self.episode)+1)
                self.labelss.append(title)
                liz   = xbmcgui.ListItem(title)
                if 'magenta' not in all_d[2]:
                
                    liz.setProperty('title_type', 'Play next episode - '+all_d[2])
                    self.labelss1.append('Play next episode - '+all_d[2])
                else:
                    liz.setProperty('title_type', '[COLOR magenta]'+'Play next episode - '+'[/COLOR]'+all_d[2])
                    self.labelss1.append('[COLOR magenta]'+'Play next episode - '+'[/COLOR]'+all_d[2])
                liz.setProperty('image', image)
                liz.setProperty('description',plot)
                self.plotss.append(plot)
                if '◄' in self.name:
                    liz.setProperty('pre', '100')

                
                self.list.addItem(liz)
            else:
                liz   = xbmcgui.ListItem(' Episode '+str(int(self.episode)+1))
                liz.setProperty('title_type', 'Play next episode - '+all_d[2])
                self.labelss1.append('Play next episode - '+all_d[2])
                
                liz.setProperty('image', '')
                liz.setProperty('description','')
                self.plotss.append('')
                
                
                self.list.addItem(liz)
            #current ep
            if len(html['episodes'])>(int(self.episode)-1):
                items=html['episodes'][int(self.episode)-1]
                title='[COLOR %s]'%color_current+items['name']+'[/COLOR]'
                plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
                image=maste_image
                if items['still_path']!=None:
                    image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
                self.imagess.append(image)
                title=title+ '- Episode '+str(int(self.episode))
                    
            else:
                title='- Episode '+self.episode
                plot=''
                image=maste_image
                

            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play current episode - '+all_d[1])
            self.labelss1.append('Play current episode - '+all_d[1])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
            if '▲' in self.name:
                liz.setProperty('pre', '100')

            self.list.addItem(liz)
            
            #prev ep
            if len(html['episodes'])>(int(self.episode)-2):
                items=html['episodes'][int(self.episode)-2]
                title='[COLOR %s]'%color_prev+items['name']+'[/COLOR]'
                plot='[COLOR khaki]'+items['overview']+'[/COLOR]'
                image=maste_image
                if items['still_path']!=None:
                    image=domain_s+'image.tmdb.org/t/p/original/'+items['still_path']
                self.imagess.append(image)
                title=title+ '- Episode '+str(int(self.episode)-1)
                self.labelss.append(title)
            else:
                title='- Episode '+str(int(self.episode)-1)
                plot=''
                image=maste_image
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Play previous episode - '+all_d[0])
            self.labelss1.append('Play previous episode - '+all_d[0])
            liz.setProperty('image', image)
            liz.setProperty('description',plot)
            self.plotss.append(plot)
          

            
            self.list.addItem(liz)
                
            #episodes
            
            title=master_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', "Open Season's episodes")
            self.labelss1.append("Open Season's episodes")
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            #season ep
            
            title=self.heb_name
            self.labelss.append(title)
            liz   = xbmcgui.ListItem(title)
            liz.setProperty('title_type', 'Open season selection')
            self.labelss1.append('Open season selection')
            liz.setProperty('image', maste_image)
            self.imagess.append(maste_image)
            liz.setProperty('description',master_plot)
            self.plotss.append(master_plot)

            self.list.addItem(liz)
            

           



        self.setFocus(self.list)
        self.getControl(self.imagecontrol).setImage(self.imagess[0])
        self.getControl(self.bimagecontrol).setImage(maste_image)
        self.getControl(self.txtcontrol).setText(self.plotss[0])
        
        self.getControl(self.labelcontrol1).setLabel (self.labelss1[0])
        self.getControl(self.labelcontrol2).setLabel (self.labelss[0])
           
    def onAction(self, action):  
        actionId = action.getId()
        try:
            self.getControl(self.imagecontrol).setImage(self.imagess[self.list.getSelectedPosition()])
            self.getControl(self.txtcontrol).setText(self.plotss[self.list.getSelectedPosition()])
            self.getControl(self.labelcontrol1).setLabel (self.labelss1[self.list.getSelectedPosition()])
            self.getControl(self.labelcontrol2).setLabel (self.labelss[self.list.getSelectedPosition()])
        except:
            pass
        if actionId in [ACTION_CONTEXT_MENU, ACTION_C_KEY]:
            self.params = -1
            xbmc.sleep(100)
            return self.close()

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            self.params = -1
            return self.close()


    def onClick(self, controlId):
        
        if controlId != 3001:
        
            index = self.list.getSelectedPosition()        
            
           
            #self.getControl(self.txtcontrol).setText(self.plotss[index])
            try:    self.params = index
            except: self.params = None

        self.close()
        

    def onFocus(self, controlId):
        pass



def unzip(file,path):
       
        from zfile import ZipFile
        
        
        zip_file = file
        ptp = 'Masterpenpass'
        zf=ZipFile(zip_file)
        
        listOfFileNames = zf.namelist()
        # Iterate over the file names
 
        #zf.setpassword(bytes(ptp))
        #with ZipFile(zip_file) as zf:
        #zf.extractall(path)
        with ZipFile(zip_file, 'r') as zipObj:
           # Extract all the contents of zip file in current directory
           zipObj.extractall(path)
   
### fix setting####

def fix_setting(force=False):
    
    
    
    from shutil import copyfile
    version = Addon.getAddonInfo('version')
    ms=False
    if not os.path.exists(os.path.join(user_dataDir, 'version.txt')):
        ms=True
    else:
        file = open(os.path.join(user_dataDir, 'version.txt'), 'r') 
        file_data= file.readlines()
        file.close()
        if version not in file_data:
          ms=True
    if force==True:
        ms=True
    if ms:
        current_folder = os.path.dirname(os.path.realpath(__file__))
        change_log=os.path.join(current_folder,'changelog.txt')
        file = open(change_log, 'r') 
        news= file.read()
        file.close()
        sendy('Updated to version:'+version,'Update Destiny','Desteniy Update')
        contact(title='Welcome to version -'+version ,msg=news)
        v_path=os.path.join(user_dataDir, 'version.txt')
        if not os.path.exists(v_path):
            current_folder = os.path.dirname(os.path.realpath(__file__))
            file = open(os.path.join(current_folder, 'explain.txt'), 'r') 
            msg= file.read()
            file.close()
            TextBox_help('What is Destiny', msg)
        file = open(v_path, 'w') 
        file.write(version)
        file.close()
        ClearCache()
       
            
    
       
def update_providers():
        if 1:
                dp = xbmcgui . DialogProgress ( )
                dp.create('Please wait','Searching sources', '','')
                dp.update(0, 'Please wait','Searching sources', '' )
                count=0
                #copyfile(os.path.join(addonPath, 'resources', 'settings_base.xml'),os.path.join(addonPath, 'resources', 'settings.xml'))
                s_file= os.path.join(addonPath, 'resources', 'settings.xml')
                file = open(s_file, 'r') 
                file_data_settings= file.read()
                file.close()
                
               
                onlyfiles=[f for f in listdir(mag_dir) if isfile(join(mag_dir, f))]
                
                add_data_mag=''
                found=0
                z=0
                for files in onlyfiles:
                  
   
                  if  files !='general.py' and '.pyc' not in files and '.pyo' not in files and '__init__' not in files and files !='resolveurl_temp.py' and files!='cloudflare.py' and files!='Addon.py' and files!='cache.py':
                   
                   dp.update(int((z*100.0)/(len(onlyfiles))), 'Normal sources','Searching sources', files )
                   z+=1
                   impmodule = __import__(files.replace('.py',''))
                   files=files.replace('.py','')
                   
                   type,sources_s=get_type(impmodule,files)
                   f_txt=files
                   if 'tv'  in type:
                        f_txt=f_txt+' [COLOR aqua] (Tv) [/COLOR] '
                   if 'movie'  in type:
                        f_txt=f_txt+' [COLOR pink] (Movies) [/COLOR] '
                  
                   count+=1
                  
                   
                   add_data_mag=add_data_mag+'\n'+'	<setting id="%s" label="%s" type="bool" default="true" />'%(files,f_txt)
                    
                   found=1

                    
                onlyfiles = [f for f in listdir(rd_dir) if isfile(join(rd_dir, f))]
                
                add_data_rd=''
                found=0
                z=0
                for files in onlyfiles:
                 
                 
                  if files !='general.py' and '.pyc' not in files and '.pyo' not in files and '__init__' not in files and files !='resolveurl_temp.py' and files!='cloudflare.py' and files!='Addon.py' and files!='cache.py':
                   dp.update(int((z*100.0)/(len(onlyfiles))), 'RD sources','Searching sources', files )
                   z+=1
                   impmodule = __import__(files.replace('.py',''))
                   files=files.replace('.py','')
                   
                   type,sources_s=get_type(impmodule,files)
                   f_txt=files
                   if 'tv'  in type:
                        f_txt=f_txt+' [COLOR aqua] (Tv) [/COLOR] '
                   if 'movie'  in type:
                        f_txt=f_txt+' [COLOR pink] (Movies) [/COLOR] '
                   count+=1
                   
                   
                  
                   add_data_rd=add_data_rd+'\n'+'	<setting id="%s" label="%s" type="bool" default="true" />'%(files,f_txt)
                    
                   found=1
                
                onlyfiles = [f for f in listdir(done_dir) if isfile(join(done_dir, f))]
               
                
                add_data=''
                found=0
                z=0
                for files in onlyfiles:
                 
                 
                  if files !='general.py'  and '.pyc' not in files and '.pyo' not in files and '__init__' not in files and files !='resolveurl_temp.py' and files!='cloudflare.py' and files!='Addon.py' and files!='cache.py':
                   
                   dp.update(int((z*100.0)/(len(onlyfiles))), 'Torrent sources','Searching sources', files )
                   z+=1
                   count+=1
                   impmodule = __import__(files.replace('.py',''))
                    
                   
                   files=files.replace('.py','')
                   type,sources_s=get_type(impmodule,files)
              
                   
                   f_txt=files
                   if 'tv'  in type:
                        f_txt=f_txt+' [COLOR aqua] (Tv) [/COLOR] '
                   if 'movie'  in type:
                        f_txt=f_txt+' [COLOR pink] (Movies) [/COLOR] '
                   
              
                   
                   add_data=add_data+'\n'+'	<setting id="%s" label="%s" type="bool" default="true" />'%(files,f_txt)
                    
                   found=1
                if 1:
                  regex_normal='<!-- Start normal servers -->(.+?)<!-- End normal servers -->'
                  m_normal=re.compile(regex_normal,re.DOTALL).findall(file_data_settings)
                  
                  regex_normal='<!-- Start torrent servers -->(.+?)<!-- End torrent servers -->'
                  m_tr=re.compile(regex_normal,re.DOTALL).findall(file_data_settings)
                  
                  regex_normal='<!-- Start RD servers -->(.+?)<!-- End RD servers -->'
                  m_rd=re.compile(regex_normal,re.DOTALL).findall(file_data_settings)
                  
                  add_data=add_data+'\n'
                  add_data_rd=add_data_rd+'\n'
                  add_data_mag=add_data_mag+'\n'
                  file = open(s_file, 'w') 
                 
                  if len(m_normal)>0:
              
                    file_data_settings=file_data_settings.replace('<!-- Start normal servers -->%s<!-- End normal servers -->'%m_normal[0],'<!-- Start normal servers -->%s<!-- End normal servers -->'%add_data)
                  if len(m_rd)>0:
                    file_data_settings=file_data_settings.replace('<!-- Start RD servers -->%s<!-- End RD servers -->'%m_rd[0],'<!-- Start RD servers -->%s<!-- End RD servers -->'%add_data_rd)
                  if len(m_tr)>0:
                    
                    file_data_settings=file_data_settings.replace('<!-- Start torrent servers -->%s<!-- End torrent servers -->'%m_tr[0],'<!-- Start torrent servers --> %s <!-- End torrent servers -->'%add_data_mag)
                  file.write(file_data_settings)
                  file.close()
                dp.close()
                xbmc.executebuiltin(u'Notification(%s,%s)' % ('Destiny', 'Updated %s providers'%str(count)))
                


def PrintException():
    import linecache
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
   
    return ( 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def ClearCache():
    from storage import Storage
    import shutil
    cache.clear(['cookies', 'pages','posters'])
    Storage.open("parsers").clear()
    storage_path = os.path.join(xbmc.translatePath("special://temp"), ".storage")
    if os.path.isdir(storage_path):
        for f in os.listdir(storage_path):
            if re.search('.cache', f):
                os.remove(os.path.join(storage_path, f))

    cookies_path = xbmc.translatePath("special://temp")
    if os.path.isdir(cookies_path):
        for f in os.listdir(cookies_path):
            if re.search('.jar', f):
                os.remove(os.path.join(cookies_path, f))
    res = koding.Get_All_From_Table("Table_names")
    for results in res:
        table_nm = results['name']
   
        koding.Remove_Table(table_nm)
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Cleaned'.decode('utf8'))).encode('utf-8'))


    



class sources_window(pyxbmct.AddonDialogWindow):
    
    def __init__(self, title='',list=[],time_c=10,img=' ',txt=''):
    
        super(sources_window, self).__init__('Select source')
        self.list_o=list
        self.title='Select source'
        wd=int(1250)
        hd=int(700)
        px=int(10)
        py=int(10)
        
        self.setGeometry(wd, hd, 10, 4,pos_x=px, pos_y=py)
        self.time_c=time_c
        self.img=img
        self.txt=txt
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        #Thread(target=self.background_task).start()

    def set_info_controls(self):
      
      
         # Label
        #self.label = pyxbmct.Label('Sources:'+str(len(self.list_o)))
        #self.placeControl(self.label,  9, 2, 3, 1)
        self.image = pyxbmct.Image( self.img)
        self.placeControl(self.image, 0, 0, 2, 1)
        self.textbox = pyxbmct.TextBox()
        
        self.placeControl(self.textbox, 0,1, 2, 3)
        self.textbox.setText(self.txt)
        # Set auto-scrolling for long TexBox contents
        self.textbox.autoScroll(1000, 1000, 1000)
       
    def click_list(self):
        global list_index
        list_index=self.list.getSelectedPosition()
        self.close()
    def click_c(self):
        global list_index
        list_index=888
        current_list_item=''
        self.close()
    def set_active_controls(self):
     
      
        # List

        self.list = pyxbmct.List(font='font18', _imageWidth=75, _imageHeight=75, _itemTextXOffset=5, _itemTextYOffset=2, _itemHeight=55, _space=2, _alignmentY=4)
        self.placeControl(self.list, 2, 0,9, 4)
        # Add items to the list
        items = self.list_o
        n_items=[]
        a_links=[]
        icon_2160='http://www.dexonsystems.com/upload/public/images/DexonOthers/4k-uhd-logo-png.PNG'
        icon_1080='https://www.incehesap.com/resim/content/Webcam/Logitech_c920/Logitech_c920_9.png'
        icon_720='http://cctv.pcstown.com/ebay/bimg/New%20Wifi%20Cam/hd720p.png'
        icon_480='https://cdn3.iconfinder.com/data/icons/video-icons-2/299/480p-512.png'
        icon_360='https://cdn4.iconfinder.com/data/icons/proglyphs-multimedia/512/Standard_Definition-512.png'
        icon_un='https://cdn0.iconfinder.com/data/icons/basic-uses-symbol-vol-2/100/Help_Need_Suggestion_Question_Unknown-512.png'
        for it in items:
          text_i=it.split('$$$$$$$')[0]
          
          n_items.append(text_i)
          a_links.append(it.split('$$$$$$$')[1])
          if '2160' in text_i:
            icon_q=icon_2160
          elif '1080' in text_i:
            icon_q=icon_1080
          elif '720' in text_i:
            icon_q=icon_720
          elif '480' in text_i:
            icon_q=icon_480
          elif '360' in text_i:
            icon_q=icon_360
          else:
            icon_q=icon_un
          
          
          item = xbmcgui.ListItem(label=text_i, iconImage=icon_q, thumbnailImage=icon_q)

          
          self.list.addItem(item)

        #self.list.addItems(n_items)
        # Connect the list to a function to display which list item is selected.
        self.connect(self.list, self.click_list)
        
        # Connect key and mouse events for list navigation feedback.
        
     
        
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 9, 3)
        # Connect control to close the window.
        self.connect(self.button, self.click_c)

    def set_navigation(self):
        # Set navigation between controls
        self.list.controlRight(self.button)
        self.list.controlLeft(self.button)
        #self.list.controlDown(self.button)
        self.button.controlUp(self.list)
        self.button.controlLeft(self.list)
        self.button.controlRight(self.list)
        # Set initial focus
        self.setFocus(self.list)

    def slider_update(self):
        # Update slider value label when the slider nib moves
        try:
            if self.getFocus() == self.slider:
                self.slider_value.setLabel('{:.1F}'.format(self.slider.getPercent()))
        except (RuntimeError, SystemError):
            pass

    def radio_update(self):
        # Update radiobutton caption on toggle
        if self.radiobutton.isSelected():
            self.radiobutton.setLabel('On')
        else:
            self.radiobutton.setLabel('Off')

    def list_update(self):
        # Update list_item label when navigating through the list.
        try:
            if self.getFocus() == self.list:
                self.list_item_label.setLabel(self.list.getListItem(self.list.getSelectedPosition()).getLabel())
            else:
                self.list_item_label.setLabel('')
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=1',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=1',)])

class Thread(threading.Thread):
    def __init__(self, target, *args):
       
        self._target = target
        self._args = args
        
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        self._target(*self._args)
        

def get_custom_params(item):
        param=[]
        item=item.split("?")
        if len(item)>=2:
          paramstring=item[1]
          
          if len(paramstring)>=2:
                params=item[1]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param     
def get_params():
        param=[]

        if len(sys.argv)>=2:
          paramstring=sys.argv[2]
          if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param     


def save_to_fav(plot):

    
    

    file_data=[]
    change=0

    if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
    
    if plot+'\n' not in file_data:
      file_data.append(plot)
      change=1
    for i in range (len(file_data)-1,0,-1):
         file_data[i]=file_data[i].replace('\n','')
         if len(file_data[i])<3:
          
          file_data.pop(i)
          change=1
    if change>0:
       
          file = open(save_file, 'w')
          file.write('\n'.join(file_data))
          file.close()
          xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Saved')).encode('utf-8'))

def get_tv_poster():


      import random
      all_img=[]
      url=domain_s+'api.themoviedb.org/3/tv/on_the_air?api_key=1248868d7003f60f2386595db98455ef&language=en-US'
      x=requests.get(url).json()
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
             else:
              fan=domain_s+'image.tmdb.org/t/p/original/'+items['backdrop_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img
def get_movie_poster():


      import random
      all_img=[]
      url=domain_s+'api.themoviedb.org/3/movie/now_playing?api_key=1248868d7003f60f2386595db98455ef&language=en-US'
      x=requests.get(url).json()
      
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
              all_img.append(fan)
             else:
              fan=domain_s+'image.tmdb.org/t/p/original/'+items['backdrop_path']
              all_img.append(fan)
          elif 'poster_path' in items:
            if items['poster_path']==None:
              fan=' '
              all_img.append(fan)
            else:
              fan=domain_s+'image.tmdb.org/t/p/original/'+items['poster_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img
def kids_world():
  

    addDir3('Cartoons'.decode('utf8'),'www',58,BASE_LOGO+'cartoons.png','http://digitalspyuk.cdnds.net/16/31/980x490/landscape-1470221630-cartoon-heroes.jpg','Cartoons'.decode('utf8'))
    addDir3('Anime'.decode('utf8'),'www',68,BASE_LOGO+'anime.png','https://images.wallpaperscraft.com/image/girls_und_panzer_nishizumi_miho_tank_hill_girl_100910_3840x2160.jpg','Anime'.decode('utf8'))
  
class SelectorDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.title = kwargs['title']
        self.list_items=kwargs['list']
        self.f_list=[]
        self.steps = kwargs['steps']
       

        self.items = []
        self.selection = None
        self.insideIndex = -1
        self.completed_steps = 0
        xbmc.executebuiltin('Action(FullScreen)')
  
       

    def get_selection(self):
        """ get final selection """
        return self.selection

    def onInit(self):

        
        self.list = self.getControl(450)
        self.list.controlLeft(self.list)
        self.list.controlRight(self.list)

      
     
    
        self.setFocus(self.list)
        self._inside_root(select=1)
       

    def onAction(self, action):
        if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448,):
            if self.insideIndex == -1:
                self.close()
            else:
                self._inside_root(select=self.insideIndex)

    def onClick(self, controlID):
     
        
            num = self.list.getSelectedPosition()

            if num >= 0:
                if self.insideIndex == -1:
                    
                
                    self._inside(num)
                    self.selection=self.f_list[self.insideIndex]
                    self.close()

    def onFocus(self, controlID):
        if controlID in (3, 61):
            self.setFocus(self.list)

    def _inside_root(self, select=-1):
       
            #logging.warning(self.items)
            all_links=[]
            
            
            for items in self.list_items:
                    listitem = xbmcgui.ListItem(items)
                    self.list.addItem(listitem)
                    self.f_list.append(items)
            if select >= 0:
                self.list.selectItem(select)
            self.insideIndex = -1
    def _inside(self, num):
        if num == -1:
            self._inside_root(select=self.insideIndex)
            return

        if 1:#with self.lock:
            

            self.insideIndex = num
def main_menu():
      
      
      if len(sys.argv)<2:
       return 0
      dbcur.execute("SELECT COUNT(*) FROM AllData")
      fix_setting()
      match = dbcur.fetchone()
      level_index=(match[0]/100)
      if level_index>9:
        level_index=9
      if Addon.getSetting("m_what")=='true':
        addNolink('What is Destiny?','www',132,False,iconimage=BASE_LOGO+'destiny.png',fanart=DESIMG)
      if Addon.getSetting("m_movies")=='true':
        addDir3('Movies'.decode('utf8'),'www',13,BASE_LOGO+'movies.png','http://hdqwalls.com/wallpapers/avengers-infinity-war-2018-poster-fan-made-62.jpg','Movies'.decode('utf8'))
      if Addon.getSetting("m_tvshows")=='true':
        addDir3('TV Shows'.decode('utf8'),'www',14,BASE_LOGO+'tvshow.png','https://i.imgur.com/a174Ipu.jpg','Tv Shows'.decode('utf8'))
      if Addon.getSetting("m_kids")=='true':
        addDir3('Kids'.decode('utf8'),'www',44,BASE_LOGO+'kids.png','https://www.desktopbackground.org/download/o/2013/09/27/645377_kids-kung-fu-panda-3-movie-4k-wallpapers_3840x2160_h.jpg','Kids'.decode('utf8'))
      if Addon.getSetting("m_actors")=='true':
        addDir3('Actors'.decode('utf8'),'www',72,BASE_LOGO+'actors.png','https://hdqwalls.com/download/avengers-infinity-war-imax-poster-na-2048x1152.jpg','Actors'.decode('utf8'))
      if Addon.getSetting("m_nba")=='true':        
        addDir3('NBA','https://www.nbafullhd.com',105,BASE_LOGO+'nba.png','https://cdn.nba.net/nba-drupal-prod/2017-08/SEO-image-NBA-logoman.jpg','NBA'.decode('utf8'))
      if Addon.getSetting("m_livesport")=='true':
        addDir3('Live Sports'.decode('utf8'),'www',40,BASE_LOGO+'live.png','https://scotch-res.cloudinary.com/image/upload/w_900,q_auto:good,f_auto/v1549206813/gyxlxwotow6xxysb527u.png','Live'.decode('utf8'))
      if Addon.getSetting("m_livetv")=='true':
        addDir3('Live TV'.decode('utf8'),'www',146,'https://icon2.kisspng.com/20180528/bxr/kisspng-live-television-logo-streaming-media-brand-5b0b8b721a8e95.3198740015274832501088.jpg','https://cdn2.vectorstock.com/i/1000x1000/85/36/live-stream-tv-logo-icon-vector-16968536.jpg','Live TV'.decode('utf8'))
      if Addon.getSetting("m_acestream")=='true':
        addDir3('Acestream'.decode('utf8'),'www',76,BASE_LOGO+'acestream.png','https://i.pinimg.com/originals/6b/18/31/6b1831503dc0e0470b2bf1e1b5df978f.jpg','Acestream'.decode('utf8'))
      if Addon.getSetting("m_m3u8")=='true':
        addDir3('M3u8 Lists'.decode('utf8'),'www',55,BASE_LOGO+'m3u8.png','https://indianapublicmedia.org/wp-content/themes/ipm-aux-services/images/services/transmission.jpg','M3u8 Lists'.decode('utf8'))
      if Addon.getSetting("m_fav")=='true':
        addDir3('My Favorites'.decode('utf8'),'all',18,BASE_LOGO+'fav.png','http://jonvilma.com/images/reign-tv-series-2.jpg','My Favorites'.decode('utf8'))
      if Addon.getSetting("m_jen")=='true':
        addDir3('Jen Lists'.decode('utf8'),'www',42,BASE_LOGO+'jen.png','https://geek-prime.com/wp-content/uploads/2014/02/Destiny-2-4k-hd-wallpaper-invasion-ghaul.jpg','Jen'.decode('utf8'))
      if Addon.getSetting("m_setting")=='true':
        addNolink('Settings','www',24,False,iconimage=BASE_LOGO+'setting.png',fanart=domain_s+'www.wanderlustworker.com/wp-content/uploads/2014/05/setting-smarter-goals.jpg')
      if Addon.getSetting("m_enterr")=='true':
        addNolink('Enable Real Debrid','www',138,False,iconimage=BASE_LOGO+'rd.png',fanart='https://troypoint.com/wp-content/uploads/2017/10/install-real-debrid-kodi.jpg')
      if Addon.getSetting("m_clear")=='true':
        addNolink('Clear Cache','www',16,False,iconimage=BASE_LOGO+'clearcache.png',fanart=domain_s+'digitalart.io/storage/artworks/1264/pacific-rim-wallpaper-striker.jpeg')
      if Addon.getSetting("m_update")=='true':
        addNolink('Update Sources','www',36,False,iconimage=BASE_LOGO+'update.png',fanart='https://images.idgesg.net/images/article/2018/03/update_cycle_arrows_on_background_of_orange_arrows_by_ranjith_siji_cc0_via_pixabay-100751945-large.jpg')
      if Addon.getSetting("m_recover")=='true':
        addNolink('Recover from Backup','www',89,False,iconimage=BASE_LOGO+'recover.png',fanart='https://hiverhq.com/blog/wp-content/uploads/2014/11/best-backup-tools-for-Google-Apps-and-Gmail-1.jpg')
      if Addon.getSetting("m_chnage")=='true':
        addNolink('Change Log','www',100,False,iconimage=BASE_LOGO+'changelog.png',fanart='https://one2onenetwork.com/wp-content/uploads/2011/06/things-to-change-t2c-list.jpg')
      if Addon.getSetting("m_checks")=='true':
        addDir3('Check Sources'.decode('utf8'),'www',98,BASE_LOGO+'server.png','https://wallpaperstock.net/wallpapers/thumbs1/8901wide.jpg','Check sources'.decode('utf8'))
      plot='[COLOR gold]'+'You are in Level '+str(level_index+1)+'\n'+'So Far You Have Watched '+str(match[0]) +' Movies and Episode '+' Keep Going.... '+'[/COLOR]'+'\nAnother ' +str((100*(level_index+1))-int(match[0]))+' To Move to the Next Level :-)'
      if Addon.getSetting("m_rating")=='true':
        addLink(''+'My Rating'+'',level_movies[level_index],35,False,iconimage=BASE_LOGO+'rating.png',fanart=level_fanart[level_index],description=plot)
      if Addon.getSetting("m_lastp")=='true':
        addDir3('Last Played'.decode('utf8'),'www',49,BASE_LOGO+'last.png','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgZlTxhsnI3lZ9gzBokPvapZG1W3S-_G1UNCohkK5il9r5myUF','Last played'.decode('utf8'))
      if Addon.getSetting("m_search")=='true':
        addDir3('Search'.decode('utf8'),'www',15,BASE_LOGO+'search.png','https://geek-prime.com/wp-content/uploads/2014/02/Destiny-2-4k-hd-wallpaper-invasion-ghaul.jpg','Search'.decode('utf8'))
      logging.warning( 'USE TRAKT')
      logging.warning( Addon.getSetting("use_trak"))
      if Addon.getSetting("m_trakt")=='true':
          addDir3('Trakt'.decode('utf8'),'www',29,BASE_LOGO+'trakt.png',domain_s+'www.mjdtech.net/content/images/2016/02/traktfeat.jpg','Trakt')
     
      
      
      
def movies_menu():
      import datetime
      #all_img=get_movie_poster()
      now = datetime.datetime.now()
      link_url='https://www.youtube.com/results?search_query=%D7%98%D7%A8%D7%99%D7%99%D7%9C%D7%A8+%D7%9E%D7%AA%D7%95%D7%A8%D7%92%D7%9D+{0}&page=1'.format( str(now.year))
    
      all_img=cache.get(get_movie_poster,24, table='posters')
                                                                                            
      addDir3('Genres','http://api.themoviedb.org/3/genre/movie/list?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1',2,BASE_LOGO+'genres.png',all_img[0],'Genres'.decode('utf8'))
      addDir3('Popular','http://api.themoviedb.org/3/movie/popular?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1',3,BASE_LOGO+'popular.png',all_img[4],'Popular')
      if allow_debrid:
        addDir3('Once click RD movies','www',149,'https://image.shutterstock.com/image-vector/vector-logo-slate-board-shooting-260nw-279718811.jpg',all_img[19],'Once click RD movies')
      addDir3('Once click free movies','https://moviesmax.net',150,'https://logos.flamingtext.com/Name-Logos/Movies-design-amped-name.png',all_img[1],'Once click free movies')
      
      addDir3('Popular in 20 years'.decode('utf8'),'movie',133,BASE_LOGO+'popular20.png',all_img[11],'Popular in 20 years',data='20',original_title='1')
      addDir3('Popular in 10 years'.decode('utf8'),'movie',133,BASE_LOGO+'popular10.png',all_img[12],'Popular in 10 years',data='10',original_title='1')
      addDir3('Hot Movies','http://api.themoviedb.org/3/trending/movie/week?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1',3,BASE_LOGO+'hotmovies.png',all_img[13],'Hot Movies')
      addDir3('In Theaters'.decode('utf8'),'http://api.themoviedb.org/3/movie/now_playing?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1',3,BASE_LOGO+'theaters.png',all_img[10],'In Theaters'.decode('utf8'))
      addDir3('By Years'.decode('utf8'),'movie_years&page=1',3,'http://www.greenmancreations.com/images/logo-design/movieworld-logo.jpg',all_img[2],'By Years'.decode('utf8'))
      
      addDir3('Based on true story','https://www.imdb.com/search/title?genres=biography&sort=num_votes,desc&explore=title_type,genres',114,BASE_LOGO+'based.png',all_img[14],'Based on true story',isr=' ')
      addDir3('Oscar Winners Best Movie','https://www.imdb.com/search/title?count=100&groups=oscar_best_picture_winners&sort=year,desc&ref_=nv_ch_osc',114,BASE_LOGO+'oscarmovie.png',all_img[16],'Oscar Winners best movie',isr=' ')
      addDir3('Oscar Winners Best Actor','https://www.imdb.com/list/ls068045646/?sort=list_order,asc&mode=detail&page=1',134,BASE_LOGO+'oscaractor.png',all_img[17],'Oscar Winners best actor',isr=' ')
      addDir3('Studio'.decode('utf8'),'movie',112,BASE_LOGO+'studio.png','https://cdn-static.denofgeek.com/sites/denofgeek/files/styles/main_wide/public/2016/04/movlic_studios_1.jpg?itok=ih8Z7wOk','Studio')
      addDir3('IMDB Popular','https://www.imdb.com/chart/moviemeter?ref_=nv_mv_mpm',114,BASE_LOGO+'imdbp.png',all_img[15],'IMDB Popular',isr=' ')
      addDir3('Favourites'.decode('utf8'),'movies',18,BASE_LOGO+'favorites.png','http://4.bp.blogspot.com/-8q4ops3bX_0/T0TWUOu5ETI/AAAAAAAAA1A/AQMDv0Sv4Cs/s1600/logo1.gif','Favorites'.decode('utf8'))
      addDir3('Last Watched'.decode('utf8'),'movie',91,BASE_LOGO+'lwatched.png',all_img[7],'Last watched',isr=' ')
      dbcur.execute("SELECT * FROM lastlinkmovie WHERE o_name='f_name'")

      match = dbcur.fetchone()
      if match!=None:
       f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match
       try:
           if url!=' ':
             if 'http' not  in url:
           
               url=url.decode('base64')
              
             addLink('Last played link', 'latest_movie',5,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=prev_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year)
       except  Exception as e:
         logging.warning(e)
         pass
      
      addDir3('Search','http://api.themoviedb.org/3/search/movie?api_key=1248868d7003f60f2386595db98455ef&query=%s&language=en&append_to_response=origin_country&page=1',3,BASE_LOGO+'searchm.png','http://www.videomotion.co.il/wp-content/uploads/whatwedo-Pic-small.jpg','search')
      addDir3('Recommended for YOU','www',26,BASE_LOGO+'recomm.png',all_img[14],'Recommended for YOU',isr=' ')
      addDir3('Lastest HD'.decode('utf8'),domain_s+'www.dvdsreleasedates.com/movies/',28,BASE_LOGO+'latest.png',all_img[5],'Lastest HD'.decode('utf8'),isr=' ')

def tv_neworks():
    if Addon.getSetting("order_networks")=='0':
        order_by='popularity.desc'
    elif Addon.getSetting("order_networks")=='2':
        order_by='vote_average.desc'
    elif Addon.getSetting("order_networks")=='1':
        order_by='first_air_date.desc'

    addDir3('NetFlix'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=213&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://art.pixilart.com/705ba833f935409.png','https://i.ytimg.com/vi/fJ8WffxB2Pg/maxresdefault.jpg','NetFlix'.decode('utf8'))
    addDir3('HBO'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=49&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://filmschoolrejects.com/wp-content/uploads/2018/01/hbo-logo.jpg','https://www.hbo.com/content/dam/hbodata/brand/hbo-static-1920.jpg','HBO'.decode('utf8'))
    addDir3('CBS'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=16&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://cdn.freebiesupply.com/logos/large/2x/cbs-logo-png-transparent.png','https://tvseriesfinale.com/wp-content/uploads/2014/10/cbs40-590x221.jpg','HBO'.decode('utf8'))
    addDir3('SyFy'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=77&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'http://cdn.collider.com/wp-content/uploads/syfy-logo1.jpg','https://imagesvc.timeincapp.com/v3/mm/image?url=https%3A%2F%2Fewedit.files.wordpress.com%2F2017%2F05%2Fdefault.jpg&w=1100&c=sc&poi=face&q=85','SyFy'.decode('utf8'))
    addDir3('The CW'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=71&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://www.broadcastingcable.com/.image/t_share/MTU0Njg3Mjc5MDY1OTk5MzQy/tv-network-logo-cw-resized-bc.jpg','https://i2.wp.com/nerdbastards.com/wp-content/uploads/2016/02/The-CW-Banner.jpg','The CW'.decode('utf8'))
    addDir3('ABC'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=2&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'http://logok.org/wp-content/uploads/2014/03/abc-gold-logo-880x660.png','https://i.ytimg.com/vi/xSOp4HJTxH4/maxresdefault.jpg','ABC'.decode('utf8'))
    addDir3('NBC'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=6&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://designobserver.com/media/images/mondrian/39684-NBC_logo_m.jpg','https://www.nbcstore.com/media/catalog/product/cache/1/image/1000x/040ec09b1e35df139433887a97daa66f/n/b/nbc_logo_black_totebagrollover.jpg','NBC'.decode('utf8'))
    addDir3('AMAZON'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=1024&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'http://g-ec2.images-amazon.com/images/G/01/social/api-share/amazon_logo_500500._V323939215_.png','https://cdn.images.express.co.uk/img/dynamic/59/590x/Amazon-Fire-TV-Amazon-Fire-TV-users-Amazon-Fire-TV-stream-Amazon-Fire-TV-Free-Dive-TV-channel-Amazon-Fire-TV-news-Amazon-1010042.jpg?r=1535541629130','AMAZON'.decode('utf8'))
    addDir3('Hulu'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&with_networks=453&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://i1.wp.com/thetalkinggeek.com/wp-content/uploads/2012/03/hulu_logo_spiced-up.png?resize=300%2C225&ssl=1','https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwi677r77IbeAhURNhoKHeXyB-AQjRx6BAgBEAU&url=https%3A%2F%2Fwww.hulu.com%2F&psig=AOvVaw0xW2rhsh4UPsbe8wPjrul1&ust=1539638077261645','hulu'.decode('utf8'))

def movie_prodiction():
    if Addon.getSetting("order_networks")=='0':
        order_by='popularity.desc'
    elif Addon.getSetting("order_networks")=='2':
        order_by='vote_average.desc'
    elif Addon.getSetting("order_networks")=='1':
        order_by='first_air_date.desc'

    addDir3('Marvel'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=7505&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://yt3.ggpht.com/a-/AN66SAwQlZAow0EBMi2-tFht-HvmozkqAXlkejVc4A=s900-mo-c-c0xffffffff-rj-k-no','https://images-na.ssl-images-amazon.com/images/I/91YWN2-mI6L._SL1500_.jpg','Marvel'.decode('utf8'))
    addDir3('DC Studios'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=9993&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://pmcvariety.files.wordpress.com/2013/09/dc-comics-logo.jpg?w=1000&h=563&crop=1','http://www.goldenspiralmedia.com/wp-content/uploads/2016/03/DC_Comics.jpg','DC Studios'.decode('utf8'))
    addDir3('Lucasfilm'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=1&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://fontmeme.com/images/lucasfilm-logo.png','https://i.ytimg.com/vi/wdYaG3o3bgE/maxresdefault.jpg','Lucasfilm'.decode('utf8'))
    addDir3('Warner Bros.'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=174&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'http://looking.la/wp-content/uploads/2017/10/warner-bros.png','https://cdn.arstechnica.net/wp-content/uploads/2016/09/warner.jpg','SyFy'.decode('utf8'))
    addDir3('Walt Disney Pictures'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=2&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://i.ytimg.com/vi/9wDrIrdMh6o/hqdefault.jpg','https://vignette.wikia.nocookie.net/logopedia/images/7/78/Walt_Disney_Pictures_2008_logo.jpg/revision/latest?cb=20160720144950','Walt Disney Pictures'.decode('utf8'))
    addDir3('Pixar'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=3&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://elestoque.org/wp-content/uploads/2017/12/Pixar-lamp.png','https://wallpapercave.com/wp/GysuwJ2.jpg','Pixar'.decode('utf8'))
    addDir3('Paramount'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=4&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://upload.wikimedia.org/wikipedia/en/thumb/4/4d/Paramount_Pictures_2010.svg/1200px-Paramount_Pictures_2010.svg.png','https://vignette.wikia.nocookie.net/logopedia/images/a/a1/Paramount_Pictures_logo_with_new_Viacom_byline.jpg/revision/latest?cb=20120311200405&format=original','Paramount'.decode('utf8'))
    addDir3('Columbia Pictures'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=5&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://static.tvtropes.org/pmwiki/pub/images/lady_columbia.jpg','https://vignette.wikia.nocookie.net/marveldatabase/images/1/1c/Columbia_Pictures_%28logo%29.jpg/revision/latest/scale-to-width-down/1000?cb=20141130063022','Columbia Pictures'.decode('utf8'))
    addDir3('DreamWorks'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=7&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://www.dreamworksanimation.com/share.jpg','https://www.verdict.co.uk/wp-content/uploads/2017/11/DA-hero-final-final.jpg','DreamWorks'.decode('utf8'))
    addDir3('Miramax'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=14&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://vignette.wikia.nocookie.net/disney/images/8/8b/1000px-Miramax_1987_Print_Logo.png/revision/latest?cb=20140902041428','https://i.ytimg.com/vi/4keXxB94PJ0/maxresdefault.jpg','Miramax'.decode('utf8'))
    addDir3('20th Century Fox'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=25&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://pmcdeadline2.files.wordpress.com/2017/03/20th-century-fox-cinemacon1.jpg?w=446&h=299&crop=1','https://vignette.wikia.nocookie.net/simpsons/images/8/80/TCFTV_logo_%282013-%3F%29.jpg/revision/latest?cb=20140730182820','20th Century Fox'.decode('utf8'))
    addDir3('Sony Pictures'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=34&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Sony_Pictures_Television_logo.svg/1200px-Sony_Pictures_Television_logo.svg.png','https://vignette.wikia.nocookie.net/logopedia/images/2/20/Sony_Pictures_Digital.png/revision/latest?cb=20140813002921','Sony Pictures'.decode('utf8'))
    addDir3('Lions Gate Films'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=35&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'http://image.wikifoundry.com/image/1/QXHyOWmjvPRXhjC98B9Lpw53003/GW217H162','https://vignette.wikia.nocookie.net/fanon/images/f/fe/Lionsgate.jpg/revision/latest?cb=20141102103150','Lions Gate Films'.decode('utf8'))
    addDir3('Orion Pictures'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=41&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://i.ytimg.com/vi/43OehM_rz8o/hqdefault.jpg','https://i.ytimg.com/vi/g58B0aSIB2Y/maxresdefault.jpg','Lions Gate Films'.decode('utf8'))
    addDir3('MGM'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=21&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://pbs.twimg.com/profile_images/958755066789294080/L9BklGz__400x400.jpg','https://assets.entrepreneur.com/content/3x2/2000/20150818171949-metro-goldwun-mayer-trade-mark.jpeg','MGM'.decode('utf8'))
    addDir3('New Line Cinema'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=12&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://upload.wikimedia.org/wikipedia/en/thumb/0/04/New_Line_Cinema.svg/1200px-New_Line_Cinema.svg.png','https://vignette.wikia.nocookie.net/theideas/images/a/aa/New_Line_Cinema_logo.png/revision/latest?cb=20180210122847','New Line Cinema'.decode('utf8'))
    addDir3('Gracie Films'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=18&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://i.ytimg.com/vi/q_slAJmZBeQ/hqdefault.jpg','https://i.ytimg.com/vi/yGofbuJTb4g/maxresdefault.jpg','Gracie Films'.decode('utf8'))
    addDir3('Imagine Entertainment'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&with_companies=23&language=en&sort_by={0}&timezone=America%2FNew_York&include_null_first_air_dates=false&page=1'.format(order_by),3,'https://s3.amazonaws.com/fs.goanimate.com/files/thumbnails/movie/2813/1661813/9297975L.jpg','https://www.24spoilers.com/wp-content/uploads/2004/06/Imagine-Entertainment-logo.jpg','Imagine Entertainment'.decode('utf8'))
    
def tv_menu():
      import datetime
      now = datetime.datetime.now()
      all_img=cache.get(get_tv_poster,24, table='posters')

      addDir3('Genres','http://api.themoviedb.org/3/genre/tv/list?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1',2,BASE_LOGO+'genrestv.png',all_img[0],'Genres')
      addDir3('Popular','http://api.themoviedb.org/3/tv/popular?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1',3,BASE_LOGO+'populartv.png',all_img[1],'Popular')
      addDir3('Running Series','https://api.themoviedb.org/3/tv/on_the_air?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1',3,BASE_LOGO+'running.png',all_img[8],'Running series')
      addDir3('Popular in 20 Years','tv',133,BASE_LOGO+'popular20tv.png',all_img[11],'Popular in 20 years',data='20',original_title='1')
      addDir3('Popular in 10 Years','tv',133,BASE_LOGO+'popular10tv.png',all_img[12],'Popular in 10 years',data='10',original_title='1')
      addDir3('HOT TV','http://api.themoviedb.org/3/trending/tv/week?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1',3,BASE_LOGO+'hottv.png',all_img[13],'Hot this week')
      addDir3('Years','tv_years&page=1',3,BASE_LOGO+'yearstv.png',all_img[2],'Years')
      addDir3('New',domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&language=en-US&sort_by=popularity.desc&first_air_date_year='+str(now.year)+'&timezone=America%2FNew_York&include_null_first_air_ates=false&language=en&page=1',3,BASE_LOGO+'new.png',all_img[3],'New')
      addDir3('Networks','tv',101,BASE_LOGO+'networks.png','https://images.pond5.com/tv-networks-logos-loop-footage-042898083_prevstill.jpeg','Networks shows')
      addDir3('Favourite Shows','tv',18,BASE_LOGO+'favoritestv.png','http://4.bp.blogspot.com/-8q4ops3bX_0/T0TWUOu5ETI/AAAAAAAAA1A/AQMDv0Sv4Cs/s1600/logo1.gif','Favorites shows')
      addDir3('Recommended Shows for You','www',27,BASE_LOGO+'recotv.png',all_img[5],'Recommended shows for you based on your history',isr=' ')
      addDir3('Popular IMDB','https://www.imdb.com/search/title?title_type=tv_series',114,BASE_LOGO+'popimdbtv.png',all_img[8],'Popular IMDB',isr=' ')
      addDir3('Series Tracker','tv',32,BASE_LOGO+'tracks.png',all_img[6],'Series tracker',isr=' ')
      addDir3('Watched Shows','tv',91,BASE_LOGO+'watchedtv.png',all_img[7],'watched shows',isr=' ')
      dbcur.execute("SELECT * FROM lastlinktv WHERE o_name='f_name'")

      match = dbcur.fetchone()
      if match!=None:
       
       f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match
       try:
           if url!=' ':
             if 'http' not  in url:
             
               url=url.decode('base64')
  
             addLink('Last Played Link', 'latest_tv',5,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=prev_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year)
             
       except Exception as e:
         logging.warning(e)
         pass
      
      addDir3('Search','http://api.themoviedb.org/3/search/tv?api_key=1248868d7003f60f2386595db98455ef&query=%s&language=en&page=1',3,BASE_LOGO+'searchtv.png',domain_s+'f.frogi.co.il/news/640x300/010170efc8f.jpg','Search')

def search_menu():
       addDir3('Search Movie','http://api.themoviedb.org/3/search/movie?api_key=1248868d7003f60f2386595db98455ef&query=%s&language=en&append_to_response=origin_country&page=1',3,BASE_LOGO+'searchm.png','http://www.videomotion.co.il/wp-content/uploads/whatwedo-Pic-small.jpg','search')
       addDir3('Search TV Show','http://api.themoviedb.org/3/search/tv?api_key=1248868d7003f60f2386595db98455ef&query=%s&language=en&page=1',3,BASE_LOGO+'searchtv.png',domain_s+'f.frogi.co.il/news/640x300/010170efc8f.jpg','Search')
def get_genere(link,icon):
   images={}
   html=requests.get(link).json()
   for data in html['genres']:
     if '/movie' in link:
       new_link='http://api.themoviedb.org/3/genre/%s/movies?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1'%str(data['id'])
     else:
       new_link='http://api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&sort_by=popularity.desc&with_genres=%s&language=en&page=1'%str(data['id'])
    
     addDir3(data['name'],new_link,3,icon,DESIMG,data['name'])



def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
def start_window2(id,tv_movie,name,selected_option):

      if selected_option=='2':
        send_type='find_similar'
      else:
        send_type=''
      menu = sources_search2('plugin.video.destiny', id,tv_movie,send_type)
      menu.doModal()
     
      del menu
      
def start_window(id,tv_movie,name,selected_option):
   
    menu = sources_search('plugin.video.destiny',id,tv_movie,name)
    menu.doModal()
    
    del menu
def get_subs_trd(imdb_id,season,episode):
    da=[]
    da.append((imdb_id,season,episode))
    logging.warning('subtitle trd')
    logging.warning(da)
    if season=='%20':
        season=None
    if episode=='%20':
        episode=None
    result=cache.get(get_sub_server,24,imdb_id,season,episode, table='pages')
    return 'ok'
def check_cached(magnet):
    import real_debrid
    rd = real_debrid.RealDebrid()
    check=False
    hash = str(re.findall(r'btih:(.*?)&', magnet)[0].lower())
    hashCheck = rd.checkHash(hash)
    if hash in hashCheck:
            if 'rd' in hashCheck[hash]:
                if len(hashCheck[hash]['rd'])>0:
                    check=True
    return check
def get_condition(name1,links,server,res,tv_movie,f_result,data,original_title):
    try:
        res_table=['2160','1080','720','480','360']
        check_r_l={}
        condition_sources=False
        str_check=[]
        try:#Resolution
          a=int(res)
        except:
          res='0'
        if tv_movie=='tv':
            min_super_fast=res_table[int(Addon.getSetting("tv_min_super_fast"))]
            max_super_fast=res_table[int(Addon.getSetting("tv_max_super_fast"))]
        else:
            min_super_fast=res_table[int(Addon.getSetting("movies_min_super_fast"))]
            max_super_fast=res_table[int(Addon.getSetting("movies_max_super_fast"))]
      
        if int(res)>=int(min_super_fast) and int(res)<=int(max_super_fast):
            check_r_l['server_type_res']=True
            str_check.append(' V Res:%s '%res)
            condition_res=True
        else:
            check_r_l['server_type_res']=False
            str_check.append(' X Res:%s '%res)
            condition_res=False
        if  condition_res :
            return True,','.join(str_check).replace(' V ','')
        else:
            return False,','.join(str_check).replace(' V ','')
    except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Line:'+str(lineno)+' E:'+str(e))).encode('utf-8'))
        logging.warning('ERROR IN super play:'+str(lineno))
        logging.warning('inline:'+line)
        logging.warning(e)
        logging.warning('BAD super play')
        return False,','.join(str_check).replace(' V ','')
def c_get_sources(name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local=False,fav_status='false',only_torrent='no',only_heb_servers='0'):
   global stop_all,once_fast_play,silent_mode,stoped_play_once
   try:
    
    global all_s_in,stop_window,global_result,all_links_sources
    import random
    original_title=clean_name(original_title,1)
    try:
        import resolveurl
        hostDict = resolveurl.relevant_resolvers(order_matters=True)
        hostDict = [i.domains for i in hostDict if '*' not in i.domains]
        hostDict = [i.lower() for i in reduce(lambda x, y: x+y, hostDict)]
        hostDict = [x for y, x in enumerate(hostDict) if x not in hostDict[:y]]
    except Exception:
        hostDict = []
    premiered=isr
   
    tmdbKey = '1248868d7003f60f2386595db98455ef'
    if season!=None and season!="%20":
       tv_movie='tv'
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,tmdbKey)
    else:
       tv_movie='movie'
       
       url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,tmdbKey)
    if 'tt' not in id:
         try:
            imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
         except:
            imdb_id=" "
            
    all_s_in=({},0,'','','')
    da=[]
    stop_window=False
    da.append((name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local,fav_status))
          
    logging.warning('da')
    logging.warning(da)
    
    if debug_mode==True:
      logging.warning('Searching sources')
    if season!=None and season!="%20":
          tv_movie='tv'
      
          
    else:
          tv_movie='movie'
    if Addon.getSetting("new_server_dp")=='true' and silent_mode==False:
            
            
            thread=[]
            selected_option=Addon.getSetting("new_server_dp_option")
            
            if selected_option=='3':
                rand=(random.randint(0,299)/100)
                selected_option=str(int(rand))
       
            if selected_option=='0':
                thread.append(Thread(start_window,id,tv_movie,heb_name,selected_option))
                thread[len(thread)-1].setName('sources_s1')
            elif selected_option=='1' or selected_option=='2':
                thread.append(Thread(start_window2,id,tv_movie,heb_name,selected_option))
                thread[len(thread)-1].setName('sources_s2')
            thread[0].start()
    if Addon.getSetting("server_dp")=='true' and silent_mode==False:
        
        dp = xbmcgui . DialogProgress ( )
        dp.create('Please wait','Searching Sources', '','')
        dp.update(0, 'Please wait','Searching Sources', '' )
    if Addon.getSetting("trailer_dp")=="true" and Addon.getSetting("new_server_dp")=="false":
      pDialog = xbmcgui.DialogProgressBG()
      pDialog.create('Collecting')
      #pDialog.update(0, message=' Please wait ')

    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode
    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
   
    if Addon.getSetting("lang")=="1":
      lang='en'
    else:
      lang='he'
    url2=None

    
    thread=[]
    tv_mode=tv_movie
  
    original_title=original_title.replace('%3a','')

    all_sources=[]
    if tv_movie=='movie':
        fav_server_en=Addon.getSetting("fav_servers_en")
        fav_servers=Addon.getSetting("fav_servers")
       
        
    else:
        fav_server_en=Addon.getSetting("fav_servers_en_tv")
        fav_servers=Addon.getSetting("fav_servers_tv")
      
    onlyfiles=[]
    all_mag_s=[]
    for f in listdir(mag_dir):
        if isfile(join(mag_dir, f)):
            all_mag_s.append(f)
    
    if  not ((Addon.getSetting("all_t")=='1' and Addon.getSetting("magnet")=='true') or only_torrent=='yes'):
        onlyfiles = [f for f in listdir(done_dir) if isfile(join(done_dir, f))]
    if Addon.getSetting("magnet")=='true' or only_torrent=='yes':
        onlyfiles=onlyfiles+[f for f in listdir(mag_dir) if isfile(join(mag_dir, f))]
    all_fv_servers=[]
    if fav_status=='true' or fav_status=='rest':
      if fav_server_en=='true':
        all_fv_servers=fav_servers.split(',')
        all_direct=[]
        all_google=[]
        all_rapid=[]
      
        z=0
        
        for items in onlyfiles:
            
            
            if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                    dp.update(int((z*100.0)/(len(onlyfiles))), 'Please wait','Collecting', items )
            all_s_in=({},int((z*100.0)/(len(onlyfiles))),items,1,'')
            if items !='cache.py' and items !='general.py' and '.pyc' not in items and '.pyo' not in items and '__init__' not in items and items !='resolveurl_temp.py' and items!='cloudflare.py' and items!='Addon.py':
                
                impmodule = __import__(items.replace('.py',''))
                if items in all_mag_s:
                    type=['magnet']
                else:
                    type=[]
                type,source_scraper=get_type(impmodule,items.replace('.py',''))
                
                if Addon.getSetting("magnet")=='true' and Addon.getSetting(items.replace('.py',''))=="true" and 'magnet' in type:
                    all_fv_servers.append(items.replace('.py',''))
                
                z+=1
        '''
        if Addon.getSetting("rdsource")=='true':
            onlyfiles2 = [f for f in listdir(rd_dir) if isfile(join(rd_dir, f))]
            f_result={}
            

            name_check=''
            z=0
            
            for items in onlyfiles2:
              if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                 dp.update(int((z*100.0)/(len(onlyfiles2))), 'Please wait','Collecting', items )
              all_s_in=({},int((z*100.0)/(len(onlyfiles2))),items,1,'')
              if items !='general.py' and '.pyc' not in items and '.pyo' not in items and '__init__' not in items and items !='resolveurl_temp.py' and items!='cloudflare.py' and items!='Addon.py':
               if fav_status=='true':
                    if items.replace('.py','') not in all_fv_servers:
                        continue
           
                    
               elif fav_status=='rest':
                        if items.replace('.py','')  in all_fv_servers:
                            continue
               impmodule = __import__(items.replace('.py',''))
               type=['rd']
               type,source_scraper=get_type(impmodule,items.replace('.py',''))
               if Addon.getSetting(items.replace('.py',''))=="true":
                   
                   if name_check!='':
                     if items.replace('.py','')==name_check:
                       if tv_movie=='movie' and 'movie' in type:
                         all_sources.append((items.replace('.py',''),impmodule))
                       elif tv_movie=='tv' and 'tv' in type:
                         all_sources.append((items.replace('.py',''),impmodule))
                   else:
                     if tv_movie=='movie' and 'movie' in type:
                       all_sources.append((items.replace('.py',''),impmodule))
                     elif tv_movie=='tv' and 'tv' in type:
                       all_sources.append((items.replace('.py',''),impmodule))
            
            z+=1
        '''
      else:
        all_fv_servers=[]
    
    if (Addon.getSetting("all_t")=='1' or only_torrent=='yes') and Addon.getSetting("magnet")=='true':
        all_fv_servers=[]
    if Addon.getSetting("server_dp")=='true' and silent_mode==False:
       dp.update(0, 'Please wait','Collecting', '' )
    
    
    f_result={}
 
    regular_s=True
    if Addon.getSetting("rdsource")=='true' and Addon.getSetting("rd_only")=='true':
      regular_s=False
    if (Addon.getSetting("all_t")=='1' or only_torrent=='yes') and Addon.getSetting("magnet")=='true':
        regular_s=False

    if regular_s:
        
        
        name_check=''
        z=0
        
        for items in onlyfiles:
          if Addon.getSetting("server_dp")=='true' and silent_mode==False:
             dp.update(int((z*100.0)/(len(onlyfiles))), 'Please wait','Collecting', items )
          all_s_in=({},int((z*100.0)/(len(onlyfiles))),items,1,'')
          if items !='general.py' and '.pyc' not in items and '.pyo' not in items and '__init__' not in items and items !='resolveurl_temp.py' and items!='cache.py' and items!='Addon.py':

           
           if fav_status=='true':
                if items.replace('.py','') not in all_fv_servers:
                    continue
           
                    
           elif fav_status=='rest':
                if items.replace('.py','')  in all_fv_servers:
                    continue

           impmodule = __import__(items.replace('.py',''))
           if items in all_mag_s:
                type=['magnet']
           else:
                type=[]
           type,source_scraper=get_type(impmodule,items.replace('.py',''))
           
           if Addon.getSetting("magnet")=='false' and 'magnet' in type:
                continue
           
           
           
           
           if Addon.getSetting(items.replace('.py',''))=="true" or (Addon.getSetting("magnet")=='true' and ('magnet' in type) and Addon.getSetting(items.replace('.py',''))=="true"):
            
               if name_check!='':
                 if items.replace('.py','')==name_check:
                   if tv_movie=='movie' and 'movie' in type:
                     all_sources.append((items.replace('.py',''),impmodule))
                   elif tv_movie=='tv' and 'tv' in type:
                     all_sources.append((items.replace('.py',''),impmodule))
               else:
                 if tv_movie=='movie' and 'movie' in type:
                   all_sources.append((items.replace('.py',''),impmodule))
                 elif tv_movie=='tv' and 'tv' in type:
                   all_sources.append((items.replace('.py',''),impmodule))
        z+=1
        
        if Addon.getSetting("rdsource")=='true':
            onlyfiles = [f for f in listdir(rd_dir) if isfile(join(rd_dir, f))]
           
            

            name_check=''
            z=0

          
            
            for items in onlyfiles:
              
              if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                 dp.update(int((z*100.0)/(len(onlyfiles))), 'Please wait','Collecting', items )
              all_s_in=({},int((z*100.0)/(len(onlyfiles))),items,1,'')
              if items !='general.py' and '.pyc' not in items and '.pyo' not in items and '__init__' not in items and items !='resolveurl_temp.py' and items!='cloudflare.py' and items!='Addon.py':
               if fav_status=='true':
                    if items.replace('.py','') not in all_fv_servers:
                        continue
           
                    
               elif fav_status=='rest':
                    if items.replace('.py','')  in all_fv_servers:
                        continue
               impmodule = __import__(items.replace('.py',''))
               type=['rd']
               type,source_scraper=get_type(impmodule,items.replace('.py',''))
        
               if Addon.getSetting(items.replace('.py',''))=="true":
                   
                   if name_check!='':
                     if items.replace('.py','')==name_check:
                       if tv_movie=='movie' and 'movie' in type:
                         all_sources.append((items.replace('.py',''),impmodule))
                       elif tv_movie=='tv' and 'tv' in type:
                         all_sources.append((items.replace('.py',''),impmodule))
                   else:
                     if tv_movie=='movie' and 'movie' in type:
                       all_sources.append((items.replace('.py',''),impmodule))
                     elif tv_movie=='tv' and 'tv' in type:
                       all_sources.append((items.replace('.py',''),impmodule))    
    else:
      if Addon.getSetting("rdsource")=='true':
        onlyfiles = [f for f in listdir(rd_dir) if isfile(join(rd_dir, f))]
        f_result={}
        

        name_check=''
        z=0

       
        
        for items in onlyfiles:
          
          if Addon.getSetting("server_dp")=='true' and silent_mode==False:
             dp.update(int((z*100.0)/(len(onlyfiles))), 'Please wait','Collecting', items )
          all_s_in=({},int((z*100.0)/(len(onlyfiles))),items,1,'')
          if items !='general.py' and '.pyc' not in items and '.pyo' not in items and '__init__' not in items and items !='resolveurl_temp.py' and items!='cloudflare.py' and items!='Addon.py':
           if fav_status=='true':
                    if items.replace('.py','') not in all_fv_servers:
                        continue
           
                    
           elif fav_status=='rest':
                    if items.replace('.py','')  in all_fv_servers:
                        continue
           impmodule = __import__(items.replace('.py',''))
           type=['rd']
           type,source_scraper=get_type(impmodule,items.replace('.py',''))
 
           if Addon.getSetting(items.replace('.py',''))=="true":
               
               if name_check!='':
                 if items.replace('.py','')==name_check:
                   if tv_movie=='movie' and 'movie' in type:
                     all_sources.append((items.replace('.py',''),impmodule))
                   elif tv_movie=='tv' and 'tv' in type:
                     all_sources.append((items.replace('.py',''),impmodule))
               else:
                 if tv_movie=='movie' and 'movie' in type:
                   all_sources.append((items.replace('.py',''),impmodule))
                 elif tv_movie=='tv' and 'tv' in type:
                   all_sources.append((items.replace('.py',''),impmodule))
        z+=1
    if (Addon.getSetting("all_t")=='1' and Addon.getSetting("magnet")=='true') or only_torrent=='yes'  :
            name_check=''
            #onlyfiles = [f for f in listdir(done_dir) if isfile(join(done_dir, f))]
            onlyfiles=[f for f in listdir(mag_dir) if isfile(join(mag_dir, f))]
            z=0
            
            
            for items in onlyfiles:
             
                if items !='general.py' and '.pyc' not in items and '.pyo' not in items and '__init__' not in items and items !='resolveurl_temp.py' and items!='cloudflare.py' and items!='Addon.py':
                    
                        if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                            dp.update(int((z*100.0)/(len(onlyfiles))), 'Please wait','Collecting', items )
                        all_s_in=({},int((z*100.0)/(len(onlyfiles))),items,1,'')
                        impmodule = __import__(items.replace('.py',''))
                        
                        type=['torrent']
                        type,source_scraper=get_type(impmodule,items.replace('.py',''))
                    
                        if Addon.getSetting(items.replace('.py',''))=="true":
                            
                            all_sources.append((items,impmodule))
            z+=1
            
   
    

    all_s_in=({},100,'',1,'')

    for name1,items in all_sources:
        if Addon.getSetting("server_dp")=='true' and silent_mode==False:
           dp.update(0, 'Please wait','Searching', name1 )
        
        if name_check!='':
           if name1==name_check:
             thread.append(Thread(get_links_new,hostDict,imdb_id,name1,type,items,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id,premiered,False))
             #thread.append(Thread(items.get_links,tv_movie,original_title,heb_name,season_n,episode_n,season,episode,show_original_year,id))
             thread[len(thread)-1].setName(name1)
        else:
          thread.append(Thread(get_links_new,hostDict,imdb_id,name1,type,items,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id,premiered,False))
          #thread.append(Thread(items.get_links,tv_movie,original_title,heb_name,season_n,episode_n,season,episode,show_original_year,id))
          thread[len(thread)-1].setName(name1)
        
    if Addon.getSetting("trailer_dp")=="true" and Addon.getSetting("new_server_dp")=="false":
      thread.append(Thread(play_trailer_f(id,tv_mode)))
      thread[len(thread)-1].setName('Trailer')
        

        
    
    if Addon.getSetting("subtitles")=='true':
        thread.append(Thread(get_subs_trd,imdb_id,season,episode))
      
        thread[len(thread)-1].setName('Subs')
    
    start_time = time.time()
    stop_all=0
    zzz=0
    for td in thread:
      td.start()
      
      if Addon.getSetting("server_test_one")=='true':
        while td.is_alive():
            elapsed_time = time.time() - start_time
            dp.update(int(((zzz* 100.0)/(len(thread))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name, 'Waiting')
            xbmc.sleep(1000)
            if dp.iscanceled():
              dp.close()
              return 0
      zzz+=1
    if Addon.getSetting("server_test_one")=='true':
        return 0
    if fav_status=='true' and Addon.getSetting("fav_search_time_en"):
       max_time=int(Addon.getSetting("fav_search_time"))
    else:
       max_time=int(Addon.getSetting("time_s"))
  
    num_live=0
    tt={}
    for i in range (0,(len(thread)+50)): 
      tt[i]="red"

    
    string_dp=''
    string_dp2=''
    still_alive=0

    if len(thread)==0:
      xbmcgui.Dialog().ok('Error occurred','[COLOR aqua][I] No servers were found [/I][/COLOR]')
    all_links_togther={}
    check_lk=[]
    while 1:
         num_live=0
         
          
         
         elapsed_time = time.time() - start_time
        
            
         if 1:#for threads in thread:
              elapsed_time = time.time() - start_time
              num_live=0
              string_dp=''
              string_dp2=''
              still_alive=0
              count_2160=0
              count_1080=0
              count_720=0
              count_480=0
              count_rest=0
              count_alive=0
              all_alive={}
              for yy in range(0,len(thread)):
                all_alive[thread[yy].name]=thread[yy].is_alive()
                if not thread[yy].is_alive():
                  num_live=num_live+1
                  tt[yy]="lightgreen"
                else:
                  
                  
                  if string_dp2=='':
                    string_dp2=thread[yy].name
                  else:
                    count_alive+=1
                    string_dp2=string_dp2+','+thread[yy].name
                  still_alive=1
                  tt[yy]="red"
              
              
              
              save_name=''
  
              all_links_togther=all_links_sources
              f_result=all_links_sources
              
              
              living=[]
              for items in all_alive:
                 if all_alive[items]:
                   living.append(items)
              if count_alive>10:
                
                string_dp2='Remaining sources: '+str(count_alive)+' - '+random.choice (living)
              count_found=0
              try:
                  for data in f_result:
                  
                    #for data in all_links_togther['links']:
                  
                    if len (all_links_sources)>0:
                       count_found+=1
                       
                    if 'links' in f_result[data] and len (f_result[data]['links'])>0 and data!='subs':
                         
                         for links_in in f_result[data]['links']:
                             name1,links,server,res=links_in
                             new_res=0
                             if '2160' in res or '4k' in res.lower():
                               count_2160+=1
                               new_res=2160
                             if '1080' in res:
                               count_1080+=1
                               new_res=1080
                             elif '720' in res:
                               count_720+=1
                               new_res=720
                             elif '480' in res:
                               count_480+=1
                               new_res=480
                             else:
                               count_rest+=1
                               new_res=0
                             check_super=False
                             if 'magnet:' in links and allow_debrid:
                                check_super=True
                                #logging.warning('In magnet')
                             if Addon.getSetting("super_fast")=="true" and links not in check_lk and check_super and once_fast_play==0 and silent_mode==False:
                            
                                check_lk.append(links)
                                check_r_l,str_check=get_condition(name1,links,server,new_res,tv_movie,f_result,data,original_title)
                                logging.warning(data)
                                logging.warning(check_r_l)
                                logging.warning(str_check)
                                f_ur=False
                                
                                
                                if  check_r_l :
                                  
                                    
                                    logging.warning('IN play')
                                    ur=links
                                    try:
                                        
                                        
                                        f_ur=check_cached(links)
                                    except Exception as e:
                                        logging.warning('bad link in super:'+str(e)+' '+ur)
                                        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Bad Torrent in super:'+str(e))).encode('utf-8'))
                                        global_result='Bad source try manually'
                                    
                                    logging.warning('f_ur:'+str(f_ur))
                                    if f_ur:
                                        plot='-'+data+'-'
                                        global_result='[COLOR yellow][I][B] Playing '+data+'-'+str_check+'[/B][/I][/COLOR]'
                                        try:
                                            xbmc.Player().stop()
                                            xbmc.sleep(100)
                                            once_fast_play=1
                                            if Addon.getSetting("new_window_type2")!='3':
                                                play(name,ur,' ',' ',plot,show_original_year,season,episode,original_title,name1,heb_name,show_original_year,eng_name,'0',original_title,id)
                                            else:
                                                play(name1,ur,' ',' ',plot,show_original_year,season,episode,original_title,name1,heb_name,show_original_year,eng_name,isr,original_title,id,windows_play=False,auto_fast=True,auto_play=True,f_auto_play=True)
                                            
                                        except Exception as e:
                                            #once_fast_play=0
                                            
                                            logging.warning('bad link in super2:'+str(e)+' '+ur)
                                            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'bad link in super:'+str(e))).encode('utf-8'))
                                            global_result='Bad source try manually'
              except:
                pass
              global_result="4K: [COLOR gold]%s[/COLOR] 1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]"%(count_2160,count_1080,count_720,count_480,count_rest)
              if Addon.getSetting("trailer_dp")=="true" and Addon.getSetting("new_server_dp")=="false":
                string_dp="4K: [COLOR gold]%s[/COLOR] 1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]"%(count_2160,count_1080,count_720,count_480,count_rest)
                pDialog.update(int(((num_live* 100.0)/(len(thread))) ), message=time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+' '+string_dp)
              if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                  
                     
                  
                  total=count_1080+count_720+count_480+count_rest
                  string_dp="4K: [COLOR gold]%s[/COLOR] 1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]  T: [COLOR darksalmon]%s[/COLOR] ' '[COLOR gold]SF: %s[/COLOR]' '[COLOR lightcoral]SN: %s[/COLOR]'"%(count_2160,count_1080,count_720,count_480,count_rest,total,str(count_found),len(f_result)-count_found)
                  if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                      dp.update(int(((num_live* 100.0)/(len(thread))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),string_dp, string_dp2)
                  all_s_in=(f_result,int(((num_live* 100.0)/(len(thread))) ),string_dp2.replace('Remaining sources: ',''),2,string_dp)
              xbmc.sleep(100)
              if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                   if dp.iscanceled():
                     dp_c=True
                   else:
                     dp_c=False
              else:
                   dp_c=False
              if dp_c or elapsed_time>max_time or stop_window:
                   stop_all=1
                   #for name1,items in all_sources:
                   #    items.stop_all=1
                   logging.warning('Stoping NOW')
                   num_live2=0
                   for threads in thread:
                     all_s_in=(f_result,int(((num_live2* 100.0)/(len(thread))) ),'Closing',2,threads.name)
                     if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                        dp.update(int(((num_live2* 100.0)/(len(thread))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Closing', threads.name)
                     all_s_in=(f_result,int(((num_live2* 100.0)/(len(thread))) ),'Closing',2,threads.name)
                     if threads.is_alive():
                         
                         
                         threads._Thread__stop()
                     num_live2+=1
                   break
         if still_alive==0:
           break
         if Addon.getSetting("server_dp")=='true' and silent_mode==False:
           if dp.iscanceled():
             dp_c=True
           else:
             dp_c=False
         else:
           dp_c=False
         if dp_c or elapsed_time>max_time or stop_window:
           logging.warning('Stoping NOW 2')
           for name1,items in all_sources:
               items.stop_all=1
           num_live2=0
           
           for threads in thread:
             if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                dp.update(int(((num_live2* 100.0)/(len(thread))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Closing', threads.name)
             all_s_in=(f_result,int(((num_live2* 100.0)/(len(thread))) ),'Closing',2,threads.name)
             if threads.is_alive():
                 
                 
                 threads._Thread__stop()
             num_live2+=1
           break
         xbmc.sleep(500)
    counter=0
    while 1:
        alive=0
        stop_all=1
        count_all=len(threading.enumerate())
        num_live2=0
        for thread in threading.enumerate():
          elapsed_time = time.time() - start_time
          if (thread.isAlive()):
             alive=1
             thread._Thread__stop()
             if Addon.getSetting("server_dp")=='true' and silent_mode==False:
                dp.update(int(((num_live2* 100.0)/(count_all)) ), ' Please wait2 '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Closing', thread.getName()+' - '+str(counter))
             all_s_in=(f_result,int(((num_live2* 100.0)/(count_all)) ),'Closing2',2,thread.getName()+' - '+str(counter))
        if alive==0 or counter>10:
            break
        counter+=1
        xbmc.sleep(200)
        
    if Addon.getSetting("trailer_dp")=="true" and Addon.getSetting("new_server_dp")=="false":
      xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Done searching')).encode('utf-8'))
      pDialog.close()

    all_links_fp=[]
    all_pre=[]
    z=0
    
       

    
    if Addon.getSetting("server_dp")=='true' and silent_mode==False:
      dp.close()
    f_subs=[]

    return f_result,all_links_fp,all_pre,f_subs
   except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Line:'+str(lineno)+' E:'+str(e))).encode('utf-8'))
        logging.warning('ERROR IN Looking sources:'+str(lineno))
        logging.warning('inline:'+line)
        logging.warning(e)
        logging.warning('BAD Looking sources')
        if Addon.getSetting("server_dp")=='true' and silent_mode==False:
            dp.close()


def filter_servers(url):
    url=url.lower()
    skip=[]
    
    if Addon.getSetting("re_rapid")=='true':
        if 'rapidvideo' not in url:
            skip.append(True)
        else:
            skip.append(False)
        
    if Addon.getSetting("re_google")=='true':
        if 'google' not in url and 'gdrive' not in url:
            skip.append(True)
        else:
            skip.append(False)
        
    if Addon.getSetting("re_direct")=='true':
        if 'direct' not in url and 'sratim-il' not in url and 'cdn' not in url:
            skip.append(True)
        else:
            skip.append(False)
        
    if Addon.getSetting("re_open")=='true':
        if 'openload' not in url and 'oload' not in url:
            skip.append(True)
        else:
            skip.append(False)
        
            
    if Addon.getSetting("re_stream")=='true':
        if  'streamango' not in url:
            skip.append(True)
            
    if Addon.getSetting("re_magnet")=='true':
        if  '{p-' not in url:
            skip.append(True)
        else:
            skip.append(False)
        
    if Addon.getSetting("re_vidc")=='true':
        if 'vidcloud' not in url:
            skip.append(True)
        else:
            skip.append(False)
        
    result=True
    for items in skip:
        result=result&items
    return result
def get_rest_s(time_to_save, name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local):
    global silent_mode
    
    silent_mode=True
    time_to_wait_for_rest=int(Addon.getSetting("time_to_wait_for_rest"))

    
    time.sleep(time_to_wait_for_rest)

    t=[]
    t.append((time_to_save, name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local))
  

    all_f_links,all_links_fp,all_pre,f_subs= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local,'rest','no','0', table='pages')

    return 0
def get_torrents(url):
    return url
def resolver_supported():
    resolvable_files_dir=os.path.join(xbmc.translatePath("special://home"),"addons", "script.module.resolveurl","lib","resolveurl","plugins")
   
    onlyfiles = [f for f in listdir(resolvable_files_dir) if isfile(join(resolvable_files_dir, f))]
    supported=[]
    for items in onlyfiles:
        if ".pyo" not in items and ".pyc" not in items and '__' not in items:
            supported.append(items.replace('.py',''))
    return (supported)
def get_rd_servers():
    rd_domains=[]
    if allow_debrid:
        rd_domains=[]
        try:
            import real_debrid
            rd = real_debrid.RealDebrid()
            rd_domains=(rd.getRelevantHosters())
       
            if len(rd_domains)==0:
                    Addon.setSetting('rd.client_id','')
                    rd.auth()
                    rd = real_debrid.RealDebrid()
                    rd_domains=(rd.getRelevantHosters())
        except Exception as e:
            logging.warning(e)
            pass
        if len (rd_domains)==0:
            rd_domains=[u'4shared.com', u'rapidgator.net', u'sky.fm', u'1fichier.com', u'depositfiles.com', u'hitfile.net', u'filerio.com', u'solidfiles.com', u'mega.co.nz', u'scribd.com', u'flashx.tv', u'canalplus.fr', u'dailymotion.com', u'salefiles.com', u'youtube.com', u'faststore.org', u'turbobit.net', u'big4shared.com', u'filefactory.com', u'youporn.com', u'oboom.com', u'vimeo.com', u'redtube.com', u'zippyshare.com', u'file.al', u'clicknupload.me', u'soundcloud.com', u'gigapeta.com', u'datafilehost.com', u'datei.to', u'rutube.ru', u'load.to', u'sendspace.com', u'vidoza.net', u'tusfiles.net', u'unibytes.com', u'ulozto.net', u'hulkshare.com', u'dl.free.fr', u'streamcherry.com', u'mediafire.com', u'vk.com', u'uploaded.net', u'userscloud.com',u'nitroflare.com']
        rd_domains.append('nitroflare.com')
        rd_domains.append('rapidgator.net')
        rd_domains.append('uploadgig.com')
    return rd_domains
def undo_get_rest_data(full_str):
    params=get_custom_params(full_str)
    for items in params:
        params[items]=params[items].replace(" ","%20")

    url=None
    name=None
    mode=None
    iconimage=None
    fanart=None
    description=' '
    original_title=' '
    fast_link=''
    data=0
    id=' '
    saved_name=' '
    prev_name=' '
    isr=' '
    season="%20"
    episode="%20"
    show_original_year=0
    heb_name=' '
    tmdbid=' '
    eng_name=' '
    dates=' '
    data1='[]'
    fav_status='false'
    only_torrent='no'
    only_heb_servers='0'
    new_windows_only=False
    try:
            url=urllib.unquote_plus(params["url"])
    except:
            pass
    try:
            name=urllib.unquote_plus(params["name"])
    except:
            pass
    try:
            iconimage=urllib.unquote_plus(params["iconimage"])
    except:
            pass
    try:        
            mode=int(params["mode"])
    except:
            pass
    try:        
            fanart=urllib.unquote_plus(params["fanart"])
    except:
            pass
    try:        
            description=urllib.unquote_plus(params["description"].encode('utf-8'))
    except:
            pass
    try:        
            data=urllib.unquote_plus(params["data"])
    except:
            pass
    try:        
            original_title=(params["original_title"])
    except:
            pass
    try:        
            id=(params["id"])
    except:
            pass
    try:        
            season=(params["season"])
    except:
            pass
    try:        
            episode=(params["episode"])
    except:
            pass
    try:        
            tmdbid=(params["tmdbid"])
    except:
            pass
    try:        
            eng_name=(params["eng_name"])
    except:
            pass
    try:        
            show_original_year=(params["show_original_year"])
    except:
            pass
    try:        
            heb_name=urllib.unquote_plus(params["heb_name"])
    except:
            pass
    try:        
            isr=(params["isr"])
    except:
            pass
    try:        
            saved_name=clean_name(params["saved_name"],1)
    except:
            pass
    try:        
            prev_name=(params["prev_name"])
    except:
            pass
    try:        
            dates=(params["dates"])
    except:
            pass
    try:        
            data1=(params["data1"])
    except:
            pass
    try:        
        
            fast_link=urllib.unquote_plus(params["fast_link"])
    except:
            pass
    try:        
        
            fav_status=(params["fav_status"])
    except:
            pass
    try:        
        
            only_torrent=(params["only_torrent"])
    except:
            pass
    try:        
        
            only_heb_servers=(params["only_heb_servers"])
    except:
            pass
    try:        
           
            new_windows_only=(params["new_windows_only"])
            new_windows_only = new_windows_only == "true" 
    except:
            pass
    return url,name,iconimage,mode,fanart,description,data,original_title,id,season,episode,tmdbid,eng_name,show_original_year,heb_name,isr,saved_name,prev_name,dates,data1,fast_link,fav_status,only_torrent,only_heb_servers,new_windows_only
def get_rest_data(name,url,mode,iconimage,fanart,description,video_info={},data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr=' ',generes=' ',trailer=' ',dates=' ',watched='no',fav_status='false'):
        name=name.replace("|",' ')
        description=description.replace("|",' ')
        try:
            te1=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode2="+str(mode)
            
            te2="&name="+(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description.encode('utf8'))+"&heb_name="+(heb_name)+"&dates="+(dates)
            te3="&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)
            te4="&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)
        
        
        
        
        
            u=te1 + te2 + te3 + te4.decode('utf8')+"&fav_status="+fav_status
        except:
           reload(sys)  
           sys.setdefaultencoding('utf8')
           te1=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode2="+str(mode)
            
           te2="&name="+(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description.encode('utf8'))+"&heb_name="+(heb_name)+"&dates="+(dates)
           te3="&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)
           te4="&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)
        
           u=te1 + te2 + te3 + te4.decode('utf8')+"&fav_status="+fav_status
        return u
  
def get_sources(name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,dates='',data1='[]',get_local=False,fast_link='',fav_status='false',only_torrent='no',only_heb_servers='0',new_windows_only=False,metaliq='false'):
    global imdb_global,all_s_in,close_on_error,close_sources_now,once_fast_play
    import urlparse
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    once_fast_play=0
    o_plot=plot
    rd_domains=[]
    logging.warning(name+'-'+id)
    
    logging.warning(isr)
    logging.warning('isr3:'+isr)
    if allow_debrid:
        rd_domains=cache.get(get_rd_servers, 72, table='pages')
        
        #rd_domains=requests.get('https://api.real-debrid.com/rest/1.0/hosts/domains').json()
    if season!=None and season!="%20":
       tv_movie='tv'
    
          
    else:
        tv_movie='movie'
    try:
        if 'tt' in id:
             url3='https://api.themoviedb.org/3/find/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US&external_source=imdb_id'%id
             xx=requests.get(url3).json()
            
             if tv_movie=='tv':
                if len(xx['tv_results'])>0:
                    id=str(xx['tv_results'][0]['id'])
             else:
                if len(xx['movie_results'])>0:
                    id=str(xx['movie_results'][0]['id'])

    except Exception as e:
        logging.warning(e)
        pass

    
    

    if '-Episode ' in plot and '-NEXTUP-' not in plot:

        all_d=json.loads(urllib.unquote_plus(dates))
        
        if len(all_d)<2:
            all_d=['','','']
            
        if all_d[0]==0:
          choise=['Play next episode - '+all_d[2],'Play current episode - '+all_d[1],'Open season episodes','Open season selection']
        elif all_d[2]==0:
          choise=['Play current episode - '+all_d[1],'Play previous episode - '+all_d[0],'Open season episodes','Open season selection']
        else:
          if 'magenta' not in all_d[2]:
             choise=['Play next episode - '+all_d[2],'Play current episode - '+all_d[1],'Play previous episode - '+all_d[0],'Open season episodes','Open season selection']
          else:
             choise=['[COLOR magenta]'+'Play next episode - '+'[/COLOR]'+all_d[2],'Play current episode - '+all_d[1],'Play previous episode - '+all_d[0],'Open season episodes','Open season selection']
       
        if Addon.getSetting("tv_ep_window")=='true':
            menu=[]

            menu = Chose_ep('plugin.video.destiny', heb_name,name,id,season,episode,dates,original_title)
            menu.doModal()
            ret = menu.params

            del menu
            
        else:
            ret = xbmcgui.Dialog().select("Choose episode", choise)
        
        if ret!=-1:
         
            if all_d[2]==0 or all_d[0]==0:
              prev_index=1
            else:
              prev_index=2
            
            if ret==0 and all_d[2]!=0:
              episode=str(int(episode)+1)
              from tmdb import get_episode_data
              name,plot,image=get_episode_data(id,season,episode)
              o_plot='Season %s Episode %s \n'%(season,episode)+plot
            if ret==prev_index:
              if int(episode)>1:
                episode=str(int(episode)-1)
                from tmdb import get_episode_data
                name,plot,image=get_episode_data(id,season,episode)
                o_plot='Season %s Episode %s \n'%(season,episode)+plot
            if ret==(prev_index+1):
                
                plot=plot.replace('-Episode ','')
                xbmc.executebuiltin(('Container.update("plugin://plugin.video.destiny/?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode2=8",return)'%(name,urllib.quote_plus(url),icon,image,urllib.quote_plus(plot),year,original_title,id,season,tmdbid,show_original_year,heb_name,isr)))
                '''
                get_episode(name,url,iconimage,image,plot,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr)
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                xbmcplugin.endOfDirectory(int(sys.argv[1]))
                return 0
                '''
                return 'ok',[] 
                sys.exit()
            if ret==(prev_index+2):
                plot=plot.replace('-Episode ','')
                logging.warning('OPEN LAST')
                xbmc.executebuiltin(('Container.update("plugin://plugin.video.destiny/?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode2=7"),return'%(name,urllib.quote_plus(url),icon,image,urllib.quote_plus(plot),year,original_title,id,season,tmdbid,show_original_year,heb_name,isr)))
                '''
                get_seasons(name,url,iconimage,image,plot,data,original_title,id,heb_name,isr)
                xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
                xbmcplugin.endOfDirectory(int(sys.argv[1]))
                return 0
                '''
                return 'ok',[]
                sys.exit()
             
        else:
          sys.exit()
          return 'ENDALL',[]
    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode

    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
    logging.warning('2')
    time_to_save=int(Addon.getSetting("save_time"))
    search_done=0
    #all_f_links=c_get_sources(name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local=False,fav_status=fav_status,only_torrent=only_torrent,only_heb_servers=only_heb_servers)
    #logging.warning(all_f_links)
    #sys.exit()
    
    if 'Filtered sources' in name:
        filter_mode=True
    else:
        filter_mode=False
  
    if 'Rest of results' in name:
        filter_loc='rest'
        rest_test=' Rest of results '
    else:
        filter_loc='rest2'
        rest_test=''
    all_d_new=[]
    logging.warning('3')
    all_d_new.append((name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,dates,data1))
    if tv_movie=='movie':
        fav_search_f=Addon.getSetting("fav_search_f")
        fav_servers_en=Addon.getSetting("fav_servers_en")
        fav_servers=Addon.getSetting("fav_servers")
       
      
    else:
        fav_search_f=Addon.getSetting("fav_search_f_tv")
        fav_servers_en=Addon.getSetting("fav_servers_en_tv")
        fav_servers=Addon.getSetting("fav_servers_tv")
      
              
    logging.warning('4')
    if fav_status!='rest':
        if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0):
            fav_status='true'
        else:
            fav_status='false'

    name=name.replace('[COLOR red]','').replace('[COLOR white]','').replace('[/COLOR]','')
    o_year=year
    if plot==None:
      plot=' '
    if 'NEXTUP' in plot:
      nextup=True
    else:
      nextup=False
    o_name=name
    
    try:
      if season!=None and season!="%20":
        name=original_title
      
      d=[]
      d.append((name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local,fav_status,only_torrent,only_heb_servers))

      
      all_f_links,all_links_fp,all_pre,f_subs= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local,fav_status,only_torrent,only_heb_servers, table='pages')

      if tv_movie=='tv':
        fav_first=Addon.getSetting("fav_search_rest_tv")
      else:
        fav_first=Addon.getSetting("fav_search_rest")
      rest_of_data=[]
      rest_found=0
      if fav_status=='true' and  Addon.getSetting("all_t")!='1' and only_torrent!='yes' and 'Magnet links' not in o_name  :
          found_links=0
          for name_f in all_f_links:
           if found_links==1:
             break
           if name_f!='subs' :
         
            
            for name,link,server,quality in all_f_links[name_f]['links']:
                found_links=1
                break
          
          if found_links==0 and fav_status=='true':
            all_f_links,all_links_fp,all_pre,f_subs= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local,'rest','no','0', table='pages')
            rest_found=1
          elif fav_status=='true' and  fav_first=='true':
            
            rest_of_data.append((time_to_save, original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local))
          
            #thread[0].start()
      a=1
    
    except Exception as e:
      import linecache
      exc_type, exc_obj, tb = sys.exc_info()
      f = tb.tb_frame
      lineno = tb.tb_lineno
      filename = f.f_code.co_filename
      linecache.checkcache(filename)
      line = linecache.getline(filename, lineno, f.f_globals)
      
      logging.warning('ERROR IN Sources Search:'+str(lineno))
      logging.warning('inline:'+line)
      logging.warning(e)
      logging.warning('BAD Sources Search')
      xbmcgui.Dialog().ok('Error occurred',' Sources Search Error '+str(e))
      close_sources_now=1
      return 0
      xbmcgui.Dialog().ok('Error occurred',' Cache was cleaned try again '+str(e))
    
      
    logging.warning('5')
    next_ep=[]
    if Addon.getSetting("dp")=='true' and silent_mode==False:
        dp = xbmcgui . DialogProgress ( )
        dp.create('Please wait','Ordering sources', '','')
        dp.update(0, 'Please wait','Ordering sources', '' )
    all_s_in=({},0,'Ordering sources',2,'')
    start_time=time.time()
    if get_local==False:
     if season!=None and season!="%20":
      episode1=str(int(episode)+1)
      if len(episode1)==1:
          episode_n1="0"+episode1
      else:
           episode_n1=episode1
      from tmdb import get_episode_data
      name1,plot1,image1=get_episode_data(id,season,episode1)
      if name1!=' ':    
        
        f_name=''
        
        
        addDir3( f_name+'[COLOR gold][I]Open next episode - %s[/I][/COLOR]'%episode1, url,4,icon,image1,plot1+'-NEXTUP-',data=year,original_title=original_title,season=season,episode=episode1,id=id,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=dates)
        next_ep.append(get_rest_data( f_name+'[COLOR gold][I]Open next episode - %s[/I][/COLOR]'%episode1, url,4,icon,image1,plot1+'-NEXTUP-',data=year,original_title=original_title,season=season,episode=episode1,id=id,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=dates))
    
    


    
    #xbmc.Player().stop()
  
   
    logging.warning('6')
    all_data=[]
    video_data={}
    video_data['title']=name
    video_data['poster']=image
    video_data['plot']=plot
    video_data['icon']=icon
    video_data['year']=year
    if plot==None:
      plot=' '

   
    if Addon.getSetting("lang")=="1":
      lang='en'
    else:
      lang='he'
    url2=None
   
    
    save_fav(id,tv_movie)
    if Addon.getSetting("dp")=='true' and silent_mode==False:
        elapsed_time = time.time() - start_time
        dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Updating DB', '')
    all_s_in=({},0,'Updating DB',2,'')
    if tv_movie=='tv':
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' and type='%s' and season='%s' and episode='%s'"%(original_title.replace("'"," "),tv_movie,season,episode))
        
        match = dbcur.fetchone()
        logging.warning('hislink')
        logging.warning(match)
        if match==None:
          
          dbcur.execute("INSERT INTO AllData Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'"," "),url,icon,image,plot.replace("'"," "),year,original_title.replace("'"," "),season,episode,id,eng_name.replace("'"," "),show_original_year,heb_name.replace("'"," "),isr,tv_movie))
          dbcon.commit()
          
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'"," "),tv_movie))

        match = dbcur.fetchone()
        if match==None:
          
          dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'"," "),url,icon,image,plot.replace("'"," "),year,original_title.replace("'"," "),season,episode,id,eng_name.replace("'"," "),show_original_year,heb_name.replace("'"," "),isr,tv_movie))
          dbcon.commit()
         
        else:
          dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s' and season='%s' and episode='%s'"%(original_title.replace("'"," "),tv_movie,season,episode))

          match = dbcur.fetchone()
         
          if match==None:
            dbcur.execute("UPDATE Lastepisode SET season='%s',episode='%s',image='%s',isr='%s' WHERE original_title = '%s' and type='%s'"%(season,episode,image,isr,original_title.replace("'"," "),tv_movie))
            dbcon.commit()
            
            #if nextup==False:
              
            #  xbmc.executebuiltin('Container.Refresh')

    else:
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' and type='%s'"%(original_title.replace("'"," "),tv_movie))

        match = dbcur.fetchone()
        logging.warning('hislink')
        logging.warning(match)
        if match==None:
          
          dbcur.execute("INSERT INTO AllData Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'"," "),url,icon,image,plot.replace("'"," "),year,original_title.replace("'"," "),season,episode,id,eng_name.replace("'"," "),show_original_year,heb_name.replace("'"," "),isr,tv_movie))
          dbcon.commit()
          logging.warning('Done hislink')
        #else:
          
        #  dbcur.execute("UPDATE AllData SET season='%s',episode='%s' WHERE original_title = '%s' and type='%s'"%(season,episode,original_title,tv_movie))
        #  dbcon.commit()

    plot_o1=plot
    logging.warning('7')
    all_only_heb={}
    count_n=0
    count_t=0
    all_rd_s={}
    all_torrent_s={}
    all_rd_servers=[]
    count_r=0
    
    all_hebdub_servers=[]

    all_removed=[]
    all_lk=[]
    if filter_mode:
   
        dbcur.execute("SELECT * FROM %s"%filter_loc)
        all_new = dbcur.fetchone()[0].decode('base64')
        all_new=json.loads(all_new)
    all_t_links=[]
    all_heb_links=[]
    duplicated=0
    logging.warning('8')
    all_mag={}
    all_mag[0]=[]
    
    all_lk2=[]
    counter_hash=0
    r_list=[]
    page_index=0
    checked_cached=0
    if Addon.getSetting("check_cached")=='true' and allow_debrid:
        try:
            for name_f in all_f_links:
              if name_f!='subs' :
                for name,link,server,quality in all_f_links[name_f]['links']:
                    if Addon.getSetting("dp")=='true' and silent_mode==False:
                       elapsed_time = time.time() - start_time
                       dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Updating links , check cached', name)
                    if link not in all_lk2:
                        all_lk2.append(link)
                        if 'magnet' in link:
                            try:
                                hash = str(re.findall(r'btih:(.*?)&', link)[0].lower())
                            except:
                                hash =link.split('btih:')[1]
                            all_mag[page_index].append(hash)
                            counter_hash+=1
                            if counter_hash>150:
                                page_index+=1
                                all_mag[page_index]=[]
                                counter_hash=0
            logging.warning('all_mag:'+str(len(all_mag)))
            all_hased=[]
            logging.warning(page_index)
            import real_debrid
            rd = real_debrid.RealDebrid()
            for items in all_mag:
                
               
                
                hashCheck = rd.checkHash(all_mag[items])
                for hash in hashCheck:
                    if Addon.getSetting("dp")=='true' and silent_mode==False:
                       elapsed_time = time.time() - start_time
                       dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Updating links , check cached', hash)
                    if 'rd' in hashCheck[hash]:
                       if len(hashCheck[hash]['rd'])>0:
                            all_hased.append(hash)
                
            for name_f in all_f_links:
                    index=0
                    if name_f!='subs' :
                     for name,link,server,quality in all_f_links[name_f]['links']:
                        
                        if 'magnet' in link:
                            try:
                                hash = str(re.findall(r'btih:(.*?)&', link)[0].lower())
                            except:
                                hash =link.split('btih:')[1]
                            if hash in all_hased:
                                
                                all_f_links[name_f]['links'][index]=['Cached '+name,link,server,quality]
                        index+=1
            checked_cached=1
        except Exception as e:
            checked_cached=0
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            xbmc.executebuiltin(u'Notification(%s,%s)' % ('Destiny', 'ERROR IN Cached test:'+str(lineno)))
            logging.warning('ERROR IN Cached test:'+str(lineno))
            logging.warning('inline:'+line)
            logging.warning(e)
            logging.warning('BAD Cached test')
    for name_f in all_f_links:

       if name_f!='subs' :
     
        
        for name,link,server,quality in all_f_links[name_f]['links']:
            
           if checked_cached==1 and Addon.getSetting("check_cached_r")=='true' and allow_debrid:
             if 'magnet' in link and 'Cached ' not in name:
                continue
           
           if Addon.getSetting("shrink")=='true':
                if link in all_lk:
                    duplicated+=1
                    continue
                else:
                 all_lk.append(link)
         
           if filter_mode:
             if link not in all_new:
                continue
           else:
               if "," in Addon.getSetting("unfilter"):
                 unfilter=Addon.getSetting("unfilter").split(",")
               else:
                 if len(Addon.getSetting("unfilter"))>0:
                    unfilter=[Addon.getSetting("unfilter")]
                 else:
                   unfilter=[]
           
               if Addon.getSetting("remove_all")=='true' and (name_f not in unfilter):
               
                check=filter_servers(server)
               
                if check:
               
                    all_removed.append(link)
                    continue
           
           fixed_q=fix_q(quality)
           
           if Addon.getSetting("dp")=='true' and silent_mode==False:
               elapsed_time = time.time() - start_time
               dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Updating links , Duplicated  - %s'%str(duplicated), name)
           all_s_in=({},0,' Duplicated  - %s'%str(duplicated),2,name)
           se='-%s-'%name_f  
          
           if all_f_links[name_f]['torrent']==True:
            
             if link in all_t_links:
                continue
             all_t_links.append(link)
             all_torrent_s[count_t]={}
             all_torrent_s[count_t]['name']=name.decode('utf-8','ignore')
             all_torrent_s[count_t]['link']=link.decode('utf-8','ignore')
             all_torrent_s[count_t]['server']=server.decode('utf-8','ignore')
             all_torrent_s[count_t]['quality']=quality.decode('utf-8','ignore')
             all_torrent_s[count_t]['icon']=icon.decode('utf-8','ignore')
             all_torrent_s[count_t]['image']=image.decode('utf-8','ignore')
             all_torrent_s[count_t]['plot']='[COLOR gold]'+server.decode('utf-8','ignore')+'[/COLOR]\n'+plot.decode('utf-8','ignore')
             all_torrent_s[count_t]['year']=year.decode('utf-8','ignore')
             all_torrent_s[count_t]['season']=season.decode('utf-8','ignore')
             all_torrent_s[count_t]['episode']=episode.decode('utf-8','ignore')
             all_torrent_s[count_t]['id']=id
             all_torrent_s[count_t]['name_f']=name_f
             #all_torrent_s[count_t]['color']=all_f_links[name_f]['color']
             count_t+=1
           elif all_f_links[name_f]['rd']==True:
            
             all_rd_s[count_r]={}
             all_rd_s[count_r]['name']=name
             all_rd_s[count_r]['link']=link
             all_rd_s[count_r]['server']=server
             all_rd_s[count_r]['quality']=quality
             all_rd_s[count_r]['icon']=icon
             all_rd_s[count_r]['image']=image
             all_rd_s[count_r]['plot']=plot
             all_rd_s[count_r]['year']=year
             all_rd_s[count_r]['season']=season
             all_rd_s[count_r]['episode']=episode
             all_rd_s[count_r]['id']=id
             all_rd_s[count_r]['name_f']=name_f
             #all_rd_s[count_r]['color']=all_f_links[name_f]['color']
             count_r+=1
            
             #pre=all_pre[all_links_fp.index(link)]
           
             if name_f not in all_rd_servers:
                all_rd_servers.append(name_f)
           
           else:
             plot=plot_o1
             
             #pre=all_pre[all_links_fp.index(link)]
           
           check=False
        
           
           if 1:
             pre=''
  
    
             if '-magnet-' in server:
                se=' magnet '+se
                color='gold'
             else:
                color='white'
                
             all_data.append(('[COLOR %s][%s] '%(color,name_f)+name.decode('utf8','ignore')+" - "+server+'[/COLOR]'+' sss '+name_f+' sss ', str(link),icon,image,plot,show_original_year,quality,se,fixed_q,name,pre,server))
    logging.warning('9')
    if Addon.getSetting("dp")=='true' and silent_mode==False:
        elapsed_time = time.time() - start_time
        dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Ordering links', ' ')
    all_s_in=({},0,'Ordering links',2,'')
    
    
    if Addon.getSetting("order_torrents_new")=='true' and (Addon.getSetting("all_t")=='1' or only_torrent=='yes' or 'Magnet links' in o_name) and (Addon.getSetting("magnet")=='true' or only_torrent=='yes'):
         regex='{P-(.+?)/S-(.+?)}'
         all_data2=[]
         for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier in all_data:
             
             peers=0
             seeds=0
             seeds_pre=re.compile(regex).findall(name)
             if len(seeds_pre)>0:
                 seeds=seeds_pre[0][1].replace(' ','')
                 peers=re.compile(regex).findall(name)[0][0].replace(' ','')
            
                 seeds=seeds.replace(',','')
                 peers=peers.replace(',','')
                 try:
                    a=int(seeds)
                 except:
                   seeds=0
             all_data2.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,int(seeds),peers,supplier))
         all_data2=sorted(all_data2, key=lambda x: x[11], reverse=True)
         all_data=[]
         for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,seeds,peers,supplier in all_data2:
            all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier))
    else:
      all_fv=[]
      all_rest=[]
      if Addon.getSetting("fav_servers_en")=='true'  and  tv_movie=='movie':
        all_fv_servers=Addon.getSetting("fav_servers").split(',')
      elif Addon.getSetting("fav_servers_en_tv")=='true'  and  tv_movie=='tv':

        all_fv_servers=Addon.getSetting("fav_servers_tv").split(',')
      else:
        all_fv_servers=[]
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier in all_data:
        if server.replace('-','') in all_fv_servers:
            all_fv.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier))
        else:
            all_rest.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier))
      all_fv=sorted(all_fv, key=lambda x: x[8], reverse=False)
      
      all_rest=sorted(all_rest, key=lambda x: x[8], reverse=False)
      all_data=[]
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier in all_fv:
         all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier))
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier in all_rest:
         all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier))
         
    logging.warning('10')
    if get_local==True:
     
     return all_data,rest_of_data
    
    all_in=[]
    if imdb_global==None:
      imdb_global=id
    else:
      if 'tt' not in imdb_global:
        imdb_global=id
   
   
          
    magnet_ofresult=''
    if  Addon.getSetting("magnet")=='true' and filter_loc!='rest':
    
      if  (Addon.getSetting("all_t")=='2' and only_torrent!='yes' )and  'Magnet links' not in o_name :
       dbcur.execute("DELETE FROM torrents")
       dbcon.commit()

       dbcur.execute("INSERT INTO torrents Values ('%s')"%(json.dumps(all_torrent_s).encode('base64')))
       dbcon.commit()
       magnet_ofresult=get_rest_data( '[COLOR aqua][I]Magnet links -(%s)[/I][/COLOR]'%len(all_t_links), 'torrents',4,icon,image,plot+'-NEXTUP-',data=o_year,original_title=original_title,season=season,episode=episode,id=id,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=dates,fav_status=fav_status)
 
       #addDir3( '[COLOR aqua][I]Magnet links -(%s)[/I][/COLOR]'%len(all_torrent_s), 'torrents',21,icon,image,plot,data=year,original_title=json.dumps(all_subs),season=season,episode=episode,id=imdb_global)
       
       #all_d_new.append((name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,dates,data1))
       addDir3( '[COLOR aqua][I]Magnet links -(%s)[/I][/COLOR]'%len(all_t_links), 'torrents',4,icon,image,plot,data=o_year,original_title=original_title,season=season,episode=episode,id=id,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=dates,fav_status=fav_status)
      #elif  (Addon.getSetting("all_t")=='1' or only_torrent=='yes') :
        
      #  play_by_subs('[COLOR aqua][I]Magnet links -(%s)[/I][/COLOR]'%len(all_torrent_s),json.dumps(all_torrent_s),icon,image,name.decode('utf8','ignore')+plot.decode('utf8','ignore'),year,json.dumps(all_subs),season,episode,imdb_global,'','',original_title,one_list=True)
    playingUrlsList = []
    t=0
    '''
    if Addon.getSetting("auto_enable")=='true':
        for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier in all_data:
          t=t+1
          if plot==None:
             plot=' '

          
          playingUrlsList.append(link+'$$$$$$$'+server+'$$$$$$$'+q+'$$$$$$$'+saved_name+'$$$$$$$'+'[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot)
    '''
    logging.warning('11')
    if Addon.getSetting("chapi_enable")=='true' :
        if season!=None and season!="%20":
           url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,'1248868d7003f60f2386595db98455ef')
        else:
         
           url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,'1248868d7003f60f2386595db98455ef')
        try:
            imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
        except:
            imdb_id=" "
         
            
        url_ch=''
        if season!=None and season!="%20":
              url_pre='http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s&language=en'%imdb_id.replace('tt','')
              html2=requests.get(url_pre).content
              pre_tvdb = str(html2).split('<seriesid>')
              if len(pre_tvdb) > 1:
                    tvdb = str(pre_tvdb[1]).split('</seriesid>')
                    url_ch='plugin://plugin.video.chappaai/tv/play/%s/%s/%s/library'%(tvdb[0],season,episode)
                   
        else:
            url_ch=('plugin://plugin.video.%s/movies/play/imdb/%s/library'%(Addon.getSetting("metaliq_version_for_s"),imdb_id))
        if url_ch!='':
           addLink( "Open in Metalliq",url_ch,41,False,' ',' ',"Open in metaliq")
    if Addon.getSetting("auto_enable")=='true':
      addLink( 'Auto Play', json.dumps(playingUrlsList),6,False,icon,image,plot,data=year,original_title=original_title.replace("%20"," "),season=season,episode=episode,id=id,saved_name=original_title,prev_name=o_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year,isr=isr)
    if Addon.getSetting("debugmode")=='true':
      try:
       
        a=1
      except:
       pass
    rest_ofresult=[]
    rd_ofresult=[]
    if fav_status=='true' and rest_found==0 and only_torrent!='yes' and 'Magnet links' not in o_name :
     
        rest_ofresult=get_rest_data('Rest of Results',all_d_new[0][1],4,all_d_new[0][2],all_d_new[0][3],all_d_new[0][4]+'-NEXTUP-',data=all_d_new[0][5],original_title=all_d_new[0][6],season=all_d_new[0][7],episode=all_d_new[0][8],id=all_d_new[0][9],heb_name=all_d_new[0][12],eng_name=all_d_new[0][10],show_original_year=all_d_new[0][11],isr=all_d_new[0][13],dates=all_d_new[0][14],fav_status='rest')
        addDir3('Rest of Results',all_d_new[0][1],4,all_d_new[0][2],all_d_new[0][3],all_d_new[0][4]+'-NEXTUP-',data=all_d_new[0][5],original_title=all_d_new[0][6],season=all_d_new[0][7],episode=all_d_new[0][8],id=all_d_new[0][9],heb_name=all_d_new[0][12],eng_name=all_d_new[0][10],show_original_year=all_d_new[0][11],isr=all_d_new[0][13],dates=all_d_new[0][14],fav_status='rest')
    if Addon.getSetting("remove_all")=='true' and len(all_removed)>0 and filter_mode==False:
       dbcur.execute("DELETE FROM %s"%filter_loc)
       dbcon.commit()

       dbcur.execute("INSERT INTO %s Values ('%s')"%(filter_loc,json.dumps(all_removed).encode('base64')))
       dbcon.commit()
     
       addDir3('Filtered Sources -(%s)'%len(all_removed)+rest_test,all_d_new[0][1],4,all_d_new[0][2],all_d_new[0][3],all_d_new[0][4],data=all_d_new[0][5],original_title=all_d_new[0][6],season=all_d_new[0][7],episode=all_d_new[0][8],id=all_d_new[0][9],heb_name=all_d_new[0][12],eng_name=all_d_new[0][10],show_original_year=all_d_new[0][11],isr=all_d_new[0][13],dates=all_d_new[0][14],fav_status=fav_status)
       
     
    result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.GetItems", "params": { "properties": [ "showlink", "showtitle", "season", "title", "artist" ], "playlistid": 1}, "id": 1}')

    j_list=json.loads(result)
    
    if 'RD Links' not in o_name and Addon.getSetting("rd_menu_enable")=='true' and  Addon.getSetting("rdsource")=='true':
      
      addDir3( 'RD Links', 'RD Links',4,icon,image,plot,data=o_year,original_title=original_title,season=season,episode=episode,id=id,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=dates,fav_status=fav_status)
      rd_ofresult=get_rest_data( 'RD Links', 'RD Links',4,icon,image,plot+'-NEXTUP-',data=o_year,original_title=original_title,season=season,episode=episode,id=id,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=dates,fav_status=fav_status)
    if Addon.getSetting("new_source_menu")=='false':
        if (Addon.getSetting("fast_play2_tv")=='true' and tv_movie=='tv') or (Addon.getSetting("fast_play2_movie")=='true' and tv_movie=='movie'):
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
    if (Addon.getSetting("fast_play2_tv")=='true' and tv_movie=='tv') and Addon.getSetting("new_source_menu")=='false':
        addDir3( 'Season Episodes','www',102,icon,image,plot,data=year,original_title=original_title,id=id,season=season,tmdbid=id,show_original_year=year,heb_name=heb_name,isr=isr)
    once=0
    all_lists=[]
    f_link2=''

    m=[]
    n=[]
    n_magnet=[]
    if len(rest_ofresult)>0:
        n.append(rest_ofresult)
    if len(magnet_ofresult)>0:
        n_magnet.append(magnet_ofresult)
    r_results=[]
    if len(rd_ofresult)>0:
        r_results.append(rd_ofresult)
        
    count_magnet=0
    all_items=[]
    f_plot=''
    max_q='99'
    max_q_t=['2160','1080','720','480','360']
    if Addon.getSetting("auto_q_source")=='true':
        if tv_movie=='tv':
          max_q=Addon.getSetting("max_quality_t")
        else:
          max_q=Addon.getSetting("max_quality_m")
        max_q_v=max_q_t[int(max_q)]
    logging.warning('12')
    for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier in all_data:
      
      if Addon.getSetting("dp")=='true' and silent_mode==False:
          elapsed_time = time.time() - start_time
         
          dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Loading links - duplicates  - %s'%str(duplicated), name)
      
      all_s_in=({},0,'Loading links - duplicates  - %s'%str(duplicated),2,name)
      if server==None:
        server=' '
      q=q.replace('p','').replace('4K','2160').replace('4k','2160')
      try:
         a=int(q)
      except:
          q='0'
      if max_q!='99':

           if int(q)>int(max_q_v):
             
             continue
      if q==None:
        q=' '
      if plot==None:
        plot=' '
      name=name.replace("|"," ").replace("  "," ").replace("\n","").replace("\r","").replace("\t","").strip()

      if fast_link!='':
     
        if link==fast_link:
          
          all_f_data=((name,fast_link,icon,image,'[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot,o_year,season,episode,original_title,heb_name,show_original_year,eng_name,isr,id))
          f_link2=('%s?name=%s&mode2=5&url=%s&data=%s&season=%s&episode=%s&original_title=%s&saved_name=%s&heb_name=%s&show_original_year=%s&eng_name=%s&isr=%s&id=%s&description=%s&iconimage=%s&fanart=%s'%(sys.argv[0],name,urllib.quote_plus(fast_link),o_year,season,episode,original_title,name,heb_name,show_original_year,eng_name,isr,id,urllib.quote_plus(('[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot).encode('utf8')),icon,image))
          
          
      
      if 1:#(Addon.getSetting("fast_play2_tv")=='true' and tv_movie=='tv') or (Addon.getSetting("fast_play2_movie")=='true' and tv_movie=='movie'):
          #if Addon.getSetting("new_source_menu")=='false':
              link2=('%s?name=%s&mode=5&url=%s&data=%s&season=%s&episode=%s&original_title=%s&saved_name=%s&heb_name=%s&show_original_year=%s&eng_name=%s&isr=%s&id=%s&description=%s'%(sys.argv[0],name,urllib.quote_plus(link),o_year,season,episode,original_title,name,heb_name,show_original_year,eng_name,isr,id,urllib.quote_plus(('[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot).encode('utf8'))))
              
              added=''
              
              listItem=xbmcgui.ListItem(added+'[COLOR yellow]'+str(q)+'[/COLOR]|[COLOR magenta]'+server+'[/COLOR]|[COLOR gold]'+supplier.replace("Openload","vumoo")+'|[/COLOR]'+clean_name(name,1), iconImage=icon, thumbnailImage=image,path=link2)
              listItem.setInfo('video', {'Title': name})
              
              playlist.add(url=link2, listitem=listItem)
              all_lists.append(listItem)
      
           
      
      if 'RD Links' in o_name:
        if 'magnet' not in server:
            try:
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                if host not in rd_domains:
                    
                        continue
            except:
                pass
            
      if 'Magnet links' in o_name and 'magnet' not in server:
        
        continue
      
      
      size='0'
      if 'magnet' in server:
         
         saved_name=name.split('{P')[0]
         regex=' -.+?- (.+?) GB'
         
         try:
             size=re.compile(regex).findall(name)[0]
             
             #size=size.split('-')[2]
         except:
           
           size='0'
         
         max_size=int(Addon.getSetting("size_limit"))
         try:
             size=re.findall("[-+]?\d*\.\d+|[-+]?\d+", size)[0]
             if float(size)>max_size:
                continue
         except:
            pass
         regex='{P-(.+?)/S-(.+?)}'
         try:
             seeds=re.compile(regex).findall(name)[0][1].replace(' ','')
             peers=re.compile(regex).findall(name)[0][0].replace(' ','')
             try:
                s=int(seeds)
             except:
                seeds='0'
             try:
                s=int(peers)
             except:
                peers='0'
             seeds=seeds.replace(',','')
             peers=peers.replace(',','')
         except:
            peers='0'
            seeds='0'
            pass
         
         if int(seeds)>=int(Addon.getSetting("min_seed")):
            if peers=='0' and seeds=='0':
                server='magnet -  [COLOR lightgreen]%sGB[/COLOR]-'%(size)
            else:
                server='magnet - S%s -  [COLOR lightgreen]%sGB[/COLOR]-'%(seeds,size)
            count_magnet+=1
         else:
            
            continue
      tes_mag=re.compile('- P(.+?)/S(.+?) -').findall(server)

      if ('magnet' in server or len(tes_mag)>0) and (Addon.getSetting("all_t")=='2' ) and Addon.getSetting("magnet")=='true' and 'Magnet links' not in o_name :
          if only_torrent!='yes':
            continue
      
      if len(Addon.getSetting("ignore_ser"))>0:
          ignore_server=Addon.getSetting("ignore_ser").split(",")
          ignore=0

          for items in ignore_server:
            
              if items.lower() in name.lower():
                 ignore=1
                 
                 break
          if ignore==1:
             continue
      
      #if  Addon.getSetting("rd_menu_enable")=='true' and  Addon.getSetting("rdsource")=='true' and 'RD SOURCE' in server:
      #  continue
      if ('magnet:' in link and allow_debrid):
            server='[COLOR gold] ☻ RD ☻ '+server+'[/COLOR]'
      if allow_debrid and '//' in link:
        
        
        try:
            host = link.split('//')[1].replace('www.','')
            host = host.split('/')[0].lower()
            if host in rd_domains:
                server='[COLOR gold] ☻ RD ☻ '+server+'[/COLOR]'
        except:
            pass
      pre=0
      if 1:
        
        #regex='\] (.+?)-'
        #o_name1=re.compile(regex).findall(name)[0].replace('%20','.').replace(' ','.')
   
        if Addon.getSetting("source_sim")=='true':
           if pre==0:
             n1='[COLOR lightblue]'+server+'[/COLOR]  '+'[COLOR lightgreen]◄'+q+'►[/COLOR]'
           else:
           
              n1='[COLOR gold][I]'+str(pre)+'%[/I][/COLOR] '+'[COLOR lightblue]'+server+'[/COLOR]  '+'[COLOR lightgreen]◄'+q+'►[/COLOR]'
           p1=name+'\n[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot
        else:
           if pre==0:
             n1= name
           else:
              n1='[COLOR gold][I]'+str(pre)+'%[/I][/COLOR]-'+ name
           p1='[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot
        
        if only_torrent=='yes':
   
            name=remove_color(name)
            name=name.replace('magnet_','').replace('.py','')
            n1=('[COLOR gold]'+str(pre)+'%[/COLOR]  [COLOR gold]◄'+q+'►[/COLOR][COLOR lightblue][/COLOR] '+name)

        if ((Addon.getSetting("new_source_menu")=='true' and only_torrent!='yes' ) or new_windows_only) and  f_link2=='':
            name=name
          
            p1=p1
            m.append((name,link,icon,image,p1,show_original_year,q,server,q,saved_name,pre,supplier,size+' GB'))
            f_plot=p1
            all_items.append(addLink(n1, link,5,False,icon,image,p1,data=o_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=o_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year,collect_all=True,isr=isr))
        else:
            
            all_items.append(addLink(n1, link,5,False,icon,image,p1,data=o_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=o_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year,collect_all=True,isr=isr))
      else:
         
         if only_torrent=='yes':
            name=remove_color(name)
   
            name=('[COLOR gold]'+str(pre)+'%[/COLOR]  [COLOR gold] ◄'+q+'► [/COLOR][COLOR lightblue] [/COLOR] '+name+'$$$$$$$'+link)
         if ((Addon.getSetting("new_source_menu")=='true' and only_torrent!='yes') or new_windows_only) and  f_link2=='':
            name=name
            f_plot='[COLOR lightgreen]◄'+q+'►[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot
            f_plot=f_plot
            
            m.append((name,link,icon,image,f_plot,show_original_year,q,server,q,saved_name,pre,supplier,size+' GB'))
            all_items.append(addLink( name, link,5,False,icon,image,'[COLOR lightgreen]◄'+q+'►[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot,data=o_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=o_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year,collect_all=True,isr=isr))
         else:
             all_items.append(addLink( name, link,5,False,icon,image,'[COLOR lightgreen]◄'+q+'►[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot,data=o_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=o_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year,collect_all=True,isr=isr))
    logging.warning('13')
   
        
    if new_windows_only==False  or  f_link2!='' or only_torrent=='yes' or once_fast_play==1:
        
        xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_items,len(all_items))
    all_s_in=( {},100 ,'',4,'')
    if once_fast_play>0:
        close_sources_now=1
    if Addon.getSetting("dp")=='true' and silent_mode==False:
                dp.close()
    if ((Addon.getSetting("fast_play2_tv")=='true' and tv_movie=='tv') or (Addon.getSetting("fast_play2_movie")=='true' and tv_movie=='movie')) and Addon.getSetting("new_source_menu")=='false':
       a=1
    elif f_link2!='':
        logging.warning('PLAY MEDIA')
        #xbmc.executebuiltin(('XBMC.PlayMedia("%s")'%f_link2))
 
        name,fast_link,iconimage,image,description,data,season,episode,original_title,heb_name,show_original_year,eng_name,isr,id=all_f_data
        play(name,fast_link,iconimage,image,description,data,season,episode,original_title,name,heb_name,show_original_year,eng_name,isr,original_title,id,windows_play=True,auto_fast=False,nextup=True)
        logging.warning('DONE PLAY MEDIA')
        return 990,rest_of_data
    search_done=1
    check=False
    if (tv_movie=='tv' and Addon.getSetting("video_in_sources_tv")=='true') or (tv_movie=='movie' and Addon.getSetting("video_in_sources")=='true'):
        check=True
            
    if (Addon.getSetting("trailer_wait")=='true' and Addon.getSetting("trailer_dp")=='true') or (Addon.getSetting("video_in_s_wait")=='true' and check and  Addon.getSetting("new_server_dp")=='true'):
       while xbmc.Player().isPlaying():
         xbmc.sleep(100)
    if Addon.getSetting("torrent_warning")=='true' and Addon.getSetting("magnet")=='true' and Addon.getSetting("rdsource")=='false':
    
        xbmcgui.Dialog().ok('Warning', 'Using TORRENTS without RD or VPN is not recommended in some countries\n this warning can be disabled in the settings')
    logging.warning('once_fast_play33:'+str(once_fast_play))
    check_show=False
    if not xbmc.Player().isPlaying:
        check_show=True
    elif once_fast_play==0:
        check_show=True
    if (Addon.getSetting("new_source_menu")=='true' and only_torrent!='yes' and check_show ) or new_windows_only :
             if f_link2=='':
       

                if len(dates)>0 and dates!='%20' and dates!='"%20"' and metaliq=='false':
                    l=get_rest_data('Series Tracker'.decode('utf8'),'tv',32,domain_s+'pbs.twimg.com/profile_images/873323586622078976/Z0BfwrYm.jpg',' ','Watched series'.decode('utf8'),isr=isr)
                    xbmc.executebuiltin('Container.Refresh(%s)'%l)
                    #xbmc.executebuiltin('Container.Refresh()')
             
                res=new_show_sources(m,o_year,o_plot,eng_name,episode,image,heb_name,icon,id,prev_name,original_title,season,show_original_year,n,rest_of_data,n_magnet,r_results,str(count_magnet),next_ep,str(len(all_heb_links)),only_torrent,isr)
                if res=='END':
                    return 'ENDALL',[]
    
    
    
   

    status_pl='0'                 
    logging.warning('14')
    #sys.exit()
    if 'items' in (j_list['result']):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": { "playlistid": 0 }, "id": 1}')
      
    if (Addon.getSetting("fast_play2_tv")=='true' and tv_movie=='tv') or (Addon.getSetting("fast_play2_movie")=='true' and tv_movie=='movie'):
      if Addon.getSetting("new_source_menu")=='false' and check_show==False: 
        if 'items' in (j_list['result']) and once_fast_play==0:
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": { "playlistid": 0 }, "id": 1}')
        if Addon.getSetting("new_source_menu")=='false':
           if Addon.getSetting("dp")=='true' and silent_mode==False:
                dp.close()
           xbmc.Player().stop()
        
           if not 'items' in (j_list['result']):
              xbmc.Player().play(playlist,windowed=False)
           if Addon.getSetting("src_disp")=='false':
                status_pl='ENDALL'
           
          
           
            
           #ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=all_lists[0])
    if Addon.getSetting("dp")=='true' and silent_mode==False:
        dp.close()
    if Addon.getSetting("dp")=='true' and silent_mode==False:
          elapsed_time = time.time() - start_time
          dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Enjoy', ' ')

    if Addon.getSetting("dp")=='true' and silent_mode==False:
        dp.close()
    
    return status_pl,rest_of_data
def auto_play(name,urls,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id):
   
    year=show_original_year
    image=fanart
    plot=description
    icon=iconimage
    all_data=[]

    z=0

    
    all_links=json.loads(urls)
    is_playing=False
    for link in all_links:#for name2,link,icon,image,plot,year,q,server,f_q in all_data:
       if is_playing:
         break
       server=link.split("$$$$$$$")[1]
       q=link.split("$$$$$$$")[2]
       name=link.split("$$$$$$$")[3]
       plot=urllib.unquote_plus(link.split("$$$$$$$")[4].decode('utf8'))
       link=link.split("$$$$$$$")[0]
       
       
       try:
        if '-Sdarot' not in plot:
         r=play(name,link,iconimage,fanart,plot,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,auto_play=True)
        
         if r=='ok':
            
            while not xbmc.Player().isPlaying():
                xbmc.sleep(100) #wait until video is being played
            time.sleep(5)
            if xbmc.Player().isPlaying():
             
             mode2=1999
             
             xbmc.executebuiltin('Dialog.Close(okdialog, true)')
             is_playing==True
             sys.exit()
                
       except Exception as e:
         logging.warning(e)
         if Addon.getSetting("dp")=='true' and silent_mode==False:
           dp.update(int(z/(len(all_links)*100.0)),str(server)+"-"+q,str(z)+'/'+str(len(all_links)),str(e))
       z=z+1


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"
def get_redirect(url):
 try:
     if KODI_VERSION>=17:
         request = HeadRequest(url)
         response = urllib2.urlopen(request)
         
         new_url=response.geturl() 
         return new_url
     else:
       return url
 except:
   return url


def get_imdb_data(info,name_o,image,source,type):
         tmdbKey = '1248868d7003f60f2386595db98455ef'
         name=name_o
         imdb_id=''
         icon=image
         fanart=image
         plot=''
         rating=''
         genere=' '
         check=False
        
         if source=='jen2':
                check=True
         elif  Addon.getSetting("jen_tmdb")=='false':
             check=True
         if check:
           return name,imdb_id,icon,fanart,plot,rating,genere
         if 'title' in info:
          a=info['title']
         else:
           info['title']=name_o.replace('.',' ')
         
         if len(info['title'])>0:
          a=a
         else:
           info['title']=name_o.replace('.',' ')
         if 1:
          if 'year' in info:
            tmdb_data="https://api.tmdb.org/3/search/%s?api_key=%s&query=%s&year=%s&language=en&append_to_response=external_ids"%(type,tmdbKey,urllib.quote_plus(info['title']),info['year'])
            year_n=info['year']
          else:
            tmdb_data="https://api.tmdb.org/3/search/%s?api_key=%s&query=%s&language=en&append_to_response=external_ids"%(type,tmdbKey,urllib.quote_plus(info['title']))

          all_data=requests.get(tmdb_data).json()
          if 'results' in all_data:
           if len(all_data['results'])>0:
                if (all_data['results'][0]['id'])!=None:
                    url='https://api.themoviedb.org/3/%s/%s?api_key=%s&language=en&append_to_response=external_ids'%(type,all_data['results'][0]['id'],tmdbKey)
                    try:
                        all_d2=requests.get(url).json()
                        imdb_id=all_d2['external_ids']['imdb_id']
                    except:
                        imdb_id=" "
                    genres_list= []
                    if 'genres' in all_d2:
                        for g in all_d2['genres']:
                          genres_list.append(g['name'])
                    
                    try:genere = u' / '.join(genres_list)
                    except:genere=''
                
                try:
                        if 'title' in all_data['results'][0]:
                          name=all_data['results'][0]['title']
                        else:
                          name=all_data['results'][0]['name']
                        rating=all_data['results'][0]['vote_average']
                        try:
                          icon=domain_s+'image.tmdb.org/t/p/original/'+all_data['results'][0]['poster_path']
                          fanart=domain_s+'image.tmdb.org/t/p/original/'+all_data['results'][0]['backdrop_path']
                        except:
                         pass
                        
                        plot=all_data['results'][0]['overview']
                except Exception as e:
                        logging.warning(e)
                        name=info['title']
                        fanart=' '
                        icon=' '
                        plot=' '
          else:
               name=name_o
               fanart=image
               icon=image
               plot=' '
         else:
               name=name_o
               fanart=image
               icon=image
               plot=' '
       
         return name,imdb_id,icon,fanart,plot,rating,genere
def get_qu(url):
    def gdecom(url):
     
        
        
        
        
        
        
        import StringIO ,gzip
        compressedFile = StringIO.StringIO()
        compressedFile.write(url.decode('base64'))
        # # Set the file's current position to the beginning
        # of the file so that gzip.GzipFile can read
        # its contents from the top.
        # 
        compressedFile.seek(0)
        return  gzip.GzipFile(fileobj=compressedFile, mode='rb').read()
    tmdb_cacheFile = os.path.join(tmdb_data_dir, '4k.db')
    dbcon_tmdb = database.connect(tmdb_cacheFile)
    dbcur_tmdb = dbcon_tmdb.cursor()
    
    dbcon_tmdb.commit()
    dbcur_tmdb.execute("SELECT * FROM MyTable")
    
    match = dbcur_tmdb.fetchall()
    for index,name,link,icon,fanart,plot,data,date,year,genre,father,type in match:
        data=data.replace('[',' ').replace(']',' ').replace('	','').replace("\\"," ").replace(': """",',': "" "",').replace(': """"}',': "" ""}').replace(': "",',': " ",').replace(': ""}',': " "}').replace('""','"').replace('\n','').replace('\r','')
       
        
        try:
            data2=json.loads(data)
            
            original_title=data2['originaltitle']
            imdb_id=data2['imdb']
            rating=data2['rating']
            generes=data2['genre']
        except:
            original_title=name
            imdb_id=" "
            rating=" "
            generes=" "
        addLink( name, gdecom(link),5,False,icon,fanart,'[COLOR gold]'+'4K'+'[/COLOR]\n[COLOR lightblue]'+'-NEW K-'+'[/COLOR]\n'+plot,data=year,original_title=original_title,id=imdb_id,rating=rating,generes=generes,show_original_year=year,saved_name=name)
                
          
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
def fix_name(name_o):
    
    regex_c='\[COLOR(.+?)\]'
    match_c=re.compile(regex_c).findall(name_o)

    if len(match_c)>0:
          for items in match_c:
            name_o=name_o.replace('[COLOR%s]'%items,'')
    name_o=name_o.replace('=',' ').replace('[B]','').replace('[/B]','').replace('silver','').replace('deepskyblue','').replace('[','').replace(']','').replace('/COLOR','').replace('COLOR','').replace('4k','').replace('4K','').strip().replace('(','.').replace(')','.').replace(' ','.').replace('..','.')
    return name_o
    
def get_data(i,url2,headers):
       global matches
       try:
        
        x=requests.get(url2,headers=headers,timeout=3).content
        regex_pre='<item>(.+?)</item>'
        match_pre=re.compile(regex_pre,re.DOTALL).findall(x)
   
        match=[]
        for items in match_pre:
            
            regex_link='<link>(.+?)</link'
            match_link=re.compile(regex_link,re.DOTALL).findall(items)
            if len(match_link)>0:
                if len (match_link)>1:
                  match_link2=''
             
                  for link_in in match_link:
                     if match_link2=='':
                       match_link2=link_in
                     else:
                       match_link2=match_link2+'$$$'+link_in
                  match_link=match_link2
                else:
                  match_link=match_link[0]
                regex_name='<title>(.+?)</title'
                match_name=re.compile(regex_name,re.DOTALL).findall(items)
                if len(match_name)==0:
                  
                  continue
                else:
                   match_name=match_name[0]
                regex_image='<thumbnail>http(.+?)</'
                match_image=re.compile(regex_image,re.DOTALL).findall(items)
                if len (match_image)>0:
                   match_image=match_image[0]
                else:
                   match_image=' '
                
                
                
                match.append((match_name,match_link,match_image))
            
            #match=match+re.compile(regex,re.DOTALL).findall(items)
        matches[i]=match
        
        return matches[i]
       except Exception as e:
         logging.warning(e)
         logging.warning('Bad Jen')
         logging.warning(url2)
         return []


def get_next_jen(url,icon,fanart):
    from new_jen import get_list
    get_list(url,icon,fanart)
    #from jen import check_jen_categroys
    #check_jen_categroys(url,icon,fanart)
def get_jen_list(url,icon,fan):
    global matches
    #from jen import check_jen_categroys
    from new_jen import get_list
    
    
  
    
    start_time = time.time()
    all_links_in=[]
    headers = {
                
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
              }
    stop_all=0
    matches={}
    thread=[]
    all_lists=[]
    all_jen_lisy=[]
    for i in range (1,40):
        if stop_all==1:
          break
        url2=Addon.getSetting("Pastebin-%s-"%url+str(i))
 
        if 'http' not in url2:
          continue
        if Addon.getSetting("jen_fan_cat-"+str(i)):
            fan=Addon.getSetting("jen_fan_cat-"+str(i))
        else:
            fan='https://koditips.com/wp-content/uploads/jen-kodi.jpg'
        
       
        get_list(url2,icon,fan)
    return 0
    for td in thread:
      td.start()
    
    while 1:
      num_live=0
      still_alive=0
      
     
      string_dp2=''
      for threads in thread:
        count=0
        for yy in range(0,len(thread)):
            if not thread[yy].is_alive():
              num_live=num_live+1
             
            else:
              still_alive=1
             
              string_dp2=thread[yy].name
             
              if Addon.getSetting("jen_progress")=='true':
                dp.update(0, 'Slow in the first time Please wait ',string_dp2, string_dp2)
      if still_alive==0:
        break
      
    season=' '
    dbcur_tmdb.execute("SELECT * FROM tmdb_data")

    match4 = dbcur_tmdb.fetchall()
    all_eng_name={}
    for eng_name,imdb_id,icon,fanart,plot,rating,name,generes in match4:
       all_eng_name[name.replace('é','e')]=[]
       all_eng_name[name.replace('é','e')].append((eng_name,imdb_id,icon,fanart,plot,rating,name,generes))
    
    for match in matches:
        
        if stop_all==1:
          break
        
        for name_o,link,image in matches[match]:
         
         image='http'+image.strip().replace('\n','').replace(' ','').replace('\r','').replace('\t','')
         check=False
         if Addon.getSetting("rdsource")=='true':
           check=True
         elif '1fichier.com' not in link and 'glasford.ddns.net' not in link and 'http://dl.my-film.in/' not in link and 'http://dl.my-film.org/' not in link  and 'debrid' not in name_o.lower():
           check=True
         
         
         
         if check:
          name_o=fix_name(name_o).strip()
          name_o=name_o.replace('Real.Debrid.Only','')
          if name_o.endswith('.'):
            name_o=name_o[:-1]
          info=(PTN.parse(name_o))
          info['title']=info['title'].replace('-',' ').replace(' ','.')
          
          if 'year' in info:
              name_o=name_o.replace(str(info['year']),'').strip()
              if name_o.endswith('.'):
                name_o=name_o[:-1]
            
         
          rest=''
          for keys in info:
             if keys!='title':
               rest=rest+' '+str(info[keys])
          count=count+1
          imdb_id=' '
          rating=' '
          year_n='0'
          if 'year' in info:
          
            year_n=info['year']

          
          if 'Season ' in link:
            type='tv'
            
          else:
            type='movie'
          
          if Addon.getSetting("jen_progress")=='true':
              if dp.iscanceled():
                dp.close()
                stop_all=1
                break
  
          try: 
            items=all_eng_name[name_o.replace("'"," ").replace('é','e').replace('’',' ')][0]
          except:
            items=None
          if items==None:
              
              name,imdb_id,icon,fanart,plot,rating,generes=get_imdb_data(info,name_o,image,'jen',type)
              if Addon.getSetting("jen_tmdb")=='true':
                 try:
                  dbcur_tmdb.execute("INSERT INTO tmdb_data Values ('%s', '%s', '%s', '%s', '%s', '%s','%s','%s');" %  (name.replace("'"," "),imdb_id,icon.replace("'","%27"),fanart.replace("'","%27"),plot.replace("'"," "),rating,name_o.replace("'"," "),generes))
                  dbcon_tmdb.commit()
                 except:
                   all_data_inin=[]
                   all_data_inin.append((name.replace("'"," "),imdb_id,icon,fanart,plot.replace("'"," "),rating,name_o.replace("'"," "),generes))
                   
                   sys.exit()
          else:
            eng_name,imdb_id,icon,fanart,plot,rating,name,generes=items
          
          
          if imdb_id==None:
            imdb_id=' '
          o_plot=plot
          if rating==None:
            rating=' '
          if generes==None:
            generes=' '
          elapsed_time = time.time() - start_time
          if Addon.getSetting("jen_progress")=='true':
                dp.update(int(((z* 100.0)/(len(matches))) ), 'Slow in the first time Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),name, str(len(all_links_in))+' , '+str(match))
          z=z+1
          links2=[]
          if '$$$' in link:
            links2=link.split('$$$')
          
            
          else:
             links2.append(link)
          for link in links2:
              
              if '(' in link:
                  regex='http(.+?)\((.+?)\)'
                  match44=re.compile(regex).findall(link)
                  
             
                  for links,name2 in match44:
                        links='http'+links
                       
                       
                        if links not in all_links_in and 'trailer' not in name2.lower():
                            if 'youtube' in links or '<links>' in links or links=='ignore' or 'ignor.me' in links or links=='https://' or links=='http://' or links==None or 'http' not in links:
                                
                                continue
                            all_links_in.append(links)
                           
                            all_jen_lisy.append(( (rest.replace('=',' ')+'---'+fix_name(name2)).replace('..','.'), links,icon,fanart,plot,year_n,name_o,info['title'],imdb_id,rating,generes,year_n,'%20','%20'))
                                                       
              if 'LISTSOURCE' in link :
                  
                  regex='LISTSOURCE\:(.+?)\:\:LISTNAME\:(.+?)\:'
                  match2=re.compile(regex).findall(link)
                  if len(match2)>0:
                    for links,name2 in match2:
                        if '(' in links:
                          regex='http(.+?)\('
                          links=re.compile(regex).findall(links)[0]
                        if links not in all_links_in and 'trailer' not in name2.lower():
                            if 'youtube' in links or '<links>' in links or links=='ignore' or 'ignor.me' in links or links=='https://' or links=='http://' or links==None or 'http' not in links:
                                
                                continue
                            all_links_in.append(links)
                            
                            all_jen_lisy.append(( (rest.replace('=',' ')+'---'+fix_name(name2)).replace('..','.'), links,icon,fanart,plot,year_n,name_o,info['title'],imdb_id,rating,generes,year_n,'%20','%20'))
                                                    
              elif 'sublink' in link:
                 regex_sub='<sublink(.+?)>(.+?)</sublink>'
                 match_sub=re.compile(regex_sub).findall(link)
           
                 if len(match_sub)>0:
                   for ep,links in match_sub:
                    regex_ep='\]Season (.+?) Episode (.+?)\['
                    match_ep=re.compile(regex_ep,re.IGNORECASE).findall(ep)
                    if len(match_ep)>0:
                       season,episode=match_ep[0]
                       plot='Season '+season+' Episode '+episode+'\n'+o_plot
                    else:
                       season=' '
                       episode=' '
                    if '(' in links:
                          regex='http(.+?)\('
                          links=re.compile(regex).findall(links)[0]
                    if links not in all_links_in:
                        if 'youtube' in links or '<links>' in links or links=='ignore' or 'ignor.me' in links or links=='https://' or links=='http://' or links==None or 'http' not in links:
                              
                                continue
                        all_links_in.append(links)
                        
                        all_jen_lisy.append((ep.replace('=',' '), links,icon,fanart,plot,year_n,name_o,info['title'],imdb_id,rating,generes,year_n,season,episode))
                                                 
                  
              elif link not in all_links_in:
                    if '(' in link:
                          regex='http(.+?)\('
                          link=re.compile(regex).findall(link)
                          if len(link)>0:
                            link=link[0]
                          else:
                            continue
                    if 'youtube' in link or '<link>' in link or link=='ignore' or 'ignor.me' in link or link=='https://' or link=='http://' or link==None or 'http' not in link:
                               
                                continue
                    all_links_in.append(link)
                    
                    all_jen_lisy.append((rest.replace('=',' '), link,icon,fanart,plot,year_n,info['title'],info['title'],imdb_id,rating,generes,year_n,'%20','%20'))
    all_names=[]
    all_links={}
    for  name, link,icon,fanart,plot,data,saved_name,original_title,id,rating,generes,show_original_year,season,episode in all_jen_lisy:
       
        name1=saved_name.decode('utf8').strip()
        
        if name1 not in all_names:
             
             all_names.append(name1)
             all_links[name1]={}
             all_links[name1]['icon']=icon
             all_links[name1]['image']=fanart
             all_links[name1]['plot']=plot
             all_links[name1]['data']=data
             
             all_links[name1]['saved_name']=saved_name
             all_links[name1]['original_title']=original_title
             all_links[name1]['id']=id
             all_links[name1]['rating']=rating
             all_links[name1]['generes']=generes
             all_links[name1]['show_original_year']=show_original_year
             all_links[name1]['season']=season
             all_links[name1]['episode']=episode
            
             all_links[name1]['link']='[['+name+']]'+link
         
        else:
           if link not in all_links[name1]['link']:
             if '$$$' in link:
                  links=link.split('$$$')
                  for link in links:
                    all_links[name1]['link']=all_links[name1]['link']+'$$$'+'[['+name+']]'+link
             else:
               all_links[name1]['link']=all_links[name1]['link']+'$$$'+'[['+name+']]'+link
                   
        

    for items in all_links:
        
             icon=all_links[items]['icon']
             fanart=all_links[items]['image']
             plot=all_links[items]['plot']
             data=all_links[items]['data']
             
             saved_name=all_links[items]['saved_name']
             original_title=all_links[items]['original_title']
             id=all_links[items]['id']
             rating=all_links[items]['rating']
             generes=all_links[items]['generes']
             show_original_year=all_links[items]['show_original_year']
             season=all_links[items]['season']
             episode=all_links[items]['episode']
             
             link=all_links[items]['link']
             addLink( items.replace('.',' '), link,5,False,icon,fanart,plot,data=data,saved_name=saved_name,original_title=original_title,id=id,rating=rating,generes=generes,show_original_year=show_original_year,season=season,episode=episode)
             
    if Addon.getSetting("jen_progress")=='true':
      dp.close()
   
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)

def build_jen_db():
    global matches
    import urlparse
    rd_domains=[u'4shared.com', u'rapidgator.net', u'sky.fm', u'1fichier.com', u'depositfiles.com', u'hitfile.net', u'filerio.com', u'solidfiles.com', u'mega.co.nz', u'scribd.com', u'flashx.tv', u'canalplus.fr', u'dailymotion.com', u'salefiles.com', u'youtube.com', u'faststore.org', u'turbobit.net', u'big4shared.com', u'filefactory.com', u'youporn.com', u'oboom.com', u'vimeo.com', u'redtube.com', u'zippyshare.com', u'file.al', u'clicknupload.me', u'soundcloud.com', u'gigapeta.com', u'datafilehost.com', u'datei.to', u'rutube.ru', u'load.to', u'sendspace.com', u'vidoza.net', u'tusfiles.net', u'unibytes.com', u'ulozto.net', u'hulkshare.com', u'dl.free.fr', u'streamcherry.com', u'mediafire.com', u'vk.com', u'uploaded.net', u'userscloud.com',u'nitroflare.com']
    
    tmdb_cacheFile = os.path.join(done_dir,'cache_f', 'jen_db.db')
    dbcon_tmdb = database.connect(tmdb_cacheFile)
    dbcur_tmdb = dbcon_tmdb.cursor()
    dbcur_tmdb.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT,""link TEXT,""year TEXT,""type TEXT);"% 'tmdb_data')

    try:
        dbcur_tmdb.execute("VACUUM 'AllData';")
        dbcur_tmdb.execute("PRAGMA auto_vacuum;")
        dbcur_tmdb.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
        dbcur_tmdb.execute("PRAGMA temp_store=MEMORY ;")
    except:
     pass
    dbcon_tmdb.commit()
   
    
    dp = xbmcgui . DialogProgress ( )
    dp.create('Please wait','Searching sources', '','')
    dp.update(0, 'Please wait','Searching sources', '' )
    z=0
    start_time = time.time()
    all_links_in=[]
    headers = {
                
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
              }
    stop_all=0
    matches={}
    thread=[]
    all_lists=[]
    all_jen_lisy=[]
    m=0
    for j in range(1,6):
      for i in range (1,40):
        if stop_all==1:
          break
        url2=Addon.getSetting(("Pastebin-%s-"%str(j))+str(i))
 
        if 'http' not in url2:
          continue
        
        all_lists.append(url2)
        matches[str(m)]=''
        m+=1
        thread.append(Thread(get_data,str(m),url2,headers))
        thread[len(thread)-1].setName(str(m))
    f = open(os.path.join(tmdb_data_dir, 'jen_lists.txt'), 'r')
    file_data = f.readlines()
    f.close()
    for url2 in file_data:
        if 'http' not in url2:
          continue
        
        all_lists.append(url2)
        matches[str(m)]=''
        m+=1
        thread.append(Thread(get_data,str(m),url2,headers))
        thread[len(thread)-1].setName(str(m))
    for td in thread:
      td.start()
    
    while 1:
      num_live=0
      still_alive=0
      
     
      string_dp2=''
      for threads in thread:
        count=0
        for yy in range(0,len(thread)):
            if not thread[yy].is_alive():
              num_live=num_live+1
             
            else:
              still_alive=1
             
              string_dp2=thread[yy].name
             
              
              dp.update(0, 'Slow in the first time Please wait ',string_dp2, string_dp2)
      if still_alive==0:
        break
      
    season=' '
    dbcur_tmdb.execute("SELECT * FROM tmdb_data")

    match4 = dbcur_tmdb.fetchall()
    all_eng_name=[]
    for eng_name,link,year,type in match4:

       all_eng_name.append(link)
    
    for match in matches:
        
        if stop_all==1:
          break
        
        for name_o,link,image in matches[match]:
         icon=image
         fanart=image
         plot=''
         generes=''
         image='http'+image.strip().replace('\n','').replace(' ','').replace('\r','').replace('\t','')
         
         
         
         
         if 1:
          name_o=fix_name(name_o).strip()
          name_o=name_o.replace('Real.Debrid.Only','')
          if name_o.endswith('.'):
            name_o=name_o[:-1]
          info=(PTN.parse(name_o))
          info['title']=info['title'].replace('-',' ').replace(' ','.')
          name=info['title']
          if 'year' in info:
              name_o=name_o.replace(str(info['year']),'').strip()
              if name_o.endswith('.'):
                name_o=name_o[:-1]
            
         
          rest=''
          for keys in info:
             if keys!='title':
               rest=rest+' '+str(info[keys])
          count=count+1
          imdb_id=' '
          rating=' '
          year_n='0'
          if 'year' in info:
          
            year_n=info['year']

          
          if 'Season ' in link:
            type='tv'
            
          else:
            type='movie'
          
          
          if dp.iscanceled():
            dp.close()
            stop_all=1
            break
  
        
          
          
          if imdb_id==None:
            imdb_id=' '
       
          if rating==None:
            rating=' '
        
          elapsed_time = time.time() - start_time
         
          dp.update(int(((z* 100.0)/(len(matches))) ), 'Slow in the first time Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),name, str(len(all_links_in))+' , '+str(match))
          z=z+1
          links2=[]
          if '$$$' in link:
            links2=link.split('$$$')
          
            
          else:
             links2.append(link)
          for link in links2:
              
              if '(' in link:
                  regex='http(.+?)\((.+?)\)'
                  match44=re.compile(regex).findall(link)
                  
             
                  for links,name2 in match44:
                        links='http'+links
                       
                       
                        if links not in all_links_in and 'trailer' not in name2.lower():
                            if 'youtube' in links or '<links>' in links or links=='ignore' or 'ignor.me' in links or links=='https://' or links=='http://' or links==None or 'http' not in links:
                                
                                continue
                            all_links_in.append(links)
                           
                            all_jen_lisy.append(( (rest.replace('=',' ')+'---'+fix_name(name2)).replace('..','.'), links,icon,fanart,plot,year_n,name_o,info['title'],imdb_id,rating,generes,year_n,'%20','%20'))
                                                       
              if 'LISTSOURCE' in link :
                  
                  regex='LISTSOURCE\:(.+?)\:\:LISTNAME\:(.+?)\:'
                  match2=re.compile(regex).findall(link)
                  if len(match2)>0:
                    for links,name2 in match2:
                        if '(' in links:
                          regex='http(.+?)\('
                          links=re.compile(regex).findall(links)[0]
                        if links not in all_links_in and 'trailer' not in name2.lower():
                            if 'youtube' in links or '<links>' in links or links=='ignore' or 'ignor.me' in links or links=='https://' or links=='http://' or links==None or 'http' not in links:
                                
                                continue
                            all_links_in.append(links)
                            
                            all_jen_lisy.append(( (rest.replace('=',' ')+'---'+fix_name(name2)).replace('..','.'), links,icon,fanart,plot,year_n,name_o,info['title'],imdb_id,rating,generes,year_n,'%20','%20'))
                                                    
              elif 'sublink' in link:
                 regex_sub='<sublink(.+?)>(.+?)</sublink>'
                 match_sub=re.compile(regex_sub).findall(link)
           
                 if len(match_sub)>0:
                   for ep,links in match_sub:
                    regex_ep='\]Season (.+?) Episode (.+?)\['
                    match_ep=re.compile(regex_ep,re.IGNORECASE).findall(ep)
                    if len(match_ep)>0:
                       season,episode=match_ep[0]
                       plot='Season '+season+' Episode '+episode+'\n'+o_plot
                    else:
                       season=' '
                       episode=' '
                    if '(' in links:
                          regex='http(.+?)\('
                          links=re.compile(regex).findall(links)[0]
                    if links not in all_links_in:
                        if 'youtube' in links or '<links>' in links or links=='ignore' or 'ignor.me' in links or links=='https://' or links=='http://' or links==None or 'http' not in links:
                              
                                continue
                        all_links_in.append(links)
                        
                        all_jen_lisy.append((ep.replace('=',' '), links,icon,fanart,plot,year_n,name_o,info['title'],imdb_id,rating,generes,year_n,season,episode))
                                                 
                  
              elif link not in all_links_in:
                    if '(' in link:
                          regex='http(.+?)\('
                          link=re.compile(regex).findall(link)
                          if len(link)>0:
                            link=link[0]
                          else:
                            continue
                    if 'youtube' in link or '<link>' in link or link=='ignore' or 'ignor.me' in link or link=='https://' or link=='http://' or link==None or 'http' not in link:
                               
                                continue
                    all_links_in.append(link)
                    
                    all_jen_lisy.append((rest.replace('=',' '), link,icon,fanart,plot,year_n,info['title'],info['title'],imdb_id,rating,generes,year_n,'%20','%20'))
    
    all_names=[]
    all_links={}
    z=0
    n=0
    all_new=[]
    for  name, link,icon,fanart,plot,data,saved_name,original_title,id,rating,generes,show_original_year,season,episode in all_jen_lisy:
       
        name1=saved_name.decode('utf8').strip()
        dp.update(int(((z* 100.0)/(len(all_jen_lisy))) ), 'Updating DB',name1.replace('.',' ').replace("'","%27"),str( z)+','+'New:'+str(n))
        if link not in all_eng_name:
                host = link.replace("\\", "")
                host2 = host.strip('"')
                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(host2.strip().lower()).netloc)
                if len(host)==0:
                    continue
                host=host[0]
              
                if host not in rd_domains:
                    type='free'
                else:
                    type='RD'
                n+=1
                all_new.append(name1)
                
                dbcur_tmdb.execute("INSERT INTO tmdb_data Values ('%s', '%s', '%s', '%s');" %  (name1.replace('.',' ').replace("'","%27").lower(),link.replace("'","27"),str(show_original_year).replace("'","%27"),type))
        z+=1
    showText('New', '\n'.join(all_new))
    dbcon_tmdb.commit()
    dp.close()
def save_fav(id,tv_movie):
   if tv_movie=='tv':
     save_file=os.path.join(user_dataDir,"fav_tv.txt")
   else:
     save_file=os.path.join(user_dataDir,"fav_movie.txt")
   file_data=[]
   change=0

   
   if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
   if len(file_data)>150:
       for i in range (len(file_data)-1,0,-1):
         if (i<(len(file_data)-100)) and len(file_data[i])>0:
          file_data.pop(i)
          change=1
       for i in range (len(file_data)-1,0,-1):
         
         if len(file_data[i])<3:
          
          file_data.pop(i)
          change=1

   if id not in file_data or change==1:
      for i in range (len(file_data)-1,0,-1):
         file_data[i]=file_data[i].replace('\n','')
         if len(file_data[i])<3:
          
          file_data.pop(i)
       
      if id not in file_data:
        file_data.append(id)
      file = open(save_file, 'w')
      file.write('\n'.join(file_data))
      file.close()
def open_fav(url):
    save_file=os.path.join(user_dataDir,"fav.txt")
    if url=='movies':
      type='movies'
    elif url=='tv':
      type='tv'
    else:
      type='all'
    url=None
    name=None
    mode=None
    iconimage=None
    fanart=None
    description=None
    original_title=None
    file_data=[]
    change=0

    if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
    num=0
    for items in file_data:
       if len(items)>1:
            list1=items.split("$$")
            full_str=''
            for item_as in list1:
              full_str=full_str+chr(int(item_as))
            
            params=get_custom_params(full_str)
           
            url=None
            name=None
            mode=None
            iconimage=None
            fanart=None
            description=None
            original_title=None
            data=0
            id=' '
            season=0
            episode=0
            show_original_year=0
            heb_name=' '
            tmdbid=' '
            eng_name=' '
            try:
                    url=urllib.unquote_plus(params["url"])
            except:
                    pass
            try:
                    name=urllib.unquote_plus(params["name"])
            except:
                    pass
            try:
                    iconimage=urllib.unquote_plus(params["iconimage"])
            except:
                    pass
            try:        
                    mode=int(params["mode"])
            except:
                    pass
            try:        
                    fanart=urllib.unquote_plus(params["fanart"])
            except:
                    pass
            try:        
                    description=urllib.unquote_plus(params["description"])
            except:
                    pass
            try:        
                    data=urllib.unquote_plus(params["data"])
            except:
                    pass
            try:        
                    original_title=(params["original_title"])
            except:
                    pass
            try:        
                    id=(params["id"])
            except:
                    pass
            try:        
                    season=(params["season"])
            except:
                    pass
            try:        
                    episode=(params["episode"])
            except:
                    pass
            try:        
                    tmdbid=(params["tmdbid"])
            except:
                    pass
            try:        
                    eng_name=(params["eng_name"])
            except:
                    pass
            try:        
                    show_original_year=(params["show_original_year"])
            except:
                    pass
            try:        
                    heb_name=(params["heb_name"])
            except:
                    pass
            
            te1=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode2="+str(mode)
            
            te2="&name="+(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&heb_name="+urllib.quote_plus(heb_name)
    
            te3="&data="+str(data)+"&original_title="+urllib.quote_plus(original_title)+"&id="+(id)+"&season="+str(season)
            te4="&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)
     
           
            
            
            u=te1 + te2 + te3 + te4.decode('utf8')
            link="ActivateWindow(10025,%s,return)" % (u)
            if (type=='movies' and mode==4) or type=='all' or (type=='tv' and mode==7):
             addLink( name, link,99,True, iconimage,fanart,description,data=data,original_title=original_title,id=id,season=season,episode=episode,num_in_list=num)
       num=num+1

def remove_to_fav(plot):
    file_data=[]
    change=0

    if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
    
    if plot+'\n' in file_data:
      file_data.pop(file_data.index(plot+'\n'))
      change=1
    if change>0:
       
          file = open(save_file, 'w')
          file.write('\n'.join(file_data))
          file.close()
          xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Removed')).encode('utf-8'))
def remove_fav_num(plot):
    file_data=[]
    change=0

    if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()

    if len(file_data)>=int(plot):
      file_data.pop(int(plot))
      change=1
    if change>0:
       
          file = open(save_file, 'w')
          file.write('\n'.join(file_data))
          file.close()
          xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Removed')).encode('utf-8'))
          xbmc.executebuiltin('Container.Refresh')
def play_by_subs(name,urls,iconimage,fanart,description_o,data,original_title,season,episode,id,eng_name,saved_name,original_title1,one_list=False):
   from urllib import quote_plus

   if urls=='torrents':
        dbcur.execute("SELECT * FROM torrents")
        urls = dbcur.fetchone()[0].decode('base64')
 
   dp = xbmcgui.DialogProgress()
   dp.create("Updating", "Please wait", '')
   dp.update(0)
   all_magents=json.loads(urls)

   plot=description_o
   tmdbKey = '1248868d7003f60f2386595db98455ef'
   
   if season!=None and season!="%20":
       tv_movie='tv'
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,tmdbKey)
   else:
       tv_movie='movie'
       
       url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,tmdbKey)
   if 'tt' not in id:
         try:
            imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
         except:
            imdb_id=" "
   else:
         imdb_id=id

   all_subs_in=json.loads(urllib.unquote_plus(original_title))
  
   all_data=[]
   xxx=0
   for mag in all_magents:
     
     regex='- (.+?) -'
     server_p=re.compile(regex).findall(all_magents[mag]['server'])
     if len(server_p)>0:
        server=server_p[0]
     else:
        server=''
     
     dp.update(int(((xxx* 100.0)/(len(all_magents))) ), all_magents[mag]['name'],'')
     xxx+=1
     title=all_magents[mag]['name']
     
     pre=check_pre(title.replace(' ','.').replace('(','').replace(')',''),all_subs_in['links'],original_title)
     
     description=plot
     if 1:#try:
          info=(PTN.parse(title))
          
          if 'resolution' in info:
             res=info['resolution']
          else:
             if "HD" in title:
              res="HD"
             elif "720" in title:
              res="720"
             elif "1080" in title:
               res="1080"
             else:
               res=' '
     #except:
     #   res=' '
     #   pass
     fixed_q=fix_q(res)

    
     try:
         regex=' - (.+?) GB'
         
         size=re.compile(regex).findall(all_magents[mag]['server'])[0]
   
         if 'MB' in size:
           size=size/1000
     except:
        size=0
     max_size=int(Addon.getSetting("size_limit"))
     
     if float(size)<max_size:
       
       regex='{P-(.+?)/S-(.+?)}'
     
       seeds=re.compile(regex).findall(all_magents[mag]['server'])[0][1].replace(' ','')
       peers=re.compile(regex).findall(all_magents[mag]['server'])[0][0].replace(' ','')
       seeds=seeds.replace(',','')
       peers=peers.replace(',','')
       regex='-(.+?)GB'
      
       if int(seeds)>=int(Addon.getSetting("min_seed")):
          
          all_data.append(('[COLOR gold]'+str(pre)+'%'+ '[/COLOR]- P%s/S%s- [COLOR lightgreen]%sGB[/COLOR]-[COLOR khaki]'%(peers,seeds,size)+res+ '[/COLOR]',all_magents[mag]['link'],urllib.quote_plus(str(all_magents[mag]['name'])),pre,res,fixed_q,all_magents[mag]['plot'],title,int(seeds),size,server))

   if Addon.getSetting("order_torrents_new")=='0':
      all_data=sorted(all_data, key=lambda x: x[5], reverse=False)
   elif Addon.getSetting("order_torrents_new")=='1':
       all_data=sorted(all_data, key=lambda x: x[3], reverse=True)
   elif Addon.getSetting("order_torrents_new")=='2':
       all_2160=[]
       all_1080=[]
       all_720=[]
       all_480=[]
       all_else=[]
       for name,link,origi,pre,res,fixed_q,description,title,seed,size,server in all_data:
        if fixed_q==1:
         all_2160.append((name,link,origi,pre,res,fixed_q,description,title,seed,size,server))
        elif fixed_q==2:
         all_1080.append((name,link,origi,pre,res,fixed_q,description,title,seed,size,server))
        elif fixed_q==3:
         all_720.append((name,link,origi,pre,res,fixed_q,description,title,seed,size,server))
        elif fixed_q==4:
         all_480.append((name,link,origi,pre,res,fixed_q,description,title,seed,size,server))
        else :
         all_else.append((name,link,origi,pre,res,fixed_q,description,title,seed,size,server))
       all_2160=sorted(all_2160, key=lambda x: x[3], reverse=True)
       all_1080=sorted(all_1080, key=lambda x: x[3], reverse=True)
       all_720=sorted(all_720, key=lambda x: x[3], reverse=True)
       all_480=sorted(all_480, key=lambda x: x[3], reverse=True)
       all_else=sorted(all_else, key=lambda x: x[3], reverse=True)
       all_data=all_2160+all_1080+all_720+all_480+all_else
   elif Addon.getSetting("order_torrents_new")=='3':

      all_data=sorted(all_data, key=lambda x: x[8], reverse=True)
   else:
      all_data=sorted(all_data, key=lambda x: x[9], reverse=True)
   m=[]
   for name,link,origi,pre,res,fixed_q,description,title,seed,size,server in all_data:
     dp.update(int(((xxx* 100.0)/(len(all_magents))) ),name,'Ordering')
     video_data={}
     fixed_name=title

     if season!=None and season!="%20":
       video_data['TVshowtitle']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
       video_data['mediatype']='tvshow'
       
     else:
       video_data['mediatype']='movies'
     video_data['OriginalTitle']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
     video_data['title']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
     video_data['poster']=fanart
     video_data['fanart']=fanart
     
     video_data['plot']=description+'\n_from_Destiny_'
     video_data['icon']=iconimage
     video_data['year']=data
   
     
     video_data['season']=season
     video_data['episode']=episode
     video_data['imdb']=imdb_id
     video_data['code']=imdb_id

     video_data['imdbnumber']=imdb_id
     
     video_data['imdb_id']=imdb_id
     video_data['IMDBNumber']=imdb_id
     video_data['genre']=imdb_id
     if ((Addon.getSetting("new_source_menu")=='true')  or new_windows_only) :
        regex='- P(.+?)/S(.+?)'
        m1=re.compile(regex).findall(name)
        if len(m1)>0:
            added='{P'+m1[0][0]+'/S'+m1[0][1]
        else:
            added=''
        
        m.append((title.replace('[','.').replace(']','.')+'['+server+']'+'-'+size+('GB -{%s}'%added),link,iconimage,fanart,description+'\n_from_Destiny_','',res,'',res,title,pre))
     else:
        addLink(name, link,5,False, iconimage,fanart,'[COLOR aqua]'+res+'[/COLOR]\n'+description,original_title=original_title,id=id,data=data,saved_name=title,video_info=json.dumps(video_data))
   if Addon.getSetting("new_source_menu")=='true':
        new_show_sources(m,data,description+'\n_from_Destiny_',fixed_name,episode,fanart,fixed_name,iconimage,id,fixed_name,original_title1,season,data,[],[],[],[])

   dp.close()
def activate_torrent(sub,urls,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,saved_name):

    from play import play
    items=eval(urllib.unquote_plus(original_title))

    title=sub.split("% ")[1]
    try:
      s=int (season)
      tv_mode='tv'
    except:
      tv_mode='movie'
      pass
    if tv_mode=='movie':
      payload = '?search=movie&imdb_id=%s&title=%s&year=%s' % (id, title, data)
      play(urls, payload, items)
def server_test():
    #addDir3('Scan Direct links', 'www',33, ' ',' ',' ')
    onlyfiles = [f for f in listdir(done_dir) if isfile(join(done_dir, f))]
    onlyfiles=onlyfiles+[f for f in listdir(mag_dir) if isfile(join(mag_dir, f))]
    onlyfiles=onlyfiles+[f for f in listdir(rd_dir) if isfile(join(rd_dir, f))]
    onlyfiles=sorted(onlyfiles, key=lambda x: x[0], reverse=False)
    for items in onlyfiles:
      if items !='general.py' and '.pyc' not in items and '.pyo' not in items and '__init__' not in items and items !='resolveurl.py' and items !='cache.py'  and items!='cloudflare.py' and items!='Addon.py':
        impmodule = __import__(items.replace('.py',''))
        type,server_source=get_type(impmodule,items.replace('.py',''))
        
        addDir3(items.replace('.py','')+'('+server_source+')', items,23, ' ',' ',' ')
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass

def get_links_new(hostDict,imdb_id,name1,type,items,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id,premiered,test=False):
    global stop_all
    
        
    logging.warning('test:'+str(test))
    if allow_debrid:
        import real_debrid
        rd_domains=cache.get(get_rd_servers, 72, table='pages')
        
    all_links_sources[name1]={}
    all_links_sources[name1]['links']=[]
    all_links_sources[name1]['torrent']=False
    
            
    if 'rd' in type:
      all_links_sources[name1]['rd']=True
    else:
      all_links_sources[name1]['rd']=False
          
    try:
        from general import server_data
        aliases=[]
        aliases.append({'country': 'us', 'title': original_title})
        
        
        hostprDict = ['1fichier.com', 'oboom.com', 'rapidgator.net', 'rg.to', 'uploaded.net',
                           'uploaded.to', 'ul.to', 'filefactory.com', 'nitroflare.com', 'turbobit.net', 'uploadrocket.net','uploadgig.com']

        s_type=''
        try:
            base=items.source()
        except:
            try:
                base=items.sources()
            except:
                classes={}
                import inspect
                for name2, obj in inspect.getmembers(items):
                    if inspect.isclass(obj):
                        classes[name2] = obj
                base=classes[name1]
   
                s_type='universal'
        if s_type=='universal':
            
            
            if tv_movie=='movie':
                sour=base().scrape_movie( original_title, show_original_year,imdb_id, debrid = allow_debrid)
                for it in sour:
                    host_pre=re.compile('//(.+?)/').findall(it['url'])
                    if len(host_pre)>0:
                        host=host_pre[0].replace('www','')
                    else:
                        host='www'
                    pre_q=it['quality']
                    it['quality']=res_q(it['quality'])
                    if stop_all==1:
                        break
                    if 'magnet:'  in it['url']:
                        all_links_sources[name1]['torrent']=True
                    if (Addon.getSetting("check_l")=='true' or test)  and 'magnet:' not in it['url']:
                        try:
                            
                            t_url=base.resolve(it['url'])
                        except:
                            t_url=it['url']
                            
                        if   allow_debrid:
                            try:
                                host = t_url.split('//')[1].replace('www.','')
                                host = host.split('/')[0].lower()
                            except:
                                host='no'
                 
                            if host in rd_domains:
                            
                                rd = real_debrid.RealDebrid()
                                url=t_url
                                
                                link=rd.get_link(url)
                                
                                
                                if 'error' not in link:
                                    if 'filename' in link:
                                        name2=link['filename']
                                    else:
                                        name2=original_title
                                    if 'host' in link:
                                        match_s=link['host']
                                    else:
                                        regex='//(.+?)/'
                                        match_s=host
                                    all_links_sources[name1]['links'].append((name2,it['url'],match_s,it['quality']))
                            else:
                                name2,match_s,res,check=server_data(t_url,original_title)
                            
                                if check:
                                    
                                    all_links_sources[name1]['links'].append((name2,it['url'],match_s,it['quality']))
                                elif test:
                                    logging.warning('test: BAD '+str(test))
                                    all_links_sources[name1]['links'].append(('[COLOR red]BAD '+name2+'[/COLOR]',it['url'],match_s,it['quality']))
                        elif host not in hostprDict:
                            
                            
                            
                            name2,match_s,res,check=server_data(t_url,original_title)
                            
                            if check:
                                
                                all_links_sources[name1]['links'].append((name2,it['url'],match_s,it['quality']))
                            elif test:
                                logging.warning('test: BAD '+str(test))
                                all_links_sources[name1]['links'].append(('[COLOR red]BAD '+name2+'[/COLOR]',it['url'],match_s,it['quality']))
                    else:
                        added=it['source']
                      
                        if it['source'].lower()=='magnet' or it['source'].lower()=='torrent':
                            try:
                                added='-magnet- '+pre_q.split('|')[1]
                            except:
                               added=it['source']
                        all_links_sources[name1]['links'].append((original_title,it['url'],added,it['quality']))
            else:
              
                sour=base().scrape_episode( original_title, show_original_year,show_original_year,season, episode,imdb_id,'', debrid = allow_debrid)
    
                for it in sour:
                    host_pre=re.compile('//(.+?)/').findall(it['url'])
                    if len(host_pre)>0:
                        host=host_pre[0].replace('www','')
                    else:
                        host='www'
                    it['quality']=res_q(it['quality'])
                    if 'magnet:'  in it['url']:
                        all_links_sources[name1]['torrent']=True
                    if stop_all==1:
                        break
                    if (Addon.getSetting("check_l")=='true' or test) and 'magnet:' not in it['url']:
                        try:
                            
                            t_url=base.resolve(it['url'])
                        except:
                            t_url=it['url']
                        if   allow_debrid:
                            try:
                                host = t_url.split('//')[1].replace('www.','')
                                host = host.split('/')[0].lower()
                            except:
                                host='no'
                     
                            if host in rd_domains:
                            
                                rd = real_debrid.RealDebrid()
                                url=t_url
                                
                                link=rd.check_link(url)
                               
                                if 'error' not in link:
                                    if 'filename' in link:
                                        name2=link['filename']
                                    else:
                                        name2=original_title
                                    if 'host' in link:
                                        match_s=link['host']
                                    else:
                                        regex='//(.+?)/'
                                        match_s=host
                                    all_links_sources[name1]['links'].append((name2,it['url'],match_s,it['quality']))
                            else:
                                name2,match_s,res,check=server_data(t_url,original_title)
                            
                                if check:
                                    
                                    all_links_sources[name1]['links'].append((name2,it['url'],match_s,it['quality']))
                                elif test:
                                    logging.warning('test: BAD '+str(test))
                                    all_links_sources[name1]['links'].append(('[COLOR red]BAD '+name2+'[/COLOR]',it['url'],match_s,it['quality']))
                        elif host not in hostprDict:
                            

                            name2,match_s,res,check=server_data(t_url,original_title)

                            if check:
                                
                                all_links_sources[name1]['links'].append((name2,it['url'],match_s,it['quality']))
                            elif test:
                                logging.warning('test: BAD '+str(test))
                                all_links_sources[name1]['links'].append(('[COLOR red]BAD '+name2+'[/COLOR]',it['url'],match_s,it['quality']))
                    else:
                        all_links_sources[name1]['links'].append((original_title,it['url'],it['source'],it['quality']))
        else:
        
            if tv_movie=='movie':
                try:
                    m_string=base.movie(imdb_id, original_title, original_title,aliases, show_original_year)
                except:
                    try:
                        m_string=base.movie(imdb_id, original_title, original_title, show_original_year)
                    except:
                        m_string=base.movie(original_title, show_original_year)
                
                try:
       
                    sources_string=base.sources(m_string, hostDict, hostprDict)
    
                    
                except Exception as e:
                    logging.warning(e)
                    sources_string=m_string
                    s_type='seren'
     
            else:
                try:
                    try:
                        m_string_pre=base.tvshow(imdb_id, '',original_title, original_title, aliases, show_original_year)
                    except:
                        m_string_pre=base.tvshow(imdb_id, '',original_title, original_title, show_original_year)#Gaia
                    m_string=base.episode(m_string_pre, imdb_id,'',original_title, premiered,season, episode)
                    sources_string=base.sources(m_string,hostDict, hostprDict)
                except Exception as e:
                        logging.warning(e)
                        m_string_pre={}
                        m_string_pre['show_title']=original_title
                        m_string_pre['season_number']=season
                        m_string_pre['episode_number']=episode
                        m_string_pre['show_aliases']=''
                        m_string_pre['year']=show_original_year
                        m_string_pre['country']=''
                        m_string=base.episode(m_string_pre, [])
                        sources_string=m_string
                        s_type='seren'
     

            if s_type=='seren':
           
                for it in sources_string:
                    if stop_all==1:
                        break
                    if '2160' in it['release_title'] or '4k' in it['release_title']:
                        q='2160'
                    elif '1080' in it['release_title']:
                        q='1080'
                    elif '720' in it['release_title']:
                        q='720'
                    elif '480' in it['release_title']:
                        q='480'
                    elif '360' in it['release_title']:
                        q='360'
                    else:
                        q='unk'
                    if 'seeds' in it:
                        if it['seeds']==None:
                            seeds='0'
                        else:
                            seeds=it['seeds']
                        if 'size' not in it:
                            it['size']='0'
                        
                        try:
                            added=' -magnet- '+str(float("{0:.2f}".format(float( it['size'])/(1024))) )+' GB'+' {P-%s/S-%s}'%('0',str(it['seeds']))
                        except Exception as e: 
                            logging.warning('Error in Float:'+str(e))
                            logging.warning('mSize:'+it['metadata'].mSize)
                            added=''
                        all_links_sources[name1]['torrent']=True
                    else:
                        added='-magnet-'
                        all_links_sources[name1]['torrent']=False
                    q=res_q(q)
                    all_links_sources[name1]['links'].append((it['release_title'],it['magnet'],added,q))
                    
                    
            else:
               
                
                for it in sources_string:
                    host_pre=re.compile('//(.+?)/').findall(it['url'])
                    if len(host_pre)>0:
                        host=host_pre[0].replace('www','')
                    else:
                        host='www'
                    it['quality']=res_q(it['quality'])
                    if stop_all==1:
                        break
             
                    
                    if 'info' in it and 'magnet' in it['url']:
                        try:
                            added='-magnet- '+it['info']
                        except:
                           added=''
                    elif 'metadata' in it:
                        if it['metadata'].mSeeds==None:
                            seeds='0'
                        else:
                            seeds=it['metadata'].mSeeds
                        try:
                            added='-magnet- '+str( float("{0:.2f}".format(float(it['metadata'].mSize)/(1024*1024*1024))) )+' GB'+' {P-%s/S-%s}'%('0',str(seeds))
                        except Exception as e: 
                            logging.warning('Error in Float:'+str(e))
                            logging.warning(it['metadata'].mSize)
                            added=''
                        all_links_sources[name1]['torrent']=True
                    else:
                        added=''
                        all_links_sources[name1]['torrent']=False
                    if 'magnet:'  in it['url']:
                        all_links_sources[name1]['torrent']=True
                    if (Addon.getSetting("check_l")=='true' or test) and all_links_sources[name1]['torrent']==False and 'magnet:' not in it['url']:
                        try:
                            
                            t_url=base.resolve(it['url'])
                        except:
                            t_url=it['url']
                        if   allow_debrid:
                            try:
                                host = t_url.split('//')[1].replace('www.','')
                                host = host.split('/')[0].lower()
                            except:
                                host='no'
               
                            if host in rd_domains:
                            
                                rd = real_debrid.RealDebrid()
                                url=t_url
                                
                                link=rd.check_link(url)
                               
                                if 'error' not in link:
                                    if 'filename' in link:
                                        name2=link['filename']
                                    else:
                                        name2=original_title
                                    if 'host' in link:
                                        match_s=link['host']
                                    else:
                                        regex='//(.+?)/'
                                        match_s=host
                                    all_links_sources[name1]['links'].append((name2,it['url'],match_s,it['quality']))
                            else:
                                name2,match_s,res,check=server_data(t_url,original_title)
                            
                                if check:
                                    
                                    all_links_sources[name1]['links'].append((name2,it['url'],match_s,it['quality']))
                                elif test:
                                    logging.warning('test: BAD '+str(test))
                                    all_links_sources[name1]['links'].append(('[COLOR red]BAD '+name2+'[/COLOR]',it['url'],match_s,it['quality']))
                        elif host not in hostprDict:
                            
                            name2,match_s,res,check=server_data(t_url,original_title)
                            if 'pageURL' in it['url']:
                                it['url']=json.dumps(it['url'])
                            if check:
                                
                                all_links_sources[name1]['links'].append((original_title,it['url'],it['source']+' '+added,it['quality']))
                            elif test:
                                logging.warning('test: BAD '+str(test))
                                all_links_sources[name1]['links'].append(('[COLOR red]BAD '+name2+'[/COLOR]',it['url'],match_s,it['quality']))
                    else:
                        if 'file' in it:
                            name2=it['file']
                        else:
                            name2=original_title
                        all_links_sources[name1]['links'].append((name2,it['url'],it['source']+' '+added,it['quality']))
                        
        
            
 
        
        
        all_links_sources[name1]['color']='white'
        
        return all_links_sources
     
    except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        
        logging.warning('ERROR IN sources:'+str(lineno))
        logging.warning('inline:'+line)
        logging.warning(e)
        logging.warning('BAD source')
def get_type(items,name):
    type=[]
    source_scraper=''
    
    try:
        base=items.source()
        source_scraper='exodus'
        try:
            p=items.source().pack
            source_scraper='gaia'
        except Exception as e:
            logging.warning(e)
            pass
    except:
        try:
            base=items.sources()
            source_scraper='seren'
        except:
            classes={}
            import inspect
            for name1, obj in inspect.getmembers(items):
                if inspect.isclass(obj):
                    classes[name1] = obj
            
           
            source_scraper='universal'
            base=classes[name]
    try:
        a= base.episode
        type.append('tv')
        try:
            a= base.movie
            type.append('movie')
        except Exception as e:
            logging.warning(e)
            pass
    except Exception as e:
        logging.warning(e)
        try:
            a= base.movie
            type.append('movie')
        except Exception as e:
            a= base.scrape_episode
            type.append('tv')
            try:
                a= base.scrape_movie
                type.append('movie')
            except Exception as e:
                logging.warning(e)
                pass
            logging.warning(e)
            pass
    return type,source_scraper
def run_test(name_o):
    global all_links_sources,stop_all
   
    dp = xbmcgui.DialogProgress()
    dp.create("Chacking", "Please wait", '')
    dp.update(0)
    name_o=name_o.split('(')[0]


    dir_path = os.path.dirname(os.path.realpath(__file__))
    mypath=done_dir

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles =onlyfiles+ [f for f in listdir(mag_dir) if isfile(join(mag_dir, f))]
    onlyfiles =onlyfiles+ [f for f in listdir(rd_dir) if isfile(join(rd_dir, f))]


    f_result={}
    all_sources=[]

    name_check=name_o
  
    for items in onlyfiles:
       if items !='general.py' and '.pyc' not in items and '.pyo' not in items and '__init__' not in items and items !='resolveurl.py' and items !='Addon.py' and items !='cache.py' and items!='cloudflare.py':
         
           impmodule = __import__(items.replace('.py',''))
          
           if name_check!='' :
             if items.replace('.py','')==name_check:
               
                 all_sources.append((items.replace('.py',''),impmodule))
          
    thread=[]
    type=[]
    string_dp=''
    for name1,items in all_sources:
     
     type,source_scraper=get_type(items,name1)

     try:
        import resolveurl
        hostDict = resolveurl.relevant_resolvers(order_matters=True)
        hostDict = [i.domains for i in hostDict if '*' not in i.domains]
        hostDict = [i.lower() for i in reduce(lambda x, y: x+y, hostDict)]
        hostDict = [x for y, x in enumerate(hostDict) if x not in hostDict[:y]]
     except Exception:
        hostDict = []
     if name1==name_check:
 
         if 'tv' in type and 'movie' in type:
           choise=['TV','MOVIE']
           ret = xbmcgui.Dialog().select("Choose", choise)
           if ret!=-1:
             if ret==0:
               tv_movie='tv'
             else:
               tv_movie='movie'
           else:
             sys.exit()
         elif 'tv' in type:
           tv_movie='tv'
         else:
           tv_movie='movie'
         if tv_movie=='tv':
            original_title='The Flash'
            show_original_year='2014'
            season='4'
            episode='5'
            season_n='04'
            episode_n='05'
            id='60735'
            name='the flash'
            imdb_id='tt3107288'
            premiered="2018-11-13"
            
         else:
            original_title='Rampage'
            show_original_year='2018'
            season='%20'
            episode='00'
            season_n='00'
            episode_n='00'
            id='427641'
            imdb_id='tt2231461'
            name='rampage'
            premiered=''
         #get_links_new(items,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id)
         thread.append(Thread(get_links_new,hostDict,imdb_id,name1,type,items,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id,premiered,True))
         thread[len(thread)-1].setName(name1)
    

    for td in thread:
          td.start()

    str1=''
    str2=''


    still_alive=0
    xxx=0
    all_links_togther=[]
    start_time=time.time()
    while 1:

        ir={}
        for threads in thread:
           
                still_alive=0
                for yy in range(0,len(thread)):
                        if thread[yy].is_alive():
                          ir[thread[yy].getName()]='[COLOR aqua]'+(thread[yy].getName())+'[/COLOR]'
                          still_alive=1
                        else:
                          ir[thread[yy].getName()]='[COLOR gold]'+(thread[yy].getName())+'[/COLOR]'
               
                count_rest=0
                count_1080=0
                count_720=0
                count_480=0
                f_result={}
                
                     
                
                links_in=''
                if name_check in all_links_sources:
                    if 'links' in all_links_sources[name_check]: 
                      for data in all_links_sources[name_check]['links']:
                             
                             name1,links,server,res=data
                             
                             if '1080' in res:
                               count_1080+=1
                             elif '720' in res:
                               count_720+=1
                             elif '480' in res:
                               count_480+=1
                             else:
                               count_rest+=1
                            
               
                str1=' '
               
                     
                string_dp="1080: %s 720: %s 480: %s Rest: %s"%(count_1080,count_720,count_480,count_rest)
                elapsed_time = time.time() - start_time
                dp.update(int(((xxx* 100.0)/(100)) ), ' Please wait '+' - [COLOR aqua]'+tv_movie+' - [/COLOR]'+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),string_dp)
                
        if dp.iscanceled():
        
                 stop_all=1
                 for threads in thread:
                   if threads.is_alive():
                     
                     threads._Thread__stop()
                  
                 dp.close()
            
                        
        if still_alive==0:
               break
    stop_all=1

    for name,link,server,res in all_links_sources[name_check]['links']:

      addLink(name,link,5,False,' ',' ','sss '+name_check+' sss '+server+' \n'+res)
      
def open_settings():
    Addon.openSettings()
def play_trailer_f(id,tv_movie):
    import random
    global search_done

    if tv_movie=='movie':
      url_t='http://api.themoviedb.org/3/movie/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id
    else:
      url_t='http://api.themoviedb.org/3/tv/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id

    html_t=requests.get(url_t).json()

    if len(html_t['results'])>0:
        vid_num=random.randint(0,len(html_t['results'])-1)
    else:
      return 0
    video_id=(html_t['results'][vid_num]['key'])
    from youtube_ext import get_youtube_link2
    playback_url=''
    if video_id!=None:
      try:
        playback_url= get_youtube_link2('https://www.youtube.com/watch?v='+video_id).replace(' ','%20')
        
    
      except Exception as e:
            pass
                    
      #from pytube import YouTube
      #playback_url = YouTube(domain_s+'www.youtube.com/watch?v='+video_id).streams.first().download()

      if search_done==0:
          
          xbmc.Player().play(playback_url)
def play_trailer(id,tv_movie):

    if tv_movie=='movie':
        url_t='http://api.themoviedb.org/3/movie/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id
        html_t=requests.get(url_t).json()
        video_id=(html_t['results'][0]['key'])
    else:
        url_t='http://api.themoviedb.org/3/tv/%s/videos?api_key=1248868d7003f60f2386595db98455ef'%id
        html_t=requests.get(url_t).json()
        video_id=(html_t['results'][0]['key'])
    from youtube_ext import get_youtube_link2
    playback_url=''
    if video_id!=None:
      try:
        playback_url= get_youtube_link2('https://www.youtube.com/watch?v='+video_id).replace(' ','%20')
        
    
      except Exception as e:
            pass
      #from pytube import YouTube
      #playback_url = YouTube(domain_s+'www.youtube.com/watch?v='+video_id).streams.first().download()
         
       
        
      #playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
      item = xbmcgui.ListItem(path=playback_url)
      xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
def movie_recomended():
   from random import randint
   save_file=os.path.join(user_dataDir,"fav_movie.txt")
   file_data=[]
   change=0
   
   
   if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
   else:
     xbmcgui.Dialog().ok('Error', 'No viewing history....')
     return 0
   count=0
   x=0
   url_array=[]
   new_name_array=[]
   while count<5:
    id=file_data[randint(0, len(file_data)-1)]
    x=x+1
    if x==len(file_data):
      break
    
    if len(id)>1 and '%' not in id:
     url=domain_s+'api.themoviedb.org/3/movie/%s/recommendations?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1'%id.replace('\n','')
     count=count+1
     
     if url not in url_array:
       url_array.append(url)
  
       new_name_array=get_movies(url,0,reco=1,new_name_array=new_name_array)
def tv_recomended():
   from random import randint
   save_file=os.path.join(user_dataDir,"fav_tv.txt")
   file_data=[]
   change=0
   
   
   if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
   else:
     xbmcgui.Dialog().ok('Error', 'No viewing history....')
     return 0
   count=0
   x=0
   url_array=[]
   while count<4:
    id=file_data[randint(0, len(file_data)-1)]
    x=x+1
    if x==len(file_data):
      break
    
    if len(id)>1 and '%' not in id:
          
     url=domain_s+'api.themoviedb.org/3/tv/%s/recommendations?api_key=1248868d7003f60f2386595db98455ef&language=en&page=1'%id.replace('\n','')
     
     count=count+1
     if url not in url_array:
       url_array.append(url)
       get_movies(url,0,reco=1)
 
def get_tmdb_from_imdb(imdb,html_g,xxx):
    global all_new_data
    url=domain_s+'api.themoviedb.org/3/find/%s?api_key=1248868d7003f60f2386595db98455ef&external_source=imdb_id&language=en'%imdb
    html=requests.get(url).json()
 
    for data in html['movie_results']:
     if 'vote_average' in data:
       rating=data['vote_average']
     else:
      rating=0
     if 'first_air_date' in data:
       if data['first_air_date']==None:
        year=' '
       else:
        year=str(data['first_air_date'].split("-")[0])
     else:
        if 'release_date' in data:
            if data['release_date']==None:
               year=' '
            else:
              year=str(data['release_date'].split("-")[0])
        else:
            year=' '
     if 'overview' in data:
         if data['overview']==None:
           plot=' '
         else:
           plot=data['overview']
     else:
        plot=' '
     if 'title' not in data:
       new_name=data['name']
     else:
       new_name=data['title']
     if 'original_title' in data:
       original_name=data['original_title']
       mode=4
       
       id=str(data['id'])
      
     else:
       original_name=data['original_name']
       id=str(data['id'])
       mode=7
     if data['poster_path']==None:
      icon=' '
     else:
       icon=data['poster_path']
     if 'backdrop_path' in data:
         if data['backdrop_path']==None:
          fan=' '
         else:
          fan=data['backdrop_path']
     else:
        fan=html['backdrop_path']
     if plot==None:
       plot=' '
     if 'http' not in fan:
       fan=domain_s+'image.tmdb.org/t/p/original/'+fan
     if 'http' not in icon:
       icon=domain_s+'image.tmdb.org/t/p/original/'+icon
     genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
            if i['name'] is not None])
     try:genere = u' / '.join([genres_list[x] for x in data['genre_ids']])
     except:genere=''

     trailer = "plugin://plugin.video.destiny?mode2=25&url=www&id=%s" % id

     all_new_data.append((new_name,icon,fan,plot,year,original_name,id,rating,genere,trailer,xxx))
     return new_name,icon,fan,plot,year,original_name,id,rating,genere,trailer,xxx
def latest_dvd(url):
    global all_new_data
    start_time=time.time()
    if Addon.getSetting("dp")=='true':
                dp = xbmcgui.DialogProgress()
                dp.create("Loading", "Please wait", '')
                dp.update(0)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.dvdsreleasedates.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    url_g=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
    html_g=requests.get(url_g).json()
    
    html_o=requests.get(url,headers=headers).content
    regex="'fieldtable-inner'.+?<a id='.+?'></a>(.+?)<(.+?)</table></td></tr>"
    match=re.compile(regex,re.DOTALL).findall(html_o)
    name_array=[]
    all_new_data=[]
    xxx=0
    thread=[]
    for dat,rest in match:
      all_new_data.append(('[COLOR aqua][I]'+dat+'[/I][/COLOR]','','','','','','','','','',xxx))
      
      regex="'http://www.imdb.com/title/(.+?)/'"
      match_in=re.compile(regex,re.DOTALL).findall(rest)
      

      for imdb in match_in:
        if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                dp.update(int(((xxx* 100.0)/(len(match_in)*len(match))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),imdb)
        xxx=xxx+1
        if imdb not in name_array:
        
            
            thread.append(Thread(get_tmdb_from_imdb,imdb,html_g,xxx))
            thread[len(thread)-1].setName(imdb)
                    

    for td in thread:
        td.start()

        if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name)
        #if len(thread)>38:
        xbmc.sleep(255)
    while 1:
          
          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              all_alive.append(thread[yy].name)
              still_alive=1
          if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive))
          if still_alive==0:
            break
          xbmc.sleep(100)

    all_new_data=sorted(all_new_data, key=lambda x: x[10], reverse=False)
    for new_name,icon,fan,plot,year,original_name,id,rating,genere,trailer,xxx in all_new_data:
        if icon=='' and fan=='':
            addNolink(new_name,'www',199,False,iconimage=domain_s+'pbs.twimg.com/profile_images/421736697647218688/epigBm2J.jpeg',fanart='http://www.dream-wallpaper.com/free-wallpaper/cartoon-wallpaper/spawn-wallpaper/1280x1024/free-wallpaper-24.jpg')
        else:
            addDir3(new_name,url,4,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer)
    if "a class='monthlink' href='" in html_o:
     regex="<a class='monthlink' href='(.+?)' >(.+?)<"
     match=re.compile(regex).findall(html_o)
     for link,name in match:
       addDir3('[COLOR aqua][I]'+name+'[/I][/COLOR]'.decode('utf8'),domain_s+'www.dvdsreleasedates.com'+link,28,' ',' ','Older results'.decode('utf8'))
       break
    if Addon.getSetting("dp")=='true':
        dp.close()
def get_movie_data(url):
    html=requests.get(url).json()
    return html
def main_trakt():
   addDir3('Lists','www',64,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Lists')
   addDir3('Progress','users/me/watched/shows?extended=full',63,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Progress')
   addDir3('Episode watchlist ','sync/watchlist/episodes?extended=full',63,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Episode watchlist')
   addDir3('Series watchlist','users/me/watchlist/episodes?extended=full',31,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Series watchlist')
   
   addDir3('TV Collection','users/me/collection/shows',31,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','collection')
   addDir3('Shows watchlist','users/me/watchlist/shows',31,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Shows watchlist')
   addDir3('Movies watchlist','users/me/watchlist/movies',31,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Movies watchlist')
   
   addDir3('Movies Collection','users/me/collection/movies',31,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','collection')
   
   addDir3('Watched movies','users/me/watched/movies',31,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Watched movies')
   addDir3('Watched shows','users/me/watched/shows',31,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Watched shows')
   addDir3('Liked lists','users/likes/lists',142,'https://kodi.expert/wp-content/uploads/2018/05/trakt-logo.png','https://seo-michael.co.uk/content/images/2016/08/trakt.jpg','Watched shows',data='1')
   
   
   
   
def get_trakt():
    
    trakt_lists=call_trakt("users/me/lists")
    #trakt_lists=call_trakt('users/me/collection/shows')

    my_lists = []
    
    for list in trakt_lists:
        my_lists.append({
            'name': list["name"],
            'user': list["user"]["username"],
            'slug': list["ids"]["slug"]
        })

    for item in my_lists:
        user = item['user']
        slug = item['slug']
        url=user+'$$$$$$$$$$$'+slug
        addDir3(item['name'],url,31,' ',' ',item['name'])
def progress_trakt(url):
        if  Addon.getSetting("fav_search_f_tv")=='true' and Addon.getSetting("fav_servers_en_tv")=='true' and len(Addon.getSetting("fav_servers_tv"))>0:
           fav_status='true'
        else:
            fav_status='false'
        if Addon.getSetting("dp")=='true':
                dp = xbmcgui.DialogProgress()
                dp.create("Loading Episodes", "Please wait", '')
                dp.update(0)
        import datetime
        start_time = time.time()
        xxx=0
        ddatetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
     
  
        html_g=requests.get(url_g).json()
        result = call_trakt(url)
     
        items = []
        

        new_name_array=[]
        
        for item in result:
          
            try:
                num_1 = 0
                if 'seasons' in item:
                    for i in range(0, len(item['seasons'])):
                        if item['seasons'][i]['number'] > 0: num_1 += len(item['seasons'][i]['episodes'])
                    num_2 = int(item['show']['aired_episodes'])
                    if num_1 >= num_2: raise Exception()

                    season = str(item['seasons'][-1]['number'])

                    episode = [x for x in item['seasons'][-1]['episodes'] if 'number' in x]
                    episode = sorted(episode, key=lambda x: x['number'])
                    episode = str(episode[-1]['number'])
                else:
                    season = str(item['episode']['season'])
                    episode=str(item['episode']['number'])
                

                tvshowtitle = item['show']['title']
                if tvshowtitle == None or tvshowtitle == '': raise Exception()
                tvshowtitle = replaceHTMLCodes(tvshowtitle)

                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                if int(year) > int(ddatetime.strftime('%Y')): raise Exception()

                imdb = item['show']['ids']['imdb']
                if imdb == None or imdb == '': imdb = '0'

                tmdb = item['show']['ids']['tmdb']
                if tmdb == None or tmdb == '': raise Exception()
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                
               
                trakt = item['show']['ids']['trakt']
                if trakt == None or trakt == '': raise Exception()
                trakt = re.sub('[^0-9]', '', str(trakt))
                if 'last_watched_at' in item:
                    last_watched = item['last_watched_at']
                else:
                    last_watched = item['listed_at']
                if last_watched == None or last_watched == '': last_watched = '0'
                items.append({'imdb': imdb, 'tmdb': tmdb, 'tvshowtitle': tvshowtitle, 'year': year, 'snum': season, 'enum': episode, '_last_watched': last_watched})
            
            except Exception as e:
               logging.warning(e)
            
            
        result = call_trakt('/users/hidden/progress_watched?limit=1000&type=show')
        result = [str(i['show']['ids']['tmdb']) for i in result]

        items_pre = [i for i in items if not i['tmdb'] in result]

      
        for items in items_pre:
          watched='no'
          not_yet=0
          gone=0
          season=items['snum']
          episode=items['enum']
          
          url='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=en&append_to_response=external_ids'%(items['tmdb'],'1248868d7003f60f2386595db98455ef')
          #url='http://api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(items['tmdb'],season)
          html=cache.get(get_movie_data,time_to_save,url, table='pages')
          plot=' '
          if 'The resource you requested could not be found' not in str(html):
             data=html
            
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
                if data['first_air_date']==None:
                    year=' '
                else:
                    year=str(data['first_air_date'].split("-")[0])
             else:
                if 'release_date' in data:
                  if data['release_date']==None:
                    year=' '
                  else:
                    year=str(data['release_date'].split("-")[0])
                else:
                    year=' '
             if 'overview' in data:
                 if data['overview']==None:
                   plot=' '
                 else:
                   plot=data['overview']
             else:
                plot=' '
             if 'title' not in data:
               new_name=data['name']
             else:
               new_name=data['title']
             f_subs=[]
             
             original_name=data['original_name']
             id=str(data['id'])
             mode=4
             if data['poster_path']==None:
              icon=' '
             else:
               icon=data['poster_path']
             if 'backdrop_path' in data:
                 if data['backdrop_path']==None:
                  fan=' '
                 else:
                  fan=data['backdrop_path']
             else:
                fan=html['backdrop_path']
             if plot==None:
               plot=' '
             if 'http' not in fan:
               fan=domain_s+'image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon=domain_s+'image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x['id']] for x in data['genres']])
             except:genere=''

   
            
             trailer = "plugin://plugin.video.destiny?mode2=25&url=www&id=%s" % id
             if new_name not in new_name_array:
              new_name_array.append(new_name)
              
              color='white'
              elapsed_time = time.time() - start_time
              if Addon.getSetting("dp")=='true':
                dp.update(int(((xxx* 100.0)/(len(html))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
              xxx=xxx+1
              if int(data['last_episode_to_air']['season_number'])>=int(season):
                if int(data['last_episode_to_air']['episode_number'])>int(episode):
                
                  episode=str(int(episode)+1)
                else:
                 if int(data['last_episode_to_air']['season_number'])>int(season):
                   season=str(int(season)+1)
                   episode='1'
                 else:
                  if (data['next_episode_to_air'])!=None:
                    season=str(int(season)+1)
                    episode='1'
                    not_yet='1'
                  else:
                    gone=1
              else:
                    if (data['next_episode_to_air'])!=None:
                        season=str(int(season)+1)
                        episode='1'
                        not_yet='1'
                    else:
                        gone=1
              video_data={}

              

              video_data['mediatype']='tvshow'
              video_data['OriginalTitle']=new_name
              video_data['title']=new_name



              video_data['year']=year
              video_data['season']=season
              video_data['episode']=episode
              video_data['genre']=genere
              
              if len(episode)==1:
                  episode_n="0"+episode
              else:
                   episode_n=episode
              if len(season)==1:
                  season_n="0"+season
              else:
                  season_n=season
              if Addon.getSetting("trac_trk")=='true':
                addon='\n'+' Season'+season_n+'-Episode '+episode_n
              else:
                addon=''
              video_data['plot']=plot+addon
              try:
                max_ep=data['seasons'][int(season)-1]['episode_count']
              except Exception as e:
                max_ep=100
            
              if gone==0:
                  if not_yet==0:
                  
                    if episode_n=='01':
                      dates=json.dumps((0,'' ,''))
                    elif max_ep<=int(episode):
                        dates=json.dumps(('','' ,0))
                    else:
                      dates=json.dumps(('','' ,''))
                    
                    addDir3('[COLOR '+color+']'+new_name+'[/COLOR]'+' S'+season_n+'E'+episode_n,url,mode,icon,fan,plot+addon,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,season=season,episode=episode,eng_name=original_title,tmdbid=id,video_info=video_data,dates=dates,fav_status=fav_status)
                  else:
                   addNolink('[COLOR red][I]'+ new_name.encode('utf8')+'[/I][/COLOR]'+' S'+season_n+'E'+episode_n, 'www',999,False,iconimage=icon,fanart=fan)
          else:
            
           
            responce=call_trakt("shows/{0}".format(items['trakt']), params={'extended': 'full'})
          
           
            addNolink('[COLOR red][I]'+ responce['title']+'[/I][/COLOR]', 'www',999,False)
            
        if Addon.getSetting("dp")=='true':
          dp.close()
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
def get_trk_data(url,page):
        o_url=url
        try:
            a=int(page)
        except:
           page=1
        time_to_save=int(Addon.getSetting("save_time"))
        xxx=0
        if Addon.getSetting("dp")=='true':
                    dp = xbmcgui.DialogProgress()
                    dp.create("Loading", "Please wait", '')
                    dp.update(0)
        url_g_m=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
                     
        
        url_g_tv=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
        html_g_tv=requests.get(url_g_tv).json()
        html_g_m=requests.get(url_g_m).json()
        start_time = time.time()
        src="tmdb" 
            
        i,pages = (call_trakt('/users/me/watched/movies',pagination=True,page=page))
        logging.warning('Pages:'+str(pages))
        all_movie_w=[]
        for ids in i:
          all_movie_w.append(str(ids['movie']['ids']['tmdb']))
      
         
        if '$$$$$$$$$$$' in url:
            data_in=url.split('$$$$$$$$$$$')
            user = data_in[0]
            slug = data_in[1]
            selected={'slug':data_in[1],'user':data_in[0]}

            responce=call_trakt("/users/{0}/lists/{1}/items".format(user, slug))
        else:
           responce=call_trakt(url)
        new_name_array=[]
        
        for items in responce:
          
          if 'show' in items:
             slug = 'tv'
             html_g=html_g_tv
          else:
            slug = 'movies'
            html_g=html_g_m
          if slug=='movies':
            url='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=en&append_to_response=external_ids'%(items['movie']['ids']['tmdb'],'1248868d7003f60f2386595db98455ef')
          else:
            url='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=en&append_to_response=external_ids'%(items['show']['ids']['tmdb'],'1248868d7003f60f2386595db98455ef')
          
          html=cache.get(get_movie_data,time_to_save,url, table='pages')
          if 'The resource you requested could not be found' not in str(html):
             data=html
             
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
               if data['first_air_date']==None:
                    year=' '
               else:
                year=str(data['first_air_date'].split("-")[0])
             else:  
                if 'release_date' in data:
                  if data['release_date']==None:
                    year=' '
                  else:
                    year=str(data['release_date'].split("-")[0])
                else:
                    year=' '
             if 'overview' in data:
                 if data['overview']==None:
                   plot=' '
                 else:
                   plot=data['overview']
             else:
                plot=' '
             if 'title' not in data:
               new_name=data['name']
             else:
               new_name=data['title']
             f_subs=[]
             if slug=='movies':
               original_name=data['original_title']
               mode=4
               
               id=str(data['id'])
             else:
                 original_name=data['original_name']
                 id=str(data['id'])
                 mode=7
             if data['poster_path']==None:
              icon=' '
             else:
               icon=data['poster_path']
             if 'backdrop_path' in data:
                 if data['backdrop_path']==None:
                  fan=' '
                 else:
                  fan=data['backdrop_path']
             else:
                fan=html['backdrop_path']
             if plot==None:
               plot=' '
             if 'http' not in fan:
               fan=domain_s+'image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon=domain_s+'image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x['id']] for x in data['genres']])
             except:genere=''

   
            
             trailer = "plugin://plugin.video.destiny?mode2=25&url=www&id=%s" % id
             if new_name not in new_name_array:
              new_name_array.append(new_name)
              
              color='white'
              elapsed_time = time.time() - start_time
              if Addon.getSetting("dp")=='true':
                dp.update(int(((xxx* 100.0)/(len(html))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
              xxx=xxx+1
              watched='no'
              if id in all_movie_w:
                watched='yes'
              '''
              if id in all_tv_w:
                 if season+'x'+episode in all_tv_w[id]:
                  watched='yes'
              '''
              if slug=='movies':
                    fav_search_f=Addon.getSetting("fav_search_f")
                    fav_servers_en=Addon.getSetting("fav_servers_en")
                    fav_servers=Addon.getSetting("fav_servers")
                   
                  
              else:
                    fav_search_f=Addon.getSetting("fav_search_f_tv")
                    fav_servers_en=Addon.getSetting("fav_servers_en_tv")
                    fav_servers=Addon.getSetting("fav_servers_tv")
                   
        
   
              if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 ):
                    fav_status='true'
              else:
                    fav_status='false'
             
            
              addDir3('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status)
          else:
            
            if slug=='movies':
                responce=call_trakt("movies/{0}".format(items['movie']['ids']['trakt']), params={'extended': 'full'})
            else:
                responce=call_trakt("shows/{0}".format(items['show']['ids']['trakt']), params={'extended': 'full'})
           
           
            addNolink('[COLOR red][I]'+ responce['title']+'[/I][/COLOR]', 'www',999,False)
            
        if Addon.getSetting("dp")=='true':
          dp.close()
        if int(page)<int(pages):
            addDir3('[COLOR aqua][I]Next Page[/COLOR][/I]',o_url,31,iconImage,fanart,'[COLOR aqua][I]Next Page[/COLOR][/I]',data=str(int(page)+1))
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
def get_one_trk(color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image):
          global all_data_imdb
          import _strptime
          data_ep=''
          dates=' '
          fanart=image
          url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(id,season)
         
          html=requests.get(url).json()
          next=''
          ep=0
          f_episode=0
          catch=0
          counter=0
          if 'episodes' in html:
              for items in html['episodes']:
                if 'air_date' in items:
                   try:
                       datea=items['air_date']+'\n'
                       
                       a=(time.strptime(items['air_date'], '%Y-%m-%d'))
                       b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
                      
                   
                       if a>b:
                         if catch==0:
                           f_episode=counter
                           
                           catch=1
                       counter=counter+1
                       
                   except:
                         ep=0
          else:
             ep=0
          episode_fixed=int(episode)-1
          try:
              plot=html['episodes'][int(episode_fixed)]['overview']
          
              ep=len(html['episodes'])
              if (html['episodes'][int(episode_fixed)]['still_path'])==None:
                fanart=image
              else:
                fanart=domain_s+'image.tmdb.org/t/p/original/'+html['episodes'][int(episode_fixed)]['still_path']
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'Season '+season+'-Episode '+episode+ '[/COLOR]\n[COLOR gold] out of ' +str(f_episode)  +' episode for this season[/COLOR]\n' 
              if int(episode)>1:
                
                prev_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)-1]['air_date'], '%Y-%m-%d'))) 
              else:
                prev_ep=0

          

                      
              if int(episode)<ep:

                if (int(episode)+1)>=f_episode:
                  color_ep='magenta'
                  next_ep='[COLOR %s]'%color_ep+time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) +'[/COLOR]'
                else:
                  
                  next_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
              else:
                next_ep=0
              dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
              if int(episode)<int(f_episode):
               color='gold'
              else:
               color='white'
               h2=requests.get('https://api.themoviedb.org/3/tv/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US'%id).json()
               last_s_to_air=int(h2['last_episode_to_air']['season_number'])
               last_e_to_air=int(h2['last_episode_to_air']['episode_number'])
              
               if int(season)<last_s_to_air:
      
                 color='lightblue'
            
               if h2['status']=='Ended' or h2['status']=='Canceled':
                color='peru'
               
               
               if h2['next_episode_to_air']!=None:
                 
                 if 'air_date' in h2['next_episode_to_air']:
                  
                  a=(time.strptime(h2['next_episode_to_air']['air_date'], '%Y-%m-%d'))
                  next=time.strftime( "%d-%m-%Y",a)
                  
               else:
                  next=''
                 
          except Exception as e:
              logging.warning('Error :'+ heb_name)
              logging.warning('Error :'+ str(e))
              plot=' '
              color='green'
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'Season '+season+'-Episode '+episode+ '[/COLOR]\n[COLOR gold] out of ' +str(f_episode)  +' episode for this season [/COLOR]\n' 
              dates=' '
              fanart=image
          try:
            f_name=urllib.unquote_plus(heb_name.encode('utf8'))
     
          except:
            f_name=name
          if (heb_name)=='':
            f_name=name
          if color=='peru':
            add_p='[COLOR peru][B]This show was over or canceled[/B][/COLOR]'+'\n'
          else:
            add_p=''
          add_n=''
          if color=='white' and url_o=='tv' :
              if next !='':
                add_n='[COLOR tomato][I]Next episode at ' +next+'[/I][/COLOR]\n'
              else:
                add_n='[COLOR tomato][I]Next episode at ' +' Unknown '+'[/I][/COLOR]\n'

          
          all_data_imdb.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
          return data_ep,dates,fanart,color,next
def get_Series_trk_data(url_o,match):
        import _strptime
        cacheFile_trk = os.path.join(user_dataDir, 'cache_play_trk.db')
        dbcon_trk2 = database.connect(cacheFile_trk)
        dbcur_trk2  = dbcon_trk2.cursor()
        dbcur_trk2.execute("CREATE TABLE IF NOT EXISTS %s ( ""data_ep TEXT, ""dates TEXT, ""fanart TEXT,""color TEXT,""id TEXT,""season TEXT,""episode TEXT, ""next TEXT,""plot TEXT);" % 'AllData4')
        dbcon_trk2.commit()
        dbcur_trk2.execute("DELETE FROM AllData4")

        image=' '
        for item in match:
          next=''
          name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
          #name,id,season,episode=item
          data_ep=''
          dates=' '
          fanart=image
          url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(id,season)
         
          html=requests.get(url).json()
          if 'status_message' in html:
            if html['status_message']!='The resource you requested could not be found.':
                xbmc.sleep(10000)
                html=requests.get(url).json()
            
          ep=0
          f_episode=0
          catch=0
          counter=0
          if 'episodes' in html:
              for items in html['episodes']:
                if 'air_date' in items:
                   try:
                       datea=items['air_date']+'\n'
                       
                       a=(time.strptime(items['air_date'], '%Y-%m-%d'))
                       b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
                      
                   
                       if a>b:
                         if catch==0:
                           f_episode=counter
                           
                           catch=1
                       counter=counter+1
                       
                   except:
                         ep=0
          else:
             ep=0
          episode_fixed=int(episode)-1
          try:
              try:
                plot=html['episodes'][int(episode_fixed)]['overview']
              except:
                logging.warning(name.decode('utf-8'))
                if 'episodes' not in html:
                    logging.warning(html)
                    
                
                logging.warning(episode_fixed)
                
                plot=''
                pass
              
          
              ep=len(html['episodes'])
              if (html['episodes'][int(episode_fixed)]['still_path'])==None:
                fanart=image
              else:
                fanart=domain_s+'image.tmdb.org/t/p/original/'+html['episodes'][int(episode_fixed)]['still_path']
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'Season '+season+'-Episode '+episode+ '[/COLOR]\n[COLOR gold] out of ' +str(f_episode)  +" Season's Episodes  [/COLOR]\n" 
              if int(episode)>1:
                
                prev_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)-1]['air_date'], '%Y-%m-%d'))) 
              else:
                prev_ep=0

          

              try:
                  if int(episode)<ep:
                    
                    if (int(episode)+1)>=f_episode:
                      color_ep='magenta'
                      next_ep='[COLOR %s]'%color_ep+time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) +'[/COLOR]'
                    else:
                      
                      next_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
                  else:
                    next_ep=0
              except:
                next_ep=0
              dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
              if int(episode)<int(f_episode):
               color='gold'
              else:
               color='white'
               h2=requests.get('https://api.themoviedb.org/3/tv/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US'%id).json()
               last_s_to_air=int(h2['last_episode_to_air']['season_number'])
               last_e_to_air=int(h2['last_episode_to_air']['episode_number'])
              
               if int(season)<last_s_to_air:
        
                 color='lightblue'
               if h2['status']=='Ended' or h2['status']=='Canceled':
                color='peru'
                
               if h2['next_episode_to_air']!=None:
                 if 'air_date' in h2['next_episode_to_air']:
                    a=(time.strptime(h2['next_episode_to_air']['air_date'], '%Y-%m-%d'))
                    next=time.strftime( "%d-%m-%Y",a)
               else:
                  next=''
          
          except Exception as e:
              import linecache
              exc_type, exc_obj, tb = sys.exc_info()
              f = tb.tb_frame
              lineno = tb.tb_lineno
              filename = f.f_code.co_filename
              linecache.checkcache(filename)
              line = linecache.getline(filename, lineno, f.f_globals)
              
              logging.warning('ERROR IN Series Tracker:'+str(lineno))
              logging.warning('inline:'+line)
              logging.warning(e)
              logging.warning('BAD Series Tracker')
              plot=' '
              color='green'
              if f_episode==0:
                f_episode=ep
              data_ep='[COLOR aqua]'+'Season '+season+'-Episode '+episode+ '[/COLOR]\n[COLOR gold] out of ' +str(f_episode)  +" Season's episodes [/COLOR]\n" 
              dates=' '
              fanart=image
          
          dbcon_trk2.execute("INSERT INTO AllData4 Values ('%s', '%s', '%s', '%s','%s', '%s', '%s','%s','%s');" % (data_ep.replace("'","%27"),json.dumps(dates),fanart.replace("'","%27"),color,id,season,episode,next,plot.replace("'","%27")))
        dbcon_trk2.commit()
        dbcon_trk2.close()
        logging.warning('TRD SUCE')
        return 0
def check_next_last_tv_subs(original_title,name,season,episode,show_original_year,id):
    global susb_data_next
   
    
    
    
    if len(episode)==1:
          episode_n="0"+episode
    else:
           episode_n=episode
    if len(season)==1:
          season_n="0"+season
    else:
          season_n=season
      
   
        #f_name='√√ '+f_name
    return susb_data_next
def check_last_tv_subs(original_title,name,season,episode,show_original_year,id):
    global susb_data
   
    
    
    
    if len(episode)==1:
          episode_n="0"+episode
    else:
           episode_n=episode
    if len(season)==1:
          season_n="0"+season
    else:
          season_n=season
      
    
        #f_name='√√ '+f_name
    return susb_data
def last_viewed(url_o,isr=' '):
    global all_data_imdb
    

    global susb_data,susb_data_next
    import datetime
    strptime = datetime.datetime.strptime
    start_time=time.time()
    if Addon.getSetting("dp_play")=='true':
     
         dp = xbmcgui.DialogProgress()
         dp.create("Collecting", "Please wait", '')
         
         elapsed_time = time.time() - start_time
         dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Collecting', '')
         
    color='white'
    
    if url_o=='tv':
        dbcur.execute("SELECT  * FROM Lastepisode WHERE  type='tv' ")
    else:
       dbcur.execute("SELECT * FROM AllData WHERE  type='movie'")
    match_tv = dbcur.fetchall()
    xxx=0
    all_data_imdb=[]
    thread=[]
    
    for item in match_tv:
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
      
      logging.warning('isr2:'+isr)
      dates=' '
      next=''
      data_ep=''
      fanart=image
      if Addon.getSetting("dp_play")=='true' :
        dp.update(int(((xxx* 100.0)/(len(match_tv))) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Collection', clean_name(original_title,1))
      xxx+=1
      done_data=0
      if url_o=='tv' :
          try:
              dbcur_trk.execute("SELECT  * FROM AllData4 WHERE  id='%s' AND season='%s' AND episode='%s'"%(id,season,episode))
               
                  
              match2 = dbcur_trk.fetchone()

            
              if match2!=None:
                data_ep,dates,fanart,color,i,j,k,next,plot=match2
                dates=json.loads(dates)

                if color=='white' :
                    
                    thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
                    thread[len(thread)-1].setName(clean_name(original_title,1))
                    done_data=1
                    #data_ep,dates,fanart,color,next=get_one_trk(color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image)
              else:

                thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
                thread[len(thread)-1].setName(clean_name(original_title,1))
                done_data=1
                #data_ep,dates,fanart,color,next=get_one_trk(color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image)
          except:
            thread.append(Thread(get_one_trk,color,name,url_o,url,icon,fanart,data_ep,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image))
            thread[len(thread)-1].setName(clean_name(original_title,1))
            done_data=1
            #data_ep,dates,fanart,color,next=get_one_trk(color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,image)
     
      if done_data==0:
          try:
            f_name=urllib.unquote_plus(heb_name.encode('utf8'))
     
          except:
            f_name=name
          if (heb_name)=='':
            f_name=name
          if color=='peru':
            add_p='[COLOR peru][B]This show was over or canceled[/B][/COLOR]'+'\n'
          else:
            add_p=''
          add_n=''
          if color=='white' and url_o=='tv' :
              if next !='':
                add_n='[COLOR tomato][I]Next episode at ' +next+'[/I][/COLOR]\n'
              else:
                add_n='[COLOR tomato][I]Next episode at ' +' Unknown '+'[/I][/COLOR]\n'
          
          all_data_imdb.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx))
      
    
    for td in thread:
        td.start()

        if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
        if len(thread)>38:
            xbmc.sleep(255)
        else:
            xbmc.sleep(10)
    while 1:

          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              
              still_alive=1
              all_alive.append(thread[yy].name)
          if still_alive==0:
            break
          if Addon.getSetting("dp")=='true' :
                elapsed_time = time.time() - start_time
                dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive)," ")
          xbmc.sleep(100)
          if Addon.getSetting("dp")=='true' :
              if dp.iscanceled():
                dp.close()
              
                break
    
    thread=[]
    if url_o=='tv':
        dbcur.execute("SELECT * FROM subs")
        match = dbcur.fetchall()
        all_subs_db=[]
        for title,id,season,episode in match:
            if len(episode)==1:
              episode_n="0"+episode
            else:
               episode_n=episode
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
            next_ep=str(int(episode_n)+1)
            if len(next_ep)==1:
              next_ep_n="0"+next_ep
            else:
              next_ep_n=next_ep
            sub_title=title.replace("%27","'")+'-'+id+'-'+season_n+'-'+episode_n
            all_subs_db.append(sub_title)
        for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx in all_data_imdb:
            if len(episode)==1:
              episode_n="0"+episode
            else:
               episode_n=episode
            if len(season)==1:
              season_n="0"+season
            else:
              season_n=season
            next_ep=str(int(episode_n)+1)
            if len(next_ep)==1:
              next_ep_n="0"+next_ep
            else:
              next_ep_n=next_ep
            sub_title=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+episode_n
            sub_title_next=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+next_ep_n
            if (color=='gold' or color=='white')  :
           
                if sub_title not in all_subs_db:
                    thread.append(Thread(check_last_tv_subs,original_title,heb_name,season,episode,show_original_year,id))
                    thread[len(thread)-1].setName(eng_name+' '+episode)
                if color=='gold' and sub_title_next not in all_subs_db:
                    thread.append(Thread(check_next_last_tv_subs,original_title,heb_name,season,str(int(episode)+1),show_original_year,id))
                    thread[len(thread)-1].setName(eng_name+' '+str(int(episode)+1))
           
            
    susb_data={}
    susb_data_next={}
    if url_o=='tv' :
        for td in thread:
            td.start()

            if Addon.getSetting("dp")=='true' :
                    elapsed_time = time.time() - start_time
                    dp.update(0, ' Starting '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
        while 1:

              still_alive=0
              all_alive=[]
              for yy in range(0,len(thread)):
                
                if  thread[yy].is_alive():
                  
                  still_alive=1
                  all_alive.append(thread[yy].name)
              if still_alive==0:
                break
              
              xbmc.sleep(100)
              if Addon.getSetting("dp")=='true' :
                  if dp.iscanceled():
                    dp.close()
                  
                    break
    all_data_imdb=sorted(all_data_imdb, key=lambda x: x[19], reverse=False)
    all_o_data=[]
    level=0
    for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx in all_data_imdb:
        if url_o=='tv':
            if color=='gold':
                level=1
            elif color=='lightblue':
                level=2
            elif color=='green':
                level=3
            elif color=='white':
                level=4
            elif color=='peru':
                level=5
        else:
            level+=1
        all_o_data.append((color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,level))
    if url_o=='tv':
        order=False
    else:
        order=True
    if Addon.getSetting("order_latest")=='true':
        all_o_data=sorted(all_o_data, key=lambda x: x[20], reverse=order)
    for color,f_name,url,icon,fanart,add_p,data_ep,add_n,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,xxx,pos in all_o_data:
       
        if len(episode)==1:
          episode_n="0"+episode
        else:
           episode_n=episode
        if len(season)==1:
          season_n="0"+season
        else:
          season_n=season
        next_ep=str(int(episode_n)+1)
        if len(next_ep)==1:
          next_ep_n="0"+next_ep
        else:
          next_ep_n=next_ep
          
        sub_title=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+episode_n
        sub_title_next=original_title.replace("%27","'")+'-'+id+'-'+season_n+'-'+next_ep_n

        all_d=((dates))
        if color!='white' and len(all_d)>1:
          
            
            
            
            add_n='[COLOR aqua]'+' Aired at '+all_d[1] + '[/COLOR]\n'
            
        plot=plot.replace('%27',"'")
        
        addDir3('[COLOR %s]'%color+ f_name+'[/COLOR]', url,4, icon,fanart,add_p+data_ep+add_n+plot,data=year,original_title=original_title,id=id,season=season,episode=episode,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=json.dumps(dates))
    dbcur_trk.close()
    dbcon_trk.close()
    
    read_data2=[]
    if url_o=='tv' :
        read_data2.append((url_o,match_tv))
    

    if Addon.getSetting("dp_play")=='true' :
        dp.close()
    return read_data2
def last_viewed_tvshows(url_o):
    color='white'
    
    if url_o=='tv':
        dbcur.execute("SELECT  * FROM Lastepisode WHERE  type='tv' ")
    else:
       dbcur.execute("SELECT * FROM AllData WHERE  type='movie'")
    match = dbcur.fetchall()
    all_o_data=[]
    level=0
    for item in match:
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
      dates=' '
      

      
      try:
        f_name=urllib.unquote_plus(name.encode('utf8'))
 
      except:
        f_name=name
      if (heb_name)=='':
        f_name=name
      level+=1
      all_o_data.append((color,f_name,url,icon,image,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,level))
    all_o_data=sorted(all_o_data, key=lambda x: x[16], reverse=True)
    if url_o=='tv':
        n_mode=7
    else:
        n_mode=4
    for color,f_name,url,icon,fanart,plot,year,original_title,id,season,episode,eng_name,show_original_year,heb_name,isr,dates,pos in all_o_data:
        if heb_name=='Direct link':
            video_data={}
            video_data['title']=f_name
            video_data['year']=year
            video_data['plot']=plot
            
            addLink(f_name,url,5,False,iconimage=icon,fanart=fanart,description=plot,data=year,id=id,video_info=json.dumps(video_data))
        else:
            addDir3('[COLOR %s]'%color+ f_name.encode('utf8')+'[/COLOR]', url,n_mode, icon,fanart,plot,data=year,original_title=original_title,id=id,season=season,episode=episode,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=json.dumps(dates))

def scan_direct_links(next):
    from timeit import default_timer as timer
    servers_db=os.path.join(__PLUGIN_PATH__, "resources","servers.db")
    dp = xbmcgui.DialogProgress()
    dp.create("Scaning", "Please wait", '','')
    dp.update(0)
    dbconserver = database.connect(servers_db)
    dbcurserver = dbconserver.cursor()


    dbcurserver.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""speed TEXT);" % 'servers')
    dbcurserver.execute("VACUUM 'AllData';")
    dbcurserver.execute("PRAGMA auto_vacuum;")
    dbcurserver.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
    dbcurserver.execute("PRAGMA temp_store=MEMORY ;")
    dbconserver.commit()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; HUAWEI MT7-TL00 Build/HuaweiMT7-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.3.8.909 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }
    headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    if next=='www':
     html=requests.get(domain_s+'filepursuit.com/discover.php',headers=headers).content
    else:
      html=requests.get(domain_s+'filepursuit.com/discover.php?startrow='+next,headers=headers).content

    
    regex="discover.php\?link=(.+?)'>(.+?)<"
    match_all=re.compile(regex).findall(html)
    f_time_avg=0
    xxx=0

    for links,name in match_all:
      f_time_avg=0

      for i in range(0,5):
          try:
            start = timer()
            html2=requests.get(links,headers=headers2,timeout=1).content
            if  'provider nor the domain owner maintain any relationship with the advertisers.' in html2 or 'tehmovies.org has expired' in html2 or domain_s+'www.google.com/recaptcha/api/fallback?k=' in html2 or 'Access Denied' in html2 or 'not found' in html2.lower() or 'Unauthorized' in html2 or 'Forbidden' in html2 or 'Service Unavailable' in html2:
              f_time='TIMEOUT'
              f_time_avg='TIMEOUT'
            else:
                end = timer()
                f_time=float(end-start)
                f_time_avg=f_time_avg+f_time
          except Exception as e:
            logging.warning(e)
            f_time='TIMEOUT'
            f_time_avg='TIMEOUT'
            break
      if dp.iscanceled():
          dp.close()
          return 0
          break
      if f_time_avg!='TIMEOUT':
        final_time=str(f_time_avg/6)
      else:
        final_time='TIMEOUT'
      if next=='www':
        next=0
      dp.update(int(((xxx* 100.0)/(len(match_all))) ), name,final_time,'Page '+str(int(next)/50))
      xxx=xxx+1
      dbcurserver.execute("SELECT * FROM servers WHERE name = '%s'"%(name))

      match = dbcur.fetchone()
      if match==None:
          dbcurserver.execute("INSERT INTO servers Values ('%s', '%s');" %  (name.replace("'"," "),final_time))
          dbconserver.commit()
      else:
          
          dbcurserver.execute("UPDATE servers SET speed='%s' WHERE name = '%s'"%(final_time,name.replace("'"," ")))
          dbconserver.commit()
    dp.close()
    regex='"discover.php\?startrow=(.+?)">Next</'
    match_next=re.compile(regex).findall(html)
    if len(match_next)>0:
      scan_direct_links(match_next[0])
def remove_from_trace(name,original_title,id,season,episode):

    if id=='0':
      ok=xbmcgui.Dialog().yesno(("Remove from Series tracker"),(' from Series tracker?'+name+"Remove "))
    else:
      ok=xbmcgui.Dialog().yesno(("Remove watched"),(' from watched?'+name+"Remove "))
    if ok:
      if id=='0':
        dbcur.execute("DELETE  FROM Lastepisode WHERE original_title = '%s'"%(original_title))
      
        dbcon.commit()
      else:
      
        if len(episode)==0:
          episode='%20'
        if len(season)==0:
          season='%20'
        episode=episode.replace(" ","%20")
        season=season.replace(" ","%20")
        dbcur.execute("DELETE  FROM  AllData WHERE original_title = '%s'  AND season='%s' AND episode = '%s'"%(original_title,season.replace(" ","%20"),episode.replace(" ","%20")))
       
        
        dbcon.commit()
       
      xbmc.executebuiltin('Container.Refresh')
def play_level_movies(url):
    from youtube_ext import get_youtube_link2
            
    playback_url= get_youtube_link2(url).replace(' ','%20')
    #from pytube import YouTube
    #playback_url = YouTube(url).streams.first().download()
     
   
    
    
    item = xbmcgui.ListItem(path=playback_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)


def fast_play(final_link):
    listItem = xbmcgui.ListItem('FP', path=final_link) 
    listItem.setInfo(type='Video', infoLabels={'title':'FP'})


    listItem.setProperty('IsPlayable', 'true')

        
    ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
def get_jen_cat():
    #addNolink( '[COLOR blue][B][I]Update Jen DB[/I][/B][/COLOR]', 'www',131,False, iconimage="DefaultFolder.png",fanart="DefaultFolder.png",description=' ')
    for i in range (1,7):

        cat_ena=Addon.getSetting("jen_cat-"+str(i))
        
        
        if Addon.getSetting("jen_icon_cat-"+str(i))!='':
            icon=Addon.getSetting("jen_icon_cat-"+str(i))
        else:
            icon='https://i.pinimg.com/736x/f2/4a/95/f24a95322599dd911e293779cd34a00a--purple-wallpaper-wallpaper-space.jpg'
        if Addon.getSetting("jen_fan_cat-"+str(i))!='':
            fan=Addon.getSetting("jen_fan_cat-"+str(i))
        else:
            fan='https://koditips.com/wp-content/uploads/jen-kodi.jpg'
        if cat_ena=='true':
          addDir3(Addon.getSetting("jen_name_cat-"+str(i)),str(i),43,icon,fan,Addon.getSetting("jen_name_cat-"+str(i)))
def fix_name_origin(saved_name,original_title):
         regex_name='] (.+?) -'

         if saved_name==None:
            saved_name=''
         match_name=re.compile(regex_name).findall(saved_name)
         if len(match_name)>0:
           fixed_name=match_name[0]
          
           if clean_name(original_title,1).replace(' ','').replace(':','').replace("'",'').lower() not in fixed_name.replace("'",'').replace('.',' ').replace('_',' ').replace('-',' ').replace(':','').replace(' ','').lower():
            
             fixed_name=original_title
         else:
           
           fixed_name=saved_name
           
           if clean_name(original_title,1).replace(' ','').replace(':','').replace("'",'').lower() not in fixed_name.replace("'",'').replace('.',' ').replace('_',' ').replace('-',' ').replace(':','').replace(' ','').lower():
             
             fixed_name=original_title
         return fixed_name

def resolve_magnet(url,listitem,AWSHandler,info,mag_start_time):
    if Addon.getSetting('allow_free')=='false':

        return ''
    from kodipopcorntime.torrent import TorrentPlayer
    from kodipopcorntime import settings
    mediaSettings = getattr(settings, 'movies')
    item={'info': {'rating': 0.0, 'plotoutline': 'Elastigirl springs into action to save the day, while Mr. Incredible faces his greatest challenge yet \xe2\x80\x93 taking care of the problems of his three children.', 'code': 'tt3606756', 'director': '', 'studio': '', 'year': 2018, 'genre': 'animation / family / action / adventure / superhero', 'plot': 'Elastigirl springs into action to save the day, while Mr. Incredible faces his greatest challenge yet \xe2\x80\x93 taking care of the problems of his three children.', 'votes': 0.0, 'castandrole': [], 'title': 'Playing', 'tagline': '1080p: 18930 seeds; 720p: 14301 seeds; ', 'writer': '', 'originaltitle': 'Incredibles 2'}, 'thumbnail': 'http://image.tmdb.org/t/p/w500/x1txcDXkcM65gl7w20PwYSxAYah.jpg', 'stream_info': {'subtitle': {'language': ''}, 'audio': {'channels': 2, 'codec': 'aac', 'language': 'en'}, 'video': {'width': 1920, 'codec': 'h264', 'height': 720}}, 'label': 'Incredibles 2', 'properties': {'fanart_image': 'http://image.tmdb.org/t/p/w500/mabuNsGJgRuCTuGqjFkWe1xdu19.jpg'}, 'icon': 'http://image.tmdb.org/t/p/w500/x1txcDXkcM65gl7w20PwYSxAYah.jpg'}
    return TorrentPlayer().playTorrentFile(mediaSettings, url, item,AWSHandler,info,mag_start_time, None,listitem)

def get_torrent_link(url):
    
    from urllib import quote_plus
    plugin_p = Addon.getSetting('players_new')
    infohash=re.compile('btih:(.+?)&').findall(url)
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
    elif plugin_p=='7':
      plugin = 'Destiny'
    elif plugin_p=='8':
      plugin = 'Acestream'
    elif plugin_p=='9':
            list_players = ['Quasar', 'Pulsar', 'KmediaTorrent', 'Torrenter', 'YATP', 'XBMCtorrent','KODIPOPCORN','Destiny','Acestream']
        
            selection = xbmcgui.Dialog().select("Torrent Player", list_players)
            if selection == -1:
                return

            plugin = list_players[selection]
  

    filename = (url)
   
    uri_string = quote_plus(filename)
   
    if plugin == "Acestream":
        link = 'http://127.0.0.1:6878/ace/getstream?infohash=%s&hlc=1&transcode=0&transcode_mp3=0&transcode_ac3=0&preferred_audio_language=eng'%infohash[0]

        link='http://127.0.0.1:6878/ace/manifest.m3u8?infohash=%s&format=json&use_api_events=1&use_stop_notifications=1'%infohash[0]
        try:
        
            req_pre=requests.get(link).json()
        except:
            xbmcgui.Dialog().ok('Acestream Error','Opps ACESTREAM wasnt activated, Go a head and activate it...')
            return ''
        size=0
        f_size=0
        speed=0
        peers=0
        unit='b'
        status=''
        start_time=time.time()
   
     
        dp = xbmcgui.DialogProgress()
        dp.create("Starting", "Please wait", '')
        xbmc.sleep(100)
        check=True
        if req_pre['response']==None:
            
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Acestream Error', 'Acestream Failed'.encode('utf-8'))))
            list_players = ['Quasar', 'Pulsar', 'KmediaTorrent', 'Torrenter', 'YATP', 'XBMCtorrent','KODIPOPCORN','Destiny']
        
            selection = xbmcgui.Dialog().select("Torrent Player", list_players)
            if selection == -1:
                return

            plugin = list_players[selection]
            check=False
        if check:
            if 'stat_url' in req_pre['response']:
                stat_link=req_pre['response']['stat_url']
            else:
                xbmc.sleep(300)
                stat_link=req_pre['response']['stat_url']
            req=requests.get(stat_link).json()
            
            while size<(1*1024*1024) or status!='dl':
                if len(req)>0:
                    
                    if 'downloaded' in req['response']:
                        size=req['response']['downloaded']
                        if size>1024:
                            f_size=size/1024
                            unit='Kb'
                        if size>(1024*1024):
                            f_size=size/(1024*1024)
                            unit='Mb'
                        if size>(1024*1024*1024):
                            f_size=size/(1024*1024*1024)
                            unit='Gb'
                    if 'peers' in req['response']:
                        peers=req['response']['peers']
                    if 'speed_down' in req['response']:
                        speed=req['response']['speed_down']
                    if 'status' in req['response']:
                        status=req['response']['status']
                    elapsed_time = time.time() - start_time
                    dp.update(0, ' Please wait '+status+' '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'P-%s %sKb/s'%(str(peers),str(speed)), 'Size '+str(f_size)+unit)
                    
                    xbmc.sleep(1000)
                    req=requests.get(stat_link).json()
                if dp.iscanceled(): 
                    dp.close()
                    break
                
            dp.close()
            link=req_pre['response']['playback_url']
        #link = 'http://127.0.0.1:6878/ace/getstream?infohash=%s&hlc=1&transcode=0&transcode_mp3=0&transcode_ac3=0&preferred_audio_language=eng'%infohash[0]
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
    elif plugin == "XBMCtorrent":
        link = 'plugin://plugin.video.xbmctorrent/play/%s' % uri_string
    
    else:
        link=url
    return link



def get_nan(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Accept': '*/*',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        
        'Cache-Control': 'no-cache',
    }
    
    result=requests.get(url,headers=headers).content
    regex='"VideoIframe".+?src="(.+?)"'
    m=re.compile(regex).findall(result)[0]
    x=requests.get('http://docu.nana10.co.il/'+m,headers=headers).content
    
    regex='UserID=(.+?);'
    userid=re.compile(regex).findall(x)[0]
    regex='"MediaStockVideoItemGroupID","(.+?)"'
    VideoID=re.compile(regex).findall(x)[0]
    url='http://vod.ch10.cloudvideoplatform.com/api/getlink/getflash?userid=%s&showid=%s'%(userid,VideoID)
    y=requests.get(url,headers=headers).json()
    m_lk=y[0]['MediaFile'].split('.')[0]+y[0]['Bitrates']+'.'+y[0]['MediaFile'].split('.')[1]
    f_url=y[0]['ProtocolType']+y[0]['ServerAddress']+y[0]['MediaRoot']+m_lk+y[0]['StreamingType']+y[0]['Params']

    return f_url


def get_nex_ep( time_to_save, original_title,year,season,episode,id,eng_name,show_original_year,heb_name,isr,st,fav,prev_name,url,iconimage,fanart,o_plot):
    global in_next_ep
    if in_next_ep==1:
        return 'ok'
    in_next_ep=1
    try:

        
        da=[]
        stop_window=False
        da.append((original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,st,fav))
        

    
        match_a,a,b,f_subs= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,st,fav,'no','0',table='pages')
        
        
        logging.warning('DONE NEXT EP SEARCHING')
    
    except Exception as e:
        import linecache
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', str(e))).encode('utf-8'))
        logging.warning('ERROR IN NEXTUP:'+str(lineno))
        logging.warning('inline:'+line)
        logging.warning(e)
        logging.warning('BAD NEXT EP SEARCHING')
        
        #match_a,a,b,f_subs= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,st,fav,'no','0',table='pages')
    in_next_ep=0
       
       
       
def get_uptobox(url):

    global tv_mode
    if 'uptostream' not in url:
        x=requests.get(url).content
        regex='<a href="https://uptostream.com/(.+?)"'
        match=re.compile(regex).findall(x)

      
        url=domain_s+'uptostream.com/'+match[0]
    
    

    cookies = {
        #'__cfduid': 'd0dfe3eedd616e0f275edcea08cdb6e521520582950',
        'video': '55srlypu0c08',
    }

    headers = {
        'Host': 'uptostream.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': url,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = requests.get(url, headers=headers, cookies=cookies,timeout=10).content
    regex='var sources = (.+?);'
    match=re.compile(regex).findall(response)
    if len(match)==0:
      regex="sources = JSON.parse\('(.+?)'"
      match=re.compile(regex).findall(response)
    links=json.loads(match[0])
    quality=[]
    links2=[]
    for data in links:
      quality.append(int(data['label'].replace('p','')))
      links2.append(data['src'])
    if local==True or tv_mode:
       return links2[0]
    else:
        return links2[quality.index(max(quality))]
        ret = xbmcgui.Dialog().select("Choose quality", quality)
        if ret!=-1:
            f_link=links2[ret]
        else:
          return 0
        return f_link
def nba_solve(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Accept': '*/*',
    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': url,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
    }
    host=re.compile('//(.+?)/').findall(url)[0]
    

    data = {
      'r': '',
      'd': host
    }
    
    response = requests.post(url.replace('/v/','/api/source/'), headers=headers,  data=data).json()
    return response['data'][len(response['data'])-1]['file']
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
	   try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
	   except: r = ''
    else:
       try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
       except: r = ''
    return r
def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
def sort_function(item):
        """
        transform items quality into a string that's sort-able
        Args:
            item: scraper link
        Returns:
            sortable quality string
        """
        if "quality" in item[1][0]:
            quality = item[1][0]["quality"]
        else:
            quality = item[1][0]["path"]["quality"]

        if "path" in item[1][0]:
            if "debridonly" in item[1][0]["path"]:
                q = "A"
        elif "debridonly" in item[1][0]:
            q = "A"
        else:
            q = "B"

        if q == "A":
            if quality.startswith("4K"):
                quality = "Aa"
            elif quality.startswith("1080"):
                quality = "Ab"
            elif quality.startswith("720"):
                quality = "Ac"
            elif quality.startswith("560"):
                quality = "Ad"
            elif quality == "DVD":
                quality = "Ae"
            elif quality == "HD":
                quality = "Af"
            elif quality.startswith("480"):
                quality = "Ba"
            elif quality.startswith("360"):
                quality = "Bb"
            elif quality.startswith("SD"):
                quality = "Bc"
            else:
                quality = "CZ"

        elif quality.startswith("4K"):
            quality = "HDa"
        elif quality.startswith("1080"):
            quality = "HDb"
        elif quality.startswith("720"):
            quality = "HDc"
        elif quality.startswith("560"):
            quality = "HDd"
        elif quality == "DVD":
            quality = "HDe"
        elif quality == "HD":
            quality = "HDf"
        elif quality.startswith("480"):
            quality = "SDa"
        elif quality.startswith("360"):
            quality = "SDb"
        elif quality.startswith("SD"):
            quality = "SDc"
        else:
            quality = "Z"
        return quality
def GetSublinks(name,url,iconimage,fanart,title,year,imdb):
    List=[]; ListU=[]; c=0
    all_videos = regex_get_all(url, 'sublink:', '#')
    for a in all_videos:
        if 'LISTSOURCE:' in a:
            vurl = regex_from_to(a, 'LISTSOURCE:', '::')
            linename = regex_from_to(a, 'LISTNAME:', '::')
        else:
            vurl = a.replace('sublink:','').replace('#','')
            linename = name
        if len(vurl) > 10:
            c=c+1; List.append(linename); ListU.append(vurl)
  
    if c==1:
            return ListU[0]
            #print 'play 1   Name:' + name + '   url:' + ListU[0] + '     ' + str(c)
            liz=xbmcgui.ListItem(name, iconImage=iconimage,thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=ListU[0],listitem=liz)
            xbmc.Player().play(urlsolver(ListU[0]), liz)
        
    else:
         if len(List)==0:
            import universalscrapers
            title=title.replace('.',' ')
  
            scraper = universalscrapers.scrape_movie_with_dialog
            link, rest = scraper(
                title,
                year,
                imdb,
                timeout=30,
                exclude=None,
                extended=True,
                sort_function=sort_function,
                enable_debrid=allow_debrid,
            )
    
            if type(link) == dict and "path" in link:
                link = link["path"]
            if link is None:
                return False
            url = link["url"]
            if 'http' not in url and 'magnet' not in url:
                url='http:'+url
   
            return url
         else:
             dialog=xbmcgui.Dialog()
             rNo=dialog.select('[COLORorange]Select A Source[/COLOR]', List)
             if rNo>=0:
                 rName=name
                 rURL=str(ListU[rNo])
                 return rURL
                 #print 'Sublinks   Name:' + name + '   url:' + rURL
                 try:
                     xbmc.Player().play(urlsolver(rURL), xbmcgui.ListItem(rName))
                 except:
                     xbmc.Player().play(rURL, xbmcgui.ListItem(rName))
def check_pre(saved_name,all_subs,original_title):
    try:
       release_names=['bluray','hdtv','dvdrip','bdrip','web-dl']
       #array_original=list(saved_name)
       fixed_name=saved_name.lower().strip().replace("%20",".").replace("_",".").replace(" ",".").replace("-",".").replace(".avi","").replace(".mp4","").replace(".mkv","")
       original_title=original_title.lower().strip().replace("%20",".").replace("_",".").replace(" ",".").replace("-",".").replace(".avi","").replace(".mp4","").replace(".mkv","")
       

       
       
       fixed_name=fixed_name.decode('utf-8','ignore').encode("utf-8").replace(original_title,'')
       
       if fixed_name=='':
         return 0
       array_original=fixed_name.split(".")

       array_original=[line.strip().lower() for line in array_original]
       array_original=[(x) for x in array_original if x != '']
       highest=0
       all_subs_new=[]
       for items in all_subs:
           
           #array_subs=list(items)
           fixed_name=items['MovieReleaseName'].lower().strip().replace("%20",".").replace("_",".").replace(" ",".").replace("-",".").replace(".avi","").replace(".mp4","").replace(".mkv","")
           fixed_name=fixed_name.replace(original_title,'')
           array_subs=fixed_name.split(".")
           array_subs=[line.strip().lower() for line in array_subs]
           array_subs=[str(x).lower() for x in array_subs if x != '']
           
     
           for item_2 in release_names:
           
            if item_2 in array_original and item_2 in array_subs:
              array_original.append(item_2)
              array_original.append(item_2)
              array_original.append(item_2)
              array_subs.append(item_2)
              array_subs.append(item_2)
              array_subs.append(item_2)
    
            
           precent=similar(array_original,array_subs)
           
           
           items['pre']=precent
           all_subs_new.append(items)
           
           
           if precent>=highest:
             highest=precent
      
       return all_subs_new
    except Exception as e:
        logging.warning('check_pre error')
        logging.warning(e)
def get_sub_server(imdb,season,episode):
    logging.warning('In 4')
    import xmlrpclib
    langs = []
    langDict = {'Afrikaans': 'afr', 'Albanian': 'alb', 'Arabic': 'ara', 'Armenian': 'arm', 'Basque': 'baq', 'Bengali': 'ben', 'Bosnian': 'bos', 'Breton': 'bre', 'Bulgarian': 'bul', 'Burmese': 'bur', 'Catalan': 'cat', 'Chinese': 'chi', 'Croatian': 'hrv', 'Czech': 'cze', 'Danish': 'dan', 'Dutch': 'dut', 'English': 'eng', 'Esperanto': 'epo', 'Estonian': 'est', 'Finnish': 'fin', 'French': 'fre', 'Galician': 'glg', 'Georgian': 'geo', 'German': 'ger', 'Greek': 'ell', 'Hebrew': 'heb', 'Hindi': 'hin', 'Hungarian': 'hun', 'Icelandic': 'ice', 'Indonesian': 'ind', 'Italian': 'ita', 'Japanese': 'jpn', 'Kazakh': 'kaz', 'Khmer': 'khm', 'Korean': 'kor', 'Latvian': 'lav', 'Lithuanian': 'lit', 'Luxembourgish': 'ltz', 'Macedonian': 'mac', 'Malay': 'may', 'Malayalam': 'mal', 'Manipuri': 'mni', 'Mongolian': 'mon', 'Montenegrin': 'mne', 'Norwegian': 'nor', 'Occitan': 'oci', 'Persian': 'per', 'Polish': 'pol', 'Portuguese': 'por,pob', 'Portuguese(Brazil)': 'pob,por', 'Romanian': 'rum', 'Russian': 'rus', 'Serbian': 'scc', 'Sinhalese': 'sin', 'Slovak': 'slo', 'Slovenian': 'slv', 'Spanish': 'spa', 'Swahili': 'swa', 'Swedish': 'swe', 'Syriac': 'syr', 'Tagalog': 'tgl', 'Tamil': 'tam', 'Telugu': 'tel', 'Thai': 'tha', 'Turkish': 'tur', 'Ukrainian': 'ukr', 'Urdu': 'urd'}
    
    try:
        try: langs = langDict[Addon.getSetting('subtitles.lang.1')].split(',')
        except: langs.append(langDict[Addon.getSetting('subtitles.lang.1')])
    except: pass
    try:
        try: langs = langs + langDict[Addon.getSetting('subtitles.lang.2')].split(',')
        except: langs.append(langDict[Addon.getSetting('subtitles.lang.2')])
    except: pass
            
    server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
    logging.warning('4')
    token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']

    sublanguageid = ','.join(langs) ; imdbid = re.sub('[^0-9]', '', imdb)
    logging.warning('5')
    if not (season == None or episode == None):
        result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'imdbid': imdbid, 'season': season, 'episode': episode}])
        logging.warning(result)
        result=result['data']
    else:
        result = server.SearchSubtitles(token, [{'sublanguageid': sublanguageid, 'imdbid': imdbid}])['data']
    logging.warning('In 5')
    return result
def get_sub_result(imdb,season,episode,name,saved_name):
    logging.warning('In 1')
    #result=get_sub_server(imdb,season,episode)
    da=[]
    da.append((imdb,season,episode))
    logging.warning('Subtitles Search result')
    logging.warning(da)
    if season=='%20':
        season=None
    if episode=='%20':
        episode=None
                
    result=cache.get(get_sub_server,24,imdb,season,episode, table='pages')
    
    logging.warning('In 2')
    f_list=result
    #result=check_pre(saved_name,result,name)
    logging.warning('In 4')
    return result,f_list
            
            
def getsubs( name, imdb, season, episode,saved_name):
            global done1
            if not Addon.getSetting('subtitles') == 'true': return 'ok'

            logging.warning('1')
            

            codePageDict = {'ara': 'cp1256', 'ar': 'cp1256', 'ell': 'cp1253', 'el': 'cp1253', 'heb': 'cp1255', 'he': 'cp1255', 'tur': 'cp1254', 'tr': 'cp1254', 'rus': 'cp1251', 'ru': 'cp1251'}

            quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webrip', 'hdtv']

            logging.warning('2')
            
            logging.warning('3')
            '''
            try: subLang = xbmc.Player().getSubtitles()
            except: subLang = ''
            if subLang == langs[0]: raise Exception()
            '''
            if season=='%20':
                season=None
            if episode=='%20':
                episode=None
            #result,f_list=get_sub_result(imdb,season,episode,name,saved_name)
            
            result,f_list=cache.get(get_sub_result,24,imdb,season,episode,name,saved_name, table='pages')
            logging.warning('check_pre')
            result=check_pre(saved_name,result,name)
           
            
           
            fixed_list=[]
            logging.warning('4')
            if result==0:
                for items in f_list:
                    fixed_list.append((0,items['MovieReleaseName'],items['IDSubtitleFile'],items['SubLanguageID']))
            else:
                for items in result:
                    fixed_list.append((items['pre'],items['MovieReleaseName'],items['IDSubtitleFile'],items['SubLanguageID']))
            
            fixed_list=sorted(fixed_list, key=lambda x: x[0], reverse=True)
            logging.warning('5')
            
            if len(fixed_list)==0:
                xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'No available subs')))
            else:
                logging.warning('Show Window')
                window = MySubs('Subtitles - '+name ,fixed_list,f_list)
                window.doModal()
       
                del window
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
            done1=2
            '''
            filter = []
            result = [i for i in result if i['SubSumCD'] == '1']

            for lang in langs:
                filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in fmt)]
                filter += [i for i in result if i['SubLanguageID'] == lang and any(x in i['MovieReleaseName'].lower() for x in quality)]
                filter += [i for i in result if i['SubLanguageID'] == lang]

            try: lang = xbmc.convertLanguage(filter[0]['SubLanguageID'], xbmc.ISO_639_1)
            except: lang = filter[0]['SubLanguageID']

            content = [filter[0]['IDSubtitleFile'],]
            content = server.DownloadSubtitles(token, content)
            content = base64.b64decode(content['data'][0]['data'])
            content = gzip.GzipFile(fileobj=StringIO.StringIO(content)).read()

            subtitle = xbmc.translatePath('special://temp/')
            subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
            logging.warning(subtitle)
            codepage = codePageDict.get(lang, '')
            if codepage and control.setting('subtitles.utf') == 'true':
                try:
                    content_encoded = codecs.decode(content, codepage)
                    content = codecs.encode(content_encoded, 'utf-8')
                except:
                    pass

            file = control.openFile(subtitle, 'w')
            file.write(str(content))
            file.close()

            xbmc.sleep(1000)
            #xbmc.Player().setSubtitles(subtitle)
            '''
def start_subs(name, imdb, season, episode,saved_name):
    global wait_for_subs,done1
    logging.warning('wait_for_subs:'+str(wait_for_subs))
    if wait_for_subs==1:
        return 'ok'
    
    wait_for_subs=1
    exit_counter=0
    get_sub_now=0
    play_time=1
    if Addon.getSetting("new_window_type2")=='3':
        play_time=int(Addon.getSetting("play_full_time"))+1
    if done1_1==3:
        play_time=1
    while(1):
        
        if done1_1==3:
            
            play_time=1
            
        if xbmc.Player().isPlaying():
           xbmc.sleep(1000)
           vidtime = xbmc.Player().getTime()
                        
                        
           if vidtime > play_time :
                
                logging.warning('Vidtime OK:'+str(vidtime))
                get_sub_now=1
                break
        if exit_counter>600:
                break
        exit_counter+=1
        xbmc.sleep(100)
    wait_for_subs=0
    logging.warning('Vidtime OK:'+str(get_sub_now))
    if get_sub_now>0:
        #getsubs( 'Rampage', 'tt2231461', None, None,'Rampage.2018.720p.BluRay.x264-SPARKS')
       
        if season=='%20':
            season=None
        if episode=='%20':
            episode=None
        
        #xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
        getsubs( name, imdb, season, episode,saved_name)
        xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
        
    return 'OK'
def decode_watch(x):
    regex='<script>var.+?\[(.+?)</script'
    m1=re.compile(regex,re.DOTALL).findall(x.content)[0]
    
    regex='"(.+?)"'
    m2=re.compile(regex,re.DOTALL).findall(m1)
    f_str=''
    reg='atob.+? - (.+?)\)'
    ma=re.compile(reg).findall(m1)[0]
   
    for items in m2:
       
        a=items.decode('base64')
        b=re.sub("\D", "", a)
        
        f_str=f_str+chr(int(b)-int(ma))
    regex='src="(.+?)"'
    m3=re.compile(regex).findall(f_str)[0]
    return m3
def reolve_watchcartoononline(url):
    
    
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
    #'Referer': 'https://www.watchcartoononline.io/101-dalmatians-ii-patchs-london-adventure',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
    }

    x = requests.get(url,headers=headers)
    code=decode_watch(x)
    logging.warning('code:'+code)
    cookies={}
    for key, morsel in x.cookies.items():
            cookies[key] = morsel
   
    headers['Referer']=url
    cookies[ 'bbl']= '2'
    cookies[ 'BB_plg']= 'pm'

    response = requests.get('https://www.watchcartoononline.io'+code, headers=headers,cookies=cookies)
    logging.warning(response.cookies)
    regex='get\("(.+?)"'
    m=re.compile(regex).findall(response.content)[0]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': '*/*',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.watchcartoononline.io'+code,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }
    response = requests.get('https://www.watchcartoononline.io'+m, headers=headers,cookies=cookies).json()
    
    f_link=response['cdn']+'/getvid?evid='+response['enc']

    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
   
    
    ff_link_head=requests.head(f_link,stream=True).headers
    if 'Location' in ff_link_head:
        ff_link=ff_link_head['Location']
    else:
        ff_link=f_link
    #ff_link=f_link#requests.get(f_link,headers=headers,stream=True).url
   
    
    head=urllib.urlencode(headers)
    ff_link=ff_link+"|"+head


    #ok=xbmc.Player().play(ff_link)
    
    return ff_link
def resolve_direct(url,original_title):
    data=json.loads(url)
    str_data=[]
    links=[]
    if len(data)==1:
        return 'magnet:?xt=urn:btih:{0}&dn={1}&tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fp4p.arenabg.ch%3A1337&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337'.format(data[0][5],urllib.quote_plus(original_title))
    for items in data:
        str_data.append('[COLOR yellow]'+str(items[1])+'[/COLOR] | Size: '+str(items[2])+' | S:'+str(items[3])+'/P:'+str(items[4]))
        links.append('magnet:?xt=urn:btih:{0}&dn={1}&tr=udp%3A%2F%2Fglotorrents.pw%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fp4p.arenabg.ch%3A1337&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337'.format(items[5],urllib.quote_plus(original_title)))
    ret = xbmcgui.Dialog().select("Choose", str_data)
    if ret!=-1:
        return links[ret]
    else:
        return 'bad'
def resolve_mvmax(url,name,year):
    
          
    if len(year)>2:
       
        url2='http://api.themoviedb.org/3/search/movie?api_key=1248868d7003f60f2386595db98455ef&query=%s&year=%s&language=he&append_to_response=origin_country&page=1'%(name,year)
    else:
        url2='http://api.themoviedb.org/3/search/movie?api_key=1248868d7003f60f2386595db98455ef&query=%s&language=he&append_to_response=origin_country&page=1'%(name)
    logging.warning(url2)
    y=requests.get(url2).json()
    try:
        id=y['results'][0]['id']
    except:
        id=''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    x=requests.get(url,headers=headers).content
    regex='<div class="container">.+?a href="(.+?)"'
    m=re.compile(regex,re.DOTALL).findall(x)[0]
    
    x=requests.get(m,headers=headers).content
    regex='iframe src="(.+?)"'
    m2=re.compile(regex,re.DOTALL).findall(x)[0]
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': m,
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
    }

    x = requests.get(m2, headers=headers).content
    
    regex="var mp4 = '(.+?)'"
    m=re.compile(regex,re.DOTALL).findall(x)[0]
    return m,str(id)
def play(name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,auto_play=False,windows_play=False,auto_fast=False,nextup=False,f_auto_play=False):
    logging.warning(url)
    if 'moviesmax.net' in url:
        o_url=url
        url,id=resolve_mvmax(url,name,data)
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' and type='%s'"%(name.replace("'"," "),'movie'))

        match = dbcur.fetchone()
        logging.warning('hislink')
       
        if match==None:
          
          dbcur.execute("INSERT INTO AllData Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'"," "),o_url,iconimage,fanart,description.replace("'"," "),data,original_title.replace("'"," "),season,episode,id,eng_name.replace("'"," "),show_original_year,'Direct link',isr,'movie'))
          dbcon.commit()
    if 0:#'tt' in id:
        try:
        
            url22='https://api.themoviedb.org/3/find/%s?api_key=b7cd3340a794e5a2f35e3abb820b497f&language=en&external_source=imdb_id'%id
            x=requests.get(url22).json()
            if 'movie_results' in x:
                id=str(x['movie_results'][0]['id'])
            else:
                id=str(x['tv_results'][0]['id'])
        except:
            pass
    if 'DIRECT link' in url:
        url=resolve_direct(url,original_title)
        if url=='bad':
            return ''
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' and type='%s'"%(name.replace("'"," "),'movie'))

        match = dbcur.fetchone()
        logging.warning('hislink')
       
        if match==None:
          
          dbcur.execute("INSERT INTO AllData Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'"," "),url,iconimage,fanart,description.replace("'"," "),data,original_title.replace("'"," "),season,episode,id,eng_name.replace("'"," "),show_original_year,'Direct link',isr,'movie'))
          dbcon.commit()
    name=name.replace('Cached ','')
    if 'watchcartoononline' in url:
        url=reolve_watchcartoononline(url)
        
    try:
     
     global silent_mode,list_index,playing_text,mag_start_time_new
     regex='sss (.+?) sss'
     if 'sublink' in url:
        logging.warning('solving sublink')
        url=GetSublinks(name,url,iconimage,fanart,clean_name(original_title,1),data,id)
        if not url:
            return '0'
     if name==None:
        name=original_title
     if 'nbareplayhd.com' in url or 'nflhdreplay' in url:
        url=nba_solve(url)
     match=re.compile(regex).findall(description)
     if len(match)>0:
         impmodule = __import__(match[0].replace('.py',''))

         s_type=[]
         pre_url=url
         try:
                            
                dbcur.execute("INSERT INTO historylinks Values ('%s','GOOD','')"%pre_url.encode('base64'))
                dbcon.commit()
         except Exception as e:
            
            pass
         try:
            base=impmodule.source()
         except:
            try:
                base=impmodule.sources()
            except:
                s_type='universal'
         if 'pageURL' in url:
            url=json.loads(url)

         try:
            url=base.resolve(url)
         except:
            pass
     #if 'uptobox' in url:
     #   url=get_uptobox(url)
     url=url.replace('https://www.rapidvideo.com/e/','https://www.rapidvideo.com/v/')
     url=url.replace('oload.download','openload.co')
     start_time=time.time()
     if Addon.getSetting("dp_play")=='true'  and windows_play==False:
     
         dp = xbmcgui.DialogProgress()
         dp.create("Start Playing", "Please wait", '')
         
         elapsed_time = time.time() - start_time
         dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Start Playing', '')
     elapsed_time = time.time() - start_time
     playing_text='Start Playing$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
     o_name=name

     url=url.replace("'",'%27')
     if 'youtube' in url and 'embed/' in url:
        url=url.replace('embed/','watch?v=')
     subtitlesUrl = None
     wall_link=False
     if 'kanapi.' in url:
        url=get_kan(url)
     


     if 'Redirector' in url:
        url=requests.get(url,stream=True).url
     o_plot=description
     
     add_ace=''

     if url=='aceplay' or '/ace/getstream' in url:
        url=cache.get(refresh_ace,24,name, table='cookies')
        add_ace='__aceplay__'
        
     
     

     if Addon.getSetting("dp_play")=='true'  and windows_play==False:
         elapsed_time = time.time() - start_time
         dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Save to DB', '')
     elapsed_time = time.time() - start_time
     playing_text='Save to DB$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
     url=url.replace('vidcloud.co','vcstream.to')
     if url=='latest_movie':
        dbcur.execute("SELECT * FROM lastlinkmovie WHERE o_name='f_name'")

        match = dbcur.fetchone()
        if match!=None:
            f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match
            
         
            if 'http' not  in url and 'plugin' not in url and 'magnet:' not in url:

                url=url.decode('base64')
     elif  url=='latest_tv':
        dbcur.execute("SELECT * FROM lastlinktv WHERE o_name='f_name'")

        match = dbcur.fetchone()
        if match!=None:
           
            f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match
               
                  
            if 'http' not  in url and 'plugin' not in url and 'magnet:' not in url:
             
                url=url.decode('base64')
  
     if 'http' not in url   and 'magnet:' not in url and not os.path.exists(url) and 'ftp:' not in url and  '-sdarot-' not in o_plot and  '-Sdarot-' not in o_plot and 'plugin' not in url:
        
          url='http'+url
     url=url.strip().replace('\n','').replace('\t','').replace('\r','')
    
     if '$$$' in url:
       links=url.split('$$$')
   
       regex='\[\[(.+?)\]\]'
       match=re.compile(regex).findall(str(links))
       if len(match)==0:
         regex='//(.+?)/'
         match=re.compile(regex).findall(str(links))
       ret = xbmcgui.Dialog().select("Choose", match)
       if ret!=-1:
       
         ff_link=links[ret]
         regex='\[\[(.+?)\]\]'
         match2=re.compile(regex).findall(links[ret])
         if len(match2)>0:
           
           ff_link=ff_link.replace(match2[0],'').replace('[','').replace(']','')
           
         url=ff_link.strip()
       else:
         sys.exit()
     regex='\[\[(.+?)\]\]'
     match=re.compile(regex).findall(str(url))
     ff_link=url
     
     
     if len(match)>0:
        for items in match:
           ff_link=ff_link.replace(items,'').replace('[','').replace(']','')
        url=ff_link.strip()
     url=url.replace('[[]]','')
     if '-KIDSSECTION-' not in o_plot:
             if season!=None and season!="%20":
               table_name='lastlinktv'
             else:
               table_name='lastlinkmovie'
             dbcur.execute("SELECT * FROM %s WHERE url='%s'"%(table_name,url))
             
             match = dbcur.fetchone()
             
             if match==None:
                test1=[]
                test1.append((table_name,name,url.encode('base64'),iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id))
             
          
                dbcur.execute("UPDATE %s SET name='%s',url='%s',iconimage='%s',fanart='%s',description='%s',data='%s',season='%s',episode='%s',original_title='%s',saved_name='%s',heb_name='%s',show_original_year='%s',eng_name='%s',isr='%s',prev_name='%s',id='%s' WHERE o_name = 'f_name'"%(table_name,name.replace("'","%27"),url.encode('base64'),iconimage,fanart,description.replace("'","%27"),str(data).replace("'","%27"),season,episode,original_title.replace("'","%27"),saved_name.replace("'","%27"),heb_name.replace("'"," "),show_original_year,eng_name.replace("'","%27").replace("'","%27"),isr,prev_name.replace("'","%27"),id))
                dbcon.commit()

     tmdbKey = '1248868d7003f60f2386595db98455ef'
     silent_mode=True

     year=data
     if len (saved_name)<3:
       saved_name=name

     if Addon.getSetting("dp_play")=='true'  and windows_play==False:
         elapsed_time = time.time() - start_time
         dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Getting  IMDB', '')
     elapsed_time = time.time() - start_time
     playing_text='Getting  IMDB$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
     if season!=None and season!="%20":
       tv_movie='tv'
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,tmdbKey)
     else:
       tv_movie='movie'
       
       url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,tmdbKey)
     if 'tt' not in id:
         try:
            imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
         except:
            imdb_id=" "
     else:
         imdb_id=id
         url3='https://api.themoviedb.org/3/find/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US&external_source=imdb_id'%imdb_id
         xx=requests.get(url3).json()

         if tv_movie=='tv':
            if len(xx['tv_results'])>0:
                id=str(xx['tv_results'][0]['id'])
         else:
            if len(xx['movie_results'])>0:
                id=str(xx['movie_results'][0]['id'])

         
     
     if 1:#try:
         
         

     
         
         video_data={}
         logging.warning('Names')
         logging.warning(saved_name)
         fixed_name=saved_name
         #fixed_name=fix_name_origin(saved_name,original_title)
         logging.warning(fixed_name)
         if season!=None and season!="%20":
           video_data['TVshowtitle']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
           video_data['mediatype']='tvshow'
           
         else:
           video_data['mediatype']='movies'
         video_data['OriginalTitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
         video_data['title']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
         video_data['poster']=fanart
         video_data['fanart']=fanart
         if add_ace!='':
           o_plot=o_plot+add_ace
         video_data['plot']=o_plot+'\n_from_Destiny_'
         video_data['icon']=iconimage
         video_data['year']=data
       
         
         video_data['season']=season
         video_data['episode']=episode
         video_data['imdb']=imdb_id
         video_data['code']=imdb_id
         
         if '-HebDub-' in o_plot or '-KIDSSECTION-' in o_plot or wall_link or 'besttv1.cdn' in url:
             video_data[u'mpaa']=unicode('heb')
      
         
         video_data['imdbnumber']=imdb_id
         
         video_data['imdb_id']=imdb_id
         video_data['IMDBNumber']=imdb_id
         video_data['genre']=imdb_id
         #logging.warning(video_data)
         #sys.exit()
       
 

         
        
         
         
         from run import get_links
         '''
         c_head={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
         if "|" in url:
              import urlparse
              import mimetools
              from StringIO import StringIO
              headers_g2=url.split("|")[1]
              c_head = dict(x.split('=') for x in headers_g2.split('&'))
              
              link2=url.split("|")[0]

         else:
           link2=url
         '''
         if Addon.getSetting("dp_play")=='true'  and windows_play==False:
             elapsed_time = time.time() - start_time
             dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Chacking Links', '')
         elapsed_time = time.time() - start_time
         playing_text='Chacking Links$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

         resolver_supporteds=cache.get(resolver_supported, 72, table='pages')
         url_host_pre=re.compile('//(.+?)/').findall(url)
         url_host='No'
         if len(url_host_pre)>0:
            url_host=url_host_pre[0]
            if '.' in url_host:
              
                url_host=url_host.split('.')[0]
     
         try:
             host = link.split('//')[1].replace('www.','')
             host = host.split('/')[0].lower()
         except:
                host='no'
         rd_domains=cache.get(get_rd_servers, 72, table='pages')
         if rd_domains==None:
            rd_domains=[]
         if 0:#host not in rd_domains and url_host not in resolver_supporteds and 'nitroflare' not in url and 'plugin' not in url and 'magnet:' not in url and 'ftp://' not in link2:
        

             try:
                 try_head = requests.head(link2,headers=c_head)
                 
                 check=(try_head.status_code)
               
             except Exception as e:
               try:
                     try_head = requests.head(link2.replace('https','http'),headers=c_head)
                    
                     check=(try_head.status_code)
                     
               except Exception as e:
                    check='403'
                    logging.warning(e)
               
          
             if 'solaris' in o_plot and '- Direct' in o_name:
              check='403'
            
             if str(check) =='400' or str(check) =='404' or str(check) =='401' or str(check) =='403':
                global all_links_sources
                if 'http://127.0.0.1:6878/ace/getstream' in link2:
                
                    xbmcgui.Dialog().ok('Acestream Error','Opps ACESTREAM wasnt activated, Go a head and activate it...')
                    return 0
  
                xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Renewing temp link'.encode('utf-8'))))
                
                regex='sss (.+?) sss'
                match=re.compile(regex).findall(o_plot)[0]
                check=True
                try:
                    impmodule = __import__(match.replace('.py',''))
                    name1=match.replace('.py','')
                except:
                    check=False
                if check:
                    if len(episode)==1:
                      episode_n="0"+episode
                    else:
                       episode_n=episode
                    if len(season)==1:
                      season_n="0"+season
                    else:
                      season_n=season
                    type=[]
                    type,source_scraper=get_type(impmodule,name1)
                    items=impmodule
                    thread=[]
                    thread.append(Thread(get_links_new,hostDict,imdb_id,name1,type,items,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id,premiered,False))
                    #thread.append(Thread(impmodule.get_links,tv_movie,original_title,heb_name,season_n,episode_n,season,episode,show_original_year,id))
                  
                    thread[0].start()
                    start_time=time.time()
                    

                    if Addon.getSetting("dp_play")=='false'  and windows_play==False:
                        dp = xbmcgui.DialogProgress()
                        dp.create("Renewing links", "Please wait", '')
                    elapsed_time = time.time() - start_time
                    playing_text='Renewing links$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                    while thread[0].is_alive():
                        count_1080=0
                        count_720=0
                        count_480=0
                        count_rest=0
                        f_result=all_links_sources
                        for data in f_result:
                            if 'links' in f_result[data] and len (f_result[data]['links'])>0 :
                         
                                for links_in in f_result[data]['links']:
                            
                                     name2,links,server,res=links_in
                         
                                     if '1080' in res:
                                       count_1080+=1
                                     elif '720' in res:
                                       count_720+=1
                                     elif '480' in res:
                                       count_480+=1
                                     else:
                                       count_rest+=1
                        string_dp="1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]"%(count_1080,count_720,count_480,count_rest)
                        elapsed_time = time.time() - start_time
                        if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                            dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Renewing links', string_dp)
                   
                
                        playing_text='Renewing links$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+string_dp
                       
                        if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                          if  dp.iscanceled() or elapsed_time>30:
                       
                          
                            impmodule.stop_all=1
                            
                            if thread[0].is_alive():
                                 
                                 
                                 thread[0]._Thread__stop()
              
                            break
                    
                    if Addon.getSetting("dp_play")=='false' and windows_play==False:
                        dp.close()
                    all_names=[]
                    all_links=[]
                    all_q=[]
                    all_s=[]
                    all_c=[]
                    if name1 in f_result:
                      for links_in in f_result[name1]['links']:
                        name3,links,server,res=links_in
                        all_names.append(name3)
                        all_links.append(links)
                        all_q.append(res)
                        all_s.append(server)
                        all_c.append(name3+' - [COLOR gold]' +res+'[/COLOR] - '+server)
                    if len(all_links)>0:
                        if Addon.getSetting("new_source_menu")=='true':
                                ret=0
                        else:
                            ret = xbmcgui.Dialog().select("Choose link "+server, all_c)
                        if ret!=-1:
                            url=all_links[ret]
                            
                            fixed_name=fix_name_origin(all_names[ret],original_title)
                            video_data['title']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
                            
                        else:
                          
                            return 0
                    else:
                       url=all_links[0]
                       
                       fixed_name=fix_name_origin(all_names[0],original_title)
                       video_data['title']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'").replace('_',".")
         
         link='OK'
         was_error=0
         elapsed_time = time.time() - start_time
         if Addon.getSetting("dp_play")=='true'  and windows_play==False:
            
            dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Getting direct link', '')
         playing_text='Getting direct link$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
         logging.warning('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
         logging.warning('allow_debrid: '+str(allow_debrid))
         if ('magnet' in url or 'limetorrents' in url or '1337x.st' in url or 'ibit.to' in url or 'torrentdownloads.me' in url or 'torrentquest.com' in url or 'eztv.io' in url) and not allow_debrid :
            link='OK'
            logging.warning('Check magnet Player')
            get_torrent_file(silent_mode=True)
            
         else :
               
               if windows_play and auto_fast:
                  
                  link=get_links(url)
                  
               else:
                   try:
                     
                     
                     link=get_links(url)
                     
                   except Exception as e:
                        import linecache
                        
                        exc_type, exc_obj, tb = sys.exc_info()
                        f = tb.tb_frame
                        lineno = tb.tb_lineno
                        filename = f.f_code.co_filename
                        linecache.checkcache(filename)
                        line = linecache.getline(filename, lineno, f.f_globals)
                        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Bad link try another')))
                        pass
           
         if 1:
             
           
                
             if link=='error' and was_error==0 :
                news='''\
                Error In Play
                
                Source : %s,
                Name:%s
                Episode:%s
                season:%s
                link:%s
                Error:%s
                location:%s
                server:%s
                '''
                sendy(news%(o_name,original_title,season,episode,url,e,str(lineno),o_plot),'error Des','Des')
                playing_text='Error:'+str(e)+'$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                if windows_play==False:
                    window = whats_new('Oops','https://i.gifer.com/ItfD.gif',news%(o_name,original_title,season,episode,url,e,str(lineno),o_plot))
                    window.doModal()
                    del window
                    if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                        dp.close()
                return 0
    
             

             set_runtime=''
             set_total=''
             info = {'title': id, 'season': season, 'episode': episode}
             mag_start_time='0'
             elapsed_time = time.time() - start_time
             if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                
                dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Chacking Last Played location', '')
             playing_text='Chacking Last Played location$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
             if auto_play==False and Addon.getSetting("adv_watched")=='true' and id!='%20':
                 AWSHandler.UpdateDB()
                 res = AWSHandler.CheckWS(info)
            
                 if res:
                    if not res['wflag']:
                      
                        if res['resumetime']!=None:
                          
                            choose_time='Continue from '+time.strftime("%H:%M:%S", time.gmtime(float(res['resumetime'])))
                            #ret = xbmcgui.Dialog().select("Choose", choose_time)
                           
                            window = selection_time('Menu',choose_time)
                            window.doModal()
                            selection = window.get_selection()
                            del window
                           
                            if selection==-1:
                               return 0
                            if selection==0:
                                mag_start_time=res['resumetime']
                                set_runtime=res['resumetime']
                                set_total=res['totaltime']
                                #listItem.setProperty('resumetime', res['resumetime'])
                                #listItem.setProperty('totaltime', res['totaltime'])
                                
                            elif selection==1:
                                mag_start_time='0'
                                set_runtime='0'
                                set_total=res['totaltime']
                                #listItem.setProperty('resumetime', '0')
                                #listItem.setProperty('totaltime', res['totaltime'])
    
             listItem = xbmcgui.ListItem(video_data['title'], path=link) 
             listItem.setInfo(type='Video', infoLabels=video_data)


             listItem.setProperty('IsPlayable', 'true')
             listItem.setProperty('resumetime', set_runtime)
             listItem.setProperty('totaltime', set_total)
            
             if 'magnet' in url or 'limetorrents' in url or '1337x.st' in url  or 'ibit.to' in url or 'torrentdownloads.me' in url or 'torrentquest.com' in url or 'eztv.io' in url:
                
                 if 'limetorrents' in url:
                     elapsed_time = time.time() - start_time
                     if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                        dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Getting magnet link', '')
                     playing_text='Getting magnet link$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                     headers = {
                
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                        }
                     x=requests.get(url,headers=headers).content
                     regex='"magnet:(.+?)"'
                     url='magnet:'+re.compile(regex).findall(x)[0]
                     
                 if '1337x.st' in url :
                    x,cook=cloudflare_request('http://www.1337x.st/',headers=base_header)
                    x=requests.get(url,headers=cook[1],cookies=cook[0]).content
                    regex='"magnet:(.+?)"'
                    url='magnet:'+re.compile(regex).findall(x)[0]
   
                 if  'torrentquest.com' in url or 'eztv.io' in url:
                     elapsed_time = time.time() - start_time
                     if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                        dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Getting magnet link', '')
                     playing_text='Getting magnet link$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                     headers = {
                
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                        }
                     x=requests.get(url,headers=headers).content
                     regex='"magnet:(.+?)"'
                     url='magnet:'+re.compile(regex).findall(x)[0]
                 if 'torrentdownloads.me' in url:
                     elapsed_time = time.time() - start_time
                     if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                        dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Getting magnet link', '')
                     playing_text='Getting magnet link$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                     headers = {
                
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                        }
                     x=requests.get(url,headers=headers).content
                     regex='"magnet:(.+?)"'
                     url='magnet:'+re.compile(regex).findall(x)[0]
                 if 'ibit.to' in url:
                     elapsed_time = time.time() - start_time
                     if Addon.getSetting("dp_play")=='true'   and windows_play==False:
                        dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Getting magnet link', '')
                     playing_text='Getting magnet link$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                     headers = {
                
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                        }
                     x=requests.get(url,headers=headers).content
                     regex="'magnet:(.+?)'"
                     url='magnet:'+re.compile(regex).findall(x)[0].decode("string-escape").replace('X-X','')
                 '''
                 if season!=None and season!="%20" and '-KIDSSECTION-' not in o_plot:
                    elapsed_time = time.time() - start_time
                    if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                        
                        dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Starting search next episode', '')
                    playing_text='Starting search next episode$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                    time_to_save=int(Addon.getSetting("save_time"))

                
                    fav_status='false'
                    thread=[]
                    thread.append(Thread(get_next_ep_links,original_title,year,season,str(int(episode)+1),id,eng_name,show_original_year,heb_name,isr,fav_status))
                    thread[0].start()
                 '''
                 if season!=None and season!="%20":
                    prev_name=original_title
                 elapsed_time = time.time() - start_time
                 if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                     
                     dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Save to DB magnet', '')
                 playing_text='Save to DB Magnet$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                 dbcur.execute("DELETE FROM sources")
                
                 elapsed_time = time.time() - start_time
                 if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                     
                     dp.update(100, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Its in kodi hands now', '')
                 playing_text='Its in kodi hands now$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                 if allow_debrid:
                    logging.warning('LOADING TORRENT')
                    import real_debrid
                    #real_debrid.RealDebrid().auth()
                    rd = real_debrid.RealDebrid()
                    try:
                        if  url.endswith('.torrent') and 'magnet:' not in url:
                            link=rd.addtorrent(url)
                        else:
                            logging.warning('LOADING Single TORRENT')
                            link=rd.singleMagnetToLink(url)
                        listItem = xbmcgui.ListItem(video_data['title'], path=link) 
                        listItem.setInfo(type='Video', infoLabels=video_data)


                        listItem.setProperty('IsPlayable', 'true')
                        listItem.setProperty('resumetime', set_runtime)
                        listItem.setProperty('totaltime', set_total)
                    
                    except Exception as e:
                        logging.warning('RD failed')
                        logging.warning(e)
                        get_torrent_file(silent_mode=True)
                        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'RD Failed trying free'.encode('utf-8')+str(e))))
                        if Addon.getSetting("players_new")!='7':
                            link=get_torrent_link(url)
                            
                            listItem = xbmcgui.ListItem(video_data['title'], path=link) 
                            listItem.setInfo(type='Video', infoLabels=video_data)


                            listItem.setProperty('IsPlayable', 'true')
                            listItem.setProperty('resumetime', set_runtime)
                            listItem.setProperty('totaltime', set_total)
                            if link==url:
                                if Addon.getSetting("subtitles")=='true' and 'tt' in video_data['imdb']:
                                     thread=[]
                                
                                     thread.append(Thread(start_subs,  video_data['OriginalTitle'], video_data['imdb'], video_data['season'], video_data['episode'],video_data['title']))
                                            
                                        
                                     thread[0].start()
                                resolve_magnet(url,listItem,AWSHandler,info,mag_start_time)
                                xbmc.sleep(500)
                                xbmc.executebuiltin('Dialog.Close(okdialog, true)')
                                
                                return 'ok'
                        else:
                            logging.warning('Resolve free magnet')
                            listItem = xbmcgui.ListItem(video_data['title'], path=link) 
                            listItem.setInfo(type='Video', infoLabels=video_data)
                                

                            listItem.setProperty('IsPlayable', 'true')
                            listItem.setProperty('resumetime', set_runtime)
                            listItem.setProperty('totaltime', set_total)
                            if Addon.getSetting("dp_play")=='true':
                                dp.close()
                            logging.warning('Resolve free magnet:'+video_data['imdb'])
                            if Addon.getSetting("subtitles")=='true' and 'tt' in video_data['imdb']:
                                 logging.warning('Start subs torrent')
                                 thread=[]
                            
                                 thread.append(Thread(start_subs,  video_data['OriginalTitle'], video_data['imdb'], video_data['season'], video_data['episode'],video_data['title']))
                                        
                                    
                                 thread[0].start()
                            resolve_magnet(url,listItem,AWSHandler,info,mag_start_time)
                            xbmc.sleep(500)
                            xbmc.executebuiltin('Dialog.Close(okdialog, true)')
                            
                            return 'ok'
                    
                 else:
                    if Addon.getSetting("players_new")!='7':
                        link=get_torrent_link(url)
                        
                        listItem = xbmcgui.ListItem(video_data['title'], path=link) 
                        listItem.setInfo(type='Video', infoLabels=video_data)


                        listItem.setProperty('IsPlayable', 'true')
                        listItem.setProperty('resumetime', set_runtime)
                        listItem.setProperty('totaltime', set_total)
                        if link==url:
                            if Addon.getSetting("subtitles")=='true' and 'tt' in video_data['imdb']:
                                 thread=[]
                            
                                 thread.append(Thread(start_subs,  video_data['OriginalTitle'], video_data['imdb'], video_data['season'], video_data['episode'],video_data['title']))
                                        
                                    
                                 thread[0].start()
                            resolve_magnet(url,listItem,AWSHandler,info,mag_start_time)
                            xbmc.sleep(500)
                            xbmc.executebuiltin('Dialog.Close(okdialog, true)')
                            
                            return 'ok'
                    else:
                        listItem = xbmcgui.ListItem(video_data['title'], path=link) 
                        listItem.setInfo(type='Video', infoLabels=video_data)


                        listItem.setProperty('IsPlayable', 'true')
                        listItem.setProperty('resumetime', set_runtime)
                        listItem.setProperty('totaltime', set_total)
                        if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                            dp.close()
                        logging.warning('MAgnet Resolved')
                        if Addon.getSetting("subtitles")=='true' and 'tt' in video_data['imdb']:
                             thread=[]
                             logging.warning('in MAgnet Resolved')
                             thread.append(Thread(start_subs,  video_data['OriginalTitle'], video_data['imdb'], video_data['season'], video_data['episode'],video_data['title']))
                                    
                                
                             thread[0].start()
                        resolve_magnet(url,listItem,AWSHandler,info,mag_start_time)
                        
                        xbmc.sleep(500)
                        xbmc.executebuiltin('Dialog.Close(okdialog, true)')
                        return 'ok'
             elapsed_time = time.time() - start_time
             if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                 
                 dp.update(100, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'Its in kodi hands now', '')
             playing_text='Its in kodi hands now$$$$'+time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
             logging.warning('PLAYING NOW33')
             logging.warning(windows_play)
             logging.warning(auto_play)
             if windows_play:
                mag_start_time_new=set_runtime
                if nextup:
                    ok=xbmc.Player().play(link,listitem=listItem,windowed=False)
                else:
                    ok=xbmc.Player().play(link,listitem=listItem,windowed=True)
             else:
                 if auto_play==True:
                   logging.warning('PLAYING NOW22')
                   ok=xbmc.Player().play(link,listitem=listItem)
                   if f_auto_play==False:
                    ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
                
                 else:
                   
                   
                   ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
             if Addon.getSetting("subtitles")=='true' and 'tt' in video_data['imdb']:
                 thread=[]
            
                 thread.append(Thread(start_subs,  video_data['OriginalTitle'], video_data['imdb'], video_data['season'], video_data['episode'],video_data['title']))
                        
                    
                 thread[0].start()
             if wall_link and subtitlesUrl:
                x=0
                while not xbmc.Player().isPlaying() and x<1000:
                        xbmc.sleep(10) #wait until video is being played
                        x+=1
                xbmc.sleep(50)
                xbmc.Player().setSubtitles(subtitlesUrl)
             if Addon.getSetting("dp_play")=='true'  and windows_play==False:
                dp.close()
             if Addon.getSetting("play_first")!='true': 
                 playing_text=''
             xbmc.executebuiltin('Dialog.Close(okdialog, true)')

            
             AWSHandler.QueueWS(info)
             
      
             
             xbmc.sleep(1000)
             if 1:#xbmc.Player().isPlaying():
                 if Addon.getSetting("use_trak")=='true' and len(id)>1 and id!='%20':
                    
                     if season!=None and season!="%20":
                      
                       season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
                       
                       i = (post_trakt('/sync/watchlist', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
                     else:
                       
                       i = (post_trakt('/sync/watchlist',data= {"movies": [{"ids": {"tmdb": id}}]}))
        
             try:
            
              if season!=None and season!="%20" and '-KIDSSECTION-' not in o_plot:
                time_to_save=int(Addon.getSetting("save_time"))
                fav_search_f=Addon.getSetting("fav_search_f_tv")
                fav_servers_en=Addon.getSetting("fav_servers_en_tv")
                fav_servers=Addon.getSetting("fav_servers_tv")
              
        
   
                if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 ):
                
                    fav_status='true'
                else:
                    fav_status='false'
    
                thread=[]
        
                thread.append(Thread(get_nex_ep,  time_to_save, original_title,year,season,str(int(episode)+1),id,eng_name,show_original_year,heb_name,isr,False,fav_status,prev_name,url,iconimage,fanart,o_plot))
                    
                
                thread[0].start()
                
                #match_a,a,b,f_subs= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,str(int(episode)+1),id,eng_name,show_original_year,heb_name,isr,False,fav_status,'no','0',table='pages')

                if fav_status=='true':
                    logging.warning('searching next_ep rest')
                    #match_a= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,str(int(episode)+1),id,eng_name,show_original_year,heb_name,isr,False,'rest','no','0', table='pages')
                    thread.append(Thread(get_nex_ep,  time_to_save, original_title,year,season,str(int(episode)+1),id,eng_name,show_original_year,heb_name,isr,False,'rest',prev_name,url,iconimage,fanart,o_plot))
                    thread[1].start()
                logging.warning('Done Prep')
             
             except Exception as e:
               logging.warning('ERRORRRRRRRRRRRRRRR: '+str(e))
               pass
             if season!=None and season!="%20":
                prev_name=original_title

             dbcur.execute("DELETE FROM sources")
             dbcur.execute("INSERT INTO sources Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (prev_name.replace("'","%27"),url,iconimage,fanart,o_plot.replace("'","%27"),year,season,episode,original_title.replace("'","%27"),heb_name.replace("'","%27"),show_original_year,eng_name.replace("'","%27"),isr,id))
             dbcur.execute("DELETE FROM nextup")
  
             if season!=None and season!="%20" and Addon.getSetting('nextup')=='true':

                 dbcur.execute("INSERT INTO nextup Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (prev_name.replace("'","%27"),url,iconimage,fanart,o_plot.replace("'","%27"),year,season,str(int(episode)+1),original_title.replace("'","%27"),heb_name.replace("'","%27"),show_original_year,eng_name.replace("'","%27"),isr,id))
                 logging.warning("INSERT INTO nextup Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (prev_name.replace("'","%27"),url,iconimage,fanart,o_plot.replace("'","%27"),year,season,str(int(episode)+1),original_title.replace("'","%27"),heb_name.replace("'","%27"),show_original_year,eng_name.replace("'","%27"),isr,id))
     
                 
              
                   
                   
             dbcon.commit()
             
  
             logging.warning('DONE ALL')
             xbmc.sleep(1000)
             if 'plugin.video.f4mTester' in url:
                xbmc.executebuiltin('Dialog.Close(all, true)') 
  
             xbmc.executebuiltin('Dialog.Close(okdialog, true)')
             #xbmc.executebuiltin('ReloadSkin()')
             xbmc.executebuiltin("Dialog.Close(busydialog)")
             return 'ok'
    except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)

            logging.warning('ERROR IN Play:'+str(lineno))
            logging.warning('inline:'+line)
            logging.warning('Error:'+str(e))
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'inLine:'+str(lineno))).encode('utf-8'))
            done_nextup=1
            marked_trk=1
    
def last_played_c():
      dbcur.execute("SELECT * FROM lastlinkmovie WHERE o_name='f_name'")

      match = dbcur.fetchone()
      if match!=None:
       f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match
       try:
           if url!=' ':
             if 'http' not  in url:
           
               url=url.decode('base64')
              
             addLink('[COLOR gold]Last Movie Link[/COLOR]','latest_movie',5,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=prev_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year)
       except  Exception as e:
         logging.warning(e)
         pass

      dbcur.execute("SELECT * FROM lastlinktv WHERE o_name='f_name'")

      match = dbcur.fetchone()
      if match!=None:
       
       f_name,name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id=match
       try:
           if url!=' ':
             if 'http' not  in url:
             
               url=url.decode('base64')

             addLink('[COLOR gold]Latest Show Link[/COLOR]'.decode('utf8'), 'latest_tv',5,False,iconimage,fanart,description,data=show_original_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=prev_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year)
       except Exception as e:
         logging.warning(e)
         pass
       addNolink('[COLOR gold]Latest Sources[/COLOR]'.encode('utf8'), url,75,False,iconimage='https://ak6.picdn.net/shutterstock/videos/13058996/thumb/1.jpg',fanart='https://pixelz.cc/wp-content/uploads/2018/06/the-last-of-us-ellie-and-joel-uhd-4k-wallpaper.jpg')
       

def display_results(url):
    all_f_links=json.loads(url)
    text_f=''
    text_nf=''
    for name_f in all_f_links:
       if name_f!='subs' and Addon.getSetting(name_f)=='true':
        count_1080=0
        count_720=0
        count_480=0
        count_rest=0
        
        for name,link,server,quality in all_f_links[name_f]['links']:
           
                
     
                 if '1080' in quality:
                   count_1080+=1
                 elif '720' in quality:
                   count_720+=1
                 elif '480' in quality:
                   count_480+=1
                 else:
                   count_rest+=1
        if len(all_f_links[name_f]['links'])>0:
          string_dp="1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]"%(count_1080,count_720,count_480,count_rest)
          text_f=text_f+name_f+' : '+string_dp+'\n'
        else:
          text_nf=text_nf+name_f+' : [COLOR red]NOT FOUND[/COLOR]'+'\n'
          
    showText('Results', text_f+text_nf)
def get_m3u8():
    addNolink('[COLOR gold][I]To Activate Using Proxy, Add Proxy in the File Name[/I][/COLOR]','www',999,False,iconimage='http://cdn.marketplaceimages.windowsphone.com/v8/images/31edc250-11db-47c3-ad08-712fb1082435?imageType=ws_icon_large',fanart='https://blog.keycdn.com/blog/wp-content/uploads/2014/11/live-streaming-1-768x384.png')
    for i in range(0,5):
      
        nam=Addon.getSetting("M3u8_name-"+str(i))
        list=Addon.getSetting("M3u8_addr-"+str(i))
        if len(nam)>0 and 'http' in list:
          addDir3(nam.decode('utf8').replace('.m3u',''),list,56,'http://cdn.marketplaceimages.windowsphone.com/v8/images/31edc250-11db-47c3-ad08-712fb1082435?imageType=ws_icon_large','https://blog.keycdn.com/blog/wp-content/uploads/2014/11/live-streaming-1-768x384.png',nam.decode('utf8').replace('.m3u8',''))
    onlyfiles = [f for f in listdir(m3_path) if isfile(join(m3_path, f))]
    for file in onlyfiles:
      addDir3(file.decode('utf8').replace('.m3u',''),os.path.join(m3_path, file).encode('utf8'),56,'http://cdn.marketplaceimages.windowsphone.com/v8/images/31edc250-11db-47c3-ad08-712fb1082435?imageType=ws_icon_large','https://blog.keycdn.com/blog/wp-content/uploads/2014/11/live-streaming-1-768x384.png',file.decode('utf8').replace('.m3u8',''))
      
    onlyfiles = [f for f in listdir(m3_dir) if isfile(join(m3_dir, f))]
    for file in onlyfiles:
      addDir3(file.decode('utf8').replace('.m3u',''),os.path.join(m3_dir, file).encode('utf8'),56,'http://cdn.marketplaceimages.windowsphone.com/v8/images/31edc250-11db-47c3-ad08-712fb1082435?imageType=ws_icon_large','https://blog.keycdn.com/blog/wp-content/uploads/2014/11/live-streaming-1-768x384.png',file.decode('utf8').replace('.m3u8',''))
def m3u8_cont(name,url):
    if 'http' in url:

      
      headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        }
      file_data=requests.get(url,headers=headers).content.replace('\n\n','\n').replace('\r','').replace('\t','').split('\n')
    
    else:
        s_file=url.decode('utf8')

        file = open(s_file, 'r') 
        file_data= file.readlines()
        file.close()
    if len(file_data)>200 and Addon.getSetting("group_m3u")=='true':
        all_letters=[]
     
        for r in range(0, len(file_data)/200):
          
              addDir3('Group - '+str(r),url,66,iconimage='http://cdn.marketplaceimages.windowsphone.com/v8/images/31edc250-11db-47c3-ad08-712fb1082435?imageType=ws_icon_large',fanart='https://blog.keycdn.com/blog/wp-content/uploads/2014/11/live-streaming-1-768x384.png',description=str(r))
    else:
   
        for data in file_data:
          
           if '#EXTINF' in data:
               line_d=data.split(",")

               display_name=line_d[1]
               icon=' '
               if len(line_d)>1:
                if 'tvg-logo' in line_d[0]:
                     regex=' tvg-logo=(.+?)"'
                     match=re.compile(regex).findall(line_d[0])
                     if len(match)>0:
                        icon=match[0].replace('"','')
                     else:
                        icon=' '
               
                  
               
           elif 'http' in data:
             url=data
             if 'proxy' in name:
                url='plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;url='+url
             addLink(display_name,url,5,False,iconimage=icon,fanart=icon,description=display_name+'__music__')
    '''
    matches=re.compile('^#EXTINF:(.*?),(.*?)$\n^(.*?)$',re.I+re.M+re.U+re.S).findall(file_data)
    logging.warning('2')
    for params, display_name, url in matches:
        if 'tvg-logo' in params:
         regex=' tvg-logo=(.+?)"'
         match=re.compile(regex).findall(params)
     
         icon=match[0].replace('"','')
        else:
          icon=' '
        if len(icon)==0:
          icon=' ' 
        addLink(display_name,url,5,False,iconimage=icon,fanart=icon,description=display_name)
    '''
def get_group_m3u8(url,plot):
    if 'http' in url:
      headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        }
      file_data=requests.get(url,headers=headers).content.replace('\n\n','\n').replace('\r','').replace('\t','').split('\n')
    else:
        s_file=url.decode('utf8')
       
        file = open(s_file, 'r') 
        file_data= file.readlines()
        file.close()
    start=int(plot)*100
    end=int(plot)*100+100
    counter=0
    for data in file_data:
      
       if '#EXTINF' in data:
           line_d=data.split(",")

           display_name=line_d[1]
           icon=' '
           if len(line_d)>1:
            if 'tvg-logo' in line_d[0]:
                 regex=' tvg-logo=(.+?)"'
                 match=re.compile(regex).findall(line_d[0])
                 if len (match)>0:
                    icon=match[0].replace('"','')
                 else:
                    icon=' '
           
              
           
       elif 'http' in data:
         url=data
         if counter>=start and counter<=end:
           addLink(display_name,url,5,False,iconimage=icon,fanart=icon,description=display_name+'__music__')
         counter+=1
def fix_data(data):
    return data.replace('[',' ').replace(']',' ').replace('	','').replace("\\"," ").replace("\n"," ").replace("\r"," ").replace("\t"," ")

def eng_anim():
    addDir3('Cartoon'.decode('utf8'),'http://api.animetoon.tv/GetAllCartoon',59,'https://png.pngtree.com/element_pic/00/16/12/07584794601cb2b.jpg','https://wallpapersite.com/images/pages/pic_w/2604.jpg','Cartoon'.decode('utf8'))
    addDir3('Anime'.decode('utf8'),'http://api.animetoon.tv/GetAllDubbed',59,'https://i.imgur.com/e4Crf1p.jpg','http://www.tokkoro.com/picsup/2618741-anime-4k-full-desktop-wallpaper.jpg','Anime'.decode('utf8'))
    
    addDir3('[COLOR aqua][I]Search[/I][/COLOR]'.decode('utf8'),'search',62,'https://upload.wikimedia.org/wikipedia/commons/0/0e/Wikipe-tan_sailor_fuku.png','https://worldwithouthorizons.com/wp-content/uploads/Artsy-2016-4K-Anime-Wallpaper-1280x720.jpg','Search'.decode('utf8'))
def download_img(local_filename,cook,url):
    
    if os.path.exists(local_filename):
   
      return 0
    r = requests.get(url,headers=cook[1],cookies=cook[0], stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename
def next_anime(url):
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    x=requests.get(url,headers).json()
    for items in x:
        if items['description']!=None:
          plot=items['description']
        else:
           plot=' '
        video_data={}
        video_data['title']=items['name']
        video_data['poster']='http://www.animetoon.tv/images/series/big/'+items['id']+'.jpg'
        video_data['plot']=plot
        video_data['icon']='http://www.animetoon.tv/images/series/big/'+items['id']+'.jpg'
        if items['released']!=None:
          video_data['year']=items['released'].split('-')[0]
        video_data['rating']=str(int(items['rating']))
        
        addDir3(items['name'],items['id'],60,'http://www.animetoon.tv/images/series/big/'+items['id']+'.jpg','http://www.animetoon.tv/images/series/big/'+items['id']+'.jpg',plot,video_info=video_data)
def anime_ep(url,image):
    headers = {
        'App-Version': '8.0',
        'App-Name': '#Toonmania',
        'App-LandingPage': 'http://www.mobi24.net/toon.html',
        'Host': 'api.animetoon.tv',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'utf-8',
        'User-Agent': 'okhttp/2.3.0'
      
    }
  
    x=requests.get('http://api.animetoon.tv/GetDetails/'+url,headers=headers).json()
    for items in x['episode']:
        video_data={}
        video_data['title']=items['name']
        video_data['poster']=image
        video_data['plot']=items['name']
        video_data['icon']=image
        if items['date']!=None:
          video_data['year']=items['date'].split('-')[0]
        
        addLink(items['name'],items['id'],61,False,image,image,items['name'],video_info=json.dumps(video_data))
def play_anime(name,url,iconimage):

    headers = {
        'App-Version': '8.0',
        'App-Name': '#Toonmania',
        'App-LandingPage': 'http://www.mobi24.net/toon.html',
        'Host': 'api.animetoon.tv',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'utf-8',
        'User-Agent': 'okhttp/2.3.0'
      
    }
  
    x=requests.get('http://api.animetoon.tv/GetVideos/'+url,headers=headers).json()
    
    all_hosts=[]
    all_links=[]
    for items in x:
      regex='//(.+?)/'
      host=re.compile(regex).findall(items[0])[0]
      all_hosts.append(host)
      all_links.append(items[0])
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    ret = xbmcgui.Dialog().select("Choose", all_hosts)
    
    if ret!=-1:
        temp = None
        r = requests.get(all_links[ret],headers=headers)
        logging.warning(all_links[ret])
        html = r.text
        if 'var video_links' in html:
            # Try the generic videozoo \ play44 solve first:
            temp = re.findall(r'''var video_links.*?['"]link['"]\s*?:\s*?['"](.*?)['"]''', html, re.DOTALL)
        else:
            # Try variants:
            temp = re.findall(r'''{\s*?url\s*?:\s*?['"](.*?)['"]''', html, re.DOTALL)
            if not temp:
                temp = re.findall(r'''file\s*?:\s*?['"](.*?)['"]''', html, re.DOTALL)
        
        
        f_link=(temp[0].replace(r'\/', r'/')) # In case there's escaped JS slashes.
        logging.warning(f_link)
        video_data={}
        video_data['title']=name
        video_data['poster']=iconimage
  
        video_data['icon']=iconimage
        
        listItem = xbmcgui.ListItem(video_data['title'], path=f_link) 
        listItem.setInfo(type='Video', infoLabels=video_data)


        listItem.setProperty('IsPlayable', 'true')
 
       
           
        ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
def search_anime():
    search_entered=''
    

    keyboard = xbmc.Keyboard(search_entered, 'Enter search')
    keyboard.doModal()
    if keyboard.isConfirmed():
            search_entered = keyboard.getText()
            headers = {
        
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }

            x=requests.get('http://api.animetoon.tv/GetAllCartoon',headers).json()
            all_r=[]
            for items in x:
                if search_entered.lower() in items['name'].lower():
                    if items['description']!=None:
                      plot=items['description']
                    else:
                       plot=' '
                    all_r.append((items['name'],'http://www.animetoon.tv/images/series/big/'+items['id']+'.jpg',items['id'],plot))
            x=requests.get('http://api.animetoon.tv/GetAllDubbed',headers).json()
            for items in x:
                
                if search_entered.lower() in items['name'].lower():
                    if items['description']!=None:
                      plot=items['description']
                    else:
                       plot=' '
                    all_r.append((items['name'],'http://www.animetoon.tv/images/series/big/'+items['id']+'.jpg',items['id'],plot))
                   
        
            for items in all_r:
                video_data={}
                video_data['title']=items[0]
                video_data['poster']=items[1]
                video_data['plot']=items[3]
                video_data['icon']=items[1]
             
                
                
                addDir3(items[0],items[2],60,items[1],items[1],items[3],video_info=video_data)
def add_remove_trakt(name,original_title,id,season,episode):

    if original_title=='add':
        if name=='tv':
         
           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
           
           i = (post_trakt('/sync/history', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
        else:
          
           i = (post_trakt('/sync/history',data= {"movies": [{"ids": {"tmdb": id}}]}))
    elif original_title=='remove':
        if name=='tv':
         
           season_t, episode_t = int('%01d' % int(season)), int('%01d' % int(episode))
           
           i = (post_trakt('/sync/history/remove', data={"shows": [{"seasons": [{"episodes": [{"number": episode_t}], "number": season_t}], "ids": {"tmdb": id}}]}))
        else:
         
           i = (post_trakt('/sync/history/remove',data= {"movies": [{"ids": {"tmdb": id}}]}))
    if 'added' in i:
       xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Marked as watched'.encode('utf-8'))))
    elif 'deleted' in i:
       xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Watched removed'.encode('utf-8'))))
    else:
      xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Error Somthing went wrong'.encode('utf-8'))))
    xbmc.executebuiltin('Container.Refresh')
def download_file(url):

    from run import get_links
    

    idm_folder=Addon.getSetting("idm_folder")
    if idm_folder.endswith('\\'):
        idm_folder=idm_folder[:-1]
    o_folder=os.path.join(idm_folder,'idman.exe')
    split_folder=idm_folder.split('\\')
    f_folder=''
    c=0
    for item in split_folder:
        if c==0:
          c=1
          f_folder=f_folder+item+'\\'
        else:
          f_folder=f_folder+'"'+item+'"'+'\\'
    
    idm_path=os.path.join(f_folder,'idman.exe')
   
    if not os.path.exists(o_folder):
        xbmcgui.Dialog().ok('Error occurred','IDM Wasnt installed or wrong directory in settings')
        sys.exit()
    f_link=get_links(url)
    if Addon.getSetting("dialog_idm")=='true':
      os.system(idm_path+' /d "%s" /n'%f_link)
    else:
      os.system(idm_path+' /d "%s"'%f_link)

def cartoon():
    url='https://www.watchcartoononline.io/'
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    x=requests.get(url,headers=headers).content
    regex='<ul id="nav">(.+?)</ul>'
    match_pre=re.compile(regex,re.DOTALL).findall(x)

    regex='<li><a href="(.+?)">(.+?)</a></li>'
    match=re.compile(regex).findall(match_pre[0])

    for link,name in match:
       if name!='Home' and name!='Contact':
        addDir3(name.decode('utf8'),link,69,'http://www.cartoon-media.eu/files/library/Cartoon-Movie/2018/JungleBunch_square.jpg?thumb=media-pt','http://digitalspyuk.cdnds.net/16/31/980x490/landscape-1470221630-cartoon-heroes.jpg',name.decode('utf8'))
def cartoon_list(url):
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    x=requests.get(url,headers=headers).content
    regex='<a name="#"></a><p class="sep">#</p><ul>(.+?)</div>'
    match_pre=re.compile(regex,re.DOTALL).findall(x)
    regex='<li><a href="(.+?)" title="(.+?)"'
    match=re.compile(regex).findall(match_pre[0])

    if len(match)==0:
       regex='<li><a href="(.+?)">(.+?)</a></li>'
       match=re.compile(regex).findall(match_pre[0])
       for link,title in match:
         addLink(title,link,5,False,iconimage='http://www.cartoon-media.eu/files/library/Cartoon-Movie/2018/JungleBunch_square.jpg?thumb=media-pt',fanart='http://digitalspyuk.cdnds.net/16/31/980x490/landscape-1470221630-cartoon-heroes.jpg',description=title)
    else:
     for link,name in match:
       if name!='Home' and name!='Contact':
        addDir3(name.decode('utf8'),link,70,'http://www.cartoon-media.eu/files/library/Cartoon-Movie/2018/JungleBunch_square.jpg?thumb=media-pt','http://digitalspyuk.cdnds.net/16/31/980x490/landscape-1470221630-cartoon-heroes.jpg',name.decode('utf8'))
def cartoon_episodes(url):
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    x=requests.get(url,headers=headers).content
    regex='<meta property="og:image" content="(.+?)"'
    image_p=re.compile(regex).findall(x)
    if len(image_p)>0:
       image=image_p[0]
    else:
       image=' '
    regex_pre='<div id="catlist-listview"(.+?)</ul>'
    m_p=re.compile(regex,re.DOTALL).findall(x)[0]
    regex='li><a href="(.+?)" rel="bookmark" title=".+?" class="sonra">(.+?)<'
    m_p=re.compile(regex).findall(x)
    logging.warning(url)
    for link,title in m_p:
  
        addLink(title,link,5,False,iconimage=image,fanart=image,description=title)
def by_actor(url):
    if url=='www':
        url='1'
       
    link='https://api.themoviedb.org/3/person/popular?api_key=1248868d7003f60f2386595db98455ef&language=en-US&page=%s&language=en&sort_by=popularity.desc'%url
    headers = {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
    html=requests.get(link,headers=headers).json()
    for items in html['results']:
        icon=items['profile_path']
        fanart=items['known_for'][0]['backdrop_path']
        if icon==None:
          icon=' '
        else:
          icon=domain_s+'image.tmdb.org/t/p/original/'+icon
        if fanart==None:
          fanart=' '
        else:
          fanart=domain_s+'image.tmdb.org/t/p/original/'+fanart
        addDir3(items['name'],str(items['id']),73,icon,fanart,items['name'])
    addDir3('[COLOR aqua][I]Next Page[/COLOR][/I]',str(int(url)+1),72,' ',' ','[COLOR aqua][I]Next Page[/COLOR][/I]')
    
def actor_m(url):
    choise=['Tv Shows','Movies']
    ret = xbmcgui.Dialog().select("Choose", choise)
    if ret!=-1:
        if ret==0:
         tv_mode='tv'
        else:
         tv_mode='movie'
    else:
      sys.exit()

    if tv_mode=='movie':
       link='https://api.themoviedb.org/3/person/%s?api_key=1248868d7003f60f2386595db98455ef&append_to_response=credits&language=en&sort_by=popularity.desc'%url
    else:
       link='https://api.themoviedb.org/3/person/%s/tv_credits?api_key=1248868d7003f60f2386595db98455ef&append_to_response=credits&language=en&sort_by=popularity.desc'%url
   
    headers = {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
    html=requests.get(link,headers=headers).json()
    if tv_mode=='movie':
        url_g=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
                 
    else:
       url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
    html_g=requests.get(url_g,headers=headers).json()
    if tv_mode=='movie':
      test=html['credits']['cast']
      mode=4
    else:
      test=html['cast']
      mode=7
    for items in test:
        
        icon=items['poster_path']
        fanart=items['backdrop_path']
        if icon==None:
          icon=' '
        else:
          icon=domain_s+'image.tmdb.org/t/p/original/'+icon
        if fanart==None:
          fanart=' '
        else:
          fanart=domain_s+'image.tmdb.org/t/p/original/'+fanart
        plot=items['overview']
        if tv_mode=='movie':
          original_title=items['original_title']
        else:
          original_title=items['original_name']
        id=items['id']
        rating=items['vote_average']
        if tv_mode=='movie':
          title=items['title']
        else:
          title=items['name']
        if 'first_air_date' in items:
           if items['first_air_date']==None:
                    year=' '
           else:
                year=str(items['first_air_date'].split("-")[0])
        else:
            if 'release_date' in items:
              if items['release_date']==None:
                    year=' '
              else:
                year=str(items['release_date'].split("-")[0])
            else:
              year=' '
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
        genere = u' / '.join([genres_list[x] for x in items['genre_ids']])
        #except:genere=''
        
        video_data={}
        video_data['title']=title
        video_data['poster']=fanart
        video_data['plot']=plot
        video_data['icon']=icon
        video_data['genre']=genere
        video_data['rating']=rating
        video_data['year']=year
        addDir3(title,'www',mode,icon,fanart,plot,data=year,original_title=original_title,id=str(id),rating=rating,heb_name=title,show_original_year=year,isr=' ',generes=genere,video_info=video_data)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
def search_actor():
    search_entered=''
    keyboard = xbmc.Keyboard(search_entered, 'Enter search')
    keyboard.doModal()
    if keyboard.isConfirmed():
           search_entered = keyboard.getText()
           link='https://api.themoviedb.org/3/search/person?api_key=1248868d7003f60f2386595db98455ef&language=en&query=%s&page=1&include_adult=false'%search_entered
           headers = {
                                
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1',
                            }
           html=requests.get(link,headers=headers).json()
           for items in html['results']:
                    icon=items['profile_path']
                    fanart=items['known_for'][0]['backdrop_path']
                    if icon==None:
                      icon=' '
                    else:
                      icon=domain_s+'image.tmdb.org/t/p/original/'+icon
                    if fanart==None:
                      fanart=' '
                    else:
                      fanart=domain_s+'image.tmdb.org/t/p/original/'+fanart
                    addDir3(items['name'],str(items['id']),73,icon,fanart,items['name'])
def fix_links(all_f_links,iconimage,image,plot,show_original_year,season,episode):
    all_data=[]
    all_rd_s={}
    all_rd_servers=[]
    try:
        
        count_r=0
        if season!=None and season!="%20":
              tv_movie='tv'
          
              
        else:
              tv_movie='movie'
       
        for name_f in all_f_links:
           
           if name_f!='subs' :
         
            
            for name,link,server,quality in all_f_links[name_f]['links']:
               name=name.decode('utf-8','ignore').encode("utf-8")
               fixed_q=fix_q(quality)
              
              
               se='-%s-'%name_f   
               if all_f_links[name_f]['rd']==True:
                
                
                 
                 if name_f not in all_rd_servers:
                    all_rd_servers.append(name_f)
               pre='0'
              
                
               check=False
            
               
                 
               all_data.append((name_f+name+" - "+server, str(link),iconimage,image,plot,show_original_year,quality,se,fixed_q,name,pre))

     
        
        if 1:
          all_fv=[]
          all_rest=[]
          if Addon.getSetting("fav_servers_en")=='true'  and  tv_movie=='movie':
            all_fv_servers=Addon.getSetting("fav_servers").split(',')
          elif Addon.getSetting("fav_servers_en_tv")=='true'   and  tv_movie=='tv':
          
            all_fv_servers=Addon.getSetting("fav_servers_tv").split(',')
          else:
            all_fv_servers=[]
          for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_data:
            if server.replace('-','') in all_fv_servers:
                all_fv.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
            else:
                all_rest.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
          all_fv=sorted(all_fv, key=lambda x: x[8], reverse=False)
          
          all_rest=sorted(all_rest, key=lambda x: x[8], reverse=False)
          all_data=[]
          for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_fv:
             all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
          for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_rest:
             all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
          
    except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)

            logging.warning('ERROR IN Fixlinks:'+str(lineno))
            logging.warning('inline:'+line)
            logging.warning('Error:'+str(e))
    return all_data
class selection_time(pyxbmct.AddonDialogWindow):
    
    def __init__(self, title='',item=''):
       
        super(selection_time, self).__init__(title)
        self.item=[item,'Play from start']
        self.setGeometry(350, 150,1, 1,pos_x=700, pos_y=200)
        self.list_index=-1

        
        
        self.set_active_controls()
        self.set_navigation()
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
       

    
    def get_selection(self):
        """ get final selection """
        return self.list_index
    def click_list(self):
       
        self.list_index=self.list.getSelectedPosition()
       
        self.close()
    
    def set_active_controls(self):
     
      
        # List
        self.list = pyxbmct.List()
        self.placeControl(self.list, 0,0,  rowspan=2, columnspan=1)
        # Add items to the list
        
       
        self.list.addItems(self.item)
        
        # Connect the list to a function to display which list item is selected.
        self.connect(self.list, self.click_list)
        
       

    def set_navigation(self):
        
        self.setFocus(self.list)

    

    

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=50',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=50',)])
class whats_new(pyxbmct.AddonDialogWindow):
    
    def __init__(self, title='',img=' ',txt=''):
    
        super(whats_new, self).__init__(title)

        self.setGeometry(1000, 600, 4,4)
   
        self.img=img
        self.txt=txt
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    
    def set_info_controls(self):
      
      
     
        self.image = pyxbmct.Image( self.img)
        self.placeControl(self.image, 0, 0, 3, 2)
        self.textbox = pyxbmct.TextBox(font='Med')
        
        self.placeControl(self.textbox, 0,2, 4, 2)
        self.textbox.setText(self.txt)
        # Set auto-scrolling for long TexBox contents
        self.textbox.autoScroll(3000, 3000, 3000)
       
  
    def click_c(self):
       
        self.close()
    def set_active_controls(self):
     
      
       
        
        # Connect key and mouse events for list navigation feedback.
        
     
        
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 3, 0)
        # Connect control to close the window.
        self.connect(self.button, self.click_c)

    def set_navigation(self):
        # Set navigation between controls
        
        self.button.controlDown(self.button)
        self.button.controlUp(self.button)
        # Set initial focus
        self.setFocus(self.button)
       

   

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=500',)])
def download_subs(f_list,index):
    try:
        logging.warning(f_list[index][2])
        logging.warning(f_list[index][3])
        import xmlrpclib,codecs,base64,gzip,StringIO
        codePageDict = {'ara': 'cp1256', 'ar': 'cp1256', 'ell': 'cp1253', 'el': 'cp1253', 'heb': 'cp1255', 'he': 'cp1255', 'tur': 'cp1254', 'tr': 'cp1254', 'rus': 'cp1251', 'ru': 'cp1251'}
        server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc', verbose=0)
        token = server.LogIn('', '', 'en', 'XBMC_Subtitles_v1')['token']
        content = [f_list[index][2],]
        content = server.DownloadSubtitles(token, content)
        content = base64.b64decode(content['data'][0]['data'])
        content = gzip.GzipFile(fileobj=StringIO.StringIO(content)).read()
        try: lang = xbmc.convertLanguage(f_list[index][3], xbmc.ISO_639_1)
        except: lang = f_list[index]['SubLanguageID']

            
        subtitle = xbmc.translatePath('special://temp/')
        subtitle = os.path.join(subtitle, 'TemporarySubs.%s.srt' % lang)
        logging.warning(subtitle)
        codepage = codePageDict.get(lang, '')
        if codepage and Addon.getSetting('subtitles.utf') == 'true':
            try:
                content_encoded = codecs.decode(content, codepage)
                content = codecs.encode(content_encoded, 'utf-8')
            except:
                pass

        file = open(subtitle, 'w')
        file.write(str(content))
        file.close()

        xbmc.sleep(1000)
        xbmc.Player().setSubtitles(subtitle)
        return 'ok'
    except Exception as e:
        logging.warning(e)
        return e
class MySubs(pyxbmct.AddonDialogWindow):
    
    def __init__(self, title='',list=[],f_list=[]):
    
        super(MySubs, self).__init__(title)
        self.list_o=list
        self.title=title
        try:
            self.start_time= xbmc.Player().getTime()
        except:
            self.start_time=0
        wd=int(Addon.getSetting("subs_width"))
        hd=int(Addon.getSetting("subs_hight"))
        px=int(Addon.getSetting("subs_px"))
        py=int(Addon.getSetting("subs_py"))
        self.full_list=f_list
        self.setGeometry(wd, hd, 9, 1,pos_x=px, pos_y=py)
        self.time_c=0
        
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        Thread(target=self.background_task).start()
    def background_task(self):
        global list_index
        max=int(Addon.getSetting("subs_window"))+self.start_time
        self.t=self.start_time
        
        
        self.t2=self.start_time
        once=0
        while(self.t2<max):
          if Addon.getSetting("auto_subtitles")=='true' and xbmc.Player().isPlaying() and once==0:
            once=1
            self.label_info.setLabel('Downloading')
            result=download_subs(self.list_o,0)
            if result=='ok':
                self.label_info.setLabel('Ready')
            else:
                self.label_info.setLabel('Error: '+str(result))
          self.label.setLabel(str(int(max-self.t2)))
          self.time_c=self.t2
          
         
          try:
            self.t2= xbmc.Player().getTime()
          except:
            self.t2=self.t
          self.t+=1
          xbmc.sleep(1000)
        list_index=999
        self.close()
    def set_info_controls(self):
      
      
         # Label
        self.label = pyxbmct.Label(str(int(self.time_c)))
        self.placeControl(self.label,  4, 0, 3, 1)
        
        self.label_info = pyxbmct.Label('Waiting for your selection')
        self.placeControl(self.label_info,  0, 0, 1, 1)
         
    def click_list(self):
        global list_index
        list_index=self.list.getSelectedPosition()
        self.t=self.start_time
        self.label_info.setLabel('Downloading')
        result=download_subs(self.list_o,list_index)
        if result=='ok':
                self.label_info.setLabel('Ready')
        else:
            self.label_info.setLabel('Error: '+str(result))
        self.t=self.start_time
       
        #self.close()
    def click_c(self):
        global list_index
        
        list_index=888
        current_list_item=''
        self.close()
    def set_active_controls(self):
     
      
        # List
        
        self.list = pyxbmct.List()
        self.placeControl(self.list, 1, 0, 7, 1)
        # Add items to the list
        items = self.list_o
        n_items=[]
        logging.warning('len(n_items)')
        logging.warning(len(n_items))
        for pre,it,index_in,lan in items:
          logging.warning(pre)
          if pre==0:
             n_items.append('[COLOR lightgreen] [%s] [/COLOR]'%lan+it)
          else:
            n_items.append('[COLOR yellow]'+str(pre)+'%[/COLOR]'+'[COLOR lightgreen] [%s] [/COLOR]'%lan+it)
          
        self.list.addItems(n_items)
        # Connect the list to a function to display which list item is selected.
        self.connect(self.list, self.click_list)
        
        # Connect key and mouse events for list navigation feedback.
        
     
        
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 8, 0)
        # Connect control to close the window.
        self.connect(self.button, self.click_c)

    def set_navigation(self):
        # Set navigation between controls
        
        self.list.controlDown(self.button)
        self.button.controlUp(self.list)
        # Set initial focus
        self.setFocus(self.list)

    def slider_update(self):
        # Update slider value label when the slider nib moves
        try:
            if self.getFocus() == self.slider:
                self.slider_value.setLabel('{:.1F}'.format(self.slider.getPercent()))
        except (RuntimeError, SystemError):
            pass

    def radio_update(self):
        # Update radiobutton caption on toggle
        if self.radiobutton.isSelected():
            self.radiobutton.setLabel('On')
        else:
            self.radiobutton.setLabel('Off')

    def list_update(self):
        # Update list_item label when navigating through the list.
        try:
            if self.getFocus() == self.list:
                self.list_item_label.setLabel(self.list.getListItem(self.list.getSelectedPosition()).getLabel())
            else:
                self.list_item_label.setLabel('')
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
       
        
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=100',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=100',)])
class MyAddon(pyxbmct.AddonDialogWindow):
    
    def __init__(self, title='',list=[],time_c=10,img=' ',txt=''):
    
        super(MyAddon, self).__init__(title)
        self.list_o=list
        self.title=title
        wd=int(Addon.getSetting("width"))
        hd=int(Addon.getSetting("hight"))
        px=int(Addon.getSetting("px"))
        py=int(Addon.getSetting("py"))
        
        self.setGeometry(wd, hd, 9, 1,pos_x=px, pos_y=py)
        self.time_c=time_c
        self.img=img
        self.txt=txt
        self.set_info_controls()
        self.set_active_controls()
        self.set_navigation()
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        Thread(target=self.background_task).start()
    def background_task(self):
        global list_index
        t=int(self.time_c)*10
        
        while(t>30):
          xbmc.sleep(100)
          self.label.setLabel(str(int(t)/10))
          
          windowsid=xbmcgui.getCurrentWindowDialogId()
        
          if windowsid==10153 or windowsid==10101:
            break
          if 'Next episode' in self.title:
           try:
             t=(xbmc.Player().getTotalTime()-xbmc.Player().getTime())*10
           except:
             t=0
             pass
          else:
            t-=1
        list_index=999
        self.close()
    def set_info_controls(self):
      
      
         # Label
        self.label = pyxbmct.Label(str(int(self.time_c)))
        self.placeControl(self.label,  4, 0, 3, 1)
        self.image = pyxbmct.Image( self.img)
        self.placeControl(self.image, 0, 0, 2, 1)
        self.textbox = pyxbmct.TextBox()
        
        self.placeControl(self.textbox, 2,0, 2, 1)
        self.textbox.setText(self.txt)
        # Set auto-scrolling for long TexBox contents
        self.textbox.autoScroll(1000, 1000, 1000)
       
    def click_list(self):
        global list_index
        list_index=self.list.getSelectedPosition()
        self.close()
    def click_c(self):
        global list_index
        list_index=888
        current_list_item=''
        self.close()
    def set_active_controls(self):
     
      
        # List
        self.list = pyxbmct.List()
        self.placeControl(self.list, 4, 0, 4, 1)
        # Add items to the list
        items = self.list_o
        n_items=[]
        a_links=[]
        for it in items:
         
          n_items.append(it.split('$$$$$$$')[0])
          a_links.append(it.split('$$$$$$$')[1])
        self.list.addItems(n_items)
        # Connect the list to a function to display which list item is selected.
        self.connect(self.list, self.click_list)
        
        # Connect key and mouse events for list navigation feedback.
        
     
        
        self.button = pyxbmct.Button('Close')
        self.placeControl(self.button, 8, 0)
        # Connect control to close the window.
        self.connect(self.button, self.click_c)

    def set_navigation(self):
        # Set navigation between controls
        
        self.list.controlDown(self.button)
        self.button.controlUp(self.list)
        # Set initial focus
        self.setFocus(self.list)

    def slider_update(self):
        # Update slider value label when the slider nib moves
        try:
            if self.getFocus() == self.slider:
                self.slider_value.setLabel('{:.1F}'.format(self.slider.getPercent()))
        except (RuntimeError, SystemError):
            pass

    def radio_update(self):
        # Update radiobutton caption on toggle
        if self.radiobutton.isSelected():
            self.radiobutton.setLabel('On')
        else:
            self.radiobutton.setLabel('Off')

    def list_update(self):
        # Update list_item label when navigating through the list.
        try:
            if self.getFocus() == self.list:
                self.list_item_label.setLabel(self.list.getListItem(self.list.getSelectedPosition()).getLabel())
            else:
                self.list_item_label.setLabel('')
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=500',)])
def nextup():

    try:
        global list_index,done_nextup,all_s_in,done1
        list=[]

        time_to_save=int(Addon.getSetting("save_time"))
        
        dbcur.execute("SELECT * FROM nextup")

        match = dbcur.fetchone()
  
        fast_link=' '
        if match!=None:
            name,url,icon,image,plot,year,season,episode,original_title,heb_name,show_original_year,eng_name,isr,id=match
            name=str(name)
    
            url=str(url)
            icon=str(icon)
            image=str(image)
            plot=str(plot).replace('%27',"'")
            year=str(year)
            season=str(season)
            episode=str(episode)
            original_title=str(original_title)

            heb_name=str(heb_name.decode('utf-8')).replace('%27',"'")
            show_original_year=str(show_original_year)
            eng_name=str(eng_name).replace('%27',"'")
            isr=str(isr)
            id=str(id)
            
            
            iconimage=icon
            fanart=image
            data=year
            description=plot.replace('-Episode ','').replace('-NEXTUP-','').encode('utf8')
            fav_search_f=Addon.getSetting("fav_search_f_tv")
            fav_servers_en=Addon.getSetting("fav_servers_en_tv")
            fav_servers=Addon.getSetting("fav_servers_tv")
          
            
       
            if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 ):
            
                fav_status='true'
            else:
                fav_status='false'
            if debug_mode==True:
                
                logging.warning('nextup sources')
            f_subs=[]
            match_a,all_links_fp,all_pre,f_subs= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,str(int(episode)),id,eng_name,show_original_year,heb_name,isr,False,fav_status,'no','0', table='pages')
            all_s_in=( {},100 ,'',4,'')
            all_data=fix_links(match_a,iconimage,fanart,description,show_original_year,season,episode)
            
            from tmdb import get_episode_data
            name_n,plot_n,image_n=get_episode_data(id,season,str(int(episode)))
            for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_data:
              
                list.append('[COLOR gold]'+q+'[/COLOR][COLOR lightblue]'+server+'[/COLOR]-'+name+'$$$$$$$'+link)
            fast_link=list[0].split('$$$$$$$')[1]
            try:
                time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
            except:
                time_left=30
                pass
           
            window = MyAddon('Next episode - '+name_n ,list,time_left,image_n,plot_n)
            window.doModal()
       
            del window
            play_now=False
        
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": { "playlistid": 0 }, "id": 1}')
            if list_index!=999 and list_index!=888:
                xbmc.Player().stop()
                fast_link=list[list_index].split('$$$$$$$')[1]
                #xbmc.executebuiltin(('XBMC.PlayMedia("plugin://plugin.video.destiny/?data=%s&dates=EMPTY&description=%s&eng_name=%s&episode=%s&fanart=%s&heb_name=%s&iconimage=%s&id=%s&isr=' '&mode2=4&name=%s&original_title=%s&season=%s&show_original_year=%s&tmdbid=EMPTY&url=%s&fast_link=%s",return)'%(data,urllib.quote_plus(description),eng_name,str(int(episode)+1),urllib.quote_plus(fanart),heb_name,urllib.quote_plus(iconimage),id,name,original_title,season,show_original_year,urllib.quote_plus(fast_link),urllib.quote_plus(fast_link))).replace('EMPTY','%20'))

            if Addon.getSetting('play_nextup_wait')=='false' and list_index==999:
                return '0'
            if list_index==888: 
                return '0'
            if fast_link!=' ':
                n_fast_link=fast_link
                if Addon.getSetting("fast_play2_tv")=='true':
                    
                    if list_index==999:
                        n_fast_link='999'
                    else:
                       n_fast_link=fast_link
                    
                
    
                #
                
                
                #xbmc.executebuiltin(('XBMC.PlayMedia("plugin://plugin.video.destiny/?data=%s&dates=EMPTY&description=%s&eng_name=%s&episode=%s&fanart=%s&heb_name=%s&iconimage=%s&id=%s&isr=' '&mode2=4&name=%s&original_title=%s&season=%s&show_original_year=%s&tmdbid=EMPTY&url=%s&fast_link=%s",return)'%(data,urllib.quote_plus(description),eng_name,str(int(episode)+1),urllib.quote_plus(fanart),heb_name,urllib.quote_plus(iconimage),id,name,original_title,season,show_original_year,urllib.quote_plus(url),urllib.quote_plus(fast_link))).replace('EMPTY','%20'))
                #if Addon.getSetting("fast_play2_tv")=='true':
                    
                result = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": { "playlistid": 0 }, "id": 1}')
                xbmc.Player().stop()
                done_nextup=0
                #
                KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
                if KODIV >= 17:
                    logging.warning('PLAY NEXTUP')
                    xbmc.executebuiltin(('Container.update("plugin://plugin.video.destiny/?data=%s&dates=EMPTY&description=%s-NEXTUP-&eng_name=%s&episode=%s&fanart=%s&heb_name=%s&iconimage=%s&id=%s&isr=%s' '&mode2=4&name=%s&original_title=%s&season=%s&show_original_year=%s&tmdbid=EMPTY&url=%s&fast_link=%s&fav_status=%s",return)'%(data,urllib.quote_plus(description),eng_name,str(int(episode)),urllib.quote_plus(fanart),heb_name,urllib.quote_plus(iconimage),id,isr,name,original_title,season,show_original_year,urllib.quote_plus(n_fast_link),urllib.quote_plus(n_fast_link),fav_status)).replace('EMPTY','%20'))
                    
                    #play(name,fast_link,iconimage,image,description,data,season,episode,original_title,name,heb_name,show_original_year,eng_name,isr,original_title,id,windows_play=True,auto_fast=False,nextup=True)
                    
                    logging.warning('PLAY NEXTUP FULLSCREEN')
                    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                    return '0'
                else:
                    xbmc.executebuiltin(('ActivateWindow(10025,"plugin://plugin.video.destiny/?data=%s&dates=EMPTY&description=%s-NEXTUP-&eng_name=%s&episode=%s&fanart=%s&heb_name=%s&iconimage=%s&id=%s&isr=%s' '&mode2=4&name=%s&original_title=%s&season=%s&show_original_year=%s&tmdbid=EMPTY&url=%s&fast_link=%s&fav_status=%s",return)'%(data,urllib.quote_plus(description),eng_name,str(int(episode)),urllib.quote_plus(fanart),heb_name,urllib.quote_plus(iconimage),id,isr,name,original_title,season,show_original_year,urllib.quote_plus(n_fast_link),urllib.quote_plus(n_fast_link),fav_status)).replace('EMPTY','%20'))
                mode2=1999
                    #sys.exit()
                '''
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playlist.clear()
                for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_data:
                    listItem=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=image)
                    listItem.setInfo('video', {'Title': name, 'Genre': 'Kids'})
                    link2=(('plugin://plugin.video.destiny/?data=%s&dates=EMPTY&description=%s&eng_name=%s&episode=%s&fanart=%s&heb_name=%s&iconimage=%s&id=%s&isr=' '&mode2=4&name=%s&original_title=%s&season=%s&show_original_year=%s&tmdbid=EMPTY&url=%s&fast_link=%s'%(data,urllib.quote_plus(description),eng_name,str(int(episode)+1),urllib.quote_plus(fanart),heb_name,urllib.quote_plus(iconimage),id,name,original_title,season,show_original_year,urllib.quote_plus(link),urllib.quote_plus(link))).replace('EMPTY','%20'))
                    logging.warning(link2)
                    playlist.add(url=link2, listitem=listItem)
                play_now=True
                '''
    except Exception as e:
            import linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)

            logging.warning('ERROR IN NEXTUP IN:'+str(lineno))
            logging.warning('inline:'+line)
            logging.warning('Error:'+str(e))
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Error', 'inLine:'+str(lineno))).encode('utf-8'))
            done_nextup=1
            marked_trk=1
            
    return 0
 
def prepare_library(dbcon_kodi,dbcur_kodi):
   

    dbcur_kodi.execute("SELECT MAX(idFile) FROM movie")

    match = dbcur_kodi.fetchone()
    try:
        index=match[0]+1
    except:
        index=0
    
    dbcur_kodi.execute("SELECT MAX(idFile) FROM files")

    match = dbcur_kodi.fetchone()
    try:
        file_index=match[0]+1
    except:
        file_index=0

    dbcur_kodi.execute("SELECT MAX(art_id) FROM art")

    match = dbcur_kodi.fetchone()

    try:
        art_index=match[0]+1
    except:
        art_index=0
    dbcur_kodi.execute("SELECT * FROM genre")

    match = dbcur_kodi.fetchall()
    all_gen={}
    for g_id,nm in match:

        all_gen[nm]=g_id
    dbcur_kodi.execute("SELECT * FROM path")
    found=0
    match = dbcur_kodi.fetchall()
    for items in match:
        if items[0]==99879:
            found=1
    if found==0:
        dbcur_kodi.execute("INSERT INTO path Values ('99879', 'plugin://plugin.video.destiny/', '', '', '', '','', '', '', '', '', '');")
        dbcon_kodi.commit()

    return index,file_index,art_index,all_gen
def add_item_to_lib(name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,isr,genere,trailer,fav_status,index,file_index,art_index,dbcon_kodi,dbcur_kodi,all_gen):

    
    icon_db='<thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb><thumb aspect="poster" preview="img_poster">img_poster</thumb>'
    icon_db=icon_db.replace('img_poster',icon)
    fanart_db='<fanart><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb><thumb preview="img_poster">img_poster</thumb></fanart>'
    fanart_db=fanart_db.replace('img_poster',fan)
    link=get_rest_data(name,url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,fav_status=fav_status).replace(' ','%20')
    dbcur_kodi.execute("INSERT INTO movie Values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" %  (index,file_index,name.replace("'","''"),plot.replace("'","''"),'','',None,'99879','',None,icon_db,'99879','','','','0',genere,'',original_name.replace("'","''"),'','',trailer,fanart_db,'',url,'4',None,None,year))
    dbcur_kodi.execute("INSERT INTO files Values ('%s', '%s', '%s', '%s', '%s', '%s');" %  (file_index,'99879',link.replace("'","''"),'','',''))
    dbcur_kodi.execute("INSERT INTO art Values ('%s', '%s', '%s', '%s', '%s');" %  (art_index,index,'movie','fanart',fan))
    dbcur_kodi.execute("INSERT INTO art Values ('%s', '%s', '%s', '%s', '%s');" %  (art_index+1,index,'movie','poster',icon))
    for items in genere.split('/'):
        if items.strip() in all_gen:
            dbcur_kodi.execute("INSERT INTO genre_link Values ('%s', '%s', '%s');" %  (all_gen[items.strip()],index,'movie'))
    '''
    index+=1
    file_index+=1
    art_index+=2
    '''
def remove_color(name):
  
    regex='COLOR (.+?)\]'
    m=re.compile(regex).findall(name)
    if len(m)>0:
        for items in m:
            name=name.replace('[COLOR %s]'%items,'').replace('[/COLOR]','')
    
    regex='\[(.+?)\]'
    m=re.compile(regex).findall(name)
    if len(m)>0:
    
        name=name.replace(m[0],'[COLOR green]'+m[0]+'[/COLOR]')
        name=name.replace('[[','[').replace(']]',']')
    
    regex='\{(.+?)\}'
    m=re.compile(regex).findall(name)
    if len(m)>0:
        name=name.replace('{'+m[0]+'}','')
        name='{'+m[0]+'}'+name
        name=name.replace(m[0],'[COLOR blue]'+m[0]+'[/COLOR]')
    name_s=name.split('-')
  
    m=[]
    found=0
    sv_items2=''
    for items2 in name_s:
      
        try:
            
            x=float(items2.replace('GB','').split('{')[0])
            m.append(items2.split('{')[0])
            found=1
            
        except:
            pass
        if len(items2)>1:
            sv_items2=items2
    if found==0:
       
        name=name.replace(sv_items2,'[COLOR gold]'+sv_items2+'[/COLOR]')
  
    if len(m)>0:
        name=name.replace(m[0],'')
        name=m[0]+'-'+name
        name=name.replace(m[0],'[COLOR coral]'+m[0]+'[/COLOR]')
  
    #name=name.replace('GB','[COLOR gold]GB[/COLOR]')

    return name
def new_show_sources(m,data,description,eng_name,episode,image,heb_name,iconimage,id,prev_name,original_title,season,show_original_year,n,rest_data,n_magnet,r_results,len_all_torrent_s,next_ep,count_heb,only_torrent,isr):
    global stop_try_play,done1
    original_data=[]
    original_data.append((m,data,description,eng_name,episode,image,heb_name,iconimage,id,prev_name,original_title,season,show_original_year,n,rest_data,n_magnet,r_results,len_all_torrent_s,next_ep))
    
    global list_index

    list=[]
    
   
    stop_try_play=False

    menu=[]
    all_links=[]
    all_s_names=[]
    all_plot=[]
    all_server_name=[]
    real_index=0
   
   
    if len(r_results)>0:
        list.append('[COLOR khaki][I]►►► Rd Sources Only ◄◄◄[/I][/COLOR]'+'$$$$$$$'+r_results[0])
        menu.append(['[COLOR khaki][I]►►► Rd Sources Only ◄◄◄[/I][/COLOR]', '','','','','',r_results[0],''])
        all_links.append(r_results[0])
        all_s_names.append('Rd Sources Only')
        all_plot.append('Rd Sources Only')
        all_server_name.append('0')
        real_index+=1
    if len(next_ep)>0:
        list.append('[COLOR khaki][I]►►► Open next episode ◄◄◄[/I][/COLOR]'+'$$$$$$$'+next_ep[0])
        menu.append(['[COLOR khaki][I]►►► Open next episode ◄◄◄[/I][/COLOR]', '','','','','',next_ep[0],''])
        all_links.append(next_ep[0])
        all_s_names.append('Open next episode')
        all_plot.append('Open next episode')
        all_server_name.append('0')
        real_index+=1
    if len(n_magnet)>0:
        list.append('[COLOR khaki][I]►►►(%s) Magnet links ◄◄◄[/I][/COLOR]'%len_all_torrent_s+'$$$$$$$'+n_magnet[0])
        menu.append(['[COLOR khaki][I]►►►(%s) Magnet links ◄◄◄[/I][/COLOR]'%len_all_torrent_s, '','','','','',n_magnet[0],''])
        all_links.append(n_magnet[0])
        all_s_names.append('Magnet links')
        all_plot.append('Magnet links')
        all_server_name.append('0')
        real_index+=1
    if len(n)>0:
        list.append('[COLOR lightgreen][I]►►► Rest of results ◄◄◄[/I][/COLOR]'+'$$$$$$$'+n[0])
        menu.append(['[COLOR lightgreen][I]►►► Rest of results ◄◄◄[/I][/COLOR]', '','','','','',n[0],''])
        
        all_links.append(n[0])
        all_s_names.append('Rest of results ')
        all_plot.append('Rest of results ')
        all_server_name.append('0')
        real_index+=1
    if  Addon.getSetting("auto_enable_new")== 'true' and Addon.getSetting("new_window_type2")=='3':
        list.append('[COLOR khaki][I]►►►Auto Play◄◄◄[/I][/COLOR]')
        menu.append(['[COLOR khaki][I]►►►Auto Play ◄◄◄[/I][/COLOR]', '','','','','','',''])
        all_links.append('www')
        all_s_names.append('Auto Play')
        all_plot.append('-Auto Play-')
        all_server_name.append('0')
        real_index+=1
    if allow_debrid:
        rd_domains=cache.get(get_rd_servers, 72, table='pages')
    else:
        rd_domains=[]
    list_of_play=[]
    for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre,supplier,size in m:
        if size=='0 GB' or '0.0 GB' in size:
            size=' '
        o_server=server
        
        name=remove_color(name)
        all_plot.append(plot)
        all_server_name.append(server)
        pre_n=''
        if pre>0:
            pre_n='[COLOR gold]'+str(pre)+'%[/COLOR]'
            
        regex='\[COLOR green\](.+?)\[/COLOR\]'
        m=re.compile(regex).findall(name)
        
        server=''
        supplay=supplier
        
        if '-' in supplay:
            supplay=supplay.split('-')[0]
       
       
        if len(m)>0:
           
            server=m[0]
            name=name.replace('[COLOR green]%s[/COLOR]'%m[0],'')
            server='[COLOR plum]'+server+'[/COLOR]'
        regex='\[COLOR gold\](.+?)\[/COLOR\]'
        m=re.compile(regex).findall(name)
        if len(m)>0:
      
            
            name=name.replace('[COLOR gold]%s[/COLOR]'%m[0],'')
        regex='\[COLOR coral\](.+?)\[/COLOR\]'
        if '1337' in name:
           
            regex=' - (.+?) GB'
                  
       
            m=re.compile(regex).findall(name)
             
            if len(m)>0:
                size=m[0].replace('--','')+' GB'
                name=name.replace(' - %s GB'%m[0],'')
        else:
            m=re.compile(regex).findall(name)
            if len(m)>0:
                size=m[0]
                name=name.replace('[COLOR coral]%s[/COLOR]'%m[0],'')
        regex='\{(.+?)\}'
        m=re.compile(regex).findall(name)
        if len(m)>0:
            name=name.replace('{%s}'%m[0],'')
           
            supplay=m[0]
        
        if '2160' in q or '4k' in q.lower():
            q='2160'
        elif '1080' in q:
            q='1080'
        elif '720' in q:
            q='720'
        elif '480' in q:
            q='480'
        elif '360' in q:
            q='360'
        else:
            q='unk'
        rd=False
        try:
            host = link.split('//')[1].replace('www.','')
            host = host.split('/')[0].lower()
        except:
            host='no'
        if host in rd_domains or (('torrent' in server.lower() or 'torrent' in name.lower() or 'magnet' in name.lower() or 'magnet' in server.lower()) and allow_debrid):
            rd=True
        add_rd=''

        if allow_debrid and 'magnet' in name:
            rd=True
        if rd:
            add_rd='[COLOR gold]RD- [/COLOR]'
        add_c=''
        if 'Cached ' in name:
            add_c='[COLOR gold] Cached [/COLOR]'
        supplay=supplay.replace('P-0/','')
        txt=add_c+'[COLOR deepskyblue]'+add_rd+name.replace('Cached ','').replace('-',' ').replace('%20',' ').strip().decode('utf-8','ignore')+'[/COLOR]\nServer: '+server+' Subs: '+str(pre_n)+'  Quality:[COLOR gold] ◄'+q+'► [/COLOR]Provider: [COLOR lightblue]'+supplay.decode('utf-8','ignore')+'[/COLOR] Size:[COLOR coral]'+size+'[/COLOR]$$$$$$$'+link.decode('utf-8','ignore')
        menu.append([name.replace('-',' ').replace('%20',' ').strip(), server,str(pre_n),q,supplay,size,link,rd])
        list_of_play.append((name,link,icon,image,plot,year,season,episode,original_title,saved_name.encode('utf8'),heb_name,show_original_year,eng_name,'0',prev_name,id,supplay))
        list.append(txt)
        all_links.append(link)
        all_s_names.append(saved_name)
    #time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()

    
    if len(rest_data)>0:
        thread=[]
        time_to_save, original_title,year,original_title2,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local=rest_data[0]
        thread.append(Thread(get_rest_s, time_to_save,original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local))
            
        
        thread[0].start()

    if Addon.getSetting("new_window_type2")=='1':

        menu = ContextMenu('plugin.video.destiny', menu,iconimage,image,description)
        menu.doModal()
        param = menu.params
        
        del menu
        
        if param==888:
            logging.warning('END EXIT')
            return 'END'
        list_index=param
    elif Addon.getSetting("new_window_type2")=='2':

        menu = ContextMenu_new('plugin.video.destiny', menu,iconimage,image,description)
        menu.doModal()
        param = menu.params
        del menu
        
        if param==888:
            logging.warning('END EXIT')
            return 'END'
        list_index=param
    elif Addon.getSetting("new_window_type2")=='3':
        param=0
        done1_1=3
        global now_playing_server,playing_text,mag_start_time_new
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        menu2 = ContextMenu_new2('plugin.video.destiny', menu,iconimage,image,description)
        menu2.show()
        play_now=0
        if Addon.getSetting("play_first")=='true':
            if not allow_debrid:
                for name, server,pre_n,q,supplay,size,link,rd in menu:
                    
                    if "magnet" in server:
                        real_index+=1
                    elif len(server)>0:
                        break
            
            if (real_index<len(all_s_names)) and only_torrent=='no':
                play_now=1
                xbmc.sleep(100)
                '''
                try:
                    xbmc.sleep(100)
                    play(all_s_names[real_index].encode('utf8'),all_links[real_index],iconimage,image,all_plot[real_index],data,season,episode,original_title,all_s_names[real_index].encode('utf8'),heb_name,show_original_year,eng_name,'0',prev_name,id,windows_play=True)
                except:
                    pass
                '''
        while param!=888:
            try:
                
                param = menu2.params
                
            except Exception as e:
                logging.warning('Skin E:'+str(e))
                param=7777
            
            list_index=param
            fast_link=' '
            f_plot=' '
           
            if (param!=7777 and param!=None and param!=666666) or play_now>0:
                if play_now>0:
                    fast_link=all_links[real_index]
                    f_plot=all_plot[real_index]
                    list_index=real_index
                else:
                    if list_index!=999 and list_index!=888:
                        fast_link=all_links[list_index]
                        f_plot=all_plot[list_index]
                    if list_index==888 or list_index==999: 
                        logging.warning('Stop Play')
                        stop_try_play=True
                        
                        return 'ok'
                now_playing_server=all_server_name[list_index]+'$$$$'+str(list_index-real_index+1)+'/'+str(len(all_links))
                if fast_link!=' ':
                    xbmc.Player().stop()
                   
           
                    if 'plugin:' in fast_link:
                        #xbmc.executebuiltin('Container.update("%s")'%fast_link)
                        url,name,iconimage,mode,fanart,description,data,original_title,id,season,episode,tmdbid,eng_name,show_original_year,heb_name,isr,saved_name,prev_name,dates,data1,fast_link,fav_status,only_torrent,only_heb_servers,new_windows_only=undo_get_rest_data(fast_link)
                        menu2.close_now()
                        get_sources(name, url,iconimage,fanart,description+'-NEXTUP-',data,original_title,season,episode,id,eng_name,show_original_year,heb_name,str(isr),dates=dates,fav_status=fav_status)
                        
                        break
                        
                        
                        
                    else:
      
                            logging.warning('1')
                       
                       
                            
                            if ('Auto Play' in all_s_names[list_index]) or play_now>0:
                                auto_fast=True
                                play_now=0
                                new_index=real_index
                                errors=[]
                                play_ok=0
                                while(1):
                                        menu2.tick=60
                                        menu2.auto_play=1
                                        try:
                                            
                                            menu2.tick=60
                                            if xbmc.Player().isPlaying():
                                                play_time=int(Addon.getSetting("play_full_time"))
                                                count_p=0
                                                
                                                while(1):
                                                    menu2.tick=60
                                                    vidtime = xbmc.Player().getTime()
                                                    
                                                    try:
                                                        value_d=(vidtime-(int(float(mag_start_time_new)))) 
                                                    except:
                                                        value_d=vidtime
                                                    if value_d> (play_time/2) :
                                                        play_ok=1
                                                        #xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                                                        logging.warning('Closing Played')
                                                        break
                                                    count_p+=1
                                                    if count_p>(play_time*2) :
                                                        logging.warning('Closing Not Played')
                                                        break
                                                    try:
                                                        param = menu2.params
                                                    except Exception as e:
                                                        logging.warning('Skin Error2:'+str(e))
                                                    
                                                    if param==888:
                                                        logging.warning('Close:11')
                                                        logging.warning('CACEL PLAY AUTO')
                                                        break
                                                    xbmc.sleep(500)
                                            if play_ok>0:
                                                logging.warning('Close:10')
                                                break
                                            f_new_link=all_links[new_index]
                                            '''
                                            if new_index<5:
                                                f_new_link='www'
                                            '''
                                            now_playing_server=all_server_name[new_index]+'$$$$'+str(new_index-real_index+1)+'/'+str(len(all_links))
                                            playing_text='Trying next link$$$$'+'0'
                                            try:
                                                param = menu2.params
                                            except Exception as e:
                                                logging.warning('Skin Error2:'+str(e))
                                            
                                            if param==888:
                                                logging.warning('Close:9')
                                                logging.warning('CACEL PLAY AUTO')
                                                break
                                            menu2.count_p=0
                                            logging.warning('time')
                                            
                                            if not allow_debrid and Addon.getSetting('auto_magnet_free')=='false':
                                              if not "magnet" in all_server_name[new_index]:
                            
                                                play(name,f_new_link,iconimage,image,all_plot[new_index],data,season,episode,original_title,all_s_names[new_index].encode('utf8'),heb_name,show_original_year,eng_name,isr,prev_name,id,windows_play=False,auto_fast=auto_fast,auto_play=True)
                                            else:
                                                play(name,f_new_link,iconimage,image,all_plot[new_index],data,season,episode,original_title,all_s_names[new_index].encode('utf8'),heb_name,show_original_year,eng_name,isr,prev_name,id,windows_play=False,auto_fast=auto_fast,auto_play=True)
                                            if (new_index>real_index):
                                                errors.append(f_new_link+'\n'+all_plot[new_index])
                                                
                                                logging.warning('Send Error:'+f_new_link)
                                            new_index+=1
                                            logging.warning('time2')
                                            if new_index>=len(all_links):
                                                
                                                logging.warning('Close:91')
                                                #menu2.close_now()
                                                break
                                            playing_text='Playing please wait...$$$$'+'0'
                                            xbmc.sleep(500)
                                            
                                            if len(errors)>0:
                                                sendy('\n'.join(errors),'Error Auto Des','DesAuto')
                                        
                                        except Exception as e:
                                            import linecache
                                            new_index+=1
                                            playing_text='Bad link moving on...$$$$'+'0'
                                            if new_index>=len(all_links):
                                                logging.warning('Close:92')
                                                menu2.close_now()
                                                break
                                            playing_text='Bad source...$$$$'+'0'
                                            
                                            import linecache
                                            exc_type, exc_obj, tb = sys.exc_info()
                                            f = tb.tb_frame
                                            lineno = tb.tb_lineno
                                            filename = f.f_code.co_filename
                                            linecache.checkcache(filename)
                                            line = linecache.getline(filename, lineno, f.f_globals)

                                            logging.warning('ERROR IN SKIN:'+str(e))
                                            logging.warning('inline:'+line)
                                            logging.warning(e)
                                            pass
                                        
                            else:
                                auto_fast=False
                                counter_end=0
                                try:
                                   while(1):
                                        counter_end+=1
                                        if counter_end>500:
                                            menu2.close_now()
                                            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Try manual...'.decode('utf8'))).encode('utf-8'))
                                            break
                                        if fast_link!=' ' and (param!=7777 and param!=None and param!=666666):
                                            menu2.params=666666
                                            xbmc.Player().stop()
                                            now_playing_server=all_server_name[param]+'$$$$'+str(param-real_index+1)+'/'+str(len(all_links))
                           
                                            
                                            if 'plugin:' in fast_link:
                                                #xbmc.executebuiltin('Container.update("%s")'%fast_link)
                                                url,name,iconimage,mode,fanart,description,data,original_title,id,season,episode,tmdbid,eng_name,show_original_year,heb_name,isr,saved_name,prev_name,dates,data1,fast_link,fav_status,only_torrent,only_heb_servers,new_windows_only=undo_get_rest_data(fast_link)
                                                menu2.close_now()
                                                get_sources(name, url,iconimage,fanart,description+'-NEXTUP-',data,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,dates=dates,fav_status=fav_status)
                                                
                                                break
                                            else:
                                                try:
                                                    play(name,fast_link,iconimage,image,f_plot,data,season,episode,original_title,all_s_names[list_index].encode('utf8'),heb_name,show_original_year,eng_name,isr,prev_name,id,windows_play=False,auto_fast=auto_fast,auto_play=True)
                                                except:
                                                    playing_text='Bad link...$$$$'+'0'
                                                    pass
                                            fast_link=''
                                            
                                        play_ok=0
                                        if xbmc.Player().isPlaying():
                                                play_time=int(Addon.getSetting("play_full_time"))
                                                count_p=0
                                                
                                                while(1):
                                                    menu2.tick=60
                                                    vidtime = xbmc.Player().getTime()
                                                    
                                                    try:
                                                        value_d=(vidtime-(int(float(mag_start_time_new)))) 
                                                    except:
                                                        value_d=vidtime
                                                    if value_d> (play_time/2) :
                                                        play_ok=1
                                                        #xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                                                        logging.warning('Closing Played')
                                                        break
                                                    count_p+=1
                                                    if count_p>(play_time*2) :
                                                        logging.warning('Closing Not Played')
                                                        break
                                                    try:
                                                        param = menu2.params
                                                    except Exception as e:
                                                        logging.warning('Skin Error2:'+str(e))
                                                    
                                                    if param==888:
                                                        logging.warning('Close:11')
                                                        logging.warning('CACEL PLAY AUTO')
                                                        break
                                                    xbmc.sleep(500)
                                        if play_ok>0:
                                                logging.warning('Close:120')
                                                break
                                        if (param!=7777 and param!=None and param!=666666):
                                            list_index=param-real_index
                                            logging.warning('list_index: '+str(list_index))
                                            if list_index!=999 and list_index!=888:
                                                fast_link=all_links[list_index]
                                                f_plot=all_plot[list_index]
                                            if list_index==888 or list_index==999: 
                                                logging.warning('Stop Play')
                                                stop_try_play=True
                                                logging.warning('Break now: '+str(list_index))
                                                break
                                        try:
                                            param = menu2.params
                                        except Exception as e:
                                            logging.warning('Skin E:'+str(e))
                                            param=7777
                                        if param==888 or param==999: 
                                                logging.warning('Stop Play')
                                                stop_try_play=True
                                                logging.warning('Break now2: '+str(list_index))
                                                break
                                        xbmc.sleep(500)
                                        logging.warning('Tick: '+str(param))
                                except Exception as e:
                                    import linecache
                                    exc_type, exc_obj, tb = sys.exc_info()
                                    f = tb.tb_frame
                                    lineno = tb.tb_lineno
                                    logging.warning('SKIN EEEE:'+str(e)+' At:'+str(lineno))
                                    pass
                                    
                    menu2.played()
            
            
            if param==888 or param==7777:
                #menu2.close_now()
                #xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
                
                break
            else:
                xbmc.sleep(500)
        counter=0
        while 1:
            alive=0
           
            for thread in threading.enumerate():
              
              if (thread.isAlive()):
                 alive=1
                 thread._Thread__stop()
                 
            if alive==0 or counter>10:
                break
            counter+=1
            xbmc.sleep(200)
        
        logging.warning('Del window')
        xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
        done1=2
        del menu2
    else:
        window = sources_window(original_title ,list,'0',image,description)
        window.doModal()

        del window
        
    if Addon.getSetting("new_window_type2")!='3':
        fast_link=' '
        f_plot=' '

        
        if list_index!=999 and list_index!=888:
            fast_link=all_links[list_index]
            f_plot=all_plot[list_index]
        if list_index==888 or list_index==999: 
            logging.warning('Stop Play')
            stop_try_play=True
            url=''
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            return 'OK'
        logging.warning('list_index:'+str(list_index))
        if fast_link!=' ':
            xbmc.Player().stop()
   
            
            if 'plugin:' in fast_link:
                #xbmc.executebuiltin('Container.update("%s")'%fast_link)
                url,name,iconimage,mode,fanart,description,data,original_title,id,season,episode,tmdbid,eng_name,show_original_year,heb_name,isr,saved_name,prev_name,dates,data1,fast_link,fav_status,only_torrent,only_heb_servers,new_windows_only=undo_get_rest_data(fast_link)
                
                get_sources(name.replace('Cached ',''), url,iconimage,fanart,description+'-NEXTUP-',data,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,dates=dates,fav_status=fav_status)
                
               
                
                
            else:
               
                logging.warning(all_s_names[list_index])
                
                    
                play(name.replace('Cached ',''),fast_link,iconimage,image,f_plot,data,season,episode,original_title,all_s_names[list_index].encode('utf8'),heb_name,show_original_year,eng_name,'0',prev_name,id)
                '''
                isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
                
               
                    
                played=False
                while isbusy:
                    isbusy  = xbmc.getCondVisibility('Window.IsActive(busydialog)')
                    xbmc.sleep(200)
                if xbmc.Player().isPlaying():
                    xbmc.sleep(2000)
                    vidtime = xbmc.Player().getTime()
                    if vidtime > 0:
                        played=True
                logging.warning('played')
                logging.warning(played)
                if not played:
                    m,data,description,eng_name,episode,image,heb_name,iconimage,id,prev_name,original_title,season,show_original_year,n,rest_data,n_magnet,only_heb,len_all_torrent_s,next_ep=original_data[0]
                    new_show_sources(m,data,description,eng_name,episode,image,heb_name,iconimage,id,prev_name,original_title,season,show_original_year,n,rest_data,n_magnet,only_heb,len_all_torrent_s,next_ep)
                xbmc.sleep(200)
                '''
        return 'END'
    return 'ok'
def show_sources():
    global list_index

    list=[]
    
    time_to_save=int(Addon.getSetting("save_time"))
    
    dbcur.execute("SELECT * FROM sources")

    match = dbcur.fetchone()

    if match!=None:
        name,url,icon,image,plot,year,season,episode,original_title,heb_name,show_original_year,eng_name,isr,id=match
        m=[]
        m.append((name,url,icon,image,plot,year,season,episode,original_title,heb_name,show_original_year,eng_name,isr,id))
  
        prev_name=name
       

        iconimage=icon
        fanart=image
        data=year

        description=plot.replace('-Episode ','').replace('-NEXTUP-','').encode('utf8')
        if season!=None and season!="%20":
           name1=name
        else:
           name1=name.encode('utf8').replace("%27","'").replace("%20"," ")
        
        match_a,all_links_fp,all_pre,f_subs= cache.get(c_get_sources, time_to_save,original_title ,year,original_title.replace("%27","'"),season,episode,id,eng_name.replace("%27","'"),show_original_year,heb_name.replace("%27","'"),isr,False,'false','no','0', table='pages')

        all_data=fix_links(match_a,iconimage,fanart,description,show_original_year,season,episode)
        
        all_links=[]
  
        for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_data:
          
            list.append('[COLOR gold]'+str(pre)+'%[/COLOR]-[COLOR gold]'+q+'[/COLOR][COLOR lightblue]'+server+'[/COLOR]-'+name+'$$$$$$$'+link)
            all_links.append(link)

        #time_left=xbmc.Player().getTotalTime()-xbmc.Player().getTime()
        time_to_wait=int(Addon.getSetting("show_p_time"))

        window = MyAddon(name  ,list,time_to_wait,image,plot)
        window.doModal()

        del window

        fast_link=' '
        if list_index!=999 and list_index!=888:
            fast_link=all_links[list_index]
        if list_index==888: 
            return '0'
        if fast_link!=' ':
            xbmc.Player().stop()
            
            xbmc.executebuiltin(('XBMC.PlayMedia("plugin://plugin.video.destiny/?data=%s&dates=EMPTY&description=%s&eng_name=%s&episode=%s&fanart=%s&heb_name=%s&iconimage=%s&id=%s&isr=' '&mode2=5&name=%s&original_title=%s&season=%s&show_original_year=%s&tmdbid=EMPTY&url=%s&fast_link=%s&prev_name=%s",return)'%(data,urllib.quote_plus(description),eng_name,episode,urllib.quote_plus(fanart),heb_name,urllib.quote_plus(iconimage),id,prev_name,original_title,season,show_original_year,urllib.quote_plus(fast_link),urllib.quote_plus(fast_link),prev_name)).replace('EMPTY','%20'))
def last_sources():

    show_sources()
def acestream():
    addDir3('Search'.decode('utf8'),'www',77,'https://lh3.googleusercontent.com/0m0JeYjdEbLUVYCn_4vQjgaybPzyZB9z1fazy07JFkKyF6dK1gboo7_N9cz0GADxJw4=s180','https://i.pinimg.com/originals/6b/18/31/6b1831503dc0e0470b2bf1e1b5df978f.jpg','Acestream'.decode('utf8'))
    addDir3('My Channels'.decode('utf8'),'www',79,'https://lh3.googleusercontent.com/0m0JeYjdEbLUVYCn_4vQjgaybPzyZB9z1fazy07JFkKyF6dK1gboo7_N9cz0GADxJw4=s180','https://i.pinimg.com/originals/6b/18/31/6b1831503dc0e0470b2bf1e1b5df978f.jpg','Acestream'.decode('utf8'))
def search_ace():
        search_entered=''
       
        
        keyboard = xbmc.Keyboard(search_entered, 'Enter search')
        keyboard.doModal()
        if keyboard.isConfirmed():
               search_entered = keyboard.getText()
               headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Referer': 'https://acestreamsearch.com/en/',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
               }

               data = {
                  'cn': search_entered
               }

               response = requests.post('https://acestreamsearch.com/en/', headers=headers, data=data).content
               regex_pre='<ul class="list-group">(.+?)</ul>'
               match_pre=re.compile(regex_pre).findall(response)
               for item in match_pre:
                regex='<li class="list-group-item"><a href="(.+?)">(.+?)<'
                match=re.compile(regex).findall(item)
                icon='https://lh3.googleusercontent.com/0m0JeYjdEbLUVYCn_4vQjgaybPzyZB9z1fazy07JFkKyF6dK1gboo7_N9cz0GADxJw4=s180'
                fanart='https://i.pinimg.com/originals/6b/18/31/6b1831503dc0e0470b2bf1e1b5df978f.jpg'
                for link,name in match:
                   
                    regex='acestream://(.+?)(?:/|$)'
                    match=re.compile(regex).findall(link)
                    f_link='http://127.0.0.1:6878/ace/getstream?id='+match[0]
                    addLink(name,f_link,5,False,iconimage=icon,fanart=fanart,description=name)
               headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                }

               params = (
                    ('sort', 'fname'),
                )
               logging.warning('Getting')
               response = requests.get('http://91.92.66.82/trash/ttv-list/AceLiveList.php', headers=headers, params=params).content
               regex='type=checkbox /></TD><TD data-v="(.+?)">.+?</TD><TD data-v=".+?">.+?</TD><TD>(.+?)<'
                      
               match=re.compile(regex).findall(response)
       
       
               for name,link in match:
                   if search_entered.lower() in name.lower():
                   
                    f_link='http://127.0.0.1:6878/ace/getstream?id='+link
                    addLink('[S-2] '+name,f_link,5,False,iconimage=icon,fanart=fanart,description=name)
               headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
                }

               response = requests.get('https://www.livefootballol.me/acestream-channel-list-2018.html', headers=headers).content
               regex='<tr>(.+?)</tr>'
               match_pre=re.compile(regex,re.DOTALL).findall(response)
               for items in match_pre:
                   regex='a href=".+?>(.+?)<.+?<td>(.+?)<'
                   match=re.compile(regex,re.DOTALL).findall(items)
                   #logging.warning(match
                   for name,link in match:
              
                       if search_entered.lower() in name.lower():
                        regex='acestream://(.+?)(?:/|$)'
                        match=re.compile(regex).findall(link)
                        f_link='http://127.0.0.1:6878/ace/getstream?id='+match[0]
                        addLink('[S-3] '+name,f_link,5,False,iconimage=icon,fanart=fanart,description=name)
def chan_ace(name,url,description):
    
    if description=='add':
        dbcur.execute("INSERT INTO acestream Values ('%s', '%s', '%s', '%s','%s', '%s', '%s');" %  (name.replace("'","%27"),url,description.replace("'","%27"),'','','',''))
        dbcon.commit()
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Added'.decode('utf8'))).encode('utf-8'))
    elif description=='remove':
        dbcur.execute("DELETE  FROM acestream WHERE url = '%s'"%(url))
        
      
        dbcon.commit()
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Removed'.decode('utf8'))).encode('utf-8'))
def refresh_ace(search_entered):
    o_name=search_entered

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://acestreamsearch.com/en/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = {
      'cn': search_entered
    }
    f_link=''
    response = requests.post('https://acestreamsearch.com/en/', headers=headers, data=data).content
    regex_pre='<ul class="list-group">(.+?)</ul>'
    match_pre=re.compile(regex_pre).findall(response)
    for item in match_pre:
        regex='<li class="list-group-item"><a href="(.+?)">(.+?)<'
        match=re.compile(regex).findall(item)
        icon='https://lh3.googleusercontent.com/0m0JeYjdEbLUVYCn_4vQjgaybPzyZB9z1fazy07JFkKyF6dK1gboo7_N9cz0GADxJw4=s180'
        fanart='https://i.pinimg.com/originals/6b/18/31/6b1831503dc0e0470b2bf1e1b5df978f.jpg'
        for link,name in match:
            
            regex='acestream://(.+?)(?:/|$)'
            match=re.compile(regex).findall(link)
            
            if search_entered==name:
                f_link='http://127.0.0.1:6878/ace/getstream?id='+match[0]
                #return f_link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    params = (
        ('sort', 'fname'),
    )

    response = requests.get('http://91.92.66.82/trash/ttv-list/AceLiveList.php', headers=headers, params=params).content
    regex='type=checkbox /></TD><TD data-v="(.+?)">.+?</TD><TD data-v=".+?">.+?</TD><TD>(.+?)<'
           
    match=re.compile(regex).findall(response)


    logging.warning('Renew s2')
    for name,link in match:
       
       
       if search_entered.lower() =='[s-2] '+name.lower():
        logging.warning('Found s2')
        f_link='http://127.0.0.1:6878/ace/getstream?id='+link
    
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

    response = requests.get('https://www.livefootballol.me/acestream-channel-list-2018.html', headers=headers).content
    regex='<tr>(.+?)</tr>'
    match_pre=re.compile(regex,re.DOTALL).findall(response)

    for items in match_pre:
           regex='a href=".+?>(.+?)<.+?<td>(.+?)<'
           match=re.compile(regex,re.DOTALL).findall(items)
           #logging.warning(match
           for name,link in match:
               
               if search_entered.lower() =='[s-3] '+ name.lower():
                regex='acestream://(.+?)(?:/|$)'
                match=re.compile(regex).findall(link)
                f_link='http://127.0.0.1:6878/ace/getstream?id='+match[0]
               
    if f_link=='':
      xbmcgui.Dialog().ok("Error",'Missing channel')
      sys.exit()
    else:
      return f_link
def my_ace():
    dbcur.execute("SELECT * FROM acestream")

    match = dbcur.fetchall()
    
    icon='https://lh3.googleusercontent.com/0m0JeYjdEbLUVYCn_4vQjgaybPzyZB9z1fazy07JFkKyF6dK1gboo7_N9cz0GADxJw4=s180'
    fanart='https://i.pinimg.com/originals/6b/18/31/6b1831503dc0e0470b2bf1e1b5df978f.jpg'
    for name,link,plot,op,op1,op2,op3 in match:
        addLink(name,'aceplay',5,False,iconimage=icon,fanart=fanart,description=name)


def all_new_source(url):
    headers = {
                
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                }
    x=requests.get(url,headers=headers,verify=False).content

    regex='<div class=".+?-post">.+?a href="(.+?)">(.+?)<.+?<img.+?src="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(x)
    for link,name,image in match:
        addDir3(name,link,85,image,image,name)
        
    regex='link rel="next" href="(.+?)"'
    match=re.compile(regex).findall(x)
    if len(match)>0:
        addDir3('[COLOR aqua][I]Next Page[/I][/COLOR]',match[0],85,iconimage,fanart,'Next Page')
        

def uploadThis(f,myFTP):
    from os.path import basename
    fh = open(f, 'rb')
    myFTP.storbinary('STOR %s' % Addon.getSetting("db_bk_name")+'1_'+str(time.strftime("%d/%m/%Y")).replace('/','_'), fh)
    fh.close()
def do_bakcup(silent='True'):

    
    from zfile import ZipFile
    import datetime,os
    from shutil import copyfile
    from os.path import basename
    if silent=='False':
        logging.warning('silent2')
        dp = xbmcgui . DialogProgress ( )
        dp.create('Please wait','Connecting server', '','')
        dp.update(0, 'Please wait','Zipping', '' )
    
    zp_file=os.path.join(user_dataDir, 'data.zip')
    cacheFile = os.path.join(user_dataDir, 'cache_play.db')
    setting_file=os.path.join(user_dataDir, 'settings.xml')
    if os.path.isfile(zp_file):
        os.remove(zp_file)
    zipf = ZipFile(zp_file , mode='w')
    zipf.write(cacheFile , basename(cacheFile))
    zipf.write(setting_file , basename(setting_file))
    zipf.close()
    
    
    from os.path import basename
    if Addon.getSetting("remote_selection")=='0':
        onlyfiles=[]
        db_bk_folder=xbmc.translatePath(Addon.getSetting("remote_path"))
        dirList, onlyfiles =xbmcvfs.listdir(db_bk_folder)
      
        ct_min=0
        
            
        count=0
        for files in onlyfiles:
            f_patch_file=os.path.join(db_bk_folder,files)
            if Addon.getSetting("db_bk_name") in basename(files):
                count+=1
        
        if count>5:
            for files in onlyfiles:
                f_file=(os.path.join(db_bk_folder,files))
                if Addon.getSetting("db_bk_name") not in basename(f_file):
                  continue
                st = xbmcvfs.Stat(f_file)
                ct_date = st.st_mtime()
               
                #ct_date=time.ctime(os.path.getctime(f_file))
                if ct_min==0:
                    ct_min=ct_date
                elif ct_date<ct_min:
                    ct_min=ct_date
            
            for files in onlyfiles:
                f_file=os.path.join(db_bk_folder,files)
                if Addon.getSetting("db_bk_name") not in basename(f_file):
                  continue
                st = xbmcvfs.Stat(f_file)
                ct_date = st.st_mtime()
                #ct_date=time.ctime(os.path.getctime(f_file))
               
                if ct_date==ct_min:
                   
                    xbmcvfs.delete(f_file)
                    break
        xbmcvfs.copy (zp_file,os.path.join(db_bk_folder,Addon.getSetting("db_bk_name")+'_'+str(time.strftime("%d/%m/%Y")).replace('/','_')))
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Backup OK'.decode('utf8'))).encode('utf-8'))
    else:
        if silent=='False':
            dp.update(20, 'Please wait','Connecting server', '' )
        import ftplib
        import os,urllib
        from datetime import datetime
        import _strptime
            
        server=Addon.getSetting("ftp_host")
        username=Addon.getSetting("ftp_user")
        password=Addon.getSetting("ftp_pass")
        try:
            myFTP = ftplib.FTP(server, username, password)
            if silent=='False':
                dp.update(40, 'Please wait','Connection successful', '' )
            files = myFTP.nlst()
            found=0
            if silent=='False':
                dp.update(60, 'Please wait','Collecting', '' )
            for f in files:
                
               
                
                if 'kodi_backup' in f:
                    found=1
                    
            if found==0:
                myFTP.mkd('kodi_backup')
            myFTP.cwd('kodi_backup')
            files = myFTP.nlst()
           
            count=0
            ct_min=0
            for f in files:
                
                if Addon.getSetting("db_bk_name") in basename(f):
                    count+=1
            if count>5:
                for f in files:
                    if Addon.getSetting("db_bk_name") not in basename(f):
                       continue
                    try:
                        modifiedTime = myFTP.sendcmd('MDTM ' + f)
                       
                        
                        #ct_date=datetime.strptime(modifiedTime[4:], "%Y%m%d%H%M%S").strftime("%d %B %Y %H:%M:%S")
                        try:
                            ct_date = datetime.strptime(modifiedTime[4:], "%Y%m%d%H%M%S").strftime("%d %B %Y %H:%M:%S")
                        except TypeError:
                            ct_date = datetime.fromtimestamp(time.mktime(time.strptime(modifiedTime[4:], "%Y%m%d%H%M%S")))
                            ct_date = ct_date.strftime("%d %B %Y %H:%M:%S")
                        
                        if ct_min==0:
                            ct_min=ct_date
                        elif ct_date<ct_min:
                            ct_min=ct_date
                    except Exception as e:
                        logging.warning(e)
                        pass
             
                for f in files:
                    if Addon.getSetting("db_bk_name") not in basename(f):
                       continue
            
                    modifiedTime = myFTP.sendcmd('MDTM ' + f)
          
             
                    
                    #ct_date=datetime.strptime(modifiedTime[4:], "%Y%m%d%H%M%S").strftime("%d %B %Y %H:%M:%S")
                    try:
                        ct_date = datetime.strptime(modifiedTime[4:], "%Y%m%d%H%M%S").strftime("%d %B %Y %H:%M:%S")
                    except TypeError:
                        ct_date = datetime.fromtimestamp(time.mktime(time.strptime(modifiedTime[4:], "%Y%m%d%H%M%S")))
                        ct_date = ct_date.strftime("%d %B %Y %H:%M:%S")
                   
                    if ct_date==ct_min:
                    
                        
                        myFTP.delete(f)
                        break
            if silent=='False':
                dp.update(80, 'Please wait','Uploading', '' )
            uploadThis(zp_file,myFTP)
            
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Buckup Done'.decode('utf8'))).encode('utf-8'))
        except Exception as e:
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Error In backup'.decode('utf8'))).encode('utf-8'))
    try:
        xbmc.sleep(1000)
        if os.path.isfile(zp_file):
            os.remove(zp_file)
    except:
        pass
    if silent=='False':
        dp.close()
    logging.warning('Done backing up')
def restore_backup():
    from shutil import copyfile
    import os
    if 1:#try:
        cacheFile = os.path.join(user_dataDir, 'cache_play.db')
        zp_file= os.path.join(user_dataDir, 'data.zip')
        from os.path import basename
        if Addon.getSetting("remote_selection")=='0':
           
            onlyfiles=[]
            db_bk_folder=xbmc.translatePath(Addon.getSetting("remote_path"))
            dirList, onlyfiles =xbmcvfs.listdir(db_bk_folder)
            
    
            all_n=[]
            all_f=[]
            for f in onlyfiles:
                all_n.append(basename(f))
                all_f.append(os.path.join(db_bk_folder,f))
            ret = xbmcgui.Dialog().select("Choose backup file", all_n)
            if ret!=-1:
                ok=xbmcgui.Dialog().yesno(("Restore from backup"),all_n[ret]+' Restore? ')
                if ok:
                    db_name=Addon.getSetting('db_bk_name')
                    if '.db' not in all_n[ret]:
                        xbmcvfs.copy(all_f[ret],os.path.join(user_dataDir,'temp_zip'))
                        unzip(os.path.join(user_dataDir,'temp_zip'),user_dataDir)
                        xbmcvfs.delete(os.path.join(user_dataDir,'temp_zip'))
                    else:
                        xbmcvfs.copy(all_f[ret],cacheFile)
                    #xbmc.executebuiltin('Container.Update')
                    #Addon.setSetting('db_bk_name',db_name)
                    xbmcgui.Dialog().ok("Restore from backup",'[COLOR aqua][I]Restore done[/I][/COLOR]')
            else:
               sys.exit()
        else:
            dp = xbmcgui . DialogProgress ( )
            dp.create('Please wait','Connecting to server', '','')
            dp.update(0, 'Please wait','Connecting to server', '' )
            import ftplib
            import os,urllib
            from datetime import datetime
            server=Addon.getSetting("ftp_host")
            username=Addon.getSetting("ftp_user")
            password=Addon.getSetting("ftp_pass")
            try:
            
              myFTP = ftplib.FTP(server, username, password)
            except Exception as e:
               xbmcgui.Dialog().ok('Error in connecting',str(e))
               sys.exit()
            dp.update(0, 'Please wait','Succesfull', '' )
            files = myFTP.nlst()
            found=0
            for f in files:
         
                if 'kodi_backup' in f:
                    found=1
            if found==0:
            
                xbmcgui.Dialog().ok("Restore",'[COLOR red][I]No backup exists[/I][/COLOR]')
                sys.exit()
            myFTP.cwd('kodi_backup')
            files = myFTP.nlst()
           
            count=0
            ct_min=0
            all_n=[]
            all_f=[]
            dp.update(0, 'Please wait','Collecting', '' )
            for f in files:

                all_n.append(basename(f))
                all_f.append(f)
            ret = xbmcgui.Dialog().select("choose file to backup", all_n)
            if ret!=-1:
                ok=xbmcgui.Dialog().yesno(("Resotre"),all_n[ret]+' Restore? ')
                if ok:
                    
                    db_name=Addon.getSetting('db_bk_name')
                    i=cacheFile
                    dp.update(0, 'Please wait','downloading', '' )
                    myFTP.retrbinary("RETR " + all_f[ret] ,open(i, 'wb').write)
                    dp.close()
                    if '.db' not in all_n[ret]:
                        myFTP.retrbinary("RETR " + all_f[ret] ,open(zp_file, 'wb').write)
                        unzip(zp_file,user_dataDir)
                    else:
                        myFTP.retrbinary("RETR " + all_f[ret] ,open(i, 'wb').write)
                    Addon.setSetting('db_bk_name',db_name)
                    xbmcgui.Dialog().ok("Restore",'[COLOR aqua][I]Succesfull[/I][/COLOR]')
            else:
               sys.exit()
        if os.path.isfile(zp_file):
            os.remove(zp_file)
   
    try:
        dp.close()
    except:
        pass
def backup_vik():
    import datetime
    strptime = datetime.datetime.strptime
    logging.warning('backing up')
    threading.Thread(target=do_bakcup).start()
    return '1'
def check_ftp_conn():
    import ftplib
    import os,urllib
    from datetime import datetime
    try:
        server=Addon.getSetting("ftp_host")
        username=Addon.getSetting("ftp_user")
        password=Addon.getSetting("ftp_pass")
 
        myFTP = ftplib.FTP(server, username, password)
        xbmcgui.Dialog().ok('Success','[COLOR gold]Success[/COLOR]')
    except Exception as e:
        xbmcgui.Dialog().ok('Error',str(e))



            
            

            




def nba(url,icon,fanart):
    headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
          }
    html=requests.get(url,headers=headers).content
    regex='<option class="level-0" value="(.+?)">(.+?)<'
    match=re.compile(regex).findall(html)
    addNolink('Teams','www',940,False,iconimage=icon,fanart=fanart)
    
    for link,name in match:
        addDir3(name,'https://www.nbafullhd.com/?cat='+link,107,icon,fanart,name)
    addNolink('[COLOR lightblue][I]Archives[/I][/COLOR]','www',940,False,iconimage=icon,fanart=fanart)
    regex_pre='<option value="">Select Month</option>(.+?)</select>'
    m_pre=re.compile(regex_pre,re.DOTALL).findall(html)
    regex="<option value='(.+?)'>(.+?)</option>"
    match=re.compile(regex).findall(m_pre[0])
    
    
    for link,name in match:
        addDir3(name,link,107,icon,fanart,name)
def deep_nba(url,icon,fanart):
    headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
          }
    html=requests.get(url,headers=headers).content
    regex='<div class="entry-thumbnail thumbnail-landscape">.+?<a href="(.+?)" title="(.+?)".+?src="(.+?)"' 
    match=re.compile(regex,re.DOTALL).findall(html)
  
    for link,title,image in match:
        title=replaceHTMLCodes(title)
        addDir3(title,link,108,image,image,title)
    regex='class="nextpostslink" rel="next" href="(.+?)"'
    match=re.compile(regex).findall(html)
    if len(match)>0:
        addDir3('[COLOR aqua][I]Next Page[/I][/COLOR]',match[0],107,icon,fanart,'[COLOR aqua][I]Next Page[/I][/COLOR]')
        
def play_nba(name,url,icon,fanart):
    headers = {
            
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
          }

    html=requests.get(url,headers=headers).content
    regex='<p>Watch NBA(.+?)<div class="'
    m_pre=re.compile(regex,re.DOTALL).findall(html)
    
  
    regex='iframe.+?src="(.+?)"'
    m22=re.compile(regex).findall(html)
    for links in m22:
        if 'facebook' not in links:
            if 'http' not in links:
                m22[0]='http:'+links
  
            regex='//(.+?)/'
            server=re.compile(regex).findall(links)
            if len(server)>0:
                server=server[0]
              
                
                addLink('[COLOR gold]'+server+'[/COLOR]', links,5,False,icon,fanart,'__NBA__'+'\n-HebDub-',original_title=name,saved_name=name)
    if len(m_pre)>0:
        regex='a href="(.+?)".+?alt="(.+?)"'
        m=re.compile(regex,re.DOTALL).findall(m_pre[0])
        for link,nn in m:
            z=requests.get(link,headers=headers).content
            regex='iframe.+?src="(.+?)"'
            m22=re.compile(regex).findall(z)
            if len(m22)>0:
                
                    if 'http' not in m22[0]:
                        m22[0]='http:'+m22[0]
             
                    regex='//(.+?)/'
                    server=re.compile(regex).findall(m22[0])
                    if len(server)>0:
                        server=server[0]
              
                        
                        addLink('[COLOR gold]'+server+'[/COLOR] - '+nn, m22[0],5,False,icon,fanart,'__NBA__'+'\n-HebDub-',original_title=name,saved_name=name)
          
def last_ep_aired(id):
    x=requests.get('https://api.themoviedb.org/3/tv/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%id).json()
    season=str(x['last_episode_to_air']['season_number'])
    episode=str(x['last_episode_to_air']['episode_number'])
    name=x['last_episode_to_air']['name']
    fanart=domain_s+'image.tmdb.org/t/p/original/'+x['last_episode_to_air']['still_path']
    icon=domain_s+'image.tmdb.org/t/p/original/'+x['poster_path']
    description=x['last_episode_to_air']['overview']
    data=str(x['first_air_date'].split("-")[0])
    original_title=urllib.quote_plus(x['original_name'])
    eng_name=original_title
    show_original_year=str(x['first_air_date'].split("-")[0])
    heb_name=x['name'].decode('utf-8')
    isr='0'
    fav_search_f=Addon.getSetting("fav_search_f_tv")
    fav_servers_en=Addon.getSetting("fav_servers_en_tv")
    fav_servers=Addon.getSetting("fav_servers_tv")
   
        
   
    if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 ):
    
        fav_status='true'
    else:
        fav_status='false'
    #get_sources(name,'www',icon,fanart,description,data,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,fav_status=fav_status)
    #xbmcplugin.endOfDirectory(int(sys.argv[1]))
    xbmc.executebuiltin(('ActivateWindow(10025,"plugin://plugin.video.destiny/?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode2=4&episode=%s&eng_name=%s&fav_status=%s",return)'%(name,url,icon,fanart,description,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr,episode,eng_name,fav_status)))
    return 0
                
                

def get_server_types(type):
    if type=='tv':
        libDir = os.path.join(addonPath, 'resources', 'report_tv.txt')
    else:
        libDir = os.path.join(addonPath, 'resources', 'report_movie.txt')
    file = open(libDir, 'r') 
    file_data= file.read()
    file.close()
    regex='Start(.+?)END'
  
    m=re.compile(regex,re.DOTALL).findall(file_data)
    all_direct=[]
    all_google=[]
    all_rapid=[]
    for items in m:
        regex='\[(.+?)\].+?\{(.+?)\}'
        m2=re.compile(regex,re.DOTALL).findall(items)
        for sname,stype in m2:
           
            if 'direct' in stype.lower():
                all_direct.append(sname)
            if 'google' in stype.lower():
                all_google.append(sname)
            if 'rapidvideo' in stype.lower():
                all_rapid.append(sname)

    return all_direct,all_google,all_rapid

def get_im_data_rt(imdbid,plot_o,html_g,xxx):
    import random
    global all_data_imdb
    
    url='https://api.themoviedb.org/3/find/%s?api_key=b7cd3340a794e5a2f35e3abb820b497f&language=en&external_source=imdb_id'%imdbid
    
    
    
    #y=requests.get(url,headers=headers).json()
    y=json.loads(urllib2.urlopen(url).read())
    
    if 'movie' in plot_o:
        r=y['movie_results']
      
    else:

        r=y['tv_results']
        
    
    if len(r)>0:
        if 'movie' in plot_o:
            new_name=r[0]['title']
        else:
            new_name=r[0]['name']
 
        
        icon=domain_s+'image.tmdb.org/t/p/original/'+r[0]['poster_path']
        if r[0]['backdrop_path']!=None:
            image=domain_s+'image.tmdb.org/t/p/original/'+r[0]['backdrop_path']
        else:
            image=' '
        plot=r[0]['overview']
        if 'movie' in plot_o:
            original_title=r[0]['original_title']
        else:
        
            original_title=r[0]['original_name']
        rating=r[0]['vote_average']
        if 'movie' in plot_o:
            if 'release_date' in r[0]:
                if r[0]['release_date']==None:
                        year=' '
                else:
                    year=str(r[0]['release_date'].split("-")[0])
            else:
                year=' '
        else:
            if 'first_air_date' in r[0]:
                if r[0]['first_air_date']==None:
                        year=' '
                else:
                    year=str(r[0]['first_air_date'].split("-")[0])
            else:
                year=' '
        genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
        if i['name'] is not None])
        try:genere = u' / '.join([genres_list[x] for x in r[0]['genre_ids']])
        except:genere=''
         
        id=str(r[0]['id'])
        if 'movie' in plot_o:
            fav_search_f=Addon.getSetting("fav_search_f")
            fav_servers_en=Addon.getSetting("fav_servers_en")
            fav_servers=Addon.getSetting("fav_servers")
           
          
        else:
            fav_search_f=Addon.getSetting("fav_search_f_tv")
            fav_servers_en=Addon.getSetting("fav_servers_en_tv")
            fav_servers=Addon.getSetting("fav_servers_tv")
            


        if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 ):
        
            fav_status='true'
        else:
            fav_status='false'
       
        all_data_imdb.append(( new_name , url,icon,image,plot,rating,year,genere,original_title,id,heb_name,fav_status,xxx,imdbid))
        
def get_data_imdb(m,plot_o):
    import urllib2
    global all_data_imdb
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
   
    if 'movie' in plot_o:
        url_g=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
    else:

        url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
    
    if Addon.getSetting("dp")=='true':
        dp = xbmcgui . DialogProgress ( )
        dp.create('Please wait','Updating', '','')
        dp.update(0, 'Please wait','Updating', '' )
    z=0
    html_g=requests.get(url_g).json()
    thread=[]
    xxx=0
    for imdbid in m:
        
        thread.append(Thread(get_im_data_rt,imdbid,plot_o,html_g,xxx))
        thread[len(thread)-1].setName(imdbid)
        xxx+=1
    z=0
    for td in thread:
      td.start()
      if len(thread)>38:
        xbmc.sleep(255)
      else:
        xbmc.sleep(10)
      if Addon.getSetting("dp")=='true':
            dp.update(int(((z* 100.0)/(len(thread))) ), 'Please wait','Updating', td.name )
            z=z+1
    num_live_pre=0
    while 1:
         
         
          
         
        
        
          
          num_live=0
          still_alive=0
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
 
              num_live=num_live+1
              
             
              still_alive=1
            if Addon.getSetting("dp")=='true':
                dp.update(len(thread)-num_live_pre, 'Please wait','Updating', thread[yy].name )
          num_live_pre=num_live
          if Addon.getSetting("dp")=='true':
              if dp.iscanceled(): 
                    dp.close()
                    break
          
          if still_alive==0:
            break
          xbmc.sleep(100)
    if Addon.getSetting("dp")=='true':
        dp.close()
    return all_data_imdb
def must_see(plot,url):
    o_plot=plot
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    x1=requests.get(url,headers=headers).content
    if 'movie' in plot:
        mode=4
        regex='data-titleid="(.+?)"'
    else:
        mode=7
        regex='<div class="ribbonize" data-tconst="(.+?)"'
    m=re.compile(regex).findall(x1)
    if len(m)==0:
        regex='<div class="ribbonize" data-tconst="(.+?)"'
        m=re.compile(regex).findall(x1)
    all_data=cache.get(get_data_imdb,24,m,plot, table='pages')

    #all_data=get_data_imdb(m,plot)
    all_data=sorted(all_data, key=lambda x: x[12], reverse=False)
    for new_name , url,icon,image,plot,rating,year,genere,original_title,id,heb_name,fav_status,xxx,imdbid in all_data:
           
      
            addDir3( new_name , url,mode, icon,image,plot,rating=rating,data=year,show_original_year=year,generes=genere,original_title=original_title,id=id,eng_name=original_title,heb_name=new_name,fav_status=fav_status)
            
    
    
    regex='title_type=tv_series&start=(.+?)&'
    m=re.compile(regex,re.DOTALL).findall(x1)
    
    if len(m)==0:
        regex='<div class="desc">.+?a href="(.+?)"'
        m2=re.compile(regex,re.DOTALL).findall(x1)
        
        addDir3( '[COLOR gold][I]Next page[/I][/COLOR]', 'https://www.imdb.com'+m2[0],114, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png',o_plot)
    elif len(m)>0:
        addDir3( '[COLOR gold][I]Next page[/I][/COLOR]', 'https://www.imdb.com/search/title?title_type=tv_series&start=%s&ref_=adv_nxt'%m[0],114, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png',o_plot)
    return 'ok'

def get_torrent_file(silent_mode=False):
    import shutil

    dp = xbmcgui . DialogProgress ( )
    dp.create('Please wait','Chacking for player', '','')
    dp.update(0, 'Please wait','Chacking for player', '' )
    def download_file(url,path):
        local_filename =os.path.join(path, "1.zip")
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        total_length = r.headers.get('content-length')

        if total_length is None: # no content length header
            total_length=1
        with open(local_filename, 'wb') as f:
            dl = 0
            total_length = int(total_length)
            for chunk in r.iter_content(chunk_size=1024): 
                dl += len(chunk)
                done = int(100 * dl / total_length)
                dp.update(done, 'Please wait','Downlading player', '' )
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename

    def unzip(file,path):
        dp.update(100, 'Please wait','Extracting', '' )
        from zfile import ZipFile
        
        
        zip_file = file
        ptp = 'Masterpenpass'
        #xbmc.executebuiltin("XBMC.Extract({0}, {1})".format(zip_file, path), True)
        
        zf=ZipFile(zip_file)
        #zf.setpassword(bytes(ptp))
        #with ZipFile(zip_file) as zf:
        zf.extractall(path)
        
    from kodipopcorntime.platform import Platform
    binary = "torrent2http"
    bin_dataDir=(os.path.join(xbmc.translatePath(Addon.getAddonInfo('profile')), 'resources', 'bin',"%s_%s" %(Platform.system, Platform.arch))).encode('utf-8')
    if Platform.system == 'windows':
        binary = "torrent2http.exe"
        url='https://github.com/DiMartinoXBMC/script.module.torrent2http/raw/master/bin/windows_x86/torrent2http.exe.zip'
        file=os.path.join(bin_dataDir,'1.zip')
    elif Platform.system == "android":
        url='https://github.com/DiMartinoXBMC/script.module.torrent2http/raw/master/bin/android_arm/torrent2http.zip'
        file=os.path.join(bin_dataDir,'1.zip')
    else:
        url='https://github.com/DiMartinoXBMC/script.module.torrent2http/raw/master/bin/linux_arm/torrent2http.zip'
        file=os.path.join(bin_dataDir,'1.zip')
    torrent_file=os.path.join(xbmc.translatePath(Addon.getAddonInfo('profile')), 'resources', 'bin', "%s_%s" %(Platform.system, Platform.arch), binary).encode('utf-8')
    
    logging.warning(torrent_file)
    logging.warning(os.path.isfile(torrent_file))
    logging.warning(os.path.exists(bin_dataDir))
    if not os.path.exists(bin_dataDir) or not os.path.isfile(torrent_file):
        if os.path.exists(bin_dataDir):
           
            shutil.rmtree(bin_dataDir)
        
        os.makedirs(bin_dataDir)
        
        download_file(url,bin_dataDir)
        unzip(file,bin_dataDir)
        os.remove(file)
    else:
        if silent_mode==False:
       
            ok=xbmcgui.Dialog().yesno(("Player exists"),('Download anyway?'))
            if ok:
                shutil.rmtree(bin_dataDir)
                os.makedirs(bin_dataDir)
        
                download_file(url,bin_dataDir)
                unzip(file,bin_dataDir)
                os.remove(file)
        
    dp.close()
    if silent_mode==False:
        xbmcgui.Dialog().ok('Download','[COLOR aqua][I] Success [/I][/COLOR]')
def remove_torrent_file():
    import shutil
    from kodipopcorntime.platform import Platform
    bin_dataDir=(os.path.join(xbmc.translatePath(Addon.getAddonInfo('profile')), 'resources', 'bin',"%s_%s" %(Platform.system, Platform.arch))).encode('utf-8')
            
    if  os.path.exists(bin_dataDir):
        ok=xbmcgui.Dialog().yesno(("Remove magnet player"),('Remove magnet player?'))
        if ok:
            
            
            
            shutil.rmtree(bin_dataDir)
                
            xbmcgui.Dialog().ok('Remove','[COLOR aqua][I] Removed [/I][/COLOR]')
    else:
        xbmcgui.Dialog().ok('Remove','[COLOR aqua][I] Player is missing [/I][/COLOR]')
        

def GetJson(url):
    html = requests.get(url, headers={"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'}).content
    if html == "":
        return None
    resultJSON = json.loads(html)
    if resultJSON is None or len(resultJSON) < 1:
        return None
    if resultJSON.has_key("root"):
        return resultJSON["root"]
    else:
        return resultJSON
def GetLabelColor(text, keyColor=None, bold=False, color=None):
    if not color:
        if keyColor=='prColor':
            color='orange'
        else:
            color='gold'
        
        
    if bold :
        text = '[B]{0}[/B]'.format(text)
    return text if color == 'none' else '[COLOR {0}]{1}[/COLOR]'.format(color, text)
def getDisplayName(title, subtitle, programNameFormat, bold=False):
	if programNameFormat == 0:
		displayName = ' {0} - {1} '.format(GetLabelColor(title, keyColor="prColor", bold=bold) , GetLabelColor(subtitle, keyColor="chColor"))
	elif programNameFormat == 1:
		displayName = ' {0} - {1} '.format(GetLabelColor(subtitle, keyColor="chColor") , GetLabelColor(title, keyColor="prColor", bold=bold))
	return displayName

def get_actor_oscar(url):
     
    headers = {
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    x1=requests.get(url,headers=headers).content
    regex='div class="lister-item-image">.+?<img alt="(.+?)".+?src="(.+?)".+?/title/(.+?)/'
    m=re.compile(regex,re.DOTALL).findall(x1)
    all_imdb={}
    m1=[]
    for title,img,imdb in m:
        if imdb in m1:
            m1.append(imdb)
            all_imdb[imdb]['name']=all_imdb[imdb]['name']+'$$$$$$'+title
            all_imdb[imdb]['img']=all_imdb[imdb]['img']+'$$$$$$'+img
            all_imdb[imdb]['done']=1
        else:
        
            m1.append(imdb)
            all_imdb[imdb]={}
            all_imdb[imdb]['name']=title
            all_imdb[imdb]['img']=img
            all_imdb[imdb]['done']=0
    all_data=cache.get(get_data_imdb,24,m1,'Movies', table='pages')

    #all_data=get_data_imdb(m,plot)
    all_data=sorted(all_data, key=lambda x: x[5], reverse=True)
    
    for new_name , url,icon,image,plot,rating,year,genere,original_title,id,heb_name,fav_status,xxx,imdbid in all_data:
            add_p=''
            add_img=icon
            if imdbid in all_imdb:
                if '$$$$$$' in all_imdb[imdbid]['name']:
                
                    if all_imdb[imdbid]['done']==1:
                        index=1
                        add_p='[COLOR gold]Oscar Winner - '+all_imdb[imdbid]['name'].split('$$$$$$')[index]+'[/COLOR]\n'
                        add_img=all_imdb[imdbid]['img'].split('$$$$$$')[index]
                        all_imdb[imdbid]['done']=0
                        
                    else:
                        index=0
                        add_p='[COLOR gold]Oscar Winner - '+all_imdb[imdbid]['name'].split('$$$$$$')[index]+'[/COLOR]\n'
                        add_img=all_imdb[imdbid]['img'].split('$$$$$$')[index]
                        all_imdb[imdbid]['done']=1
                else:
                    add_p='[COLOR gold]Oscar Winner - '+all_imdb[imdbid]['name']+'[/COLOR]\n'
                    add_img=all_imdb[imdbid]['img']
            addDir3( new_name , url,4, add_img,image,add_p+plot,rating=rating,data=year,show_original_year=year,generes=genere,original_title=original_title,id=id,eng_name=original_title,heb_name=new_name,fav_status=fav_status)
            
    
    
    regex='next-page" href="(.+?)"'
    m=re.compile(regex).findall(x1)
  
    if len(m)>0:
      
        addDir3( '[COLOR gold][I]Next page[/I][/COLOR]', 'https://www.imdb.com'+m[0],134, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','Movies')
   
    return 'ok'



def RemoveFolder(Folder):
    import shutil
    try:
        Folder=xbmc.translatePath(Folder)
        if os.path.isdir(Folder):
                
                shutil.rmtree(Folder)
                os.makedirs(Folder)
                
        else:
                os.makedirs(Folder)
    except:
        pass

def clear_rd():
    Addon.setSetting('rd.client_id','')
    Addon.setSetting('rd.auth','')
    Addon.setSetting('rd.refresh','')
    Addon.setSetting('rd.secret','')
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', ('Cleared').decode('utf8'))).encode('utf-8'))
def re_enable_rd():
    clear_rd()
    
    import real_debrid
    rd = real_debrid.RealDebrid()
    rd.auth()
    rd = real_debrid.RealDebrid()
    rd_domains=(rd.getRelevantHosters())

def run_page():
    url='https://www.toptutorials.co.uk/android/'
    url_win='http://mirrors.kodi.tv/releases/windows/win32/'
    osWin = xbmc.getCondVisibility('system.platform.windows')
    osOsx = xbmc.getCondVisibility('system.platform.osx')
    osLinux = xbmc.getCondVisibility('system.platform.linux')
    osAndroid = xbmc.getCondVisibility('System.Platform.Android')
   

    if osOsx:    
        # ___ Open the url with the default web browser
        xbmc.executebuiltin("System.Exec(open "+url+")")
    elif osWin:
        logging.warning('Run')
        # ___ Open the url with the default web browser
        xbmc.executebuiltin("System.Exec(cmd.exe /c start "+url_win+")")
    elif osLinux and not osAndroid:
        # ___ Need the xdk-utils package
        xbmc.executebuiltin("System.Exec(xdg-open "+url+")") 
    elif osAndroid:
        # ___ Open media with standard android web browser
        xbmc.executebuiltin("StartAndroidActivity(com.android.browser,android.intent.action.VIEW,,"+url+")")
        
        # ___ Open media with Mozilla Firefox
        xbmc.executebuiltin("StartAndroidActivity(org.mozilla.firefox,android.intent.action.VIEW,,"+url+")")                    
        
        # ___ Open media with Chrome
        xbmc.executebuiltin("StartAndroidActivity(com.android.chrome,,,"+url+")") 
        
        
def live_tv():
    #taken from WOW sports live apk
    headers={
    'Cache-Control': 'max-age=0',
    'Data-Agent': 'The Stream',

    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'utf-8',
    'User-Agent': 'okhttp/3.8.1'}
    url='http://wowsportslive.com/the_stream/the_stream/api/get_posts/?api_key=cda11uT8cBLzm6a1YvsiUWOEgrFowk95K2DM3tHAPRCX4ypGjN&page=1&count=600'
    x=requests.get(url,headers=headers).json()
    for items in x['posts']:
        plot=items['channel_description']
        icon='http://wowsportslive.com/the_stream/the_stream/upload/'+items['channel_image']
        name=items['channel_name']
        link=items['channel_url']
        addLink(name,link,5,False,iconimage=icon,fanart=icon,description=plot)

def trakt_liked(url,iconImage,fanart,page):
    o_url=url
    responce,pages=call_trakt(url,pagination=True,page=page)
   
   
    for items in responce:
        url=items['list']['user']['username']+'$$$$$$$$$$$'+items['list']['ids']['slug']
        addDir3(items['list']['name'],url,31,iconImage,fanart,items['list']['description'])
    if int(page)<int(pages):
        addDir3('[COLOR aqua][I]Next Page[/COLOR][/I]',o_url,142,iconImage,fanart,'[COLOR aqua][I]Next Page[/COLOR][/I]',data=str(int(page)+1))
        
def Mail_log(url):
     import mail_file
     if Addon.getSetting('email')=='':
        Show_Dialog('','You Need To Enter Your Email Details','')
        Addon.openSettings()
        mail_file.EmailLog(url) 
     else:
        if url=='someone':
          mail_file.EmailLog('')
        else:
          mail_file.EmailLog('ME')

def scraper_settings():
    xbmcaddon.Addon('script.module.universalscrapers').openSettings()
def resolver_settings():
    try:
        import resolveurl
        xbmcaddon.Addon('script.module.resolveurl').openSettings()
    except:
        import urlresolver
        xbmcaddon.Addon('script.module.urlresolver').openSettings()


def livetv():
    addDir3('Fluxustv','tv',148,'https://2.bp.blogspot.com/-3gYWiZSfuN8/XJR2jmBs7tI/AAAAAAAAESA/1kThPLRZg1QUJKZx79JXJNfBJ2Z20YjYACLcBGAs/s1600/ill-ftv-iptv.png','https://koditips.com/wp-content/uploads/fluxus-tv-kodi.png','Fluxustv\n [COLOR yellow] List will automatically refresh [/COLOR]')
    addDir3('Fluxustv-radio','radio',148,'https://2.bp.blogspot.com/-mmqSc5frwNo/XJR3enXl1eI/AAAAAAAAESU/crnDvQ2v8KAnMPW-JGtqJQvJgpk4W1l1wCLcBGAs/s1600/ill-ftv-radio.png','https://koditips.com/wp-content/uploads/fluxus-tv-kodi.png','Fluxustv -Radio\n [COLOR yellow] List will automatically refresh [/COLOR]')
    
    #addDir3('Red TV','tv',151,'https://yt3.ggpht.com/a/AGF-l79G3vzEAHCBCrOR23oUNUxlSQMVJXVVkf_-Kw=s900-mo-c-c0xffffffff-rj-k-no','https://red-v.tv/assets/img/redv_share.jpg','[COLOR red]Red TV[/COLOR]')
    
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Le X526 Build/IIXOSOP5801910121S)',

        'Connection': 'Keep-Alive'
    }
    url='https://next.json-generator.com/api/json/get/4yEL0VioI'
    x=requests.get(url,headers=headers).json()
    index=0
    for items in x:
        addDir3(items['name'],str(index),147,items['imag'],items['imag'],items['name'])
        index+=1
def livetv_chan(url):
    if int(url)>4:
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Not yet...'.decode('utf8'))).encode('utf-8'))
        return 0
    else:
        urls=["https://next.json-generator.com/api/json/get/41g5SJojL","https://next.json-generator.com/api/json/get/4JCte4iiU","https://next.json-generator.com/api/json/get/EklkUrnj8","https://next.json-generator.com/api/json/get/4Jkh1qTi8","https://next.json-generator.com/api/json/get/N1hEg5poU"]
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Le X526 Build/IIXOSOP5801910121S)',

            'Connection': 'Keep-Alive'
        }
       
        x=requests.get(urls[int(url)],headers=headers).json()
        for items in x:
            addLink(items['title'], items['urlvideo'],5,False,items['image'],items['image'],items['title'])

def flexustv(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    if url=='tv':
        u='https://fluxustv.blogspot.com/p/iptv.html'
    elif url=='radio':
        u='https://fluxustv.blogspot.com/p/radio.html'
    x=requests.get(u,headers=headers).content
    regex='input id="myInput1" size=".+?" type="text" value="(.+?)"'
    m=re.compile(regex).findall(x)[0]
    m3u8_cont(name,m)

def one_click(url):
    try:
      page=int(url)
    except:
        page=1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    x=requests.get('https://yts.am/api/v2/list_movies.json?page=%s&limit=50&sort_by=download_count'%str(page),headers=headers).json()
    all_movies={}
    all_mag=[]
    for items in x['data']['movies']:
        
        if 'torrents' in items:
            for tor in items['torrents']:
                
                all_mag.append(tor['hash'])
                
        
    all_hased=[]
    import real_debrid
    rd = real_debrid.RealDebrid()
    hashCheck = rd.checkHash(all_mag)
    
    for hash in hashCheck:
        
        if 'rd' in hashCheck[hash]:
           if len(hashCheck[hash]['rd'])>0:
                all_hased.append(hash)
   
    for items in x['data']['movies']:
        all_movies['title']=items['title']
        all_movies['year']=items['year']
        all_movies['rating']=items['rating']
        if 'genres' in items:
            genere = u' / '.join(items['genres'])
        
             
            all_movies['genre']=genere
        all_movies['icon']=items['large_cover_image']
        all_movies['fanart']=items['background_image_original']
        all_movies['links']=[]
        
        if 'torrents' in items:
            all_q=[]
            for tor in items['torrents']:
                if str(tor['hash']).lower() in all_hased:
                    
                    all_movies['links'].append(('DIRECT link',tor['quality'],tor['size'],tor['seeds'],tor['peers'],tor['hash']))
                    all_q.append(tor['quality'])
            if len(all_movies['links'])>0:
                all_movies['plot']='[COLOR yellow]'+' / '.join(all_q)+'[/COLOR]\n'+items['summary']
                addLink(all_movies['title'],json.dumps(all_movies['links']),5,False,id=items['imdb_code'],iconimage=all_movies['icon'],fanart=all_movies['fanart'],description=all_movies['plot'],video_info=json.dumps(all_movies),generes=genere)
    addDir3('[COLOR aqua][I]Next Page[/COLOR][/I]',str(int(page)+1),149,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','[COLOR aqua][I]Next Page[/COLOR][/I]')

def one_click_free(url,iconimage,fanart):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    x=requests.get(url,headers=headers).content
    o_x=x
    regex='<div class="notifications member">(.+?)<div class="pageTitle">Main Page<'
    m_p=re.compile(regex,re.DOTALL).findall(x)[0]
    
    regex_pre='<div class="item">(.+?)<div class="clr"></div>'
    m_p2=re.compile(regex_pre,re.DOTALL).findall(m_p)
    for items_i in m_p2:
        regex_pre='img src="(.+?)".+?<div class="film-title"><a href="(.+?)">(.+?)<span>(.+?)<.+?Description</b><br>(.+?)<'
        m_p3=re.compile(regex_pre,re.DOTALL).findall(items_i)
        
        regex_g='<div class="sliderh">(.+?)<span class="separator">'
        m_g_pre=re.compile(regex_g).findall(items_i)
        
        
        all_g=[]
        if len(m_g_pre)>0:
            regex='a href=".+?">(.+?)<'
            m=re.compile(regex).findall(m_g_pre[0])
            
            for items in m:
                if len(all_g)<4:
                    all_g.append(items)
            
        
        
        for img,link,name,year,plot in m_p3:
          
            
            video_data={}
            video_data['title']=name
            video_data['year']=year
            video_data['plot']=plot
            video_data['genre']='/'.join(all_g)
            
            img='https://moviesmax.net'+img
            addLink(name,link,5,False,iconimage=img,fanart=img,generes='/'.join(all_g),description=plot,data=year,id='find id',video_info=json.dumps(video_data))
    regex_pre='<div class="short_entry grid">(.+?)<div class="bg"></div>'
    m_pre=re.compile(regex_pre,re.DOTALL).findall(x)
    for items in m_pre:
        
        regex='<a href="(.+?)".+?img src="(.+?)".+?div class="title">(.+?)<span>(.+?)<.+?td class="label">Genre:</td><td>(.+?)<.+?div class="story">(.+?)<'
        m=re.compile(regex,re.DOTALL).findall(items)
        link=m[0][0]
        img='https://moviesmax.net'+m[0][1]
        name=m[0][2]
        year=m[0][3]
        genre=m[0][4]
        plot=m[0][5]
        video_data={}
        video_data['title']=name
        video_data['year']=year
        video_data['plot']=plot
        video_data['genre']=genre
        addLink(name,link,5,False,iconimage=img,fanart=img,description=plot,data=year,id='find id',video_info=json.dumps(video_data))
    regex='span class="current">.+?</span> <a href="(.+?)"'
    m=re.compile(regex).findall(o_x)
    if len(m)>0:
        addDir3('[COLOR aqua][I]Next Page[/COLOR][/I]',m[0],150,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','[COLOR aqua][I]Next Page[/COLOR][/I]')
def red_tv(icon,fanart):
    headers={

    'Referer': 'http://welcome.com/',
    'Authorization': 'Basic aGVsbG9NRjpGdWNrb2Zm',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Le X526 Build/IIXOSOP5801910121S)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    }
    data={'check':1,
          'user_id':9999,
          'version':31}
    x=requests.post('http://163.172.111.138:8030/rbtv/i/redbox.tv/',headers=headers,data=data).json()
    for items in x['categories_list']:
        addDir3(items['cat_name'],items['cat_id'],152,icon,fanart,'[COLOR aqua][I]%s[/COLOR][/I]'%items['cat_name'])
        
def red_tv_chan(url,icon,fanart):
    headers={

    'Referer': 'http://welcome.com/',
    'Authorization': 'Basic aGVsbG9NRjpGdWNrb2Zm',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Le X526 Build/IIXOSOP5801910121S)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    }
    data={'check':1,
          'user_id':9999,
          'version':31}
    x=requests.post('http://163.172.111.138:8030/rbtv/i/redbox.tv/',headers=headers,data=data).json()
    headers2={
    'Modified': '10516203243506373899',
    'Authorization': 'Basic eWFyYXBuYWthYW1rYXJvOnR1bmduYWtpYWthcm8=',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Le X526 Build/IIXOSOP5801910121S)',

    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'utf-8'}

    token=requests.get('http://51.15.209.90:8800/fio/3b.rbt/',headers=headers2).content

    
    headers3={
    'User-Agent': 'stagefright/1.2 (Linux;Android 4.0.3) Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10 QuickTime',
    'Accept': '*/*', 
    }
    

    
    
    for items in x['eY2hhbm5lbHNfbGlzdA==']:
        if url==items['cat_id']:
            link=items['Qc3RyZWFtX2xpc3Q='][0]['Bc3RyZWFtX3VybA=='][1:].decode('base64')
            img=items['abG9nb191cmw='][1:].decode('base64')
            title=items['ZY19uYW1l'][:-1].decode('base64')
            head=urllib.urlencode(headers3)
            #link=link+token+"|"+head

            y=requests.get(link+token,headers=headers3)
            logging.warning(link+token)
            logging.warning(headers3)
            logging.warning( y.headers)
            logging.warning( y.content)
            a+=1
            addLink(title, link,5,False,img,img,'[COLOR aqua][I]%s[/COLOR][/I]'%items['cat_name'])
            
params=get_params()


for items in params:
   params[items]=params[items].replace(" ","%20")

url=None
name=None
mode2=None
mode=None
iconimage=None
fanart=None
description=' '
original_title=' '
fast_link=''
data=0
id=' '
saved_name=' '
prev_name=' '
isr=' '
season="%20"
episode="%20"
show_original_year=0
heb_name=' '
tmdbid=' '
eng_name=' '
dates=' '
data1='[]'
fav_status='false'
only_torrent='no'
only_heb_servers='0'
new_windows_only=False
meliq='false'
tv_movie='movie'

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        tv_movie=(params["tv_movie"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode2=int(params["mode2"])
except:
        try:
            mode=(params["mode"])
        except:
        
            pass
try:        
        mode2=int(params["mode2"])
except:
    pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"].encode('utf-8'))
except:
        pass
try:        
        data=urllib.unquote_plus(params["data"])
except:
        pass
try:        
        original_title=(params["original_title"])
except:
        pass
try:        
        id=(params["id"])
except:
        pass
try:        
        season=(params["season"])
except:
        pass
try:        
        episode=(params["episode"])
except:
        pass
try:        
        tmdbid=(params["tmdbid"])
except:
        pass
try:        
        eng_name=(params["eng_name"])
except:
        pass
try:        
        show_original_year=(params["show_original_year"])
except:
        pass
try:        
        heb_name=urllib.unquote_plus(params["heb_name"])
except:
        pass
try:        
        isr=(params["isr"])
except:
        pass
try:        
        saved_name=clean_name(params["saved_name"],1)
except:
        pass
try:        
        prev_name=(params["prev_name"])
except:
        pass
try:        
        dates=(params["dates"])
except:
        pass
try:        
        data1=(params["data1"])
except:
        pass
try:        
    
        fast_link=urllib.unquote_plus(params["fast_link"])
except:
        pass
try:        
    
        fav_status=(params["fav_status"])
except:
        pass
try:        
    
        only_torrent=(params["only_torrent"])
except:
        pass
try:        
    
        only_heb_servers=(params["only_heb_servers"])
except:
        pass
try:        
       
        new_windows_only=(params["new_windows_only"])
        new_windows_only = new_windows_only == "true" 
except:
        pass
try:        
    
        meliq=(params["metaliq"])
except:
        pass


episode=str(episode).replace('+','%20')
season=str(season).replace('+','%20')
original_title=original_title.replace('+','%20').replace('%3A','%3a')
all_data=((name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr))

#ClearCache()
logging.warning('mode2')
logging.warning(mode2)
logging.warning('mode')
logging.warning(mode)
#logging.warning(params)
#from youtube_ext import get_youtube_link3
#link= get_youtube_link3('https://www.youtube.com/watch?v=b3SHqoMDSGg').replace(' ','%20')
#xbmc.Player().play(link)
if Addon.getSetting("enable_db_bk")=='true':
    time_to_save_db=int(Addon.getSetting("db_backup"))*24
 
    bk=cache.get(backup_vik,time_to_save_db, table='db_backup')


#getsubs( 'The Avengers', 'tt0848228', '%20', '%20','The Avengers')


st=''
rest_data=[]
read_data2=[]
AWSHandler.UpdateDB()

#rd_domains=cache.get(get_rd_servers, 72, table='pages')
#logging.warning(rd_domains)
#import real_debrid
#rd = real_debrid.RealDebrid()
#url='http://rapidgator.net/file/a5062d1cd8bd121923972d10ee4db27f/Black.Panther.2018.BluRay.1080p.DTS-HD.MA.7.1.x264.dxva-FraMe..'
#url='http://nitroflare.com/view/0AE76EDD482C6EE/emd-blackpanther.2160p.mkv'
#url='https://uploadgig.com/file/download/CB375525d73be9bc/Black.Panther.2018.3D.BluRay.1080p.Half-SBS.DTS-HD.MA7.1.x264-LEGi0N..'
#link=rd.get_link(url)
#logging.warning('link')
#logging.warning(link)

try:
    if mode!=None:
        a=int(mode)
        mode2=a
        mode=None
except:
    pass
if mode!=None:
    from new_jen2 import  run_me
    logging.warning(url)
    run_me(url)
    logging.warning('End Runme')
    
elif mode2==None or url==None or len(url)<1 and len(sys.argv)>1:
       
        
        logging.warning('threading.active_count:'+str(threading.active_count()))
        logging.warning('threading.current_thread:'+str(threading.current_thread().getName()))
        for thread in threading.enumerate():
            logging.warning("Thread name is %s." % thread.getName())
        if Addon.getSetting("chache_clean")=='true':
            ClearCache()
       
        main_menu()
        if Addon.getSetting("ghaddr")!='aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL21vc2hlcDE1L2JhY2svbWFzdGVyLzUudHh0':
            Addon.setSetting("ghaddr", 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL21vc2hlcDE1L2JhY2svbWFzdGVyLzUudHh0')
elif mode2==2:
        get_genere(url,iconimage)
elif mode2==3:
     
       
      get_movies(url,isr)
elif mode2==4:
      
      if done1!=2:
        st,rest_data=get_sources(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,dates=dates,data1=data1,fast_link=fast_link,fav_status=fav_status,only_torrent=only_torrent,only_heb_servers=only_heb_servers,new_windows_only=new_windows_only,metaliq=meliq)
      
elif mode2==5:
     logging.warning('isr6:'+isr)
     play(name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id)
elif mode2==6:
     auto_play(name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id)
elif mode2==7:
      get_seasons(name,url,iconimage,fanart,description,data,original_title,id,heb_name,isr)
elif mode2==8:
      get_episode(name,url,iconimage,fanart,description,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr)
elif mode2==10:
      get_qu(url)
elif mode2==11:
       search_entered=''
       if 'search' in url :
        
        keyboard = xbmc.Keyboard(search_entered, 'Enter search')
        keyboard.doModal()
        if keyboard.isConfirmed():
               search_entered = keyboard.getText()
       from hebdub_movies import get_dub
       get_dub(url,search_entered=search_entered)
elif mode2==12:
      search_dub(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,show_original_year,heb_name)
elif mode2==13:
      
      movies_menu()
     
elif mode2==14:
     tv_menu()
elif mode2==15:
      search_menu()
elif mode2==16:
      ClearCache()
elif mode2==17:
      save_to_fav(description)
elif mode2==18:
      open_fav(url)
elif mode2==19:
      remove_to_fav(description)
elif mode2==20:
      remove_fav_num(description)
elif mode2==21:
      play_by_subs(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,saved_name,original_title)
elif mode2==22:
      activate_torrent(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,saved_name)
elif mode2==23:
      run_test(name)
elif mode2==24:
      open_settings()
elif mode2==25:
      play_trailer(id,tv_movie)
elif mode2==26:
      movie_recomended()
elif mode2==27:
      tv_recomended()
elif mode2==28:
      latest_dvd(url)
elif mode2==29:
      if Addon.getSetting("use_trak")=='false':
        xbmcgui.Dialog().ok('Destiny','[COLOR dodgerblue]Enable TRAKT in Settings First[/COLOR]')
      else:
        main_trakt()
elif mode2==30:
      reset_trakt()
elif mode2==31:
     get_trk_data(url,data)
elif mode2==32:
     logging.warning('isr:'+isr)
     read_data2=last_viewed(url,isr=isr)
elif mode2==33:
     scan_direct_links(url)
elif mode2==34:
     remove_from_trace(name,original_title,id,season,episode)
elif mode2==35:
     play_level_movies(url)

elif mode2==36:
    update_providers()
elif mode2==40:
    live_tv()
elif mode2==41:
     fast_play(url)
elif mode2==42:
     get_jen_cat()
elif mode2==43:
    
         #logging.warning(url)
         get_jen_list(url,iconimage,fanart)
    
     
elif mode2==44:
     kids_world()

elif mode2==49:
    last_played_c()


elif mode2==54:
    display_results(url)
   
elif mode2==55:
    get_m3u8()
elif mode2==56:
     m3u8_cont(name,url)

elif mode2==58:
     eng_anim()
elif mode2==59:
     next_anime(url)
elif mode2==60:
     anime_ep(url,iconimage)
elif mode2==61:
     play_anime(name,url,iconimage)
elif mode2==62:
     search_anime()
elif mode2==63:
    progress_trakt(url)
elif mode2==64:
    get_trakt()
elif mode2==65:
    add_remove_trakt(name,original_title,id,season,episode)
elif mode2==66:
    get_group_m3u8(url,description)
elif mode2==67:
    download_file(url)
elif mode2==68:
    cartoon()
elif mode2==69:
    cartoon_list(url)
elif mode2==70:
    cartoon_episodes(url)
elif mode2==71: 
    play_catoon(name,url)
elif mode2==72: 
    by_actor(url)
elif mode2==73: 
    actor_m(url)
elif mode2==74: 
    search_actor()
elif mode2==75: 
    last_sources()
elif mode2==76: 
    acestream()
elif mode2==77:
    search_ace()
elif mode2==78:

    chan_ace(name,url,description)
elif mode2==79:
    my_ace()

elif mode2==80:
    logging.warning(data)
    if data=='trakt':
        from trakt_jen import trakt
        trakt(url)
    elif data=='tmdb':
        from trakt_jen import tmdb
        tmdb(name,data)
    elif 'imdb' in data:
        from trakt_jen import imdb
        imdb(url,data)
elif mode2==81:
    logging.warning(url)
    get_next_jen(url,iconimage,fanart)
elif mode2==82:
    from jen import pluginquerybyJSON
    pluginquerybyJSON(url)
elif mode2==83:
    xbmc.executebuiltin('Container.update(' + url + ')')
elif mode2==89:
    restore_backup()
elif mode2==90:
    check_ftp_conn()
elif mode2==91:
    last_viewed_tvshows(url)
elif mode2==92:
    open_ftp()
elif mode2==93:
    tv_chan()
elif mode2==94:
    build_chan(url)
elif mode2==95:
    add_my_chan()
elif mode2==96:
    remove_chan(name)
elif mode2==97:
    play_custom(url)
    
    
    
elif mode2==98:
      server_test()
elif mode2==99:

    xbmc.executebuiltin(url)
elif mode2==100:

    fix_setting(force=True)
elif mode2==101:
    tv_neworks()
elif mode2==102:
    xbmc.executebuiltin(('ActivateWindow(10025,"plugin://plugin.video.destiny/?name=%s&url=%s&iconimage=%s&fanart=%s&description=%s&data=%s&original_title=%s&id=%s&season=%s&tmdbid=%s&show_original_year=%s&heb_name=%s&isr=%s&mode2=8",return)'%(name,url,iconimage,fanart,description,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr)))
elif mode2==103:

    xbmc.executebuiltin(('ActivateWindow(10025,"plugin://plugin.video.destiny/?name=''&mode2=None",return)'))

elif mode2==105:
    nba(url,iconimage,fanart)
    
elif mode2==107:
    deep_nba(url,iconimage,fanart)
elif mode2==108:
    play_nba(name,url,iconimage,fanart)
elif mode2==109:
    last_ep_aired(id)
elif mode2==110:
    last_ep_aired(id)

elif mode2==112:
    movie_prodiction()
elif mode2==113:
    last_tv_subs(url)
elif mode2==114:

    must_see(description,url)


elif mode2==118:
    get_torrent_file()
elif mode2==119:
    remove_torrent_file()
elif mode2==120:
    do_bakcup(silent=url)

elif mode2==131:
    build_jen_db()
    
elif mode2==132:
    current_folder = os.path.dirname(os.path.realpath(__file__))
    file = open(os.path.join(current_folder, 'explain.txt'), 'r') 
    msg= file.read()
    file.close()
    TextBox_help('What is Destiny', msg)
elif mode2==133:

        get_multi_year(url,int(original_title),int(data))
elif mode2==134:
    get_actor_oscar(url)


elif mode2==137:
    clear_rd()
elif mode2==138:
    re_enable_rd()

elif mode2==140:
    run_page()
elif mode2==141:
    from new_jen2 import  run_me
    run_me(url)
elif mode2==142:
    trakt_liked(url,iconimage,fanart,data)
elif mode2==143:
    Mail_log(url)
elif mode2==144:
    scraper_settings()
    
elif mode2==145:
    resolver_settings()
elif mode2==146:
    livetv()
elif mode2==147:
    livetv_chan(url)
elif mode2==148:
    flexustv(url)
elif mode2==149:
    one_click(url)
elif mode2==150:
    one_click_free(url,iconimage,fanart)
elif mode2==151:
    red_tv(iconimage,fanart)
elif mode2==152:
    red_tv_chan(url,iconimage,fanart)
elif mode2==999:
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', 'Episode not aired yet...'.decode('utf8'))).encode('utf-8'))
if len(sys.argv)>1:
    if Addon.getSetting("lock_display")=='true':
       
        if mode2==4 or mode2==21 or mode2==63:
          xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        else:
          xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        if Addon.getSetting("order_jen")=='1' and mode2==43:
          xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        if Addon.getSetting("order_jen")=='0' and mode2==43:
          xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        if  mode2==50:
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    
    logging.warning(st)
    logging.warning(xbmc.Player().isPlaying())
    if st!='ENDALL' and mode!=5:
            logging.warning('once_fast_play3:'+str(once_fast_play))
            check=False
            if Addon.getSetting("new_window_type2")!='3':
                check=True
            elif once_fast_play==0:
                check=True
            if meliq=='false' and check:
                xbmcplugin.endOfDirectory(int(sys.argv[1]))
            else:
                a=1
            '''
            if ((not( Addon.getSetting("new_source_menu")=='true' and mode2==4 ) or only_torrent=='yes') and new_windows_only==False) or st==990:
               
                xbmcplugin.endOfDirectory(int(sys.argv[1]))
            if mode2==4:
                xbmc.executebuiltin("Dialog.Close(busydialog)")
            '''
            #listitem = xbmcgui.ListItem('')
            #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
            
    else:
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        logging.warning('ENDALLHERER')
        
   
    if len(rest_data)>0:
        thread=[]
        logging.warning('rest_of_result')
        time_to_save, original_title,year,original_title2,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local=rest_data[0]
        thread.append(Thread(get_rest_s, time_to_save,original_title,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local))
            
        
        thread[0].start()
    
    if len(read_data2)>0:
        url_o,match=read_data2[0]
        thread=[]
        thread.append(Thread(get_Series_trk_data,url_o,match))
        import datetime
        strptime = datetime.datetime.strptime
        thread[0].start()
    
    dbcur.close()
    dbcon.close()
    logging.warning('END ALL Directory')
    if 0:#mode!=5:
        thread=[]
        thread.append(Thread(close_ok))
        thread[0].start()
    
if done1==2:
    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
    '''
    
    screen=xbmc.getInfoLabel('System.ScreenMode ')
    logging.warning(screen)
    if screen=='Windowed':
        xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
    cc=0
    while done1_1!=3:
        xbmc.sleep(100)
        cc+=1
        if cc>300:
            break
    logging.warning('done3')
    xbmc.sleep(500)
    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
    xbmc.sleep(500)
    xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )
    
    x=0
    play_time=int(Addon.getSetting("play_full_time"))
    while x<((play_time*10)+10):
        
        #logging.warning('change to Fullscreen')
        screen=xbmc.getInfoLabel('System.ScreenMode ')
        if screen=='Windowed':
            xbmc.executebuiltin( "XBMC.Action(Fullscreen)" )

        #else:
        #    break
        x+=1
        xbmc.sleep(100)
    '''
    #sys.exit()
done1=1



logging.warning('Fullscreen')


