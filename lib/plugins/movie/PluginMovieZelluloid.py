# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007 Michael Jahn
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

plugin_name         = 'Zelluloid.de'
plugin_description  = 'ZELLULOID.DE'
plugin_url          = 'www.zelluloid.de'
plugin_language     = _('German')
plugin_author       = 'Michael Jahn'
plugin_author_email = '<mikej06@hotmail.com>'
plugin_version      = '1.0'

class Plugin(movie.Movie):
	index_url = 'http://www.zelluloid.de/filme/index.php3?id='
	
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.zelluloid.de/filme/details.php3?id=" + self.movie_id

	def initialize(self):
		self.detail_page = self.page
		self.url = self.index_url + self.movie_id
		self.page = self.open_page(url=self.url)

	def get_image(self):
		self.image_url = 'http://www.zelluloid.de/images/poster/' + gutils.trim(self.page, '<IMG SRC="/images/poster/', '"');

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, 'Originaltitel: ', '<BR>')
		if self.o_title == '':
			self.o_title = gutils.trim(self.page, '<TITLE>', '|')

	def get_title(self):
		self.title = gutils.trim(self.page, '<TITLE>', '|')

	def get_director(self):
		self.director = gutils.trim(self.detail_page, 'Regie', '</A>')

	def get_plot(self):
		self.plot = gutils.trim(self.page, '<DIV CLASS=bigtext>', '</DIV>')
		
	def get_year(self):
		self.year = ''
		elements = string.split(self.detail_page, '/directory/az.php3?j')
		elements[0] = ''
		delimiter = ''
		for element in elements:
			if element <> '':
				self.year = self.year + delimiter + gutils.trim(element, '>', '<')
				delimiter = ', '

	def get_runtime(self):
		self.runtime = gutils.trim(self.detail_page, 'ca.&nbsp;', '&nbsp;min');

	def get_genre(self):
		self.genre = ''
		elements = string.split(self.detail_page, '/directory/az.php3?g')
		elements[0] = ''
		delimiter = ''
		for element in elements:
			if element <> '':
				self.genre = self.genre + delimiter + gutils.trim(element, '>', '<')
				delimiter = ', '

	def get_cast(self):
		self.cast = gutils.trim(self.detail_page, '<B>Besetzung</B>', '<TD COLSPAN=')
		self.cast = self.cast.replace('<A HREF=', '--flip--' + '<A HREF=')
		self.cast = gutils.strip_tags(self.cast)
		elements = self.cast.split('\n')
		self.cast = ''
		for element in elements:
			elements2 = element.split("--flip--")
			if len(elements2) > 1:
				self.cast += elements2[1] + '--flip--' + elements2[0] + '\n'
			else:
				self.cast += element + '\n'
		self.cast = string.replace(self.cast, '--flip--', _(' as '))

	def get_classification(self):
		self.classification = gutils.trim(self.detail_page, 'FSK: ', '</TD>')
		self.classification = re.sub(',.*', '', self.classification)

	def get_studio(self):
		self.studio = gutils.strip_tags(gutils.trim(self.detail_page, '<B>Produktion</B>', '&nbsp;'))
		if self.studio == '':
			self.studio = gutils.trim(self.detail_page, '<B>Produktion</B>', '</TABLE>')
		self.studio = self.studio.replace('\n', ', ')
		self.studio = re.sub('((^, )|(, $))', '', self.studio)
		
	def get_o_site(self):
		self.o_site = ""

	def get_site(self):
		self.site = "http://www.zelluloid.de/filme/details.php3?id=" + self.movie_id

	def get_trailer(self):
		self.trailer = ""

	def get_country(self):
		self.country = ''
		elements = string.split(self.detail_page, '/directory/az.php3?l')
		elements[0] = ''
		delimiter = ''
		for element in elements:
			if element <> '':
				self.country = self.country + delimiter + gutils.trim(element, '>', '<')
				delimiter = ', '

	def get_rating(self):
		self.rating = gutils.strip_tags(gutils.trim(self.page, 'User-Wertung:', '</TABLE>'))
		self.rating = self.rating.replace('%', '')
		self.rating = self.rating.replace('&nbsp;', '')
		try:
			ratingint = int(self.rating) / 10
		except:
			ratingint = 0
		self.rating = str(ratingint)

	def get_notes(self):
		self.notes = ""

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search   = "http://www.zelluloid.de/suche/index.php3?qstring="
		self.translated_url_search = "http://www.zelluloid.de/suche/index.php3?qstring="
		self.encode='iso-8859-1'

	def search(self,parent_window):
		self.open_search(parent_window)
		tmp = gutils.before(gutils.trim(self.page, "Der Suchbegriff erzielte", "</TABLE>"), 'ALT="Person"')
		if tmp == '':
			tmp = gutils.trim(self.page, "Der Suchbegriff erzielte", "</TABLE>")
		return tmp

	def get_searches(self):
		elements = string.split(self.page, "hit.php3?hit=")
		elements[0] = ''
		for element in elements:
			if element <> '':
				self.ids.append(gutils.trim(element, 'movie-', '-'))
				self.titles.append(gutils.strip_tags(gutils.trim(element, '>', '</A>')))
