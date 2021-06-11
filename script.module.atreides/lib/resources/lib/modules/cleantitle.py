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
2019/07/17: Added cleanup of long dash
'''

import re
import unicodedata


def get(title):
    if title is None:
        return
    try:
        title = title.encode('utf-8')
    except Exception:
        pass
    title = str(title)
    title = title.rstrip()
    title = title.replace('–', '-')
    title = re.sub('&#(\d);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\s', '', title)
    return title.lower()


def geturl(title):
    if title is None:
        return
    title = title.lower()
    title = title.rstrip()
    title = title.translate(None, ':*?"\'\.<>|&!,')
    title = title.replace('/', '-')
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    title = title.replace('–', '-')
    return title


def get_simple(title):
    if title is None:
        return
    title = title.replace('–', '-')
    title = title.lower()
    title = title.rstrip()
    title = re.sub('(\d{4})', '', title)
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def getsearch(title):
    if title is None:
        return
    title = title.lower()
    title = title.rstrip()
    title = title.replace('–', '-')
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|-|–|:|;|\*|\?|"|\'|<|>|\|', '', title).lower()
    return title


def query(title):
    if title is None:
        return
    title = title.replace('\'', '').rsplit(':', 1)[0].rsplit(' -', 1)[0].replace('-', ' ').replace('–', '-')
    return title


def normalize(title):

    try:
        try:
            return title.decode('ascii').encode("utf-8")
        except Exception:
            pass

        return str(''.join(c for c in unicodedata.normalize('NFKD', unicode(title.decode('utf-8'))) if unicodedata.category(c) != 'Mn'))
    except Exception:
        return title
