# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2009 Vasco Nunes, Piotr Ożarowski

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

import gutils
import db

def change_filter(self):
    from sqlalchemy import select, or_
    from sqlalchemy.orm.util import class_mapper, object_mapper
    statement = select(db.tables.movies.columns, bind=self.db.session.bind)
    
    change_filter_update_whereclause(self, statement)
    self.populate_treeview(statement)


def change_filter_update_whereclause(self, statement):
    from sqlalchemy import or_
    text = gutils.gescape(self.widgets['filter']['text'].get_text().decode('utf-8'))
    if text:
        (criterianame, criteria) = self.search_criteria_sorted[self.widgets['filter']['criteria'].get_active()]
        if criteria in ('year', 'runtime', 'media_num', 'rating'):
            statement.append_whereclause(db.tables.movies.c[criteria]==text)
        elif criteria == 'any':
            crits = [ ]
            for crit in ( 'director', 'title', 'o_title', 'cameraman', 'cast', 'year' ):
                crits.append(db.tables.movies.c[crit].like('%'+text+'%'))
            statement.append_whereclause(or_(*crits))
        else:
            statement.append_whereclause(db.tables.movies.c[criteria].like('%'+text+'%'))
    if self.widgets['filter']['text'].is_focus():
        if len(text)<4: # filter mode
            limit = int(self.config.get('limit', 0, section='mainlist'))
            if limit > 0:
                statement.limit = limit

    
def clear_filter(self, populate=True):
    # prevent multiple treeview updates
    self.initialized = False
    self.widgets['filter']['text'].set_text('')
    self.widgets['filter']['collection'].set_active(0)
    self.widgets['filter']['advfilter'].set_active(0)
    self.initialized = True
    if populate:
        self.populate_treeview()
