# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007
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

plugin_name = "MyMoviesIt"
plugin_description = "mymovies.it"
plugin_url = "www.mymovies.it"
plugin_language = _("Italian")
plugin_author = "Giovanni Sposito, Filippo Valsorda"
plugin_author_email = "<giovanni.sposito@gmail.com>, <filosottile.wiki@gmail.com>"
plugin_version = "0.2"

class Plugin(movie.Movie):

    def __init__(self, id):
        self.encode = 'iso-8859-1'
        self.movie_id = id
        self.url = "http://www.mymovies.it/dizionario/recensione.asp?id=%s" % self.movie_id

    def get_image(self):
        tmp_image = string.find(self.page, '<img style="float:left; border:solid 1px gray; padding:3px; margin:5px;" src="')
        if tmp_image == -1:
            self.image_url = ''
        else:
            self.image_url = gutils.trim(self.page[tmp_image:], 'src="', '"')

    def get_o_title(self):
        tmp = gutils.trim(self.page, 'Titolo originale <em>', '</em>')
        if not tmp:
            self.o_title = gutils.trim(self.page, '<h1 style="margin-bottom:3px;">', '</h1>')
        else:
            self.o_title = tmp

    def get_title(self):
        self.title = gutils.trim(self.page, '<h1 style="margin-bottom:3px;">', '</h1>')

    def get_director(self):
        pos_iniziale = string.find(self.page, '<div style="text-align:left" class="linkblu">')
        self.director = gutils.trim(self.page[pos_iniziale:],'Un film di <a','</a>')
        self.director = gutils.after(self.director,'>')
        if not self.director:
            self.director = gutils.trim(self.page[pos_iniziale:], 'Un film di ', 'Con')
        if len(self.director) > 25:
            self.director = gutils.trim(self.page[pos_iniziale:],'Un film di ','<')

    def get_plot(self):
        pos_iniziale = string.find(self.page, '<div id="recensione">')
        self.plot = gutils.trim(self.page[pos_iniziale:],'<p>','</p>')
        if '</a>' in self.plot:
            self.plot = gutils.after(self.plot, '</a>')

    def get_year(self):
        self.year = gutils.regextrim(self.page,'<strong> <a title="Film [0-9]+" href="http://www.mymovies.it/film/[0-9]+/">', '</a></strong>')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, 'durata ', ' min.')

    def get_genre(self):
        self.genre = gutils.regextrim(self.page,'<a title="Film [a-zA-Z]+" href="http://www.mymovies.it/film/[a-zA-Z]+/">', '</a>')

    def get_cast(self): # TODO
        tmp = string.find(self.page, 'Con <a')
        self.cast = gutils.trim(self.page[tmp:],'Con ','</a>.')
        self.cast = string.replace(self.cast, ',', '\n')

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = ''

    def get_o_site(self):
        self.o_site = ''
        #tmp = gutils.trim(self.page, 'http://www.imdb.com', '"')
        #if tmp != '':
        #    self.o_site = 'http://www.imdb.com' + tmp

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = "http://www.mymovies.it/trailer/?id=%s" % self.movie_id

    def get_country(self):
        pos = string.find(self.page, ' min.')
        self.country = gutils.trim(self.page[pos+2:], '- ', '  <')

    def get_rating(self):
        rat = gutils.trim(self.page, '<div style="text-align:center; font-size:23px; font-weight:bold; letter-spacing:1px; margin:0px 11px 7px 11px">', '<span style="font-size:11px">/5</span></div>')
        if rat != '':
            self.rating = int(round(float(rat.replace(',', '.'))*2, 0))
        else:
            self.rating = 0

    def get_notes(self):
        #self.notes = ''
        #tmp = gutils.trim(self.page, 'Alt. titel:', '</span>')
        #if tmp:
        #    self.notes = self.notes + 'Alt. titel:' + string.strip(gutils.strip_tags(tmp))
        self.notes = ''

class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search = "http://www.mymovies.it/database/ricerca/?q="
        self.translated_url_search = "http://www.mymovies.it/database/ricerca/?q="
        self.encode = 'iso-8859-1'

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        #self.sub_search()
        return self.page

    def sub_search(self):
        self.page = gutils.trim(self.page, "ho trovato i seguenti risultati:", "Altri risultati tra i film con la parola")

    def get_searches(self):
        elements = string.split(self.page,"<h3 style=\"margin:0px;\">")
        self.number_results = len(elements) - 1

        if self.number_results > 0:
            i = 1
            while i < len(elements):
                element = gutils.trim(elements[i],"<a","</a>")
#                print "******* elemento "+str(i)+" **********\n\n\n\n\n"+element+"\n******fine*******\n\n\n\n\n\n"
#                print "id = "+gutils.trim(element,"recensione.asp?id=","\"")
#                print "title = "+gutils.convert_entities(gutils.strip_tags(gutils.trim(element,'" title="', '"')))

                self.ids.append(gutils.trim(element,"recensione.asp?id=","\""))
                self.titles.append(gutils.convert_entities(gutils.strip_tags(gutils.trim(element,'" title="', '"'))))
                i += 1
        else:
            self.number_results = 0

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> expected result count }
    #
    test_configuration = {
        'Rocky Balboa'            : 1
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
        '44566' : {
            'title'             : 'Rocky Balboa',
            'o_title'             : 'Rocky Balboa',
            'director'            : 'Sylvester Stallone',
            'genre'                : 'Sportivo',
            'year'                : 2006
        }
    }
