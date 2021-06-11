# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Welcome to House Atreides.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: AutoExec for Atreides
# Addon id: script.atreides.artwork
# Addon Provider: House Atreides

import xbmcgui
import xbmcvfs
from atreidesartwork import theme_setter


def main():
    try:
        theme_setter.Apply_Theme('Collusion')
        xbmcvfs.delete('special://userdata/autoexec.py')
    except Exception:
        xbmcvfs.delete('special://userdata/autoexec.py')


if __name__ == '__main__':
    main()
