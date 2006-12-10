# -*- coding: iso-8859-15 -*-

__revision__ = '$Id: PluginMovieCulturalia.py 389 2006-07-29 18:43:35Z piotrek $'

# Copyright (c) 2006 Pedro D. Sánchez
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

plugin_name		= 'Culturalia'
plugin_description	= 'Base de Datos de Peliculas'
plugin_url		= 'www.culturalianet.com'
plugin_language		= _('Spanish')
plugin_author		= 'Pedro D. Sánchez'
plugin_author_email	= '<pedrodav@gmail.com>'
plugin_version		= '0.1'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='iso-8859-15'
		self.movie_id = id
		self.url = "http://www.culturalianet.com/art/ver.php?art=%s" % str(self.movie_id)

	def picture(self):
		tmp = string.find(self.page, "<font class = 'titulo2'>")
		if tmp == -1:
			self.picture_url = ''
		else:
			self.picture_url = 'http://www.culturalianet.com/art/'+gutils.trim(self.page[tmp:], '<img src = "', '"')

	def original_title(self):
		self.original_title = gutils.trim(self.page, "<font class = 'titulo2'>", '</i>')
		self.original_title = gutils.after(self.original_title, '<i>')

	def title(self):
		self.title = gutils.trim(self.page, "<font class = 'titulo2'>", '. (')

	def director(self):
		self.director = gutils.trim(self.page,"<font class = 'titulo3'>Director:", '<br><br>')

	def plot(self):
		self.plot = gutils.trim(self.page, '<b>Sinopsis:</b><br>', '<br><br>')

	def year(self):
		self.year = gutils.trim(self.page, "<font class = 'titulo2'>", ')</font>')
		self.year = gutils.after(self.year, '. (')

	def running_time(self):
		self.running_time = gutils.trim(self.page, "<font class = 'titulo3'>Duración:</font> ", ' minutos')
		if self.running_time == '':
		    self.running_time = gutils.trim(self.page, "<font class = 'titulo3'>Duraci&oacute;n:</font> ", ' minutos')

	def genre(self):
		self.genre = gutils.trim(self.page, "<font class = 'titulo3'>Género:</font><br>", '<br><br>')

	def with(self):
		self.with = ''
		self.with = gutils.trim(self.page, "<font class = 'titulo3'>Actores:</font><br>", '<br><br>')
		self.with = string.replace(self.with, '<br>', "\n")
		self.with = string.strip(gutils.strip_tags(self.with))

	def classification(self):
	    self.classification = gutils.trim(self.page, "<font class = 'titulo3'>Calificación moral:</font> ", '<br>')
	    if self.classification == '':
	        self.classification = gutils.trim(self.page, "<font class = 'titulo3'>Calificaci&oacute;n moral:</font> ", '<br>')

	def studio(self):
		self.studio = ''

	def site(self):
		self.site = ''

	def imdb(self):
		self.imdb = "http://www.culturalianet.com/art/ver.php?art=%s" % str(self.movie_id)

	def trailer(self):
		self.trailer = ''

	def country(self):
		self.country = gutils.trim(self.page, "<font class = 'titulo3'>Nacionalidad:</font><br>", '<br>')

	def rating(self):
		self.rating = gutils.trim(self.page, "Puntuación: <font class = 'titulo3'>", '</font>')
		if self.rating == '':
		    self.rating = gutils.trim(self.page, "Puntuaci&oacute;n: <font class = 'titulo3'>", '</font>')
		if self.rating:
			self.rating = str(float(gutils.clean(self.rating)))

class SearchPlugin(movie.SearchMovie):

	def __init__(self):
		self.original_url_search	= 'http://www.culturalianet.com/bus/resu.php?donde=1&texto='
		self.translated_url_search	= 'http://www.culturalianet.com/bus/resu.php?donde=1&texto='
		self.encode = 'iso-8859-15'

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		self.page = gutils.trim(self.page, '<b>ARTICULOS ENCONTRADOS:</b>', '</table>')
		self.page = gutils.after(self.page, '</td></tr><tr><td><b>')
		#self.page = self.page.decode('iso-8859-15')

	def get_searches(self):
		elements = string.split(self.page, '<td><b>')

		if (elements[0]<>''):
			for element in elements:
				self.ids.append(gutils.trim(element, 'ver.php?art=',"'"))
				self.titles.append(gutils.strip_tags(gutils.convert_entities(gutils.trim(element, "target='_top'>", '</a>'))))
