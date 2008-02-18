# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Piotr Ożarowski
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
import gutils, movie
import re,string

plugin_name		= 'Filmweb'
plugin_description	= 'Web pełen filmów'
plugin_url		= 'www.filmweb.pl'
plugin_language		= _('Polish')
plugin_author		= 'Piotr Ożarowski'
plugin_author_email	= '<ozarow+griffith@gmail.com>'
plugin_version		= '1.12'

class Plugin(movie.Movie):
	TRAILER_PATTERN     = re.compile("""<a class=["']notSelected["'].*?href=["'](.*?)["']>zwiastuny</a>\s*\[\d+\]\s*&raquo;""")
	DIRECTOR_PATTERN    = re.compile('yseria\s+(.*)\s+scenariusz', re.MULTILINE)
	O_TITLE_AKA_PATTERN = re.compile('\(AKA\s+(.*?)\)')

	def __init__(self, id):
		self.movie_id = 'filmweb'
		self.url      = str(id)
		self.encode   = 'utf-8'

	def get_image(self):
		if string.find(self.page,'http://gfx.filmweb.pl/gf/bf.gif') > -1:
			self.image_url = ''
		else:
			self.image_url = gutils.trim(self.page, '<div id="filmPhoto">', '</div')
			self.image_url = gutils.trim(self.image_url, 'src="', '"')

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, '<span class="otherTitle">', '<span')
		tmp = self.O_TITLE_AKA_PATTERN.findall(self.o_title)
		if tmp:
			self.o_title = tmp[0]
		else:
			self.o_title = string.replace(self.o_title, "\t",'')
			self.o_title = string.replace(self.o_title, "\n",'')

	def get_title(self):
		self.title = gutils.trim(self.page, '<div id="filmTitle">', '<span')
		self.title = string.replace(self.title, "\t", '')
		self.title = string.replace(self.title, "\n", '')
		if string.find(self.title, '(') > -1:
			self.title = gutils.before(self.title, '(')

	def get_director(self):
		director = self.DIRECTOR_PATTERN.findall(self.page)
		if len(director)>0:
			self.director = director[0]
			self.director = string.replace(self.director, "\t",'')
			self.director = re.sub('\s+', ' ', self.director)
			self.director = string.replace(self.director, ",",", ")
			self.director = string.replace(self.director, " ,  ",", ")
			self.director = string.replace(self.director, ",  (wi\xeacej&#160;...)",'')

	def get_plot(self):
		self.plot = gutils.trim(self.page," alt=\"o filmie\"/></div>","</div>")
		url = gutils.trim(self.plot,"\t...","</a>")
		url = gutils.trim(url, "href=\"","\">")
		self.plot = string.replace(self.plot, "\t",'')
		self.plot = gutils.strip_tags(self.plot)
		if url != '':
			#self.plot = self.plot[:len(self.plot)-1] + ": " + url
			plot_page = self.open_page(url=url)
			self.plot = gutils.trim(plot_page, '<div class="filmContent">', '</li>')

	def get_year(self):
		self.year = gutils.trim(self.page, "\tdata premiery:", '</td>')
		tmp = string.rfind(self.year, '<b>') + 3
		self.year = self.year[tmp:tmp+4]

	def get_runtime(self):
		self.runtime = gutils.trim(self.page,"\tczas trwania: ","\n")

	def get_genre(self):
		self.genre = gutils.trim(self.page,"\tgatunek:", '</td>')
		self.genre = string.replace(self.genre, "\t",'')
		self.genre = string.replace(self.genre, "\n",'')

	def get_cast(self):
		self.cast = "<%s" % gutils.trim(self.page, '/ob.gif"',"zobacz więcej")
		self.cast = string.replace(self.cast, "\n",'')
		self.cast = string.replace(self.cast, "\t",'')
		self.cast = string.replace(self.cast, ":", _(" as "))
		self.cast = string.replace(self.cast, '</span>', "\n")
		self.cast = gutils.strip_tags(self.cast)

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
		trailer = self.TRAILER_PATTERN.findall(self.page)
		if trailer:
			self.trailer = trailer[0]

	def get_country(self):
		self.country = gutils.trim(self.page,"\tprodukcja:", '</b>')
		self.country = string.replace(self.country, "\t",'')

	def get_rating(self):
		self.rating = gutils.trim(self.page, '<b id="filmRating" class="rating">', '</b>')
		self.rating = string.replace(self.rating, ',', '.')
		if self.rating != '':
			self.rating = str( float(string.strip(self.rating)) )

	def get_notes(self):
		self.notes = ''

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode='utf-8'
		self.original_url_search   = "http://www.filmweb.pl/szukaj?c=film&q="
		self.translated_url_search = "http://www.filmweb.pl/szukaj?c=film&q="

	def search(self,parent_window):
		self.open_search(parent_window)
		pos = string.find(self.page, 'Znaleziono <b>')
		if pos == -1:	# movie page
			self.page = None
		else:		# search results
			items = gutils.trim(self.page[pos:], '<b>', '</b>')
			if items == '0':
				self.page = False
			else:
				self.page = gutils.before(self.page[pos:], 'id="sitemap"')
				self.page = gutils.after(self.page, '<li ')
		return self.page

	def get_searches(self):
		if self.page is None:	# movie page
			self.number_results = 1
			self.ids.append(self.url)
			self.titles.append(gutils.convert_entities(self.title))
		elif self.page is False: # no movie found
			self.number_results = 0
		else:			# multiple matches
			elements = string.split(self.page, '<li ')
			self.number_results = elements[-1]
			if (elements[0]<>''):
				for element in elements:
					element = gutils.after(element, '<a class="searchResultTitle" href="')
					self.ids.append(gutils.before(element, '">'))
					element = gutils.trim(element, '">', '</a>')
					element = gutils.convert_entities(element)
					element = gutils.strip_tags(element)
					self.titles.append(element)
			else:
				self.number_results = 0
