# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005 Vasco Nunes
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
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
from urllib import *
import sys
import string
import gutils
import gtk
import gglobals
import os
import os.path
import threading
import time
import tempfile

class Movie:
	number = None
	original_title = None
	title = None
	director = None
	year = None
	running_time = None
	genre = None
	with = None
	classification = None
	studio = None
	site = None
	imdb = None
	trailer = None
	country = None
	page = None
	url = None
	rating = None
	engine_name = None
	engine_description = None
	engine_language = None
	engine_author = None
	engine_version = None
	movie_id = None
	picture_url = None
	picture = None
	encode = 'iso-8859-1'
	debug = False
	rating = 0  
	notes = ""	  
	def open_page(self,parent_window):
		self.parent_window = parent_window
		progress = Progress(parent_window,_("Fetching data"),_("Wait a moment"))
		retriever = Retriever(self.url,parent_window,progress)
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
		
	def fetch_picture(self):
		if len(self.picture_url):
			try:
				tmp_dest = tempfile.mktemp(suffix=self.movie_id, prefix='poster_', \
					dir=os.path.join(gglobals.griffith_dir,"posters"))
				self.picture = "%s.jpg" % \
					(string.replace(tmp_dest,os.path.join(gglobals.griffith_dir, \
					"posters")+"/",""))
				dest = tmp_dest+".jpg" 
				progress = Progress(self.parent_window,_("Fetching poster"),_("Wait a moment"))
				retriever = Retriever(self.picture_url,self.parent_window,progress,dest)
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
				self.picture = ""
		else:
			self.picture = ""
		
	def parse_movie(self):
		self.picture()
		self.fetch_picture()
		self.original_title()
		self.original_title = gutils.clean(self.original_title)
		self.original_title = gutils.gdecode(self.original_title, self.encode)
		self.title()
		self.title = gutils.clean(self.title)
		self.title = gutils.gdecode(self.title, self.encode)
		self.director()
		self.director = gutils.clean(self.director)
		self.director = gutils.gdecode(self.director, self.encode)
		self.plot()
		self.plot = gutils.clean(self.plot)
		self.plot = gutils.gdecode(self.plot, self.encode)
		self.year()
		self.year = gutils.clean(self.year)
		self.running_time()
		self.running_time = gutils.clean(self.running_time)
		self.genre()
		self.genre = gutils.clean(self.genre)
		self.genre = gutils.gdecode(self.genre, self.encode)
		self.with()
		self.with = gutils.clean(self.with)
		self.with = gutils.gdecode(self.with, self.encode)
		self.classification()
		self.classification = gutils.clean(self.classification)
		self.classification = gutils.gdecode(self.classification, self.encode)
		self.studio()
		self.studio = gutils.clean(self.studio)
		self.studio = gutils.gdecode(self.studio, self.encode)
		self.site()
		self.site = gutils.clean(self.site)
		self.imdb()
		self.imdb = gutils.clean(self.imdb)
		self.trailer()
		self.trailer = gutils.clean(self.trailer)
		self.country()
		self.country = gutils.clean(self.country)
		self.country = gutils.gdecode(self.country, self.encode)
		self.rating()
		try:
			self.notes()
			self.notes = gutils.clean(self.notes)
			self.notes = gutils.gdecode(self.notes, self.encode)
		except:
			pass
		#self.debug_info()
			
	def debug_info(self):
		pass
		#gdebug.debug("movie number: %s"%self.number)
		#gdebug.debug("original title: %s"%self.original_title)
		#gdebug.debug("title: %s"%self.title)
		#gdebug.debug("picture url: %s"%self.picture_url)
		#gdebug.debug("director: %s"%self.director)
		#gdebug.debug("year: %s"%self.year)
		#gdebug.debug("running time: %s"%self.running_time)
		#gdebug.debug("genre: %s"%self.genre)
		#gdebug.debug("actors: %s"%self.with)
		#gdebug.debug("classification: %s"%self.classification)
		#gdebug.debug("studio: %s"%self.studio)
		#gdebug.debug("imdb: %s"%self.imdb)
		#gdebug.debug("site: %s"%self.site)
		#gdebug.debug("trailer: %s"%self.trailer)
		#gdebug.debug("country: %s"%self.country)
		#gdebug.debug( "rating: %s"%self.rating)
		
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
		self.url=string.replace(self.url+self.title,' ','%20')
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
