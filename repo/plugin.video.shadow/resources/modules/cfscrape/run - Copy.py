                                                                
def get_tokens_with_headers(url,headers={},get_url=False):
    import requests                                                                    
    import cloudflare3x                                                                
                                                                                       
    s=requests.Session()                                                               
    
    headers2={                                                                          
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',                                                              
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',   
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',                                  
        'DNT': '1',                                                                    
        'Connection': 'keep-alive',                                                    
        'Upgrade-Insecure-Requests': '1',}
    if 'Referer' in headers:
        headers2['Referer']=headers['Referer']
    
    
    
    check = s.get(url,headers=headers2,timeout=10)                                               
                                                                                       
    cf = cloudflare3x.Cloudflare(url,check)
    result=''
    if cf.is_cloudflare:                                                               
        authUrl = cf.get_url()
       
        makeAuth = s.get(authUrl,headers=headers2,cookies=check.cookies,timeout=10)                                      
        result=makeAuth.content
    else:
        result='NOTCF'
    if get_url:
        result = s.get(url,headers=headers2,timeout=10)   
        result= result.url
    
    my_cookies = requests.utils.dict_from_cookiejar(s.cookies)
   
    found = ['%s=%s' % (name, value) for (name, value) in my_cookies.items()]
    kukz= ';'.join(found)
    end_c=[]
    end_c.append(my_cookies)
    end_c.append(headers2)
   
    return result,end_c
