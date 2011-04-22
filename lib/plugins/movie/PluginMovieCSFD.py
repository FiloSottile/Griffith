# -*- coding: utf-8 -*-
__revision__ = '$Id: PluginMovieCSFD.py 12 2011-05-22 08:37:14Z KamilHanus $'
# Copyright (c) 2011 Kamil Hanus
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
# Foundation, 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import movie,string
import re

plugin_name = "CSFD"
plugin_description = "Cesko-Slovenska Filmova Databaze"
plugin_url = "www.csfd.cz"
plugin_language = _("Czech")
plugin_author = "Kamil Hanus"
plugin_author_email = "<kamilhanus@gmail.com>"
plugin_version = '1.1'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.movie_id = id
        self.encode = "utf-8"
        self.url = "http://www.csfd.cz"+str(id)

    def get_image(self):
        self.image_url = re.search(r"content=\"http://img.csfd.cz/posters/([^\"]*)\"",self.page)
        if self.image_url:
            self.image_url = "http://img.csfd.cz/posters/" + gutils.strip_tags(self.image_url.group(1))
        else:
            self.image_url = ""


    def get_title(self, ret=False):
        data = re.search(r'<title>*>([^>]*)',self.page)
        if data:
            if len(data.group(1).split("/")) == 2:
		data = data.group(1).split(" | ")[0][:-7]
	    else:
		data = data.group(1).split(" / ")[0]
        else:
            data = ""
        if ret is True:
            return data
        else:
            self.title = data


    def get_o_title(self):
        self.o_title = re.findall(r'/images/flags/flag_[\d]+.gif"[^<]*>([^/]*)',self.page)
        if len(self.o_title)>0:
            self.o_title = self.o_title[0]
	    self.o_title = self.o_title[11:-1]
        else:
            self.o_title = ""
        if self.o_title == "":
            self.o_title = self.get_title(True)



    def get_director(self):
	a=re.sub("\t", "", self.page)
	a=re.sub("\n", "", a)
	try:
	    b = re.search(r'data-truncate="60">(.*)</span></div><div>',a).group()
	    b = re.search(r"<a(.*)</span", b).group()[:-6]
	    b = b.split(",")

	    self.director=""
	    for i in b:
	        self.director=self.director + ", "+i[:-4].split(">")[-1]
	    if self.director[0] == ",":
	        self.director=self.director[2:]
	except:
	    self.director=""
	if self.director=="":
	    try:
		b = re.search(r'data-truncate="60">(.*)</a></span></div>',a).group()

		b = re.search(r"<a(.*)</span", b).group()[:-6]
		b = b.split(",")

		self.director=""
	        for i in b:
	            self.director=self.director + ", "+i[:-4].split(">")[-1]
	        if self.director[0] == ",":
	            self.director=self.director[2:]
	    except:
		self.director=""


    def get_year(self):
        self.year = re.search(r'<p class="origin"[^<]*>([^>]*)', self.page)
        if self.year:
            self.year = self.year.group()[18:-7].split(", ")[-2]
        else:
            self.year = ""

    def get_runtime(self):
        self.runtime = re.search(r'<p class="origin"[^<]*>([^>]*)', self.page)
        if self.runtime:
	    self.runtime = self.runtime.group()[18:-7].split(", ")[-1]

        else:
            self.runtime = ""

    def get_genre(self):
	try:
            self.genre = re.search(r'<p class="genre"[^<]*>([^>]*)',self.page).group()[17:-3]
        except:
            self.genre = ""

    def get_country(self):
        self.country = re.search(r'<p class="origin"[^<]*>([^>]*)', self.page)
        if self.country:
            self.country = self.country.group()[18:-7].split(", ")[0]
        else:
            self.country = ""

    def get_cast(self):
	a=re.sub("\t", "", self.page)
	a=re.sub("\n", "", a)
	try:
	    b = re.search(r'data-truncate="280">(.*)</span></div></div>',a).group()
	    b = re.search(r"<a(.*)</span", b).group()[:-6]
	    b = b.split(",")
	
	    self.cast=""
	    for i in b:
	        self.cast=self.cast + ", "+i[:-4].split(">")[-1]
	    if self.cast[0] == ",":
	        self.cast=self.cast[2:]
	except:
	    self.cast=""

    def get_plot(self):

	a= re.sub("\t", "", self.page)
	a= re.sub("\n", "", a)
	a= re.sub("<BR>", "", a)
	try:
            self.plot = re.search(r'ka"([^<]*)',a).group(0)[6:]
	except:
	    self.plot = ""

    def get_site(self):
        self.site = re.search(r"href=[\"'](http://.*imdb\.com/title/[^\"']*)",self.page)
        if self.site:
            self.site = gutils.strip_tags(self.site.group(1))
        else:
            self.site = ""

    def get_trailer(self):
        self.trailer = re.search(r"<a href=\"([^\"]*)\"[^>]*>trailer<br><img src=\"http://img.csfd.cz/images/new/film/ikona_trailer",self.page)
        try:
            self.trailer = self.url+"videa"

        except:
            self.trailer = ""

    def get_rating(self):
	a= re.sub("\t", "", self.page)
	a= re.sub("\n", "", a)
        self.rating = re.search(r"[\s]*([\d]+)%[\s]*</h2>",a).group()[:-6]
	
        if self.rating:
            self.rating = str(float(self.rating)/10)
        else:
            self.rating = ""

    def get_o_site(self):
	try:
            self.o_site = "http://"+re.findall(r'<li><a\ href="http://([^>]*)',self.page)[1][:-36]

        except:
            self.o_site = ""

    def get_notes(self):
        self.notes = ""

    def get_studio(self):
        self.studio = ""

    def get_classification(self):
        self.classification = ""

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.encode = "utf-8"
        self.original_url_search   = "http://www.csfd.cz/hledat/?q="
        self.translated_url_search = "http://www.csfd.cz/hledat/?q="

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        return self.page

    def get_searches(self):
        tmp_id = self.re_items=re.search(r"window.location.href='http://www.csfd.cz/(/film/[^']*)'",self.page)
        if tmp_id:
            self.ids.append(tmp_id.group(1))
        else:
            self.re_items=re.findall(r"href=\"(/film/[^\"]+)[^>]*>([^<]+)</a>([^<]*)",self.page)
            self.number_results = len(self.re_items)
            if (self.number_results > 0):
                for item in self.re_items:
                    self.ids.append(item[0])
#                    self.titles.append(gutils.convert_entities(item[1])+' '+item[2])
                    self.titles.append(item[1]+' '+item[2])
