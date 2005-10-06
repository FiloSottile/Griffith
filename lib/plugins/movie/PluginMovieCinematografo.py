# -*- coding: UTF-8 -*-

__revision__ = '$Id: PluginMovieCinematografo.py,v 1.3 2005/09/18 20:54:07 iznogoud Exp $'

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
import gutils, movie, string

plugin_name = "Cinematografo"
plugin_description = "Rivista del Cinematografo dal 1928"
plugin_url = "www.cinematografo.it"
plugin_language = _("Italian")
plugin_author = "Vasco Nunes"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version = "0.1"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode='iso-8859-1'
        self.movie_id = id
        self.url = "http://www.cinematografo.it/bdcm/bancadati_scheda.asp?sch=" \
            + str(self.movie_id)
        
    def picture(self):
        "Find the film's poster image"
        tmp_poster = gutils.trim(self.page, "src=\"img/", ".JPG\"") 
        if tmp_poster != "":
            self.picture_url = "http://www.cinematografo.it/bdcm/img/%s.JPG" % \
                tmp_poster
        else:
            self.picture_url=""
        
    def original_title(self):
        "Find the film's original title"
        self.original_title = string.strip(string.capwords \
            (gutils.strip_tags(gutils.trim(self.page, \
            "Titolo originale</font></p>", "</font></p>"))))
    
    def title(self):
        """Find the film's local title. 
        Probably the original title translation"""
        self.title = string.strip(\
            string.capwords(gutils.strip_tags(gutils.trim(self.page, \
            "Titolo Film</font></p>", "</font></strong></p>"))))
                
    def director(self):
        "Find the film's director"
        self.director = gutils.trim(self.page, \
            "Regia</font></p>", "</font></p>")
        self.director = string.replace(self.director, "<BR>", ", ")
        self.director = string.replace(self.director, "&nbsp;&nbsp;", "&nbsp;")
        self.director = gutils.strip_tags(self.director)
        self.director = string.strip(self.director)

    def plot(self):
        "Find the film's plot"
        self.plot = gutils.trim(self.page, \
            "Trama</font></p>", "</font></p>")
        
    def year(self):
        "Find the film's year"
        self.year = string.strip(gutils.trim(self.page, \
            "Anno</font></p>", "</font></p>"))
        
    def running_time(self):
        "Find the film's running time"
        self.running_time = string.strip(gutils.trim(self.page, \
            "Durata</font></p>", "</font></p>"))
            
    def genre(self):
        "Find the film's genre"
        self.genre = gutils.trim(self.page, "Genere</font></p>", \
            "</font></p>")
        self.genre = string.replace(self.genre, "<BR>", ", ")
        self.genre = string.capwords(string.strip(self.genre.decode \
            ('iso-8859-1')) )
        
    def with(self):
        "Find the actors. Try to make it comma separated."
        self.with = gutils.trim(self.page, \
            "Attori</font></p>", "</font></p>")
        self.with = string.replace(self.with, "<BR>", "\n")
        self.with = string.replace(self.with, \
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", _(" as "))
        self.with = string.replace(self.with, "&nbsp;&nbsp;", "&nbsp;")
    
    def classification(self):
        "Find the film's classification"
        self.classification = ""
        
    def studio(self):
        "Find the studio"
        self.studio = string.capwords(string.strip( \
            gutils.trim(self.page, \
            "Distribuzione</font></p>", "</font></p>")))
        
    def site(self):
        "Find the film's oficial site"
        self.site = ""
        
    def imdb(self):
        "Find the film's imdb details page"
        self.imdb = ""
        
    def trailer(self):
        "Find the film's trailer page or location"
        self.trailer = ""
        
    def country(self):
        "Find the film's country"
        self.country = string.strip(gutils.trim(self.page, \
            "Origine</font></p>", "</font></p>"))
        
    def rating(self):
        """Find the film's rating. From 0 to 10. 
        Convert if needed when assigning."""
        self.rating = 0
        
class SearchPlugin(movie.SearchMovie):
    "A movie search object"
    def __init__(self):
        self.original_url_search = \
            "http://www.cinematografo.it/bdcm/bancadati_query.asp?ty=CONTIENEPAROLE&R1=TI&I2.x=0&I2.y=0&fi="
        self.translated_url_search = \
            "http://www.cinematografo.it/bdcm/bancadati_query.asp?ty=CONTIENEPAROLE&R1=TI&I2.x=0&I2.y=0&fi="
        
    def search(self, parent_window):
        "Perform the web search"
        self.open_search(parent_window)
        self.sub_search()
        return self.page
        
    def sub_search(self):
        "Isolating just a portion (with the data we want) of the results"
        self.page = gutils.trim(self.page, \
            "td valign=\"top\" width=\"80%\" style=\"border-left:1px solid #999966\"", \
            "la ricerca effettuata aggiungendo:")
        
    def get_searches(self):
        "Try to find both id and film title for each search result"
        self.elements = string.split(self.page, "</br>")
        self.number_results = self.elements[-1]
        
        if (self.elements[0] != ''):
            for element in self.elements:
                self.ids.append(gutils.trim(element, "sch=", "\">"))
                self.titles.append(gutils.convert_entities \
                    (gutils.trim(element, "\t\t\t\t\t\t\t", "</b>")))    
        else:
            self.number_results = 0
