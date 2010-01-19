# -*- coding: utf-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2010-2015 Enrico Carlesso
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

plugin_name         = 'IMDb-IT'
plugin_description  = 'Internet Movie Database in Italiano'
plugin_url          = 'italian.imdb.com'
plugin_language     = _('Italian')
plugin_author       = 'Enrico Carlesso'
plugin_author_email = 'enrico@ecarlesso.org'
plugin_version      = '0.1'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   = 'iso8859-1'
        self.movie_id = id
        self.url      = "http://italian.imdb.com/title/tt%s" % self.movie_id
        self.o_url      = "http://imdb.com/title/tt%s" % self.movie_id

    def initialize(self):
        self.cast_page = self.open_page(url=self.url + '/fullcredits')
        self.plot_page = self.open_page(url=self.url + '/plotsummary')
        self.o_page = self.open_page(url=self.o_url)

    def get_image(self):
        tmp = string.find(self.page, 'a name="poster"')
        if tmp == -1:        # poster not available
            self.image_url = ''
        else:
            self.image_url = gutils.trim(self.page[tmp:], 'src="', '"')

    def get_o_title(self):
        self.o_title = gutils.regextrim(self.o_page, '<h1>', '([ ]|[&][#][0-9]+[;])<span')
        if self.o_title == '':
            self.o_title = re.sub('[(].*', '', gutils.trim(self.o_page, '<title>', '</title>'))

    def get_title(self):    # same as get_o_title()
        self.title = gutils.regextrim(self.page, '<h1>', '([ ]|[&][#][0-9]+[;])<span')
        if self.title == '':
            self.title = re.sub('[(].*', '', gutils.trim(self.page, '<title>', '</title>'))

    def get_director(self):
        self.director = ''
        parts = re.split('<a href=', gutils.trim(self.cast_page, '>Regia di<', '</table>'))
        if len(parts) > 1:
            for part in parts[1:]:
                director = gutils.trim(part, '>', '<')
                self.director = self.director + director + ', '
            self.director = self.director[0:len(self.director) - 2]

    def get_plot(self):
        self.plot = gutils.regextrim(self.page, '<h5>Plot:</h5>', '(</div>|<a href.*)')
        self.plot = self.__before_more(self.plot)
        elements = string.split(self.plot_page, '<p class="plotpar">')
        if len(elements) > 1:
            self.plot = self.plot + '\n\n'
            elements[0] = ''
            for element in elements:
                if element <> '':
                    self.plot = self.plot + gutils.strip_tags(gutils.before(element, '</a>')) + '\n\n'

    def get_year(self):
        self.year = gutils.trim(self.o_page, '<a href="/Sections/Years/', '</a>')
        self.year = gutils.after(self.year, '">')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, '<h5>Durata:</h5>', ' min')

    def get_genre(self):
        self.genre = gutils.trim(self.page, '<h5>Genere:</h5>', '</div>')
        self.genre = self.__before_more(self.genre)

    def get_cast(self):
        self.cast = ''
        self.cast = gutils.trim(self.cast_page, '<table class="cast">', '</table>')
        if self.cast == '':
            self.cast = gutils.trim(self.page, '<table class="cast">', '</table>')
        self.cast = string.replace(self.cast, ' ... ', _(' as '))
        self.cast = string.replace(self.cast, '...', _(' as '))
        self.cast = string.replace(self.cast, '</tr><tr>', "\n")
        self.cast = re.sub('</tr>[ \t]*<tr[ \t]*class="even">', "\n", self.cast)
        self.cast = re.sub('</tr>[ \t]*<tr[ \t]*class="odd">', "\n", self.cast)
        self.cast = self.__before_more(self.cast)

    def get_classification(self):
        self.classification = gutils.trim(self.page, '<h5><a href="/mpaa">MPAA</a>:</h5>', '</div>')
        self.classification = gutils.trim(self.classification, 'Rated ', ' ')

    def get_studio(self):
        self.studio = gutils.trim(self.page, '<h5>Compagnia:</h5>', '</a>')

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = "http://italian.imdb.com/title/tt%s" % self.movie_id

    def get_trailer(self):
        self.trailer = "http://italian.imdb.com/title/tt%s/trailers" % self.movie_id

    def get_country(self):
        self.country = gutils.trim(self.page, '<h5>Nazionalità:</h5>', '</div>')
        self.country = re.sub('[\n]+', '', self.country)

    def get_rating(self):
        pattern = re.compile('>([0-9]([.][0-9])*)[/][0-9][0-9]<')
        result = pattern.search(self.o_page)
        if result:
            self.rating = result.groups()[0]
            if self.rating:
                try:
                    self.rating = round(float(self.rating), 0)
                except Exception, e:
                    self.rating = 0
        else:
            self.rating = 0

    def get_notes(self):
        self.notes = ''
        language = gutils.trim(self.page, '<h5>Lingua:</h5>', '</div>')
        language = gutils.strip_tags(language)
        language = re.sub('[\n]+', '', language)
        language = re.sub('[ ]+', ' ', language)
        language = language.rstrip()
        color = gutils.trim(self.page, '<h5>Colore:</h5>', '</div>')
        color = gutils.strip_tags(color)
        color = re.sub('[\n]+', '', color)
        color = re.sub('[ ]+', ' ', color)
        color = color.rstrip()
        sound = gutils.trim(self.page, '<h5>Sonoro:</h5>', '</div>')
        sound = gutils.strip_tags(sound)
        sound = re.sub('[\n]+', '', sound)
        sound = re.sub('[ ]+', ' ', sound)
        sound = sound.rstrip()
        tagline = gutils.trim(self.page, '<h5>Trama:</h5>', '</div>')
        tagline = self.__before_more(tagline)
        tagline = gutils.strip_tags(tagline)
        tagline = re.sub('[\n]+', '', tagline)
        tagline = re.sub('[ ]+', ' ', tagline)
        tagline = tagline.rstrip()
        if len(language)>0:
            self.notes = "%s: %s\n" %(_('Language'), language)
        if len(sound)>0:
            self.notes += "%s: %s\n" %(gutils.strip_tags(_('<b>Audio</b>')), sound)
        if len(color)>0:
            self.notes += "%s: %s\n" %(_('Color'), color)
        if len(tagline)>0 and tagline != "Aggiungi o traduci un riassunto della trama":
            self.notes += "%s: %s\n" %('Tagline', tagline)

    def get_screenplay(self):
        self.screenplay = ''
        parts = re.split('<a href=', gutils.trim(self.cast_page, '>Scritto da<', '</table>'))
        if len(parts) > 1:
            for part in parts[1:]:
                screenplay = gutils.trim(part, '>', '<')
                if screenplay == 'WGA':
                    continue
                screenplay = screenplay.replace(' (scritto da)', '')
                screenplay = screenplay.replace(' e<', '<')
                self.screenplay = self.screenplay + screenplay + ', '
            if len(self.screenplay) > 2:
                self.screenplay = self.screenplay[0:len(self.screenplay) - 2]

    def get_cameraman(self):
        self.cameraman = ''

    def __before_more(self, data):
        tmp = string.find(data, '>ancora<')
        if tmp > 0:
            data = data[:tmp] + '>'
        return data

class SearchPlugin(movie.SearchMovie):
    PATTERN = re.compile(r"""<A HREF=['"]/title/tt([0-9]+)/["']>(.*?)</LI>""")
    PATTERN2 = re.compile(r"""<a href=['"]/title/tt([0-9]+)/["'](.*?)</tr>""")

    def __init__(self):
        self.original_url_search   = 'http://italian.imdb.com/find?s=tt;q='
        self.translated_url_search = 'http://italian.imdb.com/find?s=tt;q='
        self.encode                = 'iso8859-1'

    def search(self, parent_window):
        if not self.open_search(parent_window):
            return None
        tmp_page = gutils.trim(self.page, 'Titoli popolari', '</table>')
        if not tmp_page:
            has_results = re.match('[(]Visualizza [1-9][0-7]* risultat[io]*[)]', self.page)
            if not has_results:
                # nothing or one result found, try another url which looks deeper in the imdb database
                # example: Adventures of Falcon -> one result, jumps directly to the movie page
                # which isn't supported by this plugin
                self.url = 'http://italian.imdb.com/find?more=tt;q='
                if not self.open_search(parent_window):
                    return None
            self.page = gutils.trim(self.page, '(Visualizza', '>Suggerimenti per migliorare i tuoi risultati<')
        else:
            self.page = tmp_page
        self.page = self.page.decode('iso-8859-1')
        # correction of all &#xxx entities
        self.page = gutils.convert_entities(self.page)
        return self.page

    def get_searches(self):
        elements = re.split('<LI>', self.page)
        if len(elements) < 2:
            elements = string.split(self.page, '<tr>')
            if len(elements):
                for element in elements[1:]:
                    match = self.PATTERN2.findall(element)
                    if len(match):
                        tmp = re.sub('^[0-9]+[.]', '', gutils.clean(gutils.after(match[0][1], '>')))
                        self.ids.append(match[0][0])
                        self.titles.append(tmp)
        else:
            for element in elements[1:]:
                match = self.PATTERN.findall(element)
                if len(match):
                    tmp = gutils.clean(match[0][1])
                    self.ids.append(match[0][0])
                    self.titles.append(tmp)
