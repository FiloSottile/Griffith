# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2006 Vasco Nunes, Piotr Ożarowski
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

plugin_name		= 'IMDb'
plugin_description	= 'Internet Movie Database'
plugin_url		= 'www.imdb.com'
plugin_language		= _('English')
plugin_author		= 'Vasco Nunes'
plugin_author_email	= '<vasco.m.nunes@gmail.com>'
plugin_version		= '1.0'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode = 'utf-8'
		self.movie_id = id
		self.url = "http://imdb.com/title/tt%s" % str(self.movie_id)

	def get_image(self):
		tmp = string.find(self.page, 'a name="poster"')
		if tmp == -1:		# poster not available
			self.image_url = ''
		else:
			self.image_url = gutils.trim(self.page[tmp:], 'src="', '"')

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, '<strong class="title">', ' <small>')

	def get_title(self):
		self.title = gutils.trim(self.page, '<strong class="title">', ' <small>')

	def get_director(self):
		self.director = gutils.trim(self.page,'Directed by</b><br>', '<br>')

	def get_plot(self):
		self.plot = gutils.trim(self.page, '<b class="ch">Plot', '<a href="/rg/title-tease/plot')
		self.plot = gutils.after(self.plot, ':</b> ')

	def get_year(self):
		self.year = gutils.trim(self.page, '<a href="/Sections/Years/', '</a>)</small>')
		self.year = gutils.after(self.year, '">')

	def get_runtime(self):
		self.runtime = gutils.trim(self.page, '<b class="ch">Runtime:</b>', ' min')

	def get_genre(self):
		self.genre = gutils.trim(self.page, '<a href="/Sections/Genres/', '<br>')
		self.genre = gutils.after(self.genre, '/">')
		self.genre = string.replace(self.genre, '(more)', '')

	def get_cast(self):
		self.cast = ''
		self.cast = gutils.trim(self.page, 'Cast overview, first billed only:', '<a href="fullcredits">')
		if (self.cast==''):
			self.cast = gutils.trim(self.page, 'cast: ','<a href="fullcredits">')
		self.cast = string.replace(self.cast, ' .... ', _(' as '))
		self.cast = string.replace(self.cast, '</tr><tr>', "\n")
		self.cast = string.replace(self.cast, '</tr><tr bgcolor="#FFFFFF">', "\n")
		self.cast = string.replace(self.cast, '</tr><tr bgcolor="#F0F0F0">', "\n")
		self.cast = string.strip(gutils.strip_tags(self.cast))

	def get_classification(self):
		self.classification = gutils.trim(self.page, 'MPAA</a>:</b> ', '.<br>')
		self.classification = ''

	def get_studio(self):
		self.studio = ''

	def get_o_site(self):
		self.o_site = ''

	def get_site(self):
		self.site = "http://www.imdb.com/title/tt%s" % self.movie_id

	def get_trailer(self):
		self.trailer = "http://www.imdb.com/title/tt%s/trailers" % self.movie_id

	def get_country(self):
		self.country = gutils.trim(self.page, '<b class="ch">Country:</b>', '</a>')
		self.country = gutils.after(self.country, '/">')

	def get_rating(self):
		self.rating = gutils.trim(self.page, '<b class="ch">User Rating:</b>', '/10</b> (')
		if self.rating:
			self.rating = str(float(gutils.clean(self.rating)))

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search	= 'http://imdb.com/find?more=tt;q='
		self.translated_url_search	= 'http://imdb.com/find?more=tt;q='
		self.encode = 'utf-8'

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		self.page = gutils.trim(self.page, '</b> found the following results:', '<b>Suggestions For Improving Your Results</b>');
		self.page = self.page.decode('iso-8859-1')

	def get_searches(self):
		elements = string.split(self.page, '<li>')

		if (elements[0]<>''):
			for element in elements:
				self.ids.append(gutils.trim(element, '/title/tt','/?fr='))
				self.titles.append(gutils.strip_tags(gutils.convert_entities(gutils.trim(element, ';fm=1">', '</li>'))))
