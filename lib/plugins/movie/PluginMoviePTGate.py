# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005 Vasco Nunes
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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import movie
import string

plugin_name = "PTGate"
plugin_description = "Cinema PTGate"
plugin_url = "www.cinema.ptgate.pt"
plugin_language = _("Portuguese")
plugin_author = "Vasco Nunes"
plugin_author_email="<vasco.m.nunes@gmail.com>"
plugin_version = "0.1.1"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode='iso-8859-1'
        self.movie_id = id
        self.url = "http://cinema.ptgate.pt/filme.php?code=" + str(self.movie_id)
        
    def picture(self):
        self.picture_url = "http://cinema.ptgate.pt/Movies/" + str(self.movie_id)+".jpg"
        
    def original_title(self):
        self.original_title = string.capwords(gutils.trim(self.page,"<b class=title>","</b><br>") ) 
    
    def title(self):
        self.title = string.capwords(gutils.trim(self.page,"class=subtitle>","</b><br>") )
                
    def director(self):
        self.director = gutils.trim(self.page,"<b>realização</b><br>","<br><br><b>")
                
    def plot(self):
        self.plot = gutils.trim(self.page,"<b>sinopse</b><br>","<br><br>")
        self.plot = string.replace(self.plot,"'","\"")
        self.plot = string.replace(self.plot,"'","\"")
        
    def year(self):
        self.year = gutils.trim(self.page,"<br><b>ano</b><br>","<br><br><b>pa")
        
    def running_time(self):
        self.running_time = ""
        
    def genre(self):
        self.genre = gutils.trim(self.page,"nero</b><br>","<br><br><b>realiza")
        self.genre = string.replace(self.genre," | ",", ")
        
    def with(self):
        self.with = ""
        self.with = gutils.trim(self.page,"pretes</b><br>","<br><br><b>data de estreia</b><br>")
        self.with = string.replace(self.with,"<br>", "\n")
        self.with = gutils.strip_tags(self.with)
    
    def classification(self):
        self.classification = ""
        
    def studio(self):
        self.studio = ""
        
    def site(self):
        self.site = gutils.trim(self.page,"tio oficial</b><br><a class=external href='", "'>")
        
    def imdb(self):
        self.imdb = gutils.trim(self.page,"<br><b>imdb</b><br><a class=external href='", "'>www.imdb.com")
        
    def trailer(self):
        self.trailer = gutils.trim(self.page,"trailer</b><br><a class=external href='", "'>visionar")
        
    def country(self):
        self.country = gutils.trim(self.page,"s</b><br>","<br><br><b>g")
        
    def rating(self):
        self.rating = ""            
                     
class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.original_url_search    = "http://cinema.ptgate.pt/pesquisa.php?pesquisa="
        self.translated_url_search    = "http://cinema.ptgate.pt/pesquisa.php?pesquisa="
        self.encode='iso-8859-1'
        
    def search(self,parent_window):
        self.open_search(parent_window)
        self.sub_search()
        return self.page
        
    def sub_search(self):
        self.page = gutils.trim(self.page,"class=group>pesquisa por filme</b>", "class=group>pesquisa por int")
        
    def get_searches(self):
        self.elements = string.split(self.page,"<br></td>")
        self.number_results = self.elements[-1]
        
        if (len(self.elements[0])):
            for element in self.elements:
                element = string.replace(element,"</a>","")
                self.ids.append(gutils.trim(element,"?code=","'>"))
                self.titles.append(gutils.convert_entities(gutils.trim(element,"'>","</td><td width=6")))
        else:
            self.number_results = 0
