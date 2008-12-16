# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2007 Vasco Nunes, Piotr Ożarowski
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

plugin_name        = 'IMDb'
plugin_description    = 'Internet Movie Database'
plugin_url        = 'www.imdb.com'
plugin_language        = _('English')
plugin_author        = 'Vasco Nunes, Piotr Ożarowski'
plugin_author_email    = 'griffith-private@lists.berlios.de'
plugin_version        = '1.5'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode = 'utf-8'
        self.movie_id = id
        self.url = "http://imdb.com/title/tt%s" % str(self.movie_id)

    def initialize(self):
        self.cast_page = self.open_page(url=self.url + '/fullcredits')
        self.plot_page = self.open_page(url=self.url + '/plotsummary')

    def get_image(self):
        tmp = string.find(self.page, 'a name="poster"')
        if tmp == -1:        # poster not available
            self.image_url = ''
        else:
            self.image_url = gutils.trim(self.page[tmp:], 'src="', '"')

    def get_o_title(self):
        self.o_title = gutils.regextrim(self.page, '<h1>', '([ ]|[&][#][0-9]+[;])<span')
        if self.o_title == '':
            self.o_title = re.sub('[(].*', '', gutils.trim(self.page, '<title>', '</title>'))

    def get_title(self):    # same as get_o_title()
        self.title = gutils.regextrim(self.page, '<h1>', '([ ]|[&][#][0-9]+[;])<span')
        if self.title == '':
            self.title = re.sub('[(].*', '', gutils.trim(self.page, '<title>', '</title>'))

    def get_director(self):
        pattern = re.compile('<h5>Director[s]*?:</h5>[\n\s\r]*(.*?)(?:<br/>)?(?:<a[^>]+>more</a>)?[\n]*</div')
        result = pattern.search(self.page)
        if result:
            self.director = result.groups()[0]
            self.director = self.director.replace('<br/>', ', ')

    def get_plot(self):
        self.plot = gutils.trim(self.page, '<h5>Plot Outline:</h5>', '</div>')
        self.plot = self.__before_more(self.plot)
        elements = string.split(self.plot_page, '<p class="plotpar">')
        if len(elements) > 1:
            self.plot = self.plot + '\n\n'
            elements[0] = ''
            for element in elements:
                if element <> '':
                    self.plot = self.plot + gutils.strip_tags(gutils.before(element, '</a>')) + '\n'

    def get_year(self):
        self.year = gutils.trim(self.page, '<a href="/Sections/Years/', '</a>')
        self.year = gutils.after(self.year, '">')

    def get_runtime(self):
        self.runtime = gutils.trim(self.page, '<h5>Runtime:</h5>', ' min')

    def get_genre(self):
        self.genre = gutils.trim(self.page, '<h5>Genre:</h5>', '</div>')
        self.genre = self.__before_more(self.genre)

    def get_cast(self):
        self.cast = ''
        self.cast = gutils.trim(self.cast_page, '<table class="cast">', '</table>')
        if self.cast == '':
            self.cast = gutils.trim(self.page, '<table class="cast">', '</table>')
        self.cast = string.replace(self.cast, ' ... ', _(' as '))
        self.cast = string.replace(self.cast, '...', _(' as '))
        self.cast = string.replace(self.cast, '</tr><tr>', "\n")
        self.cast = string.replace(self.cast, '</tr><tr class="even">', "\n")
        self.cast = string.replace(self.cast, '</tr><tr class="odd">', "\n")
        self.cast = self.__before_more(self.cast)

    def get_classification(self):
        self.classification = gutils.trim(self.page, '<h5><a href="/mpaa">MPAA</a>:</h5>', '</div>')
        self.classification = gutils.trim(self.classification, 'Rated ', ' ')

    def get_studio(self):
        self.studio = gutils.trim(self.page, '<h5>Company:</h5>', '</a>')

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = "http://www.imdb.com/title/tt%s" % self.movie_id

    def get_trailer(self):
        self.trailer = "http://www.imdb.com/title/tt%s/trailers" % self.movie_id

    def get_country(self):
        self.country = gutils.trim(self.page, '<h5>Country:</h5>', '</div>')

    def get_rating(self):
        pattern = re.compile('>([0-9]([.][0-9])*)[/][0-9][0-9]<')
        result = pattern.search(self.page)
        if result:
            self.rating = result.groups()[0]
            if self.rating:
                try:
                    self.rating = float(self.rating)
                except Exception, e:
                    self.rating = 0
        else:
            self.rating = 0

    def get_notes(self):
        self.notes = ''
        language = gutils.trim(self.page, '<h5>Language:</h5>', '</div>')
        language = gutils.strip_tags(language)
        language = re.sub('[\n]+', '', language)
        language = re.sub('[ ]+', ' ', language)
        language = language.rstrip()
        color = gutils.trim(self.page, '<h5>Color:</h5>', '</div>')
        color = gutils.strip_tags(color)
        color = re.sub('[\n]+', '', color)
        color = re.sub('[ ]+', ' ', color)
        color = color.rstrip()
        sound = gutils.trim(self.page, '<h5>Sound Mix:</h5>', '</div>')
        sound = gutils.strip_tags(sound)
        sound = re.sub('[\n]+', '', sound)
        sound = re.sub('[ ]+', ' ', sound)
        sound = sound.rstrip()
        tagline = gutils.trim(self.page, '<h5>Tagline:</h5>', '</div>')
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
        if len(tagline)>0:
            self.notes += "%s: %s\n" %('Tagline', tagline)
    
    def __before_more(self, data):
        tmp = string.find(data, '>more<')
        if tmp>0:
            data = data[:tmp] + '>'
        return data

class SearchPlugin(movie.SearchMovie):
    PATTERN = re.compile(r"""<A HREF=['"]/title/tt([0-9]+)/["']>(.*?)</LI>""")
    PATTERN2 = re.compile(r"""<a href=['"]/title/tt([0-9]+)/["'](.*?)</tr>""")

    def __init__(self):
        self.original_url_search   = 'http://www.imdb.com/List?words='
        self.translated_url_search = 'http://www.imdb.com/find?more=tt;q='
        self.encode = 'utf-8'

    def search(self,parent_window):
        self.open_search(parent_window)
        tmp_page = gutils.trim(self.page, 'Here are the', '</TABLE>')
        if tmp_page == '':
            self.page = gutils.trim(self.page, '(Displaying', '<b>Suggestions For Improving Your Results</b>')
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
