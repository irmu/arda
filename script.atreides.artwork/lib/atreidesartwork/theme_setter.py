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
# Addon id: script.atreides.artwork
# Addon Provider: House Atreides

import os
import re

import xbmc
import xbmcaddon


def Apply_Theme(new_theme):
    try:
        __settings__ = xbmcaddon.Addon(id='plugin.video.atreides')
        __settings__.setSetting("appearance.1", new_theme)
        print '[ATREIDES] #### Theme Setter: Theme Set To ' + str(new_theme)
    except Exception:
        pass
