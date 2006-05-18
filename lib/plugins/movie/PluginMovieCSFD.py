# -*- coding: WINDOWS-1250 -*-
__revision__ = '$Id: PluginMovieCSFD.py 12 2005-11-22 14:21:06Z blondak $'
# Copyright (c) 2005 Blondak
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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import movie,string
import re

plugin_name = "CSFD"
plugin_description = "esko-Slovensk Filmov Databze"
plugin_url = "www.csfd.cz"
plugin_language = _("Czech")
plugin_author = "Blonk"
plugin_author_email = "<blondak@neser.cz>"
plugin_version = "0.2"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.movie_id = id
		self.encode = "WINDOWS-1250"
		self.url = "http://www.csfd.cz/film.php?text=1&rec=&top=&kom=1&id="+str(id)

	def picture(self):
		self.picture_url = gutils.trim(self.page, "img src=\"posters/", "_1.jpg")
		self.picture_url = "http://www.csfd.cz/posters/%s_1.jpg" % self.picture_url

	def original_title(self):
		self.original_title = re.findall(r"/images/flag_[\d]+\.gif'[^>]*></td><td>([^<]*)",self.page)
		if len(self.original_title)>0:
			self.original_title = self.original_title[len(self.original_title)-1]
		else:
			self.original_title = ""

	def title(self):
		self.title = re.search(r"<title>CSFD: (.*) \(",self.page)
		if self.title:
			self.title = self.title.group(1)
		else:
			self.title = ""
		if self.original_title == "":
			self.original_title = self.title

	def director(self):
		self.director = re.search(r"Reie:(.*)<br",self.page)
		if self.director:
			self.director = gutils.strip_tags(self.director.group(1))
		else:
			self.director = ""

	def year(self):
		self.year = re.search(r"<title>CSFD:.*\(([\d]+)\)",self.page)
		if self.year:
			self.year = self.year.group(1)
		else:
			self.year = ""

	def running_time(self):
		self.running_time = re.search(r"/images/flag_[\d]+.gif[^>].*/table>.*<br>.*&nbsp;<br>[^,]+,[^,]*,[^\d]*([\d]+)",self.page)
		if self.running_time:
			self.running_time = gutils.strip_tags(self.running_time.group(1))
		else:
			self.running_time = ""

	def genre(self):
		self.genre = re.search(r"/images/flag_[\d]+.gif[^>].*/table>.*<br>(.*)&nbsp;<br>",self.page)
		if self.genre:
			self.genre = gutils.strip_tags(self.genre.group(1))
		else:
			self.genre = ""

	def country(self):
		self.country = re.search(r"/images/flag_[\d]+.gif[^>].*/table>.*<br>.*&nbsp;<br>([^,]+)",self.page)
		if self.country:
			self.country = gutils.strip_tags(self.country.group(1))
		else:
			self.country = ""

	def with(self):
		self.with = re.search(r"Hraj:(.*)</div></td>",self.page)
		if self.with:
			self.with = gutils.strip_tags(self.with.group(1))
		else:
			self.with = ""

	def plot(self):
		self.plot = gutils.strip_tags(string.replace(gutils.trim(self.page,"Obsah/Info:","</td>"),"(oficiln text distributora)",""))

	def imdb(self):
		self.imdb = re.search(r"href=\"(http://.*\.imdb\.com[^\"]*)",self.page)
		if self.imdb:
			self.imdb = gutils.strip_tags(self.imdb.group(1))
		else:
			self.imdb = ""

	def trailer(self):
		self.trailer = re.search(r"onclick=\"newwin2\('([^']*)'\)[^>]*><img src=\"images/film/trailer.gif",self.page)
		if self.trailer:
			self.trailer = gutils.strip_tags(self.trailer.group(1))
		else:
			self.trailer = ""

	def rating(self):
		self.rating = re.search(r">([\d]+)%&nbsp;",self.page)
		if self.rating:
			self.rating = str(float(self.rating.group(1))/10)
		else:
			self.rating = ""

	def site(self):
		self.site = re.search(r"href=\"([^\"]*)\"[^>]*><img src=\"images/film/www.gif",self.page)
		if self.site:
			self.site = gutils.strip_tags(self.site.group(1))
		else:
			self.site = ""

	def notes(self):
		self.notes = ""

	def studio(self):
		self.studio = ""

	def classification(self):
		self.classification = ""

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.encode = "WINDOWS-1250"
		self.original_url_search   = "http://www.csfd.cz/search_pg.php?search="
		self.translated_url_search = "http://www.csfd.cz/search_pg.php?search="

	def search(self,parent_window):
		self.open_search(parent_window)
		return self.page

	def get_searches(self):
		self.id = self.re_items=re.search(r"window.location.href='http://www.csfd.cz/film.php\?([^']*)'",self.page)
		if self.id:
			self.ids.append(self.id.group(1))
		else:
			self.re_items=re.findall(r"href=[\"]{1}film\.php\?([^\"]+)[^>]*>([^<]+)</a>[ ]*([^<]*)",self.page)
			self.number_results = len(self.re_items)
			if (self.number_results > 0):
				for item in self.re_items:
					self.ids.append(item[0])
					self.titles.append(gutils.convert_entities(item[1])+' '+item[2])

