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

import gettext
from sqlalchemy import Select, desc
import gutils
import os

def update_volume_combo_ids(self):
    self.volume_combo_ids = {}
    self.volume_combo_ids[0] = 0
    i = 1
    volumes = Select(self.db.Volume.c, order_by='name')
    for volume in volumes.execute().fetchall():
        self.volume_combo_ids[i] = volume.volume_id
        i += 1

def update_collection_combo_ids(self):
	self.collection_combo_ids = {}
	self.collection_combo_ids[0] = 0
	i = 1
	collections = Select(self.db.Collection.c, order_by='name')
	for collection in collections.execute().fetchall():
		self.collection_combo_ids[i] = collection.collection_id
		i += 1

def update_loanedto_combo_ids(self):
	self.loanedto_combo_ids = {}
	self.loanedto_combo_ids[0] = 0
	i = 1
	persons = Select(self.db.Person.c, order_by='name')
	for person in persons.execute().fetchall():
		self.loanedto_combo_ids[i] = person.person_id
		i += 1

def update_bytag_combo_ids(self):
	self.bytag_combo_ids = {}
	self.bytag_combo_ids[0] = 0
	i = 1
	tags = Select(self.db.Tag.c, order_by='name')
	for tag in tags.execute().fetchall():
		self.bytag_combo_ids[i] = tag.tag_id
		i += 1
