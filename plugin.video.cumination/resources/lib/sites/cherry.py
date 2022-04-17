'''
    Cumination
    Copyright (C) 2022 Team Cumination
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
'''

import os
import sqlite3
import json
from six.moves import urllib_parse
from resources.lib import utils
from resources.lib.adultsite import AdultSite

site = AdultSite('cherry', '[COLOR hotpink]Cherry TV[/COLOR]', 'https://cherry.tv/', 'https://cdn.cherry.tv/app/_next/static/media/cherry-logo.25e70ce4.png', 'cherry', True)


@site.register(default_mode=True)
def Main():
    female = True if utils.addon.getSetting("chatfemale") == "true" else False
    couple = True if utils.addon.getSetting("chatcouple") == "true" else False
    trans = True if utils.addon.getSetting("chattrans") == "true" else False
    site.add_dir('[COLOR red]Refresh Cherry images[/COLOR]', '', 'clean_database', '', Folder=False)
    site.add_dir('[COLOR hotpink]Featured[/COLOR]', 'featured', 'List', '', '')
    if female:
        site.add_dir('[COLOR hotpink]Female[/COLOR]', 'girls', 'List', '', '')
    if couple:
        site.add_dir('[COLOR hotpink]Couples[/COLOR]', 'groupshow', 'List', '', '')
    if trans:
        site.add_dir('[COLOR hotpink]Transsexual[/COLOR]', 'trans', 'List', '', '')
    site.add_dir('[COLOR hotpink]Spy show[/COLOR]', 'spyshow', 'List', '', '')
    utils.eod()


@site.register()
def List(url):
    if utils.addon.getSetting("chaturbate") == "true":
        clean_database(False)

    query = {
        "operationName": "findBroadcastsByPage",
        "variables": '{"slug":"%s","limit":500}' % url,
        "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"313ae181e7c38ba4028302825f47a02af8e1513d71123a43e06ff98534606543"}}'
    }
    murl = "https://api.cherry.tv/graphql?" + urllib_parse.urlencode(query)
    try:
        response = utils.getHtml(murl, site.url)
    except:
        return None
    data = json.loads(response).get('data', {}).get('broadcasts', {})
    model_list = data.get('broadcasts')

    for model in model_list:
        name = utils.cleanhtml(model.get('title'))
        videourl = model.get('username')
        img = model.get('thumbnailUrl', '')
        fanart = model.get('imageUrl', '').split('?')[0]
        subject = ''
        if model.get('description'):
            subject += '[COLOR deeppink]Topic: [/COLOR]{0}[CR]'.format(model.get('description'))
        if model.get('showStatus'):
            subject += '[COLOR deeppink]Status: [/COLOR]{0}[CR]'.format(model.get('showStatus'))
        subject += '[COLOR deeppink]Viewers: [/COLOR]{0}[CR][CR]'.format(model.get('viewers'))
        if model.get('tags'):
            subject += '[COLOR deeppink]#[/COLOR]'
            tags = [t for t in model.get('tags') if 'tag' not in t.lower()]
            subject += '[COLOR deeppink] #[/COLOR]'.join(tags)
        site.add_download_link(name, videourl, 'Playvid', img, subject, noDownload=True, fanart=fanart)
    utils.eod()


@site.register(clean_mode=True)
def clean_database(showdialog=True):
    conn = sqlite3.connect(utils.TRANSLATEPATH("special://database/Textures13.db"))
    try:
        with conn:
            list = conn.execute("SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % ".cherry.tv")
            for row in list:
                conn.execute("DELETE FROM sizes WHERE idtexture LIKE '%s';" % row[0])
                try:
                    os.remove(utils.TRANSLATEPATH("special://thumbnails/" + row[1]))
                except:
                    pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" % ".cherry.tv")
            if showdialog:
                utils.notify('Finished', 'Cherry images cleared')
    except:
        pass


@site.register()
def Playvid(url, name):
    vp = utils.VideoPlayer(name)
    vp.progress.update(25, "[CR]Loading video page[CR]")
    query = {
        "operationName": "findStreamerBySlug",
        "variables": '{"slug":"%s"}' % url,
        "extensions": '{"persistedQuery":{"version":1,"sha256Hash":"8850398f03323cf6acd9ce618fe82b5c033a3545834e8f5d5b968ad316337e54"}}'
    }
    murl = "https://api.cherry.tv/graphql?" + urllib_parse.urlencode(query)
    try:
        response = utils.getHtml(murl, site.url)
    except:
        return None
    data = json.loads(response).get('data', {}).get('streamer', {}).get('broadcast', {})
    if data.get('broadcastStatus') == 'Live':
        surl = data.get('pullUrl')
    else:
        utils.notify(name, 'Couldn\'t find a playable webcam link', icon='thumb')
        vp.progress.close()
        return

    vp.progress.update(75, "[CR]Found Stream[CR]")
    vp.play_from_direct_link(surl)
