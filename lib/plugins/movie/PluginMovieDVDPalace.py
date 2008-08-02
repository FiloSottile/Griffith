# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2007
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
import gutils
import movie
import string
import re

plugin_name = "DVD-Palace"
plugin_description = "DVD-Onlinemagazin mit DVD-Datenbank"
plugin_url = "www.dvd-palace.de"
plugin_language = _("German")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.0"

class Plugin(movie.Movie):

    def __init__(self, id):
        self.encode   = 'iso-8859-1'
        self.movie_id = id
        self.url      = 'http://www.dvd-palace.de/dvd-datenbank/' + self.movie_id

    def get_image(self):
        self.image_url = gutils.trim(self.page, 'src="/showcover.php?', '"')
        if self.image_url <> '':
            self.image_url = 'http://www.dvd-palace.de/showcover.php?' + self.image_url

    def get_o_title(self):
        self.o_title = gutils.trim(self.page, 'Originaltitel', '</b>')
        if self.o_title == '':
            self.o_title = gutils.trim(self.page, '<TITLE>', ' - DVD Details')

    def get_title(self):
        self.title = gutils.trim(self.page, '<TITLE>', ' - DVD Details')

    def get_director(self):
        self.director = gutils.trim(self.page, 'Regisseur(e)', '</TR>')

    def get_plot(self):
        self.plot = re.sub(
            '[0-9 ]+Views', '',
            re.sub(
                '[]', '-',
                re.sub(
                    '[\x93]', '"', self.regextrim(self.page, 'showcover.php[^>]*>', '</td>'))))

    def get_year(self):
        self.year = gutils.after(gutils.trim(gutils.trim(self.page, 'Originaltitel', '</TR>'), '(', ')'), ' ')

    def get_runtime(self):
        self.runtime = gutils.strip_tags(string.replace(gutils.trim(self.page, 'Laufzeit', ' min'), 'ca. ', ''))

    def get_genre(self):
        self.genre = string.replace(string.replace(gutils.trim(self.page, 'Genre(s)', '</TR>'), '&nbsp;', ''), '<br>', ', ')

    def get_cast(self):
        self.cast = string.replace(
            re.sub('<em>[^<]*</em>', ' ',
                re.sub(',[ ]*', '\n',
                    gutils.trim(self.page, 'Darsteller / Sprecher', '</TR>')
                )
            ),
            '\n ', '\n')

    def get_classification(self):
        self.classification = string.replace(gutils.trim(self.page, 'Altersfreigabe (FSK)', '</TR>'), '&nbsp;', '')

    def get_studio(self):
        self.studio = string.replace(string.replace(gutils.trim(self.page, 'Label', '</td>'), '&nbsp;', ''), ':', '')

    def get_o_site(self):
        self.o_site = ""

    def get_site(self):
        self.site = self.url

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = gutils.before(gutils.trim(gutils.trim(self.page, 'Originaltitel', '</TR>'), '(', ')'), ' ')

    def get_rating(self):
        self.rating = "0"

    def get_notes(self):
        self.notes = ""
        tmp_notes = re.sub('^[ \t]+', '',
            gutils.strip_tags(
            re.sub('(<br>|<br />)', '\r\n',
            re.sub('[\r\n]+', '',
            re.sub('[ \t][ \t\r\n]+', ' ',
            gutils.trim(self.page, 'Bildformat(e)', '</TR>')))))
        )
        if (tmp_notes != ""):
            self.notes = self.notes + "Bildformat(e):\n" + tmp_notes + "\n"
        tmp_notes = re.sub('^[ \t]+', '',
            gutils.strip_tags(
            re.sub('(<br>|<br />)', '\r\n',
            re.sub('[\r\n]+', '',
            re.sub('[ \t][ \t\r\n]+', ' ',
            gutils.trim(self.page, 'Tonformat(e)', '</TR>')))))
        )
        if (tmp_notes != ""):
            self.notes = self.notes + "Tonformat(e):\n" + tmp_notes + "\n\n"
        tmp_notes = re.sub('^[ \t]+', '',
            gutils.strip_tags(
            re.sub('(<br>|<br />)', '\r\n',
            re.sub('[\r\n]+', '',
            re.sub('[ \t][ \t\r\n]+', ' ',
            gutils.trim(self.page, 'Untertitel', '</TR>')))))
        )
        if (tmp_notes != ""):
            self.notes = self.notes + "Untertitel:" + tmp_notes + "\n\n"
            
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
            p2 = p1 + obj.end()
        return text[p1:p2]

class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search   = "http://www.dvd-palace.de/dvddatabase/dbsearch.php?action=1&suchbegriff="
        self.translated_url_search = "http://www.dvd-palace.de/dvddatabase/dbsearch.php?action=1&suchbegriff="
        self.encode='iso-8859-1'

    def search(self,parent_window):
        self.open_search(parent_window)
        tmp_pagemovie = self.page
        #
        # try to get all result pages (not so nice, but it works)
        #
        tmp_pagecount = gutils.trim(tmp_pagemovie, 'Seiten (<b>', '</b>)')
        try:
            tmp_pagecountint = int(tmp_pagecount)
        except:
            tmp_pagecountint = 1
        tmp_pagecountintcurrent = 1
        while (tmp_pagecountint > tmp_pagecountintcurrent and tmp_pagecountintcurrent < 5):
            self.url = "http://www.dvd-palace.de/dvddatabase/dbsearch.php?action=1&start=" + str(tmp_pagecountintcurrent * 20) + "&suchbegriff="
            self.open_search(parent_window)
            tmp_pagemovie = tmp_pagemovie + self.page
            tmp_pagecountintcurrent = tmp_pagecountintcurrent + 1
        self.page = tmp_pagemovie
        return self.page

    def get_searches(self):
        elements1 = re.split('&nbsp;<a title="[^"]+" href="/dvd-datenbank/', self.page)
        elements1[0] = None
        for element in elements1:
            if element <> None:
                self.ids.append(gutils.before(element,'"'))
                self.titles.append(
                    gutils.trim(element, '>', '</a>') +
                    gutils.strip_tags(
                        ' (' +
                        re.sub('[ \t\n][ \t\n]+', ' ',
                        string.replace(
                        string.replace(
                            self.regextrim(element, '<div [^>]*>', '</div>'),
                            '<br>', ' - '),
                            '&nbsp;', ''))
                        + ')'
                    )
                )
            
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
            p2 = p1 + obj.end()
        return text[p1:p2]
