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

import os
import glob
import pyxbmct
import traceback
import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.dialogs import themecontrol
from resources.lib.modules import control, log_utils


class ArtworkDialog(pyxbmct.BlankDialogWindow):
    def __init__(self):
        super(ArtworkDialog, self).__init__()
        self.setGeometry(650, 650, 60, 60)

        self.colors = themecontrol.ThemeColors()

        self.Background = pyxbmct.Image(themecontrol.bg_mid)
        self.placeControl(self.Background, 0, 0, rowspan=60, columnspan=60)

        self.selectedArtwork = control.appearance()

        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_controls(self):
        '''
        Header Text Placement
        '''
        self.header_text = '[B]Theme Selection[/B]'
        self.Header = pyxbmct.Label(self.header_text, alignment=pyxbmct.ALIGN_CENTER, textColor=self.colors.dh_color)
        self.placeControl(self.Header, 3, 0, rowspan=2, columnspan=60)

        '''
        58 characters per line
        '''
        msg = 'Please select the artwork that you would like to use.\nThis is pulled from the selected Artwork Module. You can\nchange the Artwork Module used from the Tools\nMenu by selecting Artwork Module and typing the ID\nof the new module.'
        self.Description = pyxbmct.Label(msg)
        self.placeControl(self.Description, 6, 4, rowspan=12, columnspan=53)

        self.menu = pyxbmct.List(textColor=self.colors.mt_color)
        self.placeControl(self.menu, 24, 21, rowspan=30, columnspan=17)
        items = []
        self.aModule_base = xbmcaddon.Addon('script.atreides.artwork').getSetting('artwork_module')
        self.aModule = os.path.join(xbmcaddon.Addon(self.aModule_base).getAddonInfo('path'), 'resources', 'media')
        for folder in glob.glob("%s/*" % (self.aModule)):
            folder = os.path.split(folder)[1].capitalize()
            items.append(folder)
        self.menu.addItems(items)
        self.connect(self.menu, self.menu_handler)

        self.Preview = pyxbmct.Image('%s/%s/tools.png' % (self.aModule, items[0]))
        self.placeControl(self.Preview, 24, 3, rowspan=17, columnspan=17)

        self.module_text = 'Current Module: %s' % (self.aModule_base)
        self.Module = pyxbmct.Label(self.module_text, alignment=pyxbmct.ALIGN_CENTER, textColor=self.colors.dh_color)
        self.placeControl(self.Module, 50, 0, rowspan=2, columnspan=60)

        self.OKButton = pyxbmct.Button(
            'OK', textColor='0xFFFFFFFF', shadowColor='0xFF000000', focusedColor='0xFFbababa',
            focusTexture=themecontrol.btn_focus, noFocusTexture=themecontrol.btn_nofocus)
        self.placeControl(self.OKButton, 53, 35, rowspan=4, columnspan=10)
        self.connect(self.OKButton, self.save_theme)

        self.CancelButton = pyxbmct.Button(
            'Cancel', textColor='0xFFFFFFFF', shadowColor='0xFF000000', focusedColor='0xFFbababa',
            focusTexture=themecontrol.btn_focus, noFocusTexture=themecontrol.btn_nofocus)
        self.placeControl(self.CancelButton, 53, 46, rowspan=4, columnspan=10)
        self.connect(self.CancelButton, self.close)

    def set_navigation(self):
        self.menu.controlDown(self.OKButton)
        self.OKButton.controlRight(self.CancelButton)
        self.OKButton.controlUp(self.menu)
        self.CancelButton.controlUp(self.menu)
        self.CancelButton.controlLeft(self.OKButton)

        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.update_view)

        self.setFocus(self.menu)

    def update_view(self):
        if self.getFocus() == self.menu:
            selection = self.menu.getListItem(self.menu.getSelectedPosition()).getLabel().lower()
            self.Preview.setImage('%s/%s/tools.png' % (self.aModule, selection))

    def menu_handler(self):
        try:
            self.selectedArtwork = self.menu.getListItem(self.menu.getSelectedPosition()).getLabel().lower()
            self.setFocus(self.OKButton)
        except Exception:
            pass
        pass

    def save_theme(self):
        control.setSetting('appearance.1', self.selectedArtwork)
        self.close()
        control.refresh()


def load():
    dialog = ArtworkDialog()
    dialog.doModal()
    del dialog
