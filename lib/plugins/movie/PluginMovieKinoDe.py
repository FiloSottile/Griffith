# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2007
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
plugin_version = "1.6"

class Plugin(movie.Movie):
	url_to_use = "http://www.kino.de/kinofilm/"
	url_type = "K"

	def __init__(self, id):
		self.encode='iso-8859-1'
		elements = string.split(id, "_")
		self.movie_id = elements[1]
		if (elements[0] == "V"):
			self.url_to_use = "http://www.kino.de/videofilm/"
			self.url_type = "V"
		else:
			self.url_to_use = "http://www.kino.de/kinofilm/"
			self.url_type = "K"
		self.url = self.url_to_use + str(self.movie_id)

	def initialize(self):
		self.tmp_page = gutils.trim(self.page, "<!-- PRINT-CONTENT-START-->", "<!-- PRINT-CONTENT-ENDE-->")
		self.url = self.url_to_use + string.replace(str(self.movie_id), '/', '/credits/')
		self.open_page(self.parent_window)
		self.tmp_creditspage = gutils.trim(self.page, "<!-- PRINT-CONTENT-START-->", "<!-- PRINT-CONTENT-ENDE-->")
		self.url = self.url_to_use + string.replace(str(self.movie_id), "/", "/features/")
		self.open_page(self.parent_window)
		self.tmp_dvdfeaturespage = gutils.trim(self.page, "<!-- PRINT-CONTENT-START-->", "<!-- PRINT-CONTENT-ENDE-->")

	def get_image(self):
		# first, try to get the second picture before the JavaScript block (it should be the original poster)
		# if there is no second picture, use the first picture (it should be a picture from the film)
		self.image_url = "http://images.kino.de/flbilder/" + gutils.trim(gutils.after(gutils.before(self.tmp_page, "<script language="), "img src=\"http://images.kino.de/flbilder/"),"img src=\"http://images.kino.de/flbilder/", "\"")
		if (self.image_url == "http://images.kino.de/flbilder/"):
			self.image_url = "http://images.kino.de/flbilder/" + gutils.trim(self.tmp_page,"img src=\"http://images.kino.de/flbilder/", "\"")

	def get_o_title(self):
		self.o_title = gutils.trim(self.tmp_page,"span class=\"standardsmall\"><br />(",")<")
		if (self.plot == ""):
			self.o_title = self.title

	def get_title(self):
		if (self.url_type == "V"):
			self.title = gutils.after(gutils.trim(self.tmp_page,"\"headline2\"><a href=\"http://www.kino.de/videofilm", "</a>"), ">")
		else:
			self.title = gutils.after(gutils.trim(self.tmp_page,"\"headline2\"><a href=\"http://www.kino.de/kinofilm", "</a>"), ">")
		if (self.o_title == ""):
			self.o_title = self.title

	def get_director(self):
		self.director = gutils.trim(self.tmp_creditspage,"Regie","</a>")
		self.director = gutils.after(self.director,"/star/")
		self.director = gutils.after(self.director,">")

	def get_plot(self):
		# little steps to perfect plot (I hope ... it's a terrible structured content ... )
		self.plot = gutils.trim(self.tmp_page,"Kurzinfo", "</td></tr><tr><td></td></tr><tr>")
		if (self.plot == ""):
			self.plot = gutils.trim(self.tmp_page,"Kurzinfo", "<script language=\"JavaScript\">")
		self.plot = gutils.after(self.plot, "Fotoshow</A>")
		self.plot = gutils.after(self.plot, "Filmpreise</A>")
		self.plot = gutils.after(self.plot, "Games zum Film</A>")
		self.plot = gutils.after(self.plot, " Crew</A>")
		self.plot = gutils.after(self.plot, "Soundtracks</A>")
		self.plot = gutils.after(self.plot, "DVD-Features</A>")
		self.plot = gutils.after(self.plot, " Fassungen</A>")
		self.plot = gutils.before(self.plot, "FOTOSHOW</span>")
		self.plot = gutils.after(self.plot, "</TABLE>")
		self.plot = gutils.before(self.plot, "</span>")

	def get_year(self):
		self.year = gutils.trim(self.tmp_page,"class=\"standardsmall\"><br /><b>DVD</b> - <b>","<br />")
		if self.year == "":
			self.year = gutils.trim(self.tmp_page,"class=\"standardsmall\"><b>","<br />")
		self.year = gutils.trim(self.year,"<b>","</b>")
		self.year = gutils.after(self.year," ")

	def get_runtime(self):
		self.runtime = gutils.trim(self.tmp_page,"Jahren</b> - <b>"," Min.")
		if (self.runtime == ''):
			self.runtime = gutils.trim(self.tmp_page,"Jahren</b></b> - <b>"," Min.")
		if (self.runtime == ''):
			self.runtime = gutils.trim(self.tmp_page,"</b><br /><b>"," Min.")

	def get_genre(self):
		self.genre = gutils.trim(self.tmp_page,"class=\"standardsmall\"><br /><b>DVD</b> - <b>","</b>")
		if self.genre == "":
			self.genre = gutils.trim(self.tmp_page,"class=\"standardsmall\"><b>","</b>")

	def get_cast(self):
		self.cast = gutils.trim(self.tmp_creditspage,"</td></tr><tr  class=\"dbtrefferlight", "</table>")
		if (self.cast == ""):
			self.cast = gutils.trim(self.tmp_creditspage,"</td></tr><tr class=\"dbtrefferlight", "</table>")
		self.cast = gutils.after(self.cast, "\">")
		self.cast = self.cast.replace("<tr class=\"dbtrefferlight\">", "\n")
		self.cast = self.cast.replace("<tr class=\"dbtrefferdark\">", "\n")
		self.cast = self.cast.replace("<tr  class=\"dbtrefferlight\">", "\n")
		self.cast = self.cast.replace("<tr  class=\"dbtrefferdark\">", "\n")
		self.cast = self.cast.replace("&nbsp;", "--flip--")
		self.cast = gutils.clean(self.cast)
		elements = self.cast.split("\n")
		self.cast = ''
		for element in elements:
			elements2 = element.split("--flip--")
			if len(elements2) > 1:
				self.cast += elements2[1] + "--flip--" + elements2[0] + "\n"
			else:
				self.cast = element
		self.cast = string.replace(self.cast, "--flip--", _(" as "))

	def get_classification(self):
		self.classification = gutils.trim(self.tmp_page,"FSK: ","</b>")

	def get_studio(self):
		self.studio = gutils.trim(self.tmp_page,"Verleih: ", "</b>")
		if (self.studio == ""):
			self.studio = gutils.trim(self.tmp_page,"Anbieter: ", "</b>")

	def get_o_site(self):
		self.o_site = ""

	def get_site(self):
		self.site = self.url_to_use + self.movie_id;

	def get_trailer(self):
		self.trailer = ""

	def get_country(self):
		self.country = gutils.trim(self.tmp_page,"class=\"standardsmall\"><br /><b>DVD</b> - <b>","<br />")
		if self.country == "":
			self.country = gutils.trim(self.tmp_page,"class=\"standardsmall\"><br /><b>VHS</b> - <b>","<br />")
		if self.country == "":
			self.country = gutils.trim(self.tmp_page,"class=\"standardsmall\"><br /><b>Laser Disc</b> - <b>","<br />")
		if self.country == "":
			self.country = gutils.trim(self.tmp_page,"class=\"standardsmall\"><br /><b>Video CD</b> - <b>","<br />")
		if self.country == "":
			self.country = gutils.trim(self.tmp_page,"class=\"standardsmall\"><br /><b>Blue-ray Disc</b> - <b>","<br />")
		if self.country == "":
			self.country = gutils.trim(self.tmp_page,"class=\"standardsmall\"><b>","<br />")
		self.country = gutils.trim(self.country,"<b>","</b>")
		self.country = gutils.before(self.country," ")

	def get_rating(self):
		self.rating = "0"

	def get_notes(self):
		self.notes = ""
		tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_dvdfeaturespage, "<b>Sprache</b>", "</td></tr>")), "&nbsp;", "")
		if (tmp_notes != ""):
			self.notes = self.notes + "Sprachen:\n" + tmp_notes + "\n\n"
		tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_dvdfeaturespage, "<b>Untertitel</b>", "</td></tr>")), "&nbsp;", "")
		if (tmp_notes != ""):
			self.notes = self.notes + "Untertitel:\n" + tmp_notes + "\n\n"
		tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_dvdfeaturespage, "<b>Mehrkanalton</b>", "</td></tr>")), "&nbsp;", "")
		if (tmp_notes != ""):
			self.notes = self.notes + "Mehrkanalton:\n" + tmp_notes + "\n\n"
		tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_dvdfeaturespage, "<b>EAN</b>", "</td></tr>")), "&nbsp;", "")
		if (tmp_notes != ""):
			self.notes = self.notes + "EAN:\n" + tmp_notes + "\n\n"

#
# kino.de use iso-8859-1
# it's not necessary to decode the page
# in fact if utf-8 is used you can't search for movies with german umlaut
# and if you use the decode call you get a terrible formatted result list
#

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search    = "http://www.kino.de/megasuche.php4?typ=filme&wort="
		self.translated_url_search    = "http://www.kino.de/megasuche.php4?typ=filme&wort="
#		self.encode='utf-8'
		self.encode='iso-8859-1'

	def search(self,parent_window):
		self.open_search(parent_window)
		tmp_pagemovie = string.replace( self.page, "</B>", "</b>" )
		tmp_pagemovie = string.replace( tmp_pagemovie, "A HREF", "a href" )
		tmp_pagemovie = gutils.trim(tmp_pagemovie,'</b></div><br>', '<!-- PRINT-CONTENT-ENDE-->');
		#
		# try to get all result pages (not so nice, but it works)
		#
		tmp_pagecount = gutils.trim(tmp_pagemovie, "&nbsp;von ", "</SPAN>")
		try:
			tmp_pagecountint = int(tmp_pagecount)
		except:
			tmp_pagecountint = 1
		tmp_pagecountintcurrent = 1
		while (tmp_pagecountint > tmp_pagecountintcurrent and tmp_pagecountintcurrent < 5):
			tmp_pagecountintcurrent = tmp_pagecountintcurrent + 1
			self.url = "http://www.kino.de/megasuche.php4?typ=filme&page=" + str(tmp_pagecountintcurrent) + "&wort="
			self.open_search(parent_window)
			tmp_page = string.replace( self.page, "</B>", "</b>" )
			tmp_page = string.replace( tmp_page, "A HREF", "a href" )
			tmp_page = gutils.trim(tmp_page,'</b></div><br>', '<!-- PRINT-CONTENT-ENDE-->');
			tmp_pagemovie = tmp_pagemovie + tmp_page
		#
		# Look for DVD and VHS
		#
		self.url = "http://www.kino.de/megasuche.php4?typ=video&wort="
		self.open_search(parent_window)
		tmp_pagevideo = string.replace( self.page, "<B>", "<b>" )
		tmp_pagevideo = string.replace( tmp_pagevideo, "A HREF", "a href" )
		tmp_pagevideo = gutils.trim(tmp_pagevideo,"align=center><b>Video/DVD 1", '<!-- PRINT-CONTENT-ENDE-->');
		tmp_pagevideo = tmp_pagemovie + tmp_pagevideo
		#
		# try to get all result pages (not so nice, but it works)
		#
		tmp_pagecount = gutils.trim(self.page, "&nbsp;von ", "</SPAN>")
		try:
			tmp_pagecountint = int(tmp_pagecount)
		except:
			tmp_pagecountint = 1
		tmp_pagecountintcurrent = 1
		while (tmp_pagecountint > tmp_pagecountintcurrent and tmp_pagecountintcurrent < 5):
			tmp_pagecountintcurrent = tmp_pagecountintcurrent + 1
			self.url = "http://www.kino.de/megasuche.php4?typ=video&page=" + str(tmp_pagecountintcurrent) + "&wort="
			self.open_search(parent_window)
			tmp_page = string.replace( self.page, "<B>", "<b>" )
			tmp_page = string.replace( tmp_page, "A HREF", "a href" )
			tmp_page = gutils.trim(tmp_page,"align=center><b>Video/DVD ", '<!-- PRINT-CONTENT-ENDE-->');
			tmp_pagevideo = tmp_pagevideo + tmp_page

		self.page = tmp_pagevideo
		return self.page

	def get_searches(self):
		elements1 = string.split(self.page,'headline3"><a href="http://www.kino.de/kinofilm/')
		elements1[0] = ''
		for element in elements1:
			if element <> '':
				self.ids.append("K_" + gutils.before(element,'"'))
				self.titles.append(gutils.strip_tags(
					gutils.trim(element,">","</a>") + " (" +
					gutils.trim(element, '<span class="standardsmall">', "</span>") + ")"
					)
				)

		elements2 = string.split(self.page,'headline3"><a href="http://www.kino.de/videofilm/')
		elements2[0] = ''
		for element in elements2:
			if element <> '':
				self.ids.append("V_" + gutils.before(element,'"'))
				self.titles.append(gutils.strip_tags(
					gutils.trim(element,">","</a>") + " (" +
					gutils.trim(element, '<span class="standardsmall">', '</span>') + ")"
					)
				)
