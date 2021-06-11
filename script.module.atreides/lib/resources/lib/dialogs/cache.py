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
import xbmcaddon
import xbmcgui

from resources.lib.dialogs import notification
from resources.lib.dialogs import themecontrol
from resources.lib.modules import control, log_utils

CACHE_LIST = [
    ("Base", "Clear Base Cache", 32648, "RunPlugin(plugin://plugin.video.atreides/?action=clearBaseCache)"),
    ("Providers", "Clear Provider Cache", 32649, "RunPlugin(plugin://plugin.video.atreides/?action=clearProviderCache)"),
    ("Meta", "Clear Meta Cache", 32650, "RunPlugin(plugin://plugin.video.atreides/?action=clearMetaCache)"),
    ("Search", "Clear Search History", 32651, "RunPlugin(plugin://plugin.video.atreides/?action=clearCacheSearch)"),
    ("All", "Clear All Cache", 32652, "RunPlugin(plugin://plugin.video.atreides/?action=clearAllCache)")]


def Cache_Dialog():
    class Cache_Window(xbmcgui.WindowXMLDialog):
        # until now we have a blank window, the onInit function will parse your xml file
        def onInit(self):
            self.last_selection = 'base'
            self.colors = themecontrol.ThemeColors()

            self.setProperty('mhtext', self.colors.mh_color)
            self.setProperty('mttext', self.colors.mt_color)
            self.setProperty('dhtext', self.colors.dh_color)
            self.setProperty('dttext', self.colors.dt_color)
            self.setProperty('fttext', self.colors.focus_textcolor)

            self.menu_list = 100
            self.menu = self.getControl(self.menu_list)
            self.header_id = 400
            self.header = self.getControl(self.header_id)
            self.desc_id = 501
            self.desc = self.getControl(self.desc_id)
            self.closebtn = 150
            self.clearbtn = 250

            menu_items = []
            for item in CACHE_LIST:
                the_item = control.item(label=item[0])
                menu_items.append(the_item)
            self.menu.addItems(menu_items)
            self.last_selection = 'Base'
            self.header.setLabel("Clear Base Cache")
            self.desc.setText(control.lang(32648).encode('utf-8'))

            # this puts the focus on the top item of the container
            self.setFocusId(self.getCurrentContainerId())
            self.setFocus(self.getControl(self.menu_list))
            xbmc.executebuiltin("Dialog.Close(busydialog)")

        def onClick(self, controlId):
            if (controlId == self.closebtn):
                self.close()
            elif (controlId == self.clearbtn):
                control.idle()
                from resources.lib.dialogs import yesno
                yes = yesno.YN_Dialog('Cache Tool', control.lang(32056).encode('utf-8'))
                if not yes:
                    return
                self.close()

                func = None
                for item in CACHE_LIST:
                    if str(item[0]) == self.last_selection:
                        func = item[3]
                        break

                if func is not None:
                    xbmc.executebuiltin(func)

                notification.infoDialog(msg=control.lang(32057).encode('utf-8'), style='INFO')

        def onAction(self, action):
            if action == themecontrol.ACTION_PREVIOUS_MENU or action == themecontrol.ACTION_NAV_BACK:
                self.close()
            elif any(i == action for i in themecontrol.MENU_ACTIONS):
                try:
                    '''
                    self.last_selection is used so the same code does keep running while the mouse is
                    hovering over the same item during movement.
                    '''
                    if (self.getFocusId() > 0):
                        self.setFocusId(self.getFocusId())
                    '''
                    Moving through the menu, so works to adjust the visibility of labels and buttons in
                    the XML. The property is also used to determine the onclick action of the button.
                    Allowing us to reduce actual code needing to be ran for control of a more or less
                    static XML and Code that most likely will never change once done.
                    '''
                    if self.getFocusId() == self.menu_list:
                        try:
                            selection = self.menu.getListItem(self.menu.getSelectedPosition()).getLabel()
                            if self.last_selection != selection:
                                self.last_selection = selection
                                for item in CACHE_LIST:
                                    if self.last_selection == item[0]:
                                        self.header.setLabel(item[1])
                                        self.desc.setText(control.lang(item[2]).encode('utf-8'))
                        except Exception:
                            failure = traceback.format_exc()
                            log_utils.log('Fuck, it failed.\n' + failure)
                except Exception:
                    pass


    cwindow = Cache_Window('Cache_Tool.xml', themecontrol.skinModule(), themecontrol.skinTheme(), '1080i')
    cwindow.doModal()
    del cwindow
