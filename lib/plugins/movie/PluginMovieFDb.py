# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2007 Piotr Ozarowski
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

import gettext
gettext.install('griffith', unicode=1)
import gutils
import movie
import string
import re

plugin_name        = 'FDb'
plugin_description    = 'Internetowa baza filmowa'
plugin_url        = 'fdb.pl'
plugin_language        = _('Polish')
plugin_author        = 'Piotr Ożarowski'
plugin_author_email    = '<ozarow+griffith@gmail.com>'
plugin_version        = '1.9'

class Plugin(movie.Movie):
    TRAILER_PATTERN = re.compile('http://.*\.fdb\.pl/zwiastuny/odtwarzaj/[0-9]*')

    def __init__(self, movie_id):
        from md5 import md5
        self.movie_id = md5(movie_id).hexdigest()
        self.encode   = 'utf-8'
        if string.find(movie_id, 'http://') != -1:
            self.url = str(movie_id)
        else:
            self.url = "http://fdb.pl/%s" % str(movie_id)

    def get_image(self):
        self.image_url = gutils.trim(self.page, 'class="poster"', '/></a>')
        self.image_url = gutils.trim(self.image_url,'src="','"')
        if self.image_url.endswith('no_picture.png'):
            self.image_url = ''

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<h2>', '</h2>')
        self.o_title = gutils.strip_tags(self.o_title)
        if self.o_title == '':
            self.o_title = self.get_title(True)

    def get_title(self, extra=False):
        data = gutils.trim(self.page,'<title>', '</title>')
        tmp = string.find(data, '(')
        if tmp != -1:
            data = data[:tmp]
        if extra is False:
            self.title = data
        else:
            return data

    def get_director(self):
        self.director = ''
        elements = gutils.trim(self.page,'>Reżyseria</h4>','</div>')
        elements = string.split(elements, '</li>')
        if elements[0] != '':
            for element in elements:
                element = gutils.trim(element, '>', '</a')
                if element != '':
                    self.director += ', ' + element
            self.director = string.replace(self.director[2:], ', &nbsp;&nbsp;&nbsp;(więcej)', '')

    def get_plot(self):
        self.plot = gutils.trim(self.page,'/opisy">','</a>')
        self.plot = self.TRAILER_PATTERN.sub('', self.plot)

    def get_year(self):
        self.year = gutils.trim(self.page,'<small>(', ')</small>')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page,'Czas trwania</h4>','</div>')
	self.runtime = gutils.trim(self.runtime,'<li>',' minut')

    def get_genre(self):
        self.genre = gutils.trim(self.page,'Gatunek</h4>','</div>')
	self.genre = gutils.trim(self.genre,'<li>','</li>')
	self.genre = string.replace(self.genre, ' / ', ' | ')

    def get_cast(self):
        self.cast = gutils.trim(self.page,'Obsada</h3>','</div>')
	self.cast = gutils.trim(self.cast,"<table>\n",'  </table>')
	if self.cast != '':
	    self.cast = gutils.strip_tags(self.cast)
	    self.cast = self.cast.replace("      ","")
	    self.cast = self.cast.replace("    ","")
	    self.cast = self.cast.replace("\n...\n\n  ",_(' as '))
	    self.cast = self.cast.replace("\n\n\n\n\n","")

    def get_classification(self):
        self.classification = gutils.trim(self.page,"Od lat</h4>","</div>")
	self.classification = gutils.trim(self.classification,'<li>','</li>')

    def get_studio(self):
        self.studio = ''

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        trailer_url = self.TRAILER_PATTERN.findall(self.page)
        if trailer_url:
            self.trailer = trailer_url[0]

    def get_country(self):
        self.country = gutils.trim(self.page,'Kraj produkcji</h4>','</div>')
	self.country = gutils.trim(self.country,'<li>','</li>')

    def get_rating(self):
        self.rating = gutils.trim(self.page, 'class="vote"','</strong>')
        self.rating = gutils.after(self.rating, '<strong>')
        if self.rating:
            self.rating = str(float(gutils.clean(self.rating)))

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.encode = 'utf-8'
        self.original_url_search    = 'http://fdb.pl/szukaj.php?t=f&s='
        self.translated_url_search    = 'http://fdb.pl/szukaj.php?t=f&s='

    def search(self,parent_window):
        self.open_search(parent_window)
        tmp = string.find(self.page,'<div>Wyniki wyszukiwania dla')
        if tmp == -1:        # already a movie page
            self.page = ''
        else:            # multiple matches
            self.page = gutils.before(self.page[tmp:],'<div id="mapaSerwisu">');
        return self.page

    def get_searches(self):
        if self.page == '':    # movie page already
            self.number_results = 1
            self.ids.append(self.url)
            self.titles.append(self.title)
        else:            # multiple matches
            elements = string.split(self.page,'<div class="searchItem">')
            if len(elements)>0:
                for element in elements:
                    tmpId = gutils.trim(element, '<a href="', '"')
                    if tmpId.endswith('dodajNowy.php'):
                        continue
                    self.ids.append(tmpId)
                    element = gutils.strip_tags(
                        gutils.trim(element, '">', '</div>'))
                    element = element.replace("\n", '')
                    element = element.replace('   ', '')
                    element = element.replace('aka ', ' aka ')
                    element = element.replace(' - Oryginalny', '')
                    self.titles.append(element)
            else:
                self.number_results = 0
