# -*- coding: UTF-8 -*-

__revision__ = '$Id: $'

# Copyright (c) 2005-2008 Vasco Nunes, Piotr Ożarowski
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

# these are the only to be "true" cross-platform
# other like license, icon, homepage...
# have different behaviors under different platforms

import wx, os

def display_poster_viewer(self):
    index = self.main_listcontrol.GetFirstSelected()
    item = self.main_listcontrol.GetItem(index)
    number = item.GetText()
    movie = self.db.Movie.get_by(number = number)
    if movie.has_key('image') and movie['image']:
        tmp_dest = self.locations['posters']
        tmp_img = os.path.join(tmp_dest, "%s.jpg"%movie['image'])
        if os.path.isfile(tmp_img):
            image_path = tmp_img
            image = wx.Image(image_path)
            self.viewer_frame.poster.SetBitmap(image.ConvertToBitmap())
            self.viewer_frame.Fit()
            self.viewer_frame.Center()
            self.viewer_frame.Show()