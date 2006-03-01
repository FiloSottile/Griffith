# -*- coding: UTF-8 -*-

__revision__ = '$Id: PluginMovieIMDB.py 176 2006-02-01 12:07:26Z iznogoud $'

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

plugin_name = "Allocine"
plugin_description = "Internet Movie Database"
plugin_url = "www.allocine.fr"
plugin_language = _("French")
plugin_author = "Pierre-Luc Levy"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version = "0.5"

class Plugin(movie.Movie):
    def __init__(self, id):
        # self.encode='iso-8859-1'
        self.movie_id = id
        self.url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=" + str(self.movie_id) + ".html"
	print "retrieve " + self.url +"\n"
        
    def picture(self):
	print "picture foundind ...\n";
        self.picture_url = gutils.trim(self.page,"Poster","Date de sor")
	print "eesai #0 " + self.picture_url + "\n";
        self.picture_url = gutils.after(self.picture_url,"activerlientexte.inc")
	print "eesai #1 " + self.picture_url + "\n";
        self.picture_url = gutils.trim(self.picture_url,"<img src=\"","\"")
	print "eesai #2 " + self.picture_url + "\n";

    def original_title(self):
        self.original_title = ""
        self.original_title = gutils.trim(self.page,"Titre original : <i>","</i>")
	if (self.original_title==''):
		self.original_title = gutils.trim(self.page,"<title>","</title>")

    def title(self):
        self.title = gutils.trim(self.page,"<title>","</title>")

    def director(self):       
        #self.director = gutils.trim(self.page,"<a href=\"/name/","</a><br>")
        #self.director = gutils.after(self.director,">")
        #self.director = gutils.trim(self.page,"Directed by</b><br>","<br>")
        self.director = gutils.trim(self.page," par <","</a>")
        self.director = gutils.after(self.director,">")
	print "**1* " + self.director + "\n"
	#PLL

        self.director = ""
        self.director = gutils.trim(self.page,"<h4>Réalisé par ","</h4>")
	self.director = gutils.strip_tags(self.director)
	print "**2* " + self.director + "\n"
        
    def plot(self):
        self.plot = gutils.trim(self.page,"Synopsis</b></h3></td></tr></table>","</h4>")
        self.plot = gutils.after(self.plot,"<h4>")
        
    def year(self):
        self.year = gutils.trim(self.page,"e de production : ","</h4>")
	#PLL
        
    def running_time(self):
        self.running_time = gutils.trim(self.page,"Dur*e : ","min")
        #self.running_time = self.running_time*60
	#self.running_time = self.running_time + gutils.trim(self.page,"h ","min")
	#PLL
        
    def genre(self):
        self.genre = gutils.trim(self.page,"<h4>Genre : ","</h4>")
	self.genre = gutils.strip_tags(self.genre)
        
    def with(self):
        self.with = ""
        self.with = gutils.trim(self.page,"<h4>Avec ","</h4>")
	self.with = gutils.strip_tags(self.with)
        
    def classification(self):
        self.classification = ""
        
    def studio(self):
        self.studio = ""
        
    def site(self):
        self.site = ""
        
    def imdb(self):
        self.imdb = "http://www.allocine.fr/film/fichefilm_gen_cfilm=" + self.movie_id + ".html";
        
    def trailer(self):
        self.trailer = "http://www.allocine.fr/film/video_gen_cfilm=" + self.movie_id + ".html"
        
    def country(self):
        self.country = gutils.trim(self.page,"<h4>Film ",".</h4>&nbsp;")
        # self.country = gutils.after(self.country,"/\">")
        
    def rating(self):
        self.rating = gutils.trim(self.page, """<b class="ch">User Rating:</b>""","/10</b> (")
        if self.rating:
            self.rating = str(float(gutils.clean(self.rating)))
        
class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search    = "http://www.allocine.fr/recherche/?motcle="
        self.translated_url_search    = "http://www.allocine.fr/recherche/?motcle="
        # self.encode='iso-8859-1'
        # self.encode='utf8'
        
    def search(self,parent_window):
        self.open_search(parent_window)
        self.sub_search()
        return self.page
        
    def sub_search(self):
	if (string.find(self.page,"ponse)</h4") > 0):
        	self.page = gutils.trim(self.page,"ponse)</h4>", "<hr /></td>");
	if (string.find(self.page,"ponses)</h4") > 0 ):
        	self.page = gutils.trim(self.page,"ponses)</h4>", "<b>Rechercher :");
        # self.page = self.page.decode('iso-8859-1')
        
    def get_searches(self):
        self.elements = string.split(self.page,"<h4><a href")
        if (self.elements[0]<>''):
            for element in self.elements:
                self.ids.append(gutils.trim(element,"/film/fichefilm_gen_cfilm=",".html"))
                self.titles.append(gutils.strip_tags(gutils.convert_entities(gutils.trim(element,"link1\">","</a>"))))    
        else:
            pass
