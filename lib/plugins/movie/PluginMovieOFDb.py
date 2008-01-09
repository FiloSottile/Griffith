# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Written by Christian Sagmueller <christian@sagmueller.net>
# based on PluginMovieIMDB.py, Copyright (c) 2005 Vasco Nunes
# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import movie,string,re

plugin_name = "OFDb"
plugin_description = "Online-Filmdatenbank"
plugin_url = "www.ofdb.de"
plugin_language = _("German")
plugin_author = "Christian Sagmueller, Jessica Katharina Parth"
plugin_author_email = "Jessica.K.P@women-at-work.org"
plugin_version = "0.8"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.ofdb.de/view.php?page=film&fid=%s" % str(self.movie_id)

	def initialize(self):
		# OFDb didn't provide the runtime, studio and classification but it provide a link to the german imdb entry
		# lets use the imdb page, why not
		imdb_nr = gutils.trim(self.page, 'http://german.imdb.com/Title?', '"')
		if imdb_nr != '':
			self.imdb_page = self.open_page(url='http://german.imdb.com/Title?' + imdb_nr)
		else:
			self.imdb_page = ''

	def get_image(self):
		self.image_url = "http://www.ofdb.de/images/film/" + gutils.trim( self.page, "<img src=\"images/film/", "\"" )
		
	def get_o_title(self):
		self.o_title = gutils.trim(self.page, 'Originaltitel:', '</tr>')
		if self.o_title == '':
			self.o_title = gutils.trim(self.page,'size="3"><b>','<')

	def get_title(self):
		self.title = gutils.trim(self.page,'size="3"><b>','<')

	def get_director(self):
		self.director = gutils.trim(self.page,"Regie: ","</a><br>")

	def get_plot(self):
		storyid = self.regextrim(self.page, '([?]|[&])sid=', '(">|[&])')
		story_page = self.open_page(url="http://www.ofdb.de/view.php?page=inhalt&fid=%s&sid=%s" % (str(self.movie_id),storyid))
		self.plot = gutils.trim(story_page, "</b><br><br>","</")

	def get_year(self):
		self.year = gutils.trim(self.page,"Erscheinungsjahr: ","</a>")
		self.year = gutils.strip_tags(self.year)

	def get_runtime(self):
		# from imdb
		self.runtime = gutils.trim(self.imdb_page, '<h5>L&auml;nge:</h5>', ' min')

	def get_genre(self):
		self.genre = gutils.trim(self.page,"Genre(s):","</table>")
		self.genre = string.replace(self.genre, "<br>", ", ")
		self.genre = gutils.strip_tags(self.genre)
		self.genre = string.replace(self.genre, "/", ", ")
		self.genre = gutils.clean(self.genre)
		self.genre = self.genre[0:-1]

	def get_cast(self):
		self.cast = ''
		cast_page = self.open_page(url="http://www.ofdb.de/view.php?page=film_detail&fid=%s" % str(self.movie_id) )
		self.cast = gutils.trim(cast_page, 'Darsteller</i>', '</table>')
		self.cast = re.sub('(\n|\t|&nbsp;)', '', self.cast)
		self.cast = string.replace(self.cast, '\t', '')
		self.cast = string.replace(self.cast, 'class="Daten">', '>\n')
		self.cast = string.strip(gutils.strip_tags(self.cast))
		self.cast = string.replace(self.cast, '... ', _(' as '))
		self.cast = gutils.clean(self.cast)

	def get_classification(self):
		# from imdb
		self.classification = gutils.trim(gutils.trim(self.imdb_page, 'Altersfreigabe:', '</div>'), 'Germany:', '&')

	def get_studio(self):
		# from imdb
		self.studio = gutils.trim(self.imdb_page, '<h5>Firma:</h5>', '</a>')

	def get_o_site(self):
		self.o_site = ""

	def get_site(self):
		self.site = "http://www.ofdb.de/view.php?page=film&fid=" + str(self.movie_id)

	def get_trailer(self):
		self.trailer = ""

	def get_country(self):
		self.country = gutils.trim(self.page,"Herstellungsland: ","</a>")

	def get_rating(self):
		self.rating = gutils.trim(self.page,"<br>Note: ","&nbsp;")
		if self.rating == '':
			self.rating = "0"
		self.rating = str(round(float(self.rating)))

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
		self.original_url_search    = "http://www.ofdb.de/view.php?page=suchergebnis&Kat=Titel&SText="
		self.translated_url_search    = "http://www.ofdb.de/view.php?page=suchergebnis&Kat=Titel&SText="
		self.encode='iso-8859-1'

	def search(self,parent_window):
		self.open_search(parent_window)
		self.page = gutils.trim(self.page,"</b><br><br>", "<br><br><br>");
		self.page = string.replace( self.page, "'", '"' )
		self.page = string.replace( self.page, '<font size="1">', '' )
		self.page = string.replace( self.page, '</font>', '' )
		return self.page

	def get_searches(self):
		elements = string.split(self.page,"<br>")

		if (elements[0]<>''):
			for element in elements:
				elementid = gutils.digits_only( gutils.trim(element,'<a href="view.php?page=film&fid=','">') )
				if elementid != 0:
					self.ids.append(elementid)
					self.titles.append(gutils.trim(element,'">', '</a>'))

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
		'Arahan'				: 3,
		'Ein glückliches Jahr'	: 1
	}

class PluginTest:
	#
	# Configuration for automated tests:
	# dict { movie_id -> dict { arribute -> value } }
	#
	# value: * True/False if attribute only should be tested for any value
	#        * or the expected value
	#
	test_configuration = {
		'103013' : { 
			'title' 			: 'Rocky Balboa',
			'o_title' 			: 'Rocky Balboa',
			'director'			: 'Sylvester Stallone',
			'plot' 				: True,
			'cast'				: 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie\n\
Milo Ventimiglia' + _(' as ') + 'Robert Jr.\n\
Geraldine Hughes\n\
James Francis Kelly III\n\
Tony Burton\n\
A.J. Benza\n\
Henry G. Sanders\n\
Antonio Tarver\n\
Pedro Lovell\n\
Ana Gerena\n\
Angela Boyd\n\
Louis Giansante\n\
Maureen Schilling\n\
Carter Mitchell\n\
Vinod Kumar\n\
Tobias Segal\n\
Tim Carr\n\
Paul Dion Monte\n\
Kevin King Templeton\n\
Robert Michael Kelly\n\
Don Sherman\n\
Nick Baker\n\
Rick Buchborn\n\
Stu Nahan\n\
Gary Compton\n\
Jody Giambelluca\n\
Frank Stallone\n\
Fran Pultro\n\
Michael Buffer\n\
Jack Lazzarado\n\
Marc Ratner\n\
Anthony Lato Jr.\n\
Yahya\n\
Gunnar Peterson\n\
Bernard Fernández\n\
Bert Randolph Sugar\n\
Jim Lampley\n\
Larry Merchant\n\
Max Kellerman\n\
James Binns\n\
Johnnie Hobbs Jr.\n\
Barney Fitzpatrick\n\
Brian Kenny\n\
Dana Jacobson\n\
Skip Bayless\n\
Charles Johnson\n\
Matt Frack\n\
Woody Paige\n\
Jay Crawford\n\
Lahmard J. Tate\n\
LeRoy Neiman\n\
Mike Tyson' + _(' as ') + 'Himself\n\
Lou DiBella\n\
Joe Cortez\n\
Ricky Cavazos',
			'country'			: 'USA',
			'genre'				: 'Action, Drama, Sportfilm',
			'classification'	: False,
			'studio'			: 'Metro-Goldwyn-Mayer (MGM)',
			'o_site'			: False,
			'site'				: 'http://www.ofdb.de/view.php?page=film&fid=103013',
			'trailer'			: False,
			'year'				: 2006,
			'notes'				: False,
			'runtime'			: 102,
			'image'				: True,
			'rating'			: 8
		},
		'22489' : { 
			'title' 			: 'Glückliches Jahr, Ein',
			'o_title' 			: 'Bonne année, La',
			'director'			: 'Claude Lelouch',
			'plot' 				: False,
			'cast'				: 'Lino Ventura\n\
Françoise Fabian\n\
Charles Gérard\n\
André Falcon as Le bijoutier\n\
Mireille Mathieu\n\
Lilo\n\
Claude Mann\n\
Frédéric de Pasquale\n\
Gérard Sire\n\
Silvano Tranquilli\n\
André Barello\n\
Michel Bertay\n\
Norman de la Chesnaye\n\
Pierre Edeline\n\
Pierre Pontiche\n\
Michou\n\
Bettina Rheims\n\
Joseph Rythmann\n\
Georges Staquet\n\
Jacques Villedieu\n\
Harry Walter\n\
Elie Chouraqui',
			'country'			: 'Frankreich',
			'genre'				: 'Komödie, Krimi',
			'classification'	: False,
			'studio'			: 'Les Films 13',
			'o_site'			: False,
			'site'				: 'http://www.ofdb.de/view.php?page=film&fid=22489',
			'trailer'			: False,
			'year'				: 1973,
			'notes'				: False,
			'runtime'			: 90,
			'image'				: True,
			'rating'			: 7
		},
		'54088' : { 
			'title' 			: 'Arahan',
			'o_title' 			: 'Arahan jangpung daejakjeon',
			'director'			: 'Ryoo Seung-wan',
			'plot' 				: True,
			'cast'				: 'Ryoo Seung-beom\n\
Yoon So-yi' + _(' as ') + 'Wi-jin\n\
Ahn Sung-kee' + _(' as ') + 'Ja-woon\n\
Jung Doo-hong' + _(' as ') + 'Heuk-Woon\n\
Yun Ju-sang\n\
Kim Ji-yeong\n\
Baek Chan-gi\n\
Kim Jae-man\n\
Lee Dae-yeon\n\
Kim Dong-ju\n\
Kim Su-hyeon\n\
Geum Dong-hyeon\n\
Lee Jae-goo\n\
Ahn Kil-kang\n\
Bong Tae-gyu\n\
Im Ha-ryong\n\
Yoon Do-hyeon\n\
Lee Choon-yeon',
			'country'			: 'Südkorea',
			'genre'				: 'Action, Fantasy, Komödie',
			'classification'	: '16',
			'studio'			: 'Fun and Happiness',
			'o_site'			: False,
			'site'				: 'http://www.ofdb.de/view.php?page=film&fid=54088',
			'trailer'			: False,
			'year'				: 2004,
			'notes'				: False,
			'runtime'			: 114,
			'image'				: True,
			'rating'			: 7
		}
	}
