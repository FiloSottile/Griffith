# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Vasco Nunes, Piotr Ożarowski
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

# Updated on 04/29/2007 by Djohnson "Joe" Lima
# joe1310@terra.com.br - São Paulo/Brasil


import gutils, movie, string

plugin_name = "E-Pipoca"
plugin_description = "E-Pipoca Brasil"
plugin_url = "epipoca.uol.com.br"
plugin_language = _("Brazilian Portuguese")
plugin_author = "Vasco Nunes"
plugin_author_email="<vasco.m.nunes@gmail.com>"
plugin_version = "0.5"

class Plugin(movie.Movie):
    "A movie plugin object"
    def __init__(self, id):
        self.encode='iso-8859-1'
        self.movie_id = id
        self.url = "http://epipoca.uol.com.br/filmes_detalhes.php?idf=" + str(self.movie_id)

    def get_image(self):
        "Find the film's poster image"
        tmp_pic = gutils.trim(self.page, "images/filmes/poster/poster_", "\"")
        self.image_url = \
            "http://epipoca.uol.com.br/images/filmes/poster/poster_" + tmp_pic

    def get_o_title(self):
        "Find the film's original title"
        self.o_title = string.capwords(gutils.trim(self.page, "</font><br>(", ", "))

    def get_title(self):
        """Find the film's local title.
        Probably the original title translation"""
        self.title = gutils.trim(self.page, "<TITLE>", " (")

    def get_director(self):
        "Find the film's director"
        self.director = gutils.trim(self.page, "<b>Diretor(es): </b>", "</a></td>")

    def get_plot(self):
        "Find the film's plot"
        self.plot = gutils.trim(self.page, "<b>SINOPSE</b></font><br><br>", "</td></tr>")

    def get_year(self):
        "Find the film's year"
        self.year = gutils.trim(self.page, "<a href=\"busca_mais.php?opc=ano&busca=", "\">")

    def get_runtime(self):
        "Find the film's running time"
        self.runtime = gutils.trim(self.page, "<td><b>Dura", " min.</td>")
        self.runtime = self.runtime[9:]

    def get_genre(self):
        "Find the film's genre"
        self.genre = gutils.trim(self.page, "<a href=\"busca_mais.php?opc=genero&busca=", "\">")

    def get_cast(self):
        "Find the actors. Try to make it line separated."
        self.cast = ""
        self.cast = gutils.trim(self.page, "<b>Elenco: </b>", "<b>mais...</b>")
        self.cast = gutils.strip_tags(self.cast)
        self.cast = self.cast[:-2]

    def get_classification(self):
        "Find the film's classification"
        self.classification = ""

    def get_studio(self):
        "Find the studio"
        self.studio = gutils.trim(self.page, "<b>Distribuidora(s): </b>", "</a></td>")

    def get_o_site(self):
        "Find the film's oficial site"
        self.o_site = "http://epipoca.uol.com.br/filmes_web.php?idf=" + str(self.movie_id)

    def get_site(self):
        "Find the film's imdb details page"
        self.site = "http://epipoca.uol.com.br/filmes_ficha.php?idf=" + str(self.movie_id)

    def get_trailer(self):
        "Find the film's trailer page or location"
        self.trailer = "http://epipoca.uol.com.br/filmes_trailer.php?idf=" + str(self.movie_id)
            
    def get_country(self):
        "Find the film's country"
        self.country = gutils.trim(self.page, "<a href=\"busca_mais.php?opc=pais&busca=", "\">")

    def get_rating(self):
        """Find the film's rating. From 0 to 10.
        Convert if needed when assigning."""
        tmp_rating = gutils.trim(self.page, "<br><b>Cota", " (")
        tmp_rating = gutils.after(tmp_rating, "</b>")
        if tmp_rating <> "":
            tmp_rating = string.replace(tmp_rating,',','.')
            self.rating = str( float(string.strip(tmp_rating)) )
        else:
            self.rating = ""

class SearchPlugin(movie.SearchMovie):
    "A movie search object"
    def __init__(self):
        self.original_url_search = \
            "http://epipoca.uol.com.br/busca.php?opc=todos&busca="
        self.translated_url_search = \
            "http://epipoca.uol.com.br/busca.php?opc=todos&busca="
        self.encode='iso-8859-1'

    def search(self, parent_window):
        "Perform the web search"
        self.open_search(parent_window)
        self.sub_search()
        return self.page

    def sub_search(self):
        "Isolating just a portion (with the data we want) of the results"
        self.page = gutils.trim(self.page, \
            "&nbsp;Resul","><b>Not") 

    def get_searches(self):
        "Try to find both id and film title for each search result"
        elements = string.split(self.page, "<td width=\"55\" align=\"center\" bgcolor=")
        self.number_results = elements[-1]

        if (elements[0] != ''):
            for element in elements:
                self.ids.append(gutils.trim(element, "<a href=\"filmes_detalhes.php?idf=", "\">"))
                self.titles.append(gutils.strip_tags(gutils.trim(element, "<font class=\"titulo\">", "<b>Adicionar aos meus filmes favoritos</b>") ))
        else:
            self.number_results = 0
