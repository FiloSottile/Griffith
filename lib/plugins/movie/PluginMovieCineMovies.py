# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005 Vasco Nunes
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
import movie,string

plugin_name = "Cinemovies"
plugin_description = "Cinemovies"
plugin_url = "www.cinemovies.fr"
plugin_language = _("French")
plugin_author = "Vasco Nunes"
plugin_author_email="<vasco.m.nunes@gmail.com>"
plugin_version = "0.1"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.cinemovies.fr/fiche_film.php?IDfilm=" + str(self.movie_id)

	def picture(self):
		self.picture_url = "http://www.cinemovies.fr/images/data/films/Pfilm"
		self.picture_url = self.picture_url + string.strip(gutils.trim(self.page,"data/films/Pfilm",".jpg")) + ".jpg"

	def original_title(self):
		self.original_title = string.capwords(gutils.trim(self.page,"Titre original</b></td>","</td>"))

	def title(self):
		self.title = string.capwords(gutils.trim(self.page,"<TR><TD class=\"arial12blacknews\">"," :</TD></TR><TR><TD"))

	def director(self):
		self.director = string.strip(gutils.trim(self.page," par:</b></td>","</a>"))

	def plot(self):
		self.plot = gutils.trim(self.page,"L'histoire</font></td>","</p><br>")

	def year(self):
		self.year = gutils.trim(self.page,"<B>Ano:</B> <FONT SIze=-1>","</FONT>")

	def running_time(self):
		self.running_time = gutils.trim(self.page,"height=\"12\">Durée: ","</td>")

	def genre(self):
		self.genre = gutils.trim(self.page,"Genre: ","</b></a>")

	def with(self):
		self.with = ""
		self.with = gutils.trim(self.page,"<b>Avec:</b>","</tr>")

	def classification(self):
		self.classification = gutils.trim(self.page,"<B>Idade:</B> <FONT SIze=-1>","</FONT>")

	def studio(self):
		self.studio = string.strip(gutils.trim(self.page,"&nbsp;Studio/Distributeur</b></td>","</td>"))

	def site(self):
		self.site = gutils.trim(self.page,"<A HREF='", "' TARGET=_blank><IMG SRC='/imagens/bf_siteoficial.gif'")

	def imdb(self):
		self.imdb = gutils.trim(self.page,"/imagens/bf_siteoficial.gif' WIDTH=89 HEIGHT=18 BORDER=0 ALT=''>", "' TARGET=_blank><IMG SRC='/imagens/bf_imdb.gif'")
		self.imdb = gutils.after(self.imdb,"<A HREF='")
		self.imdb = string.replace(self.imdb,"'","")

	def trailer(self):
		self.trailer = gutils.trim(self.page,"/imagens/bf_imdb.gif' WIDTH=89 HEIGHT=18 BORDER=0 ALT=''>", "' TARGET=_blank><IMG SRC='/imagens/bf_trailer.gif'")
		self.trailer = gutils.after(self.trailer,"<A HREF='")

	def country(self):
		self.country = string.strip(gutils.trim(self.page,"&nbsp;Pays</b></td>","</td>"))

	def rating(self):
		tmp_rating = gutils.trim(self.page,"<td width=\"100%\" class=\"arial12blacknews\"><p align=\"center\"><font size=\"5\">","/5</font></td>")
		if tmp_rating != "":
			self.rating = str(float(tmp_rating)*2)
		else:
			self.rating = ""

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode='iso-8859-1'
		self.original_url_search	= "http://www.cinemovies.fr/resultat_recherche.php?cherche="
		self.translated_url_search	= "http://www.cinemovies.fr/resultat_recherche.php?cherche="

	def search(self,parent_window):
		self.open_search(parent_window)
		self.sub_search()
		return self.page

	def sub_search(self):
		self.page = gutils.trim(self.page,"height=\"6\">Films</td>", "height=\"6\">News</td>")

	def get_searches(self):
		elements = string.split(self.page,"</tr>  <tr>")
		self.number_results = elements[-1]

		if (elements[0]<>''):
			for element in elements:
				self.ids.append(gutils.trim(element,"?IDfilm=","\" class=\"arial"))
				self.titles.append(gutils.convert_entities(gutils.strip_tags(gutils.trim(element,"12black3\">","</font><br>"))))
		else:
			self.number_results = 0
