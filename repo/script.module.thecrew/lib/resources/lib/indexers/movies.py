# -*- coding: utf-8 -*-

'''
 ***********************************************************
 * The Crew Add-on
 *
 *
 * @file movies.py
 * @package script.module.thecrew
 *
 * @copyright (c) 2023, The Crew
 * @license GNU General Public License, version 3 (GPL-3.0)
 *
 ********************************************************cm*
'''

from resources.lib.modules import trakt
from resources.lib.modules import keys
from resources.lib.modules import bookmarks
from resources.lib.modules import cleangenre
from resources.lib.modules import cleantitle
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.modules import log_utils
from resources.lib.indexers import navigator

import os,sys,re,datetime,base64,traceback
import json
import urllib
import requests

from urllib.parse import quote_plus, parse_qsl, urlparse, urlsplit, urlencode


try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

import six
from six.moves import zip, range

params = dict(urllib.parse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')

class movies:
    def __init__(self):
        self.count = int(control.setting('page.item.limit'))
        self.list = []

        self.session = requests.Session()

        self.showunaired = control.setting('showunaired') or 'true'

        self.imdb_link = 'https://www.imdb.com'
        self.trakt_link = 'https://api.trakt.tv'

        #####
        # dates
        self.datetime = datetime.datetime.utcnow()
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.year_date = (self.datetime - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.year = self.datetime.strftime('%Y')
        self.country = control.setting('official.country') or 'US'


        #####
        # users
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tm_user = control.setting('tm.user')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))

        self.tmdb_user = control.setting('tm.personal_user') or control.setting('tm.user')
        if not self.tmdb_user: self.tmdb_user = base64.b64decode('MDA0OTc5NWVkYjU3NTY4Yjk1MjQwYmM5ZTYxYTlkZmM=')

        self.fanart_tv_headers = {'api-key': keys.fanart_key}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

        self.fanart_tv_headers = {'api-key': '39b90a017e391afd33750f97827f8d96'}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})



        self.lang = control.apiLanguage()['trakt']

        self.hidecinema = control.setting('hidecinema')
        self.hidecinema_rollback = int(control.setting('hidecinema.rollback'))
        self.hidecinema_rollback2 = self.hidecinema_rollback * 30
        self.hidecinema_date = (datetime.date.today() - datetime.timedelta(days=self.hidecinema_rollback2)).strftime('%Y-%m')

        self.search_link = 'https://api.trakt.tv/search/movie?limit=20&page=1&query='
        self.fanart_tv_art_link = 'https://webservice.fanart.tv/v3/movies/%s'
        self.fanart_tv_level_link = 'https://webservice.fanart.tv/v3/level'
        self.tm_art_link = 'https://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % ('%s', self.tm_user, self.lang)
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'

        self.persons_link = 'https://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'https://www.imdb.com/search/name?count=100&gender=male,female'
        self.person_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&role=%s&sort=year,desc&count=%d&start=1' % ('%s', self.count)
        self.keyword_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&keywords=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
        self.oscars_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=%d&start=1' % self.count
        self.oscarsnominees_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_nominees&sort=year,desc&count=%d&start=1' % self.count
        self.theaters_link = 'https://www.imdb.com/search/title?title_type=feature&num_votes=1000,&release_date=date[365],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.year_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', '%s', self.count)

        if self.hidecinema == 'true':
            self.popular_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&release_date=,%s&sort=moviemeter,asc&count=%d&start=1' % (self.hidecinema_date, self.count)
            self.views_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=,%s&sort=num_votes,desc&count=%d&start=1' % (self.hidecinema_date, self.count)
            self.featured_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=,%s&sort=moviemeter,asc&count=%d&start=1' % (self.hidecinema_date, self.count)
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,%s&genres=%s&sort=moviemeter,asc&count=%d&start=1' % (self.hidecinema_date, '%s', self.count)
            self.language_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&release_date=,%s&count=%d&start=1' % ('%s', self.hidecinema_date, self.count)
            self.certification_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=%s&sort=moviemeter,asc&release_date=,%s&count=%d&start=1' % ('%s', self.hidecinema_date, self.count)
            self.boxoffice_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&release_date=,%s&count=%d&start=1' % (self.hidecinema_date, self.count)
        else:
            self.popular_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=%d&start=1' % self.count
            self.views_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=%d&start=1' % self.count
            self.featured_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=moviemeter,asc&count=%d&start=1' % self.count
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
            self.language_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
            self.certification_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=%s&sort=moviemeter,asc&count=%d&start=1' % ('%s', self.count)
            self.boxoffice_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&count=%d&start=1' % self.count

        self.top100_link = 'https://www.imdb.com/search/title?title_type=feature&groups=top_100&count=%d&start=1' % self.count
        self.top250_link = 'https://www.imdb.com/search/title?title_type=feature&groups=top_250&count=%d&start=1' % self.count
        self.top1000_link = 'https://www.imdb.com/search/title?title_type=feature&groups=top_1000&count=%d&start=1' % self.count
        self.rated_g_link = 'https://www.imdb.com/search/title/?certificates=US%3AG'
        self.rated_pg13_link = 'https://www.imdb.com/search/title/?certificates=US%3APG-13'
        self.rated_pg_link = 'https://www.imdb.com/search/title/?certificates=US%3APG'
        self.rated_r_link = 'https://www.imdb.com/search/title/?certificates=US%3AR'
        self.rated_nc17_link = 'https://www.imdb.com/search/title/?certificates=US%3ANC-17'
        self.bestdirector_link = 'https://www.imdb.com/search/title?title_type=feature&groups=best_director_winner&sort=user_rating,desc&count=%d&start=1' % self.count
        self.national_film_board_link = 'https://www.imdb.com/search/title?title_type=feature&groups=national_film_preservation_board_winner&sort=user_rating,desc&count=%d&start=1' % self.count
        self.dreamworks_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=dreamworks&count=%d&start=1' % self.count
        self.fox_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=fox&count=%d&start=1' % self.count
        self.paramount_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=paramount&count=%d&start=1' % self.count
        self.mgm_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=mgm&count=%d&start=1' % self.count
        self.universal_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=universal&count=%d&start=1' % self.count
        self.sony_pictures_link = 'https://www.imdb.com/search/title?title_type=feature&companies=sony&count=%d&start=1' % self.count
        self.warnerbrothers_pictures = 'https://www.imdb.com/search/title?title_type=feature&companies=warner&count=%d&start=1' % self.count
        self.amazon_prime_link = 'https://www.imdb.com/search/title?title_type=feature&online_availability=US%2Ftoday%2FAmazon%2Fsubs'
        self.disney_pictures_link = 'https://www.imdb.com/search/title?user_rating=1.0,10.0&companies=disney&count=%d&start=1' % self.count
        self.family_movies_link = 'https://www.imdb.com/search/title/?title_type=feature&genres=family&count=%d&start=1' % self.count
        self.classic_movies_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&count=%d&start=1' % self.count
        self.classic_horror_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=horror&count=%d&start=1' % self.count
        self.classic_fantasy_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=fantasy&count=%d&start=1' % self.count
        self.classic_western_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=western&count=%d&start=1' % self.count
        self.classic_annimation_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=animation&count=%d&start=1' % self.count
        self.classic_war_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=war&count=%d&start=1' % self.count
        self.classic_scifi_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=sci_fi&count=%d&start=1' % self.count
        self.eighties_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1980-01-01,1989-12-31&count=%d&start=1' % self.count
        self.nineties_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1990-01-01,1999-12-31&count=%d&start=1' % self.count
        self.thousands_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2010-12-31&count=%d&start=1' % self.count
        self.twentyten_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=2010-01-01,2019-12-31&count=%d&start=1' % self.count
        self.advancedsearchtrending_link = 'https://www.imdb.com/search/title?title_type=feature&genres=animation,family&sort=moviemeter,asc&page=1&ref_=adv_prv'
        self.collectionsactionhero_link = 'https://www.imdb.com/search/keyword/?keywords=action-hero&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=7846868c-8414-4178-8f43-9ad6b2ef0baf&pf_rd_r=N2RAG179F05MS9C7TEF4&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=moka&ref_=kw_1&sort=num_votes,desc&mode=detail&page=1'
        self.advancedsearchdcvsmarvel_link = 'https://www.imdb.com/list/ls065237713/?sort=alpha,asc&st_dt=&mode=detail&page=1'

        self.added_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&languages=en&num_votes=500,&production_status=released&release_date=%s,%s&sort=release_date,desc&count=20&start=1' % (self.year_date, self.today_date)
        self.trending_link = 'https://api.trakt.tv/movies/trending?limit=%d&page=1' % self.count
        self.traktlists_link = 'https://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'https://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'https://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'https://api.trakt.tv/users/me/collection/movies'
        self.traktwatchlist_link = 'https://api.trakt.tv/users/me/watchlist/movies'
        self.traktfeatured_link = 'https://api.trakt.tv/recommendations/movies?limit=%d' % self.count
        self.trakthistory_link = 'https://api.trakt.tv/users/me/history/movies?limit=%d&page=1' % self.count
        self.onDeck_link = 'https://api.trakt.tv/sync/playback/movies?extended=full&limit=%d' % self.count
        self.imdblists_link = 'https://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'https://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=movie,short,tvMovie,tvSpecial,video&start=1'
        self.imdblist2_link = 'https://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=movie,short,tvMovie,tvSpecial,video&start=1'
        self.imdbwatchlist_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user

        ######
        #tmdb
        #
        self.tmdb_link = 'https://api.themoviedb.org/3/'
        self.tmdb_img_link = 'https://image.tmdb.org/t/p/w%s%s'
        self.tmdb_img_prelink = 'https://image.tmdb.org/t/p/{}{}'
        self.tmdb_user = control.setting('tm.personal_user') or control.setting('tm.user')
        if not self.tmdb_user: self.tmdb_user = base64.b64decode('MDA0OTc5NWVkYjU3NTY4Yjk1MjQwYmM5ZTYxYTlkZmM=')

        self.tmdb_by_imdb = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % ('%s', self.tmdb_user)
        self.tm_search_link = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=1' % (self.tmdb_user, '%s')
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'
        self.related_link = 'https://api.themoviedb.org/3/movie/%s/similar?api_key=%s&page=1' % ('%s', self.tmdb_user)
        self.tmdb_providers_link = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&sort_by=popularity.desc&with_watch_providers=%s&watch_region=%s&page=1' % (self.tmdb_user, '%s', self.country)
        self.tmdb_art_link = 'https://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % ('%s', self.tmdb_user, self.lang)




        self.tmdb_api_link = ('{}movie/{}?api_key={}&language={}&append_to_response=aggregate_credits,content_ratings,external_ids').format(self.tmdb_link, '%s', self.tmdb_user, self.lang)
        #self.tmdb_networks_link = ('{}discover/movie?api_key={}&sort_by=popularity.desc&with_networks={}&page=1').format(self.tmdb_link, self.tmdb_user, '%s')
        #self.tmdb_networks_link = ('{}discover/movie?api_key={}&first_air_date.lte={}&sort_by=first_air_date.desc&with_networks={}&page=1').format(self.tmdb_link, self.tmdb_user, self.today_date, '%s')
        self.tmdb_networks_link_no_unaired = ('{}discover/movie?api_key={}&first_air_date.lte={}&sort_by=first_air_date.desc&with_networks={}&page=1').format(self.tmdb_link, self.tmdb_user, self.today_date, '%s')
        #self.tmdb_networks_link = ('{}discover/movie?api_key={}&include_video=true&language=en-US&release_date.lte={}&with_networks={}&sort_by=primary_release_date.desc&page=1').format(self.tmdb_link, self.tmdb_user, self.today_date, '%s')
        self.tmdb_networks_link = ('{}discover/movie?api_key={}&with_networks={}&language=en-US&release_date.lte={}&sort_by=primary_release_date.desc&page=1').format(self.tmdb_link, self.tmdb_user, '%s', self.today_date)




        self.tmdb_search_movie_link = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=1' % (self.tmdb_user, '%s')
        self.search_link = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=1' % (self.tmdb_user, '%s')
        self.related_link = 'https://api.themoviedb.org/3/movie/%s/similar?api_key=%s&page=1' % ('%s', self.tmdb_user)

        self.tmdb_info_tvshow_link = ('{}{}/{}?api_key={}&language={}&append_to_response=images').format(self.tmdb_link, 'movie', '%s', self.tmdb_user, self.lang)
        self.tmdb_by_imdb = ('{}find/{}?api_key={}&external_source=imdb_id').format(self.tmdb_link, '%s', self.tmdb_user)

        self.tmdb_movie_top_rated_link = ('{}{}/{}?api_key={}&language={}&sort_by=popularity.desc&page=1').format(self.tmdb_link, 'movie', 'top_rated', self.tmdb_user, self.lang)
        self.tmdb_movie_popular_link = ('{}{}/{}?api_key={}&language={}&page=1').format(self.tmdb_link, 'movie', 'popular', self.tmdb_user, self.lang)
        self.tmdb_movie_trending_day_link = ('{}/{}/{}/{}?api_key={}').format(self.tmdb_link, 'trending', 'movie', 'day', self.tmdb_user)
        self.tmdb_movie_trending_week_link = ('{}/{}/{}/{}?api_key={}').format(self.tmdb_link, 'trending', 'movie', 'week', self.tmdb_user)
        self.tmdb_movie_discover_year_link = ('{}{}/{}?api_key={}&language=%s&sort_by=popularity.desc&first_air_date_year={}&include_null_first_air_dates=false&with_original_language=en&page=1').format(self.tmdb_link, 'discover', 'movie', self.tmdb_user, self.year)



#######HALLOWEEN########
        self.halloween_imdb_link = 'https://www.imdb.com/list/ls066334100/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count
        self.halloween_top_100_link = 'https://www.imdb.com/list/ls000091321/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count
        self.halloween_best_link = 'https://www.imdb.com/list/ls052042029/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count
        self.halloween_great_link = 'https://www.imdb.com/list/ls050722485/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count

#######HOLIDAY########
        self.top50_holiday_link = 'https://www.imdb.com/list/ls003988974/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count
        self.best_holiday_link = 'https://www.imdb.com/list/ls053245198/?sort=user_rating,desc&st_dt=&mode=detail&page=1&count=%d&start=1' % self.count

    def __del__(self):
        self.session.close()

    def get(self, url, tid=0, idx=True, create_directory=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass

            try:
                u = urllib.parse.urlparse(url).netloc.lower()
            except:
                pass

            if self.trakt_link in url and url == self.onDeck_link:
                self.blist = cache.get(self.trakt_list, 720, url, self.trakt_user)
                self.list = []
                self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)
                self.list = self.list[::-1]

                if idx == True: self.worker()

            elif u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakthistory_link:
                        raise Exception()
                    if not '/users/me/' in url:
                        raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user):
                        raise Exception()
                    self.list = cache.get(
                        self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)

                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))

                if idx == True: self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True: self.worker()

            elif u in self.trakt_link and '/sync/playback/' in url:
                self.list = self.trakt_list(url, self.trakt_user)
                self.list = sorted(self.list, key=lambda k: int(k['paused_at']), reverse=True)
                if idx == True: self.worker()

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True: self.worker()

            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True: self.worker()

            elif u in self.imdb_link:
                #self.list = cache.get(self.imdb_list, 24, url)
                self.list = self.imdb_list(url)
                if idx == True: self.worker()

            elif u in self.tmdb_networks_link:
                #self.list = cache.get(self.tmdb_list, 24, url, id)
                self.list = self.tmdb_list(url, tid)
                if idx == True: self.worker()

            elif u in self.tmdb_link:
                #self.list = cache.get(self.tmdb_list, 24, url)
                self.list = self.tmdb_list(url)
                if idx == True: self.worker()

            if idx == True and create_directory == True:
                self.movieDirectory(self.list)
            return self.list
        except:
            pass

    def widget(self):

        setting = control.setting('movie.widget')

        if setting == '2':
            self.get(self.trending_link)
        elif setting == '3':
            self.get(self.popular_link)
        elif setting == '4':
            self.get(self.theaters_link)
        elif setting == '5':
            self.get(self.added_link)
        else:
            self.get(self.featured_link)

    def search(self):
        navigator.navigator().addDirectoryItem(32603, 'movieSearchnew', 'search.png', 'DefaultMovies.png')

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()

        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS movies (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except:
            pass

        dbcur.execute("SELECT * FROM movies ORDER BY ID DESC")
        lst = []

        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.navigator().addDirectoryItem(term, 'movieSearchterm&name=%s' % term, 'search.png', 'DefaultMovies.png')
                lst += [(term)]
        dbcur.close()

        if delete_option:
            navigator.navigator().addDirectoryItem(32605, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')

        navigator.navigator().endDirectory()

    def search_new(self):
        control.idle()

        t = control.lang(32010)
        k = control.keyboard('', t)
        k.doModal()
        q = k.getText() if k.isConfirmed() else None

        if not q: return

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM movies WHERE term = ?", (q,))
        dbcur.execute("INSERT INTO movies VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.search_link % urllib.parse.quote_plus(q)
        self.get(url)

    def search_term(self, name):
        url = self.search_link % urllib.parse.quote_plus(name)
        self.get(url)

    def person(self):
        try:
            t = control.lang(32010)
            k = control.keyboard('', t)
            k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''): return

            url = self.persons_link + urllib.parse.quote_plus(q)
            self.persons(url)
        except:
            return


# TC 2/01/19 started
    def genres(self):
        genres = [
            ('Action', 'action', True),
            ('Adventure', 'adventure', True),
            ('Animation', 'animation', True),
            ('Anime', 'anime', False),
            ('Biography', 'biography', True),
            ('Comedy', 'comedy', True),
            ('Crime', 'crime', True),
            ('Documentary', 'documentary', True),
            ('Drama', 'drama', True),
            ('Family', 'family', True),
            ('Fantasy', 'fantasy', True),
            ('History', 'history', True),
            ('Horror', 'horror', True),
            ('Music ', 'music', True),
            ('Musical', 'musical', True),
            ('Mystery', 'mystery', True),
            ('Romance', 'romance', True),
            ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True),
            ('Thriller', 'thriller', True),
            ('War', 'war', True),
            ('Western', 'western', True)
        ]

        for i in genres:
            self.list.append(
                {
                    'name': cleangenre.lang(i[0], self.lang),
                    'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                    'image': 'genres.png',
                    'action': 'movies'
                })

        self.addDirectory(self.list)
        return self.list

    def languages(self):
        languages = [
            ('Arabic', 'ar'),
            ('Bosnian', 'bs'),
            ('Bulgarian', 'bg'),
            ('Chinese', 'zh'),
            ('Croatian', 'hr'),
            ('Dutch', 'nl'),
            ('English', 'en'),
            ('Finnish', 'fi'),
            ('French', 'fr'),
            ('German', 'de'),
            ('Greek', 'el'),
            ('Hebrew', 'he'),
            ('Hindi ', 'hi'),
            ('Hungarian', 'hu'),
            ('Icelandic', 'is'),
            ('Italian', 'it'),
            ('Japanese', 'ja'),
            ('Korean', 'ko'),
            ('Macedonian', 'mk'),
            ('Norwegian', 'no'),
            ('Persian', 'fa'),
            ('Polish', 'pl'),
            ('Portuguese', 'pt'),
            ('Punjabi', 'pa'),
            ('Romanian', 'ro'),
            ('Russian', 'ru'),
            ('Serbian', 'sr'),
            ('Slovenian', 'sl'),
            ('Spanish', 'es'),
            ('Swedish', 'sv'),
            ('Turkish', 'tr'),
            ('Ukrainian', 'uk')
        ]

        for i in languages:
            self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'international.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def certifications(self):
        certificates = ['[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]G[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]', '[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]PG[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]',
                        '[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]PG-13[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]', '[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]R[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]', '[COLOR dodgerblue][B]¤[/B][/COLOR] [B][COLOR white]NC-17[/COLOR][/B] [COLOR dodgerblue][B]¤[/B][/COLOR]']

        for i in certificates:
            self.list.append({'name': str(i), 'url': self.certification_link % str(i).replace('-', '_').lower(), 'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def years(self):
        year = (self.datetime.strftime('%Y'))

        for i in range(int(year)-0, 1900, -1):
            self.list.append({'name': str(i), 'url': self.year_link % (str(i), str(i)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)):
            self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list

    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '':
                raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user):
                    raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass

        self.list = userlists
        for i in range(0, len(self.list)):
            self.list[i].update({'image': 'userlists.png', 'action': 'movies'})
        self.addDirectory(self.list, queue=True)
        return self.list

    def trakt_list(self, url, user):
        try:
            q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.parse.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urllib.parse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)
 

            items = []
            for i in result:
                try:
                    items.append(i['movie'])
                except:
                    pass
            if len(items) == 0:
                items = result
        except:
            log_utils.log('Exception in movies.trakt_list 0')
            return

        try:
            q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
            if not int(q['limit']) == len(items):
                raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib.parse.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urllib.parse.urlparse(url).query, '') + '?' + q
            next = six.ensure_str(next)
        except:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)

                year = item.get('year')
                if year: year = re.sub(r'[^0-9]', '', str(year))
                else: year = '0'
                #if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = item.get('ids', {}).get('imdb')
                #if imdb == None or imdb == '': raise Exception()
                if not imdb: imdb = '0'
                else: imdb = 'tt' + re.sub(r'[^0-9]', '', str(imdb))

                tmdb = item.get('ids', {}).get('tmdb')
                if not tmdb: tmdb == '0'
                else: tmdb = str(tmdb)

                premiered = item.get('released')
                if premiered: premiered = re.compile(r'(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                else: premiered = '0'

                genre = item.get('genres')
                if genre:
                    genre = [i.title() for i in genre]
                    genre = ' / '.join(genre)
                else: genre = '0'

                duration = item.get('runtime')
                if duration: duration = str(duration)
                else: duration = '0'

                rating = item.get('rating')
                if rating and not rating == '0.0': rating = str(rating)
                else: rating = '0'

                try: votes = str(item['votes'])
                except: votes = '0'
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == None: votes = '0'

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = item['ids']['imdb']
                if imdb == None or imdb == '':
                    raise Exception()
                imdb = 'tt' + re.sub(r'[^0-9]', '', str(imdb))

                tmdb = str(item.get('ids', {}).get('tmdb', 0))

                try:
                    premiered = item['released']
                except:
                    premiered = '0'
                try:
                    premiered = re.compile(
                        r'(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'

                try:
                    genre = item['genres']
                except:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []:
                    genre = '0'
                genre = ' / '.join(genre)

                try:
                    duration = str(item['runtime'])
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'

                try:
                    rating = str(item['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'

                try:
                    votes = str(item['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes), ',d'))
                except:
                    pass
                if not votes: votes = '0'

                try:
                    mpaa = item['certification']
                except:
                    mpaa = '0'
                if not mpaa: mpaa = '0'

                try:
                    plot = item['overview']
                except:
                    plot = '0'
                if not plot: plot = '0'
                plot = client.replaceHTMLCodes(plot)

                country = item.get('country')
                if not country: country = '0'
                else: country = country.upper()

                try:
                    tagline = item['tagline']
                except:
                    tagline = '0'
                if tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)
                paused_at = item.get('paused_at', '0') or '0'
                paused_at = re.sub('[^0-9]+', '', paused_at)

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes,
                                  'votes': votes, 'mpaa': mpaa, 'plot': plot, 'tagline': tagline, 'imdb': imdb, 'tmdb': tmdb, 'country': country, 'tvdb': '0', 'poster': '0', 'next': next, 'paused_at': paused_at})
            except:
                pass

        return self.list

    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            pass

        for item in items:
            try:
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client.replaceHTMLCodes(name)

                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

    def tmdb_list(self, url, tid=0):
        try:
            if not tid == 0: 
                url = url % tid

            result = self.session.get(url, timeout=16).json()
            items = result['results']
        except:
            return

        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total: raise Exception()
            if 'page=' not in url: raise Exception()
            next = '%s&page=%s' % (url.split('&page=', 1)[0], page+1)
        except:
            next = ''

        for item in items:

            try:
                tmdb = str(item['id'])

                title = item['title']

                originaltitle = item['original_title']

                if not originaltitle: originaltitle = title

                try: rating = str(item['vote_average'])
                except: rating = ''
                if not rating: rating = '0'

                try: votes = str(item['vote_count'])
                except: votes = ''
                if not votes: votes = '0'

                try: premiered = item['release_date']
                except: premiered = ''
                if not premiered : premiered = '0'

                try: year = re.findall('(\d{4})', premiered)[0]
                except: year = ''
                if not year : year = '0'

                if not premiered or premiered == '0': pass
                elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(self.today_date))):
                    if self.showunaired != 'true': 
                        raise Exception()

                try: plot = item['overview']
                except: plot = ''
                if not plot: plot = '0'

                try: poster_path = item['poster_path']
                except: poster_path = ''
                if poster_path: poster = self.tmdb_img_prelink.format('original', poster_path)
                else: poster = '0'

                backdrop_path = item['backdrop_path'] if 'backdrop_path' in item else ''
                if backdrop_path: 
                    fanart = self.tmdb_img_prelink.format('original', 'backdrop_path')
                else: 
                    fanart = ''

                self.list.append({'title': title, 'originaltitle': originaltitle, 
                                  'premiered': premiered, 'year': year, 'rating': rating, 
                                  'votes': votes, 'plot': plot, 'imdb': '0', 'tmdb': tmdb, 
                                  'tvdb': '0', 'fanart': fanart, 'poster': poster, 'next': next})
            except:
                pass

        return self.list


    def imdb_list(self, url):
        try:
            for i in re.findall(r'date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs={'property': 'pageId'})[0]

            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url

            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url

            result = client.request(url)

            result = result.replace('\n', ' ')

            items = client.parseDOM(result, 'div', attrs={'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs={'class': 'list_item.+?'})
        except:
            return

        try:
            next = client.parseDOM(result, 'a', ret='href', attrs={'class': '.+?ister-page-nex.+?'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs={'class': 'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'),client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urllib.parse.urlparse(url).query, urllib.parse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = six.ensure_str(next)
        except:
            next = ''

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = six.ensure_str(title)

                year = client.parseDOM(item, 'span', attrs={'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs={'class': 'year_type'})
                try:
                    year = re.compile(r'(\d{4})').findall(year)[0]
                except:
                    year = '0'
                year = str(year)

                if int(year) > int((self.datetime).strftime('%Y')):
                    raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall(r'(tt\d*)', imdb)[0]

                try:
                    poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except:
                    poster = '0'
                if '/nopicture/' in poster or '/sash/' in poster:
                    poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = six.ensure_str(poster, errors='ignore')

                try:
                    genre = client.parseDOM(item, 'span', attrs={'class': 'genre'})[0]
                except:
                    genre = '0'
                genre = ' / '.join([i.strip() for i in genre.split(',')])
                if genre == '':
                    genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = six.ensure_str(genre)

                try:
                    duration = re.findall(r'(\d+?) min(?:s|)', item)[-1]
                except:
                    duration = '0'
                duration = six.ensure_str(duration)

                rating = '0'
                try:
                    rating = client.parseDOM(item, 'span', attrs={'class': 'rating-rating'})[0]
                except:
                    pass
                try:
                    rating = client.parseDOM(rating, 'span', attrs={'class': 'value'})[0]
                except:
                    rating = '0'
                try:
                    rating = client.parseDOM(item, 'div', ret='data-value', attrs={'class': '.*?imdb-rating'})[0]
                except:
                    pass
                if rating == '' or rating == '-':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)

                try:
                    votes = client.parseDOM(item, 'div', ret='title', attrs={'class': '.*?rating-list'})[0]
                except:
                    votes = '0'
                try:
                    votes = re.findall('\((.+?) vote(?:s|)\)', votes)[0]
                except:
                    votes = '0'
                if not votes: votes = '0'
                votes = client.replaceHTMLCodes(votes)

                try: mpaa = client.parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa.lower() in ['not_rated', 'not rated']: mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = six.ensure_str(mpaa, errors='ignore')

                try:
                    director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
                    director = client.parseDOM(director, 'a')
                    director = ' / '.join(director)
                    if not director: director = '0'
                    director = client.replaceHTMLCodes(director)
                    director = six.ensure_str(director, errors='ignore')
                except:
                    director = '0'

                try:
                    cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
                    cast = client.replaceHTMLCodes(cast)
                    cast = six.ensure_str(cast, errors='ignore')
                    cast = client.parseDOM(cast, 'a')
                    if not cast: cast = '0'
                except:
                    cast = '0'

                plot = '0'
                try: plot = client.parseDOM(item, 'p', attrs = {'class': 'text-muted'})[0]
                except: pass
                if plot == '0':
                    try: plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                    except: pass
                if plot == '0':
                    try: plot = client.parseDOM(item, 'p')[1]
                    except: pass
                if plot == '': plot = '0'
                if plot and not plot == '0':
                    plot = plot.rsplit('<span>', 1)[0].strip()
                    plot = re.sub(r'<.+?>|</.+?>', '', plot)
                    plot = client.replaceHTMLCodes(plot)
                    plot = six.ensure_str(plot, errors='ignore')

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 
                                  'genre': genre, 'duration': duration, 'rating': rating, 
                                  'votes': votes, 'mpaa': mpaa, 'director': director, 
                                  'plot': plot, 'tagline': '0', 'imdb': imdb, 'tmdb': '0', 
                                  'tvdb': '0', 'poster': poster, 'cast': cast, 'next': next})
            except:
                pass

        return self.list

    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs={'class': '.+?etail'})
        except:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = six.ensure_str(name)

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall(r'(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)

                image = client.parseDOM(item, 'img', ret='src')[0]
                # if not ('._SX' in image or '._SY' in image): raise Exception()
                image = re.sub(r'(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            result = control.six_decode(result)
            items = client.parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = six.ensure_str(name)

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

    def worker(self, level=1):
        self.meta = []
        clearlogo = control.addonClearlogo()
        clearart = control.addonClearart()
        total = len(self.list)


        for i in range(0, total):
            self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in list(range(0, total, 40)): 
            threads = []
            for i in list(range(r, r+40)):
                if i <= total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

        if self.meta: metacache.insert(self.meta)

        self.list = [i for i in self.list if not i['imdb'] == '0']

        #self.list = metacache.local(self.list, self.tm_img_link, 'poster3', 'fanart2')

        if self.fanart_tv_user == '':
            for i in self.list: i.update({'clearlogo': clearlogo, 'clearart': clearart})

    def super_info(self, i):
        try:
            #oh - last entry always raises exception, zero-based
            if self.list[i]['metacache'] == True:
                #raise Exception()
                return

            imdb = self.list[i]['imdb'] if 'imdb' in self.list[i] else '0'
            tmdb = self.list[i]['tmdb'] if 'tmdb' in self.list[i] else '0'
            list_title = self.list[i]['title']

            if tmdb == '0' and not imdb == '0':
                try:
                    url = self.tmdb_by_imdb % imdb
                    result = self.session.get(url, timeout=15).json()
                    movie_result = result['movie_results'][0]
                    tmdb = movie_result['id']
                    if not tmdb: tmdb = '0'
                    else: tmdb = str(tmdb)
                except:
                    pass


            _id = tmdb if not tmdb == '0' else imdb
            if _id == '0': raise Exception()

            en_url = self.tmdb_api_link % _id
            trans_url = en_url + ',translations'
            url = en_url if self.lang == 'en' else trans_url

            item = self.session.get(url, timeout=15).json()

            if imdb == '0':
                try:
                    imdb = item['external_ids']['imdb_id']
                    if not imdb: imdb = '0'
                except:
                    imdb = '0'

            mpaa = ''

            original_language = item.get('original_language', '')

            if self.lang == 'en':
                en_trans_item = None
            else:
                try:
                    translations = item['translations']['translations']
                    en_trans_item = [x['data'] for x in translations if x['iso_639_1'] == 'en'][0]
                except:
                    en_trans_item = {}

            name = item.get('title', '')
            original_title = item.get('original_title', '')
            en_trans_name = en_trans_item.get('title', '') if not self.lang == 'en' else None
            #log_utils.log('self_lang: %s | original_language: %s | list_title: %s | name: %s | original_title: %s | en_trans_name: %s' % (self.lang, original_language, list_title, name, original_name, en_trans_name))

            if self.lang == 'en':
                title = label = name
            else:
                title = en_trans_name or original_title
                if original_language == self.lang:
                    label = name
                else:
                    label = en_trans_name or name
            if not title: title = list_title
            if not label: label = list_title

            plot = item.get('overview') or self.list[i]['plot']

            tagline = item.get('tagline') or '0'

            if not self.lang == 'en':
                if plot == '0':
                    en_plot = en_trans_item.get('overview', '')
                    if en_plot: plot = en_plot

                if tagline == '0':
                    en_tagline = en_trans_item.get('tagline', '')
                    if en_tagline: tagline = en_tagline

            premiered = item.get('release_date') or '0'

            try: _year = re.findall('(\d{4})', premiered)[0]
            except: _year = ''
            if not _year : _year = '0'
            year = self.list[i]['year'] if not self.list[i]['year'] == '0' else _year

            status = item.get('status') or '0'

            try: studio = item['production_companies'][0]['name']
            except: studio = ''
            if not studio: studio = '0'

            try:
                genre = item['genres']
                genre = [d['name'] for d in genre]
                genre = ' / '.join(genre)
            except:
                genre = ''
            if not genre: genre = '0'

            try:
                country = item['production_countries']
                country = [c['name'] for c in country]
                country = ' / '.join(country)
            except:
                country = ''
            if not country: country = '0'

            try:
                duration = str(item['runtime'])
            except:
                duration = ''
            if not duration: duration = '0'

            rating = item['vote_average'] if 'vote_average' in item else '0'
            votes = item['votese'] if 'votes' in item else '0'

            castwiththumb = []
            try:
                c = item['aggregate_credits']['cast'][:30]
                for person in c:
                    _icon = person['profile_path']
                    icon = self.tmdb_img_link % ('185', _icon) if _icon else ''
                    castwiththumb.append({'name': person['name'], 'role': person['roles'][0]['character'], 'thumbnail': icon})
            except:
                pass
            if not castwiththumb: castwiththumb = '0'

            try:
                crew = item['credits']['crew']
                director = ', '.join([d['name'] for d in [x for x in crew if x['job'] == 'Director']])
                writer = ', '.join([w['name'] for w in [y for y in crew if y['job'] in ['Writer', 'Screenplay', 'Author', 'Novel']]])
            except:
                director = writer = '0'

            poster1 = self.list[i]['poster']

            poster_path = item.get('poster_path')
            if poster_path:
                poster2 = self.tmdb_img_prelink.format('original', poster_path)
            else:
                poster2 = None

            backdrop_path = item.get('backdrop_path')
            if backdrop_path:
                fanart1 = self.tmdb_img_prelink.format('original', backdrop_path)
            else:
                fanart1 = '0'

            poster3 = fanart2 = None
            banner = clearlogo = clearart = landscape = discart = '0'
            #if self.hq_artwork == 'true' and not imdb == '0':# and not self.fanart_tv_user == '':
            if not imdb == '0':

                try:
                    r2 = self.session.get(self.fanart_tv_art_link % imdb, headers=self.fanart_tv_headers, timeout=10)
                    r2.raise_for_status()
                    r2.encoding = 'utf-8'
                    art = r2.json()

                    try:
                        _poster3 = art['movieposter']
                        _poster3 = [x for x in _poster3 if x.get('lang') == self.lang][::-1] + [x for x in _poster3 if x.get('lang') == 'en'][::-1] + [x for x in _poster3 if x.get('lang') in ['00', '']][::-1]
                        _poster3 = _poster3[0]['url']
                        if _poster3: poster3 = _poster3
                    except:
                        pass

                    try:
                        if 'moviebackground' in art: _fanart2 = art['moviebackground']
                        else: _fanart2 = art['moviethumb']
                        _fanart2 = [x for x in _fanart2 if x.get('lang') == self.lang][::-1] + [x for x in _fanart2 if x.get('lang') == 'en'][::-1] + [x for x in _fanart2 if x.get('lang') in ['00', '']][::-1]
                        _fanart2 = _fanart2[0]['url']
                        if _fanart2: fanart2 = _fanart2
                    except:
                        pass

                    try:
                        _banner = art['moviebanner']
                        _banner = [x for x in _banner if x.get('lang') == self.lang][::-1] + [x for x in _banner if x.get('lang') == 'en'][::-1] + [x for x in _banner if x.get('lang') in ['00', '']][::-1]
                        _banner = _banner[0]['url']
                        if _banner: banner = _banner
                    except:
                        pass

                    try:
                        if 'hdmovielogo' in art: _clearlogo = art['hdmovielogo']
                        else: _clearlogo = art['clearlogo']
                        _clearlogo = [x for x in _clearlogo if x.get('lang') == self.lang][::-1] + [x for x in _clearlogo if x.get('lang') == 'en'][::-1] + [x for x in _clearlogo if x.get('lang') in ['00', '']][::-1]
                        _clearlogo = _clearlogo[0]['url']
                        if _clearlogo: clearlogo = _clearlogo
                    except:
                        pass

                    try:
                        if 'hdmovieclearart' in art: _clearart = art['hdmovieclearart']
                        else: _clearart = art['clearart']
                        _clearart = [x for x in _clearart if x.get('lang') == self.lang][::-1] + [x for x in _clearart if x.get('lang') == 'en'][::-1] + [x for x in _clearart if x.get('lang') in ['00', '']][::-1]
                        _clearart = _clearart[0]['url']
                        if _clearart: clearart = _clearart
                    except:
                        pass

                    try:
                        if 'moviethumb' in art: _landscape = art['moviethumb']
                        else: _landscape = art['moviebackground']
                        _landscape = [x for x in _landscape if x.get('lang') == self.lang][::-1] + [x for x in _landscape if x.get('lang') == 'en'][::-1] + [x for x in _landscape if x.get('lang') in ['00', '']][::-1]
                        _landscape = _landscape[0]['url']
                        if _landscape: landscape = _landscape
                    except:
                        pass

                    try:
                        if 'moviedisc' in art: _discart = art['moviedisc']
                        _discart = [x for x in _discart if x.get('lang') == self.lang][::-1] + [x for x in _discart if x.get('lang') == 'en'][::-1] + [x for x in _discart if x.get('lang') in ['00', '']][::-1]
                        _discart = _discart[0]['url']
                        if _discart: discart = _discart
                    except:
                        pass
                except Exception as e:
                    log_utils.log('fanart.tv art fail. Error = ' + str(e))
                    pass


            poster = poster3 or poster2 or poster1
            fanart = fanart2 or fanart1

            item = {'title': title, 'originaltitle': title, 'year': year, 'imdb': imdb,
                    'tmdb': tmdb, 'poster': poster, 
                    'banner': banner, 'fanart': fanart, 'landscape': landscape, 'discart': discart,
                    'fanart2': fanart2, 'clearlogo': clearlogo,
                    'clearart': clearart, 'premiered': premiered, 'genre': genre, 
                    'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 
                    'director': director, 'writer': writer, 'castwiththumb': castwiththumb, 
                    'plot': plot, 'tagline': tagline}

            item = dict((k,v) for k, v in item.items() if not v == '0')
            self.list[i].update(item)

            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)

        except:
            pass





    def movieDirectory(self, items):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])


        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')
        addonClearlogo, addonClearart = control.addonClearlogo(), control.addonClearart()


        traktCredentials = trakt.getTraktCredentialsInfo()
        
        kodiVersion = control.getKodiVersion()

        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'
        indicators = playcount.getMovieIndicators(refresh=True) if action == 'movies' else playcount.getMovieIndicators()
        findSimilar = control.lang(32100)
        playbackMenu = control.lang(32063) if control.setting('hosts.mode') == '2' else control.lang(32064)
        watchedMenu = control.lang(32068) if traktCredentials else control.lang(32066)
        unwatchedMenu = control.lang(32069) if traktCredentials else control.lang(32067)
        queueMenu = control.lang(32065)
        traktManagerMenu = control.lang(32070)
        nextMenu = control.lang(32053)
        addToLibrary = control.lang(32551)
        infoMenu = control.lang(32101)

        for i in items:
            try:
                label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                sysname = urllib.parse.quote_plus('%s (%s)' % (title, year))
                label = i['label'] if 'label' in i and not i['label'] == '0' else title
                label = '%s (%s)' % (label, year)
                status = i['status'] if 'status' in i else '0'
                try:
                    premiered = i['premiered']
                    if (premiered == '0' and status in ['Upcoming', 'In Production', 'Planned']) or (int(re.sub('[^0-9]', '', premiered)) > int(re.sub('[^0-9]', '', str(self.today_date)))):

                        #changed by oh -  17-5-2023
                        colorlist = [32589, 32590, 32591, 32592, 32593, 32594, 32595, 32596, 32597, 32598]
                        colornr = colorlist[int(control.setting('unaired.identify'))]
                        unairedcolor = re.sub("\][\w\s]*\[", "][I]%s[/I][", control.lang(int(colornr)))
                        label = unairedcolor % label

                        if unairedcolor == '':
                            unairedcolor = '[COLOR red][I]%s[/I][/COLOR]'
                except:
                    pass

                sysname = urllib.parse.quote_plus('%s (%s)' % (title, year))
                systitle = urllib.parse.quote_plus(title)

                meta = dict((k,v) for k, v in i.items() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'imdb_id': imdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s&tmdb=%s&imdb=%s' % (sysaddon, urllib.parse.quote_plus(label), tmdb, imdb)})

                if (not 'duration' in i) or (i['duration'] == '0'):
                    meta.update({'duration': '120'})

                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass

                poster = i['poster'] if 'poster' in i and not i['poster'] == '0' else addonPoster
                fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else addonFanart
                banner = i['banner'] if 'banner' in i and not i['banner'] == '0' else addonBanner
                landscape = i['landscape'] if 'landscpape' in i and not i['landscape'] == '0' else fanart
                clearlogo = i['clearlogo'] if 'clearlogo' in i and not i['clearlogo'] == '0' else addonClearlogo
                clearart = i['clearart'] if 'clearart' in i and not i['clearart'] == '0' else addonClearart


                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})

                sysmeta = urllib.parse.quote_plus(json.dumps(meta))

                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.parse.quote_plus(url)

                #path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)

                cm = []
                #cm.append(('Find similar', 'ActivateWindow(10025,%s?action=movies&url=https://api.trakt.tv/movies/%s/related,return)' % (sysaddon, imdb)))
                cm.append((findSimilar, 'Container.Update(%s?action=movies&url=%s)' % (sysaddon, urllib.parse.quote_plus(self.related_link % tmdb))))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' % (sysaddon, sysname, imdb)))

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                cm.append((addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, sysname, systitle, year, imdb, tmdb)))

                try: item = control.item(label=label, offscreen=True)
                except: item = control.item(label=label)

                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})

                fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else addonFanart

                if settingFanart == 'true':
                    art.update({'fanart': fanart})
                else:
                    art.update({'fanart': addonFanart})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})

                if 'landscape' in i and not i['landscape'] == '0':
                    landscape = i['landscape']
                else:
                    landscape = fanart
                art.update({'landscape': landscape})

                if 'discart' in i and not i['discart'] == '0':
                    art.update({'discart': i['discart']})

                item.setArt(art)

                item.addContextMenuItems(cm)

                item.setProperty('IsPlayable', isPlayable)

                castwiththumb = i.get('castwiththumb')


                if castwiththumb and not castwiththumb == '0':
                    item.setCast(castwiththumb)

                offset = bookmarks.get('movie', imdb, '', '', True)
                if float(offset) > 120:
                    percentPlayed = int(float(offset) / float(meta['duration']) * 100)
                    item.setProperty('resumetime', str(offset))
                    item.setProperty('percentplayed', str(percentPlayed))

                item.setProperty('imdb_id', imdb)
                item.setProperty('tmdb_id', tmdb)
                try: item.setUniqueIDs({'imdb': imdb, 'tmdb': tmdb})
 
                except: pass
                item.setInfo(type='Video', infoLabels = control.metadataClean(meta))

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()

            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.parse.quote_plus(url))

            try: item = control.item(label=nextMenu, offscreen=True)
            except: item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon, 'fanart': addonFanart})

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})

    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        queueMenu = control.lang(32065)

        playRandom = control.lang(32535)

        addToLibrary = control.lang(32551)

        for i in items:
            try:
                name = i['name']

                plot = i.get('plot') or '[CR]'
                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib.parse.quote_plus(i['url'])
                except:
                    pass

                cm = []

                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=movie&url=%s)' % (sysaddon, urllib.parse.quote_plus(i['url']))))

                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=moviesToLibrary&url=%s)' % (sysaddon, urllib.parse.quote_plus(i['context']))))
                except:
                    pass

                try: item = control.item(label=name, offscreen=True)
                except: item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb, 'poster': thumb, 'fanart': addonFanart})
                item.setInfo(type='video', infoLabels={'plot': plot})

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                log_utils.log('mov_addDir', 1)
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
