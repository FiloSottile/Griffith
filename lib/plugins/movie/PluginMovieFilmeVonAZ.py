# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006
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

plugin_name = "FilmeVonA-Z.de"
plugin_description = "FILMEvonA-Z.de"
plugin_url = "www.filmevona-z.de"
plugin_language = _("German")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.0"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert=" + str(self.movie_id)

	def picture(self):
		self.picture_url = "http://www.filmevona-z.de/" + gutils.trim(self.page,"ProductCover=", "\"")

	def original_title(self):
		self.original_title = string.capwords(gutils.after(gutils.trim(self.page, "sucheNach=titel", "(Orginaltitel)"), "\n			"))

	def title(self):
		self.title = gutils.after(gutils.trim(self.page, "sucheNach=titel", "</a>"), ">")

	def director(self):
		self.director = gutils.after(gutils.trim(self.page, "(Regie)","</a>"), ">")

	def plot(self):
		self.plot = gutils.trim(self.page, "\n						<p>", "</p>")

	def year(self):
		self.year = gutils.after(gutils.trim(self.page, "sucheNach=produktionsjahr", "</a>"), ">")

	def running_time(self):
		self.running_time = gutils.trim(self.page,"L&auml;nge: "," Minuten")

	def genre(self):
		elements = string.split(self.page, "sucheNach=genre")
		if (elements[0]<>''):
			elements[0] = ''
			self.delimiter = ''
			self.genre = ''
			for element in elements:
				if (element <> ''):
					self.genre += self.delimiter + gutils.trim(element, ">", "</a>")
					self.delimiter = ", "

	def with(self):
		self.with = gutils.trim(self.page, "(Darsteller)", "\n\n\n")
		self.with = gutils.clean(self.with)
		self.with = self.with.replace(" als ", _(" as "))
		self.with = self.with.replace("			", "")
		self.with = self.with.replace("\n", "")
		self.with = self.with.replace(", ", "\n")
		self.with = self.with.replace(",", "")

	def classification(self):
		self.classification = gutils.trim(self.page, "FSK: ", ";")

	def studio(self):
		self.studio = gutils.after(gutils.trim(self.page, "sucheNach=produktionsfirma", "</a>"), ">")

	def site(self):
		self.site = ""

	def imdb(self):
		self.imdb = "http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert=" + self.movie_id;

	def trailer(self):
		self.trailer = ""

	def country(self):
		self.country = gutils.after(gutils.trim(self.page, "sucheNach=produktionsland", "</a>"), ">")

	def rating(self):
		self.rating = 0

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.original_url_search	= "http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert="
		self.translated_url_search	= "http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert="
		self.encode='iso-8859-1'

	def search(self,parent_window):
		self.open_search(parent_window)
		self.page = gutils.trim(self.page,"Alle Treffer aus der Kategorie", "<!-- ENDE ErgebnissAusgabe -->");
		return self.page

	def get_searches(self):
		elements = string.split(self.page,"\n	<a href=\"filmsuche.cfm?wert=")
		if (elements[0]<>''):
			elements[0] = ''
			for element in elements:
				if (element <> ''):
					self.ids.append(gutils.before(element,"&"))
					self.titles.append(gutils.strip_tags(
						gutils.trim(element,">","</a>") + " (" +
						string.capwords(gutils.trim(element, "\n			", "(Orginaltitel)")) + ", " +
						gutils.after(gutils.trim(element, "sucheNach=produktionsland", "</a>"), ">") + ", " +
						gutils.after(gutils.trim(element, "sucheNach=produktionsjahr", "</a>"), ">") +
						")"))
