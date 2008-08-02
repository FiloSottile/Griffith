# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Piotr Ożarowski
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
import gutils, movie
import re,string

plugin_name        = 'Filmweb'
plugin_description    = 'Web pełen filmów'
plugin_url        = 'www.filmweb.pl'
plugin_language        = _('Polish')
plugin_author        = 'Piotr Ożarowski'
plugin_author_email    = '<ozarow+griffith@gmail.com>'
plugin_version        = '1.12'

class Plugin(movie.Movie):
    TRAILER_PATTERN     = re.compile("""<a class=["']notSelected["'].*?href=["'](.*?)["']>zwiastuny</a>\s*\[\d+\]\s*&raquo;""")
    DIRECTOR_PATTERN    = re.compile('yseria\s+(.*)\s+scenariusz', re.MULTILINE)
    O_TITLE_AKA_PATTERN = re.compile('\(AKA\s+(.*?)\)')

    def __init__(self, id):
        self.movie_id = 'filmweb'
        self.url      = str(id)
        self.encode   = 'utf-8'

    def get_image(self):
        if string.find(self.page,'<div class="film-poster">') > -1:
            self.image_url = gutils.trim(self.page, 'rel="artshow" href="', '">')
        else:
            self.image_url = ''

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<title>', '</title>')
        if string.find(self.o_title, '/') > -1:
            self.o_title = gutils.trim(self.o_title, '/', '(')
        if string.find(self.o_title, '(') > -1:
            self.o_title = gutils.before(self.o_title, '(')

    def get_title(self):
        self.title = gutils.trim(self.page, '<title>', '</title>')
        if string.find(self.title, '(') > -1:
            self.title = gutils.before(self.title, '(')
        if string.find(self.title, '/') > -1:
            self.title = gutils.before(self.title, '/')
            
    def get_director(self):
        director = self.DIRECTOR_PATTERN.findall(self.page)
        if len(director)>0:
            self.director = director[0]
            self.director = string.replace(self.director, "\t",'')
            self.director = re.sub('\s+', ' ', self.director)
            self.director = string.replace(self.director, ",",", ")
            self.director = string.replace(self.director, "  "," ")
            self.director = string.replace(self.director, " ,  ",", ")
            self.director = string.replace(self.director, ",  (wi\xeacej&#160;...)",'')

    def get_plot(self):
        self.plot = gutils.trim(self.page,'<h2 id="o-filmie-header" class="replace">','</div>')
        self.plot = gutils.after(self.plot, '<p>')
        url = gutils.trim(self.plot,"\t...","</a>")
        url = gutils.trim(url, 'href="','"')
        self.plot = gutils.strip_tags(self.plot)
        if url != '':
            plot_page = self.open_page(url=url)
            self.plot = gutils.trim(plot_page, '<div class="filmContent">', '</ul>')
            self.plot = gutils.after(self.plot, 'zgłoś poprawkę')

    def get_year(self):
        self.year = gutils.trim(self.page, '<span class="year">', '</a>')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page,"\tczas trwania: ","\n")

    def get_genre(self):
        self.genre = gutils.trim(self.page,"\tgatunek:", '</p>')
        self.genre = string.replace(self.genre, "\t",'')
        self.genre = string.replace(self.genre, "\n",'')

    def get_cast(self):
        self.cast = gutils.trim(self.page, '<td class="film-actor">',"zobacz więcej")
        self.cast = string.replace(self.cast, chr(13),"")
        self.cast = string.replace(self.cast, chr(10),"")
#        self.cast = string.replace(self.cast, "\n","")
        self.cast = string.replace(self.cast, "\t",'')
        self.cast = string.replace(self.cast, "  ",'')
        self.cast = string.replace(self.cast, '<td class="film-protagonist">', _(" as "))
        self.cast = string.replace(self.cast, '</tr>',"\n")
        self.cast = gutils.strip_tags(self.cast)

    def get_classification(self):
        self.classification = gutils.trim(self.page,"\tod lat: ","\t")
        self.classification = string.replace(self.classification, "\t",'')
        self.classification = string.replace(self.classification, "\n",'')

    def get_studio(self):
        self.studio = ''

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        trailer = self.TRAILER_PATTERN.findall(self.page)
        if trailer:
            self.trailer = trailer[0]

    def get_country(self):
        self.country = gutils.trim(self.page,"\tprodukcja:", '</strong>')
        self.country = string.replace(self.country, "\t",'')

    def get_rating(self):
        self.rating = gutils.trim(self.page, '\t<span><strong class="value">', '</strong>')
        if self.rating != '':
            self.rating = string.replace(self.rating, ',', '.')
            self.rating = str( float(string.strip(self.rating)) )

    def get_notes(self):
        self.notes = ''

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.encode='utf-8'
        self.original_url_search   = "http://www.filmweb.pl/szukaj?c=film&q="
        self.translated_url_search = "http://www.filmweb.pl/szukaj?c=film&q="

    def search(self,parent_window):
        self.open_search(parent_window)
        pos = string.find(self.page, 'Znaleziono <b>')
        if pos == -1:    # movie page
            self.page = None
        else:        # search results
            items = gutils.trim(self.page[pos:], '<b>', '</b>')
            if items == '0':
                self.page = False
            else:
                self.page = gutils.before(self.page[pos:], 'id="sitemap"')
                self.page = gutils.after(self.page, '<li ')
        return self.page

    def get_searches(self):
        if self.page is None:    # movie page
            self.number_results = 1
            self.ids.append(self.url)
            self.titles.append(gutils.convert_entities(self.title))
        elif self.page is False: # no movie found
            self.number_results = 0
        else:            # multiple matches
            elements = string.split(self.page, '<li ')
            self.number_results = elements[-1]
            if (elements[0]<>''):
                for element in elements:
                    element = gutils.after(element, '<a class="searchResultTitle" href="')
                    self.ids.append(gutils.before(element, '">'))
                    element = gutils.trim(element, '">', '</a>')
                    element = gutils.convert_entities(element)
                    element = gutils.strip_tags(element)
                    self.titles.append(element)
            else:
                self.number_results = 0
