# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright © 2009 Piotr Ożarowski
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

import logging

from sqlalchemy.sql import delete

from db.tables import movies as movies_table
from gutils import question
from plugins.extensions import GriffithExtensionBase as Base
from sql import update_whereclause

log = logging.getLogger('Griffith')

class GriffithExtension(Base):
    name = 'Remover'
    description = _('Removes all currently filtered movies')
    author = 'Piotr Ożarowski'
    email = 'piotr@griffith.cc'
    version = 0.1
    api = 1
    enabled = True # TODO: disable it by default

    toolbar_icon = 'gtk-delete'

    def toolbar_icon_clicked(self, widget, movie):
        if question(_('Are you sure you want to remove %d movies?') % self.app.total):
            session = self.db.Session()

            query = delete(movies_table)
            # FIXME: self.app._search_conditions contains advfilter conditions only (no other filters)
            query = update_whereclause(query, self.app._search_conditions)
            query = query.where(movies_table.c.loaned==False) # don't delete loaned movies

            session.execute(query)
            session.commit()

            self.app.populate_treeview()
