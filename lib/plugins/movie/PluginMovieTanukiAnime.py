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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import movie,string

plugin_name = "Tanuki-Anime"
plugin_description = "Dawniej Wszechbiblia Anime"
plugin_url = "anime.tanuki.pl"
plugin_language = _("Polish")
plugin_author = "Piotr Ozarowski"
plugin_author_email = "<ozarow@gmail.com>"
plugin_version = "1.1"

class Plugin(movie.Movie):
	def __init__(self, id):
		if str(id).find("http://") != -1:
			self.movie_id = "TA"
			self.url = str(id)
		else:
			self.movie_id = str(id)
			self.url = "http://anime.tanuki.pl/strony/anime/"+str(id)
		self.encode='UTF-8'

	def picture(self):
		# TODO: move it to __init__
		if self.movie_id == "TA":
			self.movie_id = gutils.trim(self.page, "\"><a href=\"/strony/anime/", "/oceny")
			self.url = "http://anime.tanuki.pl/strony/anime/" + self.movie_id

		self.picture_url = gutils.trim(self.page,"<img src=\"/screens/","<br />")
		self.picture_url = gutils.before(self.picture_url,"\"")
		self.picture_url = "http://anime.tanuki.pl/screens/" + self.picture_url

	def original_title(self):
		self.original_title = gutils.trim(self.page, "<h3 class=\"animename\"", "</h3>")
		self.original_title = gutils.after(self.original_title, ">")

	def title(self):
		self.title = self.original_title

	def director(self):
		self.director = gutils.trim(self.page, "<th scope=\"row\">Reżyser:</th>\n\t<td>","</td>")

	def plot(self):
		self.plot = gutils.trim(self.page, "<div class=\"copycat\">\n", "</div>")

	def year(self):
		self.year = gutils.trim(self.page,"<div class=\"sitem\">Rok wydania: <","</a>")
		self.year = gutils.after(self.year,">")

	def running_time(self):
		self.running_time = gutils.trim(self.page,"<div class=\"sitem\">Czas trwania: <b>\n\t\t","\n</b>")
		if self.running_time.find("?") != -1:
			self.running_time = ''
		else:
			self.running_time = gutils.after(self.running_time, "×")
			self.running_time = gutils.before(self.running_time, " min")

	def genre(self):
		self.genre = gutils.trim(self.page,"<div class=\"sitem\">Gatunki:\n\t\t","</div>")
		self.genre = string.replace(self.genre, "\t\t"," ")

	def with(self):
		self.with = ''

	def classification(self):
		self.classification = ''

	def studio(self):
		self.studio = gutils.trim(self.page, "<th scope=\"row\">Studio:</th>\n\t<td>\n", "\t</td>")

	def site(self):
		self.site = ''

	def imdb(self):
		self.imdb = self.url

	def trailer(self):
		self.trailer = ''

	def country(self):
		self.country = ''

	def rating(self):
		self.rating = gutils.trim(self.page," alt=\"Ocena ","/10")

	def notes(self):
		self.notes = "Czas trwania: " + gutils.trim(self.page,"<div class=\"sitem\">Czas trwania: <b>\n\t\t","\n</b>") + '\n'

		t = self.page.find("<tr><th scope=\"row\">Autor:</th>")
		if t != -1:
			self.notes += "Autor: " + gutils.trim(self.page[t:], "<td>\n", "\t</td>") + '\n'

		t = self.page.find("<th scope=\"row\">Projekt:</th>")
		if t != -1:
			self.notes += "Projekt: " + gutils.trim(self.page[t:], "<td>\n", "\t</td>") + '\n'

		t = self.page.find("<tr><th scope=\"row\">Scenariusz:</th>")
		if t != -1:
			self.notes += "Scenariusz: " + gutils.trim(self.page[t:], "<td>\n", "\t</td>") + '\n'

		t = self.page.find("<th scope=\"row\">Muzyka:</th>")
		if t != -1:
			self.notes += "Muzyka: " + gutils.trim(self.page[t:], "<td>\n", "\t</td>") + '\n'

		self.notes += '\n' + gutils.trim(self.page,"<p class=\"dwazdania\">\n\t\t", "\n</p>")

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode='UTF-8'
		self.original_url_search   = "http://anime.tanuki.pl/strony/anime/lista/title/1/?&title="
		self.translated_url_search = "http://anime.tanuki.pl/strony/anime/lista/title/1/?&title="

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		tmp = string.find(self.page,"<table class=\"animelist strippedlist\"")
		if tmp == -1:	# only one match!
			self.page = ''
		else:		# multiple matches
			self.page = gutils.trim(self.page,"<table class=\"animelist strippedlist\"", "</tbody>");
			self.page = gutils.after(self.page, "<tbody>")

	def get_searches(self):
		if self.page == '':	# immidietly redirection to movie page
			self.number_results = 1
			self.ids.append(self.url)
			self.titles.append(gutils.convert_entities(self.title))
		else:			# multiple matches
			elements = string.split(self.page,"<tr")
			self.number_results = elements[-1]
			if (elements[0]<>''):
				for element in elements:
					self.ids.append(gutils.trim(element,"href=\"/strony/anime/","\" >"))
					element = gutils.after(element," >\n\t")
					element = element.replace("</a>\n\t</td>\n", " (")
					element = element.replace("\t<td>", "")
					element = element.replace("</td>\n", "; ")
					element = element.replace("</tr>", "")
					element = element[:len(element)-3] + ')'
					self.titles.append(element)
			else:
				self.number_results = 0

# vim: encoding=iso-8859-2
