# -*- coding: utf-8 -*-

'''
 ***********************************************************
 * The Crew Add-on
 *
 *
 * @file trailer.py
 * @package script.module.thecrew
 *
 * @copyright (c) 2023, The Crew
 * @license GNU General Public License, version 3 (GPL-3.0)
 *
 ********************************************************cm*
'''

import sys
import simplejson as json
import re
import six
import time
import requests

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils
from resources.lib.modules import utils
from resources.lib.modules import cache
from resources.lib.modules import keys


class trailers:
    def __init__(self):
        try:

            self.session = requests.Session()


            self.imdb_baselink = 'https://www.imdb.com/_json/video/{}';
            self.tmdb_base = 'https://api.themoviedb.org/3'
            self.tmdb_user = control.setting('tm.personal_user') or control.setting('tm.user')
            self.tmdb_lang = control.apiLanguage()['tmdb']
            if not self.tmdb_user: self.tmdb_user = keys.tmdb_key
            self.tmdb_baselink = '';
            self.tmdb_url = '{}/{}/{}/videos?api_key={}&language=en-US'.format(self.tmdb_base,'{}', '{}', self.tmdb_user)
            self.show_url = 'https://api.themoviedb.org/3/tv/%s/videos?api_key=%s&include_video_language=%s' % ('%s', self.tmdb_user, self.tmdb_lang)
            self.base_link = 'https://www.youtube.com'
            self.base_link2 = 'https://youtube.com'
            self.base_link3 = 'https://youtu.be'
            self.yt_url = 'https://www.youtube.com/watch?v='
            self.yt_plugin_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s'
            self.name = ''
            self.url = ''
            self.meta = ''
            self.windowedtrailer = 0


            self.is_youtube_link = 'true' if 'youtu' in self.url else 'false'

            self.key = control.addon('plugin.video.youtube').getSetting('youtube.api.key');

            self.key_link = '&key=%s' % self.key
            self.search_link = 'https://www.googleapis.com/youtube/v3/search?part=id&type=video&maxResults=5&q=%s' + self.key_link
            self.youtube_watch = 'https://www.youtube.com/watch?v=%s'


        except Exception as e:
            import traceback
            failure = traceback.format_exc()
            log_utils.log('[CM Debug @ 62 in trailer.py]Traceback:: ' + str(failure))
            log_utils.log('[CM Debug @ 63 in trailer.py]Exception raised. Error = ' + str(e))
        pass


    def __del__(self):
        self.session.close()

    def get(self, name, url, imdb, tmdb, windowedtrailer):
        try:
            self.name = name
            self.url = url
            self.imdb = imdb
            self.tmdb = tmdb
            self.windowedtrailer = windowedtrailer


            #1. start with imdb
            #First try imdb
            result = self.getSources('imdb')

            #2. next, continue with tmdb
            # result = self.getSources('tmdb')
            # disabled tmdb and yt for now. Needs a yt secret api key for each user
            # and will still disable playback of trailers due to the fact that yt
            # doesn't allow for viewing videos without ad monetization


            if not result in ['canceled', 'empty'] and not result == '':
                self.play(result)
            else:
                if result == 'empty':
                    control.infoDialog('No trailers available.')
                elif result == 'canceled':
                    control.infoDialog('User canceled trailers')
                else:
                    control.infoDialog('Unexpexcted result in trailers')
        except:
            pass



    def play(self, result):
        try:
            if not self.imdb or self.imdb == '0': 
                raise Exception()
 
            url, title, plot, icon = result['video'], result['title'], result['plot'], result['icon']

            item = control.item(label=title, path=url)
            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon})
            item.setInfo(type='video', infoLabels={'title': title, 'plot': plot})
            item.setProperty('IsPlayable', 'true')
            control.resolve(handle=int(sys.argv[1]), succeeded=True, listitem=item)

            if self.windowedtrailer == 1:
                control.sleep(1000)
                while control.player.isPlayingVideo():
                    control.sleep(1000)
                control.execute('Dialog.Close(%s, true)' % control.getCurrentDialogId)

        except:
            pass


    def getSources(self, mode):
        try:
            if mode == 'imdb':
                result = cache.get(client.request, 72, self.imdb_baselink.format(self.imdb))
                items = utils.json_loads_as_str(result)

                listItems = items['playlists'][self.imdb]['listItems']
                videoMetadata = items['videoMetadata']
                trailer_list = []
                for item in listItems:
                    try:
                        metadata = videoMetadata[item['videoId']]
                        title = metadata['title']
                        icon = metadata['smallSlate']['url2x']
                        canoniculUrl = metadata['canonicalUrl']
                        plot = item.get('description') or title
                        related_to = metadata.get('primaryConst') or self.imdb

                        if (not related_to == self.imdb) and (not self.name.lower() in ' '.join((title, desc)).lower()):
                            continue

                        trailerUrl = [i['videoUrl'] for i in metadata['encodings'] if i['definition'] in ['1080', '720', '480p', '360p', 'SD']]
                        trailerUrl2 = 'https://imdb.com' + str(canoniculUrl)

                        if not trailerUrl: continue

                        trailer_list.append({'title': title, 'icon': icon, 'plot': plot, 'video': trailerUrl[0]})

                    except:
                        pass
            elif mode == 'tmdb':
                result = self.session.get(self.tmdb_url.format('tv', self.tmdb), timeout=16).json()

                listItems = result['results']
                trailer_list = []

                for item in listItems:
                    try:
                        title = item['name']
                        if item['site'] == 'YouTube':
                            trailerUrl = self.yt_plugin_url + str(item['key'])
                        else:
                            trailerUrl = ''
                        icon = control.addonThumb()
                        plot = title

                        if trailerUrl == '': continue

                        trailer_list.append({'title': title, 'icon': icon, 'plot': plot, 'video': trailerUrl})
                    except:
                        pass
            if not trailer_list: 
                return 'empty'

            try:

                if mode == 'imdb':
                    trailers = []
                    for t in trailer_list:
                        li = control.item(label=t['title'])
                        li.setArt({'icon': t['icon'], 'thumb': t['icon'], 'poster': t['icon']})
                        trailers.append(li)

                    select = control.selectDialog(trailers, control.lang(90220) % 'imdb', useDetails=True)

                    if select == -1: 
                        return 'canceled'
                    return trailer_list[select]


                elif mode == 'tmdb':
                    trailers = []
                    for t in trailer_list:
                        li = control.item(label=t['title'])
                        li.setArt({'icon': t['icon'], 'thumb': t['icon'], 'poster': t['icon']})
                        trailers.append(li)

                    select = control.selectDialog(trailers, control.lang(90220) % 'tmdb', useDetails=True)

                    if select == -1: 
                        return 'canceled'
                    return trailer_list[select]

                return trailer_list[0]

            except:
                pass
        except:
            pass