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
import re

plugin_name = "Kino.de"
plugin_description = "KINO.DE"
plugin_url = "www.kino.de"
plugin_language = _("German")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.8"

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
		self.tmp_page = gutils.before(self.page, 'kinode_navi1')
		self.url = self.url_to_use + string.replace(str(self.movie_id), '/', '/credits/')
		self.open_page(self.parent_window)
		self.tmp_creditspage = gutils.before(self.page, 'kinode_navi1')
		self.url = self.url_to_use + string.replace(str(self.movie_id), "/", "/features/")
		self.open_page(self.parent_window)
		self.tmp_dvdfeaturespage = gutils.before(self.page, 'kinode_navi1')

	def get_image(self):
		self.image_url = gutils.trim(self.tmp_page, 'class="navi', '.jpg"')
		if self.image_url <> '':
			self.image_url = 'http://images.kino.de/flbilder/' + gutils.after(self.image_url, 'http://images.kino.de/flbilder/') + '.jpg'
		else:
			self.image_url = self.regextrim(self.tmp_page, 'http://images.kino.de/flbilder/', 'headline2')
			if self.image_url <> '':
				self.image_url = 'http://images.kino.de/flbilder/' + gutils.before(self.image_url, '"')

	def get_o_title(self):
		self.o_title = gutils.trim(self.tmp_page,"span class=\"standardsmall\"><br />(",")<")
		if self.o_title == "":
			if self.url_type == "V":
				self.o_title = gutils.after(gutils.trim(self.tmp_page,"\"headline2\"><a href=\"/videofilm", "</a>"), ">")
			else:
				self.o_title = gutils.after(gutils.trim(self.tmp_page,"\"headline2\"><a href=\"/kinofilm", "</a>"), ">")

	def get_title(self):
		if self.url_type == "V":
			self.title = gutils.after(gutils.trim(self.tmp_page,"\"headline2\"><a href=\"/videofilm", "</a>"), ">")
		else:
			self.title = gutils.after(gutils.trim(self.tmp_page,"\"headline2\"><a href=\"/kinofilm", "</a>"), ">")

	def get_director(self):
		self.director = gutils.trim(self.tmp_creditspage,"Regie","</a>")
		self.director = gutils.after(self.director,"/star/")
		self.director = gutils.after(self.director,">")

	def get_plot(self):
		# little steps to perfect plot (I hope ... it's a terrible structured content ... )
		self.plot = gutils.trim(self.tmp_page, '<span style="line-height:', '</spa')
		if self.plot == '':
			self.plot = gutils.trim(self.tmp_page,"Kurzinfo", "</td></tr><tr><td></td>")
			if (self.plot == ''):
				self.plot = gutils.trim(self.tmp_page,"Kurzinfo", '<script ')
				self.plot = gutils.after(self.plot, '>')
			while len(self.plot) and string.find(self.plot, '</A>') > -1:
				self.plot = gutils.after(self.plot, '</A>');
			self.plot = gutils.after(gutils.after(self.plot, '</table>'), '>')
		else:
			self.plot = gutils.after(self.plot, '>')

	def get_year(self):
		self.year = self.regextrim(self.tmp_page,"class=\"standardsmall\"><br /><b>(DVD|VHS|Laser Disc|Video CD|Blue-ray Disc)</b> - <b>","<br />")
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
		self.genre = self.regextrim(self.tmp_page,"class=\"standardsmall\"><br /><b>(DVD|VHS|Laser Disc|Video CD|Blue-ray Disc)</b> - <b>","</b>")
		if self.genre == "":
			self.genre = gutils.trim(self.tmp_page,"class=\"standardsmall\"><b>","</b>")

	def get_cast(self):
		self.cast = gutils.trim(self.tmp_creditspage,'>Cast<', '</table><br')
		if len(self.cast):
			if self.cast.find('>mehr<') > 0:
				self.cast = gutils.after(self.cast, '>mehr<')
			self.cast = gutils.after(self.cast, '>')
			self.cast = re.sub('<tr[ ]+class="(dbtrefferlight|dbtrefferdark)">', "\n", self.cast)
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
		self.country = self.regextrim(self.tmp_page,"class=\"standardsmall\"><br /><b>(DVD|VHS|Laser Disc|Video CD|Blue-ray Disc)</b> - <b>","<br />")
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
			
	def regextrim(self,text,key1,key2):
		obj = re.search(key1, text)
		if obj is None:
			return ''
		else:
			p1 = obj.end()
		obj = re.search(key2, text[p1:])
		if obj is None:
			return ''
		else:
			p2 = p1 + obj.end()
		return text[p1:p2]

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
		tmp_pagemovie = self.page
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
			tmp_pagemovie = tmp_pagemovie + self.page
		#
		# Look for DVD and VHS
		#
		self.url = "http://www.kino.de/megasuche.php4?typ=video&wort="
		self.open_search(parent_window)
		tmp_pagevideo = tmp_pagemovie + self.page
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
			tmp_pagevideo = tmp_pagevideo + self.page

		self.page = tmp_pagevideo
		return self.page

	def get_searches(self):
		elements1 = re.split('headline3"><a href="(http://www.kino.de)*/kinofilm/', self.page)
		elements1[0] = None
		for element in elements1:
			if element <> None:
				self.ids.append("K_" + re.sub('[?].*', '', gutils.before(element,'"')))
				self.titles.append(string.replace(string.replace(
					gutils.strip_tags(
						gutils.trim(element,'>','</a>') + ' (' +
						string.replace(
							gutils.trim(element, '<span class="standardsmall">', "</span>"),
							'<br />', ' - ')
						+ ')'
					),
					'( - (', '('), '))', ')')
				)

		elements2 = re.split('headline3"><a href="(http://www.kino.de)*/videofilm/', self.page)
		elements2[0] = None
		for element in elements2:
			if element <> None:
				self.ids.append("V_" + re.sub('[?].*', '', gutils.before(element,'"')))
				self.titles.append(string.replace(string.replace(
					gutils.strip_tags(
						gutils.trim(element,'>','</a>') + ' (' +
						string.replace(
							gutils.trim(element, '<span class="standardsmall">', '</span>'),
							'<br />', ' - ')
						+ ')'
					),
					'( - (', '('), '))', ')')
				)
