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
import urllib2
import re

class PageNotFoundException(Exception):
    pass

class Source(object):
    PAGES = {}
    def getPageIndex(self, page):
        if self.PAGES.has_key(page):
            return self.PAGES[page]
        return None

PAGE_FRONTPAGE = 1
PAGE_INDEX = 2
PAGE_NEWS = 3
PAGE_SPORT = 4
PAGE_WEATHER = 5
PAGE_TRAFFIC = 6
PAGE_TV = 7
PAGE_RADIO = 8

class DR1Source(Source):
    BASE_URL = 'http://www.dr.dk/cgi-bin/fttv1.exe/<PAGE>'
    PAGES = {
        PAGE_FRONTPAGE : 100,
        PAGE_INDEX : 104,
        PAGE_NEWS : 110,
        PAGE_SPORT : 200,
        PAGE_WEATHER : 400,
        PAGE_TRAFFIC : 440,
        PAGE_TV : 300,
        PAGE_RADIO : 600
    }

    def getPageImageUrl(self, page):
        u = urllib2.urlopen(self.BASE_URL.replace('<PAGE>', str(page)))
        html = u.read()
        u.close()

        m = re.search('SRC="(/fttvimg/[^"]+)', html)
        if m is not None:
            return 'http://www.dr.dk%s' % m.group(1)
        else:
            raise PageNotFoundException()


class DR2Source(Source):
    BASE_URL = 'http://www.dr.dk/cgi-bin/fttv2.exe/<PAGE>'
    PAGES = {
        PAGE_FRONTPAGE : 100,
        PAGE_INDEX : 104,
        PAGE_NEWS : 110,
        PAGE_SPORT : 200,
        PAGE_WEATHER : 400,
        PAGE_TRAFFIC : 440,
        PAGE_TV : 300,
        PAGE_RADIO : 600
    }

    def getPageImageUrl(self, page):
        u = urllib2.urlopen(self.BASE_URL.replace('<PAGE>', str(page)))
        html = u.read()
        u.close()

        m = re.search('SRC="(/fttvimg/[^"]+)', html)
        if m is not None:
            return 'http://www.dr.dk%s' % m.group(1)
        else:
            raise PageNotFoundException()


class TV2Source(Source):
    BASE_URL = 'http://ttv.tv2.dk/index.php?side=<PAGE>'
    PAGES = {
        PAGE_FRONTPAGE : 100,
        PAGE_INDEX : 102,
        PAGE_NEWS : 110,
        PAGE_SPORT : 200,
        PAGE_WEATHER : 401,
        PAGE_TV : 300
    }

    def getPageImageUrl(self, page):
        u = urllib2.urlopen(self.BASE_URL.replace('<PAGE>', str(page)))
        html = u.read()
        u.close()

        m = re.search('src="(/gif.php[^"]+)', html)
        if m is not None:
            url = 'http://ttv.tv2.dk%s' % m.group(1)
            url = url.replace('&amp;', '&')
            url = url.replace(' ', '+')
            return url
        else:
            raise PageNotFoundException()
