# -*- coding: UTF-8 -*-

__revision__ = '$Id: $'

# Copyright (c) 2011 Ivo Nunes
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

plugin_name         = "IMDb-pt"
plugin_description  = "Internet Movie Database Portuguese"
plugin_url          = "www.imdb.pt"
plugin_language     = _("Portuguese")
plugin_author       = "Ivo Nunes"
plugin_author_email = "<netherblood@gmail.com>"
plugin_version      = "0.1"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   ='iso-8859-1'
        self.movie_id = id
        self.url      = "http://www.imdb.pt/title/" + str(self.movie_id)

    def initialize(self):
        self.page = gutils.convert_entities(self.page)

    def get_image(self):
        self.image_url = gutils.trim(self.page, u'src="http://ia.media-imdb.com/images/', u'.jpg" /></a>')
        self.image_url = "http://ia.media-imdb.com/images/" + self.image_url + ".jpg"
        
    def get_o_title(self):
        self.o_title = gutils.trim(self.page, u'<title>', u' (')
        self.o_title = self.o_title.encode(self.encode)

    def get_title(self):
        self.title = gutils.trim(self.page, u'<div class="info-content">       "', u'" - Brasil<br>')
        self.title = self.title.encode(self.encode)

    def get_director(self):
        self.director = gutils.trim(self.page, u'<h5>Diretor:</h5>', u'</a><br/>')
        self.director = gutils.strip_tags(self.director)

    def get_plot(self):
        self.plot = gutils.trim(self.page, u'<meta name="description" content="', u'Visit IMDb for Photos, Showtimes, Cast, Crew, Reviews, Plot Summary, Comments, Discussions, Taglines, Trailers, Posters, Fan Sites">')
        self.plot = self.plot.encode(self.encode)

    def get_year(self):
        self.year = gutils.trim(self.page, u' (', u')</title>')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, u'<h5>Duração:</h5><div class="info-content">', u' min')
        self.runtime = self.runtime.encode(self.encode)

    def get_genre(self):
        self.genre = gutils.trim(self.page, u'<h5>Gênero:</h5>', u'</div>')
        self.genre = gutils.strip_tags(self.genre)
        self.genre = string.replace(self.genre, " | ", ", ")
        self.genre = self.genre.encode(self.encode)

    def get_cast(self):
        #self.cast = gutils.trim(self.page, u'Intérpretes:</b><br />', u'</p>')
        #self.cast = gutils.strip_tags(self.cast)
        #self.cast = string.replace(self.cast, ', ', '\n')
        self.cast = "" # FIXME

    def get_classification(self):
        self.classification = gutils.trim(self.page, u'<h5>Certificação:</h5><div class="info-content">', u'</div>')
        self.classification = gutils.strip_tags(self.classification)
        self.classification = string.replace(self.classification, " | ", ", ")
        self.classification = self.classification.encode(self.encode)

    def get_studio(self):
        self.studio = ''

    def get_o_site(self):
        self.o_site = self.url

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = gutils.trim(self.page, u'<h5>País:</h5><div class="info-content">', '</div>')
        self.country = string.replace(self.country, " | ", ", ")
        self.country = self.country.encode(self.encode)
        
    def get_notes(self):
        self.notes = ''

    def get_rating(self):
        self.rating = gutils.trim(self.page, u'<div class="starbar-meta">', '/10')
    	self.rating = gutils.strip_tags(self.rating)
    	self.rating = string.replace(self.rating, ",", ".")
        self.rating = float(self.rating)
    	self.rating = round(self.rating)

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.original_url_search   = 'http://www.imdb.pt/find?s=all&q='
        self.translated_url_search = 'http://www.imdb.pt/find?s=all&q='
        self.encode                = 'iso-8859-1'

    def search(self, parent_window):
        """Perform the web search"""
        if not self.open_search(parent_window):
            return None
            self.sub_search()
        return self.page

    def sub_search(self):
        """Isolating just a portion (with the data we want) of the results"""
        self.page = gutils.trim(self.page, \
            "Resultado)<table>", "<p><b>Nomes (Coincid")

    def get_searches(self):
        """Try to find both id and film title for each search result"""
        elements = string.split(self.page, 'height="6"><br><a href="')
        self.number_results = elements[-1]

        if (len(elements[0])):
            for element in elements:
                self.ids.append(gutils.trim(element, "title/", '/" onclick="'))
                self.titles.append(gutils.convert_entities \
                    (gutils.trim(element, """/';">""", "</a> ")))
        else:
            self.number_results = 0