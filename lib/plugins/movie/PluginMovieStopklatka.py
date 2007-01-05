# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Piotr Ożarowski
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
import movie,string

plugin_name         = 'Stopklatka'
plugin_description  = 'Internetowy Serwis Filmowy'
plugin_url          = 'www.stopklatka.pl'
plugin_language     = _('Polish')
plugin_author       = 'Piotr Ożarowski'
plugin_author_email = '<ozarow+griffith@gmail.com>'
plugin_version      = '1.7'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.url = "http://www.stopklatka.pl/film/film.asp?fi=%s" % str(self.movie_id)
		self.encode = 'iso-8859-2' # with some cp-1250 data (sic!)

	def initialize(self):
		self.page = self.page.replace('\x9c','ś')
		self.page = self.page.replace('š','ą')

	def get_image(self):
		self.image_url = gutils.trim(self.page,"http://img.stopklatka.pl/film/","' border=1")
		self.image_url = 'http://img.stopklatka.pl/film/' + self.image_url

	def get_o_title(self):
		self.o_title = gutils.trim(self.page,"<h2>(",")</h2>")
		if self.o_title == '':
			self.o_title = self.get_title(True)

	def get_title(self, ret=False):
		data = gutils.trim(self.page,"<i><h1>","</h1>")
		if ret is True:
			return data
		else:
			self.title = data

	def get_director(self):
		self.director = gutils.trim(self.page,">re\xbfyseria:<","</font>")
		self.director = gutils.after(self.director,"<b>")
		self.director = gutils.strip_tags(self.director)

	def get_plot(self):
		self.plot = gutils.trim(self.page,"class='zdjecie'","</font></td></tr>")
		self.plot = gutils.after(self.plot,"\"text2\">")

	def get_year(self):
		self.year = gutils.trim(self.page,">rok produkcji:<","</b>")
		self.year = gutils.after(self.year,"<b>")

	def get_runtime(self):
		self.runtime = gutils.trim(self.page,"trwania:<"," min</b>")
		self.runtime = gutils.after(self.runtime,"<b>")

	def get_genre(self):
		self.genre = gutils.trim(self.page,">gatunek:<","</b>")
		self.genre = gutils.after(self.genre,"<b>")

	def get_cast(self):
		self.cast = gutils.trim(self.page,">obsada:</font>","</font>")
		self.cast = gutils.after(self.cast,"<b>")
		self.cast = string.replace(self.cast,", ", "\n")
		self.cast = string.strip(gutils.strip_tags(self.cast))
		pos = string.find(self.cast, 'Więcej &gt;')
		if pos > 0:
			self.cast = self.cast[0:pos]

	def get_classification(self):
		self.classification = ""

	def get_studio(self):
		self.studio = ""

	def get_o_site(self):
		self.o_site = gutils.trim(self.page,">strona oficjalna:<"," target=_blank")
		self.o_site = gutils.after(self.o_site,"href=")

	def get_site(self):
		self.site = self.url

	def get_trailer(self):
		self.trailer = "http://www.stopklatka.pl/film/film.asp?fi=" + self.movie_id + "&sekcja=mmedia"

	def get_country(self):
		self.country = gutils.trim(self.page,">kraj:<","</b>")
		self.country = gutils.after(self.country,"<b>")

	def get_rating(self):
		self.rating = "0"

	def get_notes(self):
		self.notes = ''

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode='iso-8859-2'
		self.original_url_search	= "http://www.stopklatka.pl/szukaj/szukaj.asp?kategoria=film&szukaj="
		self.translated_url_search	= "http://www.stopklatka.pl/szukaj/szukaj.asp?kategoria=film&szukaj="

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		self.page = gutils.trim(self.page,"<blockquote>", "</blockquote>");
		self.page = self.page.replace('\x9c','ś')
		self.page = self.page.replace('š','ą')

	def get_searches(self):
		elements = string.split(self.page,"<li>")
		self.number_results = elements[-1]

		if (elements[0]<>''):
			for element in elements:
				self.ids.append(gutils.trim(element,"/film/film.asp?fi=","\"><b>"))
				self.titles.append(gutils.convert_entities(gutils.trim(element,"<b>","</b></a>")))
		else:
			self.number_results = 0
