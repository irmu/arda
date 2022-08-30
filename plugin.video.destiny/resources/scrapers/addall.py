# -*- coding: utf-8 -*-

import sys,xbmcplugin,xbmcgui,urllib,os,json,logging
from globals import dbcur,Addon,user_dataDir,save_file,win_system,AWSHandler
def addNolink( name, url,mode,isFolder, iconimage="DefaultFolder.png",fanart="DefaultFolder.png",description=' '):
 

          
         
          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode2="+str(mode)+"&name="+(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name),'plot':description   })
          art = {}
          art.update({'poster': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","false")
          liz.setProperty( "Fanart_Image", fanart )
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
###############################################################################################################        

def addDir3(name,url,mode,iconimage,fanart,description,video_info={},data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr='0',generes=' ',trailer=' ',dates=' ',watched='no',fav_status='false',collect_all=False):
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
          
           url=url.encode('utf8')
           te1=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode2="+str(mode)
            
           te2="&name="+(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description.encode('utf8'))+"&heb_name="+(heb_name)+"&dates="+(dates)
           te3="&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)
           te4="&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)
        
           u=te1 + te2 + te3 + te4.decode('utf8')+"&fav_status="+fav_status
 
        ok=True
        video_data={}
        video_data['title']=original_title
        if episode!=' ' and episode!='%20' and episode!=None:
          video_data['mediatype']='tvshow'
          video_data['TVshowtitle']=original_title
          video_data['Season']=int(str(season).replace('%20','0'))
          video_data['Episode']=int(str(episode).replace('%20','0'))
          tv_show='tv'
        else:
           video_data['mediatype']='movies'
           video_data['TVshowtitle']=''
           video_data['tvshow']=''
           video_data['season']=0
           video_data['episode']=0
           tv_show='movie'
        video_data['OriginalTitle']=original_title
        if data!=' ':
            try:
                a=int(data)
                video_data['year']=data
            except:
                pass
        if generes!=' ':
            video_data['genre']=generes
        video_data['rating']=str(rating)
    
        video_data['poster']=fanart
        video_data['plot']=description.replace('%27',"'")
        if trailer!=' ':
            video_data['trailer']=trailer
        menu_items=[]

        if watched=='yes':
          video_data['playcount']=1
          video_data['overlay']=7

        str_e1=list(u.encode('utf8'))
        for i in range(0,len(str_e1)):
           str_e1[i]=str(ord(str_e1[i]))
        str_e='$$'.join(str_e1)
        file_data=[]
        change=0

        if os.path.exists(save_file):
            f = open(save_file, 'r')
            file_data = f.readlines()
            f.close()
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s'"%(original_title.replace("'"," ").replace(" ","%20").replace(':','%3a').replace("'",'%27')))

        match = dbcur.fetchone()
        if match!=None:
        
          menu_items.append(('[COLOR peru][I]Remove from series tracker[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&original_title=%s&mode2=34&name=%s&id=0')%(sys.argv[0],original_title,name)))
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s'  AND season='%s' AND episode = '%s'"%(original_title.replace("'"," ").replace(" ","%20").replace(':','%3a').replace("'",'%27'),season,episode))
     
        match = dbcur.fetchone()
        if match!=None:
        
          menu_items.append(('[COLOR pink][I]Remove watched[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&original_title=%s&mode2=34&name=%s&id=1&season=%s&episode=%s')%(sys.argv[0],original_title,name,season,episode))) 
        if str_e+'\n' not in file_data:
           menu_items.append(('[COLOR lightblue][I]Clear cache[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&description=%s&mode2=16')%(sys.argv[0],str_e)))
          
        if str_e+'\n' not in file_data:
           menu_items.append(('[COLOR lightblue][I]Add to my favorites[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&description=%s&mode2=17')%(sys.argv[0],str_e)))
           
        else:
           
           menu_items.append(('[COLOR red][I]Remove from my favorites[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&description=%s&mode2=19')%(sys.argv[0],str_e)))
        if mode==7:
            menu_items.append(('[I]Open last episode Aired[/I]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&mode2=109&id=%s')%(sys.argv[0],id)))
        if Addon.getSetting("use_trak")=='true' and len(id)>1:
            
            
              
              menu_items.append(('[I]watched with Trakt[/I]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&original_title=add&mode2=65&name=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],tv_show,id,season,episode))) 
            
              menu_items.append(('[I]Not watched with Trakt[/I]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&original_title=remove&mode2=65&name=%s&id=%s&season=%s&episode=%s')%(sys.argv[0],tv_show,id,season,episode))) 
        menu_items.append(('Details', 'Action(Info)'))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(menu_items, replaceItems=False)
        if video_info!={}:
            
            video_data=video_info
            
        if 'fast' not in video_info:
            info = {'title': id, 'season': season, 'episode': episode}
            
            res = AWSHandler.CheckWS(info)
            if res:
                if res['wflag']:
                    #listitem.setInfo(type = 'video', infoLabels = {'playcount': 1, 'overlay': 5})
                    video_data['playcount']=1
                    video_data['overlay']=5
            if res:
                if not res['wflag']:
                  if res['resumetime']!=None:
                    liz.setProperty('ResumeTime', res['resumetime'])
                    liz.setProperty('TotalTime', res['totaltime'])
        liz.setProperty( "Fanart_Image", fanart )
        art = {}
        art.update({'poster': iconimage})
        liz.setArt(art)
        video_data['title']=video_data['title'].replace("|",' ')
        video_data['plot']=video_data['plot'].replace("|",' ')
  
        
        if mode==4 and Addon.getSetting("new_source_menu")=='true' and  Addon.getSetting("new_window_type2")!='3':
            liz.setProperty("IsPlayable","true")
            isfolder=False
            video_data['title']=name
        else:
            isfolder=True
        logging.warning('F_type:'+str(isfolder))
        
        liz.setInfo( type="Video", infoLabels=video_data)
        if collect_all:
            return u,liz,True
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isfolder)
        
        return ok



def addLink( name, url,mode,isFolder, iconimage,fanart,description,video_info={},data='',original_title=' ',id=' ',season=' ',episode=' ',rating=0,saved_name=' ',prev_name=' ',eng_name=' ',heb_name=' ',show_original_year=' ',generes=' ',num_in_list=None,dont_earse=False,collect_all=False,isr='0'):
          #url=url.encode('utf8')
          
          name=name.replace("|",' ')
          description=description.replace("|",' ')
          try:
            name=urllib.unquote(name)
          except:
            pass
          name=name
          
          description=description
          name=name
          description=description
          
          te1=sys.argv[0]+"?url="+urllib.quote_plus(url.encode('utf8'))+"&mode2="+str(mode)
          
          te2="&name="+(name)+"&iconimage="+urllib.quote_plus(iconimage.encode('utf8'))+"&fanart="+urllib.quote_plus(fanart.encode('utf8'))+"&description="+(description)+"&heb_name="+(heb_name)
          te3="&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)
          te4="&episode="+str(episode)
        
       
          u=sys.argv[0]+"?url="+urllib.quote_plus(url.encode('utf8'))+"&mode2="+str(mode)+"&name="+(name)+"&data="+str(data)+"&iconimage="+urllib.quote_plus(iconimage.encode('utf8'))+"&fanart="+urllib.quote_plus(fanart.encode('utf8'))+"&description="+(description)+"&original_title="+(original_title)+"&id="+str(id)+"&season="+str(season)+"&episode="+str(episode)+"&saved_name="+str(saved_name)+"&prev_name="+str(prev_name)+"&eng_name="+str(eng_name)+"&heb_name="+(heb_name)+"&show_original_year="+str(show_original_year)+"&isr="+str(isr)
          

          info = {'title': id, 'season': season, 'episode': episode}
          #res = AWSHandler.CheckWS(info)
          
          menu_items=[]
          
          video_data={}
          video_data['title']=name
          video_data['season']=season
          video_data['episode']=episode
          video_data['poster']=fanart
          video_data['plot']=description.replace('%27',"'")
          video_data['genre']=generes
          video_data['year']=show_original_year
          if rating!=0:
            video_data['rating']=str(rating)
          #video_data['playcount']=1
          if 0:
            if res['wflag']:
                #listitem.setInfo(type = 'video', infoLabels = {'playcount': 1, 'overlay': 5})
                video_data['playcount']=1
                video_data['overlay']=5
            
          
          #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode2="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
          if video_info!={}:
            #if type(video_data) is dict:
            #  video_data=video_info
            #else:
            video_data=json.loads(video_info)
          video_data['title']=video_data['title'].replace("|",' ')
          video_data['plot']=video_data['plot'].replace("|",' ')
          liz.setInfo(type="Video", infoLabels=video_data)
        
          art = {}
          art.update({'poster': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )

          if 0:
            if not res['wflag']:
           
                liz.setProperty('ResumeTime', '0')
                liz.setProperty('TotalTime', '1')
          if dont_earse==False:
              liz.setProperty('ResumeTime', '0')
              liz.setProperty('TotalTime','1')
          if num_in_list=='remove':
             menu_items.append(('Remove my channel', 'XBMC.RunPlugin(%s)' % ('%s?url=www&name=%s&mode2=96')%(sys.argv[0],name)))
          elif num_in_list!=None:
             menu_items.append(('[COLOR red][I]Remove from my favorites[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&description=%s&mode2=20')%(sys.argv[0],num_in_list)))
          if win_system:
            menu_items.append(('[I]Download with IDM[/I]', 'XBMC.RunPlugin(%s)' % ('%s?url=%s&mode2=67')%(sys.argv[0],url)))
          if '127.0.0.1:6878' in url:
             menu_items.append(('Add to my acestream', 'XBMC.RunPlugin(%s)' % ('%s?url=%s&description=add&name=%s&mode2=78')%(sys.argv[0],urllib.quote_plus(url),name)))
             menu_items.append(('Remove from my acesteam', 'XBMC.RunPlugin(%s)' % ('%s?url=%s&description=remove&name=%s&mode2=78')%(sys.argv[0],urllib.quote_plus(url),name)))
          liz.addContextMenuItems(menu_items, replaceItems=False)
          if collect_all:
            return u,liz,isFolder
          
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)

          