# -*- coding: UTF-8 -*-

# $Id$

# Copyright (c) 2005-2007 Vasco Nunes
# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

import gutils
import movie,string

plugin_name = "Moviefone"
plugin_description = "A Service of America Online"
plugin_url = "movies.aol.com"
plugin_language = _("English")
plugin_author = "Vasco Nunes"
plugin_version = "0.3"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.movie_id = id
        self.url = "http://movies.aol.com/movie/main.adp?_pgtyp=pdct&mid=" + str(self.movie_id)

    def get_image(self):
        self.image_url = gutils.trim(self.page,"http://cdn.channel.aol.com/amgvideo/dvd/cov150/",".jpg")
        self.image_url = "http://cdn.channel.aol.com/amgvideo/dvd/cov150/" + self.image_url + ".jpg"

    def get_o_title(self):
        self.o_title = string.capwords(gutils.trim(self.page,"<title>"," - Moviefone</title>") )

    def get_title(self):
        self.title = self.o_title

    def get_director(self):
        self.director = gutils.trim(self.page,"<strong>Directed By:</strong> ","<br />")
        self.director = string.strip(gutils.strip_tags(self.director))

    def get_plot(self):
        self.plot = gutils.trim(self.page,"<strong>Synopsis:</strong> ","<br />")
        self.plot = string.strip(gutils.strip_tags(self.plot))

    def get_year(self):
        self.year = gutils.trim(self.page,"<strong>DVD Release Date:</strong> ","<br />")
        self.year = self.year[-4:]

    def get_runtime(self):
        self.runtime = gutils.trim(self.page,"<strong>Run Time:</strong> "," min.<br />")

    def get_genre(self):
        self.genre = gutils.trim(self.page,"<strong>Genre:</strong> ","<br />")

    def get_cast(self):
        self.cast = gutils.trim(self.page,"<strong>Starring:</strong> ","<br />")
        self.cast = string.strip(gutils.strip_tags(self.cast))

    def get_classification(self):
        self.classification = gutils.trim(self.page,"<strong>Rating:</strong> ","<br />")

    def get_studio(self):
        self.studio = gutils.trim(self.page,"<strong>Released By:</strong> ","<br />")

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = ""

    def get_trailer(self):
        self.trailer = gutils.trim(self.page,"""onclick="setTrailerOmni();window.open('""", \
            "','_dlplayer'")

    def get_country(self):
        self.country = ""

    def get_rating(self):
        self.rating = "0"

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.original_url_search    = "http://movies.aol.com/search/encyresults.adp?query=";
        self.translated_url_search    = "http://movies.aol.com/search/encyresults.adp?query=";

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        self.sub_search()
        return self.page

    def sub_search(self):
        self.page = gutils.trim(self.page,"--start LT_MultiColumn_1.0 module-->", 'pagnationleft">Results   ')

    def get_searches(self):
        elements = string.split(self.page,'class="dvdtitle">')
        elements[0] = ''

        for element in elements:
            element = gutils.trim( element, '<a href="', '<br/>' )
            if element != '':
                self.ids.append( gutils.after( gutils.trim( element, 'movie/','/main') , '/' ) )
                self.titles.append( string.replace( gutils.after( element, '">' ), '</a></span>', '' ) )
