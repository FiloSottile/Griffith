# -*- coding: iso-8859-2 -*-
__revision__ = '$Id: PluginMovieWP.py,v 1.7 2005/09/22 22:35:24 pox Exp $'
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

plugin_name = "Wirtualna Polska"
plugin_description = "Serwis filmowy Wirtualnej Polski"
plugin_url = "www.film.wp.pl"
plugin_language = _("Polish")
plugin_author = "Piotr Ozarowski"
plugin_author_email = "<ozarow@gmail.com>"
plugin_version = "1.3"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.url = "http://film.wp.pl/film.html?id=" + str(self.movie_id)
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
		print "ot="+self.original_title

	def title(self):
		self.title = gutils.trim(self.page,"<b class=\"ti\" style=\"font-size: 15px\">","</b>")
		tmp = string.find(self.title," (")
		if tmp != -1:
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
		self.classification = ""

	def studio(self):
		self.studio = ""

	def site(self):
		self.site = ""

	def imdb(self):
		self.imdb = self.url

	def trailer(self):
		self.trailer = ""

	def country(self):
		self.country = gutils.trim(self.page,"<b>Kraj:</b> ","<br>")

	def rating(self):
		self.rating = gutils.trim(self.page,"<b>Ocena internautów: ","</b>")
		if self.rating <> "":
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

	def get_searches(self):
		self.elements = string.split(self.page,"<a href=\"http://film.wp.pl/film.html")
		self.number_results = self.elements[-1]

		if (self.elements[0]<>''):
			for element in self.elements:
				self.ids.append(gutils.trim(element,"?id=","&h=1\">"))
				element = gutils.trim(element,">","</")
				element = gutils.strip_tags(element)
				self.titles.append(element)
		else:
			self.number_results = 0

# vim: encoding=iso-8859-2
