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

import gutils, movie, string, re

plugin_name         = "Cinematografo"
plugin_description  = "Rivista del Cinematografo dal 1928"
plugin_url          = "www.cinematografo.it"
plugin_language     = _("Italian")
plugin_author       = "Vasco Nunes, Piotr Ożarowski"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version      = "1.3"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   = 'iso-8859-1'
        self.movie_id = id
        self.url      = "http://www.cinematografo.it/bancadati/consultazione/schedafilm.jsp?completa=si&codice=%s" % str(self.movie_id)

    def get_image(self):
        # Find the film's poster image
        tmp_poster = gutils.regextrim(self.page, "../images_locandine/%s/" % self.movie_id, ".(JPG|jpg)\"")
        if tmp_poster != "":
            self.image_url = "http://www.cinematografo.it/bancadati/images_locandine/%s/%s.jpg" % (self.movie_id, tmp_poster)
        else:
            self.image_url=""

    def get_o_title(self):
        # Find the film's original title
        self.o_title = gutils.trim(self.page, ">Titolo Originale</font>", "</tr>")
        self.o_title = string.capwords(self.o_title)
        # if nothing found, use the title
        if self.o_title == '':
            self.o_title = gutils.trim(self.page, "<!--TITOLO-->", "<!--FINE TITOLO-->")
            self.o_title = gutils.trim(self.o_title, "<b>", "</b>")

    def get_title(self):
        # Find the film's local title.
        # Probably the original title translation
        self.title = gutils.trim(self.page, "<!--TITOLO-->", "<!--FINE TITOLO-->")
        self.title = gutils.trim(self.title, "<b>", "</b>")

    def get_director(self):
        # Find the film's director
        self.director = gutils.trim(self.page, ">Regia", "Attori<")
        self.director = self.director.replace("&nbsp;&nbsp;", "&nbsp;")
        self.director = gutils.strip_tags(self.director)
        self.director = string.strip(self.director)

    def get_plot(self):
        # Find the film's plot
        self.plot = gutils.trim(self.page, "\"fontYellowB\">Trama</font>", "\n")

    def get_year(self):
        # Find the film's year
        self.year = gutils.trim(self.page, ">Anno</font>", "</tr>")
        self.year = gutils.digits_only(gutils.clean(self.year))

    def get_runtime(self):
        # Find the film's running time
        self.runtime = gutils.trim(self.page, ">Durata</font>", "</tr>")
        self.runtime = gutils.digits_only(gutils.clean(self.runtime))

    def get_genre(self):
        # Find the film's genre
        self.genre = gutils.trim(self.page, ">Genere</font>", "</tr>").lower()

    def get_cast(self):
        # Find the actors. Try to make it comma separated.
        self.cast = gutils.regextrim(self.page, ">Attori</font>", '(<font class="fontViolaB">|\n)')
        self.cast = string.replace(self.cast, "target='_self'>", "\n>")
        self.cast = string.replace(self.cast, "<a>",_(" as ").encode('utf8'))
        self.cast = string.replace(self.cast, "</tr><tr>", '\n')
        self.cast = string.replace(self.cast, "...vedi il resto del cast", '')
        self.cast = gutils.clean(self.cast)
        self.cast = string.replace(self.cast, "&nbsp;&nbsp;", ' ')
        self.cast = re.sub('[ ]+', ' ', self.cast)
        self.cast = re.sub('\n[ ]+', '\n', self.cast)

    def get_classification(self):
        # Find the film's classification
        self.classification = ''

    def get_studio(self):
        # Find the studio
        self.studio = string.capwords(gutils.clean(gutils.trim(self.page, ">Distribuzione</font>", "</tr>")))

    def get_o_site(self):
        # Find the film's oficial site
        self.o_site = ''

    def get_site(self):
        # Find the film's imdb details page
        self.site = self.url

    def get_trailer(self):
        # Find the film's trailer page or location
        self.trailer = ""

    def get_country(self):
        # Find the film's country
        self.country = gutils.trim(self.page, ">Origine</font>", "</tr>")

    def get_rating(self):
        # Find the film's rating. From 0 to 10.
        # Convert if needed when assigning.
        self.rating = 0

class SearchPlugin(movie.SearchMovie):
    # A movie search object
    def __init__(self):
        self.encode                = 'iso-8859-1'
        self.original_url_search   = 'http://www.cinematografo.it/bancadati/consultazione/trovatitoli.jsp?startrighe=0&endrighe=100&tipo=CONTIENEPAROLE&word='
        self.translated_url_search = self.original_url_search

    def search(self, parent_window):
        # Perform the web search
        self.open_search(parent_window)
        self.sub_search()
        return self.page

    def sub_search(self):
        # Isolating just a portion (with the data we want) of the results
        self.page = gutils.trim(self.page, '<td valign="top" width="73%" bgcolor="#4d4d4d">', '</td>')

    def get_searches(self):
        # Try to find both id and film title for each search result
        elements = string.split(self.page, "<li>")
        self.number_results = elements[-1]

        if (elements[0] != ''):
            for element in elements:
                id = gutils.trim(element, "?codice=", "\">")
                if id <> '':
                    self.ids.append(id)
                    self.titles.append(gutils.convert_entities(gutils.trim(element, "<b>", "</b>")))
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
        'Rocky'      : [ 12, 12 ],
        'però'       : [  6,  6 ],
        'il ritorno' : [ 97, 97 ]
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
        '3996' : { 
            'title'             : 'Amor non ho, però... però...',
            'o_title'           : 'Amor non ho, però... però...',
            'director'          : 'Giorgio Bianchi',
            'plot'              : True,
            'cast'              : 'Renato Rascel' + _(' as ') + 'Teodoro\n\
Gina Lollobrigida' + _(' as ') + 'Gina\n\
Luigi Pavese' + _(' as ') + 'Antonio Scutipizzo\n\
Aroldo Tieri' + _(' as ') + 'Giuliano\n\
Carlo Ninchi' + _(' as ') + 'Maurizio\n\
Kiki Urbani' + _(' as ') + 'Kiki, la ballerina\n\
Adriana Danieli' + _(' as ') + 'Olga\n\
Strelsa Brown' + _(' as ') + 'Mabel\n\
Virgilio Riento' + _(' as ') + 'Il contadino\n\
Gabriele Tinti' + _(' as ') + '(Gastone Tinti) Un componente dell\'orchestra\n\
Guglielmo Barnabò' + _(' as ') + '\n\
Giuseppe De Martino' + _(' as ') + '\n\
Raimondo Vianello' + _(' as ') + '(Riccardo Vianello) \n\
Maria Carla Vittone' + _(' as ') + '\n\
Marco Tulli' + _(' as ') + '\n\
Giuseppe Ricagno' + _(' as ') + '\n\
Luciano Rebeggiani' + _(' as ') + '\n\
Kurt Lary' + _(' as ') + '\n\
Giovanni Lesa' + _(' as ') + '\n\
Riccardo Ferri' + _(' as ') + '\n\
Pia De Doses' + _(' as ') + '\n\
Guido Barbarisi' + _(' as ') + '\n\
Galeazzo Benti as',
            'country'           : 'ITALIA',
            'genre'             : 'commedia',
            'classification'    : False,
            'studio'            : 'Minervafilm - Mfd Home Video',
            'o_site'            : False,
            'site'              : 'http://www.cinematografo.it/bancadati/consultazione/schedafilm.jsp?completa=si&codice=3996',
            'trailer'           : False,
            'year'              : 1951,
            'notes'             : False,
            'runtime'           : 90,
            'image'             : False,
            'rating'            : False
        },
    }
