# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2010 Michael Jahn
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
import re

plugin_name = "FilmeVonA-Z.de"
plugin_description = "FILMEvonA-Z.de"
plugin_url = "www.zweitausendeins.de"
plugin_language = _("German")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.4"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode = 'utf-8'
        self.movie_id = id
        self.url = 'http://www.zweitausendeins.de/filmlexikon/?sucheNach=titel&wert=' + str(self.movie_id)

    def initialize(self):
        url = 'http://www.zweitausendeins.de/getimage/?imageNo=0&movieNo=' + str(self.movie_id)
        self.imagelinks = self.open_page(self.parent_window, url=url)

    def get_image(self):
        if string.find(self.imagelinks, '|') > 0:
            self.image_url = gutils.before(self.imagelinks, '|')

    def get_o_title(self):
        self.o_title = gutils.clean(gutils.after(
            gutils.regextrim(self.page, 'class="text_ergebniss_faz_3"', '[ \t]+[(]Originaltitel[)]'), '</a>'))
        p1 = string.rfind(self.o_title, ',')
        if p1 > 0:
            self.o_title = self.o_title[p1 + 1:]
        self.o_title = string.capwords(self.o_title)
        if self.o_title == '':
            self.o_title = gutils.after(gutils.trim(self.page, 'class="text_ergebniss_faz_3"', '</a>'), '>')

    def get_title(self):
        self.title = gutils.after(gutils.trim(self.page, 'class="text_ergebniss_faz_3"', '</a>'), '>')

    def get_director(self):
        self.director = gutils.after(gutils.trim(self.page, '(Regie)', '</span>'), '>')
        self.director = re.sub(',[ ]*$', '', self.director)

    def get_plot(self):
        self.plot = gutils.after(gutils.trim(self.page, 'Inhalt des Films:', '</td>'), '</div>')

    def get_year(self):
        self.year = gutils.after(gutils.trim(self.page, 'sucheNach=produktionsjahr', '</a>'), '>')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, 'L&auml;nge: ', ' Minuten')

    def get_genre(self):
        elements = string.split(self.page, 'sucheNach=genre')
        if (elements[0]<>''):
            elements[0] = ''
            self.delimiter = ''
            self.genre = ''
            for element in elements:
                if (element <> ''):
                    self.genre += self.delimiter + gutils.trim(element, '>', '</a>')
                    self.delimiter = ", "

    def get_cast(self):
        self.cast = gutils.regextrim(self.page, '[(]Darsteller[)]', '(</td>|<br><span[^>]+>)')
        self.cast = gutils.clean(self.cast)
        self.cast = self.cast.replace(' als ', _(' as '))
        self.cast = re.sub('( \t|\t|\r|\n)', '', self.cast)
        self.cast = self.cast.replace(',', '\n')

    def get_classification(self):
        self.classification = gutils.regextrim(self.page, 'FSK:[ ]+', '[,;]')

    def get_studio(self):
        self.studio = gutils.after(gutils.trim(self.page, 'sucheNach=produktionsfirma', '</span>'), '>')
        self.studio = string.replace(self.studio, '/', ',')
        self.studio = re.sub(',[ ]*$', '', self.studio)

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = gutils.after(gutils.trim(self.page, 'sucheNach=produktionsland', '</span>'), '>')
        self.country = re.sub(',[ ]*$', '', self.country)
        self.country = string.replace(self.country, '/', ',')

    def get_rating(self):
        self.rating = 0

    def get_screenplay(self):
        self.screenplay = gutils.trim(self.page, '(Drehbuch)', '</span>')
        self.screenplay = re.sub(',[ ]*$', '', self.screenplay)

    def get_cameraman(self):
        self.cameraman = gutils.trim(self.page, '(Kamera)', '</span>')
        self.cameraman = re.sub(',[ ]*$', '', self.cameraman)

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.original_url_search = "http://www.zweitausendeins.de/filmlexikon/?sucheNach=Titel&wert="
        self.translated_url_search = "http://www.zweitausendeins.de/filmlexikon/?sucheNach=Titel&wert="
        self.encode = 'utf-8'

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        # used for looking for subpages
        tmp_page = gutils.trim(self.page, '<span class="trefferliste">', '</span>')
        elements = string.split(tmp_page, 'cp=')
        # first results
        tmp_page = gutils.after(gutils.trim(self.page, 'Alle Treffer aus der Kategorie', '<span class="trefferliste">'), "Titel:")
        # look for subpages
        for element in elements:
            element = gutils.before(element, '"')
            try:
                tmp_element = int(element)
            except:
                tmp_element = 1
            if tmp_element != 1:
                self.url = 'http://www.zweitausendeins.de/filmlexikon/?sucheNach=Titel&cp=' + str(tmp_element) + "&wert="
                if self.open_search(parent_window):
                    tmp_page2 = gutils.trim(self.page, 'Alle Treffer aus der Kategorie', '<span class="trefferliste">')
                    tmp_page = tmp_page + tmp_page2
        self.page = tmp_page

        return self.page

    def get_searches(self):
        elements = string.split(self.page, '<div class="text_ergebniss_faz_3"')
        i = 1
        while i < len(elements):
            element = elements[i]
            i = i + 1
            self.ids.append(gutils.trim(element, 'filmlexikon/?wert=', '&'))
            self.titles.append(string.strip(gutils.clean(
                        gutils.trim(element, '>', '</a>') + ' (' +
                        string.capwords(gutils.trim(element, '</a>', '(Originaltitel)')) + ', ' +
                        gutils.after(gutils.trim(element, 'sucheNach=produktionsland', '</a>'), '>') + ', ' +
                        gutils.after(gutils.trim(element, 'sucheNach=produktionsjahr', '</a>'), '>') +
                        ')')))

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Rocky'                : [ 15, 15 ],
        'Arahan'               : [ 1, 1 ],
        'Ein glückliches Jahr' : [ 0, 0 ]
    }

class PluginTest:
    #
    # Configuration for automated tests:
    # dict { movie_id -> dict { arribute -> value } }
    #
    # value: * True/False if attribute should only be tested for any value
    #        * or the expected value
    #
    test_configuration = {
        '528267' : { 
            'title'             : 'Rocky Balboa',
            'o_title'           : 'Rocky Balboa',
            'director'          : 'Sylvester Stallone',
            'plot'              : True,
            'cast'              : 'A.J. Benza' + _(' as ') + 'L.C.\n\
Milo Ventimiglia' + _(' as ') + 'Rocky jr.\n\
Antonio Tarver' + _(' as ') + 'Mason \'The Line\' Dixon\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie\n\
Tony Burton' + _(' as ') + 'Duke',
            'country'           : 'USA',
            'genre'             : 'Boxerfilm',
            'classification'    : 'ab 12',
            'studio'            : 'Columbia Pic., MGM, Rogue Marble, Revolution Studios, Chartoff-Winkler Prod.',
            'o_site'            : False,
            'site'              : 'http://www.zweitausendeins.de/filmlexikon/?sucheNach=titel&wert=528267',
            'trailer'           : False,
            'year'              : 2006,
            'notes'             : False,
            'runtime'           : 102,
            'image'             : True,
            'rating'            : False,
            'screenplay'        : 'Sylvester Stallone',
            'cameraman'         : 'J. Clark Mathis',
        },
        '26956' : { 
            'title'             : 'Bürgschaft für ein Jahr',
            'o_title'           : 'Bürgschaft für ein Jahr',
            'director'          : 'Herrmann Zschoche',
            'plot'              : True,
            'cast'              : 'Heide Kipp' + _(' as ') + 'Frau Braun\n\
Jan Spitzer' + _(' as ') + 'Werner Horn\n\
Monika Lennartz' + _(' as ') + 'Irmgard Behrend\n\
Katrin Saß' + _(' as ') + 'Nina\n\
Ursula Werner' + _(' as ') + 'Frau Müller\n\
Christian Steyer' + _(' as ') + 'Heiner Menk\n\
Jaecki Schwarz' + _(' as ') + 'Peter Müller\n\
Barbara Dittus' + _(' as ') + 'Heimleiterin',
            'country'           : 'DDR',
            'genre'             : 'Arbeiterfilm, Frauenfilm, Literaturverfilmung',
            'classification'    : 'ab 6',
            'studio'            : 'DEFA, Gruppe "Berlin"',
            'o_site'            : False,
            'site'              : 'http://www.zweitausendeins.de/filmlexikon/?sucheNach=titel&wert=26956',
            'trailer'           : False,
            'year'              : 1981,
            'notes'             : False,
            'runtime'           : 93,
            'image'             : True,
            'rating'            : False,
            'screenplay'        : 'Gabriele Kotte',
            'cameraman'         : 'Günter Jaeuthe',
        },
        '524017' : { 
            'title'             : 'Arahan',
            'o_title'           : 'Arahan Jangpung Daejakjeon',
            'director'          : 'Ryoo Seung-wan',
            'plot'              : True,
            'cast'              : 'Ryu Seung-beom' + _(' as ') + 'Sang-hwan\n\
Yoon So-yi' + _(' as ') + 'Wi-jin\n\
Yun Ju-sang' + _(' as ') + 'Mu-woon\n\
Ahn Sung-kee' + _(' as ') + 'Ja-woon\n\
Jung Doo-hong' + _(' as ') + 'Heukwoon',
            'country'           : 'Südkorea',
            'genre'             : False,
            'classification'    : 'ab 16',
            'studio'            : 'Fun and Happiness, Good Movie',
            'o_site'            : False,
            'site'              : 'http://www.zweitausendeins.de/filmlexikon/?sucheNach=titel&wert=524017',
            'trailer'           : False,
            'year'              : 2004,
            'notes'             : False,
            'runtime'           : 108,
            'image'             : False,
            'rating'            : False,
            'screenplay'        : 'Ryoo Seung-wan',
            'cameraman'         : 'Lee Jun-gyu',
        }
    }
