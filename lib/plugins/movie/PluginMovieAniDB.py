# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright © 2005-2011 Piotr Ożarowski
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

import urllib2
from datetime import datetime, timedelta
from locale import getdefaultlocale
from os.path import getmtime, isfile, join

from lxml import etree

from gutils import decompress
from movie import Movie, SearchMovie

plugin_name         = 'AnimeDB'
plugin_description  = 'Anime DataBase'
plugin_url          = 'www.anidb.net'
plugin_language     = _('English')
plugin_author       = 'Piotr Ożarowski'
plugin_author_email = 'piotr@griffith.cc'
plugin_version      = '3.0'

ANIME_TITLES_URL = 'http://anidb.net/api/animetitles.xml.gz'
ANIME_IMG_URL = 'http://img7.anidb.net/pics/anime/'
ANIME_WEB_URL = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid='
REQUEST = "http://api.anidb.net:9001/httpapi?request=anime&client=%(client)s&clientver=%(version)s&protover=%(protocol)s&aid="
REQUEST %= dict(client='griffith', version=1, protocol=1)

lang = getdefaultlocale()[0][:2]  # TODO: get it from settings


class Plugin(Movie):
    def __init__(self, aid):
        self.encode = 'utf-8'
        self._aid = aid
        self.url = REQUEST + aid

    def initialize(self):
        if not self.page.startswith('<?xml'):
            raise Exception('page not in XML format')
        self._xml = etree.fromstring(self.page)

    def get_image(self):
        self.image_url = ANIME_IMG_URL + self._xml.find('picture').text

    def get_o_title(self):
        self.o_title = self._xml.find('titles/title[@type="main"]').text

    def get_title(self):
        node = self._xml.xpath("titles/title[@xml:lang='%s' and @type='official']" % lang)
        if node:
            self.title = node[0].text

    def get_director(self):
        self.director = ', '.join(n.text for n in self._xml.xpath('creators/name[@type="Direction"]'))

    def get_plot(self):
        self.plot = self._xml.xpath('description')[0].text

    def get_year(self):
        node = self._xml.xpath('episodes/episode[title="Complete Movie"]')
        if node:
            self.year = node.xpath('airdate')[0][:4]
        # XXX: should we take the first child if "Complete Movie" is missing?

    def get_runtime(self):
        node = self._xml.xpath('episodes/episode[title="Complete Movie"]')
        if node:
            self.runtime = node.xpath('length')[0]

    def get_genre(self):
        nodes = self._xml.xpath('categories/category/name')
        self.genre = ', '.join(n.text for n in nodes)

    def get_cast(self):
        nodes = self._xml.xpath('characters/character[@type="main character in"]')
        self.cast = ''
        for node in nodes:
            name = node.xpath('name')[0].text
            actor = node.xpath('seiyuu')[0].text
            self.cast += "[%s] voiced by %s\n" % (name, actor)

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = ', '.join(n.text for n in self._xml.xpath('creators/name[@type="Animation Production"]'))

    def get_o_site(self):
        self.site = self._xml.xpath('url')[0].text

    def get_site(self):
        self.site = ANIME_TITLES_URL + self._aid

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = ''

    def get_rating(self):
        rating = self._xml.xpath('ratings/permanent')
        if rating:
            self.rating = str(round(float(rating[0].text)))

    def get_notes(self):
        self.notes = ''
        # ...type and episodes
        type_ = self._xml.find('type')
        if type_ is not None:
            self.notes += "Type: %s\n" % type_.text
        episodes = {}
        for node in self._xml.xpath('episodes/episode'):
            key = node.find('epno').text
            titles = {}
            for tnode in node.xpath('title'):
                titles[tnode.attrib['xml:lang']] = tnode.text
            duration = node.find('length').text
            airdate = node.find('airdate')
            airdate = airdate.text if airdate is not None else None
            episodes[key] = dict(titles=titles, duration=duration, airdate=airdate)
        for key, details in sorted(episodes.iteritems()):
            self.notes += "\n%s: " % key
            self.notes += details['titles'].get(lang, details['titles']['en'])
            self.notes += " (%s" % details['duration']
            if details['airdate']:
                self.notes += ", %s)" % details['airdate']
            else:
                self.notes += ')'


def load_titles(fpath):
    # animetitles.xml.gz is updated once a day
    remote = None
    download = True
    if isfile(fpath):
        cache_last_modified = datetime.fromtimestamp(getmtime(fpath))
        if cache_last_modified > datetime.now() - timedelta(days=1):
            download = False
        else:
            remote = urllib2.urlopen(ANIME_TITLES_URL)
            last_modified = datetime(*remote.info().getdate('Last-Modified')[:7])
            if cache_last_modified >= last_modified:
                download = False
    else:
        remote = urllib2.urlopen(ANIME_TITLES_URL)

    if download:
        fp = open(fpath, 'wb')
        fp.write(remote.read())
        fp.close()

    return etree.fromstring(decompress(open(fpath, 'rb').read()))


class SearchPlugin(SearchMovie):
    original_url_search = 'http://anidb.net/'
    translated_url_search = 'http://anidb.net/'

    def search(self, parent_window):
        self._search_results = []
        exml = load_titles(join(self.locations['home'], 'animetitles.xml.gz'))
        for node in exml.xpath("anime[contains(., '%s')]" % self.title.replace("'", r"\'")):
            aid = node.attrib['aid']
            title = node.xpath("title[@xml:lang='%s']" % lang)
            # XXX: how about xpath with both cases and sorting results later?
            if not title:
                title = node.xpath('title[@type="main"]')[0].text
            else:
                title = title[0].text
            self._search_results.append((aid, title))

        return self._search_results

    def get_searches(self):
        del self.ids[:]
        del self.titles[:]
        self.number_results = len(self._search_results)
        for aid, title in self._search_results:
            self.ids.append(aid)
            self.titles.append(title)

#
# Plugin Test
#


class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Hellsing': [ 9, 9 ]
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
        '32': {
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
            'genre'               : 'Action, Contemporary Fantasy, Cops, Fantasy, Gunfights, Horror, Law and Order, Manga, Seinen, Special Squads, Vampires, Violence',
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
