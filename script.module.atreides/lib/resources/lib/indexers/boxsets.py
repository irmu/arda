# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
#  As long as you retain this notice you can do whatever you want with this
# stuff. Just please ask before copying. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

'''
2020/01/11: Updates votes and rating block in imdb section
'''

import datetime
import json
import os
import re
import sys
import urllib

from resources.lib.modules import cleangenre, client, control, jsonmenu, metacache, playcount, trakt, views, workers

import xbmcplugin

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])
artPath = control.artPath()
addonFanart = control.addonFanart()


class boxsets:
    def __init__(self):
        self.boxset_list = []
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.tmdb_key = control.setting('tm.user')
        self.tmdb_link = 'https://api.themoviedb.org/3/list/%s?api_key=%s' % ('%s', self.tmdb_key)
        self.tmdb_c_link = 'https://api.themoviedb.org/3/collection/%s?api_key=%s' % ('%s', self.tmdb_key)
        self.tmdb_info_link = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=credits,releases,external_ids' % ('%s', self.tmdb_key, 'en')
        self.tmdb_image = 'http://image.tmdb.org/t/p/original'
        self.tmdb_poster = 'http://image.tmdb.org/t/p/w500'
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'
        self.tm_art_link = 'https://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % (
            '%s', self.tmdb_key, 'en')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/movies/%s'
        self.imdbinfo = 'http://www.omdbapi.com/?i=%s&plot=short&r=json'

    def get(self, mFile, mSection):
        rootMenu = jsonmenu.jsonMenu()
        rootMenu.load(mFile)
        rootMenu.process(mSection)

        if mSection == 'boxsets_main':
            self.endDirectory(category='Boxsets')
        else:
            mSection = mSection.split('_')[1].capitalize()
            self.endDirectory(contentType='movies', sortMethod=control.xDirSort.Label, category=mSection)

    def boxsetlist(self, url, list_id):
        if url == 'tmdbbox':
            list_url = self.tmdb_link % (list_id)
            self.tmdbBoxSetParser(list_url, list_id)
            self.worker()
            self.movieDirectory(self.boxset_list)
        elif url == 'tmdbbox':
            list_url = self.tmdb_c_link % (list_id)
            self.tmdbBoxSetParser(list_url, list_id)
            self.worker()
            self.movieDirectory(self.boxset_list)

    def tmdbBoxSetParser(self, url, list_id):
        try:
            content = client.request(url, timeout=10)
            result = json.loads(content)
            items = result['items']
        except Exception:
            return

        next = ''
        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = item['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')

                tmdb = item['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')

                poster = item['poster_path']
                if poster == '' or poster is None:
                    raise Exception()
                else:
                    poster = '%s%s' % (self.tmdb_poster, poster)
                poster = poster.encode('utf-8')

                fanart = item['backdrop_path']
                if fanart == '' or fanart is None:
                    fanart = '0'
                if not fanart == '0':
                    fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')

                premiered = item['release_date']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except Exception:
                    premiered = '0'
                premiered = premiered.encode('utf-8')

                rating = str(item['vote_average'])
                if rating == '' or rating is None:
                    rating = '0'
                rating = rating.encode('utf-8')

                votes = str(item['vote_count'])
                try:
                    votes = str(format(int(votes), ',d'))
                except Exception:
                    pass
                if votes == '' or votes is None:
                    votes = '0'
                votes = votes.encode('utf-8')

                plot = item['overview']
                if plot == '' or plot is None:
                    plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try:
                    tagline = tagline.encode('utf-8')
                except Exception:
                    pass

                self.boxset_list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered,
                                         'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes,
                                         'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot,
                                         'tagline': tagline, 'code': '0', 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0',
                                         'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except Exception:
                pass

        return self.boxset_list

    def worker(self, level=1):
        self.meta = []
        total = len(self.boxset_list)

        for i in range(0, total):
            self.boxset_list[i].update({'metacache': False})
        self.boxset_list = metacache.fetch(self.boxset_list, 'en')

        for r in range(0, total, 100):
            threads = []
            for i in range(r, r+100):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        self.boxset_list = [i for i in self.boxset_list]

        if len(self.meta) > 0:
            metacache.insert(self.meta)

    def super_info(self, i):
        try:
            if self.boxset_list[i]['metacache'] is True:
                raise Exception()

            try:
                tmdb = self.boxset_list[i]['tmdb']
            except Exception:
                tmdb = '0'

            if not tmdb == '0':
                url = self.tmdb_info_link % tmdb

            else:
                raise Exception()

            item = client.request(url, timeout='10')
            item = json.loads(item)

            title = item['title']
            if not title == '0':
                self.boxset_list[i].update({'title': title})

            year = item['release_date']
            try:
                year = re.compile('(\d{4})').findall(year)[0]
            except Exception:
                year = '0'
            if year == '' or year is None:
                year = '0'
            year = year.encode('utf-8')
            if not year == '0':
                self.boxset_list[i].update({'year': year})

            tmdb = item['id']
            if tmdb == '' or tmdb is None:
                tmdb = '0'
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            if not tmdb == '0':
                self.boxset_list[i].update({'tmdb': tmdb})

            imdb = item['imdb_id']
            if imdb == '' or imdb is None:
                imdb = '0'
            imdb = imdb.encode('utf-8')
            if not imdb == '0' and "tt" in imdb:
                self.boxset_list[i].update({'imdb': imdb, 'code': imdb})

            poster = item['poster_path']
            if poster == '' or poster is None:
                poster = '0'
            if not poster == '0':
                poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            if not poster == '0':
                self.boxset_list[i].update({'poster': poster})

            fanart = item['backdrop_path']
            if fanart == '' or fanart is None:
                fanart = '0'
            if not fanart == '0':
                fanart = '%s%s' % (self.tmdb_image, fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.boxset_list[i]['fanart'] == '0':
                self.boxset_list[i].update({'fanart': fanart})

            premiered = item['release_date']
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except Exception:
                premiered = '0'
            if premiered == '' or premiered is None:
                premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0':
                self.boxset_list[i].update({'premiered': premiered})

            studio = item['production_companies']
            try:
                studio = [x['name'] for x in studio][0]
            except Exception:
                studio = '0'
            if studio == '' or studio is None:
                studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0':
                self.boxset_list[i].update({'studio': studio})

            genre = item['genres']
            try:
                genre = [x['name'] for x in genre]
            except Exception:
                genre = '0'
            if genre == '' or genre is None or genre == []:
                genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0':
                self.boxset_list[i].update({'genre': genre})

            try:
                duration = str(item['runtime'])
            except Exception:
                duration = '0'
            if duration == '' or duration is None:
                duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0':
                self.boxset_list[i].update({'duration': duration})

            rating = str(item['vote_average'])
            if rating == '' or rating is None:
                rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0':
                self.boxset_list[i].update({'rating': rating})

            votes = str(item['vote_count'])
            try:
                votes = str(format(int(votes), ',d'))
            except Exception:
                pass
            if votes == '' or votes is None:
                votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0':
                self.boxset_list[i].update({'votes': votes})

            mpaa = item['releases']['countries']
            try:
                mpaa = [x for x in mpaa if not x['certification'] == '']
            except Exception:
                mpaa = '0'
            try:
                mpaa = ([x for x in mpaa if x['iso_3166_1'].encode('utf-8') == 'US'] + [x for x in mpaa if not x['iso_3166_1'].encode('utf-8') == 'US'])[0]['certification']
            except Exception:
                mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0':
                self.boxset_list[i].update({'mpaa': mpaa})

            director = item['credits']['crew']
            try:
                director = [x['name'] for x in director if x['job'].encode('utf-8') == 'Director']
            except Exception:
                director = '0'
            if director == '' or director is None or director == []:
                director = '0'
            director = ' / '.join(director)
            director = director.encode('utf-8')
            if not director == '0':
                self.boxset_list[i].update({'director': director})

            writer = item['credits']['crew']
            try:
                writer = [x['name'] for x in writer if x['job'].encode('utf-8') in ['Writer', 'Screenplay']]
            except Exception:
                writer = '0'
            try:
                writer = [x for n, x in enumerate(writer) if x not in writer[:n]]
            except Exception:
                writer = '0'
            if writer == '' or writer is None or writer == []:
                writer = '0'
            writer = ' / '.join(writer)
            writer = writer.encode('utf-8')
            if not writer == '0':
                self.boxset_list[i].update({'writer': writer})

            cast = item['credits']['cast']
            try:
                cast = [(x['name'].encode('utf-8'), x['character'].encode('utf-8')) for x in cast]
            except Exception:
                cast = []
            if len(cast) > 0:
                self.boxset_list[i].update({'cast': cast})

            plot = item['overview']
            if plot == '' or plot is None:
                plot = '0'
            plot = plot.encode('utf-8')
            if not plot == '0':
                self.boxset_list[i].update({'plot': plot})

            tagline = item['tagline']
            if (tagline == '' or tagline is None) and not plot == '0':
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            elif tagline == '' or tagline is None:
                tagline = '0'
            try:
                tagline = tagline.encode('utf-8')
            except Exception:
                pass
            if not tagline == '0':
                self.boxset_list[i].update({'tagline': tagline})

            # IMDB INFOS
            try:
                if imdb is not None or imdb == '0':
                    url = self.imdbinfo % imdb

                    item = client.request(url, timeout='10')
                    item = json.loads(item)

                    plot2 = item['Plot']
                    if plot2 == '' or plot2 is None:
                        plot = plot
                    plot = plot.encode('utf-8')
                    if not plot == '0':
                        self.boxset_list[i].update({'plot': plot})

                    rating2 = str(item['imdbRating'])
                    if rating2 == '' or rating2 is None:
                        rating2 = '0'
                    rating2 = rating2.encode('utf-8')
                    if not rating2 == '0':
                        self.boxset_list[i].update({'rating': rating2})

                    votes2 = str(item['imdbVotes'])
                    try:
                        votes2 = str(votes2)
                    except Exception:
                        pass
                    if votes2 == '' or votes2 is None:
                        votes2 = '0'
                    votes2 = votes2.encode('utf-8')
                    if not votes2 == '0':
                        self.boxset_list[i].update({'votes': votes2})
            except Exception:
                pass
            self.meta.append(
                {'tmdb': tmdb, 'imdb': imdb, 'tvdb': '0', 'lang': 'en',
                 'item':
                 {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster,
                  'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration,
                  'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast,
                  'plot': plot, 'tagline': tagline}})
        except Exception:
            pass

    def movieDirectory(self, items):
        if items is None or len(items) == 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        show_trailers = True if control.setting('showtrailers') == 'true' else False

        try:
            isOld = False
            control.item().getArt('type')
        except Exception:
            isOld = True

        isPlayable = 'true' if 'plugin' not in control.infoLabel('Container.PluginName') else 'false'

        indicators = playcount.getMovieIndicators()
        playbackMenu = control.lang(32063).encode('utf-8') if control.setting('hosts.mode') == '2' else control.lang(32064).encode('utf-8')
        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() is True else control.lang(32066).encode('utf-8')
        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() is True else control.lang(32067).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                sysname = urllib.quote_plus('%s (%s)' % (title, year))
                systitle = urllib.quote_plus(title)

                meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})
                # meta.update({'trailer': 'plugin://script.extendedinfo/?info=playtrailer&&id=%s' % imdb})
                if 'duration' not in i:
                    meta.update({'duration': '120'})
                elif i['duration'] == '0':
                    meta.update({'duration': '120'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except Exception:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], 'en')})
                except Exception:
                    pass

                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})

                sysmeta = urllib.quote_plus(json.dumps(meta))

                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                cm = []

                if show_trailers is True:
                    cm.append(('Watch Trailer', 'RunPlugin(%s?action=trailer&name=%s)' % (sysaddon, urllib.quote_plus(label))))

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except Exception:
                    pass

                if traktCredentials is True:
                    cm.append(
                        (traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' %
                         (sysaddon, sysname, imdb)))

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if isOld is True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))

                cm.append(
                    (addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' %
                     (sysaddon, sysname, systitle, year, imdb, tmdb)))

                item = control.item(label=label)

                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})

                if settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    item.setProperty('Fanart_Image', i['fanart2'])
                elif settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                elif addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels=meta)

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except Exception:
                pass

        try:
            url = items[0]['next']
            if url == '':
                raise Exception()

            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if addonFanart is not None:
                item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except Exception:
            pass

        # control.content(syshandle, 'movies')
        # control.directory(syshandle, cacheToDisc=True)
        # views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})
        self.endDirectory(contentType='movies', sortMethod=control.xDirSort.Label, category='Boxset List')

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        try:
            name = control.lang(name).encode('utf-8')
        except Exception:
            pass
        url = '%s?action=%s' % (sysaddon, query) if isAction is True else query
        if 'http' not in thumb:
            thumb = os.path.join(artPath, thumb) if artPath is not None else icon
        cm = []

        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if context is not None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if addonFanart is not None:
            item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, contentType='addons', sortMethod=control.xDirSort.NoSort, category=None):
        control.content(syshandle, contentType)
        if category is not None:
            control.category(syshandle, category)
        if sortMethod is not control.xDirSort.NoSort:
            control.sortMethod(syshandle, sortMethod)
        control.directory(syshandle, cacheToDisc=True)

    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                item = control.item(label=name)

                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')

                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
