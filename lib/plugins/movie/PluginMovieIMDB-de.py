# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007-2011 Michael Jahn
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

plugin_name         = 'IMDb-de'
plugin_description  = 'Internet Movie Database German'
plugin_url          = 'www.imdb.de'
plugin_language     = _('German')
plugin_author       = 'Michael Jahn'
plugin_author_email = 'mikej06@hotmail.com'
plugin_version      = '1.8'

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   = 'iso8859-1'
        self.movie_id = id
        self.url      = "http://www.imdb.de/title/tt%s" % str(self.movie_id)

    def initialize(self):
        self.cast_page = self.open_page(url=self.url + '/fullcredits')
        self.plot_page = self.open_page(url=self.url + '/plotsummary')
        self.comp_page = self.open_page(url=self.url + '/companycredits')
        # looking for the original imdb page
        self.imdb_page = self.open_page(url="http://www.imdb.com/title/tt%s" % str(self.movie_id))
        self.imdb_plot_page = self.open_page(url="http://www.imdb.com/title/tt%s/plotsummary" % str(self.movie_id))
        # correction of all &#xxx entities
        self.page = gutils.convert_entities(self.page)
        self.cast_page = gutils.convert_entities(self.cast_page)
        self.plot_page = gutils.convert_entities(self.plot_page)
        self.comp_page = gutils.convert_entities(self.comp_page)
        self.imdb_page = gutils.convert_entities(self.imdb_page)
        self.imdb_plot_page = gutils.convert_entities(self.imdb_plot_page)

    def get_image(self):
        tmp = string.find(self.page, 'a name="poster"')
        if tmp == -1:        # poster not available
            self.image_url = ''
        else:
            self.image_url = gutils.trim(self.page[tmp:], 'src="', '"')

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<h1>', '<span')
        tmp = gutils.regextrim(self.page, '<h5>(Alternativ|Auch bekannt als):', '</div>')
        if tmp:
            elements = string.split(tmp, '<br>')
            for element in elements:
                index = string.find(element,'(Originaltitel)')
                if index > 0:
                    tmp = element[:index]
                    self.o_title = gutils.before(tmp, '- ')
                    if not self.o_title:
                        self.o_title = tmp
                    self.o_title = string.replace(self.o_title, '"', '')
                    break

    def get_title(self):
        self.title = gutils.trim(self.page, '<h1>', '<span')
        elements = string.split(gutils.regextrim(self.page, '<h5>(Alternativ|Auch bekannt als):', '</div>'), '<i class="transl"')
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
        self.plot = gutils.trim(self.page, '<h5>Handlung:</h5>', '</div>')
        self.plot = self.__before_more(self.plot)
        germanplot = gutils.clean(gutils.trim(self.plot_page, '<div id="swiki.2.1">', '</div>').replace('<br/>', '\n'))
        if germanplot:
            self.plot = germanplot
        if self.plot == '':
            # nothing in german found, try original
            self.plot = gutils.regextrim(self.imdb_page, '<h5>Plot:</h5>', '(</div>|<a href.*)')
            self.plot = self.__before_more(self.plot)
            elements = string.split(self.imdb_plot_page, '<p class="plotpar">')
            if len(elements) > 1:
                self.plot = self.plot + '\n\n'
                elements[0] = ''
                for element in elements:
                    if element <> '':
                        self.plot = self.plot + gutils.strip_tags(gutils.before(element, '</a>')) + '\n\n'

    def get_year(self):
        self.year = gutils.trim(self.page, '<h1>', ' <span class')
        self.year = gutils.trim(self.year, '(', ')')

    def get_runtime(self):
        self.runtime = gutils.regextrim(self.page, '<h5>L[^n]+nge:</h5>', ' [Mm]in')

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
        self.cast = re.sub('</tr>[ \t]*<tr[ \t]*class="even">', "\n", self.cast)
        self.cast = re.sub('</tr>[ \t]*<tr[ \t]*class="odd">', "\n", self.cast)
        self.cast = self.__before_more(self.cast)
        self.cast = re.sub('[ ]+', ' ', self.cast)

    def get_classification(self):
        self.classification = gutils.trim(gutils.trim(self.page, 'Altersfreigabe:', '</div>'), 'Deutschland:', '|')

    def get_studio(self):
        self.studio = gutils.trim(self.comp_page, '<h2>Produktionsfirmen</h2>', '</ul>')
        self.studio = string.replace(self.studio, '</li><li>', ', ')
        if not self.studio:
            self.studio = gutils.trim(self.page, '<h5>Firma:</h5>', '</div>')
            self.studio = self.__before_more(self.studio)

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = "http://www.imdb.de/title/tt%s" % self.movie_id

    def get_trailer(self):
        self.trailer = "http://www.imdb.com/title/tt%s/trailers" % self.movie_id

    def get_country(self):
        self.country = gutils.trim(self.page, '<h5>Land:</h5>', '</div>')
        self.country = self.__before_more(self.country)
        self.country = re.sub('[\n]+', '', self.country)
        self.country = re.sub('[ ]+', ' ', self.country)

    def get_rating(self):
        self.rating = gutils.trim(self.page, '<h5>Nutzer-Bewertung:</h5>', '/10')
        if self.rating:
            try:
                tmp = re.findall('[0-9.,]+', gutils.clean(self.rating))
                if tmp and len(tmp) > 0:
                    self.rating = round(float(tmp[0].replace(',', '.')))
            except:
                self.rating = 0
        else:
            self.rating = 0

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

    def get_screenplay(self):
        self.screenplay = ''
        parts = re.split('<a href=', gutils.trim(self.cast_page, '>Buch<', '</table>'))
        if len(parts) > 1:
            for part in parts[1:]:
                screenplay = gutils.trim(part, '>', '<')
                if screenplay == 'WGA':
                    continue
                screenplay = screenplay.replace(' (geschrieben von)', '')
                screenplay = screenplay.replace(' (original scenario)', '')
                screenplay = screenplay.replace(' und<', '<')
                self.screenplay = self.screenplay + screenplay + ', '
            if len(self.screenplay) > 2:
                self.screenplay = self.screenplay[0:len(self.screenplay) - 2]

    def get_cameraman(self):
        self.cameraman = gutils.trim(self.cast_page, '>Kamera</a>', '</table>')
        self.cameraman = string.replace(self.cameraman, '(Kamera)', '')
        self.cameraman = string.replace(self.cameraman, '(nicht im Abspann)', '')
        self.cameraman = string.replace(self.cameraman, '</a>', ', ')
        self.cameraman = gutils.clean(self.cameraman)
        self.cameraman = re.sub(',[ \t]*$', '', self.cameraman)
        self.cameraman = re.sub('[ ]+', ' ', self.cameraman)

    def __before_more(self, data):
        for element in ['>Mehr ansehen<', '>mehr<', '>Full summary<', '>Full synopsis<']:
            tmp = string.find(data, element)
            if tmp>0:
                data = data[:tmp] + '>'
        return data

class SearchPlugin(movie.SearchMovie):
    PATTERN = re.compile(r"""<a href=['"]/title/tt([0-9]+)/["'](.*?)</tr>""", re.IGNORECASE)
    PATTERN_POWERSEARCH = re.compile(r"""Here are the [0-9]+ matching titles""")

    def __init__(self):
        self.original_url_search   = 'http://www.imdb.de/find?more=tt&q='
        self.translated_url_search = 'http://www.imdb.de/find?more=tt&q='
        self.encode                = 'utf8'
        self.remove_accents        = False

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        tmp = gutils.trim(self.page, ' angezeigt)', ' Treffergenauigkeit')
        if tmp == '':
            if self.PATTERN_POWERSEARCH.search(self.page) is None:
                self.page = ''
        else:
            self.page = tmp
        # correction of all &#xxx entities
        self.page = self.page.decode('iso8859-1')
        self.page = gutils.convert_entities(self.page)
        #self.page = self.page.encode(self.encode)
        return self.page

    def get_searches(self):
        elements = string.split(self.page, '<tr>')
        if len(elements) < 2:
            elements = string.split(self.page, '<TR>')

        if len(elements):
            for element in elements[1:]:
                match = self.PATTERN.findall(element)
                for entry in match:
                    tmp  = re.sub('^[0-9]+[.]', '', gutils.clean(gutils.after(entry[1], '>')))
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
        'Rocky Balboa'         : [ 23, 23 ],
        'Ein glückliches Jahr' : [  6,  6 ]
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
            'o_title'           : 'Rocky Balboa',
            'director'          : 'Sylvester Stallone',
            'plot'              : True,
            'cast'              : 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie\n\
Antonio Tarver' + _(' as ') + 'Mason \'The Line\' Dixon\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Milo Ventimiglia' + _(' as ') + 'Robert Balboa Jr.\n\
Tony Burton' + _(' as ') + 'Duke\n\
A.J. Benza' + _(' as ') + 'L.C.\n\
James Francis Kelly III' + _(' as ') + 'Steps\n\
Talia Shire' + _(' as ') + 'Adrian (Archivmaterial)\n\
Lou DiBella' + _(' as ') + 'als er selbst\n\
Mike Tyson' + _(' as ') + 'als er selbst\n\
Henry G. Sanders' + _(' as ') + 'Martin\n\
Pedro Lovell' + _(' as ') + 'Spider Rico\n\
Ana Gerena' + _(' as ') + 'Isabel\n\
Angela Boyd' + _(' as ') + 'Angie\n\
Louis Giansante' + _(' as ') + 'Bar Thug\n\
Maureen Schilling' + _(' as ') + 'Lucky\'s Bartender\n\
Lahmard J. Tate' + _(' as ') + 'X-Cell (als Lahmard Tate)\n\
Woody Paige' + _(' as ') + 'ESPN Commentator (als Woodrow W. Paige)\n\
Skip Bayless' + _(' as ') + 'ESPN Commentator\n\
Jay Crawford' + _(' as ') + 'ESPN Commentator\n\
Brian Kenny' + _(' as ') + 'ESPN Host\n\
Dana Jacobson' + _(' as ') + 'ESPN Host\n\
Charles Johnson' + _(' as ') + 'ESPN Host (als Chuck Johnson)\n\
James Binns' + _(' as ') + 'Commissioner (als James J. Binns)\n\
Johnnie Hobbs Jr.' + _(' as ') + 'Commissioner\n\
Barney Fitzpatrick' + _(' as ') + 'Commissioner\n\
Jim Lampley' + _(' as ') + 'HBO Commentator\n\
Larry Merchant' + _(' as ') + 'HBO Commentator\n\
Max Kellerman' + _(' as ') + 'HBO Commentator\n\
LeRoy Neiman' + _(' as ') + 'als er selbst\n\
Bert Randolph Sugar' + _(' as ') + 'Ring Magazine Reporter\n\
Bernard Fernández' + _(' as ') + 'Boxing Association of America Writer (als Bernard Fernandez)\n\
Gunnar Peterson' + _(' as ') + 'Weightlifting Trainer\n\
Yahya' + _(' as ') + 'Dixon\'s Opponent\n\
Marc Ratner' + _(' as ') + 'Weigh-In Official\n\
Anthony Lato Jr.' + _(' as ') + 'Rocky\'s Inspector\n\
Jack Lazzarado' + _(' as ') + 'Dixon\'s Inspector\n\
Michael Buffer' + _(' as ') + 'Ring Announcer\n\
Joe Cortez' + _(' as ') + 'Schiedsrichter\n\
Carter Mitchell' + _(' as ') + 'Shamrock Foreman\n\
Vinod Kumar' + _(' as ') + 'Ravi\n\
Fran Pultro' + _(' as ') + 'Father at Restaurant\n\
Frank Stallone' + _(' as ') + 'Dinner Patron (als Frank Stallone Jr.)\n\
Jody Giambelluca' + _(' as ') + 'Dinner Patron\n\
Tobias Segal' + _(' as ') + 'Robert\'s Friend\n\
Tim Carr' + _(' as ') + 'Robert\'s Friend\n\
Matt Frack' + _(' as ') + 'Robert\'s Friend #3\n\
Paul Dion Monte' + _(' as ') + 'Robert\'s Friend\n\
Kevin King Templeton' + _(' as ') + 'Robert\'s Friend (als Kevin King-Templeton)\n\
Robert Michael Kelly' + _(' as ') + 'Mr. Tomilson\n\
Rick Buchborn' + _(' as ') + 'Rocky Fan\n\
Nick Baker' + _(' as ') + 'Irish Pub Bartender\n\
Don Sherman' + _(' as ') + 'Andy\n\
Stu Nahan' + _(' as ') + 'Computer Fight Commentator (Sprechrolle)\n\
Gary Compton' + _(' as ') + 'Sicherheitsbediensteter übrige Besetzung in alphabetischer Reihenfolge:\n\
Vale Anoai' + _(' as ') + 'Shopper in Italian Market\n\
Sikander Malik' + _(' as ') + 'Boxer\n\
Michael Ahl' + _(' as ') + 'Restaurant Patron (nicht im Abspann)\n\
Andrew Aninsman' + _(' as ') + 'Promoter (nicht im Abspann)\n\
Ben Bachelder' + _(' as ') + 'The Arm (nicht im Abspann)\n\
Lacy Bevis' + _(' as ') + 'Boxing Spectator (nicht im Abspann)\n\
Tim Brooks' + _(' as ') + 'Boxing Spectator (nicht im Abspann)\n\
D.T. Carney' + _(' as ') + 'High Roller (nicht im Abspann)\n\
Ricky Cavazos' + _(' as ') + 'Boxing Spectator (nicht im Abspann)\n\
Rennie Cowan' + _(' as ') + 'Boxing Spectator (nicht im Abspann)\n\
Deon Derrico' + _(' as ') + 'High Roller at Limo (nicht im Abspann)\n\
Jacob \'Stitch\' Duran' + _(' as ') + 'Dixon\'s Trainer (nicht im Abspann)\n\
Simon P Edwards' + _(' as ') + 'Crowd Member (nicht im Abspann)\n\
Ruben Fischman' + _(' as ') + 'High-Roller in Las Vegas (nicht im Abspann)\n\
David Gere' + _(' as ') + 'Patron at Adrian\'s (nicht im Abspann)\n\
Noah Jacobs' + _(' as ') + 'Boxing Fan (nicht im Abspann)\n\
Mark J. Kilbane' + _(' as ') + 'Businessman (nicht im Abspann)\n\
Zach Klinefelter' + _(' as ') + 'Boxing Spectator (nicht im Abspann)\n\
David Kneeream' + _(' as ') + 'Adrian\'s Patron (nicht im Abspann)\n\
Dolph Lundgren' + _(' as ') + 'Captain Ivan Drago (Archivmaterial) (nicht im Abspann)\n\
Dean Mauro' + _(' as ') + 'Sports Journalist (nicht im Abspann) (unbestätigt)\n\
Burgess Meredith' + _(' as ') + 'Mickey Goldmill (Archivmaterial) (nicht im Abspann)\n\
Dan Montero' + _(' as ') + 'Boxing Spectator (nicht im Abspann)\n\
Keith Moyer' + _(' as ') + 'Bargast (nicht im Abspann)\n\
Mr. T' + _(' as ') + 'Clubber Lang (Archivmaterial) (nicht im Abspann)\n\
Jacqueline Olivia' + _(' as ') + 'Mädchen (nicht im Abspann)\n\
Brian H. Scott' + _(' as ') + 'Ringside Cop #1 (nicht im Abspann)\n\
Keyon Smith' + _(' as ') + 'Boxing Spectator (nicht im Abspann)\n\
Frank Traynor' + _(' as ') + 'Rechtsanwalt (nicht im Abspann)\n\
Ryan Tygh' + _(' as ') + 'Ring Photographer (nicht im Abspann)\n\
Kimberly Villanova' + _(' as ') + 'Businesswoman (nicht im Abspann)',
            'country'           : 'USA',
            'genre'             : 'Drama | Sport',
            'classification'    : False,
            'studio'            : 'Metro-Goldwyn-Mayer (MGM) (presents) (copyright owner), Columbia Pictures (presents) (copyright owner), Revolution Studios (presents) (copyright owner), Chartoff-Winkler Productions, Rogue Marble',
            'o_site'            : False,
            'site'              : 'http://www.imdb.de/title/tt0479143',
            'trailer'           : 'http://www.imdb.com/title/tt0479143/trailers',
            'year'              : 2006,
            'notes'             : _('Language') + ': Englisch | Spanisch\n'\
+ _('Audio') + ': DTS | Dolby Digital | SDDS\n'\
+ _('Color') + ': Farbe',
            'runtime'           : 102,
            'image'             : True,
            'rating'            : 7,
            'screenplay'        : 'Sylvester Stallone, Sylvester Stallone',
            'cameraman'         : 'Clark Mathis'
        },
        '0069815' : {
            'title'             : 'Ein glückliches Jahr',
            'o_title'           : 'La bonne année',
            'director'          : 'Claude Lelouch',
            'plot'              : True,
            'cast'              : 'Lino Ventura' + _(' as ') + 'Simon\n\
Françoise Fabian' + _(' as ') + 'Françoise\n\
Charles Gérard' + _(' as ') + 'Charlot\n\
André Falcon' + _(' as ') + 'Le bijoutier\n\
Mireille Mathieu' + _(' as ') + 'als sie selbst / Elle-même\n\
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
Michou' + _(' as ') + 'als er selbst\n\
Bettina Rheims' + _(' as ') + 'La jeune vendeuse\n\
Joseph Rythmann\n\
Georges Staquet\n\
Jacques Villedieu\n\
Harry Walter übrige Besetzung in alphabetischer Reihenfolge:\n\
Anouk Aimée' + _(' as ') + 'Une femme (Archivmaterial) (nicht im Abspann)\n\
Elie Chouraqui' + _(' as ') + ' (nicht im Abspann)\n\
Rémy Julienne' + _(' as ') + 'Chauffeur de taxi (nicht im Abspann)\n\
Jean-Louis Trintignant' + _(' as ') + 'Un homme (Archivmaterial) (nicht im Abspann)',
            'country'            : 'Frankreich | Italien',
            'genre'              : 'Komödie',
            'classification'     : '12 (f)',
            'studio'             : 'Les Films 13, Rizzoli Film',
            'o_site'             : False,
            'site'               : 'http://www.imdb.de/title/tt0069815',
            'trailer'            : 'http://www.imdb.com/title/tt0069815/trailers',
            'year'               : 1973,
            'notes'              : _('Language') + ': Französisch\n'\
+ _('Audio') + ': Mono\n'\
+ _('Color') + ': Farbe (Eastmancolor)',
            'runtime'            : 90,
            'image'              : True,
            'rating'             : 7,
            'screenplay'         : 'Claude Lelouch, Pierre Uytterhoeven, Claude Lelouch',
            'cameraman'          : 'Claude Lelouch'
        },
    }
