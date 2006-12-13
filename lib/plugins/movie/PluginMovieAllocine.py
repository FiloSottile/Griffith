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
plugin_version = "0.6"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=%s.html" % str(self.movie_id)

	def get_image(self):
		self.image_url = gutils.trim(self.page,"Poster","Date de sor")
		self.image_url = gutils.after(self.image_url,"activerlientexte.inc")
		self.image_url = gutils.trim(self.image_url,"<img src=\"","\"")

	def get_o_title(self):
		self.o_title = ""
		self.o_title = gutils.trim(self.page,"Titre original : <i>","</i>")
		if (self.o_title==''):
			self.o_title = gutils.trim(self.page,"<title>","</title>")

	def get_title(self):
		self.title = gutils.trim(self.page,"<title>","</title>")

	def get_director(self):
		self.director = gutils.trim(self.page,"<h4>Réalisé par ","</a></h4>")

	def get_plot(self):
		self.plot = gutils.trim(self.page,"Synopsis</b></h3></td></tr></table>","</h4>")
		self.plot = gutils.after(self.plot,"<h4>")

	def get_year(self):
		self.year = gutils.trim(self.page,"Année de production : ","</h4>")

	def get_runtime(self):
		self.runtime = ""
		self.runtime = gutils.trim(self.page,"<h4>Durée : ","min.</h4>&nbsp;")
		if self.runtime:
			self.runtime = str (int(gutils.before(self.runtime,"h"))*60 + int(gutils.after(self.runtime,"h")))

	def get_genre(self):
		self.genre = gutils.trim(self.page,"<h4>Genre : ","</h4>")
		self.genre = gutils.strip_tags(self.genre)

	def get_cast(self):
		self.cast = ""
		self.cast = gutils.trim(self.page,"<h4>Avec ","</h4>")
		self.cast = gutils.strip_tags(self.cast)
		self.cast = string.replace(self.cast,", ", "\n")

	def get_image(self):
		self.classification = ""

	def get_studio(self):
		self.studio = ""

	def get_o_site(self):
		self.o_site = ""

	def get_site(self):
		self.site = "http://www.allocine.fr/film/fichefilm_gen_cfilm=%s.html" % self.movie_id

	def get_trailer(self):
		self.trailer = "http://www.allocine.fr/film/video_gen_cfilm=%s.html" % self.movie_id

	def get_country(self):
		self.country = gutils.trim(self.page,"<h4>Film ",".</h4>&nbsp;")

	def get_rating(self):
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
