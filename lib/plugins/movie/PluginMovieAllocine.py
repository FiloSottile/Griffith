# -*- coding: UTF-8 -*-

__revision__ = '$Id: PluginMovieIMDB.py 176 2006-02-01 12:07:26Z iznogoud $'

# Copyright (c) 2005-2006 Vasco Nunes, Piotr Ozarowski
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, orprint
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

plugin_name = "Allocine"
plugin_description = "Internet Movie Database"
plugin_url = "www.allocine.fr"
plugin_language = _("French")
plugin_author = "Pierre-Luc Levy"
plugin_author_email = ""
plugin_version = "0.5"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=" + str(self.movie_id) + ".html"

	def picture(self):
		self.picture_url = gutils.trim(self.page,"Poster","Date de sor")
		self.picture_url = gutils.after(self.picture_url,"activerlientexte.inc")
		self.picture_url = gutils.trim(self.picture_url,"<img src=\"","\"")

	def original_title(self):
		self.original_title = ""
		self.original_title = gutils.trim(self.page,"Titre original : <i>","</i>")
		if (self.original_title==''):
			self.original_title = gutils.trim(self.page,"<title>","</title>")

	def title(self):
		self.title = gutils.trim(self.page,"<title>","</title>")

	def director(self):
		self.director = gutils.trim(self.page,"<h4>Réalisé par ","</a></h4>")

	def plot(self):
		self.plot = gutils.trim(self.page,"Synopsis</b></h3></td></tr></table>","</h4>")
		self.plot = gutils.after(self.plot,"<h4>")

	def year(self):
		self.year = gutils.trim(self.page,"Année de production : ","</h4>")

	def running_time(self):
		self.running_time = ""
		self.running_time = gutils.trim(self.page,"<h4>Durée : ","min.</h4>&nbsp;")
		if self.running_time:
			self.running_time = str (int(gutils.before(self.running_time,"h"))*60 + int(gutils.after(self.running_time,"h")))

	def genre(self):
		self.genre = gutils.trim(self.page,"<h4>Genre : ","</h4>")
		self.genre = gutils.strip_tags(self.genre)

	def with(self):
		self.with = ""
		self.with = gutils.trim(self.page,"<h4>Avec ","</h4>")
		self.with = gutils.strip_tags(self.with)
		self.with = string.replace(self.with,", ", "\n")

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

	def rating(self):
		self.rating = gutils.trim(self.page, "Spectateurs</a> ", "</h4>")
		self.rating = gutils.trim(self.rating, "etoile_", ".gif")
		if self.rating:
			self.rating = str(float(int(self.rating)*2.25))

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search	= "http://www.allocine.fr/recherche/?motcle="
		self.translated_url_search	= "http://www.allocine.fr/recherche/?motcle="

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		self.page = gutils.trim(self.page,"Recherche : <b>", "<h3><b>Articles <h4>");

	def get_searches(self):
		elements = string.split(self.page,"<td colspan=\"2\" height=\"1\" valign=\"top\"><hr /></td>")
		if (elements[0]<>''):
			for element in elements:
				self.ids.append(gutils.trim(element,"/film/fichefilm_gen_cfilm=",".html"))
				self.titles.append(gutils.strip_tags(gutils.convert_entities(gutils.trim(element,"link1\">","</a>"))))
