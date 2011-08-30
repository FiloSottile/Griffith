# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2011 Vasco Nunes, Piotr Ożarowski
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
plugin_version      = "0.4"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   = 'iso-8859-1'
        self.movie_id = id
        self.url      = "http://www.cinemovies.fr/fiche_film.php?IDfilm=" + str(self.movie_id)

    def initialize(self):
        self.page_cast = self.open_page(self.parent_window, url = 'http://www.cinemovies.fr/fiche_cast.php?IDfilm='+ str(self.movie_id))

    def get_image(self):
        self.image_url = gutils.trim(self.page, '<link rel="image_src" href="', '">')

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, 'Titre original :', '</tr>')

    def get_title(self):
        self.title = gutils.trim(self.page, '<h1 class="h1artist" property="v:name">', '</h1>')

    def get_director(self):
        self.director = gutils.clean(gutils.trim(self.page_cast, u'Réalisé par</h2> :', '<div id="cast_film">'))
        self.director = re.sub('[\n|\t]+', ', ', self.director)

    def get_plot(self):
        self.plot = gutils.trim(gutils.after(self.page, '>L\'histoire<'), '<div id="story_fiche" property="v:summary">', '</div>')

    def get_year(self):
        self.year = gutils.trim(self.page, 'Date(s) de Sortie(s)', '</a>')
        if len(self.year) > 4:
            self.year = self.year[len(self.year) - 4:len(self.year)]

    def get_runtime(self):
        self.runtime = gutils.clean(gutils.trim(self.page, u'>Durée :', '</tr>'))
        if self.runtime:
           if self.runtime.find('h') > 0:
              self.runtime = str (int(gutils.before(self.runtime,'h'))*60 + int(gutils.after(self.runtime,'h')))
           else:
              self.runtime = gutils.before(self.runtime,' mn')

    def get_genre(self):
        self.genre = gutils.trim(self.page, 'Genre :', '</tr>')
        self.genre = re.sub('[,][^,]*$', '', self.genre)
        self.genre = self.genre.replace(',', ', ')

    def get_cast(self):
        self.cast = gutils.trim(self.page_cast, u'Comédiens</h2> :', '<div id="cast_film">')
        self.cast = self.cast.replace('\n', '')
        self.cast = self.cast.replace('</tr>', '\n')
        self.cast = re.sub('</a></h5>', _(' as '), self.cast)
        self.cast = gutils.clean(self.cast)
        self.cast = re.sub(_(' as ') + '[ \t]*(\n|$)', '\n', self.cast)
        self.cast = re.sub('[ \t]*\n[ \t]+', '\n', self.cast)

    def get_classification(self):
        # not available on this site
        self.classification = ''

    def get_studio(self):
        self.studio = string.strip(gutils.trim(self.page, 'Distributeur :', '</tr>'))

    def get_o_site(self):
        self.o_site = gutils.after(gutils.after(gutils.trim(self.page, '>Site(s) Officiel(s)<', '</a'), '<a '), '>')

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = 'http://www.cinemovies.fr/fiche_multimedia.php?IDfilm=' + str(self.movie_id)

    def get_country(self):
        self.country = gutils.trim(self.page, 'Pays :', '</tr>')

    def get_rating(self):
        # site's rating, not users'
        self.rating = gutils.clean(gutils.trim(self.page, '<div class=number3>', '</div>'))

    def get_screenplay(self):
        self.screenplay = gutils.clean(gutils.trim(self.page_cast, u'Scénario de</h2> :', '<div id="cast_film">'))
        self.screenplay = re.sub('[\n|\t]+', ', ', self.screenplay)


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

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Rocky Balboa' : [ 2, 2 ],
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
        '6065' : { 
            'title'               : 'Rocky Balboa',
            'o_title'             : 'Rocky VI',
            'director'            : 'Sylvester Stallone',
            'plot'                : True,
            'cast'                : 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie\n\
Antonio Tarver' + _(' as ') + 'Mason "The Line"Dixon\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Milo Ventimiglia' + _(' as ') + 'Rocky Jr.\n\
Tony Burton' + _(' as ') + 'Duke\n\
A.J. Benza' + _(' as ') + 'L.C.\n\
James Francis Kelly III' + _(' as ') + 'Steps\n\
Talia Shire' + _(' as ') + 'Adrian\n\
Lou DiBella' + _(' as ') + 'Lui-même\n\
Mike Tyson' + _(' as ') + 'Lui-même\n\
Henry G. Sanders' + _(' as ') + 'Martin\n\
Pedro Lovell' + _(' as ') + 'Spider Rico\n\
Angela Boyd' + _(' as ') + 'Angie\n\
Lahmard J. Tate' + _(' as ') + 'X-Cell',
            'country'             : 'USA',
            'genre'               : 'Drame',
            'classification'      : False,
            'studio'              : 'Twentieth Century Fox France',
            'o_site'              : 'http://www.sonypictures.com/movies/rocky/',
            'site'                : 'http://www.cinemovies.fr/fiche_film.php?IDfilm=6065',
            'trailer'             : 'http://www.cinemovies.fr/fiche_multimedia.php?IDfilm=6065',
            'year'                : 2007,
            'notes'               : False,
            'runtime'             : 105,
            'image'               : True,
            'rating'              : 7,
            'cameraman'           : False,
            'screenplay'          : 'Sylvester Stallone',
            'barcode'             : False
        },
        '18158' : { 
            'title'               : 'Miss Mars',
            'o_title'             : 'Miss March',
            'director'            : 'Zach Cregger, Trevor Moore',
            'plot'                : True,
            'cast'                : 'Zach Cregger' + _(' as ') + 'Eugene Bell\n\
Trevor Moore' + _(' as ') + 'Tucker Cleigh\n\
Raquel Alessi' + _(' as ') + 'Cindi Whitehall\n\
Molly Stanton' + _(' as ') + 'Candace\n\
Craig Robinson' + _(' as ') + 'Horsedick.MPEG\n\
Hugh M. Hefner' + _(' as ') + u'Lui même\n\
Carla Jimenez' + _(' as ') + u'Juanita / Infirmière\n\
Cedric Yarbrough' + _(' as ') + 'Docteur\n\
Geoff Meed' + _(' as ') + 'Rick / Pompier\n\
Slade Pearce' + _(' as ') + 'Eugene jeune\n\
Remy Thorne' + _(' as ') + 'Tucker jeune\n\
Tanjareen Martin' + _(' as ') + 'Crystal\n\
Eve Mauro' + _(' as ') + 'Vonka\n\
Alexis Raben' + _(' as ') + 'Katja\n\
Windell Middlebrooks' + _(' as ') + 'Videur\n\
Lindsay Schoneweis' + _(' as ') + 'Sheila\n\
David Wells' + _(' as ') + 'Principal\n\
Britten Kelley' + _(' as ') + 'Chevonne\n\
Barry Sigismondi' + _(' as ') + 'Mr. Whitehall\n\
Alex Donnelley' + _(' as ') + 'Mrs. Whitehall\n\
Josh Fadem' + _(' as ') + 'Flava Flav Kid\n\
Paul Rogan' + _(' as ') + 'Mr. Biederman\n\
Kate Luyben' + _(' as ') + 'Mrs. Biederman\n\
Seth Morris' + _(' as ') + 'Boss\n\
Michael Busch' + _(' as ') + u'Employé\n\
Ryan Kitley' + _(' as ') + 'Serveur\n\
Anthony Jeselnik' + _(' as ') + 'Directeur\n\
Niki J. Crawford' + _(' as ') + 'Janine\n\
Bonita Friedericy' + _(' as ') + u'Serveuse du dîner\n\
Carrie Keagan' + _(' as ') + u'Elle même\n\
Shark Firestone' + _(' as ') + u'Lui même',
            'country'             : 'USA',
            'genre'               : u'Comédie',
            'classification'      : False,
            'studio'              : 'Twentieth Century Fox France',
            'o_site'              : 'http://www.missmars-lefilm.com',
            'site'                : 'http://www.cinemovies.fr/fiche_film.php?IDfilm=18158',
            'trailer'             : 'http://www.cinemovies.fr/fiche_multimedia.php?IDfilm=18158',
            'year'                : 2009,
            'notes'               : False,
            'runtime'             : 90,
            'image'               : True,
            'rating'              : 2,
            'cameraman'           : False,
            'screenplay'          : 'Zach Cregger, Trevor Moore',
            'barcode'             : False
        },
    }
