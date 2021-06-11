# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# As long as you retain this notice you can do whatever you want with
# this stuff. If we meet some day, and you think this stuff is worth it,
# you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import json
import requests
import traceback

from resources.lib.modules import control, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 0
        self.source = ['www']
        self.domain = 'furk.net/'
        self.base_link = 'https://www.furk.net'
        self.meta_search_link = "/api/plugins/metasearch?api_key=%s&q=%s&cached=yes" \
                                "&match=%s&moderated=%s%s&sort=relevance&type=video&offset=0&limit=%s"
        self.tfile_link = "/api/file/get?api_key=%s&t_files=1&id=%s"
        self.login_link = "/api/login/login?login=%s&pwd=%s"
        self.user_name = control.setting('furk.user_name')
        self.user_pass = control.setting('furk.user_pass')
        self.api_key = control.setting('furk.api')
        self.search_limit = control.setting('furk.limit')
        self.mod_level = control.setting('furk.mod.level').lower()

    def verify_settings(self):
        try:
            api_key = self.api_key

            if api_key == '':
                if self.user_name == '' or self.user_pass == '':
                    return False
            else:
                return True
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FurkIt - Exception: \n' + str(failure))
            return False

    def get_api(self):
        try:
            api_key = self.api_key

            if api_key == '':
                if self.user_name == '' or self.user_pass == '':
                    return

                else:
                    s = requests.Session()
                    link = (self.base_link + self.login_link % (self.user_name, self.user_pass))
                    p = s.post(link)
                    p = json.loads(p.text)

                    if p['status'] == 'ok':
                        api_key = p['api_key']
                        control.setSetting('furk.api', api_key)
                    else:
                        pass

            return api_key
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FurkIt - Exception: \n' + str(failure))
            pass

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            if self.verify_settings() is False:
                return
            url = {'imdb': imdb, 'title': title, 'year': year}
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FurkIt - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            if self.verify_settings() is False:
                return
            url = tvshowtitle
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FurkIt - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if self.verify_settings() is False:
                return
            url = {'tvshowtitle': url, 'season': season, 'episode': episode}
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FurkIt - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict, sc_timeout):
        if url is None:
            return

        api_key = self.get_api()

        if not api_key:
            return

        sources = []

        try:
            content_type = 'episode' if 'tvshowtitle' in url else 'movie'
            match = 'all'
            moderated = 'no' if content_type == 'episode' else self.mod_level
            search_in = ''

            if content_type == 'movie':
                title = url['title'].replace(':', ' ').replace(' ', '+').replace('&', 'and')
                title = title.replace("'", "")
                year = url['year']
                link = '{0}+{1}'.format(title, year)

            elif content_type == 'episode':
                title = url['tvshowtitle'].replace(':', ' ').replace(' ', '+').replace('&', 'and')
                season = int(url['season'])
                episode = int(url['episode'])
                # season00 = 's%02d' % (season)
                season00_ep00_SE = 's%02de%02d' % (season, episode)
                season0_ep0_SE = 's%de%d' % (season, episode)
                season00_ep00_X = '%02dx%02d' % (season, episode)
                season0_ep0_X = '%dx%d' % (season, episode)
                season0_ep00_X = '%dx%02d' % (season, episode)
                link = '%s+%s' \
                       % (title, season00_ep00_SE)

            s = requests.Session()
            link = (
                self.base_link + self.meta_search_link % (
                    api_key, link, match, moderated, search_in, self.search_limit))

            timer = control.Time(start=True)

            p = s.get(link)
            p = json.loads(p.text)

            if p['status'] != 'ok':
                return

            files = p['files']

            for i in files:
                # Stop searching 8 seconds before the provider timeout, otherwise might continue searching, not complete in time, and therefore not returning any links.
                if timer.elapsed() > sc_timeout:
                    log_utils.log('Furk - Timeout Reached')
                    break

                if i['is_ready'] == '1' and i['type'] == 'video':
                    try:
                        source = 'SINGLE'
                        if int(i['files_num_video']) > 3:
                            source = 'PACK [B](x%02d)[/B]' % int(i['files_num_video'])
                        file_name = i['name']
                        file_id = i['id']
                        file_dl = i['url_dl']
                        if content_type == 'episode':
                            url = '%s<>%s<>%s<>%s<>%s<>%s' % (
                                file_id, season00_ep00_SE, season0_ep0_SE, season00_ep00_X, season0_ep0_X,
                                season0_ep00_X)
                            details = self.details(file_name, i['size'], i['video_info'])
                        else:
                            url = '%s<>%s<>%s+%s' % (file_id, 'movie', title, year)
                            details = self.details(file_name, i['size'], i['video_info']).split('|')
                            details = details[0] + ' | ' + file_name.replace('.', ' ')

                        quality = source_utils.get_release_quality(file_name, file_dl)
                        sources.append({'source': source,
                                        'quality': quality[0],
                                        'language': "en",
                                        'url': url,
                                        'info': details,
                                        'direct': True,
                                        'debridonly': False})
                    except Exception:
                        pass
                else:
                    continue
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FurkIt - Exception: \n' + str(failure))
            pass

    def resolve(self, url):
        try:
            info = url.split('<>')
            file_id = info[0]
            content_type = 'movie' if info[1] == 'movie' else 'episode'

            filtering_list = info[1:]

            link = (self.base_link + self.tfile_link % (self.api_key, file_id))
            s = requests.Session()
            p = s.get(link)
            p = json.loads(p.text)

            if p['status'] != 'ok' or p['found_files'] != '1':
                return

            files = p['files']
            files = (files[0])['t_files']

            for i in files:
                name = i['name']
                # ct = i['ct']
                if 'video' in i['ct']:
                    if content_type == 'movie':
                        if name.lower() != 'rarbg.mp4' and name.lower() != 'rarbg.mkv' and 'furk320' not in name.lower() and 'sample' not in name.lower() and not name.lower().endswith(
                                'sub'):
                            if int(i['size']) > 150:
                                mv_title = str(info[2]).split('+')
                                fail = 0
                                for word in mv_title:
                                    if word.lower() not in name.lower():
                                        if word != 'and':
                                            fail += 1
                                            break
                                if fail == 0:
                                    url = i['url_dl']
                            else:
                                pass
                    else:
                        if 'furk320' not in name.lower() and 'sample' not in name.lower():
                            for x in filtering_list:
                                if x in name.lower():
                                    url = i['url_dl']
                                else:
                                    pass
                else:
                    pass
            log_utils.log('Furkin Resolve: ' + str(url))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FurkIt - Exception: \n' + str(failure))
            pass

    def details(self, name, size, video_info):
        import HTMLParser
        import re

        name = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", name)
        name = HTMLParser.HTMLParser().unescape(name)
        name = name.replace("&quot;", "\"")
        name = name.replace("&amp;", "&")
        size = float(size) / 1073741824
        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', name)
        fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
        fmt = [x.lower() for x in fmt]
        info = video_info.replace('\n', '')
        v = re.compile('Video: (.+?),').findall(info)[0]
        a = re.compile('Audio: (.+?), .+?, (.+?),').findall(info)[0]
        if '3d' in fmt:
            q = '  | 3D'
        else:
            q = ''
        info = '%.2f GB%s | %s | %s | %s' % (size, q, v, a[0], a[1])
        info = re.sub('\(.+?\)', '', info)
        info = info.replace('stereo', '2.0')
        info = info.replace('eac3', 'dd+')
        info = info.replace('ac3', 'dd')
        info = ' '.join(info.split())

        return info
