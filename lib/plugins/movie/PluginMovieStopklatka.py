# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2008 Piotr Ożarowski
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

from gettext import gettext as _
import gutils, movie
import string, re

plugin_name         = 'Stopklatka'
plugin_description  = 'Internetowy Serwis Filmowy'
plugin_url          = 'www.stopklatka.pl'
plugin_language     = _('Polish')
plugin_author       = 'Piotr Ożarowski'
plugin_author_email = '<ozarow+griffith@gmail.com>'
plugin_version      = '1.9'

class Plugin(movie.Movie):
    IMAGE_PATTERN = re.compile('(http://img.stopklatka.pl/film/.*?)"')

    def __init__(self, id):
        self.movie_id = id
        self.url = "http://www.stopklatka.pl/film/film.asp?fi=%s" % str(self.movie_id)
        self.encode = 'iso-8859-2' # with some cp-1250 data (sic!)

    def initialize(self):
        self.page = self.page.replace('\x9c','ś')
        self.page = self.page.replace('š','ą')

    def get_image(self):
        image = self.IMAGE_PATTERN.findall(self.page)
        if len(image):
            self.image_url = image[0]

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<h2> (', ')</h2>')
        if self.o_title == '':
            self.o_title = self.get_title(True)

    def get_title(self, ret=False):
        data = gutils.trim(self.page, '<h1>', '</h1>')
        if ret is True:
            return data
        else:
            self.title = data

    def get_director(self):
        self.director = gutils.trim(self.page, '>re\xbfyseria:<', '</td></tr>')
        self.director = gutils.after(self.director, '>')

    def get_plot(self):
        self.plot = gutils.trim(self.page, '<p>', '</p>')
        self.plot = gutils.before(self.plot, '<b>Wi\xEAcej ')

    def get_year(self):
        self.year = gutils.trim(self.page, '>rok produkcji:<', '</span>')
        self.year = gutils.after(self.year, '>')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, 'trwania:<', ' min<')
        self.runtime = gutils.after(self.runtime, '>')

    def get_genre(self):
        self.genre = gutils.trim(self.page, '>gatunek:<', '</span>')
        self.genre = gutils.after(self.genre, '>')

    def get_cast(self):
        self.cast = gutils.trim(self.page, '>obsada:<', '</td></tr>')
        self.cast = gutils.after(self.cast, '>')
        self.cast = string.replace(self.cast, ', ', "\n")
        self.cast = gutils.before(self.cast, '<b>Wi\xEAcej ')

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = ""

    def get_o_site(self):
        self.o_site = gutils.trim(self.page,">strona oficjalna:<"," target=_blank")
        self.o_site = gutils.after(self.o_site,"href=")

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = "http://www.stopklatka.pl/film/film.asp?fi=" + self.movie_id + "&sekcja=mmedia"

    def get_country(self):
        self.country = gutils.trim(self.page, '>kraj:<', '</span>')
        self.country = gutils.after(self.country, '>')

    def get_rating(self):
        self.rating = '0'

    def get_notes(self):
        self.notes = ''

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.encode='iso-8859-2'
        self.original_url_search    = "http://www.stopklatka.pl/szukaj/szukaj.asp?kategoria=film&szukaj="
        self.translated_url_search    = "http://www.stopklatka.pl/szukaj/szukaj.asp?kategoria=film&szukaj="

    def search(self,parent_window):
        self.open_search(parent_window)
        self.page = gutils.trim(self.page, '>Wyniki poszukiwania frazy:', '</div>');
        self.page = self.page.replace('\x9c','ś')
        self.page = self.page.replace('š','ą')
        return self.page

    def get_searches(self):
        elements = re.findall("""/film/film.asp\?fi=(\d+)">.*?searchTitle\s*textB">(.*?)</span""", self.page)
        self.number_results = len(elements)

        for element in elements:
            self.ids.append(element[0])
            self.titles.append(element[1])
