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

plugin_name = "Kino.de"
plugin_description = "KINO.DE"
plugin_url = "www.kino.de"
plugin_language = _("German")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.2"

class Plugin(movie.Movie):
	url_to_use = "http://www.kino.de/kinofilm.php4?"
	url_type = "K"

	def __init__(self, id):
		self.encode='iso-8859-1'
		elements = string.split(id, "_")
		self.movie_id = elements[1]
		if (elements[0] == "V"):
			self.url_to_use = "http://www.kino.de/videofilm.php4?"
			self.url_type = "V"
		else:
			self.url_to_use = "http://www.kino.de/kinofilm.php4?"
			self.url_type = "K"
		self.url = self.url_to_use + "typ=film&nr=" + str(self.movie_id)

	def initialize(self):
		if (gutils.trim(self.url, "typ=", "&") <> "film"):
			self.url = self.url_to_use + "typ=film&nr=" + str(self.movie_id)
			self.open_page(self.parent_window)
		self.tmp_page = gutils.trim(self.page, "<!-- PRINT-CONTENT-START-->", "<!-- PRINT-CONTENT-ENDE-->")
	
	def picture(self):
		if (self.url_type == "V"):
			self.picture_url = "http://www.kino.de/pix/MBBILDER/VIDEO/" + gutils.trim(self.tmp_page,"IMG SRC=\"/pix/MBBILDER/VIDEO/", "\"")
		else:
			self.picture_url = gutils.trim(self.tmp_page,"IMG SRC=\"/pix/MBBILDER/KINOPLAK/", "\"")
			if self.picture_url <> '':
				self.picture_url = "http://www.kino.de/pix/MBBILDER/KINOPLAK/" + self.picture_url
			else:
				self.picture_url = "http://www.kino.de/pix/MBBILDER/KINO/" + gutils.trim(self.tmp_page,"IMG SRC=\"/pix/MBBILDER/KINO/", "\"")

	def original_title(self):
		self.original_title = gutils.trim(self.page,"span CLASS=\"standardsmall\"><br>(",")<")

	def title(self):
		if (self.url_type == "V"):
			self.title = gutils.after(gutils.trim(self.page,"\"headline2\"><A HREF=\"/videofilm.php4?nr=", "</A>"), ">")
		else:
			self.title = gutils.after(gutils.trim(self.page,"\"headline2\"><A HREF=\"/kinofilm.php4?nr=", "</A>"), ">")

	def director(self):
		if (gutils.trim(self.url, "typ=", "&") <> "credits"):
			self.url = self.url_to_use + "typ=credits&nr=" + str(self.movie_id)
			self.open_page(self.parent_window)
		self.director = gutils.trim(self.page,"Regie","</a>")
		self.director = gutils.after(self.director,"mitwirk.php4")
		self.director = gutils.after(self.director,">")

	def plot(self):
		if (gutils.trim(self.url, "typ=", "&") <> "film"):
			self.url = self.url_to_use + "typ=film&nr=" + str(self.movie_id)
			self.open_page(self.parent_window)
		self.tmp_page = gutils.trim(self.page, "<!-- PRINT-CONTENT-START-->", "<!-- PRINT-CONTENT-ENDE-->")
		if (self.url_type == "V"):
			self.plot = gutils.after(self.tmp_page,"IMG SRC=\"/pix/MBBILDER/VIDEO")
			self.plot = gutils.trim(self.plot,"</TABLE>", "</TD>")
		else:
			self.plot = gutils.after(self.tmp_page,"IMG SRC=\"/pix/MBBILDER/KINOPLAK")
			self.plot = gutils.trim(self.plot,"</TABLE>", "</TD>")
			if self.plot == '':
				self.plot = gutils.trim(self.tmp_page, "BORDER=\"0\" align=\"left\" ><TR><TD>", "</TD>")

	def year(self):
		self.year = gutils.trim(self.page,"class=\"standardsmall\"><br><b>DVD</b> - <b>","<BR>")
		if self.year == "":
			self.year = gutils.trim(self.page,"class=\"standardsmall\"><b>","<BR>")
		self.year = gutils.trim(self.year,"<b>","</b>")
		self.year = gutils.after(self.year," ")

	def running_time(self):
		self.running_time = gutils.trim(self.page,"Jahren</b> - <b>"," Min.")
		if (self.running_time == ''):
			self.running_time = gutils.trim(self.page,"Jahren</b></b> - <b>"," Min.")
		if (self.running_time == ''):
			self.running_time = gutils.trim(self.page,"</b><BR><b>"," Min.")

	def genre(self):
		self.genre = gutils.trim(self.page,"class=\"standardsmall\"><br><b>DVD</b> - <b>","</b>")
		if self.genre == "":
			self.genre = gutils.trim(self.page,"class=\"standardsmall\"><b>","</b>")

	def with(self):
		if (gutils.trim(self.url, "typ=", "&") <> "credits"):
			self.url = self.url_to_use + "typ=credits&nr=" + str(self.movie_id)
			self.open_page(self.parent_window)
		self.with = gutils.trim(self.page,"</TD></TR><TR  CLASS=\"dbtreffer", "\n")
		self.with = gutils.after(self.with, "\">")
		self.with = self.with.replace("<TR  CLASS=\"dbtrefferlight\">", "\n")
		self.with = self.with.replace("<TR  CLASS=\"dbtrefferdark\">", "\n")
		self.with = self.with.replace("&nbsp;", "--flip--")
		self.with = gutils.clean(self.with)
		elements = self.with.split("\n")
		self.with = ''
		for element in elements:
			elements2 = element.split("--flip--")
			if len(elements2) > 1:
				self.with += elements2[1] + "--flip--" + elements2[0] + "\n"
			else:
				self.with = element
		self.with = string.replace(self.with, "--flip--", _(" as "))

	def classification(self):
		self.classification = gutils.trim(self.page,"FSK: ","</b>")

	def studio(self):
		self.studio = gutils.trim(self.page,"Verleih: ", "</b>")

	def site(self):
		self.site = ""

	def imdb(self):
		self.imdb = self.url_to_use + "nr=" + self.movie_id;

	def trailer(self):
		self.trailer = ""

	def country(self):
		self.country = gutils.trim(self.page,"class=\"standardsmall\"><br><b>DVD</b> - <b>","<BR>")
		if self.country == "":
			self.country = gutils.trim(self.page,"class=\"standardsmall\"><b>","<BR>")
		self.country = gutils.trim(self.country,"<b>","</b>")
		self.country = gutils.before(self.country," ")

	def rating(self):
		self.rating = 0

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search    = "http://www.kino.de/megasuche.php4?typ=filme&wort="
		self.translated_url_search    = "http://www.kino.de/megasuche.php4?typ=filme&wort="
		self.encode='iso-8859-1'

	def search(self,parent_window):
		self.open_search(parent_window)
		self.page = gutils.trim(self.page,"align=center><B>Kinofilm 1", "<!-- PRINT-CONTENT-ENDE-->");
		self.page = self.page.decode('iso-8859-1')
		if (self.page<>''):
			return self.page
		self.url = "http://www.kino.de/megasuche.php4?typ=video&wort="
		self.open_search(parent_window)
		self.page = gutils.trim(self.page,"align=center><B>Video/DVD 1", "<!-- PRINT-CONTENT-ENDE-->");
		self.page = self.page.decode('iso-8859-1')
		return self.page

	def get_searches(self):
		elements_tmp = string.split(self.page,"kinofilm.php4")

		if (elements_tmp[0]<>self.page):
			elements = string.split(self.page,"headline3\"><A HREF=\"/kinofilm.php4?nr=")
			if (elements[0]<>''):
				elements[0] = ''
				for element in elements:
					if (element <> ''):
						self.ids.append("K_" + gutils.before(element,"&"))
						self.titles.append(gutils.strip_tags(
							gutils.trim(element,">","</A>") + " " +
							gutils.trim(element, "<span CLASS=\"standardsmall\"><br>", "</SPAN>") + " (" +
							string.replace(
								gutils.trim(element, "<span class=\"standardsmall\"><b>", "</span>"), "<b>", ", ")
							+ ")"))
		else:
			elements_tmp2 = string.split(self.page, "videofilm.php4")
			if (elements_tmp2[0]<>self.page):
				elements = string.split(self.page,"headline3\"><A HREF=\"/videofilm.php4?nr=")
				if (elements[0]<>''):
					elements[0] = ''
					for element in elements:
						if (element <> ''):
							self.ids.append("V_" + gutils.before(element,"&"))
							self.titles.append(gutils.strip_tags(
								gutils.trim(element,">","</A>") + " " +
								gutils.trim(element, "<span CLASS=\"standardsmall\"><br>", "</SPAN>") + " (" +
								string.replace(
									gutils.trim(element, "<span class=\"standardsmall\"><b>", "</span>"), "<b>", ", ") + ")"))
