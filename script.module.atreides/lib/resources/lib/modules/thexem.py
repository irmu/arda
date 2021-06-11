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

import json

from resources.lib.modules import client

URL_PATTERN = 'http://thexem.de/map/single?id=%s&origin=tvdb&season=%s&episode=%s&destination=scene'


def get_scene_episode_number(tvdbid, season, episode):

    try:
        url = URL_PATTERN % (tvdbid, season, episode)
        r = client.request(url)
        r = json.loads(r)
        if r['result'] == 'success':
            data = r['data']['scene']
            return data['season'], data['episode']
    except Exception:
        pass

    return season, episode
