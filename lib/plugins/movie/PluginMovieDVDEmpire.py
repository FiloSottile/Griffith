# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2007-2009
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
import re

plugin_name         = "DVD Empire"
plugin_description  = "International Retailer of DVD Movies"
plugin_url          = "www.dvdempire.com"
plugin_language     = _("English")
plugin_author       = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version      = "1.1"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode   = 'iso-8859-1'
        self.movie_id = id
        self.url      = "http://www.dvdempire.com/Exec/v4_item.asp?item_id=" + str(self.movie_id)

    def get_image(self):
        tmp_page = gutils.trim(self.page, '<td align="center" valign="top" class="fontsmall">', '</td>')
        self.image_url = gutils.trim(tmp_page, '<img src=\'', '\' ')

    def get_o_title(self):
        self.o_title = gutils.strip_tags(gutils.trim(self.page,'<td class="fontxlarge" valign="top" align="left">', '<nobr>'))

    def get_title(self):
        self.title = gutils.strip_tags(gutils.trim(self.page,'<td class="fontxlarge" valign="top" align="left">', '<nobr>'))

    def get_director(self):
        self.director = gutils.strip_tags(gutils.trim(self.page,">Directors:","</a>"))
        self.director = self.director.replace('&nbsp;', '')
        self.director = self.director.replace('&#149;', '')

    def get_plot(self):
        self.plot = gutils.strip_tags(gutils.trim(self.page, '<td width="100%" valign="top" class="fontsmall3">', '</td>'))
        self.plot = self.plot.replace(u'\x93', '"')
        self.plot = self.plot.replace(u'\x84', '"')

    def get_year(self):
        self.year = gutils.strip_tags(gutils.trim(self.page, '>Production Year:', '<br />'))

    def get_runtime(self):
        self.runtime = gutils.strip_tags(gutils.trim(self.page, '>Length:', '<br />'))

    def get_genre(self):
        self.genre = gutils.strip_tags(gutils.trim(self.page, '>Genre</b>:', '</tr>'))

    def get_cast(self):
        self.cast = gutils.trim(self.page, '>Actors:', '</td><td')
        self.cast = self.cast.replace('<br>', '\n')
        self.cast = self.cast.replace('<br />', '\n')
        self.cast = self.cast.replace('&nbsp;', '')
        self.cast = self.cast.replace('&#8226;', '')
        self.cast = self.cast.replace('&#149;', '')
        self.cast = gutils.strip_tags(self.cast)

    def get_classification(self):
        self.classification = gutils.strip_tags(gutils.trim(self.page, '>Rating:', '<br />'))

    def get_studio(self):
        self.studio = gutils.strip_tags(gutils.trim(self.page, '>Studio:', '<br />'))

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ""

    def get_country(self):
        self.country = ""

    def get_rating(self):
        self.rating = gutils.clean(gutils.trim(self.page, '>Overall Rating:', ' out of'))
        try:
            tmp_float = float(self.rating)
            tmp_float = round(2 * tmp_float, 0)
            self.rating = str(tmp_float)
        except:
            self.rating = '0'

    def get_notes(self):
        self.notes = ''
        tmp_page = gutils.trim(self.page, 'Features:', '<b>')
        tmp_page = tmp_page.replace('<br>', '\n')
        tmp_page = tmp_page.replace('<br />', '\n')
        tmp_page = gutils.strip_tags(tmp_page)
        if tmp_page <> '':
            tmp_page = re.sub('[\r\n]+', '\n', tmp_page)
            self.notes = self.notes + '\nFeatures:' + tmp_page + '\n'
        tmp_page = gutils.trim(self.page, 'Video:', '<b>')
        tmp_page = tmp_page.replace('<br>', '\n')
        tmp_page = tmp_page.replace('<br />', '\n')
        tmp_page = gutils.strip_tags(tmp_page)
        if tmp_page <> '':
            tmp_page = re.sub('[\r\n]+', '\n', tmp_page)
            self.notes = self.notes + '\nVideo:' + tmp_page + '\n'
        tmp_page = gutils.trim(self.page, 'Audio:', '<b>')
        tmp_page = tmp_page.replace('<br>', '\n')
        tmp_page = tmp_page.replace('<br />', '\n')
        tmp_page = tmp_page.replace('(more info)', '\n')
        tmp_page = gutils.strip_tags(tmp_page)
        if tmp_page <> '':
            tmp_page = re.sub('[\r\n]+', '\n', tmp_page)
            self.notes = self.notes + '\nAudio:' + tmp_page
        tmp_page = gutils.trim(self.page, 'Subtitles:', '<b>')
        tmp_page = gutils.strip_tags(tmp_page)
        if tmp_page <> '':
            tmp_page = re.sub('[\r\n]+', '\n', tmp_page)
            self.notes = self.notes + '\nSubtitles:\n' + tmp_page + '\n'

    def get_screenplay(self):
        self.screenplay = gutils.strip_tags(gutils.trim(self.page, '>Writers:', '</a>'))
        self.screenplay = self.screenplay.replace('&nbsp;', '')
        self.screenplay = self.screenplay.replace('&#149;', '')

    def get_barcode(self):
        self.barcode = gutils.trim(self.page, '<b>UPC Code:</b>', '<')

class SearchPlugin(movie.SearchMovie):
    def __init__(self):
        self.original_url_search   = "http://www.dvdempire.com/Exec/v1_search_all.asp?&site_media_id=0&pp=&search_refined=32&used=0&string="
        self.translated_url_search = "http://www.dvdempire.com/Exec/v1_search_all.asp?&site_media_id=0&pp=&search_refined=32&used=0&string="
        self.encode                = 'iso-8859-1'

    def search(self,parent_window):
        if not self.open_search(parent_window):
            return None
        # short the content
        tmp_page = gutils.trim(self.page,'<select name="sort"', 'Click Here to make a Suggestion</a>')
        #
        # try to get all result pages (not so nice, but it works)
        #
        tmp_pagecount = gutils.trim(self.page, '<div id="Search_Container" name="Search_Container">', '</table>')
        tmp_pagecountintuse = 1
        elements = tmp_pagecount.split("&page=")
        for element in elements:
            try:
                tmp_pagecountint = int(gutils.before(element, '\''))
            except:
                tmp_pagecountint = 0
            if tmp_pagecountint > tmp_pagecountintuse:
                tmp_pagecountintuse = tmp_pagecountint
        tmp_pagecountintcurrent = 1
        while tmp_pagecountintuse > tmp_pagecountintcurrent and tmp_pagecountintuse < 4:
            tmp_pagecountintcurrent = tmp_pagecountintcurrent + 1
            self.url = "http://www.dvdempire.com/Exec/v1_search_all.asp?&site_media_id=0&pp=&search_refined=32&used=0&page=" + str(tmp_pagecountintcurrent) + "&string="
            self.open_search(parent_window)
            if self.open_search(parent_window):
                tmp_page2 = gutils.trim(self.page,'<select name="sort"', 'Click Here to make a Suggestion</a>')
                tmp_page = tmp_page + tmp_page2

        self.page = tmp_page
        return self.page

    def get_searches(self):
        split_pattern = re.compile('<a[\t ]+href=["\']/Exec/v4_item[.]asp[?](?:userid=[-0-9]+[&]amp;)*item_id=([0-9]+)\'')
        elements = split_pattern.split(self.page)
        for index in range(1, len(elements), 2):
            title_element = elements[index + 1]
            tmp_title = gutils.strip_tags(gutils.trim(title_element, '>', '</a>'))
            if tmp_title <> '':
                self.ids.append(elements[index])
                type = re.search('<b>Blu-ray</b>', title_element)
                if type:
                    tmp_title = tmp_title + ' (Blu-ray)'
                type = re.search('<b>DVD-Video</b>', title_element)
                if type:
                    tmp_title = tmp_title + ' (DVD)'
                self.titles.append(tmp_title)

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Rocky Balboa' : [ 2, 2 ],
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
        '1300280' : { 
            'title'               : 'Rocky Balboa',
            'o_title'             : 'Rocky Balboa',
            'director'            : 'Sylvester Stallone',
            'plot'                : True,
            'cast'                : 'Sylvester Stallone\n\
Burt Young\n\
Geraldine Hughes\n\
Milo Ventimiglia\n\
Antonio Tarver',
            'country'             : False,
            'genre'               : 'Sports, Boxing, Drama',
            'classification'      : 'PG',
            'studio'              : 'Sony Pictures Home Entertainment',
            'o_site'              : False,
            'site'                : 'http://www.dvdempire.com/Exec/v4_item.asp?item_id=1300280',
            'trailer'             : False,
            'year'                : 2006,
            'notes'               : 'Features:\n\
Deleted Scenes & Alternate Ending\n\
Boxing\'s Bloopers\n\
Skill Vs. Will: The Making of Rocky Balboa\n\
Reality in the Ring: Filming Rocky\'s Final Fight\n\
Virtual Champion: Creating the Computer Fight\n\
Audio Commentary with Sylvester Stallone\n\
\n\
Video:\n\
Widescreen 1.85:1 Color (Anamorphic) \n\
\n\
Audio: \n\
ENGLISH: Dolby Digital 5.1 [CC]\n\
FRENCH: Dolby Digital 5.1\n\
\n\
Subtitles:\n\
English, Spanish, French',
            'runtime'             : 102,
            'image'               : True,
            'rating'              : 9,
            'screenplay'          : 'Sylvester Stallone',
            'barcode'             : '043396161900'
        },
    }
