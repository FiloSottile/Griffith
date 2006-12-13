# -*- coding: iso-8859-2 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2006 Piotr Ozarowski
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
import re

plugin_name         = 'Wirtualna Polska'
plugin_description  = 'Serwis filmowy Wirtualnej Polski'
plugin_url          = 'www.film.wp.pl'
plugin_language     = _('Polish')
plugin_author       = 'Piotr Ozarowski'
plugin_author_email = '<ozarow+griffith@gmail.com>'
plugin_version      = '1.6'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.url = "http://film.wp.pl/h,1,id,%s,film.html" % str(self.movie_id)
		self.encode='iso-8859-2'

	def initialize(self):
		self.page = gutils.trim(self.page,"<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">","<script ")

	def get_image(self):
		if string.find(self.page,"http://film.wp.pl/f/no.gif") > -1:
			self.image_url = ""
		else:
			self.image_url = gutils.trim(self.page,"http://film.wp.pl/f/prev/","\" width=")
			self.image_url = 'http://film.wp.pl/f/prev/' + self.image_url

	def get_o_title(self):
		self.o_title = gutils.trim(self.page,"<i class=\"ti\" id=\"gr\" style=\"font-size: 14px\">","</i>")

	def get_title(self):
		self.title = gutils.trim(self.page,"<b class=\"ti\"","</b>")
		self.title = gutils.after(self.title, ">")
		tmp = string.find(self.title," (")
		if tmp != -1:
			self.tmp_year = self.title[tmp+2:tmp+6]	# save for later - see year()
			self.title = self.title[:tmp]	# cut " (YEAR)"
		if self.o_title == '':
			self.o_title = gutils.gdecode(self.title, self.encode)

	def get_director(self):
		self.director = gutils.trim(self.page,"<b>Re¿yseria:</b>","<br>")
		self.director = gutils.after(self.director,"\">")
		self.director = gutils.strip_tags(self.director)

	def get_plot(self):
		self.plot = gutils.trim(self.page,"<span id=\"mi\">","</span>")
		self.plot = gutils.strip_tags(self.plot)
		self.plot = string.replace(self.plot[1:],"\r\n\r\n","")

	def get_year(self):
		self.year = gutils.trim(self.page,"<b>Premiera ","<br>")
		self.year = gutils.after(self.year,"</b> ")
		if self.year == '' and self.tmp_year != '':	# if premiere date is not available, use header data
			self.year = self.tmp_year

	def get_runtime(self):
		self.runtime = gutils.trim(self.page,"<b>Czas trwania:</b> "," min.<br>")

	def get_genre(self):
		self.genre = gutils.trim(self.page,"<b>Gatunek:</b> ","<br>")

	def get_cast(self):
		self.cast = gutils.trim(self.page,"<b>Obsada:</b><br>","<div ")
		self.cast = string.replace(self.cast," ..... ", _(" as "))
		self.cast = string.replace(self.cast,"<br>\n<a", "\n<a")
		self.cast = string.strip(gutils.strip_tags(self.cast))


	def get_classification(self):
		self.classification = ''

	def get_studio(self):
		self.studio = ''

	def get_o_site(self):
		self.o_site = ''

	def get_site(self):
		self.site = self.url

	def get_trailer(self):
		self.trailer = "http://film.wp.pl/p/id,%s,film_trailer.html" % self.movie_id

	def get_country(self):
		self.country = gutils.trim(self.page,"<b>Kraj:</b> ","<br>")

	def get_rating(self):
		self.rating = gutils.trim(self.page,"<b>Ocena internautów: ","</b>")
		if self.rating != '':
			self.rating = str( float(self.rating) )

	def get_notes(self):
		self.notes = ''

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode='iso-8859-2'
		self.original_url_search	= 'http://film.wp.pl/p/szukaj.html?w='
		self.translated_url_search	= 'http://film.wp.pl/p/szukaj.html?w='

	def search(self,parent_window):
		self.open_search(parent_window)
		self.page = gutils.trim(self.page,"<span class=\"btw\">&nbsp;Filmy</span>", "<span class=\"btw\">&nbsp;Ludzie</span>");
		self.page = gutils.after(self.page,"<td valign=\"top\">");
		self.page = re.sub(r"<a href=\"http://film.wp.pl/h,1,id,[0-9]+,osoba.html\">", "", self.page)
		return self.page

	def get_searches(self):
		elements = string.split(self.page,"http://film.wp.pl/h,1")
		self.number_results = elements[-1]

		if (elements[0]<>''):
			for element in elements:
				self.ids.append(gutils.trim(element,",id,",",film.html\">"))
				element = gutils.trim(element,">","</")
				element = gutils.strip_tags(element)
				self.titles.append(element)
		else:
			self.number_results = 0
# vim: encoding=iso-8859-2