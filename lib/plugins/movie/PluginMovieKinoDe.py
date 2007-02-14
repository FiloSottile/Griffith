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
plugin_version = "1.5"

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
	
	def get_image(self):
		# first, try to get the second picture before the JavaScript block (it should be the original poster)
		# if there is no second picture, use the first picture (it should be a picture from the film)
		self.image_url = "http://images.kino.de/flbilder/" + gutils.trim(gutils.after(gutils.before(self.tmp_page, "<script language="), "img src=\"http://images.kino.de/flbilder/"),"img src=\"http://images.kino.de/flbilder/", "\"")
		if (self.image_url == "http://images.kino.de/flbilder/"):
			self.image_url = "http://images.kino.de/flbilder/" + gutils.trim(self.tmp_page,"img src=\"http://images.kino.de/flbilder/", "\"")

	def get_o_title(self):
		self.o_title = gutils.trim(self.page,"span CLASS=\"standardsmall\"><br>(",")<")

	def get_title(self):
		if (self.url_type == "V"):
			self.title = gutils.after(gutils.trim(self.page,"\"headline2\"><A HREF=\"/videofilm.php4?nr=", "</A>"), ">")
		else:
			self.title = gutils.after(gutils.trim(self.page,"\"headline2\"><A HREF=\"/kinofilm.php4?nr=", "</A>"), ">")

	def get_director(self):
		if (gutils.trim(self.url, "typ=", "&") <> "credits"):
			self.url = self.url_to_use + "typ=credits&nr=" + str(self.movie_id)
			self.open_page(self.parent_window)
		self.director = gutils.trim(self.page,"Regie","</a>")
		self.director = gutils.after(self.director,"mitwirk.php4")
		self.director = gutils.after(self.director,">")

	def get_plot(self):
		if (gutils.trim(self.url, "typ=", "&") <> "film"):
			self.url = self.url_to_use + "typ=film&nr=" + str(self.movie_id)
			self.open_page(self.parent_window)
		self.tmp_page = gutils.trim(self.page, "<!-- PRINT-CONTENT-START-->", "<!-- PRINT-CONTENT-ENDE-->")
		# little steps to perfect plot (I hope ... it's a terrible structured content ... )
		self.plot = gutils.trim(self.tmp_page,"Kurzinfo", "</TD></TR><tr><td></td></tr><TR>")
		if (self.plot == ""):
			self.plot = gutils.trim(self.tmp_page,"Kurzinfo", "<script language=\"JavaScript\">")
		self.plot = gutils.after(self.plot, "Fotoshow</A>")
		self.plot = gutils.after(self.plot, "Filmpreise</A>")
		self.plot = gutils.after(self.plot, "Games zum Film</A>")
		self.plot = gutils.after(self.plot, " Crew</A>")
		self.plot = gutils.before(self.plot, "FOTOSHOW</SPAN>")
		self.plot = gutils.after(self.plot, "</TABLE>")

	def get_year(self):
		self.year = gutils.trim(self.page,"class=\"standardsmall\"><br><b>DVD</b> - <b>","<BR>")
		if self.year == "":
			self.year = gutils.trim(self.page,"class=\"standardsmall\"><b>","<BR>")
		self.year = gutils.trim(self.year,"<b>","</b>")
		self.year = gutils.after(self.year," ")

	def get_runtime(self):
		self.runtime = gutils.trim(self.page,"Jahren</b> - <b>"," Min.")
		if (self.runtime == ''):
			self.runtime = gutils.trim(self.page,"Jahren</b></b> - <b>"," Min.")
		if (self.runtime == ''):
			self.runtime = gutils.trim(self.page,"</b><BR><b>"," Min.")

	def get_genre(self):
		self.genre = gutils.trim(self.page,"class=\"standardsmall\"><br><b>DVD</b> - <b>","</b>")
		if self.genre == "":
			self.genre = gutils.trim(self.page,"class=\"standardsmall\"><b>","</b>")

	def get_cast(self):
		if (gutils.trim(self.url, "typ=", "&") <> "credits"):
			self.url = self.url_to_use + "typ=credits&nr=" + str(self.movie_id)
			self.open_page(self.parent_window)
		self.cast = gutils.trim(self.page,"</TD></TR><TR  CLASS=\"dbtreffer", "\n")
		self.cast = gutils.after(self.cast, "\">")
		self.cast = self.cast.replace("<TR  CLASS=\"dbtrefferlight\">", "\n")
		self.cast = self.cast.replace("<TR  CLASS=\"dbtrefferdark\">", "\n")
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
		self.classification = gutils.trim(self.page,"FSK: ","</b>")

	def get_studio(self):
		self.studio = gutils.trim(self.page,"Verleih: ", "</b>")
		if (self.studio == ""):
			self.studio = gutils.trim(self.page,"Anbieter: ", "</b>")

	def get_o_site(self):
		self.o_site = ""

	def get_site(self):
		self.site = self.url_to_use + "nr=" + self.movie_id;

	def get_trailer(self):
		self.trailer = ""

	def get_country(self):
		self.country = gutils.trim(self.page,"class=\"standardsmall\"><br><b>DVD</b> - <b>","<BR>")
		if self.country == "":
			self.country = gutils.trim(self.page,"class=\"standardsmall\"><b>","<BR>")
		self.country = gutils.trim(self.country,"<b>","</b>")
		self.country = gutils.before(self.country," ")

	def get_rating(self):
		self.rating = "0"

	def get_notes(self):
		self.notes = ""
		self.url = self.url_to_use + "typ=features&nr=" + str(self.movie_id)
		self.open_page(self.parent_window)
		self.tmp_page = gutils.trim(self.page, "<!-- PRINT-CONTENT-START-->", "<!-- PRINT-CONTENT-ENDE-->")
		self.tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_page, "<b>Sprache</b>", "</TD></TR>")), "&nbsp;", "")
		if (self.tmp_notes != ""):
			self.notes = self.notes + "Sprachen:\n" + self.tmp_notes + "\n\n"
		self.tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_page, "<b>Untertitel</b>", "</TD></TR>")), "&nbsp;", "")
		if (self.tmp_notes != ""):
			self.notes = self.notes + "Untertitel:\n" + self.tmp_notes + "\n\n"
		self.tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_page, "<b>Mehrkanalton</b>", "</TD></TR>")), "&nbsp;", "")
		if (self.tmp_notes != ""):
			self.notes = self.notes + "Mehrkanalton:\n" + self.tmp_notes + "\n\n"
		self.tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_page, "<b>EAN</b>", "</TD></TR>")), "&nbsp;", "")
		if (self.tmp_notes != ""):
			self.notes = self.notes + "EAN:\n" + self.tmp_notes + "\n\n"

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
		self.tmp_pagemovie = string.replace( self.page, "</B>", "</b>" )
		self.tmp_pagemovie = string.replace( self.tmp_pagemovie, "A HREF", "a href" )
		self.tmp_pagemovie = gutils.trim(self.tmp_pagemovie,'</b></div><br>', '<!-- PRINT-CONTENT-ENDE-->');
		#
		# try to get all result pages (not so nice, but it works)
		#
		self.tmp_pagecount = gutils.trim(self.tmp_pagemovie, "&nbsp;von ", "</SPAN>")
		try:
			self.tmp_pagecountint = int(self.tmp_pagecount)
		except:
			self.tmp_pagecountint = 1
		self.tmp_pagecountintcurrent = 1
		while (self.tmp_pagecountint > self.tmp_pagecountintcurrent):
			self.tmp_pagecountintcurrent = self.tmp_pagecountintcurrent + 1
			self.url = "http://www.kino.de/megasuche.php4?typ=filme&page=" + str(self.tmp_pagecountintcurrent) + "&wort="
			self.open_search(parent_window)
			self.tmp_page = string.replace( self.page, "</B>", "</b>" )
			self.tmp_page = string.replace( self.tmp_page, "A HREF", "a href" )
			self.tmp_page = gutils.trim(self.tmp_page,'</b></div><br>', '<!-- PRINT-CONTENT-ENDE-->');
			self.tmp_pagemovie = self.tmp_pagemovie + self.tmp_page
		#
		# Look for DVD and VHS
		#
		self.url = "http://www.kino.de/megasuche.php4?typ=video&wort="
		self.open_search(parent_window)
		self.tmp_pagevideo = string.replace( self.page, "<B>", "<b>" )
		self.tmp_pagevideo = string.replace( self.tmp_pagevideo, "A HREF", "a href" )
		self.tmp_pagevideo = gutils.trim(self.tmp_pagevideo,"align=center><b>Video/DVD 1", '<!-- PRINT-CONTENT-ENDE-->');
		self.tmp_pagevideo = self.tmp_pagemovie + self.tmp_pagevideo
		#
		# try to get all result pages (not so nice, but it works)
		#
		self.tmp_pagecount = gutils.trim(self.page, "&nbsp;von ", "</SPAN>")
		try:
			self.tmp_pagecountint = int(self.tmp_pagecount)
		except:
			self.tmp_pagecountint = 1
		self.tmp_pagecountintcurrent = 1
		while (self.tmp_pagecountint > self.tmp_pagecountintcurrent):
			self.tmp_pagecountintcurrent = self.tmp_pagecountintcurrent + 1
			self.url = "http://www.kino.de/megasuche.php4?typ=video&page=" + str(self.tmp_pagecountintcurrent) + "&wort="
			self.open_search(parent_window)
			self.tmp_page = string.replace( self.page, "<B>", "<b>" )
			self.tmp_page = string.replace( self.tmp_page, "A HREF", "a href" )
			self.tmp_page = gutils.trim(self.tmp_page,"align=center><b>Video/DVD ", '<!-- PRINT-CONTENT-ENDE-->');
			self.tmp_pagevideo = self.tmp_pagevideo + self.tmp_page

		self.page = self.tmp_pagevideo
		return self.page

	def get_searches(self):
		elements1 = string.split(self.page,'headline3"><a href="/kinofilm.php4?nr=')
		elements1[0] = ''
		for element in elements1:
			if element <> '':
				self.ids.append("K_" + gutils.before(element,'&'))
				self.titles.append(gutils.strip_tags(
					gutils.trim(element,">","</A>") + " " +
					gutils.trim(element, "<span CLASS=\"standardsmall\"><br>", "</SPAN>") + " (" +
					string.replace(
						gutils.trim(element, "<span class=\"standardsmall\"><b>", "</span>"), "<b>", ", ")
							+ ")"))
							
		elements2 = string.split(self.page,'headline3"><a href="/videofilm.php4?nr=')
		elements2[0] = ''
		for element in elements2:
			if element <> '':
				self.ids.append("V_" + gutils.before(element,'&'))
				self.titles.append(gutils.strip_tags( 
					gutils.trim(element,">","</A>") + " " +
					gutils.trim(element, '<span CLASS="standardsmall"><br>', '</SPAN>') + " (" +
					string.replace(
						gutils.trim(element, '<span class="standardsmall"><br><b>', "</span>"), "<b>", ", ") + ")"))
