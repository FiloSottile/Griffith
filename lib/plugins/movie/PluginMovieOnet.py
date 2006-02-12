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

plugin_name         = "Onet"
plugin_description  = "Onet Film"
plugin_url          = "film.onet.pl"
plugin_language     = _("Polish")
plugin_author       = "Piotr Ozarowski"
plugin_author_email = "<ozarow@gmail.com>"
plugin_version      = "1.3"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='iso-8859-2'
		self.movie_id = id
		self.url = "http://film.onet.pl/" + str(self.movie_id)

	def picture(self):
		self.picture_url = ''
		if string.find(self.page,"IMG class=pic alt=\"Plakat\"") <> -1:
			self.picture_url = gutils.trim(self.page," class=pic alt=\"Plakat\" border=1 src=\"","\">")
			self.picture_url = 'http://film.onet.pl/' + self.picture_url
		self.movie_id = '' # often bad characters (problems with decoding polish characters in UTF8), so dont remember ID

	def original_title(self):
		self.original_title = gutils.trim(self.page,"class=a2 valign=top width=\"100%\"><B>","</B>")
		if self.original_title[0:4] == "The ":
			self.original_title = self.original_title[4:] + ", The"

	def title(self):
		self.title = gutils.trim(self.page,"<TITLE>Onet.pl - Film - ","</TITLE>")
		if self.original_title == '':
			self.original_title = self.title

	def director(self):
		self.director = gutils.trim(self.page,"<BR>Reżyseria:&nbsp;&nbsp;","<BR>")
		if string.find(self.director,"-->") <> -1:
			self.director = gutils.after(self.director,"-->")
			self.director = gutils.before(self.director,"<!--")
		else:
			self.director = gutils.after(self.director,"<B>")
			self.director = gutils.before(self.director,"</B>")

	def plot(self):
		self.plot = gutils.trim(self.page,"<DIV class=a2>","</DIV>")

	def year(self):
		self.year = gutils.trim(self.page,"class=a2 valign=top width=\"100%\">",")<BR>")
		self.year = gutils.after(self.year,"</B> (")
		self.year = gutils.after(self.year,", ")

	def running_time(self):
		self.running_time = gutils.trim(self.page,"color=\"#666666\">czas "," min.")

	def genre(self):
		self.genre = gutils.trim(self.page,"class=a2 valign=top width=\"100%\">","<BR><SPAN class=a1>")
		self.genre = gutils.after(self.genre,"<BR>")

	def with(self):
		self.with = '<'+gutils.trim(self.page,"#FF7902\">Obsada<","<DIV ")
		self.with = string.replace(self.with,"</A> - ", _(" as "))
		self.with = string.replace(self.with,"<A class=u ", "\n<a ")
		self.with = string.strip(gutils.strip_tags(self.with))
		self.with = self.with[18:]

	def classification(self):
		self.classification = ''

	def studio(self):
		self.studio = ''

	def site(self):
		self.site = ''

	def imdb(self):
		self.imdb = self.url

	def trailer(self):
		self.trailer = ''

	def country(self):
		self.country = gutils.trim(self.page,"class=a2 valign=top width=\"100%\">",")<BR>")
		self.country = gutils.after(self.country,"(")
		self.country = gutils.before(self.country,",")

	def rating(self):
		self.rating = gutils.trim(self.page,">Ocena filmu</TD>","głosów)")
		self.rating = gutils.after(self.rating,"<BR><B>")
		self.rating = gutils.before(self.rating,"/5</B>")
		if self.rating <> "":
			self.rating = str( float(self.rating)*2 )

	def notes(self):
		self.notes = ''
		self.movie_id = 'onet'	# movie_id often has bad characters, so after fetching poster, delete poster's name

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode='iso-8859-2'
		self.original_url_search	= "http://film.onet.pl/filmoteka.html?O=0&S="
		self.translated_url_search	= "http://film.onet.pl/filmoteka.html?O=1&S="

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		self.page = gutils.trim(self.page,">Wynik wyszukiwania<", "<TABLE border=0 cellpadding=0");
		self.page = gutils.after(self.page,"</SPAN></DIV><BR>");

	def get_searches(self):
		self.elements = string.split(self.page," class=pic")
		self.number_results = self.elements[-1]

		if (self.elements[0]<>''):
			for element in self.elements:
				self.ids.append(gutils.trim(element,"class=a2 width=\"100%\"><A href=\"","\" class=u"))
				element = gutils.trim(element,"class=u><B>","</B>")
				element = gutils.strip_tags(element)
				self.titles.append(element)
		else:
			self.number_results = 0

# vim: encoding=iso-8859-2
