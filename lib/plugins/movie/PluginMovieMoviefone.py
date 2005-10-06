# -*- coding: UTF-8 -*-

# $Id: PluginMovieMoviefone.py,v 1.1 2005/09/18 14:37:08 iznogoud Exp $

# Copyright (c) 2005 Vasco Nunes
# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import movie,string

plugin_name = "Moviefone"
plugin_description = "A Service of America Online"
plugin_url = "movies.aol.com"
plugin_language = _("English")
plugin_author = "Vasco Nunes"
plugin_version = "0.1"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.url = "http://movies.aol.com/movie/main.adp?_pgtyp=pdct&mid=" + str(self.movie_id)
		
	def picture(self):
		self.picture_url = gutils.trim(self.page,"http://cdn.channel.aol.com/amgvideo/dvd/cov150/",".jpg")
		self.picture_url = "http://cdn.channel.aol.com/amgvideo/dvd/cov150/" + self.picture_url + ".jpg"
		
	def original_title(self):
		self.original_title = string.capwords(gutils.trim(self.page,"<title>Moviefone: ","</title>") )
	
	def title(self):
		self.title = self.original_title		
				
	def director(self):
		self.director = gutils.trim(self.page,"<strong>Directed By:</strong> ","<br />")
		self.director = string.strip(gutils.strip_tags(self.director))	
					
	def plot(self):
		self.plot = gutils.trim(self.page,"<strong>Synopsis:</strong> ","<br />")
		self.plot = string.strip(gutils.strip_tags(self.plot))
		
	def year(self):
		self.year = gutils.trim(self.page,"<strong>DVD Release Date:</strong> ","<br />")
		self.year = self.year[-4:]
		
	def running_time(self):
		self.running_time = gutils.trim(self.page,"<strong>Run Time:</strong> "," min.<br />") 
		
	def genre(self):
		self.genre = gutils.trim(self.page,"<strong>Genre:</strong> ","<br />")
		
	def with(self):
		self.with = gutils.trim(self.page,"<strong>Starring:</strong> ","<br />")
		self.with = string.strip(gutils.strip_tags(self.with))	
		
	def classification(self):
		self.classification = gutils.trim(self.page,"<strong>Rating:</strong> ","<br />")
		
	def studio(self):
		self.studio = gutils.trim(self.page,"<strong>Released By:</strong> ","<br />")
		
	def site(self):
		self.site = ""
		
	def imdb(self):
		self.imdb = ""
		
	def trailer(self):
		self.trailer = gutils.trim(self.page,"""onclick="setTrailerOmni();window.open('""", \
			"','_dlplayer'")
		
	def country(self):
		self.country = ""

	def rating(self):
		self.rating = ""
		 			
class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search	= "http://movies.aol.com/search/dvdresults.adp?query=";
		self.translated_url_search	= "http://movies.aol.com/search/dvdresults.adp?query=";
		
	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page
		
	def sub_search(self):
		self.page = gutils.trim(self.page,"--start LT_MultiColumn_1.0 module-->", """<div class="pagnationleft">Results   """)
		
	def get_searches(self):
		self.elements = string.split(self.page,"</br>")
		self.number_results = self.elements[-1]
		
		if (self.elements[0]<>''):
			for element in self.elements:
				self.ids.append(gutils.trim(element,"26mid%3d","\">"))
				self.titles.append(gutils.convert_entities(gutils.trim(element,(gutils.trim(element,"26mid%3d","\">"))+"\">","""</a></span>""")))	
		else:
			self.number_results = 0
