# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2008 Vasco Nunes, Piotr Ożarowski

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

from gettext import gettext as _
import gutils, statusbar
import os, wx

def treeview_clicked(self, number=None):
    if self.initialized is False:
        return False
    movie = self.db.Movie.get_by(number=number)
    set_details(self, movie)

def set_details(self, item=None):

    if item is None:
        item = {}
    if item.has_key('movie_id') and item['movie_id']:
        self._movie_id = item['movie_id']
    else:
        self._movie_id = None
    if item.has_key('movie_id') and item['movie_id']:
        self.number.SetLabel(unicode(item['number']))
    else:
        self.o_title.SetLabel('')
    if item.has_key('o_title') and item['o_title']:
        self.o_title.SetLabel(unicode(item['o_title']))
    else:
        self.o_title.SetLabel('')
    if item.has_key('title') and item['title']:
        self.title.SetLabel(unicode(item['title']))
    else:
        self.title.SetLabel('')
    if item.has_key('plot') and item['plot']:
        self.plot.SetValue(unicode(item['plot']))
    else:
        self.plot.SetValue('')
    if item.has_key('cast') and item['cast']:
        self.cast.SetValue(unicode(item['cast']))
    else:
        self.cast.SetValue('')
    if item.has_key('notes') and item['notes']:
        self.notes.SetValue(unicode(item['notes']))
    else:
        self.notes.SetValue('')
        
    # poster
    if item.has_key('image') and item['image']:
        tmp_dest = self.locations['posters']
        tmp_img = os.path.join(tmp_dest, "%s.jpg"%item['image'])
        if os.path.isfile(tmp_img):
            image_path = tmp_img

        else:
            image_path = os.path.join(self.locations['images'], 'default.png')

    else:
        image_path = os.path.join(self.locations['images'], 'default.png')

    image = wx.Image(image_path)
    image.Rescale(150,200,wx.IMAGE_QUALITY_NORMAL)
    self.poster.SetBitmapLabel(image.ConvertToBitmap())

def populate(self, movies=None, where=None):#{{{
    import sys
    if self.initialized is False:
        return False
    from sqlalchemy import Select, desc
    
    if movies is None:
        movies = Select([self.db.Movie.c.number,
            self.db.Movie.c.o_title, self.db.Movie.c.title,
            self.db.Movie.c.director, self.db.Movie.c.image,
            self.db.Movie.c.genre, self.db.Movie.c.seen,
            self.db.Movie.c.year, self.db.Movie.c.runtime])
            
    if isinstance(movies, Select):
        """if not where: # because of possible 'seen', 'loaned', 'collection_id' in where
            # seen / loaned
            #loaned_only = self.widgets['menu']['loaned_movies'].get_active()
            #not_seen_only = self.widgets['menu']['not_seen_movies'].get_active()
            pass
            if loaned_only:
                movies.append_whereclause(self.db.Movie.c.loaned==True)
            if not_seen_only:
                movies.append_whereclause(self.db.Movie.c.seen==False)
            # collection
            #pos = self.widgets['filter']['collection'].get_active()
            if pos >= 0:
                #col_id = self.collection_combo_ids[pos]
                if col_id > 0:
                    movies.append_whereclause(self.db.Movie.c.collection_id==col_id)
            # volume
            #pos = self.widgets['filter']['volume'].get_active()
            if pos >= 0:
                #vol_id = self.volume_combo_ids[pos]
                if vol_id > 0:
                    movies.append_whereclause(self.db.Movie.c.volume_id==vol_id)
        """
        # select sort column
        sort_column_name = self.config.get('sortby', 'number', section='mainlist')
        sort_reverse = self.config.get('sortby_reverse', False, section='mainlist')
        for i in sort_column_name.split(','):
            if self.db.Movie.c.has_key(i):
                if sort_reverse:
                    movies.append_order_by(desc(self.db.Movie.c[i]))
                else:
                    #movies.append_order_by(self.db.Movie.c[i])
                    pass
        
        # additional whereclause (volume_id, collection_id, ...)
        if where:
            for i in where:
                if self.db.Movie.c.has_key(i):
                    movies.append_whereclause(self.db.Movie.c[i]==where[i])
        movies = movies.execute().fetchall()

    self.main_listcontrol.DeleteAllItems()

    for movie in movies:
        index = self.main_listcontrol.InsertStringItem(sys.maxint, str(movie.number))
        self.main_listcontrol.SetStringItem(index, 1, unicode(movie.o_title))
        self.main_listcontrol.SetStringItem(index, 2, unicode(movie.title))
        self.main_listcontrol.SetStringItem(index, 3, unicode(movie.director))
        self.main_listcontrol.SetStringItem(index, 4, unicode(movie.genre))
        self.main_listcontrol.SetStringItem(index, 5, str(movie.seen))
        self.main_listcontrol.SetStringItem(index, 6, str(movie.year))
        self.main_listcontrol.SetStringItem(index, 7, str(movie.runtime))
   
    statusbar.count_statusbar(self)
        
    self.main_listcontrol.SetColumnWidth(0, 40)
    self.main_listcontrol.SetColumnWidth(1, wx.LIST_AUTOSIZE)
    self.main_listcontrol.SetColumnWidth(2, wx.LIST_AUTOSIZE)
    self.main_listcontrol.SetColumnWidth(3, wx.LIST_AUTOSIZE)