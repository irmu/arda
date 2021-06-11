# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Welcome to House Atreides.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Atreides
# Addon id: plugin.video.atreides
# Addon Provider: House Atreides

import sys
import urllib
import urlparse

from resources.lib.modules import log_utils

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))

action = params.get('action')

subid = params.get('subid')

playbasic = params.get('playBasic')

resolved = params.get('resolved')

docu_category = params.get('docuCat')

docu_watch = params.get('docuPlay')

podcast_show = params.get('podcastshow')

page = params.get('page')

podcast_cat = params.get('podcastlist')

podcast_cats = params.get('podcastcategories')

podcast_episode = params.get('podcastepisode')

menu_title = params.get('menu_title')

menu_sort = params.get('menu_sort')

menu_file = params.get('menu_file')

menu_section = params.get('menu_section')

list_id = params.get('listid')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

tmdb = params.get('tmdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')

windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ("0", "1") else 0

if action is None:
    from resources.lib.indexers import navigator
    from resources.lib.modules import cache
    cache.cache_version_check()
    import service
    navigator.navigator().root()

elif action == 'newsNavigator':
    # from resources.lib.indexers import navigator
    # navigator.navigator().news()
    from resources.lib.dialogs import news
    news.load()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'bmNavigator':
    from resources.lib.modules import jsonbm
    if url == 'channels':
        jsonbm.jsonBookmarks().show_channels()
    elif url == 'podcasts':
        jsonbm.jsonBookmarks().show_podcasts()
    elif url == 'radio':
        jsonbm.jsonBookmarks().show_radio()

elif action == 'add_channel':
    from resources.lib.modules import jsonbm
    jsonbm.jsonBookmarks().add_channel(url)

elif action == 'remove_channel':
    from resources.lib.modules import jsonbm
    jsonbm.jsonBookmarks().rem_channel(url)

elif action == 'add_podcast':
    from resources.lib.modules import jsonbm
    jsonbm.jsonBookmarks().add_podcast(url)

elif action == 'remove_podcast':
    from resources.lib.modules import jsonbm
    jsonbm.jsonBookmarks().rem_podcast(url)

elif action == 'add_radio':
    from resources.lib.modules import jsonbm
    jsonbm.jsonBookmarks().add_radio(url)

elif action == 'remove_radio':
    from resources.lib.modules import jsonbm
    jsonbm.jsonBookmarks().rem_radio(url)

elif action == 'libraryNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().library()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.dialogs import cache
    cache.Cache_Dialog()

elif action == 'clearBaseCache':
    from resources.lib.modules import cache
    cache.cache_clear()

elif action == 'clearProviderCache':
    from resources.lib.modules import cache
    cache.cache_clear_providers()

elif action == 'clearMetaCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCacheMeta()

elif action == 'clearCacheSearch':
    from resources.lib.modules import cache
    cache.cache_clear_search()

elif action == 'clearAllCache':
    from resources.lib.modules import cache
    cache.cache_clear_all()

elif action == 'logViewer':
    from resources.lib.dialogs import logviewer
    logviewer.LogViewer(logfile='kodi.log')

elif action == 'bugReports':
    from resources.lib.dialogs import bugreports
    bugreports.BugReporter()

elif action == 'pairTools':
    from resources.lib.dialogs import pairing
    pairing.Pair_Dialog()

elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'movieSearchnew':
    from resources.lib.indexers import movies
    movies.movies().search_new()

elif action == 'movieSearchterm':
    from resources.lib.indexers import movies
    movies.movies().search_term(name)

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvSearchnew':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_new()

elif action == 'tvSearchterm':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search_term(name)

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvReviews':
    from resources.lib.indexers import youtube
    if subid is None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'openArtwork':
    from resources.lib.modules import control
    control.openSettings(query, 'script.atreides.artwork')

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()

elif action == 'customartwork':
    from resources.lib.modules import control
    control.chooseArtwork()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name, url, windowedtrailer)

elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()

elif action == 'menu':
    from resources.lib.indexers import navigator
    from resources.lib.modules import control
    if menu_sort is not None:
        nvar = 'control.xDirSort.' + menu_sort
        menu_sort = eval(nvar)
    else:
        menu_sort = control.xDirSort.NoSort
    navigator.navigator().jsonMenu(menu_file, menu_section, menuSort=menu_sort, menuCategory=menu_title)

elif action == 'urlResolver':
    try:
        import resolveurl
    except Exception:
        pass
    resolveurl.display_settings()

elif action == 'urlResolverRDTorrent':
    from resources.lib.modules import control
    control.openSettings(query, "script.module.resolveurl")

elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try:
        downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except Exception:
        pass

elif action == 'kidsBoxsetNavigator':
    from resources.lib.indexers import boxsets
    boxsets.boxsets().get(menu_file, menu_section)

elif action == 'b98Navigator':
    from resources.lib.indexers import anime
    anime.b98tv().root()

elif action == 'b98RabbitNav':
    from resources.lib.indexers import anime
    anime.b98tv().scrape(url)

elif action == 'b98CarrotLink':
    from resources.lib.indexers import anime
    anime.b98tv().play(url, title, image)

elif action == 'pbsKids':
    from resources.lib.indexers import anime
    if playbasic is not None:
        anime.pbskids().play(url)
    elif url is not None:
        anime.pbskids().scrape(url)
    else:
        anime.pbskids().root()

elif action == 'fitness':
    from resources.lib.indexers import youtube
    if subid is None:
        youtube.yt_index().root(action)
    else:
        youtube.yt_index().get(action, subid)

elif action == 'radio':
    from resources.lib.indexers import radio
    radio.radionet().get_stations(url)

elif action == 'radioCat':
    from resources.lib.indexers import radio
    radio.radionet().get_categories(url)

elif action == 'radioCatStations':
    from resources.lib.indexers import radio
    radio.radionet().get_category_stations(url)

elif action == 'radioPlayStation':
    from resources.lib.indexers import radio
    radio.radionet().play_station(url)

elif action == 'podcastNavigator':
    from resources.lib.indexers import podcast
    podcast.podcast().root()

elif action == 'podcastOne':
    from resources.lib.indexers import podcast
    if podcast_show is not None:
        podcast.podcast().pco_show(podcast_show, page)
    elif podcast_cat is not None:
        podcast.podcast().pco_cat(podcast_cat)
    elif podcast_cats is not None:
        podcast.podcast().pcocats_list()
    elif podcast_episode is not None:
        podcast.podcast().podcast_play(action, podcast_episode)
    else:
        podcast.podcast().pco_root()

elif action == 'boxsetNavigator':
    from resources.lib.indexers import boxsets
    boxsets.boxsets().get(menu_file, menu_section)

elif action == 'boxsetList':
    from resources.lib.indexers import boxsets
    boxsets.boxsets().boxsetlist(url, list_id)

elif action == 'docuNavigator':
    from resources.lib.indexers import docu
    docu.documentary().root()

elif action == 'docuTDNavigator':
    from resources.lib.indexers import docu
    if docu_category is not None:
        docu.topdocs().get(docu_category)
    elif docu_watch is not None:
        docu.topdocs().docu_play(docu_watch)
    else:
        docu.topdocs().get()

elif action == 'docuDHNavigator':
    from resources.lib.indexers import docu
    if docu_category is not None:
        docu.docuheaven().get(docu_category)
    elif docu_watch is not None:
        docu.docuheaven().docu_play(docu_watch)
    else:
        docu.docuheaven().get()

elif action == 'docuDSNavigator':
    from resources.lib.indexers import docu
    if docu_category is not None:
        docu.docustorm().docu_list(docu_category)
    elif docu_watch is not None:
        docu.docustorm().docu_play(docu_watch)
    else:
        docu.docustorm().root()

elif action == 'podbay':
    from resources.lib.indexers import podcast
    if podcast_show is not None:
        podcast.podcast().pb_show(podcast_show)
    elif podcast_cat is not None:
        podcast.podcast().pb_cat(podcast_cat)
    elif podcast_cats is not None:
        podcast.podcast().pb_root()
    elif podcast_episode is not None:
        podcast.podcast().podcast_play(action, podcast_episode)
    else:
        podcast.podcast().pb_root()

elif action == 'sectionItem':
    pass  # Placeholder. This is a non-clickable menu item for notes, etc.

elif action == 'play':
    from resources.lib.modules import sources
    sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.sources().playItem(title, source)

elif action == 'playSimple':
    from resources.lib.modules import sources
    sources.sources().playSimple(title, url, resolved)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.modules import sources
    sources.sources().clearSources()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.modules import control
    from random import randint
    import json
    try:
        rand = randint(1, len(rlist))-1
        for p in ['title', 'year', 'imdb', 'tvdb', 'season', 'episode', 'tvshowtitle', 'premiered', 'select']:
            if rtype == "show" and p == "tvshowtitle":
                try:
                    r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except Exception:
                    pass
            else:
                try:
                    r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except Exception:
                    pass
        try:
            r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except Exception:
            r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try:
                control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except Exception:
                pass
        elif rtype == "episode":
            try:
                control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except Exception:
                pass
        control.execute('RunPlugin(%s)' % r)
    except Exception:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)

elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()
