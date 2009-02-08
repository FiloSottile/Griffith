# -*- coding: iso-8859-15 -*-

__revision__ = '$Id: PluginMovieFilmAffinity.py 389 2006-07-29 18:43:35Z piotrek $'

# Copyright (c) 2006 Pedro D. Sánchez
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

import gutils
import movie
import string

plugin_name        = 'FilmAffinity'
plugin_description    = 'Base de Datos de Peliculas'
plugin_url        = 'www.filmaffinity.com'
plugin_language        = _('Spanish')
plugin_author        = 'Pedro D. Sánchez'
plugin_author_email    = '<pedrodav@gmail.com>'
plugin_version        = '0.2'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode='iso-8859-15'
        self.movie_id = id
        self.url = "http://www.filmaffinity.com/es/film%s.html" % str(self.movie_id)

    def get_image(self):
        tmp = string.find(self.page, '<img src="http://www.filmaffinity.com/imgs/movies/')
        if tmp == -1:
            self.image_url = ''
        else:
            self.image_url = gutils.trim(self.page[tmp-1:], 'src="', '"')

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<b>TITULO ORIGINAL</b></td>', '</b></td>')
        self.o_title = gutils.after(self.o_title, '<b>')

    def get_title(self):
        self.title = gutils.trim(self.page, '<img src="http://www.filmaffinity.com/images/movie.gif" border="0"> ', '</span>')

    def get_director(self):
        self.director = gutils.trim(self.page,'<b>DIRECTOR</b></td>', '</td>')

    def get_plot(self):
        self.plot = gutils.trim(self.page, '<b>GÉNERO Y CRÍTICA</b>', '<br />')
        if self.plot == '':
            self.plot = gutils.trim(self.page, '<b>G&Eacute;NERO Y CR&Iacute;TICA</b>', '<br />')
        self.plot = gutils.after(self.plot, '<td valign="top">')
        self.plot = gutils.after(self.plot, '/')
        self.plot = string.replace(self.plot, ' SINOPSIS: ', '')
        self.plot = string.replace(self.plot, ' SINOPSIS:', '')
        self.plot = string.replace(self.plot, 'SINOPSIS: ', '')
        self.plot = string.replace(self.plot, 'SINOPSIS:', '')
        self.plot = string.replace(self.plot, ' (FILMAFFINITY)', '')
        self.plot = string.replace(self.plot, '(FILMAFFINITY)', '')

    def get_year(self):
        self.year = gutils.trim(self.page, '<b>AÑO</b></td>', '</td>')
        self.year = gutils.after(self.year, '<td >')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, '<b>DURACIÓN</b></td>', ' min.</td>')
        if self.runtime == '':
            self.runtime = gutils.trim(self.page, '<b>DURACI&Oacute;N</b></td>', ' min.</td>')
        self.runtime = gutils.after(self.runtime[-10:], '<td>')

    def get_genre(self):
        self.genre = gutils.trim(self.page, '<b>GÉNERO Y CRÍTICA</b>', '<br />')
        if self.genre == '':
            self.genre = gutils.trim(self.page, '<b>G&Eacute;NERO Y CR&Iacute;TICA</b>', '<br />')
        self.genre = gutils.trim(self.genre, '<td valign="top">', '/')
        self.genre = string.replace(self.genre, '.', " /")

    def get_cast(self):
        self.cast = ''
        self.cast = gutils.trim(self.page, '<b>REPARTO</b></td>', '</td>')
        self.cast = string.replace(self.cast, '</a>,', '\n')
        self.cast = string.strip(gutils.strip_tags(self.cast))
        self.cast = string.replace(self.cast, '  ', '')

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = gutils.trim(self.page, '<b>PRODUCTORA</b></td>', '</td>')
        self.studio = gutils.after(self.studio, '<td  >')

    def get_o_site(self):
        self.o_site = gutils.trim(self.page, '<b>WEB OFICIAL</b></td>', '</a>')
        self.o_site = gutils.after(self.o_site, '">')

    def get_site(self):
        self.site = "http://www.filmaffinity.com/es/film%s.html" % str(self.movie_id)

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = gutils.trim(self.page, '<b>PAÍS</b></td>', '</td>')
        self.country = gutils.trim(self.country, 'alt="', '"')

    def get_rating(self):
        self.rating = gutils.trim(self.page, '<tr><td align="center" style="color:#990000; font-size:22px; font-weight: bold;">', '</td></tr>')
        if self.rating:
            self.rating = str(float(gutils.clean(string.replace(self.rating, ',', '.'))))

class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search    = 'http://www.filmaffinity.com/es/search.php?stype=title&stext='
        self.translated_url_search    = 'http://www.filmaffinity.com/es/search.php?stype=title&stext='
        self.encode = 'iso-8859-15'

    def search(self,parent_window):
        self.open_search(parent_window)
        auxPage = self.page
        self.sub_search()
        if self.page <> '':
            return self.page
        auxPage = gutils.trim(auxPage, '<b>TU CRÍTICA</b></div>', '</a>')
        self.page = gutils.trim(auxPage, 'movie_id=', '">')
        return self.page

    def sub_search(self):
        self.page = gutils.trim(self.page, 'Resultados por título</span>', '<br>')
        #self.page = gutils.after(self.page, '</td></tr><tr><td><b>')
        #self.page = self.page.decode('iso-8859-15')

    def get_searches(self):
        if len(self.page) < 20:    # immidietly redirection to movie page
            self.number_results = 1
            self.ids.append(self.page)
            self.titles.append(self.url)
        else:            # multiple matches
            elements = string.split(self.page, '</a></b>')

            if (elements[0]<>''):
                for element in elements[:-1]:
                    self.ids.append(gutils.trim(element, '<b><a href="/es/film','.html'))
                    title = gutils.after(element, '<b><a href="/es/film')
                    self.titles.append(gutils.strip_tags(gutils.convert_entities(gutils.after(title, '>'))))
