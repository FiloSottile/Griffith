# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2006 Vasco Nunes, Piotr Ożarowski
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
from urllib import *
import sys
import string
import gutils
import gtk
import os
import os.path
import threading
import time
import tempfile

class Movie:
	cast = None
	classification = None
	country = None
	director = None
	genre = None
	image = None
	notes = None
	number = None
	o_site = None
	o_title = None
	plot = None
	rating = None
	runtime = None
	site = None
	studio = None
	title = None
	trailer = None
	year = None
	
	movie_id = None
	debug = False
	locations = None
	engine_author = None
	engine_description = None
	engine_language = None
	engine_name = None
	engine_version = None
	page = None
	url = None
	image_url = None
	encode = 'iso-8859-1'
	fields_to_fetch = []
	
	# functions that plugin should implement: {{{
	def initialize(self):
		pass
	def get_cast(self):
		pass
	def get_classification(self):
		pass
	def get_country(self):
		pass
	def get_director(self):
		pass
	def get_genre(self):
		pass
	def get_image(self):
		pass
	def get_notes(self):
		pass
	def get_o_site(self):
		pass
	def get_o_title(self):
		pass
	def get_plot(self):
		pass
	def get_runtime(self):
		pass
	def get_site(self):
		pass
	def get_studio(self):
		pass
	def get_title(self):
		pass
	def get_trailer(self):
		pass
	def get_year(self):
		pass
	#}}}

	def __getitem__(self, key):
		return getattr(self,key)
	def __setitem__(self, key, value):
		setattr(self,key,value)
	
	def open_page(self, parent_window=None, url=None):
		if url is None:
			url_to_fetch = self.url
		else:
			url_to_fetch = url
		if parent_window is not None:
			self.parent_window = parent_window
		progress = Progress(self.parent_window,_("Fetching data"),_("Wait a moment"))
		retriever = Retriever(url_to_fetch, self.parent_window,progress)
		retriever.start()
		while retriever.isAlive():
			progress.pulse()
			if progress.status:
				retriever.suspend()
			while gtk.events_pending():
				gtk.main_iteration()
		progress.close()
		try:
			data = file (retriever.html[0]).read()
		except IOError:
			pass
		if url is None:
			self.page = data
		return data
		urlcleanup()

	def fetch_picture(self):
		if self.image_url:
			tmp_dest = tempfile.mktemp(prefix='poster_', dir=self.locations['temp'])
			self.image = tmp_dest.split('poster_', 1)[1]
			dest = "%s.jpg" % tmp_dest
			try:
				progress = Progress(self.parent_window,_("Fetching poster"),_("Wait a moment"))
				retriever = Retriever(self.image_url,self.parent_window,progress,dest)
				retriever.start()
				while retriever.isAlive():
					progress.pulse()
					if progress.status:
						retriever.suspend()
					while gtk.events_pending():
						gtk.main_iteration()
				progress.close()
				urlcleanup()
			except:
				self.image = ""
				try:
					os.remove("%s.jpg" % tmp_dest )
				except:
					print "Can't remove %s file" % tmp_dest # FIXME: use debug.show()
		else:
			self.image = ""

	def parse_movie(self):
		from copy import deepcopy
		fields = deepcopy(self.fields_to_fetch)

		self.initialize()

		if 'year' in fields:
			self.get_year()
			self.year = gutils.digits_only(self.year, 2100)
			fields.pop(fields.index('year'))
		if 'runtime' in fields:
			self.get_runtime()
			self.runtime = gutils.digits_only(self.runtime)
			fields.pop(fields.index('runtime'))
		if 'rating' in fields:
			self.get_rating()
			self.rating = gutils.digits_only(self.rating, 10)
			fields.pop(fields.index('rating'))
		if 'cast' in fields:
			self.get_cast()
			self.cast = gutils.clean(self.cast)
			self.cast = gutils.gdecode(self.cast, self.encode)
			fields.pop(fields.index('cast'))
		if 'plot' in fields:
			self.get_plot()
			self.plot = gutils.clean(self.plot)
			self.plot = gutils.gdecode(self.plot, self.encode)
			fields.pop(fields.index('plot'))
		if 'notes' in fields:
			self.get_notes()
			self.notes = gutils.clean(self.notes)
			self.notes = gutils.gdecode(self.notes, self.encode)
			fields.pop(fields.index('notes'))
		if 'image' in fields:
			self.get_image()
			self.fetch_picture()
			fields.pop(fields.index('image'))

		for i in fields:
			getattr(self, "get_%s" % i)()
			self[i] = gutils.clean(self[i])
			self[i] = gutils.gdecode(self[i], self.encode)
		
		if 'o_title' in self.fields_to_fetch and self.o_title is not None:
			if self.o_title[:4] == 'The ':
				self.o_title = self.o_title[4:] + ', The'
		if 'title' in self.fields_to_fetch and self.title is not None:
			if self.title[:4] == 'The ':
				self.title = self.title[4:] + ', The'

class SearchMovie:
	page = None
	number_results = None
	titles = [""]
	ids = [""]
	url = None
	encode = 'utf-8'
	original_url_search = None
	translated_url_search = None
	elements = None
	title = None

	def __init__(self):
		pass

	def open_search(self,parent_window):
		self.titles = [""]
		self.ids = [""]
		if self.url.find('%s') > 0:
			self.url = self.url % self.title
			self.url = string.replace(self.url, ' ', '%20')
		else:
			self.url = string.replace(self.url+self.title,' ','%20')
		progress = Progress(parent_window,_("Searching"),_("Wait a moment"))
		try:
			url = self.url.encode(self.encode)
		except UnicodeEncodeError:
			url = self.url.encode('utf-8')
		retriever = Retriever(url, parent_window, progress)
		retriever.start()
		while retriever.isAlive():
			progress.pulse()
			if progress.status:
				retriever.suspend()
			while gtk.events_pending():
				gtk.main_iteration()
		progress.close()
		try:
			self.page = file (retriever.html[0]).read()
		except IOError:
			pass
		urlcleanup()

class Retriever(threading.Thread):
	def __init__(self, URL, parent_window, progress, destination=None):
		self.URL = URL
		self.html = None
		self.destination = destination
		self.parent_window = parent_window
		self.progress = progress
		self._stopevent = threading.Event()
		self._sleepperiod = 1.0
		threading.Thread.__init__(self, name="Retriever")
	def run(self):
		try:
			self.html = urlretrieve(self.URL, self.destination, self.hook)
			#self.html = urlretrieve(self.URL.encode('utf-8'), self.destination, self.hook)
			if self.progress.status:
				self.html = []
		except IOError:
			self.progress.dialog.hide()
			gutils.urllib_error(_("Connection error"), self.parent_window)
			self.suspend()
	def hook(self,count, blockSize, totalSize):
		if totalSize ==-1:
			pass
		else:
			try:
				downloaded_percentage = min((count*blockSize*100)/totalSize, 100)
			except:
				downloaded_percentage = 100
			if count != 0:
				downloaded_kbyte = int(count * blockSize/1024.0)
				filesize_kbyte = int(totalSize/1024.0)

class Progress:
	def __init__(self, window, title, message):
		self.status = False
		self.dialog = gtk.Dialog(title, window, gtk.DIALOG_MODAL, ())
		self.label = gtk.Label()
		self.label.set_markup(message)
		self.dialog.vbox.pack_start(self.label)
		self.progress = gtk.ProgressBar()
		self.progress.set_pulse_step(0.01)
		self.dialog.vbox.pack_start(self.progress, False, False)
		self.button = gtk.Button(_("Cancel"), gtk.STOCK_CANCEL)
		self.button.connect("clicked", self.callback)
		self.dialog.vbox.pack_start(self.button, False, False)
		self.dialog.show_all()
	def callback(self, widget):
		self.dialog.hide()
		self.status = True
	def pulse(self):
		self.progress.pulse()
		time.sleep(0.01)
	def close(self):
		self.dialog.destroy()
# vim: fdm=marker
