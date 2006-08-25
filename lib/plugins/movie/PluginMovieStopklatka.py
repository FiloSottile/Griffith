# -*- coding: iso-8859-2 -*-
__revision__ = '$Id$'
# Copyright (c) 2005 Piotr Ozarowski
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

plugin_name = "Stopklatka"
plugin_description = "Internetowy Serwis Filmowy"
plugin_url = "www.stopklatka.pl"
plugin_language = _("Polish")
plugin_author = "Piotr Ozarowski"
plugin_author_email = "<ozarow@gmail.com>"
plugin_version = "1.5"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.url = "http://www.stopklatka.pl/film/film.asp?fi=" + str(self.movie_id)
		self.encode='iso-8859-2'

	def initialize(self):
		self.page = self.page.replace('\x9c','ś')
		self.page = self.page.replace('š','ą')

	def picture(self):
		self.picture_url = gutils.trim(self.page,"http://img.stopklatka.pl/film/","' border=1")
		self.picture_url = 'http://img.stopklatka.pl/film/' + self.picture_url

	def original_title(self):
		self.original_title = gutils.trim(self.page,"<h2>(",")</h2>")

	def title(self):
		self.title = gutils.trim(self.page,"<i><h1>","</h1>")
		if self.original_title == "":
			self.original_title = self.title

	def director(self):
		self.director = gutils.trim(self.page,">reżyseria:<","</font>")
		self.director = gutils.after(self.director,"<b>")
		self.director = gutils.strip_tags(self.director)

	def plot(self):
		self.plot = gutils.trim(self.page,"class='zdjecie'","</font></td></tr>")
		self.plot = gutils.after(self.plot,"\"text2\">")

	def year(self):
		self.year = gutils.trim(self.page,">rok produkcji:<","</b>")
		self.year = gutils.after(self.year,"<b>")

	def running_time(self):
		self.running_time = gutils.trim(self.page,"trwania:<"," min</b>")
		self.running_time = gutils.after(self.running_time,"<b>")

	def genre(self):
		self.genre = gutils.trim(self.page,">gatunek:<","</b>")
		self.genre = gutils.after(self.genre,"<b>")

	def with(self):
		self.with = gutils.trim(self.page,">obsada:</font>","</font>")
		self.with = gutils.after(self.with,"<b>")
		self.with = string.replace(self.with,", ", "\n")
		self.with = string.strip(gutils.strip_tags(self.with))
		pos = string.find(self.with,"Więcej &gt;")
		if pos > 0:
			self.with = self.with[0:pos]

	def classification(self):
		self.classification = ""

	def studio(self):
		self.studio = ""

	def site(self):
		self.site = gutils.trim(self.page,">strona oficjalna:<"," target=_blank")
		self.site = gutils.after(self.site,"href=")

	def imdb(self):
		self.imdb = self.url

	def trailer(self):
		self.trailer = "http://www.stopklatka.pl/film/film.asp?fi=" + self.movie_id + "&sekcja=mmedia"

	def country(self):
		self.country = gutils.trim(self.page,">kraj:<","</b>")
		self.country = gutils.after(self.country,"<b>")

	def rating(self):
		self.rating = "0"

	def notes(self):
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
# vim: encoding=iso-8859-2
