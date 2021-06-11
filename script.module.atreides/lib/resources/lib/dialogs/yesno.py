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

import xbmc
import xbmcgui
import xbmcaddon

from resources.lib.dialogs import themecontrol
from resources.lib.modules import control, log_utils


def YN_Dialog(title, msg, yestext='Yes', notext='No'):
    class YN_Box(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.colors = themecontrol.ThemeColors()

            self.title = 1
            self.body = 2
            self.yesbtn = 5
            self.nobtn = 6

            self.getControl(self.title).setLabel(title)
            self.setProperty('dhtext', self.colors.dh_color)
            self.setProperty('btnfocus', self.colors.btn_focus)
            self.getControl(self.body).setText(msg)
            self.getControl(self.yesbtn).setLabel(yestext)
            self.getControl(self.nobtn).setLabel(notext)

            xbmc.sleep(100)
            # this puts the focus on the top item of the container
            self.setFocusId(self.getCurrentContainerId())
            self.setFocus(self.getControl(self.nobtn))
            xbmc.executebuiltin("Dialog.Close(busydialog)")

        def onClick(self, controlId):
            if (controlId == self.nobtn):
                self.close()
            if (controlId == self.yesbtn):
                self.close()

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()

    yn = YN_Box('Dialog_YesNo.xml', themecontrol.skinModule(), themecontrol.skinTheme(), '1080i', title=title, msg=msg, yestext=yestext, notext=notext)
    yn.doModal()
    ret = yn.getProperty('btnret')
    del yn
    if ret == 'true':
        return True
    else:
        return False
