# -*- coding: UTF-8 -*-

__revision__ = '$Id: PluginMovieIMDB.py 176 2006-02-01 12:07:26Z iznogoud $'

# Copyright (c) 2005-2009 Vasco Nunes, Piotr Ozarowski
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, orprint
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

import gutils
import movie
import string
import re
import logging
log = logging.getLogger("Griffith")

plugin_name         = "Allocine"
plugin_description  = "Internet Movie Database"
plugin_url          = "www.allocine.fr"
plugin_language     = _("French")
plugin_author       = "Pierre-Luc Levy"
plugin_author_email = ""
plugin_version      = "0.7"


class Plugin(movie.Movie):
    replace_tabs = re.compile('[\t\r\n]', re.M)

    def __init__(self, id):
        self.movie_id = id
        self.url      = "http://www.allocine.fr/film/fichefilm_gen_cfilm=%s.html" % str(self.movie_id)
        self.encode   = 'utf-8'

    def initialize(self):
        self.page_cast = self.open_page(self.parent_window, url = "http://www.allocine.fr/film/casting_gen_cfilm=%s.html" % str(self.movie_id))

    def get_image(self):
        urls = re.split('<img[ \t]+src=[\'"]', gutils.trim(self.page, '<div class="poster">', '</div>'))
        for url in urls[1:]:
            url = gutils.before(url, '"')
            url = gutils.before(url, '\'')
            if string.find(url, '.jpg') >= 0:
                self.image_url = url
                break

    def get_o_title(self):
        self.o_title = gutils.after(gutils.trim(self.page, 'Titre original : <span', '</span>'), '>')
        if (self.o_title == ''):
            self.o_title = re.sub('[(][0-9]+[)]', '', string.replace(gutils.trim(self.page, '<title>', '</title>'), u' - AlloCiné', ''))

    def get_title(self):
        self.title = re.sub('[(][0-9]+[)]', '', string.replace(gutils.trim(self.page, '<title>', '</title>'), u' - AlloCiné', ''))

    def get_director(self):
        self.director = gutils.trim(self.page, u'Réalisé par ', '</a>')

    def get_plot(self):
        self.plot = gutils.trim(self.page, 'Synopsis : ', '</div>')

    def get_year(self):
        self.year = gutils.clean(gutils.trim(self.page, u'Année de production : ', '</a>'))

    def get_runtime(self):
        self.runtime = gutils.clean(gutils.trim(self.page, u'Durée :', 'min'))
        if self.runtime:
            self.runtime = str(int(gutils.before(self.runtime, "h")) * 60 + int(gutils.after(self.runtime, "h")))

    def get_genre(self):
        self.genre = gutils.regextrim(self.page, 'Genre : ', '</a>[^,]')
        self.genre = string.replace(self.replace_tabs.sub('', gutils.clean(self.genre)), ',', ', ')

    def get_cast(self):
        self.cast = ""
        casts = gutils.trim(self.page_cast, 'Acteurs, rôles, personnages', '<h2>')
        parts = string.split(casts, 'href="/personne/fichepersonne_gen_cpersonne=')
        for index in range(1, len(parts), 1):
            character = gutils.clean(gutils.trim(parts[index], 'Rôle :', '<'))
            if not character:
                character = gutils.clean(gutils.trim(parts[index - 1], '<td>', '</td>'))
            actor = gutils.clean(gutils.trim(parts[index], '>', '<'))
            if actor:
                if character:
                    self.cast = self.cast + actor + _(' as ') + character + '\n'
                else:
                    self.cast = self.cast + actor + '\n'

    def get_classification(self):
        self.classification = ""

    def get_studio(self):
        self.studio = ""

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = "http://www.allocine.fr/film/fichefilm_gen_cfilm=%s.html" % self.movie_id

    def get_trailer(self):
        self.trailer = "http://www.allocine.fr/film/video_gen_cfilm=%s.html" % self.movie_id

    def get_country(self):
        self.country = gutils.trim(self.page, 'Long-métrage', '</a>')

    def get_rating(self):
        self.rating = gutils.trim(self.page, 'Spectateurs</a>', 'src=')
        self.rating = gutils.trim(self.rating, 'class="stareval n', ' ')
        if self.rating:
            try:
                self.rating = str(round(float(int(self.rating) * .225)))
            except:
                self.rating = 0

    def get_screenplay(self):
        self.screenplay = gutils.clean(gutils.trim(self.page_cast, u'Scénariste', '</tr>'))

    def get_cameraman(self):
        self.cameraman = gutils.clean(gutils.trim(self.page_cast, 'Directeur de la photographie', '</tr>'))


class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search   = "http://www.allocine.fr/recherche/1/?q="
        self.translated_url_search = "http://www.allocine.fr/recherche/1/?q="
        self.encode                = 'utf-8'
        self.remove_accents        = True

    def search(self, parent_window):
        if not self.open_search(parent_window):
            return None
        # try to find next pages if more than 20 results
        match = re.search('<span class="navcurrpage">1</span> / ([0-9])+</li>', self.page)
        self.sub_search()
        if match:
            saved_url = self.url
            saved_title = self.title
            self.title = ''
            try:
                maxpages = int(match.group(1))
                if maxpages > 1:
                    currpage = 2
                    while currpage <= maxpages and currpage < 5:
                        oldpage = self.page
                        self.url = string.replace(saved_url, '/?q=', '/?p=%s&q=' % currpage)
                        if not self.open_search(parent_window):
                            return None
                        self.sub_search()
                        self.page = oldpage + self.page
                        currpage = currpage + 1
            except:
                log.exception('')
            self.url = saved_url
            self.title = saved_title
        return self.page

    def sub_search(self):
        self.page = gutils.regextrim(self.page, u'résultat[s]* trouvé[s]*', '<form method=')

    def get_searches(self):
        elements = string.split(self.page, '<a href=\'/film/fichefilm_gen_cfilm=')
        if (elements[0] <> ''):
            for index in range(1, len(elements), 1):
                element = elements[index]
                title = gutils.clean(gutils.convert_entities(gutils.trim(element, '>', '</a>')))
                year = gutils.clean(gutils.trim(element, '<span class="fs11">', '<br'))
                if title:
                    self.ids.append(gutils.before(element, '.'))
                    if year:
                        self.titles.append(title + ' (' + year + ')')
                    else:
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
        'Le Prix à payer' : [ 4, 4 ],
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
        '110585' : {
            'title'               : u'Le Prix à payer',
            'o_title'             : u'Le Prix à payer',
            'director'            : u'Alexandra Leclère',
            'plot'                : True,
            'cast'                : u'Christian Clavier' + _(' as ') + 'Jean-Pierre Ménard\n\
Nathalie Baye' + _(' as ') + 'Odile Ménard\n\
Gérard Lanvin' + _(' as ') + 'Richard\n\
Géraldine Pailhas' + _(' as ') + 'Caroline\n\
Patrick Chesnais' + _(' as ') + 'Grégoire l\'amant\n\
Anaïs Demoustier' + _(' as ') + 'Justine\n\
Maud Buquet' + _(' as ') + 'la prostituée\n\
Francis Leplay' + _(' as ') + 'l\'agent immobilier',
            'country'             : u'français',
            'genre'               : u'Comédie',
            'classification'      : False,
            'studio'              : False,
            'o_site'              : False,
            'site'                : 'http://www.allocine.fr/film/fichefilm_gen_cfilm=110585.html',
            'trailer'             : 'http://www.allocine.fr/film/video_gen_cfilm=110585.html',
            'year'                : 2007,
            'notes'               : False,
            'runtime'             : 95,
            'image'               : True,
            'rating'              : 6,
            'cameraman'           : u'Jean-François Robin',
            'screenplay'          : u'Alexandra Leclère',
            'barcode'             : False
        },
        '309' : {
            'title'               : u'Terminator',
            'o_title'             : u'Terminator',
            'director'            : u'James Cameron',
            'plot'                : True,
            'cast'                : u'Arnold Schwarzenegger' + _(' as ') + 'le Terminator\n\
Michael Biehn' + _(' as ') + 'Kyle Reese\n\
Linda Hamilton' + _(' as ') + 'Sarah Connor\n\
Lance Henriksen' + _(' as ') + 'l\'inspecteur Vukovich\n\
Paul Winfield' + _(' as ') + 'le lieutenant Ed Traxler\n\
Bess Motta' + _(' as ') + 'Ginger Ventura\n\
Rick Rossovich' + _(' as ') + 'Matt Buchanan\n\
Earl Boen' + _(' as ') + 'le Dr Peter Silberman\n\
Dick Miller' + _(' as ') + 'le marchand d\'armes\n\
Shawn Schepps' + _(' as ') + 'Nancy\n\
Bill Paxton' + _(' as ') + 'le chef des punks\n\
Brian Thompson' + _(' as ') + 'un punk\n\
Marianne Muellerleile' + _(' as ') + 'la \'mauvaise\' Sarah Connor\n\
Franco Columbu' + _(' as ') + 'le Terminator infiltrant le bunker dans le futur\n\
Ken Fritz' + _(' as ') + 'Policeman\n\
Stan Yale' + _(' as ') + 'Derelict in Alley\n\
Brad Rearden' + _(' as ') + 'Punk\n\
Joe Farago' + _(' as ') + 'TV Anchorman\n\
Anthony Trujillo' + _(' as ') + 'Mexican Boy (close-ups)\n\
Harriet Medin' + _(' as ') + 'Customer\n\
Hugh Farrington' + _(' as ') + 'Customer\n\
Philip Gordon' + _(' as ') + 'Mexican Boy (long shots)\n\
Patrick Pinney' + _(' as ') + 'Bar Customer\n\
Wayne Stone' + _(' as ') + 'Tanker Driver\n\
Norman Friedman' + _(' as ') + 'Cleaning Man at Flophouse\n\
Hettie Lynne Hurtes' + _(' as ') + 'TV Anchorwoman\n\
Al Kahn' + _(' as ') + 'Customer\n\
Bill W. Richmond' + _(' as ') + 'Bartender\n\
Bruce M. Kerner' + _(' as ') + 'Desk Sergeant\n\
David Pierce' + _(' as ') + 'Tanker Partner\n\
Barbara Powers' + _(' as ') + 'Ticket Taker at Club Technoir\n\
Ed Dogans' + _(' as ') + 'Acteur',
            'country'             : u'américain',
            'genre'               : u'Science fiction',
            'classification'      : False,
            'studio'              : False,
            'o_site'              : False,
            'site'                : 'http://www.allocine.fr/film/fichefilm_gen_cfilm=309.html',
            'trailer'             : 'http://www.allocine.fr/film/video_gen_cfilm=309.html',
            'year'                : 1984,
            'notes'               : False,
            'runtime'             : 108,
            'image'               : True,
            'rating'              : 9,
            'cameraman'           : u'Adam Greenberg',
            'screenplay'          : u'James Cameron',
            'barcode'             : False
        },
    }
