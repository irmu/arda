# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    ///Updated for Moria///

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import os,sys

import six

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache
from resources.lib.modules import api_keys
from resources.lib.modules.justwatch import providers

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065)


class navigator:
    def root(self):
        api_keys.chk()
        self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'airing-today.png', 'DefaultTVShows.png')

        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        if not control.setting('movie.widget') == '0':
            self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'returning-tvshows.png', 'DefaultRecentlyAddedEpisodes.png')

        if not control.setting('channels') == '0':
            self.addDirectoryItem(32007, 'channels', 'channels.png', 'DefaultMovies.png')

        self.addDirectoryItem(32013, 'persons', 'people.png', 'DefaultMovies.png')

        if not control.setting('furk.api') == '':
            self.addDirectoryItem('Furk.net', 'furkNavigator', 'movies.png', 'defaultaddonvideo.png')
        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultAddonsSearch.png')

        self.endDirectory()


    def furk(self):
        self.addDirectoryItem('User Files', 'furkUserFiles', 'mymovies.png', 'DefaultVideoPlaylists.png')
        self.addDirectoryItem('Search', 'furkSearch', 'search.png', 'DefaultAddonsSearch.png')
        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem(32580, 'movies&url=added', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32017, 'movies&url=trending', 'eye.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32321, 'movies&url=featured', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'movieYears', 'year.png', 'DefaultMovies.png')
        self.addDirectoryItem(32123, 'movieDecades', 'decades.png', 'DefaultMovies.png')
        self.addDirectoryItem('Movie Mosts', 'movieMosts', 'most.png', 'DefaultMovies.png')
        self.addDirectoryItem(32018, 'movies&url=popular', 'featured.png', 'DefaultMovies.png')
        self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
        self.addDirectoryItem(32023, 'movies&url=rating', 'highly_r.png', 'DefaultMovies.png')
        self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')
        self.addDirectoryItem(32015, 'movieCertificates', 'certificates.png', 'DefaultMovies.png')
        self.addDirectoryItem('Great Directors', 'greatDirectors', 'person.png', 'DefaultMovies.png')        
        self.addDirectoryItem('J.R.R. Tolkien', 'movies&url=tolkien', 'tolkien.png', 'DefaultMovies.png')
        self.addDirectoryItem('Boxsets & Collections', 'collections', 'collect.png', 'DefaultMovies.png')  
        self.addDirectoryItem('IMDB Top100', 'movies&url=top100', 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('IMDB Top250', 'movies&url=top250', 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem(32125, 'movieCustomLists', 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem(32124, 'movieKeywords', 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('IMDb Keywords', 'movieKeywords2', 'imdb.png', 'DefaultMovies.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')

        self.addDirectoryItem(32028, 'peopleSearch&content=movies', 'searchR.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultAddonsSearch.png')

        self.endDirectory()

    def greatDirectors(self, lite=False):  # Directors ####################
        self.addDirectoryItem('Alfred Hitchcock', 'movies&url=hitchcock', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Brian De Palma', 'movies&url=depalma', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Christopher Nolan', 'movies&url=nolan', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Clint Eastwood', 'movies&url=eastwood', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Coen Brothers', 'movies&url=coen', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Danny Boyle', 'movies&url=boyle', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Darren Aronofsky', 'movies&url=aronofsky', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('David Fincher', 'movies&url=fincher', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('David Lynch', 'movies&url=lynch', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Denis Villeneuve', 'movies&url=villeneuve', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Edgar Wright', 'movies&url=wright', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Francis Ford Coppola', 'movies&url=coppola', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('George Lucas', 'movies&url=lucas', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('George Romero', 'movies&url=romero', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Guillermo Del Toro', 'movies&url=guillermo', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Guy Ritchie', 'movies&url=ritchie', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('James Cameron', 'movies&url=cameron', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('James Wan', 'movies&url=wan', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('John Carpenter', 'movies&url=carpenter', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Jordan Peele', 'movies&url=peele', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('M. Night Shyamalan', 'movies&url=night', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Martin Scorsese', 'movies&url=scorsese', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Mel Gibson', 'movies&url=gibson', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Oliver Stone', 'movies&url=stone', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Peter Jackson', 'movies&url=jackson', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Quentin Tarantino', 'movies&url=tarantino', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Ridley Scott', 'movies&url=ridley', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Robert Rodriguez', 'movies&url=rodriguez', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Rob Reiner', 'movies&url=reiner', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Ron Howard', 'movies&url=howard', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Sam Raimi', 'movies&url=raimi', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Stanley Kubrick', 'movies&url=kubrick', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Steven Spielberg', 'movies&url=spielberg', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Taika Waititi', 'movies&url=waititi', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Tim Burton', 'movies&url=burton', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Wes Anderson', 'movies&url=wes', 'person.png', 'DefaultMovies.png')
        self.addDirectoryItem('Wes Craven', 'movies&url=craven', 'person.png', 'DefaultMovies.png')
        # self.addDirectoryItem('Tobe Hooper', 'movies&url=hooper', 'person.png', 'DefaultMovies.png')

        
        self.endDirectory()
        # self.endDirectory(category='Directors', sortMethod=control.xDirSort.Label)

    def collections(self, lite=False):  # Collections ####################
        self.addDirectoryItem('The Best of Bruce Lee', 'movies&url=lee', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Middle Earth Collection', 'movies&url=lotr', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Wizarding World Collection', 'movies&url=wizard', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Chronicles of Narnia Collection', 'movies&url=narnia', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Marvel MCU Collection', 'movies&url=mcu', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Sony Marvel Universe', 'movies&url=sony', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Spider-Man Collection', 'movies&url=spiderman', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('X-Men Collection', 'movies&url=xmen', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Deadpool Collection', 'movies&url=deadpool', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('DC Extended Universe', 'movies&url=dc', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Batman Collection', 'movies&url=batman', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Unbreakable Collection', 'movies&url=unbreak', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Hellboy Collection', 'movies&url=hellboy', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Matrix Collection', 'movies&url=matrix', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Star Trek Collection', 'movies&url=trekkie', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Star Wars Collection', 'movies&url=starwars', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Avatar Collection', 'movies&url=avatar', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('MonsterVerse', 'movies&url=monster', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Jurassic Park Collection', 'movies&url=jurassic', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Pirates of the Carribean Collection', 'movies&url=pirates', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Mummy Collection', 'movies&url=mummy', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Indiana Jones Collection', 'movies&url=indiana', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('National Treasure Collection', 'movies&url=treasure', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Now You See Me Collection', 'movies&url=seeme', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Oceans Eleven Collection', 'movies&url=oceans', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Mission: Impossible Collection', 'movies&url=mission', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('John Wick Collection', 'movies&url=wick', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Jason Bourne Collection', 'movies&url=bourne', 'collect.png', 'DefaultMovies.png')
        # self.addDirectoryItem('Jack Ryan', 'movies&url=ryan', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Jack Ryan Collection', 'movies&url=jack', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('James Bond Collection', 'movies&url=bond', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Kingsman Collection', 'movies&url=kingsman', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Kill Bill Collection', 'movies&url=killbill', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Twilight Saga', 'movies&url=twilight', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Fifty Shades Collection', 'movies&url=fifty', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Fast and the Furious Collection', 'movies&url=fast', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Mad Max Collection', 'movies&url=max', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Hunger Games Collection', 'movies&url=games', 'collect.png', 'DefaultMovies.png')        
        self.addDirectoryItem('Planet of the Apes Collection', 'movies&url=apes', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Riddick Collection', 'movies&url=riddick', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Terminator Collection', 'movies&url=terminator', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Monty Python Collection', 'movies&url=python', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Austin Powers Collection', 'movies&url=powers', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Naked Gun Collection', 'movies&url=gun', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Ace Ventura Collection', 'movies&url=ace', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Rush Hour Collection', 'movies&url=rush', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Fockers Collection', 'movies&url=fockers', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Scary Movie Collection', 'movies&url=scary', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Men in Black Collection', 'movies&url=black', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Alien and Predator Collection', 'movies&url=alien', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('A Quiet Place Collection', 'movies&url=quiet', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('IT Collection', 'movies&url=it', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Final Destination Collection', 'movies&url=destination', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Conjuring Chronology', 'movies&url=conjuring', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Incidious Collection', 'movies&url=insidious', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Purge Collection', 'movies&url=purge', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('SAW Collection', 'movies&url=saw', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Evil Dead Collection', 'movies&url=evildead', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('The Living Dead Collection', 'movies&url=livingdead', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Halloween Collection', 'movies&url=halloween', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Friday the 13th and Nightmare On Elm Street', 'movies&url=friday', 'collect.png', 'DefaultMovies.png')
        self.addDirectoryItem('Christmas Movies & Themes', 'movies&url=xmas', 'collect.png', 'DefaultMovies.png')

        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()

        if providers.SCRAPER_INIT:
            self.addDirectoryItem('My Services', 'movieServices', 'mymovies.png', 'DefaultMovies.png')

        if traktCredentials == True and imdbCredentials == True:
            self.addDirectoryItem(32094, 'movies&url=onDeck', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            if control.setting('imdb.sort.order') == '1':
                self.addDirectoryItem(32034, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)
            else:
                self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials == True:
            self.addDirectoryItem(32094, 'movies&url=onDeck', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')
            self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials == True:
            if control.setting('imdb.sort.order') == '1':
                self.addDirectoryItem(32034, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)
            else:
                self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')

        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32017, 'tvshows&url=trending', 'eye.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32018, 'tvshows&url=popular', 'featured.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
        self.addDirectoryItem('TV Show Mosts', 'tvMosts', 'most.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly_r.png', 'DefaultTVShows.png')
        self.addDirectoryItem('Binge Box TV', 'tvshows&url=binge', 'collect.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32026, 'tvshows&url=premiere', 'latest-movies.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'horse.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
        self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32015, 'tvCertificates', 'certificates.png', 'DefaultTVShows.png')

        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        self.addDirectoryItem(32028, 'peopleSearch&content=tvshows', 'searchR.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultAddonsSearch.png')

        self.endDirectory()


    def mytvshows(self, lite=False):
        try:
            self.accountCheck()

            if providers.SCRAPER_INIT:
                self.addDirectoryItem('My Services', 'tvServices', 'mytvshows.png', 'DefaultTVShows.png')

            if traktCredentials == True and imdbCredentials == True:

                self.addDirectoryItem(32094, 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
                if control.setting('imdb.sort.order') == '1':
                    self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')
                else:
                    self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

            elif traktCredentials == True:
                self.addDirectoryItem(32094, 'calendar&url=onDeck', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
                self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
                self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
                self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

            elif imdbCredentials == True:
                if control.setting('imdb.sort.order') == '1':
                    self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')
                else:
                    self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
                self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

            if lite == False:
                self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')

            self.endDirectory()
        except:
            print("ERROR")


    def tools(self):
        self.addDirectoryItem('[B]Moria[/B] : Changelog', 'changelog', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32079, 'moriascrapersettings', 'icon.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32076, 'smuSettings', 'resolveurl.png', 'DefaultAddonProgram.png', isFolder=False)
        if not control.condVisibility('System.HasAddon(script.module.orion)'):
            self.addDirectoryItem('[B]Orion[/B] : Install', 'installOrion', 'orion.png', 'DefaultAddonProgram.png', isFolder=False)
        else:
            self.addDirectoryItem(32080, 'orionsettings', 'orion.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Moria[/B] : Cache Functions', 'cacheNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('[B]Moria[/B] : Log Functions', 'logNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32108, 'cleanSettings', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32073, 'authTrakt', 'trakt.png', 'DefaultAddonProgram.png', isFolder=False)

        self.endDirectory()


    def library(self):
        self.addDirectoryItem(32557, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png', isFolder=False)
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', isFolder=False)
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', isFolder=False)
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', isFolder=False)

        self.endDirectory()


    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')

        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

        self.endDirectory()


    def cache_functions(self):
        self.addDirectoryItem(32604, 'clearCacheSearch&select=all', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32116, 'clearDebridCheck', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem(32611, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)

        self.endDirectory()


    def log_functions(self):
        self.addDirectoryItem('[B]Moria[/B] : View Log', 'viewLog', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[B]Moria[/B] : Upload Log to hastebin', 'uploadLog', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        self.addDirectoryItem('[B]Moria[/B] : Empty Log', 'emptyLog', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)

        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32013, 'peopleSearch', 'search.png', 'DefaultAddonsSearch.png')

        self.endDirectory()


    def views(self):
        try:
            control.idle()

            items = [ (control.lang(32001), 'movies'), (control.lang(32002), 'tvshows'), (control.lang(32054), 'seasons'), (control.lang(32038), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049))

            if select == -1: return

            content = items[select][1]

            title = control.lang(32059)
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)

            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

            item = control.item(label=title)
            item.setInfo(type='Video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)

            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)

            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False and providers.SCRAPER_INIT == False:
            control.idle()
            control.infoDialog(control.lang(32042), sound=True, icon='WARNING')
            sys.exit()


    def clearCache(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')

    def clearCacheMeta(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_meta()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')

    def clearCacheProviders(self):
        # yes = control.yesnoDialog(control.lang(32056))
        # if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_providers()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')

    def clearCacheSearch(self, select):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_search(select)
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')

    def clearDebridCheck(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_debrid()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')

    def clearCacheAll(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import cache
        cache.cache_clear_all()
        control.infoDialog(control.lang(32057), sound=True, icon='INFO')

    def uploadLog(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import log_utils
        log_utils.upload_log()

    def emptyLog(self):
        yes = control.yesnoDialog(control.lang(32056))
        if not yes: return
        from resources.lib.modules import log_utils
        log_utils.empty_log()

    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        try: name = control.lang(name)
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
        thumb = os.path.join(artPath, thumb) if not artPath == None else icon
        cm = []
        if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
        if not context == None: cm.append((control.lang(context[0]), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
        try: item = control.item(label=name, offscreen=True)
        except: item = control.item(label=name)
        item.addContextMenuItems(cm)
        item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': addonFanart})
        item.setInfo(type='video', infoLabels={'plot': '[CR]'})
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def endDirectory(self, cache=True):
        syshandle = int(sys.argv[1])
        control.content(syshandle, '')
        control.directory(syshandle, cacheToDisc=cache)
