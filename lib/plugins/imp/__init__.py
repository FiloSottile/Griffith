# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2006-2007 Piotr Ożarowski
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

# detect all plugins:
import glob
import os.path
import time
import gc
import gettext
gettext.install('griffith', unicode=1)
import logging
log = logging.getLogger("Griffith")

import db

__all__ = [os.path.basename(x)[:-3] for x in glob.glob("%s/*.py" % os.path.dirname(__file__))]
__all__.remove('__init__')

class ImportPlugin(object):
    description = None
    author = None
    email = None
    version = None
    # file chooser:
    file_filters = None
    mime_types = None

    edit = False        # open add window for every movie?

    imported = 0
    data = None

    def __init__(self, parent, fields_to_import):
        self.db = parent.db
        self.locations = parent.locations
        self.fields = parent.field_names
        self.conditions = parent._conditions
        self.colors = parent._colors
        self.lang_types = parent._lang_types
        self.layers = parent._layers
        self.regions = parent._regions
        self.widgets = parent.widgets['import']
        self.fields_to_import = fields_to_import
        self._continue = True

    def initialize(self):
        """Initializes plugin (get all parameters from user, etc.)"""
        self.imported = 0
        return True

    def abort(self, *args):
        """called after abort button clicked"""
        self._continue = False

    def set_source(self, name):
        """Prepare source (open file, etc.)"""

    def count_movies(self):
        """Returns number of movies in file which is about to be imported"""
        pass

    def get_movie_details(self):
        """Returns dictionary with movie details"""
        pass

    def run(self, name):
        """Import movies, function called in a loop over source files"""
        from add import validate_details, edit_movie
        from gutils import find_next_available
        from sqlalchemy import select, func
        import gtk
        
        if not self.set_source(name):
            log.info("Can't read data from file %s", name)
            return False
        
        self.widgets['pwindow'].show()
        while gtk.events_pending():    # give GTK some time for updates
            gtk.main_iteration()

        # progressbar
        update_on = []
        count = self.count_movies()
        if count > 0:
            for i in range(0,100):
                update_on.append(int(float(i)/100*count))

        session = self.db.Session()
        session.bind = self.db.session.bind
        
        # move some stuff outside the loop to speed it up
        set_fraction = self.widgets['progressbar'].set_fraction
        set_text = self.widgets['progressbar'].set_text
        main_iteration = gtk.main_iteration

        # get some values from DB to avoid queries in the loop
        statement = select([db.Movie.number, db.Movie.title, db.Movie.o_title])
        data = session.execute(statement).fetchall()
        numbers = set([i[0] for i in data])
        titles = set(i[1].lower() for i in data)
        o_titles = set(i[2].lower() for i in data)

        gc_was_enabled = gc.isenabled()
        if gc_was_enabled:
            gc.collect()
            gc.disable()

        begin = time.time()
        processed = 0
        while self._continue:
            details = self.get_movie_details()
            if details is None:
                break
            
            processed += 1
            if processed in update_on:
                set_fraction(float(processed)/count)
                main_iteration()
                set_text("%s (%s/%s)" % (self.imported, processed, count))
                main_iteration()
                main_iteration() # extra iteration for abort button

            o_title_avail = 'o_title' in details
            title_avail = 'title' in details

            if (o_title_avail and details['o_title']) or (title_avail and details['title']):
                if o_title_avail and details['o_title'].lower() in o_titles:
                    if title_avail and details['title'].lower() in titles:
                        log.info("movie already exists (o_title=%s, title=%s)", details['o_title'], details['title'])
                        continue
                elif title_avail and details['title'].lower() in titles: # o_title is not available so lets check title only
                    log.info("movie already exists (title=%s)", details['title'])
                    continue
                validate_details(details, self.fields_to_import)
                if self.edit: # XXX: not used for now
                    response = edit_movie(self.parent, details)    # FIXME: wait until save or cancel button pressed
                    if response == 1:
                        self.imported += 1
                else:
                    number = details.get('number', 1)
                    while number in numbers:
                        number += 1
                    details['number'] = number
                    #movie = db.Movie()
                    #movie.add_to_db(details)
                    try:
                        db.movies_table.insert(bind=self.db.session.bind).execute(details)
                        self.imported += 1
                    except Exception, e:
                        log.info("movie details are not unique, skipping: %s", e)
                    numbers.add(number)
            else:
                log.info('skipping movie without title and original title')
        log.info("Import process took %s s; %s/%s movies imported", (time.time() - begin), processed, count)
        if gc_was_enabled:
            gc.enable()
        self.widgets['pwindow'].hide()
        return True

    def clear(self):
        """clear plugin before next source file"""
        self.data = None
        self.imported = 0
        self.__source_name = None
        self._continue = True
    
    def destroy(self):
        """close all resources"""
        pass


def on_import_plugin_changed(combobox, widgets, *args):
    from gtk import FileFilter
    import plugins.imp
    plugin_name = widgets['plugin'].get_active_text()
    __import__("plugins.imp.%s" % plugin_name)
    ip = eval("plugins.imp.%s.ImportPlugin" % plugin_name)
    widgets['author'].set_markup("<i>%s</i>" % ip.author)
    widgets['email'].set_markup("<i>%s</i>" % ip.email)
    widgets['version'].set_markup("<i>%s</i>" %ip.version)
    widgets['description'].set_markup("<i>%s</i>" %ip.description)
    # file filters
    for i in widgets['fcw'].list_filters():
        widgets['fcw'].remove_filter(i)
    f = FileFilter()
    f.set_name(plugin_name)
    if ip.file_filters is not None:
        if isinstance(ip.file_filters, tuple) or isinstance(ip.file_filters, list):
            for i in ip.file_filters:
                f.add_pattern(i)
        else:
            f.add_pattern(ip.file_filters)
    if ip.mime_types is not None:
        if isinstance(ip.mime_types, tuple) or isinstance(ip.mime_types, list):
            for i in ip.mime_types:
                f.add_mime_type(i)
        else:
            f.add_mime_type(ip.mime_types)
    widgets['fcw'].add_filter(f)
    f = FileFilter()
    f.set_name(_("All files"))
    f.add_pattern("*")
    widgets['fcw'].add_filter(f)

def on_import_button_clicked(button, self, *args):
    import plugins.imp, gutils
    plugin_name = self.widgets['import']['plugin'].get_active_text()
    filenames = self.widgets['import']['fcw'].get_filenames()
    
    fields = []
    w = self.widgets['import']['fields']
    for i in w:
        if w[i].get_active():
            fields.append(i)

    __import__("plugins.imp.%s" % plugin_name)
    ip = eval("plugins.imp.%s.ImportPlugin(self, fields)" % plugin_name)
    if ip.initialize():
        self.widgets['window'].set_sensitive(False)
        self.widgets['import']['window'].hide()
        self.widgets['import']['pabort'].connect('clicked', ip.abort, ip)
        for filename in filenames:
            self.widgets['import']['progressbar'].set_fraction(0)
            self.widgets['import']['progressbar'].set_text('')
            if ip.run(filename):
                gutils.info(self, _("%s file has been imported. %s movies added.") \
                    % (plugin_name, ip.imported), self.widgets['window'])
                self.populate_treeview()
            ip.clear()
        ip.destroy()
        self.widgets['import']['pwindow'].hide()
        self.widgets['window'].set_sensitive(True)

def on_abort_button_clicked(button, self, *args):
    self.widgets['import']['window'].hide()
    self.widgets['import']['pwindow'].hide()
    self.widgets['window'].set_sensitive(True)

