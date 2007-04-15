# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Vasco Nunes, Piotr Ożarowski
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
import string, re

plugin_name		= 'IMDb'
plugin_description	= 'Internet Movie Database'
plugin_url		= 'www.imdb.com'
plugin_language		= _('English')
plugin_author		= 'Vasco Nunes, Piotr Ożarowski'
plugin_author_email	= 'griffith-private@lists.berlios.de'
plugin_version		= '1.3'

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
		self.o_title = gutils.trim(self.page, '<h1>', ' <span')

	def get_title(self):	# same as get_o_title()
		self.title = gutils.trim(self.page, '<h1>', ' <span')

	def get_director(self):
		pattern = re.compile('<h5>Directors?:</h5>[\n\s\r]*(.*?)(?:<br/>)?(?:<a[^>]+>more</a>)?\n</div')
		result = pattern.search(self.page)
		if result:
			self.director = result.groups()[0]
			self.director = self.director.replace('<br/>', ', ')

	def get_plot(self):
		self.plot = gutils.trim(self.page, '<h5>Plot Outline:</h5>', '</div>')
		self.plot = self.__before_more(self.plot)

	def get_year(self):
		self.year = gutils.trim(self.page, '<a href="/Sections/Years/', '</a>')
		self.year = gutils.after(self.year, '">')

	def get_runtime(self):
		self.runtime = gutils.trim(self.page, '<h5>Runtime:</h5>', ' min')

	def get_genre(self):
		self.genre = gutils.trim(self.page, '<h5>Genre:</h5>', '</div>')
		self.genre = self.__before_more(self.genre)

	def get_cast(self):
		self.cast = ''
		self.cast = gutils.trim(self.page, '<table class="cast">', '</table>')
		self.cast = string.replace(self.cast, ' ... ', _(' as '))
		self.cast = string.replace(self.cast, '</tr><tr>', "\n")
		self.cast = string.replace(self.cast, '</tr><tr class="even">', "\n")
		self.cast = string.replace(self.cast, '</tr><tr class="odd">', "\n")
		self.cast = self.__before_more(self.cast)

	def get_classification(self):
		self.classification = gutils.trim(self.page, '<h5><a href="/mpaa">MPAA</a>:</h5>', '</div>')
		self.classification = gutils.trim(self.classification, 'Rated ', ' ')

	def get_studio(self):
		self.studio = ''

	def get_o_site(self):
		self.o_site = ''

	def get_site(self):
		self.site = "http://www.imdb.com/title/tt%s" % self.movie_id

	def get_trailer(self):
		self.trailer = "http://www.imdb.com/title/tt%s/trailers" % self.movie_id

	def get_country(self):
		self.country = gutils.trim(self.page, '<h5>Country:</h5>', '</div>')

	def get_rating(self):
		self.rating = gutils.trim(self.page, '<b>User Rating:</b>', '/10')
		if self.rating and self.rating.find('awaiting') == -1:
			try:
				self.rating = float(self.rating)
			except Exception, e:
				self.rating = 0
		else:
			self.rating = 0

	def get_notes(self):
		self.notes = ''
		language = gutils.trim(self.page, '<h5>Language:</h5>', '</div>')
		language = gutils.strip_tags(language)
		color = gutils.trim(self.page, '<h5>Color:</h5>', '</div>')
		color = gutils.strip_tags(color)
		sound = gutils.trim(self.page, '<h5>Sound Mix:</h5>', '</div>')
		sound = gutils.strip_tags(sound)
		tagline = gutils.trim(self.page, '<h5>Tagline:</h5>', '</div>')
		tagline = self.__before_more(tagline)
		tagline = gutils.strip_tags(tagline)
		if len(language)>0:
			self.notes = "%s: %s\n" %(_('Language'), language)
		if len(sound)>0:
			self.notes += "%s: %s\n" %(gutils.strip_tags(_('<b>Audio</b>')), sound)
		if len(color)>0:
			self.notes += "%s: %s\n" %(_('Color'), color)
		if len(tagline)>0:
			self.notes += "%s: %s\n" %('Tagline', tagline)
	
	def __before_more(self, data):
		tmp = string.find(data, '>more<')
		if tmp>0:
			data = data[:tmp] + '>'
		return data

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
