# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2009 Piotr Ożarowski
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

import gutils, movie
import string, re
from gutils import decompress

plugin_name         = 'AnimeDB'
plugin_description  = 'Anime DataBase'
plugin_url          = 'www.anidb.net'
plugin_language     = _('English')
plugin_author       = 'Piotr Ożarowski'
plugin_author_email = 'piotr@griffith.cc'
plugin_version      = '2.8'

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
        match = re.search('img\d*.anidb.net/pics/anime/\d*.jpg', self.page)
        if match is not None:
            self.image_url = 'http://' + match.group()
        else:
            self.image_url = ''

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<span class="i_icon i_audio_ja" title=" language: japanese"><span>ja</span></span>', '</td>')
        self.o_title = gutils.trim(self.o_title, '<label>', '</label>')

    def get_title(self):
        self.title = gutils.trim(self.page, '<h1 class="anime">Anime: ', '</h1>')

    def get_director(self):
        self.director = gutils.trim(self.page, '>Direction (&#x76E3;&#x7763;', '</tr>')
        self.director = gutils.after(gutils.trim(self.director, '<a ', '</a>'), '>')

    def get_plot(self):
        self.plot = gutils.regextrim(self.page, 'class="(g_bubble )*desc">', '</div>')
        self.plot = self.plot.replace('<br/>', '\n')

    def get_year(self):
        self.year = gutils.trim(self.page, '"field">Year', '</td>')
        self.year = gutils.after(self.year, '"value">')[-4:]

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, '<label>Complete Movie</label>', '</tr>')
        self.runtime = gutils.trim(self.runtime, '<td class="duration">', 'm')

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
        self.cast = 'Characters:\n---------------'
        castv = gutils.trim(self.page, '<table id="characterlist" class="characterlist">', '</table>')
        if castv != '':
            castparts = string.split(castv, '<tr ')
            for index in range(2, len(castparts), 1):
                castpart = castparts[index]
                castcharacter = gutils.clean(gutils.trim(castpart, '<td rowspan="1" class="name">', '</td>'))
                castentity = gutils.clean(gutils.trim(castpart, '<td rowspan="1" class="entity">', '</td>'))
                castactor = gutils.clean(gutils.trim(castpart, '<td class="name"><a href="animedb.pl?show=creator&amp;creatorid=', 'd>'))
                castactor = gutils.clean(gutils.trim(castactor, '">', '</t'))
                if castv == ' ':
                    castactor = 'unknown'
                castrelation = gutils.clean(gutils.trim(castpart, '<td rowspan="1" class="relation">', '</td>'))
                castappearance = gutils.clean(gutils.trim(castpart, '<td rowspan="1" class="eprange">', '</td>'))
                self.cast += '\n\n' + '[' + castcharacter + '] voiced by ' + castactor + '\n' + castentity + '; ' + castrelation + '; appears in episodes: ' + castappearance

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = gutils.trim(self.page, '<tr class="producers">', '</tr>')
        if self.studio == '':
            self.studio = gutils.trim(self.page, '<tr class="g_odd producers">', '</tr>')
        self.studio = gutils.trim(self.studio, '<td class="value">', '</td>')
        self.studio = gutils.strip_tags(self.studio)
        if len(self.studio) and self.studio[:2] == " (":
            self.studio = self.studio[2:]
            if self.studio[len(self.studio)-1:] == ')':
                self.studio = self.studio[:len(self.studio)-1]
        self.studio = string.replace(self.studio, '\n', '')

    def get_o_site(self):
        self.o_site = gutils.trim(self.page, '<th class="field">Resources</th>', '</tr>') #class varies, tag used
        self.o_site = gutils.trim(self.o_site, '<a href="', '" rel="anidb::extern">Official page</a>')

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = ''

    def get_rating(self):
        self.rating = gutils.clean(gutils.after(gutils.trim(self.page, '<span class="rating', '</a>'), '>'))
        if self.rating:
            try:
                self.rating = str(round(float(self.rating)))
            except:
                self.rating = ''

    def get_notes(self):
        self.notes = ''
        # ...type and episodes
        atype = gutils.trim(self.page, '"field">Type', '</td>')
        atype = gutils.clean(atype)
        if atype != '':
            self.notes += "Type: %s\n" % atype
        episodes = gutils.trim(self.page, '>Episode list<', '</table>')
        if episodes != '':
            parts = string.split(episodes, '<tr ')
            for index in range(2, len(parts), 1):
                part = parts[index]
                nr = gutils.clean(gutils.trim(part, 'class="id eid">', '</td>'))
                title = gutils.clean(gutils.after(gutils.trim(part, '<label', '</td>'), '>'))
                duration = gutils.clean(gutils.trim(part, 'class="duration">', '</td>'))
                airdate = gutils.clean(gutils.trim(part, 'class="date airdate">', '</td>'))
                self.notes += '\n' + nr + ': ' + title + ' (' + duration + ', ' + airdate + ')'

    def get_screenplay(self):
        self.screenplay = gutils.trim(self.page, 'Script/Screenplay (&#x811A;&#x672C;', '</tr>')
        self.screenplay = gutils.after(gutils.trim(self.screenplay, '<a ', '</a>'), '>')

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.encode = 'utf-8'
        self.original_url_search = 'http://anidb.net/perl-bin/animedb.pl?show=animelist&do.search=search&adb.search='
        self.translated_url_search = 'http://anidb.net/perl-bin/animedb.pl?show=animelist&do.search=search&adb.search='

    def search(self,parent_window):
        self.open_search(parent_window)
        self.page = decompress(self.page)

        tmp = string.find(self.page, '>Anime List - Search for: ')
        if tmp == -1:        # already a movie page
            self.page = 'movie'
        else:            # multiple matches
            self.page = gutils.trim(self.page, 'class="animelist"', '</table>');
            self.page = gutils.after(self.page, '</tr>');

        return self.page

    def get_searches(self):
        if self.page == 'movie':    # already a movie page
            self.number_results = 1
            self.ids.append(self.url)
            self.titles.append(self.title)
        else:            # multiple matches
            elements = string.split(self.page,"</tr>")
            self.number_results = elements[-1]

            if len(elements[0]):
                for element in elements:
                    aid = aid_pattern.search(element)
                    if not aid:
                        continue
                    title = gutils.clean(gutils.trim(element, '<td class="name">', '</a>'))
                    type = gutils.clean(gutils.after(gutils.trim(element, '<td class="type', '</td>'), '>'))
                    self.ids.append(aid.groups()[0])
                    if type:
                        self.titles.append(title + ' (' + type + ')')
                    else:
                        self.titles.append(title)
            else:
                self.number_results = 0

#
# Plugin Test
#


class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Hellsing' : [ 8, 8 ]
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
        '32' : {
            'title'               : 'Hellsing',
            'o_title'             : u'ヘルシング',
            'director'            : 'Urata Yasunori',
            'plot'                : True,
            'cast'                : u'Characters:\n\
---------------\n\
\n\
[Alucard] voiced by Nakata Jouji\n\
male; main character in; appears in episodes: -\n\
\n\
[Incognito] voiced by Yamazaki Takumi\n\
-; main character in; appears in episodes: 8-13\n\
\n\
[Seras Victoria] voiced by Orikasa Fumiko\n\
female; main character in; appears in episodes: -\n\
\n\
[Sir Integral Fairbrook Wingates Hellsing] voiced by Sakakibara Yoshiko\n\
22, female; main character in; appears in episodes: -\n\
\n\
[Alexander Anderson] voiced by Nozawa Nachi\n\
male; secondary cast in; appears in episodes: -\n\
\n\
[Enrico Maxwell] voiced by Tanaka Hideyuki\n\
male; secondary cast in; appears in episodes: -\n\
\n\
[Helena] voiced by Hiramatsu Akiko\n\
female; secondary cast in; appears in episodes: 8, 11\n\
\n\
[Walter C. Dornez] voiced by Kiyokawa Motomu\n\
male; secondary cast in; appears in episodes: -\n\
\n\
[Hellsing Organization] voiced by \n\
Organisation; appears in; appears in episodes: -\n\
\n\
[Iscariot Organization] voiced by \n\
Organisation; appears in; appears in episodes: -\n\
\n\
[Police Officer inside Heli (ヘリ機内警察官)] voiced by Andy Holyfield\n\
-; appears in; appears in episodes: 8',
            'country'             : False,
            'genre'               : 'Action, Contemporary Fantasy, Cops, Fantasy, Gunfights, Horror, Law and Order, Seinen, Special Squads, Vampires, Violence',
            'classification'      : False,
            'studio'              : False,
            'o_site'              : 'http://www.gonzo.co.jp/works/0102.html',
            'site'                : 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=32',
            'trailer'             : False,
            'year'                : 2002,
            'notes'               : True,
            'runtime'             : 0,
            'image'               : True,
            'rating'              : 8,
            'cameraman'           : False,
            'screenplay'          : 'Konaka Chiaki'
        },
    }
