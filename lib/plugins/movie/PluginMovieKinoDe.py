# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2009
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

import gutils
import movie
import string
import re

plugin_name         = "Kino.de"
plugin_description  = "KINO.DE"
plugin_url          = "www.kino.de"
plugin_language     = _("German")
plugin_author       = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version      = "1.14"

class Plugin(movie.Movie):
    url_to_use_base = 'http://www.kino.de/'
    url_to_use      = url_to_use_base + 'kinofilm/'
    url_type        = 'K'

    def __init__(self, id):
        self.encode='iso-8859-1'
        elements = string.split(id, "_")
        self.movie_id = elements[1]
        if (elements[0] == "V"):
            self.url_to_use_base = 'http://www.video.de/'
            self.url_to_use      = self.url_to_use_base + 'videofilm/'
            self.url_type        = 'V'
        else:
            self.url_to_use_base = 'http://www.kino.de/'
            self.url_to_use      = self.url_to_use_base + 'kinofilm/'
            self.url_type        = 'K'
        self.url = self.url_to_use + str(self.movie_id)

    def initialize(self):
        if self.url_type == 'K':
            url = self.url_to_use + string.replace(str(self.movie_id), '/', '/credits/')
            self.creditspage = self.open_page(self.parent_window, url=url)
        else:
            self.creditspage = ''

    def get_image(self):
        self.image_url = ''
        tmpdata = gutils.regextrim(self.page, '<div class="cover-area">', '</div>')
        if tmpdata:
            # video page
            tmpdata = re.search('(http[:][/][/][^/]+[/]flbilder[/][^"]+)', tmpdata)
            if tmpdata:
                self.image_url = tmpdata.group(1)
        else:
            # kino page
            tmpdata = gutils.before(self.page, '<span style="line-height: 15px;">')
            if tmpdata:
                tmpparts = re.split('http://images.kino.de/s/', tmpdata)
                if len(tmpparts) > 2:
                    self.image_url = 'http://images.kino.de/s/' + gutils.before(tmpparts[2], '"')
                elif len(tmpparts) > 1:
                    self.image_url = 'http://images.kino.de/s/' + gutils.before(tmpparts[1], '"')

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, '<p>Originaltitel: ', '</p>')
        if not self.o_title:
            self.o_title = gutils.trim(self.page, '<span class="standardsmall">(', ')')
            if not self.o_title:
                self.o_title = gutils.trim(self.page, '<div class="teaser">', '</')
                if not self.o_title:
                    self.o_title = gutils.regextrim(self.page, '<title>', '([|]|</title>)')

    def get_title(self):
        self.title = gutils.trim(self.page, '<div class="teaser">', '</')
        if not self.title:
            self.title = gutils.regextrim(self.page, '<title>', '([|]|</title>)')

    def get_director(self):
        self.director = gutils.trim(self.page, '<th>Regie:', '<th>')
        if not self.director:
            self.director = gutils.trim(self.creditspage, 'Regie&nbsp;', '</tr>')

    def get_plot(self):
        self.plot = gutils.trim(self.page, '<div class="yui-content">', '<div class="footer">')
        if self.plot:
            # video page
            self.plot = re.sub('<script type="text/javascript">[^<]+</script>', '', self.plot)
            self.plot = string.replace(self.plot, '>Großansicht</a>', '>')
            self.plot = string.replace(self.plot, '>Schließen</a>', '>')
            self.plot = string.replace(self.plot, '>zur&uuml;ck </a>', '>')
            self.plot = string.replace(self.plot, '>1</a>', '>')
            self.plot = string.replace(self.plot, '> weiter</a>', '>')
            self.plot = string.replace(self.plot, '</h4>', '\n')
            self.plot = gutils.clean(self.plot)
            compiledmultiline = re.compile(r'^[^(]+[(]Foto[:][^)]+[)][ ]*$', re.MULTILINE)
            self.plot = compiledmultiline.sub('', self.plot)
            compiledmultiline = re.compile(r"(^\s+$|^\s*//\s*$)", re.MULTILINE)
            self.plot = compiledmultiline.sub('', self.plot)
            compiledmultiline = re.compile("^[\n]+$", re.MULTILINE)
            self.plot = compiledmultiline.sub("\n", self.plot)
        else:
            # kino page
            self.plot = gutils.trim(self.page, '<span style="line-height: 15px;">', '<table')

    def get_year(self):
        self.year = ''
        tmp = gutils.trim(self.page, '<div class="description">', '</div>')
        if tmp:
            searchyearandcountry = re.search('([0-9]{4})<br', tmp)
            if searchyearandcountry:
                self.year = searchyearandcountry.group(1)
        if not self.year:
            tmp = gutils.trim(self.page, '<span class="standardsmall"><strong>', '<br')
            if tmp:
                tmp = gutils.trim(tmp, '<strong>', '</strong>')
                if tmp:
                    srchyear = re.search('([0-9]{4})', tmp)
                    if srchyear:
                        self.year = srchyear.group(1)

    def get_runtime(self):
        self.runtime = ''
        srchresult = re.search('Laufzeit: ([0-9]+)[ \t]Min[.]<', self.page)
        if srchresult <> None:
            self.runtime = srchresult.group(1)
        if not self.runtime:
            srchresult = re.search('>([0-9]+)[ \t]Min[.]<', self.page)
            if srchresult <> None:
                self.runtime = srchresult.group(1)

    def get_genre(self):
        self.genre = gutils.trim(self.page,'<p class="genre">', '</p>')
        if not self.genre:
            self.genre = gutils.trim(self.page, '<span class="standardsmall"><strong>', '</strong>')

    def get_cast(self):
        self.cast = ''
        tmp = gutils.trim(self.page, '<th>Darsteller:', '</table>')
        if tmp:
            tmpparts = string.split(tmp, '<a href="/star/')
            for tmppart in tmpparts[1:]:
                name = gutils.trim(tmppart, '>', '<')
                role = gutils.trim(tmppart, '>als ', '<')
                if name:
                    if role:
                        self.cast = self.cast + name + _(' as ') + role + '\n'
                    else:
                        self.cast = self.cast + name + '\n'
        if not self.cast:
            tmp = gutils.trim(self.creditspage, '>Cast<br />', '>Crew<')
            if tmp:
                castparts = re.split('width="50%"><a href="/star/', tmp)
                for index in range(1, len(castparts), 1):
                    role = gutils.clean(gutils.trim(castparts[index - 1], 'width="50%">', '</td>'))
                    name = gutils.clean(gutils.trim(castparts[index], '">', '<'))
                    if role:
                        self.cast = self.cast + name + _(' as ') + role + '\n'
                    else:
                        self.cast = self.cast + name + '\n'

    def get_classification(self):
        self.classification = gutils.regextrim(self.page,'FSK: ', '<')

    def get_studio(self):
        self.studio = ''
        tmp = gutils.trim(self.page, '<div class="description">', '</div>')
        if tmp:
            tmp = gutils.trim(tmp, 'Regie:', '</p>')
            if tmp:
                self.studio = gutils.after(tmp, '<br/>')
        if not self.studio:
            self.studio = gutils.trim(self.page, 'Verleih: ', '<')

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = self.url_to_use + self.movie_id

    def get_trailer(self):
        self.trailer = ''
        trailerparts = re.split('href="/trailer-und-bilder/film', self.page)
        if len(trailerparts) > 1:
            for trailerpart in trailerparts[1:]:
                trailermatch = re.search('Trailer[ ]*</p>', trailerpart)
                if trailermatch:
                    self.trailer = self.url_to_use_base + 'trailer-und-bilder/film' + gutils.before(trailerpart, '"')
                    break
        if not self.trailer and self.url_type == 'K':
            self.trailer = self.url_to_use + string.replace(str(self.movie_id), '/', '/trailer/')

    def get_country(self):
        self.country = ''
        tmp = gutils.trim(self.page, '<div class="description">', '</div>')
        if tmp:
            searchyearandcountry = re.search('([^>0-9]+)[0-9]{4}<br', tmp)
            if searchyearandcountry:
                self.country = searchyearandcountry.group(1)
        if not self.country:
            tmp = gutils.trim(self.page, '<span class="standardsmall"><strong>', '<br')
            if tmp:
                tmp = gutils.trim(tmp, '<strong>', '</strong>')
                if tmp:
                    self.country = gutils.before(tmp, ' ')

    def get_rating(self):
        self.rating = 0
        tmp = gutils.trim(self.page, '<h4>Filmbewertung</h4>', '</script>')
        if tmp:
            matched = re.search('ratingBar.setValue[(]([0-9]+)[)]', tmp)
            if matched:
                try:
                    self.rating = round(int(matched.group(1)) / 10.0, 0)
                except:
                    pass

    def get_notes(self):
        self.notes = ""
        tmp_notes = gutils.clean(gutils.trim(self.page, "<strong>Sprachen:</strong>", "</p>"))
        if tmp_notes != "":
            self.notes = self.notes + "Sprachen:\n" + tmp_notes + "\n\n"
        tmp_notes = gutils.clean(gutils.trim(self.page, "<strong>Untertitel:</strong>", "</p>"))
        if tmp_notes != "":
            self.notes = self.notes + "Untertitel:\n" + tmp_notes + "\n\n"
        tmp_notes = gutils.clean(gutils.trim(self.page, "<strong>Tonformat:</strong>", "</p>"))
        if tmp_notes != "":
            self.notes = self.notes + "Tonformat:\n" + tmp_notes + "\n\n"
        tmp_notes = gutils.clean(gutils.trim(self.page, "<strong>Bildformat:</strong>", "</p>"))
        if tmp_notes != "":
            self.notes = self.notes + "Bildformat:\n" + tmp_notes + "\n\n"
        tmp_notes = gutils.clean(gutils.trim(self.page, "<strong>EAN</strong>", "</p>"))
        if tmp_notes != "":
            self.notes = self.notes + "EAN:\n" + tmp_notes + "\n\n"

    def get_screenplay(self):
        self.screenplay = gutils.regextrim(self.page, '<th>Buch:', '<th>')
        if not self.screenplay:
            self.screenplay= gutils.trim(self.creditspage, 'Drehbuch&nbsp;', '</tr>')

    def get_cameraman(self):
        self.cameraman = gutils.regextrim(self.page, '<th>Kamera:', '<th>')
        if not self.cameraman:
            self.cameraman= gutils.trim(self.creditspage, 'Kamera&nbsp;', '</tr>')

class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search   = 'http://www.kino.de/search.php?mode=megaSearch&searchCategory=film&inputSearch='
        self.translated_url_search = 'http://www.kino.de/search.php?mode=megaSearch&searchCategory=film&inputSearch='
        self.encode='iso-8859-1'
        self.remove_accents = False

    def search(self,parent_window):
        self.open_search(parent_window)
        pagemovie = self.page
        #
        # try to get all result pages (not so nice, but it works)
        #
        pagecount = gutils.clean(gutils.trim(pagemovie, '>von', '</a>'))
        try:
            pagecountint = int(pagecount)
        except:
            pagecountint = 1
        pagecountintcurrent = 1
        while (pagecountint > pagecountintcurrent and pagecountintcurrent < 5):
            pagecountintcurrent = pagecountintcurrent + 1
            self.url = 'http://www.kino.de/search.php?mode=megaSearch&searchCategory=film&page=' + str(pagecountintcurrent) + "&inputSearch="
            self.open_search(parent_window)
            pagemovie = pagemovie + self.page
        #
        # Look for DVD and VHS
        #
        self.url = "http://www.kino.de/search.php?mode=megaSearch&searchCategory=video&inputSearch="
        self.open_search(parent_window)
        pagevideo = pagemovie + self.page
        #
        # try to get all result pages (not so nice, but it works)
        #
        pagecount = gutils.clean(gutils.trim(self.page, '>von', '</a>'))
        try:
            pagecountint = int(pagecount)
        except:
            pagecountint = 1
        pagecountintcurrent = 1
        while (pagecountint > pagecountintcurrent and pagecountintcurrent < 5):
            pagecountintcurrent = pagecountintcurrent + 1
            self.url = "http://www.kino.de/search.php?mode=megaSearch&searchCategory=video&page=" + str(pagecountintcurrent) + "&inputSearch="
            self.open_search(parent_window)
            pagevideo = pagevideo + self.page

        self.page = pagevideo
        return self.page

    def get_searches(self):
        elements1 = re.split('headline3"[^>]*>[ \t\r\n]*<a href="(?:http://www.kino.de)*/kinofilm/', self.page)
        elements1[0] = None
        for element in elements1:
            if element <> None:
                self.ids.append("K_" + re.sub('[?].*', '', gutils.before(element,'"')))
                self.titles.append('Kino: ' + string.replace(string.replace(
                    gutils.strip_tags(
                        gutils.trim(element,'>','</a>') + ' (' +
                        string.replace(
                            gutils.trim(element, '<span class="standardsmall">', "</span>"),
                            '<br />', ' - ')
                        + ')'
                    ),
                    '( - (', '('), '))', ')')
                )

        elements2 = re.split('headline3"[^>]*>[ \t\r\n]*<a href="(?:http://www.video.de)*/videofilm/', self.page)
        elements2[0] = None
        for element in elements2:
            if element <> None:
                self.ids.append("V_" + re.sub('[?].*', '', gutils.before(element,'"')))
                self.titles.append('Video: ' + string.replace(string.replace(
                    gutils.strip_tags(
                        gutils.trim(element,'>','</a>') + ' (' +
                        string.replace(
                            gutils.trim(element, '<span class="standardsmall">', '</span>'),
                            '<br />', ' - ')
                        + ')'
                    ),
                    '( - (', '('), '))', ')')
                )

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Rocky Balboa'         : [ 8, 8 ],
        'Arahan'               : [ 6, 6 ],
        'Ein glückliches Jahr' : [ 4, 4 ]
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
        'K_rocky-balboa/96132.html' : { 
            'title'               : 'Rocky Balboa',
            'o_title'             : 'Rocky Balboa',
            'director'            : 'Sylvester Stallone',
            'plot'                : True,
            'cast'                : 'Sylvester Stallone' + _(' as ') + 'Rocky Balboa\n\
Antonio Traver' + _(' as ') + 'Mason "The Line" Dixon\n\
Burt Young' + _(' as ') + 'Paulie\n\
Geraldine Hughes' + _(' as ') + 'Marie\n\
Milo Ventimiglia' + _(' as ') + 'Rocky Jr.\n\
James Francis Kelly III' + _(' as ') + 'Steps\n\
Tony Burton' + _(' as ') + 'Duke\n\
A.J. Benza' + _(' as ') + 'L.C.',
            'country'             : 'USA',
            'genre'               : 'Drama',
            'classification'      : 'Freigegeben ab 12 Jahren',
            'studio'              : 'Fox',
            'o_site'              : False,
            'site'                : 'http://www.kino.de/kinofilm/rocky-balboa/96132.html',
            'trailer'             : 'http://www.kino.de/kinofilm/rocky-balboa/trailer/96132.html',
            'year'                : 2006,
            'notes'               : False,
            'runtime'             : 102,
            'image'               : True,
            'rating'              : False,
            'cameraman'           : 'J. Clark Mathis',
            'screenplay'          : 'Sylvester Stallone'
        },
        'K_ein-glueckliches-jahr/28675.html' : { 
            'title'               : 'Ein glückliches Jahr',
            'o_title'             : 'La bonne année',
            'director'            : 'Claude Lelouch',
            'plot'                : False,
            'cast'                : 'Lino Ventura\n\
Françoise Fabian\n\
Charles Gérard\n\
André Falcon',
            'country'             : 'Frankreich/Italien',
            'genre'               : 'Drama',
            'classification'      : 'Freigegeben ab 12 Jahren',
            'studio'              : 'Columbia TriStar',
            'o_site'              : False,
            'site'                : 'http://www.kino.de/kinofilm/ein-glueckliches-jahr/28675.html',
            'trailer'             : 'http://www.kino.de/kinofilm/ein-glueckliches-jahr/trailer/28675.html',
            'year'                : 1973,
            'notes'               : False,
            'runtime'             : 115,
            'image'               : False,
            'rating'              : False,
            'cameraman'           : 'Jean Collomb',
            'screenplay'          : 'Claude Lelouch'
        },
        'V_ein-glueckliches-jahr-dvd/85546.html' : { 
            'title'               : 'Ein glückliches Jahr',
            'o_title'             : 'La bonne année',
            'director'            : 'Claude Lelouch',
            'plot'                : True,
            'cast'                : 'Lino Ventura\n\
Françoise Fabian\n\
Charles Gérard\n\
André Falcon',
            'country'             : 'Frankreich/Italien',
            'genre'               : 'Drama',
            'classification'      : 'ab 12 Jahren',
            'studio'              : 'Warner Home Video',
            'o_site'              : False,
            'site'                : 'http://www.video.de/videofilm/ein-glueckliches-jahr-dvd/85546.html',
            'trailer'             : False,
            'year'                : 1973,
            'notes'               : 'Sprachen:\n\
Deutsch DD 2.0, Französisch DD 2.0\n\
\n\
Tonformat:\n\
Dolby Digital 2.0\n\
\n\
Bildformat:\n\
1:1,33/4:3',
            'runtime'             : 110,
            'image'               : True,
            'rating'              : False,
            'cameraman'           : 'Jean Collomb',
            'screenplay'          : 'Claude Lelouch'
        },
        'V_arahan-vanilla-dvd/90405.html' : { 
            'title'               : 'Arahan',
            'o_title'             : 'Arahan jangpung dae jakjeon',
            'director'            : 'Ryoo Seung-wan',
            'plot'                : True,
            'cast'                : 'Ryu Seung-beom' + _(' as ') + 'Sang-hwan\n\
Yoon So-yi' + _(' as ') + 'Wi-jin\n\
Ahn Sung-kee' + _(' as ') + 'Ja-woon\n\
Jung Doo-hong' + _(' as ') + 'Heuk-woon\n\
Yun Ju-sang' + _(' as ') + 'Mu-woon',
            'country'             : 'Südkorea',
            'genre'               : 'Action/ Komödie',
            'classification'      : 'ab 16 Jahren',
            'studio'              : 'WVG Medien',
            'o_site'              : False,
            'site'                : 'http://www.video.de/videofilm/arahan-vanilla-dvd/90405.html',
            'trailer'             : False,
            'year'                : 2004,
            'notes'               : 'Sprachen:\n\
Deutsch DD 5.1\n\
\n\
Tonformat:\n\
Dolby Digital 5.1\n\
\n\
Bildformat:\n\
1:1,78/16:9',
            'runtime'             : 108,
            'image'               : True,
            'rating'              : False,
            'cameraman'           : 'Lee Jun-gyu',
            'screenplay'          : 'Ryoo Seung-wan'
        }
    }
