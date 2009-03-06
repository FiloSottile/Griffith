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

plugin_name = "Kino.de"
plugin_description = "KINO.DE"
plugin_url = "www.kino.de"
plugin_language = _("German")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.13"

class Plugin(movie.Movie):
    url_to_use = "http://www.kino.de/kinofilm/"
    url_type = "K"

    def __init__(self, id):
        self.encode='iso-8859-1'
        elements = string.split(id, "_")
        self.movie_id = elements[1]
        if (elements[0] == "V"):
            self.url_to_use = "http://www.kino.de/videofilm/"
            self.url_type = "V"
        else:
            self.url_to_use = "http://www.kino.de/kinofilm/"
            self.url_type = "K"
        self.url = self.url_to_use + str(self.movie_id)

    def initialize(self):
        self.tmp_page = gutils.before(self.page, '<!-- PRINT-CONTENT-ENDE-->')
        self.url = self.url_to_use + string.replace(str(self.movie_id), '/', '/credits/')
        self.open_page(self.parent_window)
        self.tmp_creditspage = gutils.before(self.page, '<!-- PRINT-CONTENT-ENDE-->')
        self.url = self.url_to_use + string.replace(str(self.movie_id), "/", "/features/")
        self.open_page(self.parent_window)
        self.tmp_dvdfeaturespage = gutils.before(self.page, '<!-- PRINT-CONTENT-ENDE-->')

    def get_image(self):
        self.image_url = ''
        tmpdata = gutils.regextrim(self.tmp_page, '(PRINT[-]CONTENT[-]START|<td class="content">)', '(Dieser Film wurde |>FOTOSHOW<|>KRITIK<)')
        tmpdatasplit = re.split('src="http://.+/flbilder', tmpdata)
        if len(tmpdatasplit) > 2:
            tmpdata = gutils.before(tmpdatasplit[2], '.jpg')
            if tmpdata <> '':
                self.image_url = 'http://images.kino.de/flbilder' + tmpdata + '.jpg'
        elif len(tmpdatasplit) > 1:
            tmpdata = gutils.before(tmpdatasplit[1], '.jpg')
            if tmpdata <> '':
                self.image_url = 'http://images.kino.de/flbilder' + tmpdata + '.jpg'

    def get_o_title(self):
        self.o_title = gutils.trim(self.tmp_page, 'span class="standardsmall">(', ')<')
        if self.o_title == '':
            if self.url_type == 'V':
                self.o_title = gutils.after(gutils.regextrim(self.tmp_page, 'headline2"[^>]*>[ \t\r\n]*<a href="/videofilm', '</a>'), '>')
            else:
                self.o_title = gutils.after(gutils.regextrim(self.tmp_page, 'headline2"[^>]*>[ \t\r\n]*<a href="/kinofilm', '</a>'), '>')

    def get_title(self):
        if self.url_type == "V":
            self.title = gutils.after(gutils.regextrim(self.tmp_page, 'headline2"[^>]*>[ \t\r\n]*<a href="/videofilm', '</a>'), '>')
        else:
            self.title = gutils.after(gutils.regextrim(self.tmp_page, 'headline2"[^>]*>[ \t\r\n]*<a href="/kinofilm', '</a>'), '>')

    def get_director(self):
        self.director = gutils.regextrim(self.tmp_creditspage, '>[ ]*Regie', '</a>')
        self.director = gutils.after(self.director, '/star/')
        self.director = gutils.after(self.director, '>')

    def get_plot(self):
        # little steps to perfect plot (I hope ... it's a terrible structured content ... )
        self.plot = gutils.before(self.tmp_page, '<!-- PRINT-CONTENT-ENDE-->')
        self.plot = gutils.regextrim(self.plot, 'Kurzinfo', '</td></tr>[ \t\r\n]*<tr><td></td></tr>')
        if self.plot != '':
            lastpos = self.plot.rfind('</table>')
            if lastpos == -1:
                self.plot = ''
            else:
                self.plot = self.plot[lastpos:]
        else:
            self.plot = gutils.trim(self.tmp_page, '<span style="line-height:', '</spa')
            if self.plot == '':
                self.plot = gutils.trim(self.tmp_page,"Kurzinfo", "</td></tr><tr><td></td>")
                if (self.plot == ''):
                    self.plot = gutils.trim(self.tmp_page,"Kurzinfo", '<script ')
                    self.plot = gutils.after(self.plot, '>')
                while len(self.plot) and string.find(self.plot, '</A>') > -1:
                    self.plot = gutils.after(self.plot, '</A>');
                self.plot = gutils.after(gutils.after(self.plot, '</table>'), '>')
            else:
                self.plot = gutils.after(self.plot, '>')

    def get_year(self):
        self.year = ''
        tmp = gutils.regextrim(self.tmp_page, 'span class="standardsmall"[^>]*><strong>', '</span>')
        if tmp <> None:
            srchresult = re.search('[0-9][0-9][0-9][0-9]</strong>', tmp)
            if srchresult <> None:
                self.year = srchresult.string[srchresult.start():srchresult.end()]

    def get_runtime(self):
        self.runtime = ''
        srchresult = re.search('>[0-9]+[ \t]Min[.]<', self.tmp_page)
        if srchresult <> None:
            self.runtime = gutils.regextrim(srchresult.string[srchresult.start():srchresult.end()], '>', '[^0-9]')

    def get_genre(self):
        self.genre = gutils.regextrim(self.tmp_page,'span class="standardsmall"[^>]*>[ \t\r\n]*<strong>((DVD|VHS|Laser Disc|Video CD|Blue-ray Disc)</strong>[ \t]-[ \t]<strong>)*', '</strong>[ \t]-[ \t]<strong>')

    def get_cast(self):
        self.cast = gutils.trim(self.tmp_creditspage,'>Cast<', '</table><br')
        if len(self.cast):
            if self.cast.find('>mehr<') > 0:
                self.cast = gutils.after(self.cast, '>mehr<')
            self.cast = gutils.after(self.cast, '>')
            self.cast = re.sub('<tr[ ]+class="(dbtrefferlight|dbtrefferdark)">', "\n", self.cast)
            self.cast = self.cast.replace('&nbsp;', '--flip--')
            self.cast = gutils.clean(self.cast)
            self.cast = re.sub("[\t]+", '', self.cast)
            self.cast = re.sub("[\n]+", "\n", self.cast)
            self.cast = re.sub("--flip--[\n]+", '--flip--', self.cast)
            elements = self.cast.split("\n")
            self.cast = ''
            for element in elements:
                elements2 = element.split('--flip--')
                if len(elements2) > 1:
                    if elements2[0] <> '':
                        self.cast += elements2[1] + '--flip--' + elements2[0] + "\n"
                    else:
                        self.cast += elements2[1] + "\n"
                else:
                    self.cast += element + "\n"
            self.cast = string.replace(self.cast, '--flip--', _(' as '))

    def get_classification(self):
        self.classification = gutils.regextrim(self.tmp_page,'FSK:( |&nbsp;)+', '</strong>')

    def get_studio(self):
        self.studio = gutils.regextrim(self.tmp_page, '>[ ]*Verleih:( |&nbsp;)+', '( - |&nbsp;-&nbsp;)*</strong>')
        if (self.studio == ""):
            self.studio = gutils.regextrim(self.tmp_page, '>[ ]*Anbieter:( |&nbsp;)+', '( - |&nbsp;-&nbsp;)*</strong>')

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = self.url_to_use + self.movie_id;

    def get_trailer(self):
        self.trailer = ""

    def get_country(self):
        self.country = gutils.regextrim(self.tmp_page, 'span class="standardsmall"[^>]*><strong>((DVD|VHS|Laser Disc|Video CD|Blue-ray Disc)</strong>[ \t]-[ \t]<strong>)*', '</span>')
        if self.country <> None:
            self.country = gutils.regextrim(self.country, '-[ \t]<strong>', '</strong>')
            self.country = re.sub('[0-9]+$', '', self.country)
        else:
            self.country = ''

    def get_rating(self):
        self.rating = "0"

    def get_notes(self):
        self.notes = ""
        tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_dvdfeaturespage, "<b>Sprache</b>", "</td></tr>")), "&nbsp;", "")
        if tmp_notes != "":
            self.notes = self.notes + "Sprachen:\n" + tmp_notes + "\n\n"
        tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_dvdfeaturespage, "<b>Untertitel</b>", "</td></tr>")), "&nbsp;", "")
        if tmp_notes != "":
            self.notes = self.notes + "Untertitel:\n" + tmp_notes + "\n\n"
        tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_dvdfeaturespage, "<b>Mehrkanalton</b>", "</td></tr>")), "&nbsp;", "")
        if tmp_notes != "":
            self.notes = self.notes + "Mehrkanalton:\n" + tmp_notes + "\n\n"
        tmp_notes = string.replace(gutils.strip_tags(gutils.trim(self.tmp_dvdfeaturespage, "<b>EAN</b>", "</td></tr>")), "&nbsp;", "")
        if tmp_notes != "":
            self.notes = self.notes + "EAN:\n" + tmp_notes + "\n\n"

class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search   = 'http://www.kino.de/search.php?mode=megaSearch&searchCategory=film&inputSearch='
        self.translated_url_search = 'http://www.kino.de/search.php?mode=megaSearch&searchCategory=film&inputSearch='
        self.encode='iso-8859-1'
        self.remove_accents = False

    def search(self,parent_window):
        self.open_search(parent_window)
        tmp_pagemovie = self.page
        #
        # try to get all result pages (not so nice, but it works)
        #
        tmp_pagecount = gutils.clean(gutils.trim(tmp_pagemovie, '>von', '</a>'))
        try:
            tmp_pagecountint = int(tmp_pagecount)
        except:
            tmp_pagecountint = 1
        tmp_pagecountintcurrent = 1
        while (tmp_pagecountint > tmp_pagecountintcurrent and tmp_pagecountintcurrent < 5):
            tmp_pagecountintcurrent = tmp_pagecountintcurrent + 1
            self.url = 'http://www.kino.de/search.php?mode=megaSearch&searchCategory=film&page=' + str(tmp_pagecountintcurrent) + "&inputSearch="
            self.open_search(parent_window)
            tmp_pagemovie = tmp_pagemovie + self.page
        #
        # Look for DVD and VHS
        #
        self.url = "http://www.kino.de/search.php?mode=megaSearch&searchCategory=video&inputSearch="
        self.open_search(parent_window)
        tmp_pagevideo = tmp_pagemovie + self.page
        #
        # try to get all result pages (not so nice, but it works)
        #
        tmp_pagecount = gutils.clean(gutils.trim(self.page, '>von', '</a>'))
        try:
            tmp_pagecountint = int(tmp_pagecount)
        except:
            tmp_pagecountint = 1
        tmp_pagecountintcurrent = 1
        while (tmp_pagecountint > tmp_pagecountintcurrent and tmp_pagecountintcurrent < 5):
            tmp_pagecountintcurrent = tmp_pagecountintcurrent + 1
            self.url = "http://www.kino.de/search.php?mode=megaSearch&searchCategory=video&page=" + str(tmp_pagecountintcurrent) + "&inputSearch="
            self.open_search(parent_window)
            tmp_pagevideo = tmp_pagevideo + self.page

        self.page = tmp_pagevideo
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
        'Rocky Balboa'          : [ 7, 7 ],
        'Arahan'                : [ 6, 6 ],
        'Ein glückliches Jahr' : [ 3, 3 ]
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
            'trailer'             : False,
            'year'                : 2006,
            'notes'               : False,
            'runtime'             : 102,
            'image'               : True,
            'rating'              : False
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
            'trailer'             : False,
            'year'                : 1973,
            'notes'               : False,
            'runtime'             : 115,
            'image'               : False,
            'rating'              : False
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
            'classification'      : 'Freigegeben ab 12 Jahren',
            'studio'              : 'Black Hill Pictures',
            'o_site'              : False,
            'site'                : 'http://www.kino.de/videofilm/ein-glueckliches-jahr-dvd/85546.html',
            'trailer'             : False,
            'year'                : 1973,
            'notes'               : 'Sprachen:\n\
Deutsch DD 2.0, Französisch DD 2.0\n\
\n\
Mehrkanalton:\n\
Dolby Digital 2.0\n\
\n\
EAN:\n\
7321921998843',
            'runtime'             : 110,
            'image'               : True,
            'rating'              : False
        },
        'V_arahan-vanilla-dvd/90405.html' : { 
            'title'               : 'Arahan (Vanilla-DVD)',
            'o_title'             : 'Arahan jangpung dae jakjeon',
            'director'            : 'Ryoo Seung-wan',
            'plot'                : True,
            'cast'                : 'Ryu Seung-beom' + _(' as ') + 'Sang-hwan\n\
Yoon So-yi' + _(' as ') + 'Wi-jin\n\
Ahn Sung-kee' + _(' as ') + 'Ja-woon\n\
Jung Doo-hong' + _(' as ') + 'Heuk-woon\n\
Yun Ju-sang' + _(' as ') + 'Mu-woon',
            'country'             : 'Südkorea',
            'genre'               : 'Action/Komödie',
            'classification'      : 'Freigegeben ab 16 Jahren',
            'studio'              : 'Splendid',
            'o_site'              : False,
            'site'                : 'http://www.kino.de/videofilm/arahan-vanilla-dvd/90405.html',
            'trailer'             : False,
            'year'                : 2004,
            'notes'               : 'Sprachen:\n\
Deutsch DD 5.1\n\
\n\
Mehrkanalton:\n\
Dolby Digital 5.1\n\
\n\
EAN:\n\
4013549871105',
            'runtime'             : 108,
            'image'               : True,
            'rating'              : False
        }
    }
