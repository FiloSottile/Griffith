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

import gutils, movie, string

plugin_name = 'Filmweb'
plugin_description = 'Web pełen filmów'
plugin_url = 'www.filmweb.pl'
plugin_server = '193.200.227.13'
plugin_language = _('Polish')
plugin_author = 'Piotr Ożarowski, Bartosz Kurczewsk, Mariusz Szczepanek'
plugin_author_email = '<mariusz2806@gmail.com>'
plugin_version = '1.21'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.movie_id = 'filmweb'
        self.url = str(id)
        self.encode = 'utf-8'

    def get_image(self):
        if string.find(self.page, '<div class="posterLightbox">') > -1:
            self.image_url = gutils.trim(self.page, '<div class="posterLightbox">', '</div>')
            self.image_url = gutils.trim(self.image_url, 'href="', '" ')
        else:
            self.image_url = ''

    def get_o_title(self):
        self.url = string.replace(self.url, plugin_server, plugin_url)
        self.o_title = gutils.trim(self.page, '<title>', '</title>')
        if string.find(self.o_title, '/') > -1:
            self.o_title = gutils.trim(self.o_title, '/', '(')
        if string.find(self.o_title, '(') > -1:
            self.o_title = gutils.before(self.o_title, '(')

    def get_title(self):
        self.url = string.replace(self.url, plugin_server, plugin_url)
        self.title = gutils.trim(self.page, '<title>', '</title>')
        if string.find(self.title, '(') > -1:
            self.title = gutils.before(self.title, '(')
        if string.find(self.title, '/') > -1:
            self.title = gutils.before(self.title, '/')

    def get_director(self):
        self.director = gutils.trim(self.page, "reżyseria:", '</tr>')
        self.director = gutils.after(self.director, '</th>')
        self.director = string.replace(self.director, "(więcej...)", '')
        self.director = string.replace(self.director, '  ', '\t')
        self.director = string.replace(self.director, "\t ", '')
        self.director = string.replace(self.director, "\t", '')
        self.director = string.replace(self.director, ',', ', ')
        self.director = gutils.strip_tags(self.director)

    def get_screenplay(self):
        self.screenplay = gutils.trim(self.page,"scenariusz:", '</tr>')
        self.screenplay = gutils.after(self.screenplay, '</th>')
        self.screenplay = string.replace(self.screenplay, "(więcej...)", '')
        self.screenplay = string.replace(self.screenplay, '  ', '\t')
        self.screenplay = string.replace(self.screenplay, "\t ", '')
        self.screenplay = string.replace(self.screenplay, "\t", '')
        self.screenplay = string.replace(self.screenplay, ',', ', ')
        self.screenplay = gutils.strip_tags(self.screenplay)

    def get_plot(self):
        self.plot = gutils.trim(self.page, '<span class="filmDescrBg">', '</span>')
        self.plot = string.replace(self.plot, '  ', ' ')

    def get_year(self):
        self.year = gutils.trim(self.page, '<span id="filmYear" class="filmYear">', '</span>')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, '<div class="time">', '<')

    def get_genre(self):
        self.genre = gutils.trim(self.page, "gatunek:", '</tr>')
        self.genre = string.replace(self.genre, "\t", '')
        self.genre = string.replace(self.genre, "\n", '')
        self.genre = string.replace(self.genre, '  ', '')
        self.genre = string.replace(self.genre, ',', ', ')

    def get_cast(self):
        self.cast = gutils.trim(self.page, '<div class="castListWrapper cl">', '<div class="additional-info comBox">')
        url = gutils.after(self.cast, '</ul>')
        url = gutils.trim(url, 'href="','"')
        self.cast = gutils.before(self.cast, '</ul>')
        self.cast = string.replace(self.cast, chr(13), '')
        self.cast = string.replace(self.cast, chr(10), '')
        self.cast = string.replace(self.cast, "  ", '\t')
        self.cast = string.replace(self.cast, "\t ", '')
        self.cast = string.replace(self.cast, '\t', '')
        self.cast = string.replace(self.cast, " (", '(')
        self.cast = string.replace(self.cast, '(', " (")
        self.cast = string.replace(self.cast, '<div>', _(" as "))
        self.cast = string.replace(self.cast, '</li>', "\n")

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = ''

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = gutils.trim(self.page, "produkcja:", '</tr>')
        self.country = string.replace(self.country, '  ', '')
        self.country = string.replace(self.country, "\t", '')

    def get_rating(self):
        self.rating = gutils.trim(self.page, '<div class="rates">', '</div>')
        self.rating = gutils.trim(self.rating, '<span class="average">', '</span>')
        if self.rating != '':
            self.rating = string.replace(self.rating, ' ', '')
            self.rating = string.replace(self.rating, ',', '.')
            self.rating = str(float(string.strip(self.rating)))

    def get_notes(self):
        self.notes = ''

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.encode='utf-8'
        self.original_url_search = 'http://' + plugin_server + '/search?alias=film&q='
        self.translated_url_search = 'http://' + plugin_server + '/search?alias=film&q='

    def search(self, parent_window):
        if not self.open_search(parent_window):
            return None
        pos = string.find(self.page, '<div class="stdBar">')
        if pos == -1: # movie page
            self.page = None
        else: # search results
            items = gutils.trim(self.page[pos:], '(', ')')
            if items == '0':
                self.page = False
            else:
                self.page = gutils.before(self.page[pos:], '</ul>')
                self.page = gutils.after(self.page, '<li ')
        return self.page

    def get_searches(self):
        if self.page is None: # movie page
            self.ids.append(self.url)
            self.titles.append(gutils.convert_entities(self.title))
        elif self.page is False: # no movie found
            self.number_results = 0
        else: # multiple matches
            elements = string.split(self.page, '<li ')
            self.number_results = elements[-1]
            if (elements[0] <> ''):
                for element in elements:
                    element = gutils.after(element, '<a href="')
                    self.ids.append('http://' + plugin_server + gutils.before(element, '"'))
                    element_title = gutils.trim(element, 'class="searchResultTitle"', '</a>')
                    element_title = gutils.after(element_title, '">')
                    element_title = string.replace(element_title, "\t", '')
                    element = gutils.after(element, 'class="searchResultDetails"')
                    element_year = gutils.trim(element, '>', '|')
                    element_year = string.replace(element_year, " ", '')
                    element_year = gutils.strip_tags(element_year)
                    element_country = gutils.trim(element, '">', '</a>')
                    element = string.strip(element_title)
                    if (element_year <> ''):
                        element = element + ' (' + string.strip(element_year) + ')'
                    if (element_country <> ''):
                        element = element + ' - ' + string.strip(element_country)
                    element = gutils.convert_entities(element)
                    element = gutils.strip_tags(element)
                    self.titles.append(element)
            else:
                self.number_results = 0
