# -*- coding: UTF-8 -*-

__revision__ = '$Id: PluginMovieIMDB.py 176 2006-02-01 12:07:26Z iznogoud $'

# Copyright (c) 2005-2009 Vasco Nunes, Piotr Ozarowski
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, orprint
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
import string, re

plugin_name         = "Allocine"
plugin_description  = "Internet Movie Database"
plugin_url          = "www.allocine.fr"
plugin_language     = _("French")
plugin_author       = "Pierre-Luc Levy"
plugin_author_email = ""
plugin_version      = "0.7"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.movie_id = id
        self.url      = "http://www.allocine.fr/film/fichefilm_gen_cfilm=%s.html" % str(self.movie_id)
        self.encode   = 'iso-8859-1'

    def initialize(self):
        self.page_cast = self.open_page(self.parent_window, url = "http://www.allocine.fr/film/casting_gen_cfilm=%s.html" % str(self.movie_id))

    def get_image(self):
        urls = re.split('<img[ \t]+src=[\'"]', gutils.trim(self.page, '</h1>', '</h2>'))
        for url in urls[1:]:
            url = gutils.before(url, '"')
            if string.find(url, '.jpg') >= 0:
                self.image_url = url
                break

    def get_o_title(self):
        self.o_title = ""
        self.o_title = gutils.trim(self.page,"Titre original : <i>","</i>")
        if (self.o_title==''):
            self.o_title = string.replace(gutils.trim(self.page, '<title>', '</title>'), u' - AlloCiné', '')

    def get_title(self):
        self.title = string.replace(gutils.trim(self.page, '<title>', '</title>'), u' - AlloCiné', '')

    def get_director(self):
        self.director = gutils.trim(self.page, u'Réalisé par ', '</a></h3>')

    def get_plot(self):
        self.plot = gutils.trim(self.page, 'Synopsis', '</h4></div>')

    def get_year(self):
        self.year = gutils.trim(self.page, u'Année de production : ', '<')

    def get_runtime(self):
        self.runtime = ""
        self.runtime = gutils.trim(self.page, u'>Durée : ', 'min')
        if self.runtime:
            self.runtime = str (int(gutils.before(self.runtime,"h"))*60 + int(gutils.after(self.runtime,"h")))

    def get_genre(self):
        self.genre = gutils.trim(self.page, 'Genre : ', '<h3')
        self.genre = gutils.strip_tags(self.genre)

    def get_cast(self):
        self.cast = ""
        casts = gutils.trim(self.page_cast, 'Acteurs', '</table>')
        parts = string.split(casts, '<td ')
        for index in range(1, len(parts) - 1, 3):
            character = gutils.after(parts[index + 1], '>')
            actor = gutils.after(parts[index + 2], '>')
            self.cast = self.cast + gutils.clean(actor) + _(' as ') + gutils.clean(character) + '\n'

    def get_classification(self):
        self.classification = ""

    def get_studio(self):
        self.studio = ""

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = "http://www.allocine.fr/film/fichefilm_gen_cfilm=%s.html" % self.movie_id

    def get_trailer(self):
        self.trailer = "http://www.allocine.fr/film/video_gen_cfilm=%s.html" % self.movie_id

    def get_country(self):
        self.country = gutils.trim(self.page, '>Film ', '.&nbsp;<')

    def get_rating(self):
        self.rating = gutils.trim(self.page, 'Spectateurs</a>', '</tr>')
        self.rating = gutils.trim(self.rating, 'etoile_', '"')
        if self.rating:
            self.rating = str(round(float(int(self.rating)*2.25)))

    def get_screenplay(self):
        self.screenplay = gutils.clean(gutils.trim(self.page_cast, u'Scénariste', '</tr>'))

    def get_cameraman(self):
        self.cameraman = gutils.clean(gutils.trim(self.page_cast, 'Directeur de la photographie', '</tr>'))

class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search   = "http://www.allocine.fr/recherche/?rub=1&motcle="
        self.translated_url_search = "http://www.allocine.fr/recherche/?rub=1&motcle="
        self.encode                = 'iso-8859-1'

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        self.sub_search()
        return self.page

    def sub_search(self):
        self.page = gutils.trim(self.page, 'Recherche : <b>', '</table><script');

    def get_searches(self):
        elements = string.split(self.page, '<h4><a href="/film/fichefilm_gen_cfilm=')
        if (elements[0]<>''):
            for index in range(1, len(elements), 1):
                element = elements[index]
                self.ids.append(gutils.before(element, '.'))
                title = gutils.strip_tags(gutils.convert_entities(gutils.trim(element, '>', '</a>')))
                year = gutils.clean(gutils.trim(element, '</h4>', '</h4>'))
                if year:
                    self.titles.append(title + ' (' + year + ')')
                else:
                    self.titles.append(title)

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Le Prix à payer' : [ 4, 4 ],
    }

class PluginTest:
    #
    # Configuration for automated tests:
    # dict { movie_id -> dict { arribute -> value } }
    #
    # value: * True/False if attribute only should be tested for any value
    #        * or the expected value
    #
    test_configuration = {
        '110585' : { 
            'title'               : u'Le Prix à payer',
            'o_title'             : u'Le Prix à payer',
            'director'            : u'Alexandra Leclère',
            'plot'                : True,
            'cast'                : u'Christian Clavier' + _(' as ') + 'Jean-Pierre Ménard\n\
Nathalie Baye' + _(' as ') + 'Odile Ménard\n\
Gérard Lanvin' + _(' as ') + 'Richard\n\
Géraldine Pailhas' + _(' as ') + 'Caroline\n\
Patrick Chesnais' + _(' as ') + 'Grégoire l\'amant\n\
Anaïs Demoustier' + _(' as ') + 'Justine\n\
Maud Buquet' + _(' as ') + 'la prostituée\n\
Francis Leplay' + _(' as ') + 'l\'agent immobilier',
            'country'             : u'français',
            'genre'               : u'Comédie',
            'classification'      : False,
            'studio'              : False,
            'o_site'              : False,
            'site'                : 'http://www.allocine.fr/film/fichefilm_gen_cfilm=110585.html',
            'trailer'             : 'http://www.allocine.fr/film/video_gen_cfilm=110585.html',
            'year'                : 2007,
            'notes'               : False,
            'runtime'             : 95,
            'image'               : True,
            'rating'              : 5,
            'cameraman'           : u'Jean-François Robin',
            'screenplay'          : u'Alexandra Leclère',
            'barcode'             : False
        },
    }
