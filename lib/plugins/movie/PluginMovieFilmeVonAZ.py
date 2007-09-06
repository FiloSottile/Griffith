# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2007 Michael Jahn
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

plugin_name = "FilmeVonA-Z.de"
plugin_description = "FILMEvonA-Z.de"
plugin_url = "www.filmevona-z.de"
plugin_language = _("German")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.3"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='utf-8'
		self.movie_id = id
		self.url = 'http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert=' + str(self.movie_id)

	def get_image(self):
		self.image_url = gutils.trim(self.page, 'ProductCover=', '"')
		if not self.image_url == '':
			self.image_url = "http://www.filmevona-z.de/" + self.image_url

	def get_o_title(self):
		self.o_title = string.capwords(
			gutils.clean(gutils.after(
			self.regextrim(self.page, '"[ \t]+class="text_ergebniss_titel"', '[ \t]+[(]Originaltitel[)]'), '</a>')))
		if self.o_title == '':
			self.o_title = gutils.after(gutils.trim(self.page, 'sucheNach=titel', '</a>'), '>')

	def get_title(self):
		self.title = gutils.after(gutils.trim(self.page, 'sucheNach=titel', '</a>'), '>')

	def get_director(self):
		self.director = gutils.after(gutils.trim(self.page, '(Regie)', '</a>'), '>')

	def get_plot(self):
		self.plot = gutils.after(self.regextrim(self.page, '[(]Darsteller[)]', '</[pP]>'), '<p>')

	def get_year(self):
		self.year = gutils.after(gutils.trim(self.page, 'sucheNach=produktionsjahr', '</a>'), '>')

	def get_runtime(self):
		self.runtime = gutils.trim(self.page, 'L&auml;nge: ', ' Minuten')

	def get_genre(self):
		elements = string.split(self.page, 'sucheNach=genre')
		if (elements[0]<>''):
			elements[0] = ''
			self.delimiter = ''
			self.genre = ''
			for element in elements:
				if (element <> ''):
					self.genre += self.delimiter + gutils.trim(element, '>', '</a>')
					self.delimiter = ", "

	def get_cast(self):
		self.cast = self.regextrim(self.page, '[(]Darsteller[)]', '<[pP]>')
		self.cast = gutils.clean(self.cast)
		self.cast = self.cast.replace(' als ', _(' as '))
		self.cast = self.cast.replace('		', '')
		self.cast = self.cast.replace('\r\n', '')
		self.cast = self.cast.replace(', ', '\n')
		self.cast = self.cast.replace(',', '')

	def get_classification(self):
		self.classification = self.regextrim(self.page, 'FSK:[ ]+', '[,;]')

	def get_studio(self):
		self.studio = gutils.after(gutils.trim(self.page, 'sucheNach=produktionsfirma', '</a>'), '>')

	def get_o_site(self):
		self.o_site = ''

	def get_site(self):
		self.site = 'http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert=' + self.movie_id;

	def get_trailer(self):
		self.trailer = ''

	def get_country(self):
		self.country = gutils.after(gutils.trim(self.page, 'sucheNach=produktionsland', '</a>'), '>')

	def get_rating(self):
		self.rating = 0
		
	def regextrim(self,text,key1,key2):
		obj = re.search(key1, text)
		if obj is None:
			return ''
		else:
			p1 = obj.end()
		obj = re.search(key2, text[p1:])
		if obj is None:
			return ''
		else:
			p2 = p1 + obj.start()
		return text[p1:p2]

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.original_url_search	= "http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert="
		self.translated_url_search	= "http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert="
		self.encode='utf-8'

	def search(self,parent_window):
		self.open_search(parent_window)
		# used for looking for subpages
		tmp_page = gutils.trim(self.page, "Treffer-Seite", "chste Seite")
		elements = string.split(tmp_page, '" class="text_navi">')
		# first results
		tmp_page = gutils.after(gutils.trim(self.page,"Alle Treffer aus der Kategorie", "Treffer-Seite"), "Titel:")
		# look for subpages
		for element in elements:
			element = gutils.before(element, "</a>")
			try:
				tmp_element = int(element)
			except:
				tmp_element = 1
			if (tmp_element <> 1):
				self.url = "http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&currentPage=" + str(tmp_element) + "&wert="
				self.open_search(parent_window)
				tmp_page2 = gutils.trim(self.page,"Alle Treffer aus der Kategorie", "Treffer-Seite")
				tmp_page = tmp_page + tmp_page2
		self.page = tmp_page

		return self.page

	def get_searches(self):
		elements = string.split(self.page,'class="text_ergebniss_titel"')
		i = 0
		while i < len(elements) - 1:
			id_part = elements[i]
			i = i + 1
			text_part = elements[i]
			i = i + 1
			self.ids.append(gutils.trim(id_part, 'filmsuche.cfm?wert=', '&'))
			self.titles.append(gutils.strip_tags(
						gutils.trim(text_part, '>', '</a>') + ' (' +
						string.capwords(gutils.trim(text_part, '</a>', '(Originaltitel)')) + ', ' +
						gutils.after(gutils.trim(text_part, 'sucheNach=produktionsland', '</a>'), '>') + ', ' +
						gutils.after(gutils.trim(text_part, 'sucheNach=produktionsjahr', '</a>'), '>') +
						')'))

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
	#
	# Configuration for automated tests:
	# dict { movie_id -> expected result count }
	#
	test_configuration = {
		'Rocky Balboa'			: 1,
		'Arahan'				: 1,
		'Ein glückliches Jahr'	: 0
	}

class PluginTest:
	#
	# Configuration for automated tests:
	# dict { movie_id -> dict { arribute -> value } }
	#
	# value: * True/False if attribute should only be tested for any value
	#        * or the expected value
	#
	test_configuration = {
		'528267' : { 
			'title' 			: 'Rocky Balboa',
			'o_title' 			: 'Rocky Balboa',
			'director'			: 'Sylvester Stallone',
			'plot' 				: True,
			'cast'				: 'A.J. Benza' + _(' as ') + 'L.C.\n\
Milo Ventimiglia' + _(' as ') + 'Rocky jr.\n\
Antonio Tarver' + _(' as ') + 'Mason \'The Line\' Dixon\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie\n\
Tony Burton' + _(' as ') + 'Duke',
			'country'			: 'USA',
			'genre'				: 'Boxerfilm',
			'classification'	: 'ab 12',
			'studio'			: 'Columbia Pic./ MGM/ Rogue Marble/ Revolution Studios/ Chartoff-Winkler Prod.',
			'o_site'			: False,
			'site'				: 'http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert=528267',
			'trailer'			: False,
			'year'				: 2006,
			'notes'				: False,
			'runtime'			: 102,
			'image'				: True,
			'rating'			: False
		},
		'26956' : { 
			'title' 			: 'Bürgschaft für ein Jahr',
			'o_title' 			: 'Bürgschaft für ein Jahr',
			'director'			: 'Herrmann Zschoche',
			'plot' 				: True,
			'cast'				: 'Heide Kipp' + _(' as ') + 'Frau Braun\n\
Jan Spitzer' + _(' as ') + 'Werner Horn\n\
Monika Lennartz' + _(' as ') + 'Irmgard Behrend\n\
Katrin Saß' + _(' as ') + 'Nina\n\
Ursula Werner' + _(' as ') + 'Frau Müller\n\
Christian Steyer' + _(' as ') + 'Heiner Menk\n\
Jaecki Schwarz' + _(' as ') + 'Peter Müller\n\
Barbara Dittus' + _(' as ') + 'Heimleiterin',
			'country'			: 'DDR',
			'genre'				: 'Arbeiterfilm, Frauenfilm, Literaturverfilmung',
			'classification'	: 'ab 6',
			'studio'			: 'DEFA, Gruppe "Berlin"',
			'o_site'			: False,
			'site'				: 'http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert=26956',
			'trailer'			: False,
			'year'				: 1981,
			'notes'				: False,
			'runtime'			: 93,
			'image'				: False,
			'rating'			: False
		},
		'524017' : { 
			'title' 			: 'Arahan',
			'o_title' 			: 'Arahan Jangpung Daejakjeon',
			'director'			: 'Ryoo Seung-wan',
			'plot' 				: True,
			'cast'				: 'Yoon So-yi' + _(' as ') + 'Wi-jin\n\
Yun Ju-sang' + _(' as ') + 'Mu-woon\n\
Ahn Sung-kee' + _(' as ') + 'Ja-woon\n\
Jung Doo-hong' + _(' as ') + 'Heukwoon\n\
Ryu Seung-beom' + _(' as ') + 'Sang-hwan',
			'country'			: 'Südkorea',
			'genre'				: False,
			'classification'	: 'ab 16',
			'studio'			: 'Fun and Happiness/ Good Movie',
			'o_site'			: False,
			'site'				: 'http://www.filmevona-z.de/filmsuche.cfm?sucheNach=Titel&wert=524017',
			'trailer'			: False,
			'year'				: 2004,
			'notes'				: False,
			'runtime'			: 108,
			'image'				: True,
			'rating'			: False
		}
	}
