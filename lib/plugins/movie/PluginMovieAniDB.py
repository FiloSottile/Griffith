# -*- coding: iso-8859-1 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2006 Piotr OĹźarowski
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
from gutils import decompress

plugin_name         = 'AnimeDB'
plugin_description  = 'Anime DataBase'
plugin_url          = 'www.anidb.info'
plugin_language     = _('English')
plugin_author       = 'Piotr Ozarowski'
plugin_author_email = '<ozarow+griffith@gmail.com>'
plugin_version      = '2.1'

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode = 'iso-8859-1'
		if string.find(id, 'http://') != -1:
			self.url = str(id)
			self.movie_id = 'anidb'
		else:
			self.movie_id = str(id)
			self.url = "http://anidb.info/perl-bin/animedb.pl?show=anime&aid=%s" % self.movie_id

	def initialize(self):
		self.page = decompress(self.page)
		if self.movie_id == 'anidb':
			self.movie_id = gutils.trim(self.page, 'animedb.pl?show=addgenren&aid=', '&')
			self.url = "http://anidb.info/perl-bin/animedb.pl?show=anime&aid=%s" % self.movie_id
		self.page = gutils.trim(self.page, '<h1>Show Anime - ',"<table border=0>\n\t<tr>")

	def get_image(self):
		match = re.search('http://img\d*.anidb.info/pics/anime/\d*.jpg', self.page)
		if match is not None:
			self.image_url = match.group()
		else:
			self.image_url = ''

	def get_o_title(self):
		self.o_title = gutils.trim(self.page, '<td> Title: </td>', '</td>')
		self.o_title = gutils.after(self.o_title, '<td> ')
		self.o_title = re.sub(' \(\d*\)', '', self.o_title)

	def get_title(self):
		self.title = gutils.trim(self.page,'<td> English: </td>', ' </td>')
		self.title = gutils.after(self.title, '<td> ')
		if self.title == '':
			self.title = gutils.gdecode(self.o_title, self.encode)

	def get_director(self):
		self.director = ''

	def get_plot(self):
		self.plot = gutils.trim(self.page,"<tr>\n\t<td>\n\t    ","\n\t</td>")
		self.plot = string.replace(self.plot,"<br />","\n")
		self.plot = gutils.strip_tags(self.plot)

	def get_year(self):
		self.year = gutils.trim(self.page, '<td> Year: </td>', '</td>')
		self.year = gutils.after(self.year, '<td> ')[:4]

	def get_runtime(self):
		self.runtime = ''

	def get_genre(self):
		self.genre = gutils.trim(self.page, '>Genre:<', '[similar]</a> </td>')
		self.genre = gutils.after(self.genre, '<td> ')
		self.genre = gutils.strip_tags(self.genre)
		if self.genre[len(self.genre)-3:] == ' - ':
			self.genre =  self.genre[:-3]
		elif self.genre == '-':
			self.genre = ''

	def get_cast(self):
		self.cast = ''

	def get_classification(self):
		self.classification = ''

	def get_studio(self):
		self.studio = gutils.trim(self.page, '<td> Companies: </td>', ' </td>')
		self.studio = gutils.after(self.studio, '<td> ')
		self.studio = gutils.strip_tags(self.studio)
		if self.studio[:2] == " (":
			self.studio = self.studio[2:]
			if self.studio[len(self.studio)-1:] == ')':
				self.studio = self.studio[:len(self.studio)-1]

	def get_o_site(self):
		self.o_site = gutils.trim(self.page, '<td> URL: </td>', ' </td>')
		self.o_site = gutils.after(self.o_site, 'href="')
		self.o_site = gutils.before(self.o_site, '" ')

	def get_site(self):
		self.site = self.url

	def get_trailer(self):
		self.trailer = ''

	def get_country(self):
		self.country = ''

	def get_rating(self):
		self.rating = gutils.trim(self.page, '<td> Rating: </td>', ' </td>')
		self.rating = gutils.after(self.rating, '<td> ')
		self.rating = gutils.before(self.rating,' ')
		if self.rating != '':
			self.rating = str( float(self.rating) )
	def get_notes(self):
		self.notes = ''
		# ...type
		atype = gutils.trim(self.page, '<td> Type: </td>',' </td>')
		atype = gutils.after(atype, '<td> ')
		if atype != '':
			self.notes += "Type: %s\n" % atype
		# ...number of episodes
		episodes = gutils.trim(self.page, '<td> Episodes: </td>', ' </td>')
		episodes = gutils.after(episodes, '<td> ')
		if episodes != '':
			self.notes += "Episodes: %s\n" % episodes

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode = "iso-8859-1"
		self.original_url_search	= 'http://anidb.info/perl-bin/animedb.pl?show=animelist&adb.search='
		self.translated_url_search	= 'http://anidb.info/perl-bin/animedb.pl?show=animelist&adb.search='

	def search(self,parent_window):
		self.open_search(parent_window)
		self.page = decompress(self.page)

		tmp = string.find(self.page, '<h1>Anime List - Search for: ')
		if tmp == -1:		# already a movie page
			self.page = ''
		else:			# multiple matches
			self.page = gutils.trim(self.page, '>hide synonyms</a><hr>', '<hr>');
			self.page = gutils.after(self.page, '</tr>');

		return self.page

	def get_searches(self):
		if self.page == '':	# already a movie page
			self.number_results = 1
			self.ids.append(self.url)
			self.titles.append(self.title)
		else:			# multiple matches
			elements = string.split(self.page,"<tr>")
			self.number_results = elements[-1]

			if len(elements[0]):
				for element in elements:
					element = gutils.trim(element, '<td', '</td>')
					self.ids.append(gutils.trim(element, 'animedb.pl?show=anime&aid=','"'))
					element = gutils.after(element, '">')
					element = gutils.strip_tags(element)
					self.titles.append(element)
			else:
				self.number_results = 0

