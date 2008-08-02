# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Vasco Nunes, Piotr Ozarowski
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

import gettext
gettext.install('griffith', unicode=1)
import gutils
import movie
import string

plugin_name = "PTGate"
plugin_description = "Cinema PTGate"
plugin_url = "www.cinema.ptgate.pt"
plugin_language = _("Portuguese")
plugin_author = "Vasco Nunes"
plugin_author_email="<vasco.m.nunes@gmail.com>"
plugin_version = "0.4.1"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode='iso-8859-1'
        self.movie_id = id
        self.url = "http://cinema.ptgate.pt/filme.php?code=" + str(self.movie_id)

    def get_image(self):
        self.image_url = "http://cinema.ptgate.pt/Movies/" + str(self.movie_id)+".jpg"

    def get_o_title(self):
        self.o_title = string.capwords(gutils.trim(self.page,"<b class=title>","</b><br>") )

    def get_title(self):
        self.title = string.capwords(gutils.trim(self.page,"class=subtitle>","</b><br>") )

    def get_director(self):
        self.director = gutils.trim(self.page,"<b>realização</b><br>","<br><br><b>")

    def get_plot(self):
        self.plot = gutils.trim(self.page,"<b>sinopse</b><br>","<br><br>")
        self.plot = string.replace(self.plot,"'","\"")
        self.plot = string.replace(self.plot,"'","\"")

    def get_year(self):
        self.year = gutils.trim(self.page,"<br><b>ano</b><br>","<br><br><b>pa")

    def get_runtime(self):
        self.runtime = ""

    def get_genre(self):
        self.genre = gutils.trim(self.page,"nero</b><br>","<br><br><b>realiza")
        self.genre = string.replace(self.genre," | ",", ")

    def get_cast(self):
        self.cast = ""
        self.cast = gutils.trim(self.page,"pretes</b><br>","<br><br><b>data de estreia</b><br>")
        self.cast = string.replace(self.cast,"<br> ","\n")
        self.cast = string.replace(self.cast,"<br>", "\n")
        self.cast = gutils.strip_tags(self.cast)

    def get_classification(self):
        self.classification = ""

    def get_studio(self):
        self.studio = ""

    def get_o_site(self):
        self.o_site = gutils.trim(self.page,"tio oficial</b><br><a class=external href='", "'>")

    def get_site(self):
        self.site = gutils.trim(self.page,"<br><b>imdb</b><br><a class=external href='", "'>www.imdb.com")

    def get_trailer(self):
        self.trailer = gutils.trim(self.page,"trailer</b><br><a class=external href='", "'>visionar")

    def get_country(self):
        self.country = gutils.trim(self.page,"s</b><br>","<br><br><b>g")
        
    def get_notes(self):
        self.notes = gutils.trim(self.page,"prémios e nomeações</b><br><b>", "<td width=6 background='Images/group_r.gif'")
        self.notes = gutils.strip_tags(self.notes)

    def get_rating(self):
        tmp=gutils.trim(self.page,"'Images/mstar",".gif")
        if(tmp):
            self.rating = float(tmp)
            if (self.rating>10):
                self.rating = int(self.rating/10)
                self.rating = self.rating*2
        else:
            self.rating=""

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.original_url_search    = "http://cinema.ptgate.pt/pesquisa-filme.php?titulo="
        self.translated_url_search    = "http://cinema.ptgate.pt/pesquisa-filme.php?titulo="
        self.encode='iso-8859-1'

    def search(self,parent_window):
        self.open_search(parent_window)
        self.sub_search()
        return self.page

    def sub_search(self):
        self.page = gutils.trim(self.page,"<!-- DISPLAY RESULTS -->", "<!-- /DISPLAY RESULTS -->")

    def get_searches(self):
        elements = string.split(self.page,"</td><td>")
        self.number_results = elements[-1]

        if (len(elements[0])):
            for element in elements:
                element = string.replace(element,"</a>","")
                self.ids.append(gutils.trim(element,"?code=","'>"))
                self.titles.append(gutils.convert_entities(gutils.trim(element,"'>","</td><td width=6")))
        else:
            self.number_results = 0
