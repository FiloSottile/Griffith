# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2009 Vasco Nunes, Piotr Ożarowski
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
import movie,string,re

plugin_name         = "Cinemovies"
plugin_description  = "Cinemovies"
plugin_url          = "www.cinemovies.fr"
plugin_language     = _("French")
plugin_author       = "Vasco Nunes"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version      = "0.3"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   = 'iso-8859-1'
        self.movie_id = id
        self.url      = "http://www.cinemovies.fr/fiche_film.php?IDfilm=" + str(self.movie_id)

    def initialize(self):
        self.page_cast = self.open_page(self.parent_window, url = 'http://www.cinemovies.fr/fiche_cast.php?IDfilm='+ str(self.movie_id))

    def get_image(self):
        self.image_url = 'http://www.cinemovies.fr/images/data/affiches/Paff'
        self.image_url = self.image_url + string.strip(gutils.trim(self.page, 'data/affiches/Paff', '.jpg')) + '.jpg'

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, 'Titre original :', '</tr>')

    def get_title(self):
        self.title = gutils.trim(self.page, '<h1 class="h1artist">', '</h1>')

    def get_director(self):
        self.director = string.strip(gutils.trim(self.page, 'par :</b></td>', '</a>'))

    def get_plot(self):
        self.plot = gutils.trim(gutils.after(self.page, '>L\'histoire<'), '<div id="story_fiche">', '</div>')

    def get_year(self):
        self.year = gutils.trim(self.page, 'Date(s) de Sortie(s)', '</a>')
        if len(self.year) > 4:
            self.year = self.year[len(self.year) - 4:len(self.year)]

    def get_runtime(self):
        self.runtime = gutils.clean(gutils.trim(self.page, u'>Durée :', '</tr>'))
        if self.runtime:
            self.runtime = str (int(gutils.before(self.runtime,"h"))*60 + int(gutils.after(self.runtime,"h")))

    def get_genre(self):
        self.genre = gutils.trim(self.page, 'Genre :', '</tr>')

    def get_cast(self):
        self.cast = gutils.trim(self.page_cast, 'diens</b> :', '</table>')
        self.cast = self.cast.replace('\n', '')
        self.cast = self.cast.replace('</tr>', '\n')
        self.cast = gutils.clean(self.cast)
        self.cast = re.sub('\n[ \t]+', '\n', self.cast)
        self.cast = re.sub('[.]+', _(' as '), self.cast)
        self.cast = re.sub(_(' as ') + '(\n|$)', '\n', self.cast)

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = string.strip(gutils.trim(self.page, 'Distributeur :', '</tr>'))

    def get_o_site(self):
        self.o_site = gutils.after(gutils.after(gutils.trim(self.page, '>Site(s) Officiel(s):<', '</a'), '<a '), '>')

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = gutils.trim(self.page, 'Pays :', '</tr>')

    def get_rating(self):
        self.rating = gutils.clean(gutils.trim(self.page, '<DIV id=scoree>', '</DIV>'))


class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.encode                = 'iso-8859-1'
        self.original_url_search   = "http://www.cinemovies.fr/resultat_recherche.php?typsearch=11&cherche="
        self.translated_url_search = "http://www.cinemovies.fr/resultat_recherche.php?typsearch=11&cherche="

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        self.sub_search()
        return self.page

    def sub_search(self):
        self.page = gutils.trim(self.page, '<div class=searchban>Les film', '<div class=spaceblank>')

    def get_searches(self):
        elements = string.split(self.page, '<tr')
        self.number_results = elements[-1]

        if (elements[0]<>''):
            for element in elements:
                self.ids.append(gutils.trim(element, 'IDfilm=', '"'))
                title = gutils.convert_entities(gutils.strip_tags(gutils.after(gutils.trim(element, 'IDfilm=', '</a>'), '>')))
                year = gutils.after(gutils.trim(element, '<td valign="bottom"', '</td>'), '>')
                self.titles.append(title + ' (' + year + ')')
        else:
            self.number_results = 0
