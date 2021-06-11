import threading

from bs4 import BeautifulSoup
from resources.lib.common import tools
from resources.lib.common import source_utils
from resources.lib.common.source_utils import serenRequests

class sources:

    def __init__(self):
        self.domain = "thepiratebay.org"
        self.base_link = 'https://thepiratebay.org/'
        self.search_link = 'search/'
        self.threads = []
        self.threadResults = []

    def movie(self, title, year):
        url = self.base_link + self.search_link + tools.quote('%s %s' % (title, year))
        response = serenRequests().get(url, timeout=10)
        results = BeautifulSoup(response.text, 'html.parser').find_all('tr')
        torrent_list = []
        for i in results:
            try:
                torrent = {}
                torrent['package'] = 'single'
                torrent['release_title'] = i.find('a', {'class', 'detLink'}).text
                if not source_utils.filterMovieTitle(torrent['release_title'], title, year):
                    continue
                torrent['magnet'] = i.find_all('a')[3]['href']
                if 'magnet:?' not in torrent['magnet']:
                    torrent['magnet'] = self.magnet_request(torrent['magnet'])
                torrent['seeds'] = int(i.find_all('td')[2].text)
                torrent_list.append(torrent)
            except:
                continue
        return torrent_list

    def episode(self, simpleInfo, allInfo):

        self.threads.append(threading.Thread(target=self.seasonPack, args=(simpleInfo, allInfo)))
        self.threads.append(threading.Thread(target=self.singleEpisode, args=(simpleInfo, allInfo)))
        self.threads.append(threading.Thread(target=self.showPack, args=(simpleInfo, allInfo)))

        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

        return self.threadResults

    def showPack(self, simpleInfo, allInfo):

        try:
            showTitle = source_utils.cleanTitle(simpleInfo['show_title'])

            url = self.base_link + self.search_link + tools.quote(
                '%s season 1-%s' % (showTitle, simpleInfo['no_seasons']))
            response = serenRequests().get(url, timeout=10)
            try:
                if response.status_code != 200:
                    return
            except:
                return
            webpage = BeautifulSoup(response.text, 'html.parser')
            results = webpage.find_all('tr')

            url = self.base_link + self.search_link + tools.quote(
                '%s complete' % showTitle)
            response = serenRequests().get(url)
            webpage = BeautifulSoup(response.text, 'html.parser')
            results += webpage.find_all('tr')

            torrent_list = []

            for i in results:
                try:
                    torrent = {}
                    torrent['package'] = 'pack'
                    torrent['release_title'] = i.find('a', {'class', 'detLink'}).text
                    if not source_utils.filterShowPack(simpleInfo, torrent['release_title']):
                        continue
                    torrent['magnet'] = i.find_all('a')[3]['href']
                    if 'magnet:?' not in torrent['magnet']:
                        torrent['magnet'] = self.magnet_request(torrent['magnet'])
                    torrent['seeds'] = int(i.find_all('td')[2].text)
                    torrent_list.append(torrent)
                except:
                    continue

            self.threadResults += torrent_list

        except:
            pass


    def seasonPack(self, simpleInfo, allInfo):

        try:
            showTitle = source_utils.cleanTitle(simpleInfo['show_title'])

            url = self.base_link + self.search_link + tools.quote(
                '%s season %s' % (showTitle, simpleInfo['season_number']))
            response = serenRequests().get(url, timeout=10)
            webpage = BeautifulSoup(response.text, 'html.parser')
            results = webpage.find_all('tr')
            torrent_list = []
            page_limit = 2

            for x in range(1, page_limit):

                for i in results:
                    try:
                        torrent = {}
                        torrent['package'] = 'pack'
                        torrent['release_title'] = i.find('a', {'class', 'detLink'}).text

                        if not source_utils.filterSeasonPack(simpleInfo, torrent['release_title']):
                            continue

                        torrent['magnet'] = i.find_all('a')[3]['href']
                        if 'magnet:?' not in torrent['magnet']:
                            torrent['magnet'] = self.magnet_request(torrent['magnet'])
                        torrent['seeds'] = int(i.find_all('td')[2].text)
                        torrent_list.append(torrent)
                        url = url + '/%s' % x
                    except:
                        continue

                self.threadResults += torrent_list

        except:
            pass

    def singleEpisode(self, simpleInfo, allInfo):

        try:
            showTitle = source_utils.cleanTitle(simpleInfo['show_title'])
            season = simpleInfo['season_number'].zfill(2)
            episode = simpleInfo['episode_number'].zfill(2)

            url = self.base_link + self.search_link + tools.quote('%s s%se%s' % (showTitle, season, episode))
            response = serenRequests().get(url, timeout=10)
            webpage = BeautifulSoup(response.text, 'html.parser')
            results = webpage.find_all('tr')
            torrent_list = []

            page_limit = 2
            torrent_list = []

            for x in range(1, page_limit):
                for i in results:
                    try:
                        torrent = {}
                        torrent['package'] = 'single'
                        torrent['release_title'] = i.find('a', {'class', 'detLink'}).text

                        if not source_utils.filterSingleEpisode(simpleInfo, torrent['release_title']):
                            continue

                        torrent['magnet'] = i.find_all('a')[3]['href']
                        if 'magnet:?' not in torrent['magnet']:
                            torrent['magnet'] = self.magnet_request(torrent['magnet'])
                        torrent['seeds'] = int(i.find_all('td')[2].text)
                        torrent_list.append(torrent)
                    except:
                        import traceback
                        traceback.print_exc()
                        continue

                self.threadResults += torrent_list
        except:
            pass

    def magnet_request(self, url):
        response = serenRequests().get(url)
        magnet = BeautifulSoup(response.text, 'html.parser').find('div', {'class':'download'})
        magnet = magnet.find('a')['href']
        return magnet
