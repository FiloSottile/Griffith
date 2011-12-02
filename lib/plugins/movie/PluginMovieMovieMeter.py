# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2009
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
import urllib, httplib
from xmlrpclib import ServerProxy, Transport

plugin_name         = 'MovieMeter'
plugin_description  = 'de filmsite voor liefhebbers'
plugin_url          = 'www.moviemeter.nl'
plugin_language     = _('Dutch')
plugin_author       = 'Michael Jahn'
plugin_author_email = 'griffith-private@lists.berlios.de'
plugin_version      = '1.0'
# API key created for Griffith
moviemeter_api_key  = '6h70thfmkwhq55hst69gnr65ckbaqu6h'

#
# XMLRPC through proxy if necessary
#
class ProxiedTransport(Transport):
    proxy_is_used = False

    def make_connection(self, host):
        self.realhost = host
        proxies = urllib.getproxies()
        proxyurl = None
        if 'http' in proxies:
            proxyurl = proxies['http']
        elif 'all' in proxies:
            proxyurl = proxies['all']
        if proxyurl:
            urltype, proxyhost = urllib.splittype(proxyurl)
            host, selector = urllib.splithost(proxyhost)
            h = httplib.HTTP(host)
            self.proxy_is_used = True
            return h
        else:
            self.proxy_is_used = False
            return Transport.make_connection(self, host)

    def send_request(self, connection, handler, request_body):
        if self.proxy_is_used:
            connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))
        else:
            Transport.send_request(self, connection, handler, request_body)

    def send_host(self, connection, host):
        if self.proxy_is_used:
            connection.putheader('Host', self.realhost)
        else:
            Transport.send_host(self, connection, host)

class Plugin(movie.Movie):
    server = ServerProxy('http://www.moviemeter.nl/ws', transport=ProxiedTransport())

    def __init__(self, id):
        self.encode   = 'iso8859-1'
        self.movie_id = id
        # only for user visible url field, fetching is based on the XML RPC API
        self.url      = "http://www.moviemeter.nl/film/%s" % str(self.movie_id)

    def open_page(self, parent_window=None, url=None):
        self.result_array = None
        if parent_window is not None:
            self.parent_window = parent_window
        self.progress.set_data(parent_window, _("Fetching data"), _("Wait a moment"), False)
        self.progress.pulse()
        sessionkey = None
        result = self.server.api.startSession(moviemeter_api_key)
        self.progress.pulse()
        try:
            sessionkey = result['session_key']
            self.result_array = self.server.film.retrieveDetails(sessionkey, int(self.movie_id))
            #self.imdb_result_array = self.server.film.retrieveImdb(sessionkey, int(self.movie_id))
            self.progress.pulse()
        finally:
            if sessionkey:
                self.server.api.closeSession(sessionkey)
            self.progress.pulse()
        return True

    def get_image(self):
        self.image_url = self.result_array['thumbnail']

    def get_o_title(self):
        self.o_title = self.result_array['title']

    def get_title(self):
        self.title = self.result_array['title']

    def get_director(self):
        self.director = ''
        for element in self.result_array['directors']:
            self.director = self.director + element['name'] + ', '
        self.director = re.sub(', $', '', self.director)

    def get_plot(self):
        self.plot = self.result_array['plot']

    def get_year(self):
        self.year = self.result_array['year']

    def get_runtime(self):
        self.runtime = self.result_array['duration']

    def get_genre(self):
        self.genre = string.join(self.result_array['genres'], ', ')

    def get_cast(self):
        self.cast = ''
        for element in self.result_array['actors']:
            self.cast = self.cast + element['name'] + '\n'

    def get_classification(self):
        self.classification = ''

    def get_studio(self):
        self.studio = ''

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        self.site = self.result_array['url']

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        self.country = self.result_array['countries_text']

    def get_rating(self):
        try:
            self.rating = round(float(self.result_array['average']) * 2.0)
        except:
            self.rating = 0

    def get_notes(self):
        self.notes = ''
        if len(self.result_array['alternative_titles']):
            self.notes = self.notes + 'Alternatieve titel:\n'
            for element in self.result_array['alternative_titles']:
                self.notes = self.notes + element['title'] + '\n'

class SearchPlugin(movie.SearchMovie):
    server = ServerProxy('http://www.moviemeter.nl/ws', transport=ProxiedTransport())

    def __init__(self):
        self.original_url_search   = 'http://www.moviemeter.nl/film/search/'
        self.translated_url_search = 'http://www.moviemeter.nl/film/search/'
        self.encode                = 'iso8859-1'

    def search(self,parent_window):
        self.result_array = None
        if not self.open_search(parent_window):
            return None
        if self.result_array:
            return 'dummy'
        return None

    def open_search(self, parent_window):
        self.titles = [""]
        self.ids = [""]
        if parent_window is not None:
            self.parent_window = parent_window
        self.progress.set_data(parent_window, _("Searching"), _("Wait a moment"), False)
        self.progress.pulse()
        sessionkey = None
        result = self.server.api.startSession(moviemeter_api_key)
        self.progress.pulse()
        try:
            sessionkey = result['session_key']
            self.result_array = self.server.film.search(sessionkey, self.title)
            self.progress.pulse()
        finally:
            if sessionkey:
                self.server.api.closeSession(sessionkey)
            self.progress.pulse()
        return True

    def get_searches(self):
        for element in self.result_array:
            self.ids.append(element['filmId'])
            if element['alternative_title']:
                self.titles.append(element['title'] + ' (' + element['year'] + '; ' + element['alternative_title'] + ')')
            else:
                self.titles.append(element['title'] + ' (' + element['year'] + ')')

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Rocky Balboa'         : [ 1, 1 ],
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
        '1017' : { 
            'title'             : 'Rocky II',
            'o_title'           : 'Rocky II',
            'director'          : 'Sylvester Stallone',
            'plot'              : True,
            'cast'              : 'Sylvester Stallone\n\
Talia Shire\n\
Carl Weathers',
            'country'           : 'Verenigde Staten',
            'genre'             : 'Actie, Drama',
            'classification'    : False,
            'studio'            : False,
            'o_site'            : False,
            'site'              : 'http://www.moviemeter.nl/film/1017/',
            'trailer'           : False,
            'year'              : 1979,
            'notes'             : 'Alternatieve titel:\n\
De Uitdager',
            'runtime'           : 119,
            'image'             : True,
            'rating'            : 7
        },
    }
