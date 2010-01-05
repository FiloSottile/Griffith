# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright © 2010 Michael Jahn
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published byp
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

import os
import logging
from urllib import quote, urlcleanup
import gtk
import gutils
from edit import update_image_from_memory
from movie import Progress, Retriever
from plugins.extensions import GriffithExtensionBase as Base

log = logging.getLogger('Griffith')


class GriffithExtension(Base):
    name = 'MoviePosterDB'
    description = _('Fetch posters from MoviePosterDB.com')
    author = 'Michael Jahn'
    email = 'mike@griffith.cc'
    version = 1
    api = 1
    enabled = True

    toolbar_icon = 'gtk-network'

    baseurltitle = 'http://www.movieposterdb.com/embed.inc.php?movie_title=%s'
    baseurltitleyear = 'http://www.movieposterdb.com/embed.inc.php?movie_title=%s[%s]'

    progress = None
    encode = 'iso8859-1'

    def toolbar_icon_clicked(self, widget, movie):
        log.info('fetching poster from MoviePosterDB.com...')
        self.movie = movie

        # correction of the movie name for the search
        o_title = None
        title = None
        if movie.o_title:
            if movie.o_title[-5:] == ', The':
                o_title = u'The ' + movie.o_title[:-5]
            else:
                o_title = movie.o_title
        if movie.title:
            if movie.title[-5:] == ', The':
                title = u'The ' + movie.title[:-5]
            else:
                title = movie.title

        # try to get an url to the large version of a poster for the movie
        # (requests are in the order:
        #  original title + year, original title only, title + year, title only)
        try:
            largeurl = None
            result = False
            self.encode = 'iso8859-1'
            if o_title:
                if movie.year:
                    url = self.baseurltitleyear % (quote(o_title), movie.year)
                    result = self.search(url, self.widgets['window'])
                    largeurl = gutils.trim(self.data, 'src=\\"', '\\"').replace('/t_', '/l_')
                if not result or not largeurl:
                    url = self.baseurltitle % quote(o_title)
                    result = self.search(url, self.widgets['window'])
                    largeurl = gutils.trim(self.data, 'src=\\"', '\\"').replace('/t_', '/l_')
            if not result or not largeurl and title and title != o_title:
                if movie.year:
                    url = self.baseurltitleyear % (quote(title), movie.year)
                    result = self.search(url, self.widgets['window'])
                    largeurl = gutils.trim(self.data, 'src=\\"', '\\"').replace('/t_', '/l_')
                if not result or not largeurl:
                    url = self.baseurltitle % quote(title)
                    result = self.search(url, self.widgets['window'])
                    largeurl = gutils.trim(self.data, 'src=\\"', '\\"').replace('/t_', '/l_')
        except:
            log.exception('')
            gutils.warning(_('No posters found for this movie.'))
            return

        if not result or not largeurl:
            gutils.warning(_('No posters found for this movie.'))
            return

        # got the url for a large poster, fetch the data, show preview and update the
        # movie entry if the user want it
        self.encode = None
        if not self.search(largeurl, self.widgets['window']):
            gutils.warning(_('No posters found for this movie.'))
            return

        if self.show_preview():
            update_image_from_memory(self.app, movie.number, self.data)

    def show_preview(self):
        loader = gtk.gdk.PixbufLoader()
        loader.write(self.data, len(self.data))
        loader.close()
        handler = self.widgets['big_poster'].set_from_pixbuf(loader.get_pixbuf())
        self.widgets['poster_window'].show()
        self.widgets['poster_window'].move(0, 0)
        result = gutils.question(_("Do you want to use this poster instead?"), self.widgets['window'])
        self.widgets['poster_window'].hide()
        return result

    def search(self, url, parent_window):
        try:
            #
            # initialize the progress dialog once for the following search process
            #
            if self.progress is None:
                self.progress = Progress(parent_window)
            self.progress.set_data(parent_window, _("Searching"), _("Wait a moment"), True)
            #
            # call the plugin specific search method
            #
            return self._search(url, parent_window)
        finally:
            # dont forget to hide the progress dialog
            if self.progress:
                self.progress.hide()

    def _search(self, url, parent_window):
        result = False
        try:
            if self.encode:
                url = url.encode(self.encode)
            else:
                url = url.encode('iso8859-1')
        except UnicodeEncodeError:
            url = url.encode('utf-8')
        log.debug('Using url <%s>' % url)
        self.progress.set_data(parent_window, _("Searching"), _("Wait a moment"), False)
        retriever = Retriever(url, parent_window, self.progress)
        retriever.start()
        while retriever.isAlive():
            self.progress.pulse()
            if self.progress.status:
                retriever.join()
            while gtk.events_pending():
                gtk.main_iteration()
        try:
            if retriever.html:
                ifile = file(retriever.html[0], 'rb')
                try:
                    self.data = ifile.read()
                finally:
                    ifile.close()
                # check for gzip compressed pages before decoding to unicode
                if len(self.data) > 2 and self.data[0:2] == '\037\213':
                    self.data = gutils.decompress(self.data)
                if self.encode:
                    self.data = self.data.decode(self.encode, 'replace')
                result = True
                os.remove(retriever.html[0])
        except IOError:
            log.exception('')
        urlcleanup()
        return result
