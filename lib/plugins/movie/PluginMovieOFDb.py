# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Written by Christian Sagmueller <christian@sagmueller.net>
# based on PluginMovieIMDB.py, Copyright (c) 2005 Vasco Nunes
# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

import gutils
import movie,string,re

plugin_name = "OFDb"
plugin_description = "Online-Filmdatenbank"
plugin_url = "www.ofdb.de"
plugin_language = _("German")
plugin_author = "Christian Sagmueller, Jessica Katharina Parth"
plugin_author_email = "Jessica.K.P@women-at-work.org"
plugin_version = "0.10"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode='utf-8'
        self.movie_id = id
        self.url = "http://www.ofdb.de/%s" % str(self.movie_id)

    def initialize(self):
        # OFDb didn't provide the runtime, studio and classification but it provide a link to the german imdb entry
        # lets use the imdb page, why not
        imdb_nr = gutils.trim(self.page, 'http://german.imdb.com/Title?', '"')
        if imdb_nr != '':
            self.imdb_page = self.open_page(url='http://german.imdb.com/Title?' + imdb_nr)
        else:
            imdb_nr = gutils.trim(self.page, 'http://www.imdb.com/Title?', '"')
            if imdb_nr != '':
                self.imdb_page = self.open_page(url='http://www.imdb.com/Title?' + imdb_nr)
            else:
                self.imdb_page = ''

    def get_image(self):
        self.image_url = "http://img.ofdb.de/film/" + gutils.trim(self.page, 'img src="http://img.ofdb.de/film/', '"' )
        
    def get_o_title(self):
        self.o_title = gutils.clean(gutils.trim(self.page, 'Originaltitel:', '</tr>'))
        if self.o_title == '':
            self.o_title = string.replace(self.o_title, '&nbsp;', '' )

    def get_title(self):
        self.title = gutils.trim(self.page,'size="3"><b>','<')

    def get_director(self):
        self.director = gutils.trim(self.page,"Regie:","</a><br>")

    def get_plot(self):
        storyid = gutils.regextrim(self.page, '<a href="plot/', '(">|[&])')
        if not storyid is None:
            story_page = self.open_page(url="http://www.ofdb.de/plot/%s" % (storyid))
        self.plot = gutils.trim(story_page, "</b><br><br>","</")

    def get_year(self):
        self.year = gutils.trim(self.page,"Erscheinungsjahr:","</a>")
        self.year = gutils.strip_tags(self.year)

    def get_runtime(self):
        # from imdb
        self.runtime = gutils.regextrim(self.imdb_page, '<h5>(L&auml;nge|Runtime):</h5>', ' (min|Min)')

    def get_genre(self):
        self.genre = gutils.trim(self.page,"Genre(s):","</table>")
        self.genre = string.replace(self.genre, "<br>", ", ")
        self.genre = gutils.strip_tags(self.genre)
        self.genre = string.replace(self.genre, "/", ", ")
        self.genre = gutils.clean(self.genre)
        self.genre = self.genre[0:-1]

    def get_cast(self):
        self.cast = ''
        movie_id_elements = string.split(self.movie_id, ',')
        movie_id_elements[0] = string.replace(movie_id_elements[0], "film/", "")
        cast_page = self.open_page(url="http://www.ofdb.de/view.php?page=film_detail&fid=%s" % str(movie_id_elements[0]) )
        self.cast = gutils.trim(cast_page, 'Darsteller</i>', '</table>')
        self.cast = re.sub('(\n|\t|&nbsp;)', '', self.cast)
        self.cast = string.replace(self.cast, '\t', '')
        self.cast = string.replace(self.cast, 'class="Daten">', '>\n')
        self.cast = string.strip(gutils.strip_tags(self.cast))
        self.cast = string.replace(self.cast, '... ', _(' as '))
        self.cast = gutils.clean(self.cast)

    def get_classification(self):
        # from imdb
        self.classification = gutils.regextrim(gutils.regextrim(self.imdb_page, '(Altersfreigabe|Certification):', '</div>'), 'Germany:', '(&|[|])')

    def get_studio(self):
        # from imdb
        self.studio = gutils.regextrim(self.imdb_page, '<h5>(Firma|Company):</h5>', '</a>')

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ""

    def get_country(self):
        self.country = gutils.trim(self.page,"Herstellungsland:","</a>")

    def get_rating(self):
        self.rating = gutils.trim(self.page,"<br>Note: ","&nbsp;")
        if self.rating == '':
            self.rating = "0"
        self.rating = str(round(float(self.rating)))

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.original_url_search   = "http://www.ofdb.de/view.php?page=suchergebnis&Kat=OTitel&SText="
        self.translated_url_search = "http://www.ofdb.de/view.php?page=suchergebnis&Kat=DTitel&SText="
        self.encode='utf-8'
        self.remove_accents = False

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        self.page = gutils.trim(self.page,"</b><br><br>", "<br><br><br>");
        self.page = string.replace( self.page, "'", '"' )
        self.page = string.replace( self.page, '<font size="1">', '' )
        self.page = string.replace( self.page, '</font>', '' )
        return self.page

    def get_searches(self):
        elements = string.split(self.page,"<br>")

        if (elements[0]<>''):
            for element in elements:
                elementid = gutils.trim(element,'<a href="','"')
                if not elementid is None and not elementid == '':
                    self.ids.append(elementid)
                    elementname = gutils.clean(element)
                    p1 = string.find(elementname, '>')
                    if p1 == -1:
                        self.titles.append(elementname)
                    else:
                        self.titles.append(elementname[p1+1:])

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Rocky Balboa' : [ 1, 1 ],
        'Arahan'       : [ 3, 2 ],
        'glückliches'  : [ 4, 2 ]
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
        'film/103013,Rocky%20Balboa' : { 
            'title'             : 'Rocky Balboa',
            'o_title'             : 'Rocky Balboa',
            'director'            : 'Sylvester Stallone',
            'plot'                 : True,
            'cast'                : 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Burt Young' + _(' as ') + 'Paulie\n\
Milo Ventimiglia' + _(' as ') + 'Robert Jr.\n\
Geraldine Hughes' + (' as ') + 'Marie\n\
James Francis Kelly III\n\
Tony Burton\n\
A.J. Benza\n\
Henry G. Sanders\n\
Antonio Tarver' + (' as ') + 'Mason \'The Line\' Dixon\n\
Pedro Lovell\n\
Ana Gerena\n\
Angela Boyd\n\
Louis Giansante\n\
Maureen Schilling\n\
Carter Mitchell\n\
Vinod Kumar\n\
Tobias Segal\n\
Tim Carr\n\
Paul Dion Monte\n\
Kevin King Templeton\n\
Robert Michael Kelly\n\
Don Sherman\n\
Nick Baker\n\
Rick Buchborn\n\
Stu Nahan\n\
Gary Compton\n\
Jody Giambelluca\n\
Frank Stallone\n\
Fran Pultro\n\
Michael Buffer as Ring Announcer\n\
Jack Lazzarado\n\
Marc Ratner\n\
Anthony Lato Jr.\n\
Yahya\n\
Gunnar Peterson\n\
Bernard Fernández\n\
Bert Randolph Sugar\n\
Jim Lampley\n\
Larry Merchant\n\
Max Kellerman\n\
James Binns\n\
Johnnie Hobbs Jr.\n\
Barney Fitzpatrick\n\
Brian Kenny\n\
Dana Jacobson\n\
Skip Bayless\n\
Charles Johnson\n\
Matt Frack\n\
Woody Paige\n\
Jay Crawford\n\
Lahmard J. Tate\n\
LeRoy Neiman\n\
Mike Tyson' + _(' as ') + 'Himself\n\
Lou DiBella\n\
Joe Cortez\n\
Ricky Cavazos',
            'country'            : 'USA',
            'genre'                : 'Action, Drama, Sportfilm',
            'classification'    : False,
            'studio'            : 'Metro-Goldwyn-Mayer (MGM)',
            'o_site'            : False,
            'site'                : 'http://www.ofdb.de/film/103013,Rocky%20Balboa',
            'trailer'            : False,
            'year'                : 2006,
            'notes'                : False,
            'runtime'            : 102,
            'image'                : True,
            'rating'            : 8
        },
        'film/22489,Ein-Gl%C3%BCckliches-Jahr' : { 
            'title'             : 'Glückliches Jahr, Ein',
            'o_title'             : 'Bonne année, La',
            'director'            : 'Claude Lelouch',
            'plot'                 : False,
            'cast'                : 'Lino Ventura\n\
Françoise Fabian\n\
Charles Gérard\n\
André Falcon as Le bijoutier\n\
Mireille Mathieu\n\
Lilo\n\
Claude Mann\n\
Frédéric de Pasquale\n\
Gérard Sire\n\
Silvano Tranquilli\n\
André Barello\n\
Michel Bertay\n\
Norman de la Chesnaye\n\
Pierre Edeline\n\
Pierre Pontiche\n\
Michou\n\
Bettina Rheims\n\
Joseph Rythmann\n\
Georges Staquet\n\
Jacques Villedieu\n\
Harry Walter\n\
Elie Chouraqui',
            'country'            : 'Frankreich',
            'genre'                : 'Komödie, Krimi',
            'classification'    : False,
            'studio'            : 'Les Films 13',
            'o_site'            : False,
            'site'                : 'http://www.ofdb.de/film/22489,Ein-Gl%C3%BCckliches-Jahr',
            'trailer'            : False,
            'year'                : 1973,
            'notes'                : False,
            'runtime'            : 90,
            'image'                : True,
            'rating'            : 6
        },
        'film/54088,Arahan' : { 
            'title'             : 'Arahan',
            'o_title'             : 'Arahan jangpung daejakjeon',
            'director'            : 'Ryoo Seung-wan',
            'plot'                 : True,
            'cast'                : 'Ryoo Seung-beom\n\
Yoon Soy' + _(' as ') + 'Wi-jin\n\
Ahn Sung-kee' + _(' as ') + 'Ja-woon\n\
Jung Doo-hong' + _(' as ') + 'Heuk-Woon\n\
Yun Ju-sang\n\
Kim Ji-yeong\n\
Baek Chan-gi\n\
Kim Jae-man\n\
Lee Dae-yeon\n\
Kim Dong-ju\n\
Kim Su-hyeon\n\
Geum Dong-hyeon\n\
Lee Jae-goo\n\
Ahn Kil-kang\n\
Bong Tae-gyu\n\
Im Ha-ryong\n\
Yoon Do-hyeon\n\
Lee Choon-yeon',
            'country'            : 'Südkorea',
            'genre'                : 'Action, Fantasy, Komödie',
            'classification'    : '16',
            'studio'            : 'Fun and Happiness',
            'o_site'            : False,
            'site'                : 'http://www.ofdb.de/film/54088,Arahan',
            'trailer'            : False,
            'year'                : 2004,
            'notes'                : False,
            'runtime'            : 114,
            'image'                : True,
            'rating'            : 7
        }
    }
