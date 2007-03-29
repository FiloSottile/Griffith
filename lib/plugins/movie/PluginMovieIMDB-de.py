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

plugin_name         = 'IMDb-de'
plugin_description  = 'Internet Movie Database German'
plugin_url          = 'german.imdb.com'
plugin_language     = _('German')
plugin_author       = 'Michael Jahn'
plugin_author_email = 'mikej06@hotmail.com'
plugin_version      = '1.0'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode = 'utf-8'
		self.movie_id = id
		self.url = "http://german.imdb.com/title/tt%s" % str(self.movie_id)

	def get_image(self):
		tmp = string.find(self.page, 'a name="poster"')
		if tmp == -1:		# poster not available
			self.image_url = ''
		else:
			self.image_url = gutils.trim(self.page[tmp:], 'src="', '"')

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, '<h1>', ' <span')

	def get_title(self):
		self.title = gutils.trim(self.page, '<h1>', ' <span')
		elements = string.split(gutils.trim(self.page, '<h5>Alternativ:', '</div>'), '<i class="transl"')
		if len(elements) > 1:
			for element in elements:
				tmp = gutils.before(gutils.trim(element, '>', '[de]'), '(')
				if tmp <> '':
					self.title = tmp
					break

	def get_director(self):
		self.director = gutils.trim(self.page,'<h5>Regie</h5>', '<br/>\n<br/>')
		self.director = self.__before_more(self.director)
		self.director = self.director.replace('<br/>', ', ')

	def get_plot(self):
		self.plot = gutils.trim(self.page, '<h5>Kurzbeschreibung:</h5>', '</div>')
		self.plot = self.__before_more(self.plot)
		plot_page = self.open_page(url="http://german.imdb.com/title/tt" + str(self.movie_id) + "/plotsummary")
		self.plot = self.plot + '\n\n' + gutils.strip_tags(gutils.trim(plot_page, '<p class="plotpar">', '<div'))

	def get_year(self):
		self.year = gutils.trim(self.page, '<a href="/Sections/Years/', '</a>')
		self.year = gutils.after(self.year, '">')

	def get_runtime(self):
		self.runtime = gutils.trim(self.page, '<h5>L&auml;nge:</h5>', ' min')

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
		self.classification = gutils.trim(gutils.trim(self.page, 'Altersfreigabe:', '</div>'), 'Germany:', '&')

	def get_studio(self):
		self.studio = gutils.trim(self.page, '<h5>Company:</h5>', '</a>')

	def get_o_site(self):
		self.o_site = ''

	def get_site(self):
		self.site = "http://german.imdb.com/title/tt%s" % self.movie_id

	def get_trailer(self):
		self.trailer = "http://german.imdb.com/title/tt%s/trailers" % self.movie_id

	def get_country(self):
		self.country = gutils.trim(self.page, '<h5>Produktionsland:</h5>', '</div>')

	def get_rating(self):
		self.rating = gutils.trim(self.page, '<b>Ihre Bewertung:</b>', '/10')
		if self.rating:
			try:
				self.rating = str(float(gutils.clean(self.rating)))
			except:
				self.rating = ''

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
		tmp = string.find(data, '>mehr...<')
		if tmp>0:
			data = data[:tmp] + '>'
		return data

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search	= 'http://german.imdb.com/find?more=tt&q='
		self.translated_url_search	= 'http://german.imdb.com/find?more=tt&q='
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
