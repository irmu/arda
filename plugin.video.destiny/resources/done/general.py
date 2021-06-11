# -*- coding: utf-8 -*-
import logging,re,requests,cache,PTN,time
try:
    import urllib3

    urllib3.disable_warnings()
except:
  pass
try:
   import xbmcgui
   import xbmcaddon
   Addon = xbmcaddon.Addon()
except:
  import Addon
  pass
from urlparse import urlparse
try:
    import xbmc
    KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])
    if KODI_VERSION>=17:
     
      domain_s='https://'
    elif KODI_VERSION<17:
      domain_s='http://'
   
except:
    domain_s='https://'
all_colors=['aliceblue', 'anitquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred ', 'indigo  ', 'ivory', 'khaki', 'kodi', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'none', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
def get_rd_servers():
    
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
            rd_domains=[u'4shared.com', u'openload.co', u'rapidgator.net', u'sky.fm', u'1fichier.com', u'docs.google.com', u'depositfiles.com', u'hitfile.net', u'rapidvideo.com', u'filerio.com', u'solidfiles.com', u'mega.co.nz', u'scribd.com', u'flashx.tv', u'canalplus.fr', u'dailymotion.com', u'salefiles.com', u'youtube.com', u'faststore.org', u'turbobit.net', u'big4shared.com', u'filefactory.com', u'youporn.com', u'oboom.com', u'vimeo.com', u'redtube.com', u'zippyshare.com', u'file.al', u'clicknupload.me', u'soundcloud.com', u'gigapeta.com', u'datafilehost.com', u'datei.to', u'rutube.ru', u'load.to', u'streamango.com', u'sendspace.com', u'vidoza.net', u'tusfiles.net', u'unibytes.com', u'ulozto.net', u'hulkshare.com', u'dl.free.fr', u'streamcherry.com', u'vidlox.tv', u'mediafire.com', u'vk.com', u'uploaded.net', u'userscloud.com']
            pass
        return rd_domains

rd_sources=Addon.getSetting("rdsource")
allow_debrid = rd_sources == "true" 
if allow_debrid:
    rd_domains=cache.get(get_rd_servers, 720, table='RD_Account')
    rd_domains.append('nitroflare.com')
else:
    rd_domains=[]

base_header={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',

            'Pragma': 'no-cache',
            
           
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            }
class cleantitle():
   @classmethod
   def get(self,name):
    return name.replace('%20',' ').replace('%3a',':').replace('%27',"'")
class client():
  
  def __init__(self, url):
        self.url = url 
  @classmethod
  def request(self,url,cookie=None):
     headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
           
            'Pragma': 'no-cache',
            
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
     return requests.get(url,headers=headers,cookies=cookie).content
BASE_URL = 'http://api.trakt.tv'
SETTING_TRAKT_EXPIRES_AT = "trakt_expires_at"
SETTING_TRAKT_ACCESS_TOKEN = "trakt_access_token"
SETTING_TRAKT_REFRESH_TOKEN = "trakt_refresh_token"
CLIENT_ID = "8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6"
CLIENT_SECRET = "1ec4f37e5743e3086abace0c83444c25d9b655d1d77b793806b2c8205a510426"

def reset_trakt():
    ret =xbmcgui.Dialog().yesno(("Authenticate Trakt"), ("Clear Trakt?"))
    if ret:
      Addon.setSetting(SETTING_TRAKT_ACCESS_TOKEN, '')
      xbmc.executebuiltin((u'Notification(%s,%s)' % ('Destiny', ' Trakt Cleared'.decode('utf8'))).encode('utf-8'))
def trakt_get_device_code():
    data = { 'client_id': CLIENT_ID }
    return call_trakt("oauth/device/code", data=data, with_auth=False)
def trakt_authenticate():
    code = trakt_get_device_code()
    token = trakt_get_device_token(code)
    if token:
        expires_at = time.time() + 60*60*24*30#*3
        Addon.setSetting(SETTING_TRAKT_EXPIRES_AT, str(expires_at))
        Addon.setSetting(SETTING_TRAKT_ACCESS_TOKEN, token["access_token"])
        Addon.setSetting(SETTING_TRAKT_REFRESH_TOKEN, token["refresh_token"])
        return True
    return False
def trakt_refresh_token():
    data = {        
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "refresh_token",
        "refresh_token": unicode(Addon.getSetting(SETTING_TRAKT_REFRESH_TOKEN))
    }
    response = call_trakt("oauth/token", data=data, with_auth=False)
    if response:
        Addon.setSetting(SETTING_TRAKT_ACCESS_TOKEN, response["access_token"])
        Addon.setSetting(SETTING_TRAKT_REFRESH_TOKEN, response["refresh_token"])
def trakt_get_device_token(device_codes):
    data = {
        "code": device_codes["device_code"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    start=time.time()
    expires_in = device_codes["expires_in"]
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(("Authenticate Trakt"), ("Please go to https://trakt.tv/activate and enter the code"),str(device_codes["user_code"])    )
    try:
        time_passed = 0
        while not xbmc.abortRequested and not progress_dialog.iscanceled() and time_passed < expires_in:            
            try:
                response = call_trakt("oauth/device/token", data=data, with_auth=False)
            except requests.HTTPError, e:
                if e.response.status_code != 400:
                    raise e
                progress = int(100 * time_passed / expires_in)
                progress_dialog.update(progress)
                xbmc.sleep(max(device_codes["interval"], 1)*1000)
            else:
                return response
            time_passed = time.time() - start
    finally:
        progress_dialog.close()
        del progress_dialog
    return None




def post_trakt(path,data=None, with_auth=True):
    import urllib
    API_ENDPOINT = "https://api-v2launch.trakt.tv"

    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': CLIENT_ID
    }


    
    if with_auth:
           
            token =unicode( Addon.getSetting(SETTING_TRAKT_ACCESS_TOKEN))
            headers.update({'Authorization': 'Bearer %s' % token})
            
        
            return requests.post("{0}/{1}".format(API_ENDPOINT, path), json=(data), headers=headers).content
  
        
      

def call_trakt(path, params={}, data=None, is_delete=False, with_auth=True, pagination = False, page = 1):
    import urllib
    params = dict([(k, (v).encode('utf8')) for k, v in params.items() if v])
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': CLIENT_ID
    }


    API_ENDPOINT = "https://api-v2launch.trakt.tv"
    
    def send_query():
        if with_auth:
            try:
                expires_at = int(Addon.getSetting(SETTING_TRAKT_EXPIRES_AT))
                if time.time() > expires_at:
                    trakt_refresh_token()
            except:
                pass
            token =unicode( Addon.getSetting(SETTING_TRAKT_ACCESS_TOKEN))
            if token:
                headers['Authorization'] = 'Bearer ' + token
        if data is not None:
            assert not params
            return requests.post("{0}/{1}".format(API_ENDPOINT, path), json=(data), headers=headers)
        elif is_delete:
            return requests.delete("{0}/{1}".format(API_ENDPOINT, path), headers=headers)
        else:
            return requests.get("{0}/{1}".format(API_ENDPOINT, path), params, headers=headers)

    def paginated_query(page):
        lists = []
        params['page'] = page
        results = send_query()
        if with_auth and results.status_code == 401 and xbmcgui.Dialog().yesno(("Authenticate Trakt"), ("You must authenticate with Trakt. Do you want to authenticate now?")) and trakt_authenticate():
            response = paginated_query(1)
            return response
        results.raise_for_status()
        results.encoding = 'utf-8'
        lists.extend(results.json())
        if "X-Pagination-Page-Count" in results.headers:
        
            return lists, results.headers["X-Pagination-Page-Count"]
        else:   
            return lists,1
    if pagination == False:
        response = send_query()
        if with_auth and response.status_code == 401 and xbmcgui.Dialog().yesno(("Authenticate Trakt"),("You must authenticate with Trakt. Do you want to authenticate now?")) and trakt_authenticate():
            response = send_query()
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.json()
    else:
        (response, numpages) = paginated_query(page)
        return response, numpages
def base_convert(x,b,alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    'convert an integer to its string representation in a given base'
    if b<2 or b>len(alphabet):
        if b==64: # assume base64 rather than raise error
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        else:
            raise AssertionError("int2base base out of range")
    if isinstance(x,complex): # return a tuple
        return ( int2base(x.real,b,alphabet) , int2base(x.imag,b,alphabet) )
    if x<=0:
        if x==0:
            return alphabet[0]
        else:
            return  '-' + int2base(-x,b,alphabet)
    # else x is non-negative real
    rets=''
    while x>0:
        x,idx = divmod(x,b)
        rets = alphabet[idx] + rets
    return rets
def parseDOM(html, name='', attrs=None, ret=False):
    import dom_parser
    if attrs: attrs = dict((key, re.compile(value + ('$' if value else ''))) for key, value in attrs.iteritems())
    results = dom_parser.parse_dom(html, name, attrs, ret)
    if ret:
        results = [result.attrs[ret.lower()] for result in results]
    else:
        results = [result.content for result in results]
    return results
def fix_q(quality):
    f_q=100
    if quality.lower()=='4k':
        quality='2160'
    if '2160' in quality:
      f_q=1
    if '1080' in quality:
      f_q=2
    elif '720' in quality:
      f_q=3
    elif '480' in quality:
      f_q=4
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q=5
    elif '360' in quality or 'sd' in quality.lower():
      f_q=6
    elif '240' in quality:
      f_q=7
    return f_q
def base_convert(x,b,alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    'convert an integer to its string representation in a given base'
    if b<2 or b>len(alphabet):
        if b==64: # assume base64 rather than raise error
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        else:
            raise AssertionError("int2base base out of range")
    if isinstance(x,complex): # return a tuple
        return ( int2base(x.real,b,alphabet) , int2base(x.imag,b,alphabet) )
    if x<=0:
        if x==0:
            return alphabet[0]
        else:
            return  '-' + int2base(-x,b,alphabet)
    # else x is non-negative real
    rets=''
    while x>0:
        x,idx = divmod(x,b)
        rets = alphabet[idx] + rets
    return rets
    
def get_imdb_data(info,name_o,image,source,type):
         tmdbKey = '653bb8af90162bd98fc7ee32bcbbfb3d'
         name=name_o
         imdb_id=''
         icon=image
         fanart=image
         plot=''
         rating=''
         genere=' '
         check=False
         if source=='4k':
            if  Addon.getSetting("4k_tmdb")=='false':
              check=True
         else:
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
            tmdb_data="https://api.tmdb.org/3/search/%s?api_key=%s&query=%s&year=%s&language=he&append_to_response=external_ids"%(type,tmdbKey,urllib.quote_plus(info['title']),info['year'])
            year_n=info['year']
          else:
            tmdb_data="https://api.tmdb.org/3/search/%s?api_key=%s&query=%s&language=he&append_to_response=external_ids"%(type,tmdbKey,urllib.quote_plus(info['title']))

          all_data=requests.get(tmdb_data).json()
          if 'results' in all_data:
           if len(all_data['results'])>0:
                if (all_data['results'][0]['id'])!=None:
                    url='https://api.themoviedb.org/3/%s/%s?api_key=%s&language=he&append_to_response=external_ids'%(type,all_data['results'][0]['id'],tmdbKey)
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
         
def fix_name(name_o):
    
    regex_c='\[COLOR(.+?)\]'
    match_c=re.compile(regex_c).findall(name_o)

    if len(match_c)>0:
          for items in match_c:
            name_o=name_o.replace('[COLOR%s]'%items,'')
    name_o=name_o.replace('=',' ').replace('[B]','').replace('[/B]','').replace('silver','').replace('deepskyblue','').replace('[','').replace(']','').replace('/COLOR','').replace('COLOR','').replace('4k','').replace('4K','').strip().replace('(','.').replace(')','.').replace(' ','.').replace('..','.')
    return name_o
def res_q(quality):
    f_q=' '
    if '2160' in quality or '4k' in quality.lower():
      f_q='2160'
    elif '1080' in quality:
      f_q='1080'
    elif '720' in quality:
      f_q='720'
    elif '480' in quality:
      f_q='480'
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q='hd'
    elif '360' in quality or 'sd' in quality.lower():
      f_q='360'
    elif '240' in quality:
      f_q='240'
    return f_q
def fix_q(quality):
    f_q=100
    if '2160' in quality:
      f_q=1
    if '1080' in quality:
      f_q=2
    elif '720' in quality:
      f_q=3
    elif '480' in quality:
      f_q=4
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q=5
    elif '360' in quality or 'sd' in quality.lower():
      f_q=6
    elif '240' in quality:
      f_q=7
    return f_q
    
def similar(w1, w2):
    from difflib import SequenceMatcher
    
    s = SequenceMatcher(None, w1, w2)
    return int(round(s.ratio()*100))
def cloudflare_request(url, post=None, headers={}, mobile=False, safe=False,get_url=False, timeout=30):
    from cfscrape import run
    parsed_uri = urlparse( url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if get_url:
        domain=url
    
    #print run.get_tokens_with_headers(domain,headers,get_url)
    if safe:
        
        x,token=cache.get(run.get_tokens_with_headers,0,domain,headers,get_url, table='cookies')
         
        
        if get_url:
            
            result= x
        else:
            result=requests.get(url,headers=token[1],cookies=token[0],timeout=10)   
            result=result.content
        
        
    else:
        x,token=cache.get(run.get_tokens_with_headers,3,domain,headers,get_url, table='cookies')
        
        counter=0
        if 'jschl-answer' in x:
            while 'jschl-answer' in x:
                x,token=cache.get(run.get_tokens_with_headers,0,domain,headers,get_url, table='cookies')
                
                if get_url:
                    
                    result= x
                else:
                    result=requests.get(url,headers=token[1],cookies=token[0],timeout=10)   
                    result=result.content
                counter+=1
                print counter
                if counter>5:
                    return '',[]
        else:
               
            if get_url:
                
                result= x
            else:
            
                result=requests.get(url,headers=token[1],cookies=token[0],timeout=10)
                result=result.content
        if x=='NOTCF':
            result=requests.get(url,headers=token[1],timeout=10)
            result=result.content
    return result,token
def cloudflare_request_old(url, post=None, headers=None, mobile=False, safe=False, timeout=30):
    #try:
        
        
        user_agent ='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        if headers==None:
          headers = {'User-Agent': user_agent}
        tokens={}
        result=''
        import cfscrape_o as cfscrape
        parsed_uri = urlparse( url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        
        
        
        
        #tokens, user_agent =cfscrape.get_tokens(domain,headers)

        #tokens, user_agent = cache.get(cfscrape.get_tokens,0,domain,headers, table='cookies')
        
        #cfscrape.get_tokens(domain,user_agent=user_agent)
       
        try:
          if headers==None:
            tokens, user_agent = cache.get(cfscrape.get_tokens,3,domain,user_agent, table='cookies')
          else:
            tokens, user_agent = cache.get(cfscrape.get_tokens_with_headers,3,domain,headers, table='cookies')
        except Exception as e:
          print e
          try:
            result = requests.get(url,headers=headers,timeout=timeout)
          except:
            return ' ','OK'
          
          return result.content,'ok'
       

        
        if post!=None:
         
          result = requests.post(url,headers=headers,cookies=tokens,data=post)
        else:

          
          result = requests.get(url,headers=headers,cookies=tokens,timeout=timeout)
        if 'jschl-answer' in result.content:
          
            tokens, user_agent = cache.get(cfscrape.get_tokens,0,domain,user_agent, table='cookies')
           
            
            if post!=None:
              
              result = requests.post(url,headers=headers,cookies=tokens,data=post)
            else:
              result = requests.get(url,headers=headers,cookies=tokens,timeout=timeout)

        #scraper = cfscrape.create_scraper()
        #r = scraper.get(url).content
        content=[]
        content.append(tokens)
        content.append(headers)
        return result.content,content
      
    #except:
    #    return
    
def clean_name(name,option):

    if option==1:
      return name.replace('%20',' ').replace('%3a',':').replace('%27',"'")
    else:
      return name.replace('%20',' ').replace('%3a',':').replace('%27'," ")
      
def check_link(x,full_data=False):
    if full_data==False:
      html=x.content
    else:
      html=x
    if len(html)<20:
      return False
    all_condition=['removed due a copyright violation','404 Not Found','File was deleted','File size: <span>0.0 Mb<' , 'Object not found' , "The video has been blocked at the copyright owner","his stream doesn't exist !",'Invalid Download Link','page not found' , 'this file has been removed ' , 'removed due a copyright violation' , 'no longer available' , 'file has been deleted' , 'Page Not Found' , 'got removed by the owner.' , 'it maybe got deleted' , 'file not found' , 'file was deleted' , '<title>Error 404</title>' , '<H2>Error 404</H2>' , '<h1>Not Found</h1>' , '<b>File Not Found</b>' , 'Video Was Deleted' , 'Has Been Removed' , 'file does not exist' , 'Video not found' , 'got deleted by the owner' , 'Video not found']
    if ('uptostream.com' not in html and 'uptobox' in html):
        return False
    for items in all_condition:
        if items.lower() in html.lower():
            
            return False
    return True

def server_data(f_link,original_title,direct='NO',c_head={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'},check_now=False):
       time.sleep(0.01)
       not_working_servers=['flashx.pw','thevideo.me','vev.io','movpod.in','daclips.in','dl8.heyserver.in','cloudtime.to','speedvid.net','watchers.to','vidzella.me','not_found.php','nitroflare','nitrobit','youtube','vidto.me','vidzi.tv','vidoza.net','nowvideo.sx','vidzi.nu','estream','streamcherry.com']
       
       if 'mystream.to' in f_link:
          f_link=f_link.replace('mystream.to/watch','embed.mystream.to')
       for items in not_working_servers:
            if items in f_link:
                
                return original_title,' ',' ',False
       if 'mega.nz' in f_link or 'mega.co.nz' in f_link:
            if  Addon.getSetting('rdsource')=='false':
               
                return original_title,' ',' ',False
            else:
            
                f_link=f_link.replace('mega.nz','mega.co.nz')
       
       if 'gorillavid.in' in f_link:
            return original_title,' ',' ',False
       if 'userscloud.com' in f_link and direct!='rd':
           
            return original_title,' ',' ',False
       if 'http' not in f_link:
          
           return original_title,' ',' ',False
       
       if 'drive.google.com' in f_link:
             f_link=f_link.replace('preview','view')
       try:
          import resolveurl
       except:
          import resolveurl_temp as resolveurl
       
       try:
        
        
            
        
     
        
            
        #if 'cdn1.smotrim.live' in f_link:
        #  return original_title,' ',' ',True
        if 'rapidvideo' in f_link:
            if f_link.endswith('/'):
                f_link = f_link[:-1]
            ids=f_link.split('/')
            id=ids[len(ids)-1]
            if '&' in id:
                id=id.split('&')[0]
            f_link='https://api.rapidvideo.com/v1/objects.php?ac=info&code='+id
            x=requests.get(f_link,headers=c_head).json()
            
            
            if x['result'][id]['status']!=200:
               
                return original_title,' ',' ',False
            name1=x['result'][id]['name']
            name1=name1.replace('Watch','').replace('.mp4','').replace('watch','').replace('.MP4','').replace('.mkv','').replace('.MKV','').replace("_",".").replace("|",".")

         
            if clean_name(original_title,1).replace(' ','').replace(':','').replace("'",'').lower() not in name1.replace("'",'').replace('.',' ').replace('_',' ').replace('-',' ').replace(':','').replace(' ','').lower():
                 
                 name1=original_title
                 
            if len(name1)<2:
              name1=original_title
            if "1080" in name1:
              res="1080"
            elif "720" in name1:
              res="720"
            elif "480" in name1:
               res="480"
            else:
               res='1080'
            return name1,'Rapidvideo',res,True
       
        resolvable=resolveurl.HostedMediaFile(f_link).valid_url()
       
        #if 'estream' in f_link or resolvable==False:
        #  return original_title,'estream',' ',True
        if  resolvable==False :
          logging.warning('RETURN NON RESO')
          regex_s="//(.+?)/"
          match_s=re.compile(regex_s).findall(f_link)[0]
          return original_title,match_s,' ',True
        direct='yes'
       
        if direct=='yes':
           
           try_head = requests.get(f_link,headers=c_head, stream=True,verify=False,timeout=10)
           

           
           if 'Content-Type' in try_head.headers:
        
             if 'stream'  in try_head.headers['Content-Type'] or 'application' in try_head.headers['Content-Type'] or 'video' in try_head.headers['Content-Type'] or 'mp4' in try_head.headers['Content-Type']:
                if "HD" in f_link:
                  res="720"
                elif "720" in f_link:
                  res="720"
                elif "1080" in f_link:
                   res="1080"
                else:
                   res=' '
                regex_s="//(.+?)/"
                match_s=re.compile(regex_s).findall(f_link)
             
                return original_title,match_s[0],res,True
           html2=''
           for chunk in try_head.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    html2+=chunk
          #if 'thevideo' in f_link or 'vev.io' in f_link:
          #  html2=requests.get(f_link,headers=c_head,timeout=10,verify=False).content
          #else:
          #  html2=requests.get(f_link,headers=c_head,timeout=10).content
        else:
          html2,cook=cloudflare.request(f_link,timeout=5)
        
        if 'cloud.mail.ru' in f_link:
            if '"hash"' not in html2:
                return original_title,' ',' ',False
        if 'uptostream' in f_link:
            if "window.sources = JSON.parse('');" in html2:
                return original_title,' ',' ',False
        if 'nitroflare' in f_link:
           regex='<span title="(.+?)"'
           match4=re.compile(regex).findall(html2)
        elif 'uptostream' in f_link:
            regex="<h1 class='file-title'>(.+?)<"
            match4=re.compile(regex).findall(html2)
            if len(match4)==0:
                regex="filename = '(.+?)'"
                match4=re.compile(regex).findall(html2)
        else:
            regex='"og:title" content="(.+?)"'
            match4=re.compile(regex).findall(html2)
          
            if '1fichier.com' in f_link:
               regex='<td class="normal">(.+?)<'
               match4=re.compile(regex,re.DOTALL).findall(html2)
            if len( match4)==0:
                regex='<Title>(.+?)</Title>'
                match4=re.compile(regex,re.DOTALL).findall(html2)
            if len(match4)==0:
                 regex='name="fname" value="(.+?)"'
                 match4=re.compile(regex,re.DOTALL).findall(html2)
            if len(match4)==0:
                 regex='<title>(.+?)</title>'
                 match4=re.compile(regex,re.DOTALL).findall(html2)
            if len(match4)==0:
                 regex="title: '(.+?)',"
                 match4=re.compile(regex,re.DOTALL).findall(html2)
            if len(match4)==0:
                 regex='><span title="(.+?)"'
                 match4=re.compile(regex,re.DOTALL).findall(html2)
            if len(match4)==0:
                 regex='description" content="(.+?)"'
                 match4=re.compile(regex,re.DOTALL).findall(html2)
            
        
        if len(match4)>0:
              name1=match4[0]
              try:
                  info=(PTN.parse(match4[0]))
                  
                  if 'resolution' in info:
                     res=info['resolution']
                  else:
                     if "HD" in match4[0]:
                      res="720"
                     elif "720" in match4[0]:
                      res="720"
                     elif "1080" in match4[0]:
                       res="1080"
                     elif "2160" in match4[0]:
                       res="2160"
                     elif "4k" in match4[0].lower():
                       res="2160"
                     else:
                       res=' '
              except:
                res=' '
                pass
        else: 
            name1=original_title.replace('%20',' ')
            res=' '
        if 'rapidvideo' in f_link:
             if "=1080p" in html2:
              res="1080"
             elif "=720p" in html2:
              res="720"
             elif "=480p" in html2:
               res="480"
             else:
               res=' '
        if 'drive.google.com' in f_link:
            
             if "fmt_list" not in html2:
               
               return original_title,' ',' ',False
             if "x1080" in html2:
              res="1080"
             elif "x720" in html2:
              res="720"
             elif "x480" in html2:
               res="480"
             elif "x360" in html2:
               res="360"
             else:
               res=' '
        regex='>(.+?) (?:GB|MB)<'
        size=re.compile(regex).findall(html2)
       
        f_size='0'
        if len(size):
            sizes=size[0].split(">")
            s1=sizes[len(sizes)-1]
            if ' MB<' in html2:
            
               f_size=str(s1)+' MB'
            else:
               f_size=str(s1)+' GB'
        
        regex_s="//(.+?)/"
        match_s=re.compile(regex_s).findall(f_link)
        if 'letsupload.co' in f_link:
            regex='class="fa fa-file-text"></i>(.+?)<'
            match_le=re.compile(regex).findall(html2)
            check=True
            if len (match_le)==0:
                check=False
        else:
            check=check_link(html2,full_data=True)
        
        name1=name1.replace('Watch','').replace('.mp4','').replace('watch','').replace('.MP4','').replace('.mkv','').replace('.MKV','').replace("_",".")
        
           
        if clean_name(original_title,1).replace(' ','').replace(':','').replace("'",'').lower() not in name1.replace("'",'').replace('.',' ').replace('_',' ').replace('-',' ').replace(':','').replace(' ','').lower():
             
             name1=original_title
       
        if len(name1)<2:
          name1=original_title
        if f_size!='0':
          s_name=match_s[0]+' - '+f_size
        else:
          s_name=match_s[0]
        name1=name1.replace('\n','').replace('\t','').replace('\r','')
        return name1,s_name,res,check
       except Exception as e:
          logging.warning(e)
          logging.warning('Error FALSE')
          logging.warning(f_link)
          return original_title,' ',' ',False
############################################################################

def replaceHTMLCodes(txt):
    import HTMLParser
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.replace("&#8211", "-")
    txt = txt.strip()
    return txt