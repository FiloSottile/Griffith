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


def count_statusbar(self):
    allmovies = self.db.Movie.count_by()
    loaned = self.db.Movie.count_by(loaned=True)
    not_seen = self.db.Movie.count_by(seen=False)
    update_statusbar(self,_("Listing")+" "+str(self.main_listcontrol.GetItemCount())+"/"+str(allmovies) + _(' film(s) in collection. ') + str(loaned) + _(' film(s) loaned. ') + _('You haven\'t seen ')+"%s"%str(not_seen)+ _(" film(s)")
        )

def update_statusbar(self, text):
    self.main_frame_statusbar.SetStatusText(text)