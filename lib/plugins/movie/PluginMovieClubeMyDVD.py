# -*- coding: iso-8859-1 -*-

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
import gutils
import movie
import string

plugin_name = "Clube MyDVD"
plugin_description = "A Melhor Forma de Alugar Filmes"
plugin_url = "www.clubemydvd.com"
plugin_language = _("Portuguese")
plugin_author = "Vasco Nunes"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version = "0.2"

class Plugin(movie.Movie):
	"""A movie plugin object"""
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.clubemydvd.com/film.php?id=" + str(self.movie_id)

	def picture(self):
		"""Finds the film's poster image"""
		self.picture_url = "http://www.clubemydvd.com/img/filmes/" + \
			str(self.movie_id) + "_big.jpg"

	def original_title(self):
		"""Finds the film's original title"""
		self.original_title = string.capwords \
			(gutils.trim(self.page, "<span class=\"txt1\">(", ")</span></nobr></td>"))

	def title(self):
		"""Finds the film's local title.
		Probably the original title translation"""
		self.title = string.capwords(gutils.trim(self.page, \
			"<nobr>&nbsp;<b>", "</b></nobr>"))

	def director(self):
		"""Finds the film's director"""
		self.director = gutils.trim(self.page, "<b>Realizador:</b> ", "</a></td>")
		self.director = string.replace(self.director, "\t", "")
		self.director = gutils.after(self.director, "\">")

	def plot(self):
		"""Finds the film's plot"""
		self.plot = gutils.trim(self.page, "<b>Sinopse:</b> ", "</td>")

	def year(self):
		"""Finds the film's year"""
		self.year = gutils.trim(self.page, "<b>Ano:</b> ", "</td>")

	def running_time(self):
		"""Finds the film's running time"""
		self.running_time = gutils.trim(self.page, "<b>Dura", " min.")
		self.running_time = gutils.after(self.running_time, "</b> ")

	def genre(self):
		"""Finds the film's genre"""
		self.genre = gutils.trim(self.page, "nero:</b> ", "</a>")

	def with(self):
		self.with = ""
		self.with = gutils.trim(self.page, "<b>Actores:</b> ", "</tr>")
		self.with = gutils.strip_tags(self.with)
		self.with = string.replace(self.with, ", ", "")
		self.with = string.replace(self.with, "\t\t\t\t ", "")

	def classification(self):
		"""Find the film's classification"""
		self.classification = gutils.trim(self.page, "<b>Idade:</b> ", "</td>")

	def studio(self):
		"""Find the studio"""
		self.studio = ""

	def site(self):
		"""Find the film's oficial site"""
		self.site = gutils.trim(self.page, \
			"5px;\"><a class=\"botao\"", "\" title=")
		self.site = string.replace(self.site,"href=\"","")

	def imdb(self):
		"""Find the film's imdb details page"""
		self.imdb = gutils.trim(self.page, \
			"Site Oficial</a> <a class=\"botao\" href=\"", "\" title=")

	def trailer(self):
		"""Find the film's trailer page or location"""
		self.trailer = ""

	def country(self):
		"""Find the film's country"""
		self.country = gutils.trim(self.page, "s origem:</b> ", "</a></td>")

	def rating(self):
		"""Find the film's rating. From 0 to 10.
		Convert if needed when assigning."""
		self.rating = ""

	def notes(self):
		"""Finds the film's notes"""
		self.notes = "Video: " + gutils.trim(self.page, "<b>Video:</b> ", "</td>")
		self.notes += "\nAudio: " + gutils.trim(self.page, "<b>Audio:</b> ", "</td>")
		self.notes += "\nLegendas: " + gutils.trim(self.page, "<b>Legendas:</b> ", "</td>")

class SearchPlugin(movie.SearchMovie):
	"""A movie search object"""
	def __init__(self):
		self.original_url_search = \
			"http://www.clubemydvd.com/filmes_search.php?search=1&titulo="
		self.translated_url_search = \
			"http://www.clubemydvd.com/filmes_search.php?search=1&titulo="
		self.encode='iso-8859-1'

	def search(self, parent_window):
		"""Perform the web search"""
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		"""Isolating just a portion (with the data we want) of the results"""
		self.page = gutils.trim(self.page, "Foram encontrados ", "<b>Dica:</b>")

	def get_searches(self):
		"""Try to find both id and film title for each search result"""
		elements = string.split(self.page, """<td>&nbsp;""")
		self.number_results = elements[-1]

		if (len(elements[0])):
			for element in elements:
				self.ids.append(gutils.trim(element, """<a href="film.php?id=""", "\""))
				self.titles.append( string.capwords(gutils.strip_tags(gutils.convert_entities \
					(gutils.trim(element, "<b>", "</nobr></td>")))))
		else:
			self.number_results = 0
