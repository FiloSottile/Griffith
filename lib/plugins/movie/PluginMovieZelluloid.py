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
import re

plugin_name         = 'Zelluloid.de'
plugin_description  = 'ZELLULOID.DE'
plugin_url          = 'www.zelluloid.de'
plugin_language     = _('German')
plugin_author       = 'Michael Jahn'
plugin_author_email = '<mikej06@hotmail.com>'
plugin_version      = '1.0'

class Plugin(movie.Movie):
    index_url = 'http://www.zelluloid.de/filme/index.php3?id='
    
    def __init__(self, id):
        self.encode='iso-8859-1'
        self.movie_id = id
        self.url = "http://www.zelluloid.de/filme/details.php3?id=" + self.movie_id

    def initialize(self):
        self.detail_page = self.page
        self.url = self.index_url + self.movie_id
        self.page = self.open_page(url=self.url)

    def get_image(self):
        self.image_url = 'http://www.zelluloid.de/images/poster/' + gutils.trim(self.page, '<IMG SRC="/images/poster/', '"');

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, 'Originaltitel: ', '<BR>')
        if self.o_title == '':
            self.o_title = gutils.trim(self.page, '<title>', '|')

    def get_title(self):
        self.title = gutils.trim(self.page, '<title>', '|')

    def get_director(self):
        self.director = gutils.trim(self.detail_page, 'Regie', '</A>')

    def get_plot(self):
        self.plot = gutils.trim(self.page, '<DIV CLASS=bigtext>', '</DIV>')
        
    def get_year(self):
        self.year = ''
        elements = string.split(self.detail_page, '/directory/az.php3?j')
        elements[0] = ''
        delimiter = ''
        for element in elements:
            if element <> '':
                self.year = self.year + delimiter + gutils.trim(element, '>', '<')
                delimiter = ', '

    def get_runtime(self):
        self.runtime = gutils.trim(self.detail_page, 'ca.&nbsp;', '&nbsp;min');

    def get_genre(self):
        self.genre = ''
        elements = string.split(self.detail_page, '/directory/az.php3?g')
        elements[0] = ''
        delimiter = ''
        for element in elements:
            if element <> '':
                self.genre = self.genre + delimiter + gutils.trim(element, '>', '<')
                delimiter = ', '

    def get_cast(self):
        self.cast = gutils.trim(self.detail_page, 'alt="Besetzung"', '<TD COLSPAN=')
        self.cast = self.cast.replace('<A HREF=', '--flip--' + '<A HREF=')
        self.cast = gutils.strip_tags(self.cast)
        self.cast = gutils.after(self.cast, '>')
        elements = self.cast.split('\n')
        self.cast = ''
        for element in elements:
            elements2 = element.split("--flip--")
            if len(elements2) > 1:
                self.cast += elements2[1] + '--flip--' + elements2[0] + '\n'
            else:
                self.cast += element + '\n'
        self.cast = string.replace(self.cast, '--flip--', _(' as '))

    def get_classification(self):
        self.classification = gutils.trim(self.detail_page, 'FSK: ', '</TD>')
        self.classification = re.sub(',.*', '', self.classification)

    def get_studio(self):
        self.studio = gutils.strip_tags(gutils.trim(self.detail_page, 'alt="Produktion"', '&nbsp;'))
        if self.studio == '':
            self.studio = gutils.trim(self.detail_page, 'alt="Produktion"', '</TABLE>')
        self.studio = gutils.after(self.studio, '>')
        self.studio = self.studio.replace('\n', ', ')
        self.studio = re.sub('((^, )|(, $))', '', self.studio)
        
    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = "http://www.zelluloid.de/filme/details.php3?id=" + self.movie_id

    def get_trailer(self):
        self.trailer = ""

    def get_country(self):
        self.country = ''
        elements = string.split(self.detail_page, '/directory/az.php3?l')
        elements[0] = ''
        delimiter = ''
        for element in elements:
            if element <> '':
                self.country = self.country + delimiter + gutils.trim(element, '>', '<')
                delimiter = ', '

    def get_rating(self):
        self.rating = gutils.strip_tags(gutils.trim(self.page, 'User-Wertung:', '</TABLE>'))
        self.rating = self.rating.replace('%', '')
        self.rating = self.rating.replace('&nbsp;', '')
        self.rating = self.rating.replace('\n', '')
        try:
            ratingint = round(float(self.rating) / 10.0)
        except:
            ratingint = 0
        self.rating = str(ratingint)

    def get_notes(self):
        self.notes = ""

class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search   = "http://www.zelluloid.de/suche/index.php3?qstring="
        self.translated_url_search = "http://www.zelluloid.de/suche/index.php3?qstring="
        self.encode='iso-8859-1'
        self.remove_accents = False

    def search(self,parent_window):
        self.open_search(parent_window)
        tmp = gutils.trim(self.page, "Der Suchbegriff erzielte", "</TABLE>")
        return tmp

    def get_searches(self):
        elements = string.split(self.page, "hit.php3?hit=")
        elements[0] = ''
        for element in elements:
            if element <> '':
                id = gutils.trim(element, 'movie-', '-')
                if id <> '':
                    self.ids.append(id)
                    self.titles.append(gutils.strip_tags(string.replace(gutils.trim(element, '>', '</A>'), '<BR>', ' - ')))

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> expected result count }
    #
    test_configuration = {
        'Rocky Balboa'        : 1,
        'Die wilden Hühner'    : 3
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
        '2835' : { 
            'title'             : 'Rocky Balboa',
            'o_title'             : 'Rocky Balboa',
            'director'            : 'Sylvester Stallone',
            'plot'                 : True,
            'cast'                : 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie\n\
Antonio Tarver' + _(' as ') + 'Mason Dixon\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Milo Ventimiglia' + _(' as ') + 'Rocky Jr.\n\
Tony Burton' + _(' as ') + 'Duke\n\
A.J. Benza' + _(' as ') + 'L.C.\n\
James Francis Kelly III' + _(' as ') + 'Steps\n\
Talia Shire' + _(' as ') + 'Adrian\n\
Lou DiBella' + _(' as ') + 'Lou DiBella\n\
Mike Tyson' + _(' as ') + 'Mike Tyson\n\
Henry G. Sanders' + _(' as ') + 'Martin',
            'country'            : 'USA',
            'genre'                : 'Drama, Sport',
            'classification'    : 'ab 12',
            'studio'            : 'Chartoff-Winkler Productions, Columbia Pictures Corporation, Metro-Goldwyn-Mayer, Revolution Studios, Rogue Marble',
            'o_site'            : False,
            'site'                : 'http://www.zelluloid.de/filme/details.php3?id=2835',
            'trailer'            : False,
            'year'                : 2006,
            'notes'                : False,
            'runtime'            : 102,
            'image'                : True,
            'rating'            : 8.0
        },
        '6342' : { 
            'title'             : 'Die wilden Hühner',
            'o_title'             : 'Die wilden Hühner',
            'director'            : 'Vivian Naefe',
            'plot'                 : True,
            'cast'                : 'Michelle von Treuberg' + _(' as ') + 'Sprotte\n\
Lucie Hollmann' + _(' as ') + 'Frieda\n\
Paula Riemann' + _(' as ') + 'Melanie\n\
Zsa Zsa Inci Bürkle' + _(' as ') + 'Trude\n\
Jette Hering' + _(' as ') + 'Wilma\n\
Jeremy Mockridge' + _(' as ') + 'Fred\n\
Philip Wiegratz' + _(' as ') + 'Steve\n\
Martin Kurz' + _(' as ') + 'Torte\n\
Vincent Redetzki' + _(' as ') + 'Willi\n\
Veronica Ferres' + _(' as ') + 'Sprottes Mutter Sibylle\n\
Doris Schade' + _(' as ') + 'Oma Slättberg\n\
Jessica Schwarz' + _(' as ') + 'Frau Rose\n\
Benno Fürmann' + _(' as ') + 'Herr Grünbaum\n\
Axel Prahl' + _(' as ') + 'Willis Vater\n\
Lukas Steimel' + _(' as ') + 'Luki\n\
Lukas Engel' + _(' as ') + 'Titus\n\
Pino Severino Geyssen' + _(' as ') + 'Paolo\n\
Christine Rose' + _(' as ') + 'Jutta\n\
Herbert Meurer' + _(' as ') + 'Herr Feistkorn\n\
Marius Fischer' + _(' as ') + 'Bo\n\
Anya Hoffmann' + _(' as ') + 'Melanies Mutter\n\
Frank Wickermann' + _(' as ') + 'Melanies Vater\n\
Axel Häfner' + _(' as ') + 'Schrottplatzwärter\n\
Simon Gosejohann' + _(' as ') + 'junger Mann\n\
Piet Klocke' + _(' as ') + 'Junggeselle',
            'country'            : 'Deutschland',
            'genre'                : 'Kinder',
            'classification'    : 'ohne',
            'studio'            : 'Bavaria Film, Constantin Film',
            'o_site'            : False,
            'site'                : 'http://www.zelluloid.de/filme/details.php3?id=6342',
            'trailer'            : False,
            'year'                : 2006,
            'notes'                : False,
            'runtime'            : 109,
            'image'                : True,
            'rating'            : 8.0
        }
    }
