import requests
import urlparse,logging
import re,random
import resolveurl as urlresolver
import xbmc,xbmcaddon,time


def clean_search(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?', ' ', title).lower()
    title = ' '.join(title.split())
    return title

def random_agent():
    BR_VERS = [
        ['%s.0' % i for i in xrange(18, 43)],
        ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111',
         '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
         '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124',
         '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
         '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
        ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1',
                'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES),
                                  br_ver=random.choice(BR_VERS[index]))
class source:
    domains = ['https://cmovies.cc']
    name = "Cmovies"
    

    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.base_link = 'https://cmovies.cc'
        self.sources2=[]
    def movie(self, imdb, title, localtitle, aliases, year):
        return title+'$$$$'+year+'$$$$'+imdb+'$$$$movie'
        
    def sources(self, url, hostDict, hostprDict):
        data=url.split('$$$$')
        title=data[0]
        year=data[1]
        imdb=data[2]
        if data[3]!='movie':
            return 0
    
        if 1:#try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        

            start_url = '%s/%s/' %(self.base_link,search_id.replace(' ','-'))         
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url                                  
            
            #headers={'User-Agent':random_agent()}
            #html = requests.get(start_url,headers=headers,timeout=5).content            
            
            #match = re.compile('class="span2 gallery-item".+?><a href="(.+?)">(.+?)</a></span>',re.DOTALL).findall(html) 
            #for item_url, name in match:
                #print 'scraperchk - scrape_movie - name: '+name
                #if year in name:
                    #print 'scraperchk - scrape_movie - item_url: '+item_url                                                           
                    #if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                        #print 'scraperchk - scrape_movie - Send this URL: ' + item_url                             
            self.get_source(start_url,title,year,start_time)                                      
            return self.sources2
        #except Exception, argument:
       


    def get_source(self,start_url,title,year,start_time):
        if 1:#try:
            #print 'PASSEDURL >>>>>>'+start_url
            count = 0
            headers={'User-Agent':random_agent()}
       
            OPEN = requests.get(start_url,headers=headers,timeout=5).content
            Endlinks = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for link1 in Endlinks:
                #print 'scraperchk - scrape_movie - link: '+str(link1)
                link='https:'+link1
                #print link+'?<<<<<<<<<<<<<<<<<<<,,,'     
                if '1080' in link:
                    qual = '1080p'
                if '720' in link:
                    qual = '720p'
                else:
                    qual = 'SD'
                    count+=1
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    self.sources2.append({'source':host, 'quality':qual,'language': 'en', 'url':link, 'direct':False, 'debridonly': False})
                        
            
        #except Exception, argument:
            
        #    return[]
    def resolve(self, url):
        return url