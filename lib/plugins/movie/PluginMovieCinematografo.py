# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2006 Vasco Nunes, Piotr Ożarowski
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
import gutils, movie, string

plugin_name = "Cinematografo"
plugin_description = "Rivista del Cinematografo dal 1928"
plugin_url = "www.cinematografo.it"
plugin_language = _("Italian")
plugin_author = "Vasco Nunes, Piotr Ożarowski"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version = "1.0"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.cinematografo.it/bancadati/consultazione/schedafilm.jsp?codice=%s" % str(self.movie_id)

	def picture(self):
		"Find the film's poster image"
		tmp_poster = gutils.trim(self.page, "../images_locandine/%s/"%self.movie_id, ".JPG\"")
		if tmp_poster != "":
			self.picture_url = "http://www.cinematografo.it/bancadati/images_locandine/%s/%s.JPG" % (self.movie_id, tmp_poster)
		else:
			self.picture_url=""

	def original_title(self):
		"Find the film's original title"
		self.original_title = gutils.trim(self.page, ">Titolo Originale</font>", "</tr>")
		self.original_title = string.capwords(self.original_title)

	def title(self):
		"""Find the film's local title.
		Probably the original title translation"""
		self.title = gutils.trim(self.page, "<!--TITOLO-->", "<!--FINE TITOLO-->")
		self.title = gutils.trim(self.title, "<b>", "</b>")
		self.title = string.capwords(self.title)

	def director(self):
		"Find the film's director"
		self.director = gutils.trim(self.page, ">Regia", "Attori<")
		self.director = self.director.replace("&nbsp;&nbsp;", "&nbsp;")
		self.director = gutils.strip_tags(self.director)
		self.director = string.strip(self.director)

	def plot(self):
		"Find the film's plot"
		self.plot = gutils.trim(self.page, "\"fontYellowB\">Trama</font>", "\n")

	def year(self):
		"Find the film's year"
		self.year = gutils.trim(self.page, ">Anno</font>", "</tr>")
		self.year = gutils.after(self.year, "\n                  ")
		self.year = gutils.before(self.year, "\n")

	def running_time(self):
		"Find the film's running time"
		self.running_time = gutils.trim(self.page, ">Durata</font>", "</tr>")
		self.running_time = gutils.after(self.running_time, "\n                  ")
		self.running_time = gutils.before(self.running_time, "\n")
		print self.running_time

	def genre(self):
		"Find the film's genre"
		self.genre = gutils.trim(self.page, ">Genere</font>", "</tr>").lower()

	def with(self):
		"Find the actors. Try to make it comma separated."
		self.with = gutils.trim(self.page, ">Attori</font>", "\n")
		self.with = string.replace(self.with, "target='_self'>", "\n>")
		self.with = string.replace(self.with, "&nbsp;&nbsp;", ' ')
		self.with = string.replace(self.with, "<a>",_(" as "))
		self.with = string.replace(self.with, "</tr><tr>", '\n')
		self.with = string.replace(self.with, "...vedi il resto del cast", '')

	def classification(self):
		"Find the film's classification"
		self.classification = ""

	def studio(self):
		"Find the studio"
		self.studio = string.capwords(gutils.trim(self.page, ">Distribuzione</font>", "</tr>"))

	def site(self):
		"Find the film's oficial site"
		self.site = ""

	def imdb(self):
		"Find the film's imdb details page"
		self.imdb = self.url

	def trailer(self):
		"Find the film's trailer page or location"
		self.trailer = ""

	def country(self):
		"Find the film's country"
		self.country = gutils.trim(self.page, ">Origine</font>", "</tr>")

	def rating(self):
		"""Find the film's rating. From 0 to 10.
		Convert if needed when assigning."""
		self.rating = 0

class SearchPlugin(movie.SearchMovie):
	"A movie search object"
	def __init__(self):
		self.encode='iso-8859-1'
		self.original_url_search = "http://www.cinematografo.it/bancadati/consultazione/trovatitoli.jsp?tipo=CONTIENEPAROLE&word="
		self.translated_url_search = self.original_url_search

	def search(self, parent_window):
		"Perform the web search"
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		"Isolating just a portion (with the data we want) of the results"
		self.page = gutils.trim(self.page, "<td valign=\"top\" width=\"73%\" bgcolor=\"#4d4d4d\">", "</td>")

	def get_searches(self):
		"Try to find both id and film title for each search result"
		elements = string.split(self.page, "<li>")
		self.number_results = elements[-1]

		if (elements[0] != ''):
			for element in elements:
				self.ids.append(gutils.trim(element, "?codice=", "\">"))
				self.titles.append(gutils.convert_entities(gutils.trim(element, "<b>", "</b>")))
		else:
			self.number_results = 0
