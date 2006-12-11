# -*- coding: iso-8859-2 -*-

__revision__ = '$Id$'

# Copyright (c) 2005, 2006 Piotr Ozarowski
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

plugin_name		= 'Filmweb'
plugin_description	= 'Web pelen filmow'
plugin_url		= 'www.filmweb.pl'
plugin_language		= _('Polish')
plugin_author		= 'Piotr Ozarowski'
plugin_author_email	= '<ozarow+griffith@gmail.com>'
plugin_version		= '1.8'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = 'filmweb'
		self.url      = str(id)
		self.encode   = 'iso-8859-2'

	def get_image(self):
		if string.find(self.page,'http://gfx.filmweb.pl/gf/bf.gif') > -1:
			self.image_url = ''
		else:
			self.image_url = gutils.trim(self.page,' class="k1"','<br />')
			self.image_url = gutils.after(self.image_url,'<img  src="')
			self.image_url = gutils.before(self.image_url,'" alt=')

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, '<span class="styt">', '</span>')
		tmp = len(self.o_title) - 1
		if self.o_title[tmp:] == ' ':
			self.o_title = self.o_title[:tmp]
		self.o_title = string.replace(self.o_title, "\t", '')
		self.o_title = string.replace(self.o_title, "\n", '')
		if string.find(self.o_title, '(') > -1:
			self.o_title = gutils.before(self.o_title, '(')

	def get_title(self):
		self.title = gutils.trim(self.page,"<div class=\"tyt\">","<span")
		self.title = string.replace(self.title, "\t",'')
		self.title = string.replace(self.title, "\n",'')
		if self.o_title == '':
			self.o_title = gutils.gdecode(self.title, self.encode)

	def get_director(self):
		self.director = gutils.trim(self.page,"yseria\t\t\t\t","\tscenariusz\t")
		self.director = string.replace(self.director, "\t",'')
		self.director = string.replace(self.director, "\n",'')
		self.director = string.replace(self.director, ",",", ")
		self.director = string.replace(self.director, ",  (wiÄÂĂÂcej&#160;...)",'')

	def get_plot(self):
		self.plot = gutils.trim(self.page," alt=\"o filmie\"/></div>","</div>")
		url = gutils.trim(self.plot,"\t...","</a>")
		url = gutils.trim(url, "href=\"","\">")
		self.plot = string.replace(self.plot, "\t",'')
		self.plot = gutils.strip_tags(self.plot)
		if url != '':
			self.plot = self.plot[:len(self.plot)-1] + ": " + url

	def get_year(self):
		self.year = gutils.trim(self.page, "\tdata premiery:", '</td>')
		tmp = string.rfind(self.year, '<b>') + 3
		self.year = self.year[tmp:tmp+4]

	def get_runtime(self):
		self.runtime = gutils.trim(self.page,"\tczas trwania: ","\n")

	def get_genre(self):
		self.genre = gutils.trim(self.page,"\tgatunek: ","\t")
		self.genre = string.replace(self.genre, "\t",'')
		self.genre = string.replace(self.genre, "\n",'')

	def get_cast(self):
		self.cast = gutils.trim(self.page,"alt=\"obsada\" />","</table>")
		self.cast = string.replace(self.cast,":&#160;", _(" as "))
		self.cast = string.replace(self.cast,_(" as ")+"</td>",_(" as "))
		self.cast = string.replace(self.cast, "\n",'')
		self.cast = string.replace(self.cast,"</td>","\n")
		self.cast = string.replace(self.cast,"valign=\"top\"", "\n")
		self.cast = string.replace(self.cast, "\t",'')
		self.cast = gutils.strip_tags(self.cast)
		self.cast = string.replace(self.cast, _(" as ")+"\n","\n")

	def get_classification(self):
		self.classification = gutils.trim(self.page,"\tod lat: ","\t")
		self.classification = string.replace(self.classification, "\t",'')
		self.classification = string.replace(self.classification, "\n",'')

	def get_studio(self):
		self.studio = ''

	def get_o_site(self):
		self.o_site = ''

	def get_site(self):
		self.site = self.url

	def get_trailer(self):
		self.trailer = ''

	def get_country(self):
		self.country = gutils.trim(self.page,"\tprodukcja: ","\t")
		self.country = string.replace(self.country, "\t",'')

	def get_rating(self):
		self.rating = gutils.trim(self.page, '<b class="rating">', '</b>')
		self.rating = string.replace(self.rating, ',', '.')
		if self.rating != '':
			self.rating = str( float(string.strip(self.rating)) )

	def get_notes(self):
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
