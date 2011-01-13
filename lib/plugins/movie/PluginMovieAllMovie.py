# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2009-2011
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
import string, re

plugin_name         = "allmovie"
plugin_description  = "All Media Guide"
plugin_url          = "www.allmovie.com"
plugin_language     = _("English")
plugin_author       = "Michael Jahn"
plugin_author_email = "griffith-private@lists.berlios.de"
plugin_version      = "1.0"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   = 'utf-8'
        self.movie_id = id
        self.url      = 'http://allmovie.com/work/' + str(self.movie_id)

    def initialize(self):
        self.page_cast = self.open_page(url = 'http://allmovie.com/work/' + str(self.movie_id) + '/cast')
        self.page_cast = gutils.trim(self.page_cast, 'id="results-table"', '</table>')
        self.page_credits = self.open_page(url = 'http://allmovie.com/work/' + str(self.movie_id) + '/credits')
        self.page_credits = gutils.trim(self.page_credits, 'id="results-table"', '</table>')

    def get_image(self):
        tmp_page = gutils.trim(self.page, 'image.allmusic.com', '"')
        if tmp_page:
            self.image_url = 'http://image.allmusic.com' + tmp_page
        else:
            self.image_url = ''

    def get_o_title(self):
        title = re.search('(?:[<]span[\t ]+class="title"[>])([^<]+)(?:</span>)', self.page)
        if title:
            self.o_title = title.group(0)
        else:
            self.o_title = ''

    def get_title(self):
        title = re.search('(?:[<]span[\t ]+class="title"[>])([^<]+)(?:</span>)', self.page)
        if title:
            self.title = title.group(0)
        else:
            self.title = ''

    def get_director(self):
        self.director = ''
        tmp = gutils.trim(self.page, '<span>Director</span>', '</table>')
        directors = re.split('artist/', tmp)
        for index in range(1, len(directors), 1):
            director = directors[index]
            if index > 1:
                self.director = self.director + ', ' + gutils.trim(director, '>', '<')
            else:
                self.director = self.director + gutils.trim(director, '>', '<')

    def get_plot(self):
        self.plot = gutils.trim(self.page, 'Plot Synopsis</td>', '</table>')
        self.plot = string.replace(self.plot, '</tr>', '\n')

    def get_year(self):
        self.year = gutils.trim(self.page, 'href="http://allmovie.com/explore/year/', '"')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, '<span>Run Time</span>', '</table>')
        foundtime = re.search('([0-9]+)(?: min[.])', self.runtime)
        if foundtime:
            self.runtime = foundtime.group(1)
        else:
            self.runtime = 0

    def get_genre(self):
        self.genre = ''
        genres = re.split('href=["\']*http[:]//allmovie.com/explore/genre/', gutils.trim(self.page, '<span>Genres</span>', '</table>'))
        for index in range(1, len(genres), 1):
            genre = genres[index]
            if index > 1:
                self.genre = self.genre + ', ' + gutils.trim(genre, '>', '<')
            else:
                self.genre = self.genre + gutils.trim(genre, '>', '<')

    def get_cast(self):
        self.cast = ''
        casts = re.split('artist/', self.page_cast)
        for index in range(1, len(casts), 1):
            cast = casts[index]
            name = gutils.trim(cast, '>', '<')
            played = gutils.clean(gutils.trim(cast, '>- ', '</td>'))
            if played:
                name = name + _(' as ') + played
            if index > 1:
                self.cast = self.cast + '\n' + name
            else:
                self.cast = self.cast + name

    def get_classification(self):
        self.classification = ''
        tmp = gutils.trim(self.page, '<span>MPAA Rating</span>', '</table>')
        jumptd = string.find(tmp, '</td>')
        if jumptd >= 0:
            jumptd = string.find(tmp[jumptd + 1:], '</td>')
            if jumptd >= 0:
                self.classification = tmp[jumptd + 1:]

    def get_studio(self):
        self.studio = ''
        tmp = gutils.trim(self.page, '<span>Produced by</span>', '</table>')
        studios = re.split('search/tag/899/', tmp)
        for index in range(1, len(studios), 1):
            studio = studios[index]
            if index > 1:
                self.studio = self.studio + ', ' + gutils.trim(studio, '>', '<')
            else:
                self.studio = self.studio + gutils.trim(studio, '>', '<')

    def get_o_site(self):
        self.o_site = ''
        offsindex = string.find(self.page, '>Official Site</a>')
        if offsindex >= 0:
            offsindex = string.rfind(self.page[:offsindex], 'href="')
            if offsindex >= 0:
                self.o_site = gutils.before(self.page[offsindex + 6:], '"')

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = ''
        countries = re.split('href=["\']*http[:]//allmovie.com/explore/country/', self.page)
        for index in range(1, len(countries), 1):
            country = countries[index]
            if index > 1:
                self.country = self.country + ', ' + gutils.trim(country, '>', '<')
            else:
                self.country = self.country + gutils.trim(country, '>', '<')

    def get_rating(self):
        tmp = gutils.trim(self.page, '<span>Work Rating</span>', '</table>')
        foundnumber = re.search('(?:title=")([0-9])(?: Stars)', tmp)
        if foundnumber:
            try:
                self.rating = str(int(foundnumber.group(1)) * 2)
            except:
                self.rating = '0'

    def get_notes(self):
        self.notes = ''

    def get_cameraman(self):
        self.cameraman = ''
        credits = re.split('artist/', self.page_credits)
        for index in range(1, len(credits), 1):
            credit = credits[index]
            name = gutils.trim(credit, '>', '<')
            played = string.find(credit, 'Cinematographer')
            if played >= 0:
                if self.cameraman:
                    self.cameraman = self.cameraman + ', ' + name
                else:
                    self.cameraman = self.cameraman + name

    def get_screenplay(self):
        self.screenplay = ''
        credits = re.split('artist/', self.page_credits)
        for index in range(1, len(credits), 1):
            credit = credits[index]
            name = gutils.trim(credit, '>', '<')
            played = string.find(credit, 'Screenwriter')
            if played >= 0:
                if self.screenplay:
                    self.screenplay = self.screenplay + ', ' + name
                else:
                    self.screenplay = self.screenplay + name

    def get_barcode(self):
        self.barcode = ''

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.original_url_search   = "http://allmovie.com/search/all/"
        self.translated_url_search = "http://allmovie.com/search/all/"
        self.encode                = 'utf-8'

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        return self.page

    def get_searches(self):
        elements = re.split('href=["\']*http[:]//allmovie.com/work/', self.page)
        for index in range(1, len(elements), 1):
            element = elements[index]
            idend = re.search('["\']', element)
            if idend:
                id = element[:idend.end() - 1]
                title = gutils.trim(element, '>', '<')
                additionals = re.split('class=["\']cell[^>]+[>]', element)
                if len(additionals) > 2:
                    title = title + ' (' + gutils.clean(gutils.before(additionals[2], '</td'))
                    if len(additionals) > 3:
                        title = title + ', ' + gutils.clean(gutils.before(additionals[3], '</td'))
                        if len(additionals) > 4:
                            title = title + ', ' + gutils.clean(gutils.before(additionals[4], '</td'))
                    title = title + ')'
                self.ids.append(id)
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
        'Rocky Balboa' : [ 28, 28 ],
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
        'rocky-balboa-337682' : { 
            'title'               : 'Rocky Balboa',
            'o_title'             : 'Rocky Balboa',
            'director'            : 'Sylvester Stallone',
            'plot'                : True,
            'cast'                : 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie\n\
Antonio Tarver' + _(' as ') + 'Mason "The Line" Dixon\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Milo Ventimiglia' + _(' as ') + 'Rocky Balboa Jr.\n\
Tony Burton' + _(' as ') + 'Duke\n\
A.J. Benza' + _(' as ') + 'L.C.\n\
James Francis Kelly III' + _(' as ') + 'Steps\n\
Lou DiBella\n\
Mike Tyson' + _(' as ') + 'Himself\n\
Woodrow W. Paige\n\
Skip Bayless\n\
Jay Crawford\n\
Brian Kenny\n\
Dana Jacobson\n\
Chuck Johnson\n\
Jim Lampley\n\
Larry Merchant\n\
Max Kellerman\n\
Leroy Neiman\n\
Bert Randolph Sugar\n\
Bernard Fernandez\n\
Michael Buffer\n\
Talia Shire',
            'country'             : 'USA',
            'genre'               : 'Drama',
            'classification'      : 'PG',
            'studio'              : 'Chartoff Winkler Productions, Columbia Pictures, MGM, Revolution Studios',
            'o_site'              : 'http://www.rocky.com/',
            'site'                : 'http://allmovie.com/work/rocky-balboa-337682',
            'trailer'             : False,
            'year'                : 2006,
            'notes'               : False,
            'runtime'             : 101,
            'image'               : True,
            'rating'              : 6,
            'cameraman'           : 'Clark Mathis',
            'screenplay'          : 'Sylvester Stallone',
            'barcode'             : False
        },
    }
