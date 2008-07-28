# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007 Michael Jahn
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
import gutils
import movie
import string

plugin_name        = 'FilmDb.de'
plugin_description    = 'FILMDB.DE'
plugin_url        = 'www.filmdb.de'
plugin_language        = _('German')
plugin_author        = 'Michael Jahn'
plugin_author_email    = '<mikej06@hotmail.com>'
plugin_version        = '1.0'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode='iso-8859-1'
        self.movie_id = id
        self.url = "http://www.filmdb.de/filmanzeige.php?alle=1&filmid=" + self.movie_id

    def initialize(self):
        self.tmp_page = gutils.trim(self.page, "<h1>Filmdatenbank - ", "Kommentare</a>")
    
    def get_image(self):
        self.image_url = gutils.trim(self.tmp_page, '<td background="', '"');

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<h1>Filmdatenbank - ', '</h1>')

    def get_title(self):
        self.title = gutils.trim(self.page, '<h1>Filmdatenbank - ', '</h1>')

    def get_director(self):
        self.director = gutils.after(gutils.trim(self.tmp_page, 'regisseursuche.php', '</a>'), '>')

    def get_plot(self):
        self.plot = gutils.trim(self.tmp_page, '>Inhalt</strong>', '<td width="150" valign="top">')
        self.plot = self.plot.replace('\t', '')
        self.plot = self.plot.replace('\n', '')
        self.plot = self.plot.replace('„', '"')
        self.plot = self.plot.replace('“', '"')

    def get_year(self):
        elements = string.split(self.tmp_page, 'landjahrsuche.php')
        self.year = gutils.trim(elements[2], '>', '</a>') + '\n'

    def get_runtime(self):
        self.runtime = ""
        tmp = gutils.trim(self.tmp_page, '</a>  – ', ' Stunden')
        if tmp <> '':
            elements = string.split(tmp, ':')
            try:
                hours = int(elements[0])
                mins = int(elements[1])
                self.runtime = str(hours * 60 + mins)
            except:
                self.runtime = ""

    def get_genre(self):
        self.genre = gutils.after(gutils.trim(self.tmp_page, 'genresuche.php', '</a>'), '>')

    def get_cast(self):
        self.cast = ""
        elements = string.split(self.tmp_page, 'schauspielersuche.php')
        elements[0] = ''
        for element in elements:
            if element <> '':
                self.cast = self.cast + gutils.trim(element, '>', '</a>') + '\n'

    def get_classification(self):
        self.classification = ""

    def get_studio(self):
        self.studio = ""

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = "http://www.filmdb.de/filmanzeige.php?filmid=" + self.movie_id

    def get_trailer(self):
        self.trailer = ""

    def get_country(self):
        elements = string.split(self.tmp_page, 'landjahrsuche.php')
        self.country = gutils.trim(elements[1], '>', '</a>') + '\n'

    def get_rating(self):
        self.rating = gutils.trim(self.tmp_page, 'Unsere User haben diesen Film mit ', ' bewertet.')
        self.rating = self.rating.replace('%', '')
        self.rating = gutils.strip_tags(self.rating)
        elements = self.rating.split('.')
        try:
            tmprating = int(elements[0])
            self.rating = str(tmprating / 10)
        except:
            self.rating = '0'

    def get_notes(self):
        self.notes = ""

class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search   = "http://www.filmdb.de/globalsuche.php?name="
        self.translated_url_search = "http://www.filmdb.de/globalsuche.php?name="
        self.encode='iso-8859-1'

    def search(self,parent_window):
        self.open_search(parent_window)
        return gutils.trim(self.page, "<span class=font_normal>", "<table width=590")

    def get_searches(self):
        elements = string.split(self.page, "<!--")
        elements[0] = ''
        for element in elements:
            if element <> '':
                self.ids.append(gutils.trim(element, "filmid=", ">"))
                self.titles.append(gutils.trim(
                    gutils.after(element, "filmid="), ">", "<") + " - " +
                    gutils.trim(gutils.after(element, "</a>"), "<td>", "</td>") + " - " +
                    gutils.trim(gutils.after(gutils.after(element, "<td>"), "<td>"), "<td>", "</td>"))
