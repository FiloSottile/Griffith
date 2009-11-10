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
        '47931' : { 
            'title'             : 'Rocky Balboa',
            'o_title'           : 'Rocky Balboa',
            'director'          : 'Sylvester Stallone',
            'plot'              : True,
            'cast'              : 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Pauliev\n\
Antonio Tarver' + _(' as ') + 'Mason \'The Line\' Dixon\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Milo Ventimiglia' + _(' as ') + 'Robert Jr.\n\
Tony Burton' + _(' as ') + 'Duke\n\
A.J. Benza' + _(' as ') + 'L.C.\n\
James Francis Kelly III' + _(' as ') + 'Steps\n\
Talia Shire' + _(' as ') + 'Adrian (imagens de arquivo)\n\
Lou DiBella' + _(' as ') + 'Lou DiBella\n\
Mike Tyson (1)' + _(' as ') + 'Mike Tyson\n\
Henry G. Sanders' + _(' as ') + 'Martin\n\
Pedro Lovell' + _(' as ') + 'Spider Rico\n\
Ana Gerena' + _(' as ') + 'Isabel\n\
Angela Boyd' + _(' as ') + 'Angie\n\
Louis Giansante' + _(' as ') + 'Bandido do bar\n\
Maureen Schilling' + _(' as ') + 'Bartender do Lucky\n\
Lahmard Tate¹' + _(' as ') + 'X-Cell\n\
Woodrow W. Paige¹' + _(' as ') + 'Comentarista da ESPN\n\
Skip Bayless' + _(' as ') + 'Comentarista da ESPN\n\
Jay Crawford' + _(' as ') + 'Comentarista da ESPN\n\
Brian Kenny' + _(' as ') + 'Apresentador da ESPN\n\
Dana Jacobson' + _(' as ') + 'Apresentador da ESPN\n\
Chuck Johnson¹' + _(' as ') + 'Apresentador da ESPN\n\
James Binns' + _(' as ') + 'Comissário\n\
Johnnie Hobbs Jr.' + _(' as ') + 'Comissário\n\
Barney Fitzpatrick' + _(' as ') + 'Comissário\n\
Jim Lampley' + _(' as ') + 'Comentarista da HBO\n\
Larry Merchant' + _(' as ') + 'Comentarista da HBO\n\
Max Kellerman' + _(' as ') + 'Comentarista da HBO\n\
LeRoy Neiman' + _(' as ') + 'LeRoy Neiman\n\
Bert Randolph Sugar' + _(' as ') + 'Repórter da Ring Magazine\n\
Bernard Fernández' + _(' as ') + 'Articulista da Boxing Association of America\n\
Gunnar Peterson' + _(' as ') + 'Treinador de levantamento de peso\n\
Yahya' + _(' as ') + 'Oponente de Dixon\n\
Marc Ratner (1)' + _(' as ') + 'Oficial de luta\n\
Anthony Lato Jr.' + _(' as ') + 'Inspetor de Rocky\n\
Jack Lazzarado' + _(' as ') + 'Inspetor de Dixon\n\
Michael Buffer' + _(' as ') + 'Anunciador de luta\n\
Joe Cortez' + _(' as ') + 'Árbitro\n\
Carter Mitchell' + _(' as ') + 'Shamrock Foreman\n\
Vinod Kumar (1)' + _(' as ') + 'Ravi\n\
Fran Pultro' + _(' as ') + 'Pai no restaurante\n\
Frank Stallone Jr.¹' + _(' as ') + 'Cliente do restaurante\n\
Jody Giambelluca' + _(' as ') + 'Cliente do restaurante\n\
Tobias Segal' + _(' as ') + 'Amigo de Robert\n\
Tim Carr' + _(' as ') + 'Amigo de Robert\n\
Matt Frack' + _(' as ') + 'Amigo de Robert\n\
Paul Dion Monte' + _(' as ') + 'Amigo de Robert\n\
Kevin King Templeton' + _(' as ') + 'Amigo de Robert\n\
Robert Michael Kelly' + _(' as ') + 'Senhor Tomilson\n\
Rick Buchborn' + _(' as ') + 'Fã de Rocky\n\
Nick Baker' + _(' as ') + 'Bartender do pub irlandês\n\
Don Sherman' + _(' as ') + 'Andy\n\
Stu Nahan' + _(' as ') + 'Comentarista da luta pelo computador\n\
Gary Compton' + _(' as ') + 'Segurança\n\
Ricky Cavazos' + _(' as ') + 'Espectador da luta (não creditado)\n\
Dolph Lundgren' + _(' as ') + 'Capitão Ivan Drago (imagens de arquivo) (não creditado)\n\
Burgess Meredith' + _(' as ') + 'Mickey (imagens de arquivo) (não creditado)\n\
Mr. T' + _(' as ') + 'Clubber Lang (imagens de arquivo) (não creditado)\n\
Carl Weathers' + _(' as ') + 'Apollo Creed (imagens de arquivo) (não creditado)',
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
