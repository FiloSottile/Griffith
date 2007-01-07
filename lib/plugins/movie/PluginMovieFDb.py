# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2007 Piotr Ozarowski
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

plugin_name		= 'FDb'
plugin_description	= 'Internetowa baza filmowa'
plugin_url		= 'fdb.pl'
plugin_language		= _('Polish')
plugin_author		= 'Piotr Ożarowski'
plugin_author_email	= '<ozarow+griffith@gmail.com>'
plugin_version		= '1.6'

class Plugin(movie.Movie):
	def __init__(self, movie_id):
		from md5 import md5
		self.movie_id = md5(movie_id).hexdigest()
		self.encode   = 'utf-8'
		if string.find(movie_id, 'http://') != -1:
			self.url = str(movie_id)
		else:
			self.url = "http://fdb.pl/%s" % str(movie_id)

	def get_image(self):
		self.image_url = gutils.trim(self.page, 'class="moviePosterTable"', '</td>');
		self.image_url = gutils.trim(self.image_url,' src="',"\"\n")
		self.image_url = "http://fdb.pl%s" % self.image_url

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, '<h2>', '</h2>')
		self.o_title = gutils.strip_tags(self.o_title)
		if self.o_title == '':
			self.o_title = self.get_title(True)

	def get_title(self, extra=False):
		data = gutils.trim(self.page,'<title>', '</title>')
		tmp = string.find(data, '(')
		if tmp != -1:
			data = data[:tmp]
		if extra is False:
			self.title = data
		else:
			return data

	def get_director(self):
		self.director = ''
		elements = gutils.trim(self.page,'>Reżyseria</div>','<br />')
		elements = string.split(elements, '<div>')
		if elements[0] != '':
			for element in elements:
				element = gutils.trim(element, '>', '</a')
				if element != '':
					self.director += ', ' + element
			self.director = string.replace(self.director[2:], ', &nbsp;&nbsp;&nbsp;(więcej)', '')

	def get_plot(self):
		self.plot = gutils.trim(self.page,'>Opis filmu:</div>','</div>')

	def get_year(self):
		self.year = gutils.trim(self.page,' class="movieYear">(', ')</span>')

	def get_runtime(self):
		self.runtime = gutils.trim(self.page,">Czas trwania:</span>\n        ",' min')

	def get_genre(self):
		self.genre = gutils.trim(self.page,'>Gatunek:</span>','</div>')
		self.genre = string.replace(self.genre, '   ', '')

	def get_cast(self):
		self.cast = gutils.trim(self.page,'>Obsada:</div>', """<tr>
            <td colspan""")
		if self.cast != '':
			self.cast = self.cast.replace('....',_(' as '))
			self.cast = self.cast.replace('  ', '')
			self.cast = self.cast.replace("\n", '')
			self.cast = self.cast.replace('</tr>', "\n")

	def get_classification(self):
		self.classification = gutils.trim(self.page,">Od lat:</span>\n","\n")

	def get_studio(self):
		self.studio = ''

	def get_o_site(self):
		self.o_site = ''

	def get_site(self):
		self.site = self.url

	def get_trailer(self):
		self.trailer = ''

	def get_country(self):
		self.country = gutils.trim(self.page,">Kraj:</span>\n",'</div>')
		self.country = string.replace(self.country, "   ", '')

	def get_rating(self):
		self.rating = gutils.trim(self.page, '>Ocena:</span>','/10</span>')
		self.rating = gutils.after(self.rating, 'bold">')
		if self.rating:
			self.rating = str(float(gutils.clean(self.rating)))

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode = 'utf-8'
		self.original_url_search	= 'http://fdb.pl/szukaj.php?t=f&s='
		self.translated_url_search	= 'http://fdb.pl/szukaj.php?t=f&s='

	def search(self,parent_window):
		self.open_search(parent_window)
		tmp = string.find(self.page,'<div>Wyniki wyszukiwania dla')
		if tmp == -1:		# already a movie page
			self.page = ''
		else:			# multiple matches
			self.page = gutils.before(self.page[tmp:],'<div id="mapaSerwisu">');
		return self.page

	def get_searches(self):
		if self.page == '':	# movie page already
			self.number_results = 1
			self.ids.append(self.url)
			self.titles.append(self.title)
		else:			# multiple matches
			elements = string.split(self.page,'<div class="searchItem">')
			if len(elements)>0:
				for element in elements:
					self.ids.append(gutils.trim(element, '<a href="', '"'))
					element = gutils.strip_tags(
						gutils.trim(element, '">', '</div>'))
					element = element.replace("\n", '')
					element = element.replace('   ', '')
					element = element.replace('aka ', ' aka ')
					element = element.replace(' - Oryginalny', '')
					self.titles.append(element)
			else:
				self.number_results = 0
