# -*- coding: utf-8 -*-
import re,time,os,xbmcaddon,xbmc,xbmcplugin,sys,urllib,xbmcgui,logging
from globals import dbcur,Addon,user_dataDir,requests
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")

done_dir = os.path.join(addonPath, 'resources', 'done')
sys.path.append( done_dir)
import pyxbmct
from general import call_trakt
import threading
global all_d

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
all_d=[]
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
if KODI_VERSION>=17:
 
  domain_s='https://'
elif KODI_VERSION<17:
  domain_s='http://'

#from general import domain_s
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
cacheFile2 = os.path.join(user_dataDir, 'lastsubs.db')
cacheFile = os.path.join(user_dataDir, 'cache_play.db')


class Thread(threading.Thread):
    def __init__(self, target, *args):
       
        self._target = target
        self._args = args
        
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        self._target(*self._args)
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
                                
from addall import addNolink,addDir3,addLink
class A(object):
    pass
class new_movies(pyxbmct.AddonDialogWindow):
    
    def __init__(self, title='',item=[]):
        ACTION_ENTER=13
        ACTION_MOUSE_LEFT_CLICK = 100
        ACTION_MOUSE_RIGHT_CLICK = 101
        super(new_movies, self).__init__(title)
        self.item=item
        item_l=len(item)+1
        if len(item)<6:
            leng=(1000/4)
            wid=(700/5)*item_l
            leng=700
            wid=1000
            col=item_l
            row=1
        else:
            
            row_ln=int(item_l / 5) + (item_l % 5 > 0)
            
            leng=(700/4)*row_ln
            wid=1000
            col=5
            row=row_ln
        self.setGeometry(wid, leng,row, col)
        self.list_index=-1

        
        
        self.set_active_controls()
        self.set_navigation()
       
        # Connect control to close the window.
        
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
   
       

    def function_builder(self,args):
        def function():
            
           
            self.list_index=args
            self.close()
        return function
    def get_selection(self):
        return self.list_index
    def click_c(self):
        
        self.list_index=-1
        self.close()
    def set_active_controls(self):
        my_dynamic_functions = {}
        self.button={}
        # List
        i=0
        j=0
        x=0
        for img in self.item:
            self.image = pyxbmct.Image(img)
            self.placeControl(self.image, i, j, rowspan=1, columnspan=1)
            self.button[x] = pyxbmct.Button('')
            
            my_dynamic_functions['button_'+str(x)] = self.function_builder(x)

            self.connect(self.button[x], my_dynamic_functions['button_'+str(x)])
            self.placeControl(self.button[x], i, j)
            j+=1
            if j>4:
              j=0
              i+=1
            #self.connect(self.image, self.close)
            
            x+=1
        self.image = pyxbmct.Image('http://www.cling.co.il/wp-content/uploads/2016/06/%D7%A1%D7%92%D7%95%D7%A8.jpg')
        self.placeControl(self.image, i, j, rowspan=1, columnspan=1)
        self.button2 = pyxbmct.Button('')
        self.connect(self.button2, self.click_c)
        self.placeControl(self.button2, i, j)
        
       

    def set_navigation(self):
        if len(self.button)>1:
            for x in range(0,len(self.button)-1):
              self.button[x].controlDown(self.button[x+1])
              self.button[x+1].controlUp(self.button[x])
              
              self.button[x].controlRight(self.button[x+1])
              self.button[x+1].controlLeft(self.button[x])
             
            self.button[x+1].controlRight(self.button2)
            self.button[x+1].controlDown(self.button2)
        
            self.button2.controlLeft(self.button[x+1])
            self.button2.controlUp(self.button[x+1])
        
        self.button2.controlRight(self.button[0])
        self.button2.controlDown(self.button[0])
        
        self.button[0].controlLeft(self.button2)
        self.button[0].controlUp(self.button2)
          
        self.setFocus(self.button2)

    

    

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=50',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=50',)])
def get_tmdb_data(new_name_array,html_g,fav_search_f,fav_servers_en,fav_servers,google_server,rapid_server,direct_server,heb_server,url,isr,xxx):
           global all_d
           if Addon.getSetting("use_trak")=='true':
               i = (call_trakt('/users/me/watched/movies'))
               all_movie_w=[]
               for ids in i:
                  all_movie_w.append(str(ids['movie']['ids']['tmdb']))
           dbcon = database.connect(cacheFile)
           dbcur = dbcon.cursor()

           html=requests.get(url).json()
           for data in html['results']:
             
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
               year=str(data['first_air_date'].split("-")[0])
             else:
                year=str(data['release_date'].split("-")[0])
             if data['overview']==None:
               plot=' '
             else:
               plot=data['overview']
             if 'title' not in data:
               tv_movie='tv'
               new_name=data['name']
             else:
               tv_movie='movie'
               new_name=data['title']
              
                
             f_subs=[]
             if 'original_title' in data:
               original_name=data['original_title']
               mode=4
               
               id=str(data['id'])
              
               if data['original_language']!='en':
                
                html2=requests.get('http://api.themoviedb.org/3/movie/%s?api_key=1248868d7003f60f2386595db98455ef'%id).json()
                original_name=html2['title']
                
               
             else:
               original_name=data['original_name']
               id=str(data['id'])
               mode=7
               
               if data['original_language']!='en':
                
                    html2=requests.get('http://api.themoviedb.org/3/tv/%s?api_key=1248868d7003f60f2386595db98455ef'%id).json()
                    
                    original_name=html2['name']
               
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

             trailer = "plugin://plugin.video.destiny?mode2=25&url=www&id=%s&tv_movie=%s" % (id,tv_movie)
            
             if new_name not in new_name_array:
              new_name_array.append(new_name)
             
              color='white'
              start_time = time.time()
              
              dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' AND type='%s' "%(original_name.replace("'"," ").replace(" ","%20").replace(':','%3a').replace("'",'%27'),'movie'))

              match = dbcur.fetchone()

              if match!=None:
                
                color='magenta'
              
              
              
              elapsed_time = time.time() - start_time
              
              
              if  Addon.getSetting("disapear")=='true' and color=='red' and mode!=7:
                a=1
              else:
                if mode==7:
                  color='white'
                  dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s'"%(urllib.quote_plus(original_name.encode('utf8')).replace("+","%20")))
                 
                  match = dbcur.fetchone()

                  if match!=None:
                    color='orange'
                watched='no'
                if Addon.getSetting("use_trak")=='true':
                    if id in all_movie_w:
                        watched='yes'
                if  mode==4 and fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 or heb_server=='true' or google_server=='true' or rapid_server=='true' or direct_server=='true'):
                
                    fav_status='true'
                else:
                    fav_status='false'
            
                
                all_d.append(('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx))
           dbcur.close()
           dbcon.close()
def get_all_data(first,last,url,link,new_name_array,isr):
    try:
        global all_d
        
        all_d=[]
        xxx=0
        if '/tv/' in url:
            fav_search_f=Addon.getSetting("fav_search_f")
            fav_servers_en=Addon.getSetting("fav_servers_en")
            fav_servers=Addon.getSetting("fav_servers")
           
            google_server= Addon.getSetting("google_server")
            rapid_server=Addon.getSetting("rapid_server")
            direct_server=Addon.getSetting("direct_server")
            heb_server=Addon.getSetting("heb_server")
        else:
            fav_search_f=Addon.getSetting("fav_search_f_tv")
            fav_servers_en=Addon.getSetting("fav_servers_en_tv")
            fav_servers=Addon.getSetting("fav_servers_tv")
            google_server= Addon.getSetting("google_server_tv")
            rapid_server=Addon.getSetting("rapid_server_tv")
            direct_server=Addon.getSetting("direct_server_tv")
            heb_server=Addon.getSetting("heb_server_tv")
        
   
              
              
        if '/tv/' in url:
         url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
         
        else:
         url_g=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
        html_g=requests.get(url_g).json()
        if Addon.getSetting("dp")=='true' and (last-first)>1:
                dp = xbmcgui.DialogProgress()
                dp.create("Loading movies", "Please wait", '')
                dp.update(0)
        thread=[]
        for i in range(first,last):
           
           url=link+'page='+str(i)
          
           
           thread.append(Thread(get_tmdb_data,new_name_array,html_g,fav_search_f,fav_servers_en,fav_servers,google_server,rapid_server,direct_server,heb_server,url,isr,xxx))
           thread[len(thread)-1].setName('Page '+str(i))
           xxx+=1
       

           
          
           
           

                #addDir3('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status)
    except Exception ,err:
            import traceback
            from os.path import basename
            exc_info=sys.exc_info()
            e=(traceback.format_exc())
            et=e.split(',')
          
            e=','.join(et).replace('UnboundLocalError: ','')
            home1=xbmc.translatePath("special://home/")
            e_al=e.split(home1)
            logging.warning(e_al)
            e=e_al[len(e_al)-1].replace(home1,'')
            news='''\
                Error
err :[COLOR aqua]%s[/COLOR]

                
                '''
            window = whats_new('Oops','https://comps.canstockphoto.com/oops-vector-smiley-clip-art-vector_csp11504160.jpg',(e))
            window.doModal()
            del window
    start_time=time.time()
    for td in thread:
        td.start()
        if 1:#Addon.getSetting("fast_pages")=='false':
            
            while td.is_alive():
                xbmc.sleep(100)
            
        if Addon.getSetting("dp")=='true' and (last-first)>1:
                elapsed_time = time.time() - start_time
                dp.update(0, ' Activating '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
        
        #xbmc.sleep(255)
        
    while 1:

          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              
              still_alive=1
              all_alive.append(thread[yy].name)
          if still_alive==0:
            break
          if Addon.getSetting("dp")=='true' and (last-first)>1:
                elapsed_time = time.time() - start_time
                dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive)," ")
          xbmc.sleep(100)
    if Addon.getSetting("dp")=='true' and (last-first)>1:
        dp.close()
    return all_d
def get_all_m_data(url,page,time_dialation,now_y,base_url):
    global all_d
    all_d=[]
    thread=[]
    if Addon.getSetting("dp")=='true' :
            dp = xbmcgui.DialogProgress()
            dp.create("Loading movies", "Please wait", '')
            dp.update(0)
    
    for year_c in range(now_y-time_dialation,now_y):
        url_new=base_url%(year_c,page)
        
     
  
   
        html={}
        html['results']=[]
        regex='page=(.+?)$'
        match=re.compile(regex).findall(url_new)

        if len(match)==0:
            first=1
            last=2
            link=url_new.split('page=')[0]
        else:
           link=url_new.split('page=')[0]
           first=int(match[0])
           
           last=first+1
           




        
        thread.append(Thread(get_all_data,first,last,url_new,link,[],'0'))
        thread[len(thread)-1].setName(str(year_c))
        
    start_time=time.time()
    for td in thread:
        td.start()
       
            
        if Addon.getSetting("dp")=='true' :
            elapsed_time = time.time() - start_time
            dp.update(0, ' Activating '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),td.name," ")
        
        #xbmc.sleep(255)
        
    while 1:

          still_alive=0
          all_alive=[]
          for yy in range(0,len(thread)):
            
            if  thread[yy].is_alive():
              
              still_alive=1
              all_alive.append(thread[yy].name)
          if still_alive==0:
            break
          if Addon.getSetting("dp")=='true':
                elapsed_time = time.time() - start_time
                dp.update(0, ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive)," ")
          xbmc.sleep(100)
    if Addon.getSetting("dp")=='true' and last!=2:
        dp.close()
    return all_d
def get_multi_year(url,page,time_dialation):
    import cache,random
    start_time=time.time()
    url_o=url
    
    all_years=[]
    import datetime
    now = datetime.datetime.now()
    for year in range(now.year,1970,-1):
         all_years.append(str(year))
    
    if url=='movie':

            base_url=domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&language=en&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=en&page=%s'
        
     
    elif url=='tv':
            base_url=domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&language=en&sort_by=popularity.desc&first_air_date_year=%s&include_null_first_air_dates=false&with_original_language=en&page=%s'

    a=[]
    a.append((url,page,time_dialation,int(now.year),base_url))

    all_d=cache.get(get_all_m_data,24,url,page,time_dialation,int(now.year),base_url, table='pages')
    all_d=sorted(all_d, key=lambda x: x[9], reverse=True)
   
    all_n=[]
    all_items=[]

    if Addon.getSetting("dp")=='true' :
            dp = xbmcgui.DialogProgress()
            dp.create("Loading movies", "Please wait", '')
            dp.update(0)
    z=0
   
    for  name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx in all_d:
        if name in all_n:
            continue
        
        all_n.append(name)
        all_items.append(addDir3(name,url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status,collect_all=True))
        elapsed_time = time.time() - start_time
        if Addon.getSetting("dp")=='true' :
            dp.update(int((z*100.0)/(len(all_d))), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),name,str(len(all_d)-z))
        z+=1

    xbmcplugin .addDirectoryItems(int(sys.argv[1]),all_items,len(all_items))
    logging.warning('Got All Data')
    regex='page=(.+?)$'
    match=re.compile(regex).findall(url)
    link=url.split('page=')[0]

    
    addDir3('[COLOR aqua][I]Next[/I][/COLOR]'.decode('utf8'),url_o,133,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','Next'.decode('utf8'),data=str(time_dialation),original_title=str(int(match[0])+1))

    addLink( '[COLOR khaki][I]Return to start[/I][/COLOR]'.decode('utf8'), 'www',103,False,'http://bellaharling.com/wp-content/uploads/2015/01/007485-blue-metallic-orb-icon-arrows-arrow-undo.png','https://media.istockphoto.com/vectors/arrow-back-icon-vector-id473334504?k=6&m=473334504&s=612x612&w=0&h=oJPHGtAcfiMgjJ8QLhTX03Hy9osSo2wRQfG2WTaCS3E=','Return to start'.decode('utf8'))
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    if Addon.getSetting("dp")=='true' :
        dp.close()
    #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    return 0
def get_rest_data(name,url,mode,iconimage,fanart,description,video_info={},data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr=0,generes=' ',trailer=' ',dates=' ',watched='no',fav_status='false'):
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
def get_movies(url,isr,reco=0,new_name_array=[]):
   import cache
   all_years=[]
   import datetime
   now = datetime.datetime.now()
   for year in range(now.year,1970,-1):
         all_years.append(str(year))
   if url=='movie_years&page=1':
     
      
      ret=ret = xbmcgui.Dialog().select("Year", all_years)
      if ret!=-1:
        if isr==1:
          url=domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&language=en&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=he&page=1'%all_years[ret]
          
        else:
          url=domain_s+'api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&language=en&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=en&page=1'%all_years[ret]
        
      else:
        return 0
   if url=='tv_years&page=1' and 'page=1' in url:
      
      ret=ret = xbmcgui.Dialog().select("Year", all_years)
      if ret!=-1:
        url=domain_s+'api.themoviedb.org/3/discover/tv?api_key=1248868d7003f60f2386595db98455ef&language=en&sort_by=popularity.desc&first_air_date_year=%s&include_null_first_air_dates=false&with_original_language=en&page=1'%all_years[ret]
       
      else:
        sys.exit()
   if '/search' in url and 'page=1' in url:
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
               search_entered = keyboard.getText()
               url=url%urllib.quote_plus(search_entered)
        else:
          sys.exit()
   
   html={}
   html['results']=[]
   regex='page=(.+?)$'
   match=re.compile(regex).findall(url)

   if len(match)==0 or reco==1:
    first=1
    last=2
    link=url.split('page=')[0]
   else:
       link=url.split('page=')[0]
       first=int(match[0])
       s_last=int(Addon.getSetting("num_p"))
       if s_last>10:
         s_last=10
       last=first+int(s_last)
       


   

   

   #all_in_data=get_all_data(first,last,url,link,new_name_array,isr)
   logging.warning('Insert Got All Data')
   all_in_data=cache.get(get_all_data,24,first,last,url,link,new_name_array,isr, table='pages')
   logging.warning('Insert Got All Data2')
   all_in_data=sorted(all_in_data, key=lambda x: x[17], reverse=False)

   for  name,url,mode,icon,fan,plot,year,original_name,id,rating,new_name,year,isr,genere,trailer,watched,fav_status,xxx in all_in_data:
        
        
        addDir3(name,url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer,watched=watched,fav_status=fav_status)
   logging.warning('Got All Data')
   regex='page=(.+?)$'
   match=re.compile(regex).findall(url)
   link=url.split('page=')[0]
   
   if reco==0:
     addDir3('[COLOR aqua][I]Next[/I][/COLOR]'.decode('utf8'),link+'page='+str(int(match[0])+1),3,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','Next'.decode('utf8'),isr=isr)

     addLink( '[COLOR khaki][I]Return to start[/I][/COLOR]'.decode('utf8'), 'www',103,False,'http://bellaharling.com/wp-content/uploads/2015/01/007485-blue-metallic-orb-icon-arrows-arrow-undo.png','https://media.istockphoto.com/vectors/arrow-back-icon-vector-id473334504?k=6&m=473334504&s=612x612&w=0&h=oJPHGtAcfiMgjJ8QLhTX03Hy9osSo2wRQfG2WTaCS3E=','Return to start'.decode('utf8'))
   #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
   #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

   #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
   return new_name_array

def get_seasons(name,url,iconimage,fanart,description,data,original_title,id,heb_name,isr):
   payload= {
                    "apikey": "0629B785CE550C8D",
                    "userkey": "",
                    "username": ""
   }
   tmdbKey = '1248868d7003f60f2386595db98455ef'
   if 'tt' in id:
             url3='https://api.themoviedb.org/3/find/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US&external_source=imdb_id'%id
             xx=requests.get(url3).json()
            
             
             if len(xx['tv_results'])>0:
                    id=str(xx['tv_results'][0]['id'])
            

   url=domain_s+'api.themoviedb.org/3/tv/%s?api_key=1248868d7003f60f2386595db98455ef&language=en&append_to_response=external_ids'%id

   html=requests.get(url).json()
   show_original_year=html['first_air_date'].split("-")[0]

   #tmdb data
   #headers['Authorization'] = "Bearer %s" %  str(r_json.get('token'))
   tmdbid=html['external_ids']['tvdb_id']
   if tmdbid==None:
     response2 = requests.get(domain_s+'www.thetvdb.com/?string=%s&searchseriesid=&tab=listseries&function=Search'%name).content
     
     SearchSeriesRegexPattern = 'a href=".+?tab=series.+?id=(.+?)mp'
     match=re.compile(SearchSeriesRegexPattern).findall(response2)
   
     for tmnum in match:
       tmnum=tmnum.replace("&a","")
       if len(tmnum)>0:
         tmdbid=tmnum

   response = requests.get('http://thetvdb.com/api/0629B785CE550C8D/series/%s/all/he.xml'%html['external_ids']['tvdb_id']).content
  
   attr=['Combined_season','FirstAired']
   regex='<Episode>.+?<EpisodeName>(.+?)</EpisodeName>.+?<EpisodeNumber>(.+?)</EpisodeNumber>.+?<FirstAired>(.+?)</FirstAired>.+?<SeasonNumber>(.+?)</SeasonNumber>'
   match=re.compile(regex,re.DOTALL).findall(response)
   #seasons_tvdb=parseDOM(response,'Episode', attr)
   all_season=[]
   all_season_tvdb_data=[]
    
   all_season_imdb=[]
   all_season_imdb_data=[]
   for ep_name,ep_num,aired,s_number in match:
     if s_number not in all_season:

       all_season.append(str(s_number))
       all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"season_number":s_number,"poster_path":iconimage})
   try:
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,tmdbKey)
      
       
       imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
       xx=requests.get('https://www.imdb.com/title/%s/episodes'%imdb_id).content
       regex='<label for="bySeason">(.+?)</div'
       match_imdb_s_pre=re.compile(regex,re.DOTALL).findall(xx)[0]
       regex='<option.+?value="(.+?)"'
       match_imdb_s=re.compile(regex).findall(match_imdb_s_pre)
       regex_img='<img itemprop="image".+?src="(.+?)"'
       img_imdb_pre=re.compile(regex_img,re.DOTALL).findall(xx)
       if len (img_imdb_pre)>0:
            img_imdb=img_imdb_pre[0]
       else:
            img_imdb=' '
       for s_number in match_imdb_s:
            all_season_imdb.append(str(s_number))
            all_season_imdb_data.append({"name":'0',"episode_number":'0',"air_date":' ',"season_number":s_number,"poster_path":img_imdb,'backdrop_path':img_imdb})
   except:
    pass
   all_season_tmdb=[]
   for data in html['seasons']:
      all_season_tmdb.append(str(data['season_number']))
   for items_a in all_season:
     if items_a not in all_season_tmdb:
       html['seasons'].append(all_season_tvdb_data[all_season.index(items_a)])
       
   for items_a in all_season_imdb:
     if items_a not in all_season_tmdb:
       html['seasons'].append(all_season_imdb_data[all_season_imdb.index(items_a)])
   plot=html['overview']
   original_name=html['original_name']
   for data in html['seasons']:
   
     new_name=' Season '.decode('utf8')+str(data['season_number'])
     if data['air_date']!=None:
         year=str(data['air_date'].split("-")[0])
     else:
       year=0
     season=str(data['season_number'])
     if data['poster_path']==None:
      icon=iconimage
     else:
       icon=data['poster_path']
     if 'backdrop_path' in data:
         if data['backdrop_path']==None:
          fan=fanart
         else:
          fan=data['backdrop_path']
     else:
        fan=html['backdrop_path']
     if plot==None:
       plot=' '
     if fan==None:
       fan=fanart
     if 'http' not in fan:
       fan=domain_s+'image.tmdb.org/t/p/original/'+fan
     if 'http' not in icon:
       icon=domain_s+'image.tmdb.org/t/p/original/'+icon
     dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' AND type='%s' AND season='%s' "%(original_title.replace("'","%27"),'tv',season))
     
     match = dbcur.fetchone()

     if match!=None:
       color='magenta'
     else:
       color='white'
     addDir3( '[COLOR %s]'%color+new_name+'[/COLOR]',url,8,icon,fan,plot,data=year,original_title=original_name,id=id,season=season,tmdbid=tmdbid,show_original_year=show_original_year,heb_name=heb_name,isr=isr)
def get_episode_data(id,season,episode):
    url='http://api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=1248868d7003f60f2386595db98455ef&language=en&append_to_response=external_ids'%(id,season,episode)
    
    html=requests.get(url).json()
    if 'name' in html:
        name=html['name']
        plot=html['overview']
        if html['still_path']!=None:
          image=domain_s+'image.tmdb.org/t/p/original/'+html['still_path']
        else:
          image=' '
        return name,plot,image
    else:
       return ' ',' ',' '
def get_episode(name,url,iconimage,fanart,description,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr):
   import _strptime
   url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%(id,season)
   tmdbKey = '1248868d7003f60f2386595db98455ef'
   html=requests.get(url).json()
   #tmdb data
   if 'episodes'  in html:
       if html['episodes'][0]['name']=='':
         url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=eng'%(id,season)
         html=requests.get(url).json()
   response = requests.get('http://thetvdb.com/api/0629B785CE550C8D/series/%s/all/he.xml'%tmdbid).content
   
   attr=['Combined_season','FirstAired']
   regex='<Episode>.+?<EpisodeName>(.+?)</EpisodeName>.+?<EpisodeNumber>(.+?)</EpisodeNumber>.+?<FirstAired>(.+?)</FirstAired>.+?<Overview>(.+?)</Overview>.+?<SeasonNumber>(.+?)</SeasonNumber>'
   match=re.compile(regex,re.DOTALL).findall(response)
   regex_eng='<slug>(.+?)</slug>'
   match_eng=re.compile(regex_eng).findall(response)
   
   eng_name=name
   if len (match_eng)>0:
     eng_name=match_eng[0]

   #seasons_tvdb=parseDOM(response,'Episode', attr)

   all_episodes=[]
   all_season_tvdb_data=[]
   
   all_episodes_imdb=[]
   all_episodes_imdb_data=[]
   image2=' '
   for ep_name,ep_num,aired,overview,s_number in match:
     
     image2=fanart
     if s_number==season:
         if ep_num not in all_episodes:
           
           all_episodes.append(str(ep_num))
           all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"overview":overview,"season_number":s_number,"still_path":iconimage,"poster_path":image2})
   
   url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=en&append_to_response=external_ids'%(id,tmdbKey)
      
       
    
      
       
   imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
   xx=requests.get('https://www.imdb.com/title/%s/episodes?season=%s'%(imdb_id,season)).content

   regex='div class="image">.+?title="(.+?)"(.+?)meta itemprop="episodeNumber" content="(.+?)".+?itemprop="description">(.+?)<'
   match_imdb_s_pre=re.compile(regex,re.DOTALL).findall(xx)
  
   for ep_name,poster,ep_num,plot in match_imdb_s_pre:
        if 'src="' in poster:
            regex='src="(.+?)"'
            poster=re.compile(regex).findall(poster)[0]
        else:
            poster=' '
        all_episodes_imdb.append(str(ep_num))
        all_episodes_imdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":' ',"season_number":season,"poster_path":poster,'still_path':poster,"overview":plot})
   
  
   all_episodes_tmdb=[]

   if 'episodes' not in html:
     html['episodes']=[]
     html['poster_path']=fanart
   else:
       for data in html['episodes']:
          all_episodes_tmdb.append(str(data['episode_number']))
   for items_a in all_episodes:
     if items_a not in all_episodes_tmdb:
       html['episodes'].append(all_season_tvdb_data[all_episodes.index(items_a)])
   for items_a in all_episodes_imdb:
     if items_a not in all_episodes_tmdb:
       html['episodes'].append(all_episodes_imdb_data[all_episodes_imdb.index(items_a)])
       
   original_name=original_title

   xxx=0
   start_time = time.time()
   
   if Addon.getSetting("use_trak")=='true':
       i = (call_trakt('/users/me/watched/shows?extended=full'))
       all_tv_w={}
       for ids in i:
         all_tv_w[str(ids['show']['ids']['tmdb'])]=[]
         for seasons in ids['seasons']:
          for ep in seasons['episodes']:
            all_tv_w[str(ids['show']['ids']['tmdb'])].append(str(seasons['number'])+'x'+str(ep['number']))
   
   fav_search_f=Addon.getSetting("fav_search_f_tv")
   fav_servers_en=Addon.getSetting("fav_servers_en_tv")
   fav_servers=Addon.getSetting("fav_servers_tv")
   
   if  fav_search_f=='true' and fav_servers_en=='true' and (len(fav_servers)>0 ):

        fav_status='true'
   else:
       fav_status='false'
   from datetime import datetime
   for data in html['episodes']:
     plot=data['overview']
     new_name=str(data['episode_number'])+" . "+data['name']
     air_date=''
     
     if 'air_date' in data:
       air_date=data['air_date']
       if data['air_date']!=None:
         
         year=str(data['air_date'].split("-")[0])
       else:
         year=0
     else:
       year=0
     
     if data['still_path']!=None:
       if 'https' not in data['still_path']:
         image=domain_s+'image.tmdb.org/t/p/original/'+data['still_path']
       else:
         image=data['still_path']
       
     elif html['poster_path']!=None:
      if 'https' not in html['poster_path']:
       image=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
      else:
         image=html['poster_path']
     else:
       image=fanart
     if html['poster_path']!=None:
      if 'https' not in html['poster_path']:
       icon=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
      else:
        icon=html['poster_path']
     else:
       icon=iconimage
     #if image2==fanart:
     #  icon=iconimage
      
     #  image=fanart
     color2='white'
     try:
        if 'air_date' in data:
           
               datea='[COLOR aqua]'+str(time.strptime(data['air_date'], '%Y-%m-%d'))+'[/COLOR]\n'
               
               a=(time.strptime(data['air_date'], '%Y-%m-%d'))
               b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
               
           
               if a>b:
                 color2='red'
               else:
                 
                 color2='white'
        datea='[COLOR aqua]'+' Aired at '+time.strftime( "%d-%m-%Y",a) + '[/COLOR]\n'
     except:
             
             datea=''
             color2='red'
     f_subs=[]
     
     
   
         
         
     
     

   
     color=color2
     if season!=None and season!="%20":
        tv_movie='tv'
     else:
       tv_movie='movie'
     logging.warning('watched name: '+original_title)
     
     
     dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(original_title.replace("'","%27"),tv_movie,season,data['episode_number']))
     
     match = dbcur.fetchone()

     if match!=None:
       color='magenta'
     elapsed_time = time.time() - start_time
     
     xxx=xxx+1
     if  Addon.getSetting("disapear")=='true' and color=='red':
        a=1
     else:
     
       watched='no'
       if Addon.getSetting("use_trak")=='true':
           if id in all_tv_w:
             if season+'x'+str(data['episode_number']) in all_tv_w[id]:
              watched='yes'
       
       
       addDir3( '[COLOR %s]'%color+new_name+'[/COLOR]', url,4, icon,image,datea+plot,data=year,original_title=original_name,id=id,season=season,episode=data['episode_number'],eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=air_date,watched=watched,fav_status=fav_status)
              
     #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
     #xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
     

        