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


import urllib
import json

from resources.lib.modules import cache, client, control


class tvMaze:
    def __init__(self, show_id=None):
        self.api_url = 'https://api.tvmaze.com/%s%s'
        self.show_id = show_id
        self.tvdb_key = control.setting('tvdb.user')

    def showID(self, show_id=None):
        if (show_id is not None):
            self.show_id = show_id
            return show_id

        return self.show_id

    def request(self, endpoint, query=None):
        try:
            # Encode the queries, if there is any...
            if (query is not None):
                query = '?' + urllib.urlencode(query)
            else:
                query = ''

            # Make the request
            request = self.api_url % (endpoint, query)

            # Send the request and get the response
            # Get the results from cache if available
            response = cache.get(client.request, 24, request)

            # Retrun the result as a dictionary
            return json.loads(response)
        except Exception:
            pass

        return {}

    def showLookup(self, type, id):
        try:
            result = self.request('lookup/shows', {type: id})

            # Storing the show id locally
            if ('id' in result):
                self.show_id = result['id']

            return result
        except Exception:
            pass

        return {}

    def shows(self, show_id=None, embed=None):
        try:
            if (not self.showID(show_id)):
                raise Exception()

            result = self.request('shows/%d' % self.show_id)

            # Storing the show id locally
            if ('id' in result):
                self.show_id = result['id']

            return result
        except Exception:
            pass

        return {}

    def showSeasons(self, show_id=None):
        try:
            if (not self.showID(show_id)):
                raise Exception()

            result = self.request('shows/%d/seasons' % int(self.show_id))

            if (len(result) > 0 and 'id' in result[0]):
                return result
        except Exception:
            pass

        return []

    def showSeasonList(self, show_id):
        return {}

    def showEpisodeList(self, show_id=None, specials=False):
        try:
            if (not self.showID(show_id)):
                raise Exception()

            result = self.request('shows/%d/episodes' % int(self.show_id), 'specials=1' if specials else '')

            if (len(result) > 0 and 'id' in result[0]):
                return result
        except Exception:
            pass

        return []

    def episodeAbsoluteNumber(self, thetvdb, season, episode):
        try:
            url = 'https://thetvdb.com/api/%s/series/%s/default/%01d/%01d' % (
                self.tvdb_key, thetvdb, int(season), int(episode))
            return int(client.parseDOM(client.request(url), 'absolute_number')[0])
        except Exception:
            pass

        return episode

    def getTVShowTranslation(self, thetvdb, lang):
        try:
            url = 'https://thetvdb.com/api/%s/series/%s/%s.xml' % (
                self.tvdb_key, thetvdb, lang)
            r = client.request(url)
            title = client.parseDOM(r, 'SeriesName')[0]
            title = client.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            return title
        except Exception:
            pass
