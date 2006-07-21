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
import re

plugin_name = "Wirtualna Polska"
plugin_description = "Serwis filmowy Wirtualnej Polski"
plugin_url = "www.film.wp.pl"
plugin_language = _("Polish")
plugin_author = "Piotr Ozarowski"
plugin_author_email = "<ozarow@gmail.com>"
plugin_version = "1.4"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.url = "http://film.wp.pl/h,1,id,%s,film.html" % str(self.movie_id)
		self.encode='iso-8859-2'

	def picture(self):
		self.page = gutils.trim(self.page,"<table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">","<script ")	# should go to sub_page function!
		if string.find(self.page,"http://film.wp.pl/f/no.gif") > -1:
			self.picture_url = ""
		else:
			self.picture_url = gutils.trim(self.page,"http://film.wp.pl/f/prev/","\" width=")
			self.picture_url = 'http://film.wp.pl/f/prev/' + self.picture_url

	def original_title(self):
		self.original_title = gutils.trim(self.page,"<i class=\"ti\" id=\"gr\" style=\"font-size: 14px\">","</i>")

	def title(self):
		self.title = gutils.trim(self.page,"<b class=\"ti\"","</b>")
		self.title = gutils.after(self.title, ">")
		tmp = string.find(self.title," (")
		if tmp != -1:
			self.tmp_year = self.title[tmp+2:tmp+6]	# save for later - see year()
			self.title = self.title[:tmp]	# cut " (YEAR)"
		if self.original_title == '':
			self.original_title = self.title

	def director(self):
		self.director = gutils.trim(self.page,"<b>Reżyseria:</b>","<br>")
		self.director = gutils.after(self.director,"\">")
		self.director = gutils.strip_tags(self.director)

	def plot(self):
		self.plot = gutils.trim(self.page,"<span id=\"mi\">","</span>")
		self.plot = gutils.strip_tags(self.plot)
		self.plot = string.replace(self.plot[1:],"\r\n\r\n","")

	def year(self):
		self.year = gutils.trim(self.page,"<b>Premiera ","<br>")
		self.year = gutils.after(self.year,"</b> ")
		if self.year == '' and self.tmp_year != '':	# if premiere date is not available, use header data
			self.year = self.tmp_year

	def running_time(self):
		self.running_time = gutils.trim(self.page,"<b>Czas trwania:</b> "," min.<br>")

	def genre(self):
		self.genre = gutils.trim(self.page,"<b>Gatunek:</b> ","<br>")

	def with(self):
		self.with = gutils.trim(self.page,"<b>Obsada:</b><br>","<div ")
		self.with = string.replace(self.with," ..... ", _(" as "))
		self.with = string.replace(self.with,"<br>\n<a", "\n<a")
		self.with = string.strip(gutils.strip_tags(self.with))


	def classification(self):
		self.classification = ''

	def studio(self):
		self.studio = ''

	def site(self):
		self.site = ''

	def imdb(self):
		self.imdb = self.url

	def trailer(self):
		self.trailer = "http://film.wp.pl/p/id,%s,film_trailer.html" % self.movie_id

	def country(self):
		self.country = gutils.trim(self.page,"<b>Kraj:</b> ","<br>")

	def rating(self):
		self.rating = gutils.trim(self.page,"<b>Ocena internautów: ","</b>")
		if self.rating != '':
			self.rating = str( float(self.rating) )

	def notes(self):
		self.notes = ''

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode='iso-8859-2'
		self.original_url_search	= "http://film.wp.pl/p/szukaj.html?w="
		self.translated_url_search	= "http://film.wp.pl/p/szukaj.html?w="

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		self.page = gutils.trim(self.page,"<span class=\"btw\">&nbsp;Filmy</span>", "<span class=\"btw\">&nbsp;Ludzie</span>");
		self.page = gutils.after(self.page,"<td valign=\"top\">");
		self.page = re.sub(r"<a href=\"http://film.wp.pl/h,1,id,[0-9]+,osoba.html\">", "", self.page)

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
