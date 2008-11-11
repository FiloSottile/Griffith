# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2008
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
import amazon
import threading
import gtk
from operator import isSequenceType
from urlparse import urlsplit
import logging
log = logging.getLogger("Griffith")

plugin_name = "Amazon"
plugin_description = "Amazon"
plugin_url = "www.amazon.com/.uk/.de/.ca/.fr/.jp"
plugin_language = _("International")
plugin_author = "Michael Jahn"
plugin_author_email = "<mikej06@hotmail.com>"
plugin_version = "1.0"

class Plugin(movie.Movie):

    def __init__(self, id):
        self.encode='utf8'
        self.movie_id = id
        self.url = 'http://www.amazon.de/dp/' + str(self.movie_id)

    def open_page(self, parent_window=None, url=None):
        # dont use base functionality
        # use the Amazon Web API
        self.parent_window = parent_window
        try:
            locale = self.config.get('amazon_locale', 0, section='add')
            if locale == '1':
                locale = 'uk'
            elif locale == '2':
                locale = 'de'
            elif locale == '3':
                locale = 'ca'
            elif locale == '4':
                locale = 'fr'
            elif locale == '5':
                locale = 'jp'
            else:
                locale = None
            retriever = AmazonRetriever(self.movie_id, locale, parent_window, self.progress, 'Get')
            retriever.start()
            while retriever.isAlive():
                self.progress.pulse()
                while gtk.events_pending():
                    gtk.main_iteration()
            self.page = retriever.result.Item
        except:
            self.page = ''
            try:
                log.error("Error retrieving results from amazon.")
                log.error(retriever.result.Request.Errors.Error.Message)
            except:
                pass
        return self.page

    def get_image(self):
        self.image_url = ''
        if hasattr(self.page, 'LargeImage'):
            self.image_url = self.page.LargeImage.URL
        elif hasattr(self.page, 'MediumImage'):
            self.image_url = self.page.MediumImage.URL
        elif hasattr(self.page, 'SmallImage'):
            self.image_url = self.page.SmallImage.URL

    def get_o_title(self):
        if hasattr(self.page.ItemAttributes, 'Title'):
            self.o_title = self.page.ItemAttributes.Title
        else:
            self.director = ''

    def get_title(self):
        if hasattr(self.page.ItemAttributes, 'Title'):
            self.title = self.page.ItemAttributes.Title
        else:
            self.director = ''

    def get_director(self):
        if hasattr(self.page.ItemAttributes, 'Director'):
            self.director = self.page.ItemAttributes.Director
        else:
            self.director = ''

    def get_plot(self):
        self.plot = ''
        if hasattr(self.page, 'EditorialReviews'):
            if hasattr(self.page.EditorialReviews, 'EditorialReview'):
                if isSequenceType(self.page.EditorialReviews.EditorialReview):
                    for review in self.page.EditorialReviews.EditorialReview:
                        if string.find(review.Source, 'Amazon') > -1:
                            self.plot = review.Content
                else:
                    if hasattr(self.page.EditorialReviews.EditorialReview, 'Source') and \
                        hasattr(self.page.EditorialReviews.EditorialReview, 'Content') and \
                        string.find(self.page.EditorialReviews.EditorialReview.Source, 'Amazon') > -1:
                        self.plot = self.page.EditorialReviews.EditorialReview.Content

    def get_year(self):
        if hasattr(self.page.ItemAttributes, 'TheatricalReleaseDate'):
            self.year = self.page.ItemAttributes.TheatricalReleaseDate[:4]
        elif hasattr(self.page.ItemAttributes, 'ReleaseDate'):
            self.year = self.page.ItemAttributes.ReleaseDate[:4]
        else:
            self.year = ''

    def get_runtime(self):
        if hasattr(self.page.ItemAttributes, 'RunningTime'):
            self.runtime = self.page.ItemAttributes.RunningTime
        else:
            self.runtime = ''

    def get_genre(self):
        # BrowseNodeId 547664 (Genres)
        self.genre = ''
        delimiter = ''
        if hasattr(self.page, 'BrowseNodes') and hasattr(self.page.BrowseNodes, 'BrowseNode'):
            if isSequenceType(self.page.BrowseNodes.BrowseNode):
                for node in self.page.BrowseNodes.BrowseNode:
                    parentnode = node
                    while hasattr(parentnode, 'Ancestors') and parentnode.BrowseNodeId <> '547664' \
                            and parentnode.BrowseNodeId <> '13628901': # no production countries; they are also arranged under genres
                        parentnode = parentnode.Ancestors.BrowseNode
                    if parentnode.BrowseNodeId == '547664':
                        self.genre = self.genre + delimiter + node.Name
                        delimiter = ', '

    def get_cast(self):
        self.cast = ''
        if hasattr(self.page.ItemAttributes, 'Actor'):
            for actor in self.page.ItemAttributes.Actor:
                self.cast += actor + '\n'

    def get_classification(self):
        if hasattr(self.page.ItemAttributes, 'AudienceRating'):
            self.classification = self.page.ItemAttributes.AudienceRating
        else:
            self.classification = ''

    def get_studio(self):
        if hasattr(self.page.ItemAttributes, 'Studio'):
            self.studio = self.page.ItemAttributes.Studio
        else:
            self.studio = ''

    def get_o_site(self):
        self.o_site = ''

    def get_site(self):
        if hasattr(self.page, 'DetailPageURL'):
            parts = urlsplit(self.page.DetailPageURL)
            self.site = parts[0] + '://' + parts[1] + '/dp/' + self.movie_id
        else:
            self.site = ''

    def get_trailer(self):
        self.trailer = ''

    def get_country(self):
        # BrowseNodeId 13628901 (production countries)
        self.country = ''
        delimiter = ''
        if hasattr(self.page, 'BrowseNodes') and hasattr(self.page.BrowseNodes, 'BrowseNode'):
            if isSequenceType(self.page.BrowseNodes.BrowseNode):
                for node in self.page.BrowseNodes.BrowseNode:
                    parentnode = node
                    while hasattr(parentnode, 'Ancestors') and parentnode.BrowseNodeId <> '13628901':
                        parentnode = parentnode.Ancestors.BrowseNode
                    if parentnode.BrowseNodeId == '13628901':
                        self.country = self.country + delimiter + node.Name
                        delimiter = ', '

    def get_rating(self):
        self.rating = '0'
        if hasattr(self.page, 'CustomerReviews') and \
            hasattr(self.page.CustomerReviews, 'AverageRating'):
            try:
                tmp_float = float(self.page.CustomerReviews.AverageRating)
                tmp_float = round(2 * tmp_float, 0)
                self.rating = str(tmp_float)
            except:
                pass

    def get_notes(self):
        self.notes = ''
        if hasattr(self.page.ItemAttributes, 'EAN'):
            self.notes = 'EAN: ' + self.page.ItemAttributes.EAN


class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search   = 'http://www.amazon.de'
        self.translated_url_search = 'http://www.amazon.de'
        self.encode='utf8'
        self.remove_accents = False

    def search(self,parent_window):
        # dont use base functionality
        # use the Amazon Web API
        self.titles = [""]
        self.ids = [""]
        try:
            locale = self.config.get('amazon_locale', 0, section='add')
            if locale == '1':
                locale = 'uk'
            elif locale == '2':
                locale = 'de'
            elif locale == '3':
                locale = 'ca'
            elif locale == '4':
                locale = 'fr'
            elif locale == '5':
                locale = 'jp'
            else:
                locale = None
            retriever = AmazonRetriever(self.title.encode('iso8859-1'), locale, parent_window, self.progress)
            retriever.start()
            while retriever.isAlive():
                self.progress.pulse()
                while gtk.events_pending():
                    gtk.main_iteration()
            self.page = retriever.result
        except:
            try:
                log.error("Error retrieving results from amazon.")
                log.error(retriever.result.Request.Errors.Error.Message)
            except:
                pass
        return self.page

    def get_searches(self):
        for result in self.page:
            if hasattr(result, 'Item'):
                if hasattr(result.Item, 'ASIN'):
                    self.add_item(result.Item)
                else:
                    for item in result.Item:
                        self.add_item(item)
            elif hasattr(result, 'Items'):
                if hasattr(result.Item, 'ASIN'):
                    self.add_item(result.Items)
                else:
                    for item in result.Items:
                        self.add_item(item)

    def add_item(self, item):
        self.ids.append(item.ASIN)
        if hasattr(item.ItemAttributes, 'ProductGroup'):
            productGroup = item.ItemAttributes.ProductGroup + ' - '
        else:
            productGroup = ''
        if hasattr(item.ItemAttributes, 'Title'):
            title = item.ItemAttributes.Title
        else:
            title = ''
        if hasattr(item.ItemAttributes, 'TheatricalReleaseDate'):
            theatricalReleaseDate = ' (' + item.ItemAttributes.TheatricalReleaseDate + ')'
        else:
            theatricalReleaseDate = ''
        self.titles.append("%s%s%s" % (productGroup, title, theatricalReleaseDate))

class AmazonRetriever(threading.Thread):

    def __init__(self, title, locale, parent_window, progress, lookuptype='Search', destination=None):
        self.title = title
        self.locale = locale
        self.result = None
        self.destination = destination
        self.parent_window = parent_window
        self.progress = progress
        # Search or Get
        self.lookuptype = lookuptype
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name='Retriever')

    def run(self):
        if self.lookuptype == 'Get':
            self.run_get()
        else:
            self.run_search()

    def run_search(self):
        self.result = []
        try:
            amazon.setLicense('04GDDMMXX8X9CJ1B22G2')
            try:
                tmp = amazon.searchByTitle(self.title, type='ItemAttributes', product_line='Video', locale=self.locale, page=1)
                self.result.append(tmp)
                if hasattr(tmp, 'TotalPages'):
                    pages = int(tmp.TotalPages) - 1
                    page = 2
                    while page < pages and page < 11:
                        tmp = amazon.searchByTitle(self.title, type='ItemAttributes', product_line='Video', locale=self.locale, page=page)
                        self.result.append(tmp)
                        page = page + 1
            except amazon.AmazonError, e:
                log.error(e.Message)
            # if all digits then try to find an EAN / UPC
            if self.title.isdigit():
                if len(self.title) == 13:
                    try:
                        tmp = amazon.searchByEAN(self.title, type='ItemAttributes', product_line='Video', locale=self.locale)
                        self.result.append(tmp)
                    except amazon.AmazonError, e:
                        log.error(e.Message)
                elif len(self.title) == 12:
                    try:
                        tmp = amazon.searchByUPC(self.title, type='ItemAttributes', product_line='Video', locale=self.locale)
                        self.result.append(tmp)
                    except amazon.AmazonError, e:
                        log.error(e.Message)
        except IOError:
            self.progress.dialog.hide()
            gutils.urllib_error(_('Connection error'), self.parent_window)
            self.suspend()

    def run_get(self):
        self.result = None
        try:
            amazon.setLicense('04GDDMMXX8X9CJ1B22G2')
            # get by ASIN
            try:
                self.result = amazon.searchByASIN(self.title, type='Large', locale=self.locale)
            except amazon.AmazonError, e:
                log.error(e.Message)
        except IOError:
            self.progress.dialog.hide()
            gutils.urllib_error(_('Connection error'), self.parent_window)
            self.suspend()

#
# Plugin Test
#
class SearchPluginTest(SearchPlugin):
    #
    # Configuration for automated tests:
    # dict { movie_id -> [ expected result count for original url, expected result count for translated url ] }
    #
    test_configuration = {
        'Rocky Balboa'          : [ 10, 10 ],
        'Arahan'                : [ 6, 6 ],
        'Ein glückliches Jahr'  : [ 2, 2 ]
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
        'B000TIQMMI' : { 
            'title'             : 'Rocky Balboa',
            'o_title'             : 'Rocky Balboa',
            'director'            : '',
            'plot'                 : True,
            'cast'                : 'Sylvester Stallone\n\
Antonio Traver\n\
Burt Young',
            'country'            : 'USA',
            'genre'                : 'Mehr Drama, Drama',
            'classification'    : 'Freigegeben ab 12 Jahren',
            'studio'            : 'MGM Home Entertainment GmbH (dt.)',
            'o_site'            : False,
            'site'                : 'http://www.amazon.de/dp/B000TIQMMI',
            'trailer'            : False,
            'year'                : 2006,
            'notes'                : 'EAN: 4045167004504',
            'runtime'            : 97,
            'image'                : True,
            'rating'            : 9
        },
        'B0009NSASM' : { 
            'title'             : 'Ein glückliches Jahr',
            'o_title'             : 'Ein glückliches Jahr',
            'director'            : 'Claude Lelouch',
            'plot'                 : False,
            'cast'                : 'Lino Ventura\n\
Françoise Fabian\n\
Charles Gérard',
            'country'            : 'Frankreich, Italien',
            'genre'                : 'Krimi, Mehr Drama, Mehr Komödie, Drama, Komödie, Krimi',
            'classification'    : 'Freigegeben ab 12 Jahren',
            'studio'            : 'Warner Home Video - DVD',
            'o_site'            : False,
            'site'                : 'http://www.amazon.de/dp/B0009NSASM',
            'trailer'            : False,
            'year'                : 1973,
            'notes'                : 'EAN: 7321921998843',
            'runtime'            : 110,
            'image'                : True,
            'rating'            : 10
        },
        'B000BSNOD6' : { 
            'title'             : 'Arahan (Vanilla-DVD)',
            'o_title'             : 'Arahan (Vanilla-DVD)',
            'director'            : 'Ryoo Seung-wan',
            'plot'                 : False,
            'cast'                : 'Ryu Seung-beom\n\
Yoon So-yi\n\
Ahn Sung-kee',
            'country'            : 'Südkorea',
            'genre'                : 'Actionkomödie, Abenteuer- & Actionkomödie, Fantasykomödie, Action, Komödie, Mehr Fantasy, Korea, Action, Komödie, Fantasy, Unter 10 EUR',
            'classification'    : 'Freigegeben ab 16 Jahren',
            'o_site'            : False,
            'site'                : 'http://www.amazon.de/dp/B000BSNOD6',
            'trailer'            : False,
            'year'                : 2005,
            'notes'                : 'EAN: 4013549871105',
            'runtime'            : 108,
            'image'                : True,
            'rating'            : 8
        }
    }
