#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmcgui

from strings import *
import buggalo
import source

ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_UP = 3
ACTION_DOWN = 4
ACTION_PAGE_UP = 5
ACTION_PAGE_DOWN = 6
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
ACTION_SHOW_INFO = 11
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15

ACTION_BIG_STEP_FORWARD = 22
ACTION_BIG_STEP_BACK = 23

ACTION_REMOTE0 = 58
ACTION_REMOTE1 = 59
ACTION_REMOTE2 = 60
ACTION_REMOTE3 = 61
ACTION_REMOTE4 = 62
ACTION_REMOTE5 = 63
ACTION_REMOTE6 = 64
ACTION_REMOTE7 = 65
ACTION_REMOTE8 = 66
ACTION_REMOTE9 = 67

ACTION_NEXT_SCENE = 138
ACTION_PREV_SCENE = 139

ACTION_JUMP_SMS2 = 142
ACTION_JUMP_SMS3 = 143
ACTION_JUMP_SMS4 = 144
ACTION_JUMP_SMS5 = 145
ACTION_JUMP_SMS6 = 146
ACTION_JUMP_SMS7 = 147
ACTION_JUMP_SMS8 = 148
ACTION_JUMP_SMS9 = 149

KEY_NAV_BACK = 92
KEY_CONTEXT_MENU = 117
KEY_HOME = 159

TELETEXT_URL_DR1 = 'http://www.dr.dk/cgi-bin/fttv1.exe/%s'
TELETEXT_URL_DR2 = 'http://www.dr.dk/cgi-bin/fttv2.exe/%s'

class TeleTextWindow(xbmcgui.WindowXML):
    C_PAGE_PREV_SUBPAGE = 96
    C_PAGE_NEXT_SUBPAGE = 97
    C_PAGE_SUBPAGE = 98
    C_PAGE_NOT_FOUND = 99
    C_PAGE_IDX = 100
    C_PAGE_FRONTPAGE = 101
    C_PAGE_INDEX = 102
    C_PAGE_NEWS = 103
    C_PAGE_SPORT = 104
    C_PAGE_WEATHER = 105
    C_PAGE_TRAFFIC = 106
    C_PAGE_TV = 107
    C_PAGE_RADIO = 108

    C_SOURCE_DR1 = 201
    C_SOURCE_DR2 = 202
    C_SOURCE_TV2 = 203
    C_IMAGE = 1000

    def __new__(cls):
        return super(TeleTextWindow, cls).__new__(cls, 'script-teletext-main.xml', ADDON.getAddonInfo('path'))

    def __init__(self):
        super(TeleTextWindow, self).__init__()
        self.currentPageIdx = -1
        self.currentSubPageIdx = -1
        self.numbers = ''
        self.source = source.DR1Source()

    @buggalo.buggalo_try_except()
    def onInit(self):
        self.getControl(TeleTextWindow.C_PAGE_NOT_FOUND).setVisible(False)
        url = self.loadPage()
        if url:
            self.getControl(TeleTextWindow.C_IMAGE).setImage(url)

    @buggalo.buggalo_try_except()
    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK]:
            self.close()

        elif ACTION_REMOTE0 <= action.getId() <= ACTION_REMOTE9:
            self.numbers += str(action.getId() - ACTION_REMOTE0)
            self.getControl(TeleTextWindow.C_PAGE_IDX).setLabel(self.numbers)

            if len(self.numbers) >= 3:
                self.loadPage(int(self.numbers))
                self.numbers = ''

        elif ACTION_JUMP_SMS2 <= action.getId() <= ACTION_JUMP_SMS9:
            self.numbers += str(action.getId() - ACTION_JUMP_SMS2 + 2)
            self.getControl(TeleTextWindow.C_PAGE_IDX).setLabel(self.numbers)

            if len(self.numbers) >= 3:
                self.loadPage(int(self.numbers))
                self.numbers = ''

        elif action.getId() in [ACTION_PAGE_UP, ACTION_NEXT_SCENE, ACTION_NEXT_ITEM, ACTION_BIG_STEP_FORWARD]:
            self.loadPage(self.currentPageIdx + 1)
        elif action.getId() in [ACTION_PAGE_DOWN, ACTION_PREV_SCENE, ACTION_PREV_ITEM, ACTION_BIG_STEP_BACK]:
            self.loadPage(self.currentPageIdx - 1)

    @buggalo.buggalo_try_except()
    def onClick(self, controlId):
        if controlId == self.C_SOURCE_DR1:
            self.source = source.DR1Source()
            self.loadPage()
        elif controlId == self.C_SOURCE_DR2:
            self.source = source.DR2Source()
            self.loadPage()
        elif controlId == self.C_SOURCE_TV2:
            self.source = source.TV2Source()
            self.loadPage()

        elif controlId == self.C_PAGE_PREV_SUBPAGE:
            self.currentSubPageIdx -= 1
            if self.currentSubPageIdx < 1:
                self.currentSubPageIdx = self.source.getSubPageCount()
            self.loadPage(self.currentPageIdx, self.currentSubPageIdx)
        elif controlId == self.C_PAGE_NEXT_SUBPAGE:
            self.currentSubPageIdx += 1
            if self.currentSubPageIdx > self.source.getSubPageCount():
                self.currentSubPageIdx = 1
            self.loadPage(self.currentPageIdx, self.currentSubPageIdx)

        elif controlId == self.C_PAGE_FRONTPAGE:
            self.loadPage(self.source.getPageIndex(source.PAGE_FRONTPAGE))
        elif controlId == self.C_PAGE_INDEX:
            self.loadPage(self.source.getPageIndex(source.PAGE_INDEX))
        elif controlId == self.C_PAGE_NEWS:
            self.loadPage(self.source.getPageIndex(source.PAGE_NEWS))
        elif controlId == self.C_PAGE_SPORT:
            self.loadPage(self.source.getPageIndex(source.PAGE_SPORT))
        elif controlId == self.C_PAGE_WEATHER:
            self.loadPage(self.source.getPageIndex(source.PAGE_WEATHER))
        elif controlId == self.C_PAGE_TRAFFIC:
            self.loadPage(self.source.getPageIndex(source.PAGE_TRAFFIC))
        elif controlId == self.C_PAGE_TV:
            self.loadPage(self.source.getPageIndex(source.PAGE_TV))
        elif controlId == self.C_PAGE_RADIO:
            self.loadPage(self.source.getPageIndex(source.PAGE_RADIO))


    @buggalo.buggalo_try_except()
    def onFocus(self, controlId):
        pass


    def loadPage(self, pageIdx = 100, subPageIdx = 1):
        print "pageIdx = %d; subPageIdx = %d" % (pageIdx, subPageIdx)
        self.getControl(TeleTextWindow.C_PAGE_NOT_FOUND).setVisible(False)
        if pageIdx < 100:
            pageIdx = 999
        elif pageIdx > 999:
            pageIdx = 100

        self.currentPageIdx = pageIdx
        self.currentSubPageIdx = subPageIdx
        self.getControl(TeleTextWindow.C_PAGE_IDX).setLabel(str(pageIdx))

        try:
            url = self.source.getPageImageUrl(pageIdx, subPageIdx)
            self.getControl(TeleTextWindow.C_IMAGE).setImage(url)
            subPageLabel = "%d / %d" % (subPageIdx, self.source.getSubPageCount())
            self.getControl(TeleTextWindow.C_PAGE_SUBPAGE).setLabel(subPageLabel)
        except source.PageNotFoundException:
            self.getControl(TeleTextWindow.C_PAGE_NOT_FOUND).setVisible(True)

