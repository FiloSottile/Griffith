# -*- coding: utf-8 -*-
# vim: encoding=utf-8

__revision__ = '$Id$'

# Copyright (c) 2006 Piotr Ozarowski
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
plugin_author		= 'Piotr Ozarowski'
plugin_author_email	= '<ozarow@gmail.com>'
plugin_version		= '1.2'

class Plugin(movie.Movie):
	def __init__(self, movie_id):
		from md5 import md5
		self.movie_id = md5(movie_id).hexdigest()
		self.encode   = 'utf-8'
		if string.find(movie_id, 'http://') != -1:
			self.url = str(movie_id)
		else:
			self.url = "http://fdb.pl/%s" % str(movie_id)

	def picture(self):
		self.picture_url = gutils.trim(self.page, 'class="moviePosterTable"', '</td>');
		self.picture_url = gutils.trim(self.picture_url,' src="',"\"\n")
		self.picture_url = "http://fdb.pl%s" % self.picture_url

	def original_title(self):
		self.original_title = gutils.trim(self.page,"<div class=\"movieOtherTitle\">\n          ","\n")
		if self.original_title[:4] == 'The ':
			self.original_title = self.original_title[4:] + ', The'

	def title(self):
		self.title = gutils.trim(self.page,'<div class="movieTitle" >','  ')
		if self.title[:4] == 'The ':
			self.title = self.title[4:] + ', The'
		if self.original_title == '':
			self.original_title = self.title

	def director(self):
		self.director = ''
		elements = gutils.trim(self.page,'>Reżyseria</div>','<br />')
		elements = string.split(elements, '<div>')
		if elements[0] != '':
			for element in elements:
				element = gutils.trim(element, '>', '</a')
				if element != '':
					self.director += ', ' + element
			self.director = string.replace(self.director[2:], ', &nbsp;&nbsp;&nbsp;(więcej)', '')

	def plot(self):
		self.plot = gutils.trim(self.page,'>Opis filmu:</div>','</div>')

	def year(self):
		self.year = gutils.trim(self.page,' class="movieYear">(', ')</span>')

	def running_time(self):
		self.running_time = gutils.trim(self.page,">Czas trwania:</span>\n        ",' min')

	def genre(self):
		self.genre = gutils.trim(self.page,'>Gatunek:</span>','</div>')
		self.genre = string.replace(self.genre, '   ', '')

	def with(self):
		self.with = gutils.trim(self.page,'>Obsada:</div>', """<tr>
            <td colspan""")
		if self.with != '':
			self.with = self.with.replace('....',_(' as '))
			self.with = self.with.replace('  ', '')
			self.with = self.with.replace("\n", '')
			self.with = self.with.replace('</tr>', "\n")

	def classification(self):
		self.classification = gutils.trim(self.page,">Od lat:</span>\n","\n")

	def studio(self):
		self.studio = ''

	def site(self):
		self.site = ''

	def imdb(self):
		self.imdb = self.url

	def trailer(self):
		self.trailer = ''

	def country(self):
		self.country = gutils.trim(self.page,">Kraj:</span>\n",'</div>')
		self.country = string.replace(self.country, "   ", '')

	def rating(self):
		self.rating = gutils.trim(self.page, '>Ocena:</span>','/10</span>')
		self.rating = gutils.after(self.rating, 'bold">')
		if self.rating:
			self.rating = str(float(gutils.clean(self.rating)))

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode = 'utf-8'
		self.original_url_search	= 'http://fdb.pl/szukaj.php?s='
		self.translated_url_search	= 'http://fdb.pl/szukaj.php?s='

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
					self.ids.append(gutils.trim(element,"<a href=\"/","\""))
					element = gutils.strip_tags(
								gutils.trim(element,"\">","</div>"))
					element = element.replace("\n", '')
					element = element.replace('   ', '')
					element = element.replace('aka ', ' aka ')
					element = element.replace(' - Oryginalny', '')
					self.titles.append(element)
			else:
				self.number_results = 0
