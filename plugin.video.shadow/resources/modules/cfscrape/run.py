
def get_tokens_with_headers(url,headers={},get_url=False):
    import cfscrape,requests
    s=cfscrape.CloudflareScraper()
    
    import requests                                                                    
                                                             
                                                                                       
                                            
    
    headers2={                                                                          
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',                                                              
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',   
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',                                  
        'DNT': '1',                                                                    
        'Connection': 'keep-alive',                                                    
        'Upgrade-Insecure-Requests': '1',}
    if 'Referer' in headers:
        headers2['Referer']=headers['Referer']
    
    s.headers.update(headers2)
    r=s.get(url)
    my_cookies = requests.utils.dict_from_cookiejar(s.cookies)
    result=r.content

    if get_url:
        
        result= r.url
    
    my_cookies = requests.utils.dict_from_cookiejar(s.cookies)

    end_c=[]
    end_c.append(my_cookies)
    end_c.append(headers2)
   
    return result,end_c
