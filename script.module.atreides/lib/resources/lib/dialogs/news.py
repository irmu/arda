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
2019/5/12: Moved news control timer to news dialog
'''

import time

import pyxbmct
import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.dialogs import themecontrol
from resources.lib.modules import client, control, log_utils


newsfile = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L21nU3h1WnZ6'.decode('base64')
changesfile = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L3pNNkc3TjBS'.decode('base64')
approvedfile = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L2RmNDIyMlJE'.decode('base64')
paypalfile = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L0tYdERqMnQ2'.decode('base64')
scraperfile = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L016VlJUcGQy'.decode('base64')
rdfile = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L1VrWURnY1du'.decode('base64')
torrentfile = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L3EyMEpnODg2'.decode('base64')

scrapervid = 'aHR0cHM6Ly9naXRodWIuY29tL211YWRkaWJ0dHYvYXJ0d29yay9ibG9iL21hc3Rlci92aWRlb3Mvc2NyYXBlcnMtYW5kLWZpbHRlcnMubXA0P3Jhdz10cnVl'
rdvid = 'aHR0cHM6Ly9naXRodWIuY29tL211YWRkaWJ0dHYvYXJ0d29yay9ibG9iL21hc3Rlci92aWRlb3MvcmVhbC1kZWJyaWQubXA0P3Jhdz10cnVl'
torrentvid = 'aHR0cHM6Ly9naXRodWIuY29tL211YWRkaWJ0dHYvYXJ0d29yay9ibG9iL21hc3Rlci92aWRlb3MvdHN1cHBvcnQubXA0P3Jhdz10cnVl'


class NewsDialog(pyxbmct.BlankDialogWindow):
    def __init__(self):
        super(NewsDialog, self).__init__()
        self.setGeometry(800, 450, 20, 60)

        self.colors = themecontrol.ThemeColors()

        self.Background = pyxbmct.Image(themecontrol.bg_news)
        self.placeControl(self.Background, 0, 0, rowspan=20, columnspan=60)

        self.news = self.getDialogText(newsfile)
        self.changes = self.getDialogText(changesfile)
        self.approved = self.getDialogText(approvedfile)
        self.paypal = self.getDialogText(paypalfile)
        self.scrapers = self.getDialogText(scraperfile)
        self.rd = self.getDialogText(rdfile)
        self.torrents = self.getDialogText(torrentfile)
        self.set_controls()
        self.set_navigation()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

        self.video = None

    def set_controls(self):
        '''
        Left Side Menu Top Section
        '''
        self.Section1 = pyxbmct.Label('[B]Addon Information[/B]',
                                      alignment=pyxbmct.ALIGN_LEFT, textColor=self.colors.mh_color)
        self.placeControl(self.Section1, 3, 1, columnspan=17)
        self.menu = pyxbmct.List(textColor=self.colors.mt_color)
        self.placeControl(self.menu, 4, 1, rowspan=8, columnspan=17)
        self.menu.addItems(['News',
                            'Changes',
                            'Builds',
                            'Paypal'])
        '''
        Left Side Menu Bottom Section, currently unused
        '''
        self.Section2 = pyxbmct.Label('[B]Tips and Tricks[/B]',
                                      alignment=pyxbmct.ALIGN_LEFT, textColor=self.colors.mh_color)
        self.placeControl(self.Section2, 11, 1, rowspan=4, columnspan=17)
        self.menu2 = pyxbmct.List(textColor=self.colors.mt_color)
        self.placeControl(self.menu2, 12, 1, rowspan=12, columnspan=17)
        self.menu2.addItems(['Scraper Tips',
                             'Real Debrid',
                             'Torrents'])

        self.CloseButton = pyxbmct.Button(
            'Close', textColor='0xFFFFFFFF', shadowColor='0xFF000000', focusedColor='0xFFbababa',
            focusTexture=themecontrol.btn_focus, noFocusTexture=themecontrol.btn_nofocus)
        self.placeControl(self.CloseButton, 17, 10, rowspan=2, columnspan=8)
        self.connect(self.CloseButton, self.close)
        '''
        Right Side, to display stuff for the above menu items
        '''
        self.newsheader = '[B]Latest News[/B]'
        self.Header = pyxbmct.Label(self.newsheader, alignment=pyxbmct.ALIGN_CENTER, textColor=self.colors.dh_color)
        self.placeControl(self.Header, 2, 20, rowspan=1, columnspan=40)
        self.Description = pyxbmct.TextBox(self.news)
        self.placeControl(self.Description, 3, 21, rowspan=16, columnspan=40)
        self.Description.setText(self.news)

        self.RDLink = pyxbmct.Label('Referral Debrid Link: ' + str(get_rd_link()))
        self.placeControl(self.RDLink, 17, 21, rowspan=2, columnspan=32)
        self.RDLink.setVisible(False)

        self.WatchButton = pyxbmct.Button(
            'Watch', textColor='0xFFFFFFFF', shadowColor='0xFF000000', focusedColor='0xFFbababa',
            focusTexture=themecontrol.btn_focus, noFocusTexture=themecontrol.btn_nofocus)
        self.placeControl(self.WatchButton, 15, 36, rowspan=2, columnspan=8)
        self.WatchButton.setVisible(False)
        self.connect(self.WatchButton, self.watchVideo)

    def set_navigation(self):
        self.menu.controlUp(self.menu2)
        self.menu.controlDown(self.menu2)
        self.menu2.controlUp(self.menu)
        self.menu2.controlDown(self.CloseButton)
        self.menu2.controlRight(self.WatchButton)
        self.CloseButton.controlUp(self.menu2)
        self.CloseButton.controlDown(self.menu)
        self.WatchButton.controlLeft(self.menu2)

        self.connectEventList(
            [pyxbmct.ACTION_MOVE_DOWN,
             pyxbmct.ACTION_MOVE_UP,
             pyxbmct.ACTION_MOUSE_WHEEL_DOWN,
             pyxbmct.ACTION_MOUSE_WHEEL_UP,
             pyxbmct.ACTION_MOUSE_MOVE],
            self.update_view)
        # Set initial focus
        self.setFocus(self.menu)

    def update_view(self):
        try:
            if self.getFocus() == self.menu:
                self.WatchButton.setVisible(False)
                self.RDLink.setVisible(False)
                self.video = None
                selection = self.menu.getListItem(self.menu.getSelectedPosition()).getLabel()
                if selection == 'News':
                    self.Header.setLabel(self.newsheader)
                    self.Description.setText(self.news)
                elif selection == 'Changes':
                    self.Header.setLabel('[B]Latest Changes[/B]', textColor=self.colors.dh_color)
                    self.Description.setText(self.changes)
                elif selection == 'Builds':
                    self.Header.setLabel('[B]Approved Builds[/B]', textColor=self.colors.dh_color)
                    self.Description.setText(self.approved)
                elif selection == 'Paypal':
                    self.Header.setLabel('[B]Paypal[/B]', textColor=self.colors.dh_color)
                    self.Description.setText(self.paypal)
            elif self.getFocus() == self.menu2:
                selection = self.menu2.getListItem(self.menu2.getSelectedPosition()).getLabel()
                self.WatchButton.setVisible(True)
                if selection == 'Scraper Tips':
                    self.Header.setLabel('[B]Scraper Tips[/B]', textColor=self.colors.dh_color)
                    self.Description.setText(self.scrapers)
                    self.video = scrapervid
                    self.RDLink.setVisible(False)
                elif selection == 'Real Debrid':
                    self.Header.setLabel('[B]Real Debrid[/B]', textColor=self.colors.dh_color)
                    self.Description.setText(self.rd)
                    self.video = rdvid
                    self.RDLink.setVisible(True)
                elif selection == 'Torrents':
                    self.Header.setLabel('[B]Torrents in Atreides[/B]', textColor=self.colors.dh_color)
                    self.Description.setText(self.torrents)
                    self.video = torrentvid
                    self.RDLink.setVisible(False)
            else:
                pass
        except (RuntimeError, SystemError):
            pass

    def watchVideo(self):
        self.close()
        control.idle()
        # Kernal errors from within YouTube after displaying path details (so crash is permission based?) in Kodi 18. Need to find a valid fix
        # Have tried resolvedUrl but no valid handle due to custom GUI. Executing only causes crash or nothing at all (tried trailer url for
        # atreides default.py and just fails)
        control.execute('PlayMedia("%s")' % (self.video.decode('base64')))

    def getDialogText(self, url):
        try:
            message = open_my_url(url)

            if message is None:
                return 'Nothing today! Blame CNN'
            if '[link]' in message:
                tcolor = '[COLOR %s]' % (self.colors.link_color)
                message = message.replace('[link]', tcolor).replace('[/link]', '[/COLOR]')
            return message
        except Exception:
            return 'Nothing today! Blame CNN'


def get_rd_link():
    import random
    result = random.choice(['aHR0cDovL2JpdC5seS8yRkRlQ1Rx', 'aHR0cDovL2JpdC5seS8yUjJMZFRD',
                            'aHR0cDovL2JpdC5seS8yRkRlQ1Rx'])
    return result.decode('base64')


def open_my_url(url):
    try:
        response = client.request(url)
        return response
    except Exception:
        return None


def load():
    dialog = NewsDialog()
    dialog.doModal()
    del dialog

    newsUpdate = control.setting('NewsUpdate')
    if newsUpdate == '':
        newsUpdate = 1
    else:
        newsUpdate = int(float(newsUpdate))
    if time.time() < newsUpdate:
        return
    newsUpdate = time.time() + (60*60*24*7)
    control.setSetting('NewsUpdate', str(newsUpdate))
