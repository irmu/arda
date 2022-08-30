import requests,re,time,logging,xbmc
def get_youtube_link(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.onlinevideoconverter.com/youtube-converter',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.onlinevideoconverter.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        data = {
          'function': 'validate',
          'args[dummy]': '1',
          'args[urlEntryUser]': url,
          'args[fromConvert]': 'urlconverter',
          'args[requestExt]': 'mp4',
          'args[nbRetry]': '0',
          'args[videoResolution]': '-1',
          'args[audioBitrate]': '0',
          'args[audioFrequency]': '0',
          'args[channel]': 'stereo',
          'args[volume]': '0',
          'args[startFrom]': '-1',
          'args[endTo]': '-1',
          'args[custom_resx]': '-1',
          'args[custom_resy]': '-1',
          'args[advSettings]': 'false',
          'args[aspectRatio]': '-1'
        }

        response = requests.post('https://www2.onlinevideoconverter.com/webservice', headers=headers, data=data).json()
        print (response)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.onlinevideoconverter.com/youtube-converter',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.onlinevideoconverter.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        data = {
          'function': 'processVideo',
          'args[dummy]': '1',
          'args[urlEntryUser]': url,
          'args[fromConvert]': 'urlconverter',
          'args[requestExt]': 'mp4',
          'args[serverId]': response['result']['serverId'],
          'args[nbRetry]': '0',
          'args[title]': response['result']['title'],
          'args[keyHash]': response['result']['keyHash'],
          'args[serverUrl]': response['result']['serverUrl'],
          'args[id_process]': response['result']['id_process'],
          'args[videoResolution]': '-1',
          'args[audioBitrate]': '0',
          'args[audioFrequency]': '0',
          'args[channel]': 'stereo',
          'args[volume]': '0',
          'args[startFrom]': '-1',
          'args[endTo]': '-1',
          'args[custom_resx]': '-1',
          'args[custom_resy]': '-1',
          'args[advSettings]': 'false',
          'args[aspectRatio]': '-1'
        }

        response2 = requests.post('https://www2.onlinevideoconverter.com/webservice', headers=headers, data=data).json()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.onlinevideoconverter.com/youtube-converter',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers',
        }

        data = {
          'id': response2['result']['dPageId']
        }

        html = requests.post('https://www.onlinevideoconverter.com/success', headers=headers, data=data).content
        
        regex="'url': '(.+?)'"
        match=re.compile(regex).findall(str(html))
        return match[0]
def get_youtube_link2(url):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://bitdownloader.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }

    params = (
        ('video', url),
    )

    response = requests.get('https://bitdownloader.com/download', headers=headers, params=params).content

  
    regex=' download="(.+?)" href="(.+?)"'
    match=re.compile(regex).findall(response)
    all_results=[]
    for name,link in match:
       
        return link.replace('&amp;','&')
        all_results.append((name,link.replace('&amp;','&')))
def get_youtube_link3(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }



    response = requests.get('https://api.videograbber.net/api/video?uri='+url.encode('base64'), headers=headers).json()
    return response['data']['formats'][len(response['data']['formats'])-1]['url']

def get_youtube_link4(videoid):
    
    logging.warning(videoid)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://keepvid.pro/download?video=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D'+videoid,
        'Content-Type': 'application/json',
        'Origin': 'https://keepvid.pro',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = '{"type":"crawler","params":{"video_url":"https://www.youtube.com/watch?v=%s"}}'%videoid
    
    response = requests.post('https://v2api.keepvid.pro/v1/job', headers=headers, data=data).json()

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://keepvid.pro/download?video=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D'+videoid,
        'Content-Type': 'application/json',
        'Origin': 'https://keepvid.pro',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    params = (
        ('type', 'crawler'),
        ('job_id', response['data']['job_id']),
    )
    counter=0
    while 1:
        response = requests.get('https://v2api.keepvid.pro/v1/check', headers=headers, params=params).json()
        logging.warning(response)
        if response['data']['state']!='active':
            break
     
        xbmc.sleep(10)
        counter+=1
        if counter>100:
            return ''
    return(response['data']['formats'][len(response['data']['formats'])-1]['url'])
