# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2008 Piotr Ożarowski
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

import gettext
gettext.install('griffith', unicode=1)
import gutils, movie
import string, re
from gutils import decompress

plugin_name         = 'AnimeDB'
plugin_description  = 'Anime DataBase'
plugin_url          = 'www.anidb.net'
plugin_language     = _('English')
plugin_author       = 'Piotr Ożarowski'
plugin_author_email = '<ozarow+griffith@gmail.com>'
plugin_version      = '2.5'

aid_pattern = re.compile('[?&;]aid=(\d+)')

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode = 'utf-8'
        if string.find(id, 'http://') != -1:
            self.url = str(id)
            self.movie_id = 'anidb'
        else:
            self.movie_id = str(id)
            self.url = "http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s" % self.movie_id

    def initialize(self):
        self.page = decompress(self.page)
        if self.movie_id == 'anidb':
            aid =  aid_pattern.search(self.page)
            if aid:
                self.movie_id = aid.groups()[0]
                self.url = "http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%s" % self.movie_id
            else:
                return False
        self.page = gutils.after(self.page, 'id="layout-content"')
        pos = string.find(self.page, 'class="g_section anime_episodes">')
        if pos >0:
            self.page = self.page[:pos]

    def get_image(self):
        match = re.search('http://img\d*.anidb.net/pics/anime/\d*.jpg', self.page)
        if match is not None:
            self.image_url = match.group()
        else:
            self.image_url = ''

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<h1>Anime: ', '</h1>')

    def get_title(self):
        self.title = gutils.trim(self.page, '"field">Official Title', '</td>')
        self.title = gutils.trim(self.title, '<span>', '</span>')

    def get_director(self):
        self.director = ''

    def get_plot(self):
        self.plot = gutils.trim(self.page, 'class="desc">', '</div>')

    def get_year(self):
        self.year = gutils.trim(self.page, '"field">Year', '</td>')
        self.year = gutils.after(self.year, '"value">')[-4:]

    def get_runtime(self):
        self.runtime = ''

    def get_genre(self):
        self.genre = gutils.trim(self.page, '>Categories<', '</td>')
        self.genre = gutils.after(self.genre, 'value">')
        self.genre = gutils.strip_tags(self.genre)
        if len(self.genre) and self.genre.endswith('- similar'):
            self.genre =  self.genre[:-9]
        elif self.genre == '-':
            self.genre = ''
        self.genre = string.replace(self.genre, '\n', '')

    def get_cast(self):
        self.cast = ''

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = gutils.trim(self.page, '"field">Producers', '</td>')
        self.studio = gutils.strip_tags(self.studio)
        if len(self.studio) and self.studio[:2] == " (":
            self.studio = self.studio[2:]
            if self.studio[len(self.studio)-1:] == ')':
                self.studio = self.studio[:len(self.studio)-1]
        self.studio = string.replace(self.studio, '\n', '')

    def get_o_site(self):
        self.o_site = gutils.trim(self.page, '"field">URL', '</td>')
        self.o_site = gutils.trim(self.o_site, 'href="', '"')

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = ''

    def get_rating(self):
        self.rating = gutils.trim(self.page, '"field">Rating', '</td>')

    def get_notes(self):
        self.notes = ''
        # ...type
        atype = gutils.trim(self.page, '"field">Type', '</td>')
        atype = gutils.clean(atype)
        if atype != '':
            self.notes += "Type: %s\n" % atype
        # ...number of episodes
        episodes = gutils.trim(self.page, '"field">Episodes', '</td>')
        episodes = gutils.clean(episodes)
        if episodes != '':
            self.notes += "Episodes: %s\n" % episodes

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.encode = 'utf-8'
        self.original_url_search    = 'http://anidb.net/perl-bin/animedb.pl?show=animelist&do.search=search&adb.search='
        self.translated_url_search    = 'http://anidb.net/perl-bin/animedb.pl?show=animelist&do.search=search&adb.search='

    def search(self,parent_window):
        self.open_search(parent_window)
        self.page = decompress(self.page)

        tmp = string.find(self.page, '<h1>Anime List - Search for: ')
        if tmp == -1:        # already a movie page
            self.page = ''
        else:            # multiple matches
            self.page = gutils.trim(self.page, 'class="anime_list"', '</table>');
            self.page = gutils.after(self.page, '</tr>');

        return self.page

    def get_searches(self):
        if self.page == '':    # already a movie page
            self.number_results = 1
            self.ids.append(self.url)
            self.titles.append(self.title)
        else:            # multiple matches
            elements = string.split(self.page,"</tr>")
            self.number_results = elements[-1]

            if len(elements[0]):
                for element in elements:
                    element = gutils.trim(element, '<td', '</td>')
                    aid = aid_pattern.search(element)
                    if not aid:
                        continue
                    self.ids.append(aid.groups()[0])
                    element = gutils.after(element, '">')
                    element = gutils.strip_tags(element)
                    self.titles.append(element)
            else:
                self.number_results = 0

