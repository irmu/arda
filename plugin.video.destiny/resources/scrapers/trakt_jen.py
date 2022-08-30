import requests,tmdbsimple,logging,re,xbmcaddon,xbmc,time,xbmcgui,urllib2
import cache
from addall import addNolink,addDir3,addLink
from unidecode import unidecode
import urlparse,threading
domain_s='https://'
TRAKT_API_ENDPOINT = "https://api.trakt.tv"
SKIP_TMDB_INFO = False
Addon = xbmcaddon.Addon()
ADDON = Addon
if ADDON.getSetting("language_id") == "system":
    LANG = xbmc.getLanguage(
        xbmc.ISO_639_1)
else:
    LANG = ADDON.getSetting("language_id")
global all_new_data
all_new_data=[]
class Thread(threading.Thread):
    def __init__(self, target, *args):
       
        self._target = target
        self._args = args
        
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        self._target(*self._args)
def getHtml(url, referer=None, hdr=None, data=None):
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}
    if not hdr:
        req = urllib2.Request(url, data, headers)
    else:
        req = urllib2.Request(url, data, hdr)
    if referer:
        req.add_header('Referer', referer)
    response = urllib2.urlopen(req, timeout=60)
    data = response.read()    
    response.close()
    return data
def Decode_String(string):

    try:
        string = string.encode('ascii', 'ignore')
    except:
        string = string.decode('utf-8').encode('ascii', 'ignore')
    return string
def Keyboard(heading='',default='',hidden=False,return_false=False,autoclose=False,kb_type='alphanum'):

   
    kb_type = eval( 'xbmcgui.INPUT_%s'%kb_type.upper() )
    if hidden:
        hidden = eval( 'xbmcgui.%s_HIDE_INPUT'%kb_type.upper() )
    keyboard = dialog.input(heading,default,kb_type,hidden,autoclose)

    if keyboard != '':
        return keyboard
    
    elif not return_false:
        return Decode_String(default)
    
    else:
        return False
TRAKT_API_KEY = "8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6"
from general import trakt_authenticate

def get_season_data(id,season):
    url='https://api.themoviedb.org/3/tv/%s/season/%s?api_key=1248868d7003f60f2386595db98455ef&language=en-US'%(id,season)
    
    html=requests.get(url).json()
    if 'name' in html:
        name=html['name']
        plot=html['overview']
        if html['poster_path']!=None:
          image=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
        else:
          image=' '
        return name,plot,image
    else:
       return ' ',' ',' '
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
def get_tmdb_from_imdb(imdb,id,season,episode,type,year,title,html_g,xxx):
    global all_new_data

    if type=='movie' or type=='show':
        url=domain_s+'api.themoviedb.org/3/find/%s?api_key=1248868d7003f60f2386595db98455ef&external_source=imdb_id&language=en'%imdb
    elif type=='episode':
        name,plot,image=get_episode_data(id,season,episode)
        all_new_data.append((name+'- S'+season+'E'+episode,image,image,plot,year,title,id,'','','',xxx,4))
        return name,image,fan,plot,year,title,id,'','','',xxx,4
    elif type=='season':
     
        name,plot,image=get_season_data(id,season)
        all_new_data.append((name,image,image,plot,year,title,id,'','','',xxx,7))
        return name,image,fan,plot,year,title,id,'','','',xxx,4
    html=requests.get(url).json()
    if 'movie_results' in html:
        if len(html['movie_results'])>0 :
            data_soure=html['movie_results']
        else:
            data_soure=html['tv_results']
    else:
        data_soure=html['tv_results']
    for data in data_soure:
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

     trailer = "plugin://plugin.video.destiny?mode=25&url=www&id=%s" % id

     all_new_data.append((new_name,icon,fan,plot,year,original_name,id,rating,genere,trailer,xxx,mode))
     return new_name,icon,fan,plot,year,original_name,id,rating,genere,trailer,xxx,mode
def get_s_data(url):

    global all_new_data
    
    if Addon.getSetting("jen_progress")=='true':
                dp = xbmcgui.DialogProgress()
                dp.create("Loading", "Please wait", '')
                dp.update(0)
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_API_KEY
    }
    response = requests.get(url, headers=headers).json()
    if 'show' in response:
        type='tv'
    else:
        type='movie'
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
    url_g=domain_s+'api.themoviedb.org/3/genre/%s/list?api_key=1248868d7003f60f2386595db98455ef&language=en'%type
    html_g=requests.get(url_g).json()
    start_time=time.time()
    name_array=[]
    all_new_data=[]
    xxx=0
    thread=[]
    temp=response
    o_type=''
    if 'cast' in response:
        temp=response['cast']
        o_type='cast'
    
    for item in temp:
        if 'type' not in item:
            item['type']='movie'
        if o_type=='cast':
            type='movie'
            item['type']='movie'
        elif item['type']=='movie':
            type='movie'
        elif item['type']=='episode' or item['type']=='season' or item['type']=='show':
            type='show'
        
       
        imdb=str(item[type]['ids']['imdb'])
        tmdb=str(item[type]['ids']['tmdb'])
        year= str(item[type]['year'])
        title=item[type]['title']
        if item['type']=='episode':
            season=str(item['episode']['season'])
            episode=str(item['episode']['number'])
        elif item['type']=='season':
            season=str(item['season']['number'])
        else:
            season='0'
            episode='0'
        if Addon.getSetting("jen_progress")=='true':
                elapsed_time = time.time() - start_time
                dp.update(int((xxx* 100.0)/(len(response)) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),imdb)
        xxx=xxx+1
        if imdb not in name_array:
        
            
            thread.append(Thread(get_tmdb_from_imdb,imdb,tmdb,season,episode,item['type'],year,title,html_g,xxx))
            thread[len(thread)-1].setName(imdb+'-S'+season+'E'+episode)
                    

    for td in thread:
        td.start()

        if Addon.getSetting("jen_progress")=='true':
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
          if Addon.getSetting("jen_progress")=='true':
                elapsed_time = time.time() - start_time
                dp.update(int(((len(thread)-len(all_alive))* 100.0)/(len(thread)) ), ' Please wait '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),','.join(all_alive))
          if still_alive==0:
            break
          xbmc.sleep(100)
    if Addon.getSetting("jen_progress")=='true':
        dp.close()
    return all_new_data
def get_data(url):
    global all_new_data
    
    
    
    
    
    time_to_save=int(Addon.getSetting("c_save_time"))
    #all_new_data=get_s_data(response,html_g,dp,start_time)
 
    all_new_data=get_s_data(url)
    all_new_data=cache.get(get_s_data,time_to_save,url, table='posters')


    all_new_data=sorted(all_new_data, key=lambda x: x[10], reverse=False)

    for new_name,icon,fan,plot,year,original_name,id,rating,genere,trailer,xxx,mode in all_new_data:
        if icon=='' and fan=='':
            addNolink(new_name,'www',199,False,iconimage=domain_s+'pbs.twimg.com/profile_images/421736697647218688/epigBm2J.jpeg',fanart='http://www.dream-wallpaper.com/free-wallpaper/cartoon-wallpaper/spawn-wallpaper/1280x1024/free-wallpaper-24.jpg')
        else:
            addDir3(new_name,'www',mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=' ',generes=genere,trailer=trailer)
    
   
        
def trakt(url):
    global all_new_data
    from jen import JenItem
    if url == "search":
    
        term = Keyboard("Search For")
        url = "https://api.trakt.tv/search/movie,show,person,list?query=%s" % term
    
    if "sync" in url or "user" in url or "recommendations" in url:
        if "list" not in url or "/me/" in url or "like" in url or "sync" in url:
            auth = trakt_authenticate()
            if auth:
                headers['Authorization'] = 'Bearer ' + auth
            else:
                return ""
    pages = None
    
    #logging.warning(response.content)
    get_data(url+'?extended=full')
   

def tmdb(page,url):
    #url=url.replace('movies','movie')
    url=url.replace('person/movies','person')
    if url.startswith("genre"):
        split_url = url.split("/")
        if len(split_url) == 3:
            url += "/1"
            split_url.append(1)
        page = int(split_url[-1])
        genre_id = split_url[-2]
        media = split_url[-3]
        url='genre/%s/%s'%(genre_id,media)
    url2='https://api.themoviedb.org/3/%s?api_key=1248868d7003f60f2386595db98455ef&language=en&append_to_response=credits&language=en&sort_by=popularity.desc&page=%s'%(url,page)
    if url.startswith("year"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            release_year = split_url[-2]
            media = split_url[-3]
            
            url2='https://api.themoviedb.org/3/discover/movie?api_key=1248868d7003f60f2386595db98455ef&language=en&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=en&page=%s'%(release_year,page)
    x=requests.get(url2).json()
    logging.warning('https://api.themoviedb.org/3/%s?api_key=1248868d7003f60f2386595db98455ef&language=en'%url)
    if 'items' in x:
        type='items'
    elif 'results' in x:
        type='results'
    elif 'movie_results' in x:
        if len(x['movie_results'])>0 :
            type='movie_results'
            f_type='movie'
        else:
            type='tv_results'
            f_type='tv'
        
    else:
        type='tv_results'
        f_type='tv'
        
    if type not in x:   
        temp=x['credits']['cast']
    else:
        temp=x[type]
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
    html_g_m=requests.get(url_g).json()
    url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=1248868d7003f60f2386595db98455ef&language=en'
    html_g_tv=requests.get(url_g).json()
    
    for data in temp:
             
             if 'original_title' in data:
               original_name=data['original_title']
               mode=4
               
               id=str(data['id'])
               f_type='movie'
             else:
               original_name=data['original_name']
               id=str(data['id'])
               mode=7
               f_type='tv'
             if 'media_type' in data:
                if data['media_type']=='movie':
                    html_g=html_g_m
                else:
                    html_g=html_g_tv
             else:
                if f_type=='movie':
                    html_g=html_g_m
                else:
                    html_g=html_g_tv
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
               new_name=data['name']
             else:
               new_name=data['title']
             
             
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

             trailer = "plugin://plugin.video.destiny?mode=25&url=www&id=%s" % id

             #all_new_data.append((new_name,icon,fan,plot,year,original_name,id,rating,genere,trailer,xxx,mode))
             addDir3(new_name,'www',mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=' ',generes=genere,trailer=trailer)
    addDir3('[COLOR aqua][I]Next[/I][/COLOR]'.decode('utf8'),o_url,80,'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTNmz-ZpsUi0yrgtmpDEj4_UpJ1XKGEt3f_xYXC-kgFMM-zZujsg','https://cdn4.iconfinder.com/data/icons/arrows-1-6/48/1-512.png','Next'.decode('utf8'),data=str(int(page)+1))
def imdb(url,data):
    if data=='searchmovies':
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Search iMDB Movies')
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText().replace(' ','+')
        if len(search_entered)>1:
            url = 'http://www.imdb.com/search/title?title=' + search_entered
        data='imdbmovies'
    elif data=='searchseries':
            search_entered = ''
            keyboard = xbmc.Keyboard(search_entered, 'Search iMDB Series')
            keyboard.doModal()
            if keyboard.isConfirmed():
                search_entered = keyboard.getText().replace(' ','+')
            if len(search_entered)>1:
                url = 'http://www.imdb.com/search/title?title=' + search_entered + '&title_type=tv_series'
            data=='imdbseries'
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
    
    
    if data=='imdbmovies':
        url = url.replace("movies/popular","https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=40&start=1").replace("movies/voted","https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=40&start=1").replace("movies/trending","https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=date[365],date[60]&sort=moviemeter,asc&count=40&start=1").replace("movies/boxoffice","https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&count=40&start=1")
        listhtml=getHtml(url)
        match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>.+?<p class="text-muted">(.+?)<', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
       
        for thumbnail, imdb, title, year,plot in match:
            addDir3(title,'www',4,thumbnail,thumbnail,plot,data=year,original_title=title,id=imdb,show_original_year=year)
    elif data=='imdbseries':
        url = url.replace("tvshows/popular","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=moviemeter,asc&count=40&start=1")
        url = url.replace("tvshows/new","http://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=release_date,desc&count=40&start=1")
        url = url.replace("tvshows/rating","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=40&start=1")
        url = url.replace("tvshows/mostviews","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=num_votes,desc&count=40&start=1")
        url = url.replace("tvshows/boxoffice","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date%5B0%5D&count=40&start=1&sort=boxoffice_gross_us,desc")
        url = url.replace("tvshows/alphabetical","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date%5B0%5D&count=40&start=1&sort=alpha,asc")
        
        listhtml = getHtml(url)
        match = re.compile(
                '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>', 
                re.IGNORECASE | re.DOTALL).findall(listhtml)
        for thumbnail, imdb, title, year in match:
            addDir3(title,'www',7,thumbnail,thumbnail,' ',data=year,original_title=title,id=imdb,show_original_year=year)
    elif data=='imdbepisode':
        url = url.replace("theepisode/","")
        listhtml = getHtml(url)
        match = re.compile(
                '<div data-const="(.+?)" class="hover-over-image zero-z-index ">\n<img width=".+?" height=".+?" class="zero-z-index" alt="(.+?)" src="(.+?)">\n<div>S(.+?), Ep(.+?)</div>\n</div>\n</a>.+?</div>\n.+?<div class="info" itemprop="episodes" itemscope itemtype=".+?">\n.+?<meta itemprop="episodeNumber" content=".+?"/>\n.+?<div class="airdate">\n.+?([^"]+)\n.+?</div>', 
                re.IGNORECASE | re.DOTALL).findall(listhtml)
        for imdb, title, thumbnail, season, episode, premiered in match:
            addDir3(title,'www',8,thumbnail,thumbnail,' ',season=season,episode=episode,data=premiered,original_title=title,id=imdb,show_original_year=premiered)
    
    
        