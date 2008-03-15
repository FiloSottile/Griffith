# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2008 Vasco Nunes, Piotr Ożarowski
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

from gettext import gettext as _
import gutils
import os
import wx

def delete_movie(self):
    index = self.main_listcontrol.GetFirstSelected()
    if index == -1:
        return
    while index != -1:
        item = self.main_listcontrol.GetItem(index)
        number = item.GetText()
        movie = self.db.Movie.get_by(number=number) 
        try:
            delete_poster(self, movie.image)
        except:
            pass
        try:
            movie.remove_from_db()
            # update main treelist
            self.main_listcontrol.DeleteItem(index)
        except:
            pass
        index = self.main_listcontrol.GetNextSelected(index)    

def delete_poster(self, poster):
    if not poster:
        self.debug.show('Delete poster: no poster to delete')
        return False
    posters_dir = os.path.join(self.locations['posters'])
    image_full = os.path.join(posters_dir, poster + ".jpg")
    if os.path.isfile(image_full):
        try:
            os.remove(image_full)
        except:
            self.debug.show("Can't remove %s file"%image_full)