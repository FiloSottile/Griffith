# -*- coding: UTF-8 -*-

__revision__ = '$Id: PluginMovie7arte.py 478 2006-12-05 21:14:51Z piotrek $'

# Copyright (c) 2005-2006 Vasco Nunes, Piotr Ozarowski
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

plugin_name = "Cineteka"
plugin_description = "O seu Clube de Video Online"
plugin_url = "cineteka.com"
plugin_language = _("Portuguese")
plugin_author = "Vasco Nunes"
plugin_author_email = "<vasco.m.nunes@gmail.com>"
plugin_version = "0.2"

class Plugin(movie.Movie):
	"""A movie plugin object"""
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.cineteka.com/index.php?op=Movie&id=" + str(self.movie_id)

	def get_image(self):
		"""Finds the film's poster image"""
		self.image_url = "http://www.cineteka.com/img/filmes/" + str(self.movie_id) + "_big.jpg"

	def get_o_title(self):
		"""Finds the film's original title"""
		self.o_title = string.capwords(gutils.trim(self.page, """<nobr><span class="txt11">(""", ")"))

	def get_title(self):
		"""Finds the film's local title.
		Probably the original title translation"""
		self.title = string.capwords(gutils.trim(self.page, """<td class="txt12"><b>""", "</b>"))

	def get_director(self):
		"""Finds the film's director"""
		self.director = gutils.strip_tags(gutils.trim(self.page, "<td><b>Realizador:</b>", "</a></td>"))

	def get_plot(self):
		"""Finds the film's plot"""
		self.plot = gutils.trim(self.page, "<b>Sinopse:</b> ", "</div>")

	def get_year(self):
		"""Finds the film's year"""
		self.year = gutils.trim(self.page, "<td><b>Ano:</b> ", "</td>")

	def get_runtime(self):
		"""Finds the film's running time"""
		self.runtime = gutils.trim(self.page, "<td><b>Duração:</b> ", " min.</td>")

	def get_genre(self):
		"""Finds the film's genre"""
		self.genre = gutils.strip_tags(gutils.trim(self.page, "<b>Género:</b> ", "</td>"))

	def get_cast(self):
		self.cast = gutils.strip_tags(gutils.trim(self.page, "<b>Elenco:</b> ", "</td>"))
		self.cast = string.replace(self.cast, ", ", "")
		self.cast = string.replace(self.cast, "\t", "")
		self.cast = string.replace(self.cast, "\n ", "\n")

	def get_classification(self):
		"""Find the film's classification"""
		self.classification = gutils.trim(self.page, "<td><b>Idade:</b> ", "</td>")

	def get_studio(self):
		"""Find the studio"""
		self.studio = ""

	def get_o_site(self):
		"""Find the film's oficial site"""
		self.o_site = gutils.trim(self.page, \
			"<a class=\"button\" href=\"", \
			"""" title="Site Oficial""")

	def get_site(self):
		"""Find the film's imdb details page"""
		self.site = gutils.trim(self.page, \
			"</td><td><a class=\"button\" href=\"", \
			"""" title="Consultar título""")

	def get_trailer(self):
		"""Find the film's trailer page or location"""
		self.trailer = ""

	def get_country(self):
		"""Find the film's country"""
		self.country = gutils.trim(self.page, "<td><b>País:</b> ", "</td>")

	def get_rating(self):
		"""Find the film's rating. From 0 to 10.
		Convert if needed when assigning."""
		self.rating = 0

class SearchPlugin(movie.SearchMovie):
	"""A movie search object"""
	def __init__(self):
		self.original_url_search = "http://www.cineteka.com/index.php?op=MovieSearch&s="
		self.translated_url_search = self.original_url_search
		self.encode='iso-8859-1'

	def search(self, parent_window):
		"""Perform the web search"""
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		"""Isolating just a portion (with the data we want) of the results"""
		self.page = gutils.trim(self.page, \
			"""ordenados por data de aquisição:</div>""", """<div style="margin-top: 10px; text-align: center;"></div>""")

	def get_searches(self):
		"""Try to find both id and film title for each search result"""
		elements = string.split(self.page, "</a>]</td>")
		self.number_results = elements[-1]

		if (len(elements[0])):
			for element in elements:
				self.ids.append(gutils.trim(element, "?op=Movie&id=", "\""))
				self.titles.append(gutils.strip_tags(gutils.convert_entities \
					(gutils.trim(element, """<td class="txt12"><b>""", "</span></nobr></td>"))))
		else:
			self.number_results = 0

