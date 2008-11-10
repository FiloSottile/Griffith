# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007 Michael Jahn
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

plugin_name         = 'IMDb-de'
plugin_description  = 'Internet Movie Database German'
plugin_url          = 'german.imdb.com'
plugin_language     = _('German')
plugin_author       = 'Michael Jahn'
plugin_author_email = 'mikej06@hotmail.com'
plugin_version      = '1.3'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode = 'iso8859-1'
        self.movie_id = id
        self.url = "http://german.imdb.com/title/tt%s" % str(self.movie_id)

    def initialize(self):
        self.cast_page = self.open_page(url=self.url + '/fullcredits')
        self.plot_page = self.open_page(url=self.url + '/plotsummary')
        # correction of all &#xxx entities
        self.page = self.page.decode(self.encode)
        self.page = gutils.convert_entities(self.page)
        self.page = self.page.encode(self.encode)
        self.cast_page = self.cast_page.decode(self.encode)
        self.cast_page = gutils.convert_entities(self.cast_page)
        self.cast_page = self.cast_page.encode(self.encode)
        self.plot_page = self.plot_page.decode(self.encode)
        self.plot_page = gutils.convert_entities(self.plot_page)
        self.plot_page = self.plot_page.encode(self.encode)

    def get_image(self):
        tmp = string.find(self.page, 'a name="poster"')
        if tmp == -1:        # poster not available
            self.image_url = ''
        else:
            self.image_url = gutils.trim(self.page[tmp:], 'src="', '"')

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<h1>', '<span')

    def get_title(self):
        self.title = gutils.trim(self.page, '<h1>', '<span')
        elements = string.split(self.regextrim(self.page, '<h5>(Alternativ|Auch bekannt als):', '</div>'), '<i class="transl"')
        if len(elements) > 1:
            for element in elements:
                tmp = gutils.before(gutils.trim(element, '>', '[de]'), '(')
                if tmp <> '':
                    self.title = tmp
                    break

    def get_director(self):
        self.director = gutils.trim(self.page,'<h5>Regie</h5>', '<br/>')
        if self.director == '':
            self.director = gutils.trim(self.page,'<h5>Regisseur:</h5>', '</div>')
        self.director = self.__before_more(self.director)
        self.director = self.director.replace('<br/>', ', ')
        self.director = gutils.clean(self.director)
        self.director = re.sub(',$', '', self.director)

    def get_plot(self):
        self.plot = gutils.trim(self.page, '<h5>Kurzbeschreibung:</h5>', '</div>')
        self.plot = self.__before_more(self.plot)
        elements = string.split(self.plot_page, '<p class="plotpar">')
        if len(elements) > 1:
            self.plot = self.plot + '\n\n'
            elements[0] = ''
            for element in elements:
                if element != '':
                    self.plot = self.plot + gutils.strip_tags(gutils.before(element, '</a>')) + '\n'

    def get_year(self):
        self.year = gutils.trim(self.page, '<a href="/Sections/Years/', '</a>')
        self.year = gutils.after(self.year, '">')

    def get_runtime(self):
        self.runtime = self.regextrim(self.page, '<h5>L[^n]+nge:</h5>', ' [Mm]in')

    def get_genre(self):
        self.genre = gutils.trim(self.page, '<h5>Genre:</h5>', '</div>')
        self.genre = self.__before_more(self.genre)

    def get_cast(self):
        self.cast = ''
        self.cast = gutils.trim(self.cast_page, '<table class="cast">', '</table>')
        if self.cast == '':
            self.cast = gutils.trim(self.page, '<table class="cast">', '</table>')
        self.cast = string.replace(self.cast, ' ... ', _(' as ').encode('utf8'))
        self.cast = string.replace(self.cast, '...', _(' as ').encode('utf8'))
        self.cast = string.replace(self.cast, '</tr><tr>', "\n")
        self.cast = string.replace(self.cast, '</tr><tr class="even">', "\n")
        self.cast = string.replace(self.cast, '</tr><tr class="odd">', "\n")
        self.cast = self.__before_more(self.cast)
        self.cast = re.sub('[ ]+', ' ', self.cast)

    def get_classification(self):
        self.classification = gutils.trim(gutils.trim(self.page, 'Altersfreigabe:', '</div>'), 'Germany:', '&')

    def get_studio(self):
        self.studio = gutils.trim(self.page, '<h5>Firma:</h5>', '</div>')
        self.studio = self.__before_more(self.studio)

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = "http://german.imdb.com/title/tt%s" % self.movie_id

    def get_trailer(self):
        self.trailer = "http://german.imdb.com/title/tt%s/trailers" % self.movie_id

    def get_country(self):
        self.country = gutils.trim(self.page, '<h5>Land:</h5>', '</div>')
        self.country = self.__before_more(self.country)
        self.country = re.sub('[\n]+', '', self.country)
        self.country = re.sub('[ ]+', ' ', self.country)

    def get_rating(self):
        self.rating = gutils.trim(self.page, '<h5>Nutzer-Bewertung:</h5>', '/10')
        if self.rating:
            try:
                self.rating = str(float(gutils.clean(self.rating)))
            except:
                self.rating = ''

    def get_notes(self):
        self.notes = ''
        language = gutils.trim(self.page, '<h5>Sprache:</h5>', '</div>')
        language = gutils.strip_tags(language)
        language = re.sub('[\n]+', '', language)
        language = re.sub('[ ]+', ' ', language)
        language = language.rstrip()
        color = gutils.trim(self.page, '<h5>Farbe:</h5>', '</div>')
        color = gutils.strip_tags(color)
        color = re.sub('[\n]+', '', color)
        color = re.sub('[ ]+', ' ', color)
        color = re.sub('[ ]+$', '', color)
        color = color.rstrip()
        sound = gutils.trim(self.page, '<h5>Tonverfahren:</h5>', '</div>')
        sound = gutils.strip_tags(sound)
        sound = re.sub('[\n]+', '', sound)
        sound = re.sub('[ ]+', ' ', sound)
        sound = sound.rstrip()
        soundsplit = sound.split(' | ')
        if len(soundsplit) > 1:
            soundsplit.sort()
            sound = ''
            for elem in soundsplit:
                sound += elem + ' | '
            sound = sound[0:len(sound) - 3]
        tagline = gutils.trim(self.page, '<h5>Werbezeile:</h5>', '</div>')
        tagline = self.__before_more(tagline)
        tagline = gutils.strip_tags(tagline)
        tagline = re.sub('[\n]+', '', tagline)
        tagline = re.sub('[ ]+', ' ', tagline)
        tagline = tagline.rstrip()
        if len(language)>0:
            self.notes = "%s: %s\n" %(_('Language').encode('utf8'), language)
        if len(sound)>0:
            self.notes += "%s: %s\n" %(gutils.strip_tags(_('<b>Audio</b>').encode('utf8')), sound)
        if len(color)>0:
            self.notes += "%s: %s\n" %(_('Color').encode('utf8'), color)
        if len(tagline)>0:
            self.notes += "%s: %s\n" %('Tagline', tagline)
    
    def __before_more(self, data):
        tmp = string.find(data, '>mehr<')
        if tmp>0:
            data = data[:tmp] + '>'
        return data

    def regextrim(self,text,key1,key2):
        obj = re.search(key1, text)
        if obj is None:
            return ''
        else:
            p1 = obj.end()
        obj = re.search(key2, text[p1:])
        if obj is None:
            return ''
        else:
            p2 = p1 + obj.start()
        return text[p1:p2]

class SearchPlugin(movie.SearchMovie):
    PATTERN = re.compile(r"""<a href=['"]/title/tt([0-9]+)/["']>(.*?)(</td>|</A>)""", re.IGNORECASE)
    PATTERN_POWERSEARCH = re.compile(r"""Here are the [0-9]+ matching titles""")

    def __init__(self):
        self.original_url_search    = 'http://german.imdb.com/find?more=tt&q='
        self.translated_url_search    = 'http://german.imdb.com/List?words='
        self.encode = 'iso8859-1'
        self.remove_accents = False

    def search(self,parent_window):
        self.open_search(parent_window)
        tmp = gutils.trim(self.page, ' angezeigt)', ' Treffergenauigkeit')
        if tmp == '':
            if self.PATTERN_POWERSEARCH.search(self.page) is None:
                self.page = ''
        else:
            self.page = tmp 
        # correction of all &#xxx entities
        self.page = self.page.decode(self.encode)
        self.page = gutils.convert_entities(self.page)
        self.page = self.page.encode(self.encode)
        return self.page

    def get_searches(self):
        elements = string.split(self.page, '<tr>')
        if len(elements) < 2:
            elements = string.split(self.page, '<TR>')

        if len(elements):
            for element in elements[1:]:
                match = self.PATTERN.findall(element)
                for entry in match:
                    tmp  = gutils.clean(entry[1])
                    self.ids.append(entry[0])
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
        'Rocky Balboa'            : [ 3, 13 ],
        'Ein glückliches Jahr'    : [ 1, 30 ]
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
        '0479143' : { 
            'title'             : 'Rocky Balboa',
            'o_title'             : 'Rocky Balboa',
            'director'            : 'Sylvester Stallone',
            'plot'                 : True,
            'cast'                : 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie Panina\n\
Antonio Tarver' + _(' as ') + 'Mason \'The Line\' Dixon\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Milo Ventimiglia' + _(' as ') + 'Robert Balboa Jr.\n\
Tony Burton' + _(' as ') + 'Duke\n\
A.J. Benza' + _(' as ') + 'L.C.\n\
James Francis Kelly III' + _(' as ') + 'Steps\n\
Talia Shire' + _(' as ') + 'Adrian (archive footage)\n\
Lou DiBella' + _(' as ') + 'Himself\n\
Mike Tyson' + _(' as ') + 'Himself\n\
Henry G. Sanders' + _(' as ') + 'Martin\n\
Pedro Lovell' + _(' as ') + 'Spider Rico\n\
Ana Gerena' + _(' as ') + 'Isabel\n\
Angela Boyd' + _(' as ') + 'Angie\n\
Louis Giansante' + _(' as ') + 'Bar Thug\n\
Maureen Schilling' + _(' as ') + 'Lucky\'s Bartender\n\
Lahmard J. Tate' + _(' as ') + 'X-Cell (as Lahmard Tate)\n\
Woody Paige' + _(' as ') + 'ESPN Commentator (as Woodrow W. Paige)\n\
Skip Bayless' + _(' as ') + 'ESPN Commentator\n\
Jay Crawford' + _(' as ') + 'ESPN Commentator\n\
Brian Kenny' + _(' as ') + 'ESPN Host\n\
Dana Jacobson' + _(' as ') + 'ESPN Host\n\
Charles Johnson' + _(' as ') + 'ESPN Host (as Chuck Johnson)\n\
James Binns' + _(' as ') + 'Commissioner (as James J. Binns)\n\
Johnnie Hobbs Jr.' + _(' as ') + 'Commissioner\n\
Barney Fitzpatrick' + _(' as ') + 'Commissioner\n\
Jim Lampley' + _(' as ') + 'HBO Commentator\n\
Larry Merchant' + _(' as ') + 'HBO Commentator\n\
Max Kellerman' + _(' as ') + 'HBO Commentator\n\
LeRoy Neiman' + _(' as ') + 'Himself\n\
Bert Randolph Sugar' + _(' as ') + 'Ring Magazine Reporter\n\
Bernard Fernández' + _(' as ') + 'Boxing Association of America Writer (as Bernard Fernandez)\n\
Gunnar Peterson' + _(' as ') + 'Weightlifting Trainer\n\
Yahya' + _(' as ') + 'Dixon\'s Opponent\n\
Marc Ratner' + _(' as ') + 'Weigh-In Official\n\
Anthony Lato Jr.' + _(' as ') + 'Rocky\'s Inspector\n\
Jack Lazzarado' + _(' as ') + 'Dixon\'s Inspector\n\
Michael Buffer' + _(' as ') + 'Ring Announcer\n\
Joe Cortez' + _(' as ') + 'Referee\n\
Carter Mitchell' + _(' as ') + 'Shamrock Foreman\n\
Vinod Kumar' + _(' as ') + 'Ravi\n\
Fran Pultro' + _(' as ') + 'Father at Restaurant\n\
Frank Stallone' + _(' as ') + 'Dinner Patron (as Frank Stallone Jr.)\n\
Jody Giambelluca' + _(' as ') + 'Dinner Patron\n\
Tobias Segal' + _(' as ') + 'Robert\'s Friend\n\
Tim Carr' + _(' as ') + 'Robert\'s Friend\n\
Matt Frack' + _(' as ') + 'Robert\'s Friend #3\n\
Paul Dion Monte' + _(' as ') + 'Robert\'s Friend\n\
Kevin King Templeton' + _(' as ') + 'Robert\'s Friend (as Kevin King-Templeton)\n\
Robert Michael Kelly' + _(' as ') + 'Mr. Tomilson\n\
Rick Buchborn' + _(' as ') + 'Rocky Fan\n\
Nick Baker' + _(' as ') + 'Irish Pub Bartender\n\
Don Sherman' + _(' as ') + 'Andy\n\
Stu Nahan' + _(' as ') + 'Computer Fight Commentator (voice)\n\
Gary Compton' + _(' as ') + 'Security Guard\n\
übrige Besetzung in alphabetischer Reihenfolge:\n\
Ricky Cavazos' + _(' as ') + 'Boxing Spectator (uncredited)\n\
David Kneeream' + _(' as ') + 'Adrian\'s Patron (uncredited)\n\
Dolph Lundgren' + _(' as ') + 'Captain Ivan Drago (archive footage) (uncredited)\n\
Burgess Meredith' + _(' as ') + 'Mickey Goldmill (archive footage) (uncredited)\n\
Keith Moyer' + _(' as ') + 'Bar Patron (uncredited)\n\
Mr. T' + _(' as ') + 'Clubber Lang (archive footage) (uncredited)',
            'country'            : 'USA',
            'genre'                : 'Action | Sport',
            'classification'    : False,
            'studio'            : 'Metro-Goldwyn-Mayer (MGM)',
            'o_site'            : False,
            'site'                : 'http://german.imdb.com/title/tt0479143',
            'trailer'            : 'http://german.imdb.com/title/tt0479143/trailers',
            'year'                : 2006,
            'notes'                : _('Language') + ': Englisch | Spanisch\n'\
+ _('Audio') + ': DTS | Dolby Digital | SDDS\n'\
+ _('Color') + ': Farbe\n\
Tagline: It ain\'t over \'til it\'s over.',
            'runtime'            : 102,
            'image'                : True,
            'rating'            : 7
        },
        '0069815' : { 
            'title'             : 'Glückliches Jahr, Ein',
            'o_title'             : 'Bonne année, La',
            'director'            : 'Claude Lelouch',
            'plot'                 : True,
            'cast'                : 'Lino Ventura' + _(' as ') + 'Simon\n\
Françoise Fabian' + _(' as ') + 'Françoise\n\
Charles Gérard' + _(' as ') + 'Charlot\n\
André Falcon' + _(' as ') + 'Le bijoutier\n\
Mireille Mathieu' + _(' as ') + 'Herself / Elle-même\n\
Lilo' + _(' as ') + 'Madame Félix\n\
Claude Mann' + _(' as ') + 'L\'intellectuel\n\
Frédéric de Pasquale' + _(' as ') + 'L\'amant parisien\n\
Gérard Sire' + _(' as ') + 'Le directeur de la prison\n\
Silvano Tranquilli' + _(' as ') + 'L\'amant italien\n\
André Barello\n\
Michel Bertay\n\
Norman de la Chesnaye\n\
Pierre Edeline\n\
Pierre Pontiche\n\
Michou' + _(' as ') + 'Himself\n\
Bettina Rheims' + _(' as ') + 'La jeune vendeuse\n\
Joseph Rythmann\n\
Georges Staquet\n\
Jacques Villedieu\n\
Harry Walter\n\
übrige Besetzung in alphabetischer Reihenfolge:\n\
Anouk Aimée' + _(' as ') + 'Une femme (archive footage) (uncredited)\n\
Elie Chouraqui' + _(' as ') + '(uncredited)\n\
Rémy Julienne' + _(' as ') + 'Chauffeur de taxi (uncredited)\n\
Jean-Louis Trintignant' + _(' as ') + 'Un homme (archive footage) (uncredited)',
            'country'            : 'France | Italy',
            'genre'                : 'Komödie',
            'classification'    : False,
            'studio'            : 'Les Films 13',
            'o_site'            : False,
            'site'                : 'http://german.imdb.com/title/tt0069815',
            'trailer'            : 'http://german.imdb.com/title/tt0069815/trailers',
            'year'                : 1973,
            'notes'                : _('Language') + ': Französisch\n'\
+ _('Audio') + ': Mono\n'\
+ _('Color') + ': Farbe (Eastmancolor)',
            'runtime'            : 90,
            'image'                : True,
            'rating'            : 7
        },
    }
