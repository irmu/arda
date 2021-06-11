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

import traceback
import xbmcaddon

from resources.lib.modules import control, log_utils

try:
    import resolveurl

    debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(
        order_matters=True) if resolver.isUniversal()]

    if len(debrid_resolvers) == 0:
        # Support Rapidgator accounts! Unfortunately, `sources.py` assumes that rapidgator.net is only ever
        # accessed via a debrid service, so we add rapidgator as a debrid resolver and everything just works.
        # As a bonus(?), rapidgator links will be highlighted just like actual debrid links
        debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(
            order_matters=True, include_universal=False) if 'rapidgator.net' in resolver.domains]

except Exception:
    debrid_resolvers = []


def status(torrent=False):
    debrid_check = debrid_resolvers != []
    if debrid_check is True:
        if torrent:
            enabled = control.setting('torrent.enabled')
            if enabled == '' or enabled.lower() == 'true':
                return True
            else:
                return False
    return debrid_check


def check_torrent_cache(url, debrid):
    try:
        if url.lower().startswith('magnet:'):
            for resolver in debrid_resolvers:
                try:
                    cache_only = resolver.get_setting('cached_only')
                except Exception:
                    log_utils.log('Debrid Cache first check crashed?')
                    return False

                if cache_only == 'false':
                    return False

                # Always fails saying 401 - unauthorized??? But gives you the idea of what SHOULD be done
                # I need to do a pull request with ResolveURL to check for, and add if needed, the token
                # to the header so this works if he adds it. Otherwise, will have to fork the resolver
                log_utils.log('Debrid - Check Torrent Cache - Resolver: %s' % (resolver.name))
                try:
                    check = resolver._RealDebridResolver__check_cache(url)
                except Exception as e:
                    log_utils.log('Debrid - Check Cache Error: %s' % (str(e)))
                    if '401' in str(e):
                        resolver.refresh_token()
                    try:
                        check = resolver._RealDebridResolver__check_cache(url)
                    except Exception as e:
                        log_utils.log('Debrid - Check Cache Fallback Error: %s' % (str(e)))
                        return False

                log_utils.log('Debrid - Check Torrent Cache - check: %s' % str(check))
                if len(check) > 0:
                    return True
                else:
                    return False
        else:
            return True
    except Exception:
        failure = traceback.format_exc()
        log_utils.log('Debrid - Check Torrent Cache - Exception: ' + str(failure))
        return False


def resolver(url, debrid):
    try:
        debrid_resolver = [resolver for resolver in debrid_resolvers if resolver.name == debrid][0]

        debrid_resolver.login()
        _host, _media_id = debrid_resolver.get_host_and_id(url)
        stream_url = debrid_resolver.get_media_url(_host, _media_id, cached_only=True)

        return stream_url
    except Exception as e:
        log_utils.log('%s Resolve Failure: %s' % (debrid, e), log_utils.LOGWARNING)
        return None
