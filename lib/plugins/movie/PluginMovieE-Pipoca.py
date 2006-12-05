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

plugin_name = "E-Pipoca"
plugin_description = "E-Pipoca Brasil"
plugin_url = "epipoca.cidadeinternet.com.br"
plugin_language = _("Brazilian Portuguese")
plugin_author = "Vasco Nunes"
plugin_author_email="<vasco.m.nunes@gmail.com>"
plugin_version = "0.2"

class Plugin(movie.Movie):
	"A movie plugin object"
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://epipoca.cidadeinternet.com.br/filmes_zoom.cfm?id=" + str(self.movie_id)

	def picture(self):
		"Find the film's poster image"
		tmp_pic = gutils.trim(self.page, "/images/filmes/capa_", "\"")
		self.picture_url = \
			"http://epipoca.cidadeinternet.com.br/images/filmes/capa_" + tmp_pic

	def original_title(self):
		"Find the film's original title"
		self.original_title = string.capwords(gutils.trim(self.page, "</font><br>(<i>", "</i>, "))

	def title(self):
		"""Find the film's local title.
		Probably the original title translation"""
		self.title = gutils.trim(self.page, "'votar');\">", "</b></font><br>(")

	def director(self):
		"Find the film's director"
		self.director = gutils.trim(self.page, "<b>Diretor(es)</b>:", "</a>  <br>")

	def plot(self):
		"Find the film's plot"
		self.plot = gutils.trim(self.page, "<b>Sinopse</b><br>", "</td></tr></table>")

	def year(self):
		"Find the film's year"
		self.year = gutils.trim(self.page, "</i>, ", ")<br><img")
		self.year = gutils.after(self.year,", ")

	def running_time(self):
		"Find the film's running time"
		self.running_time = gutils.trim(self.page, "<br> <b>Dura", " min<br>")
		self.running_time = self.running_time[9:]

	def genre(self):
		"Find the film's genre"
		self.genre = gutils.trim(self.page, "nero</b>: ", "<br>")

	def with(self):
		"Find the actors. Try to make it comma separated."
		self.with = ""
		self.with = gutils.trim(self.page, "<b>Elenco:</b>", "<b>mais...</b>")
		self.with = gutils.strip_tags(self.with)
		self.with = self.with[:-2]

	def classification(self):
		"Find the film's classification"
		self.classification = ""

	def studio(self):
		"Find the studio"
		self.studio = gutils.trim(self.page, "<b>Distribuidora</b>: ", "<br> <b>")

	def site(self):
		"Find the film's oficial site"
		self.site = gutils.trim(self.page, "<A HREF='", \
			"' TARGET=_blank><IMG SRC='/imagens/bf_siteoficial.gif'")

	def imdb(self):
		"Find the film's imdb details page"
		self.imdb = gutils.trim(self.page, \
			"/imagens/bf_siteoficial.gif' WIDTH=89 HEIGHT=18 BORDER=0 ALT=''>", \
			"' TARGET=_blank><IMG SRC='/imagens/bf_imdb.gif'")
		self.imdb = gutils.after(self.imdb, "<A HREF='")
		self.imdb = string.replace(self.imdb, "'", "")

	def trailer(self):
		"Find the film's trailer page or location"
		self.trailer = gutils.trim(self.page, "onclick=\"popup('/", "', 600, 400,")
		if self.trailer:
			self.trailer = "http://epipoca.cidadeinternet.com.br/" + self.trailer

	def country(self):
		"Find the film's country"
		self.country = gutils.trim(self.page, "</i>, ", ", ")

	def rating(self):
		"""Find the film's rating. From 0 to 10.
		Convert if needed when assigning."""
		tmp_rating = gutils.trim(self.page, "<font size=\"3\"><b> ", "</b></font><br>")
		if tmp_rating <> "":
			tmp_rating = string.replace(tmp_rating,',','.')
			self.rating = str( float(string.strip(tmp_rating)) )
		else:
			self.rating = ""

class SearchPlugin(movie.SearchMovie):
	"A movie search object"
	def __init__(self):
		self.original_url_search = \
			"http://epipoca.cidadeinternet.com.br/search/?Ordenado=Popular&busca="
		self.translated_url_search = \
			"http://epipoca.cidadeinternet.com.br/search/?Ordenado=Popular&busca="
		self.encode='iso-8859-1'

	def search(self, parent_window):
		"Perform the web search"
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		"Isolating just a portion (with the data we want) of the results"
		self.page = gutils.trim(self.page, \
			"<tr><td valign=\"top\" width=\"100%\">", "&nbsp;&nbsp;<b>Resu")

	def get_searches(self):
		"Try to find both id and film title for each search result"
		elements = string.split(self.page, "<td valign=\"bottom\">&nbsp;</td>")
		self.number_results = elements[-1]

		if (elements[0] != ''):
			for element in elements:
				self.ids.append(gutils.trim(element, "<b><a href=\"/filmes_zoom.cfm?id=", "\"><font size=\"2\""))
				self.titles.append(gutils.convert_entities \
					(gutils.trim(element, "color=\"FF8000\">", "</font></a></b></a><br>") ))
		else:
			self.number_results = 0
