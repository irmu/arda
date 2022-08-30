import requests,re,logging,xbmcaddon,xbmcvfs,xbmc,os,json
import PTN
from addall import addNolink,addDir3,addLink
from general import base_header
PATH = xbmcaddon.Addon().getAddonInfo("path")
Addon = xbmcaddon.Addon()
ADDON = Addon
DEBUG =Addon.getSetting("debugmode")
Addon = xbmcaddon.Addon()
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
addon_icon=os.path.join(addonPath,'icon.jpg')
addon_fanart=os.path.join(addonPath,'fanart.jpg')

def get_xml( url):
    if url.startswith("file://"):
        url = url.replace("file://", "")
        xml_file = xbmcvfs.File(os.path.join(PATH, "xml", url))
        xml = xml_file.read()
        xml_file.close()
        return xml
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def get_xml_uncached( url):
    return self.get_xml(url)
        
def dolog(string, my_debug=False, line_info=False):

    import xbmc
    if DEBUG == 'true' or my_debug:
        try:
            xbmc.log('### %s (%s) : %s'%(ADDON_ID,AddonVersion,string), level=xbmc.LOGNOTICE)
        except:
            xbmc.log(Last_Error(),level=xbmc.LOGNOTICE)
    if line_info:
        try:
            from inspect import getframeinfo, stack
            caller = getframeinfo(stack()[1][0])
            xbmc.log('^ Line No. %s  |  File: %s'%(caller.lineno,caller.filename),level=xbmc.LOGNOTICE)
        except:
            xbmc.log(Last_Error(),level=xbmc.LOGNOTICE)
            

class JenItem(object):
    """represents an item in a jen xml list"""

    def __init__(self, item_xml):
        self.item_string = item_xml

    def get_tag_content(self, tag):
        """
        parses xml string for the content of a tag
        Args:
            collection: xml to search through
            tag: tag to find the content in
            default: value to return if nothing found
        Returns:
            tag content or default value if content is not found
        """
        return re.findall('<%s>(.+?)</%s>' % (tag, tag), self.item_string,
                          re.MULTILINE | re.DOTALL)

    def keys(self):
        """returns all keys in item"""
        return re.findall("<([^/]+?)>", self.item_string)[1:]

    def get(self, tag, default):
        """proxy for get_tag_content"""
        try:
            return self.get_tag_content(tag)[0]
        except IndexError:
            return default

    def getAll(self, tag):
        "get all tags contents" ""
        return self.get_tag_content(tag)

    def __getitem__(self, item):
        return self.get(item, "")

    def __eq__(self, other):
        return bool(self.item_string == other.item_string)

    def __repr__(self):
        return self.item_string

def sendJSON( command):
    data = ''
    try:
        data = xbmc.executeJSONRPC(uni(command))
    except UnicodeEncodeError:
        data = xbmc.executeJSONRPC(ascii(command))

    return uni(data)
def pluginquerybyJSON(url):
    json_query = uni('{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":["thumbnail","title","year","dateadded","fanart","rating","season","episode","studio"]},"id":1}') %url

    json_folder_detail = json.loads(sendJSON(json_query))
    for i in json_folder_detail['result']['files'] :
        url = i['file']
        name = removeNonAscii(i['label'])
        thumbnail = removeNonAscii(i['thumbnail'])
        try:
            fanart = removeNonAscii(i['fanart'])
        except Exception:
            fanart = ''
        try:
            date = i['year']
        except Exception:
            date = ''
        try:
            episode = i['episode']
            season = i['season']
            if episode == -1 or season == -1:
                description = ''
            else:
                description = '[COLOR yellow] S' + str(season)+'[/COLOR][COLOR hotpink] E' + str(episode) +'[/COLOR]'
        except Exception:
            description = ''
        try:
            studio = i['studio']
            if studio:
                description += '\n Studio:[COLOR steelblue] ' + studio[0] + '[/COLOR]'
        except Exception:
            studio = ''
        if i['filetype'] == 'file':

            
            addLink(name,url,5,False,iconimage=thumbnail,fanart=fanart,description=description)
        else:
            addDir3(name,url,81,thumbnail,fanart,description)
            #xbmc.executebuiltin("Container.SetViewMode(500)")
def uni(string, encoding = 'utf-8'):
    if isinstance(string, basestring):
        if not isinstance(string, unicode):
            string = unicode(string, encoding, 'ignore')
    return string
def get_url_mode(result_item,type):
        if result_item['url']!='ignorme':
            url2=result_item['url']
            mode=81
        elif result_item['json_rpc']=='ignorme':
            url2=result_item['url']
            if result_item['link']=='ignorme':
                mode=81
            else:
                if type=='dir':
                    mode=81
                else:
                    mode=5
                url2=result_item['link']
        elif result_item['link']=='ignorme':
            url2=result_item['json_rpc']
            mode=82
        else:
            url2=result_item['link']
            if type=='dir':
                mode=81
            else:
                mode=5
        return url2,mode
def check_jen_categroys(url,icon,fanart):
    addon_icon=icon
    addon_fanart=fanart
    logging.warning(url)
    from jen_cat import IMDB,TMDB,Trakt,TVMAZE
    x=requests.get(url,headers=base_header).content
    regex='<dir>(.+?)</dir>'
    m=re.compile(regex,re.DOTALL).findall(x)
   
    for item_xml in m:
       result_item=''
       if "<imdburl>" in item_xml:
            result_item=IMDB(item_xml,icon,fanart).result
            mode=80
       elif "<tmdb>" in item_xml:
            result_item=TMDB(item_xml,icon,fanart).result
            mode=80
       elif  "<trakt>" in item_xml:
            result_item=Trakt(item_xml,icon,fanart).result
            mode=80
       elif "<tvmaze>" in item_xml:
            result_item=TVMAZE(item_xml,icon,fanart).result
            mode=80
       else:
        mode=81
        item = JenItem(item_xml)
        result_item = {
                    'label': item.get("name", item["title"]) ,
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "next",
                    'url': item.get("externallink", "ignorme"),
                    'folder': True,
                    'link':item.get("link", "ignorme"),
                    'imdb': "0",
                    'content': "files",
                    
                    'json_rpc':item.get("jsonrpc", "ignorme"),
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    
                    "summary": item.get("info", ' ')
                }
        
       if result_item=='':
        continue
       if result_item['summary']==None:
        result_item['summary']=' '
       if mode==81:
        url2,mode=get_url_mode(result_item,'dir')
       else:
        url2=result_item['url']
       addDir3(result_item['label'],url2,mode,result_item['icon'],result_item['fanart'],result_item['summary'],data=result_item['mode'])
    regex='<channel>(.+?)</channel>'
    m=re.compile(regex,re.DOTALL).findall(x)
    
    for item_xml in m:
        item = JenItem(item_xml)
        result_item = {
                    'label': item["name"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "next",
                    'url': item.get("externallink", "ignorme"),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'link':item.get("link", "ignorme"),
                    'json_rpc':item.get("jsonrpc", "ignorme"),
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    
                    'year': item.get("year", '0'),
                    'imdb': item.get("imdb", ''),
                    "summary": item.get("info", ' ')
                }
        url2,mode=get_url_mode(result_item,'dir')
        if mode==5:
            regex='\[COLOR (.+?)\]'
            r=re.compile(regex).findall(result_item['label'])
            if len(r)>0:
                repl_color=r[0]
            else:
                repl_color='white'
            result_item['label']=result_item['label'].replace('[COLOR=%s]'%repl_color,' ').replace('[COLOR %s]'%repl_color,' ').replace('[/COLOR]',' ')
            info=(PTN.parse(result_item['label']))
            video_data={}
            
            video_data['title']=info['title'].replace('=',' ').replace('[B]','').replace('[/B]','').replace('silver','').replace('deepskyblue','').replace('[','').replace(']','').replace('/COLOR','').replace('COLOR','').replace('4k','').replace('4K','').strip().replace('(','.').replace(')','.').replace(' ','.').replace('..','.')
            year=''
            if 'year' in info:
                year=info['year']
                video_data['year']=info['year']
            else:
               year=result_item['year']
               
            video_data['plot']=result_item['summary']
            
            addLink(result_item['label'],url2,mode,False,iconimage=result_item['icon'],fanart=result_item['fanart'],description=result_item['summary'],video_info=json.dumps(video_data),original_title=video_data['title'],data=year,id=result_item['imdb'])
        else:
            addDir3(result_item['label'],url2,mode,result_item['icon'],result_item['fanart'],result_item['summary'],original_title=result_item['label'])
    regex='<item>(.+?)</item>'
    m=re.compile(regex,re.DOTALL).findall(x)
    
    for item_xml in m:
        item = JenItem(item_xml)
        result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "next",
                    'url': item.get("externallink", "ignorme"),
                    'folder': True,
                    'imdb': "0",
                    'link':item.get("link", "ignorme"),
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'json_rpc':item.get("jsonrpc", "ignorme"),
                    'info': {},
                    'year': item.get("year", '0'),
                    'imdb': item.get("imdb", ''),
                    
                    "summary": item.get("info", ' ')
                }
        url2,mode=get_url_mode(result_item,'item')
        if mode==5:
            regex='\[COLOR (.+?)\]'
            r=re.compile(regex).findall(result_item['label'])
            if len(r)>0:
                repl_color=r[0]
            else:
                repl_color='white'
            result_item['label']=result_item['label'].replace('[COLOR %s]'%repl_color,' ').replace('[COLOR=%s]'%repl_color,' ').replace('[/COLOR]',' ')
            
            info=(PTN.parse(result_item['label']))
            video_data={}
            
            video_data['title']=info['title'].replace('[COLOR=%s]'%repl_color,' ').replace('=',' ').replace('[B]','').replace('[/B]','').replace('silver','').replace('deepskyblue','').replace('[','').replace(']','').replace('/COLOR','').replace('COLOR','').replace('4k','').replace('4K','').strip().replace('(','.').replace(')','.').replace(' ','.').replace('..','.')
            year=''
            
            if 'year' in info:
                year=info['year']
                video_data['year']=info['year']
            else:
               year=result_item['year']
            video_data['plot']=result_item['summary']
            addLink(result_item['label'],url2,mode,False,iconimage=result_item['icon'],fanart=result_item['fanart'],description=result_item['summary'],video_info=json.dumps(video_data),original_title=video_data['title'],data=year,id=result_item['imdb'])
        else:
            addDir3(result_item['label'],url2,mode,result_item['icon'],result_item['fanart'],result_item['summary'],original_title=result_item['label'])
    regex='<plugin>(.+?)</plugin>'
    m=re.compile(regex,re.DOTALL).findall(x)
    
    for item_xml in m:
        item = JenItem(item_xml)
        link = JenItem(item_xml)["link"]
        sublinks = JenItem(link).getAll("sublink")
        if sublinks:
            if len(sublinks) > 1:
                link = choose_quality(link)
            else:
                link = sublinks[0]
        link = link.replace("&amp;", "&")
        
        result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "next",
                    'url': item.get("externallink", "ignorme"),
                    'folder': True,
                    'imdb': "0",
                    'link':item.get("link", "ignorme"),
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'json_rpc':item.get("jsonrpc", "ignorme"),
                    'info': {},
                    'year': "0",
                    
                    "summary": item.get("info", ' ')
                }
        addDir3(result_item['label'],link,83,result_item['icon'],result_item['fanart'],result_item['summary'],original_title=result_item['label'])