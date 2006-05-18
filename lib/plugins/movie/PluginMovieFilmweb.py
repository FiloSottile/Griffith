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

plugin_name		= "Filmweb"
plugin_description	= "Web pelen filmow"
plugin_url		= "www.filmweb.pl"
plugin_language		= _("Polish")
plugin_author		= "Piotr Ozarowski"
plugin_author_email	= "<ozarow@gmail.com>"
plugin_version		= "1.5"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = "filmweb"
		self.url      = str(id)
		self.encode   = "iso-8859-2"

	def picture(self):
		if string.find(self.page,"http://gfx.filmweb.pl/gf/bf.gif") > -1:
			self.picture_url = ''
		else:
			self.picture_url = gutils.trim(self.page," class=\"k1\"","<br />")
			self.picture_url = gutils.after(self.picture_url,"<img  src=\"")
			self.picture_url = gutils.before(self.picture_url,"\" alt=")

	def original_title(self):
		self.original_title = gutils.trim(self.page,"\n\t\t\t\t<span class=\"styt\">"," </span>")
		self.original_title = string.replace(self.original_title, "\t", '')
		self.original_title = string.replace(self.original_title, "\n", '')

	def title(self):
		self.title = gutils.trim(self.page,"<div class=\"tyt\">","<span")
		self.title = string.replace(self.title, "\t",'')
		self.title = string.replace(self.title, "\n",'')
		if self.original_title == '':
			self.original_title = self.title

	def director(self):
		self.director = gutils.trim(self.page,"\treżyseria	","\tscenariusz	")
		self.director = string.replace(self.director, "\t",'')
		self.director = string.replace(self.director, "\n",'')
		self.director = string.replace(self.director, ",",", ")
		self.director = string.replace(self.director, ",  (więcej&#160;...)",'')

	def plot(self):
		self.plot = gutils.trim(self.page," alt=\"o filmie\"/></div>","</div>")
		url = gutils.trim(self.plot,"\t...","</a>")
		url = gutils.trim(url, "href=\"","\">")
		self.plot = string.replace(self.plot, "\t",'')
		self.plot = gutils.strip_tags(self.plot)
		self.plot = string.replace(self.plot, "\n... więcej","...")
		if url != '':
			self.plot = self.plot + "\nWIECEJ NA: " + url

	def year(self):
		self.year = gutils.trim(self.page,"\tdata premiery:","</td>")
		tmp = string.rfind(self.year, "<b>")
		self.year = self.year[tmp:]
		self.year = gutils.before(self.year,"</b>")

	def running_time(self):
		self.running_time = gutils.trim(self.page,"\tczas trwania: ","\n")

	def genre(self):
		self.genre = gutils.trim(self.page,"\tgatunek: ","\t")
		self.genre = string.replace(self.genre, "\t",'')
		self.genre = string.replace(self.genre, "\n",'')

	def with(self):
		self.with = gutils.trim(self.page,"alt=\"obsada\" />","</table>")
		self.with = string.replace(self.with,":&#160;", _(" as "))
		self.with = string.replace(self.with,_(" as ")+"</td>",_(" as "))
		self.with = string.replace(self.with, "\n",'')
		self.with = string.replace(self.with,"</td>","\n")
		self.with = string.replace(self.with,"valign=\"top\"", "\n")
		self.with = string.replace(self.with, "\t",'')
		self.with = gutils.strip_tags(self.with)
		self.with = string.replace(self.with, _(" as ")+"\n","\n")

	def classification(self):
		self.classification = gutils.trim(self.page,"\tod lat: ","\t")
		self.classification = string.replace(self.classification, "\t",'')
		self.classification = string.replace(self.classification, "\n",'')

	def studio(self):
		self.studio = ''

	def site(self):
		self.site = ''

	def imdb(self):
		self.imdb = self.url

	def trailer(self):
		self.trailer = ''

	def country(self):
		self.country = gutils.trim(self.page,"\tprodukcja: ","\t")
		self.country = string.replace(self.country, "\t",'')

	def rating(self):
		self.rating = gutils.trim(self.page," alt=\"*\" ","</b>")
		self.rating = gutils.after(self.rating,"#8D0000;\">")
		self.rating = string.replace(self.rating, ",",".")
		if self.rating != '':
			self.rating = str( float(string.strip(self.rating)) )

	def notes(self):
		self.notes = ''

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode='iso-8859-2'
		self.original_url_search   = "http://www.filmweb.pl/Find?category=1&query="
		self.translated_url_search = "http://www.filmweb.pl/Find?category=1&query="

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		tmp = string.find(self.page,"szukana fraza")
		if tmp == -1:	# only one match!
			self.page = ''
		else:		# multiple matches
			self.page = gutils.trim(self.page,"szukana fraza:", "</form>");

	def get_searches(self):
		if self.page == "":	# immidietly redirection to movie page
			self.number_results = 1
			self.ids.append(self.url)
			self.titles.append(gutils.convert_entities(self.title))
		else:			# multiple matches
			elements = string.split(self.page,"<a title=")
			self.number_results = elements[-1]
			if (elements[0]<>''):
				for element in elements:
					self.ids.append(gutils.trim(element,"href=\"","\">"))
					element = gutils.trim(element,"'","' href=")
					element = gutils.convert_entities(element)
					self.titles.append(element)
			else:
				self.number_results = 0
# vim: encoding=iso-8859-2
