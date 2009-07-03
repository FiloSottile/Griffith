# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2009 Vasco Nunes, Piotr Ożarowski
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

plugin_name         = 'IMDb'
plugin_description  = 'Internet Movie Database'
plugin_url          = 'www.imdb.com'
plugin_language     = _('English')
plugin_author       = 'Vasco Nunes, Piotr Ożarowski'
plugin_author_email = 'griffith-private@lists.berlios.de'
plugin_version      = '1.9'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   = 'iso8859-1'
        self.movie_id = id
        self.url      = "http://imdb.com/title/tt%s" % self.movie_id

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
        self.director = ''
        parts = re.split('<a href=', gutils.trim(self.cast_page, '>Directed by<', '</table>'))
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
        self.cast = re.sub('</tr>[ \t]*<tr[ \t]*class="even">', "\n", self.cast)
        self.cast = re.sub('</tr>[ \t]*<tr[ \t]*class="odd">', "\n", self.cast)
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
        self.country = re.sub('[\n]+', '', self.country)

    def get_rating(self):
        pattern = re.compile('>([0-9]([.][0-9])*)[/][0-9][0-9]<')
        result = pattern.search(self.page)
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

    def get_screenplay(self):
        self.screenplay = ''
        parts = re.split('<a href=', gutils.trim(self.cast_page, '>Writing credits<', '</table>'))
        if len(parts) > 1:
            for part in parts[1:]:
                screenplay = gutils.trim(part, '>', '<')
                if screenplay == 'WGA':
                    continue
                screenplay = screenplay.replace(' (written by)', '')
                screenplay = screenplay.replace(' and<', '<')
                self.screenplay = self.screenplay + screenplay + ', '
            if len(self.screenplay) > 2:
                self.screenplay = self.screenplay[0:len(self.screenplay) - 2]

    def get_cameraman(self):
        self.cameraman = ''

    def __before_more(self, data):
        tmp = string.find(data, '>more<')
        if tmp > 0:
            data = data[:tmp] + '>'
        return data

class SearchPlugin(movie.SearchMovie):
    PATTERN = re.compile(r"""<A HREF=['"]/title/tt([0-9]+)/["']>(.*?)</LI>""")
    PATTERN2 = re.compile(r"""<a href=['"]/title/tt([0-9]+)/["'](.*?)</tr>""")

    def __init__(self):
        # http://www.imdb.com/List?words=
        # finds every title sorted alphabetically, first results are with a quote at
        # the beginning (episodes from tv series), no popular results at first
        # http://www.imdb.com/find?more=tt;q=
        # finds a whole bunch of results. if you look for "Rocky" you will get 903 results.
        # http://www.imdb.com/find?s=tt;q=
        # seems to give the best results. 88 results for "Rocky", popular titles first.
        self.original_url_search   = 'http://www.imdb.com/find?s=tt;q='
        self.translated_url_search = 'http://www.imdb.com/find?s=tt;q='
        self.encode                = 'iso8859-1'

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        tmp_page = gutils.trim(self.page, 'Here are the', '</TABLE>')
        if not tmp_page:
            has_results = re.match('[(]Displaying [1-9][0-7]* Result[s]*[)]', self.page)
            if not has_results:
                # nothing or one result found, try another url which looks deeper in the imdb database
                # example: Adventures of Falcon -> one result, jumps directly to the movie page
                # which isn't supported by this plugin
                self.url = 'http://www.imdb.com/find?more=tt;q='
                if not self.open_search(parent_window):
                    return None
            self.page = gutils.trim(self.page, '(Displaying', '>Suggestions For Improving Your Results<')
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
#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Rocky Balboa'         : [ 15, 15 ],
        'Ein glückliches Jahr' : [ 22, 22 ]
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
        '0138097' : { 
            'title'             : 'Shakespeare in Love',
            'o_title'           : 'Shakespeare in Love',
            'director'          : 'John Madden',
            'plot'              : True,
            'cast'              : 'Geoffrey Rush' + _(' as ') + 'Philip Henslowe\n\
Tom Wilkinson' + _(' as ') + 'Hugh Fennyman\n\
Steven O\'Donnell' + _(' as ') + 'Lambert\n\
Tim McMullan' + _(' as ') + 'Frees\n\
Joseph Fiennes' + _(' as ') + 'Will Shakespeare\n\
Steven Beard' + _(' as ') + 'Makepeace - the Preacher\n\
Antony Sher' + _(' as ') + 'Dr. Moth\n\
Patrick Barlow' + _(' as ') + 'Will Kempe\n\
Martin Clunes' + _(' as ') + 'Richard Burbage\n\
Sandra Reinton' + _(' as ') + 'Rosaline\n\
Simon Callow' + _(' as ') + 'Tilney - Master of the Revels\n\
Judi Dench' + _(' as ') + 'Queen Elizabeth\n\
Bridget McConnell' + _(' as ') + 'Lady in Waiting\n\
Georgie Glen' + _(' as ') + 'Lady in Waiting\n\
Nicholas Boulton' + _(' as ') + 'Henry Condell\n\
Gwyneth Paltrow' + _(' as ') + 'Viola De Lesseps\n\
Imelda Staunton' + _(' as ') + 'Nurse\n\
Colin Firth' + _(' as ') + 'Lord Wessex\n\
Desmond McNamara' + _(' as ') + 'Crier\n\
Barnaby Kay' + _(' as ') + 'Nol\n\
Jim Carter' + _(' as ') + 'Ralph Bashford\n\
Paul Bigley' + _(' as ') + 'Peter - the Stage Manager\n\
Jason Round' + _(' as ') + 'Actor in Tavern\n\
Rupert Farley' + _(' as ') + 'Barman\n\
Adam Barker' + _(' as ') + 'First Auditionee\n\
Joe Roberts' + _(' as ') + 'John Webster\n\
Harry Gostelow' + _(' as ') + 'Second Auditionee\n\
Alan Cody' + _(' as ') + 'Third Auditionee\n\
Mark Williams' + _(' as ') + 'Wabash\n\
David Curtiz' + _(' as ') + 'John Hemmings\n\
Gregor Truter' + _(' as ') + 'James Hemmings\n\
Simon Day' + _(' as ') + 'First Boatman\n\
Jill Baker' + _(' as ') + 'Lady De Lesseps\n\
Amber Glossop' + _(' as ') + 'Scullery Maid\n\
Robin Davies' + _(' as ') + 'Master Plum\n\
Hywel Simons' + _(' as ') + 'Servant\n\
Nicholas Le Prevost' + _(' as ') + 'Sir Robert De Lesseps\n\
Ben Affleck' + _(' as ') + 'Ned Alleyn\n\
Timothy Kightley' + _(' as ') + 'Edward Pope\n\
Mark Saban' + _(' as ') + 'Augustine Philips\n\
Bob Barrett' + _(' as ') + 'George Bryan\n\
Roger Morlidge' + _(' as ') + 'James Armitage\n\
Daniel Brocklebank' + _(' as ') + 'Sam Gosse\n\
Roger Frost' + _(' as ') + 'Second Boatman\n\
Rebecca Charles' + _(' as ') + 'Chambermaid\n\
Richard Gold' + _(' as ') + 'Lord in Waiting\n\
Rachel Clarke' + _(' as ') + 'First Whore\n\
Lucy Speed' + _(' as ') + 'Second Whore\n\
Patricia Potter' + _(' as ') + 'Third Whore\n\
John Ramm' + _(' as ') + 'Makepeace\'s Neighbor\n\
Martin Neely' + _(' as ') + 'Paris / Lady Montague (as Martin Neeley)\n\
The Choir of St. George\'s School in Windsor' + _(' as ') + 'Choir (as The Choir of St. George\'s School, Windsor) rest of cast listed alphabetically:\n\
Jason Canning' + _(' as ') + 'Nobleman (uncredited)\n\
Rupert Everett' + _(' as ') + 'Christopher Marlowe (uncredited)',
            'country'           : 'USA | UK',
            'genre'             : 'Comedy | Drama | Romance',
            'classification'    : 'R',
            'studio'            : 'Universal Pictures',
            'o_site'            : False,
            'site'              : 'http://www.imdb.com/title/tt0138097',
            'trailer'           : 'http://www.imdb.com/title/tt0138097/trailers',
            'year'              : 1998,
            'notes'             : _('Language') + ': English\n'\
+ _('Audio') + ': Dolby Digital\n'\
+ _('Color') + ': Color\n\
Tagline: ...A Comedy About the Greatest Love Story Almost Never Told...',
            'runtime'           : 123,
            'image'             : True,
            'rating'            : 7,
            'screenplay'        : 'Marc Norman, Tom Stoppard',
            'cameraman'         : False,
            'barcode'           : False
        },
    }
