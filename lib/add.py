# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005 Vasco Nunes
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

from gettext import gettext as _
import gutils
import os
import gtk
import string
import shutil
import quick_filter
import tempfile

def clear(self):
	"""clears all fields in dialog"""
	set_details(self, {})

def add_movie(self):
	quick_filter.clear_filter(self)
	next_number = gutils.find_next_available(self)
	clear(self)
	self.widgets['add']['number'].set_value(int(next_number))
	self.widgets['add']['window'].show()
	self.active_plugin = ''

def set_details(self, item=None):#{{{
	if item is None:
		item = {}
	if item.has_key('movie_id') and item['movie_id']:
		self._am_movie_id = item['movie_id']
	else:
		self._am_movie_id = None
	w = self.widgets['add']

	cast_buffer  = w['cast'].get_buffer()
	notes_buffer = w['notes'].get_buffer()
	plot_buffer  = w['plot'].get_buffer()

	if item.has_key('o_title') and item['o_title']:
		w['o_title'].set_text(item['o_title'])
	else:
		w['o_title'].set_text('')
	if item.has_key('title') and item['title']:
		w['title'].set_text(item['title'])
	else:
		w['title'].set_text('')
	if item.has_key('number') and item['number']:
		w['number'].set_value(int(item['number']))
	else:
		w['number'].set_value(int(gutils.find_next_available(self)))
	if item.has_key('title') and item['title']:
		w['title'].set_text(item['title'])
	if item.has_key('year') and item['year']:
		w['year'].set_value(int(item['year']))
	else:
		w['year'].set_value(0)
	if item.has_key('runtime') and item['runtime']:
		w['runtime'].set_value(int(item['runtime']))
	else:
		w['runtime'].set_value(0)
	if item.has_key('country') and item['country']:
		w['country'].set_text(item['country'])
	else:
		w['country'].set_text('')
	if item.has_key('classification') and item['classification']:
		w['classification'].set_text(item['classification'])
	else:
		w['classification'].set_text('')
	if item.has_key('studio') and item['studio']:
		w['studio'].set_text(item['studio'])
	else:
		w['studio'].set_text('')
	if item.has_key('o_site') and item['o_site']:
		w['o_site'].set_text(item['o_site'])
	else:
		w['o_site'].set_text('')
	if item.has_key('director') and item['director']:
		w['director'].set_text(item['director'])
	else:
		w['director'].set_text('')
	if item.has_key('site') and item['site']:
		w['site'].set_text(item['site'])
	else:
		w['site'].set_text('')
	if item.has_key('trailer') and item['trailer']:
		w['trailer'].set_text(item['trailer'])
	else:
		w['trailer'].set_text('')
	if item.has_key('title') and item['title']:
		w['title'].set_text(item['title'])
	else:
		w['title'].set_text('')
	if item.has_key('picture') and item['picture']:
		w['picture'].set_from_file(item['picture'])
	else:
		w['picture'].set_from_file('')
	if item.has_key('picture_name') and item['picture_name']:
		w['picture_name'].set_text(item['picture_name'])
	else:
		w['picture_name'].set_text('')
	if item.has_key('genre') and item['genre']:
		w['genre'].set_text(item['genre'])
	else:
		w['genre'].set_text('')
	if item.has_key('color') and item['color']:
		w['color'].set_active(int(item['color']))
	elif self.config.has_key('color'):
		w['color'].set_active(int(self.config.get('color')))
	else:
		w['color'].set_active(3)
	if item.has_key('layers') and item['layers']:
		w['layers'].set_active(int(item['layers']))
	elif self.config.has_key('layers'):
		w['layers'].set_active(int(self.config.get('layers')))
	else:
		w['layers'].set_active(4)
	if item.has_key('region') and item['region']:
		w['region'].set_active(int(item['region']))
	elif self.config.has_key('region'):
		w['region'].set_active(int(self.config.get('region')))
	else:
		w['region'].set_active(9)
	if item.has_key('cond') and item['cond']:
		w['condition'].set_active(int(item['cond']))
	elif self.config.has_key('condition'):
		w['condition'].set_active(int(self.config.get('condition')))
	else:
		w['condition'].set_active(5)
	if item.has_key('media_num') and item['media_num']:
		w['discs'].set_value(int(item['media_num']))
	else:
		w['discs'].set_value(1)
	if item.has_key('rating') and item['rating']:
		w['rating_slider'].set_value(item['rating'])
	else:
		w['rating_slider'].set_value(0)
	if item.has_key('seen') and item['seen'] is True:
		w['seen'].set_active(True)
	else:
		w['seen'].set_active(False)
	if item.has_key('cast') and item['cast']:
		cast_buffer.set_text(item['cast'])
	else:
		cast_buffer.set_text('')
	if item.has_key('notes') and item['notes']:
		notes_buffer.set_text(item['notes'])
	else:
		notes_buffer.set_text('')
	if item.has_key('plot') and item['plot']:
		plot_buffer.set_text(item['plot'])
	else:
		plot_buffer.set_text('')
	pos = 0
	if item.has_key('medium_id') and item['medium_id']:
		pos = gutils.findKey(item['medium_id'], self.media_ids)
	elif self.config.has_key('media'):
		pos = gutils.findKey(self.config['media'], self.media_ids)
	if pos is not None:
		w['media'].set_active(int(pos))
	else:
		w['media'].set_active(0)
	pos = 0
	if item.has_key('vcodec_id') and item['vcodec_id']:
		pos = gutils.findKey(item['vcodec_id'], self.vcodecs_ids)
	elif self.config.has_key('vcodec'):
		pos = gutils.findKey(self.config['vcodec'], self.vcodecs_ids)
	if pos is not None:
		w['vcodec'].set_active(int(pos))
	else:
		w['vcodec'].set_active(0)
	pos = 0
	if item.has_key('volume_id') and item['volume_id']:
		pos = gutils.findKey(item['volume_id'], self.volume_combo_ids)
	if pos is not None:
		w['volume'].set_active(int(pos))
	else:
		w['volume'].set_active(0)
	pos = 0
	if item.has_key('collection_id') and item['collection_id']:
		pos = gutils.findKey(item['collection_id'], self.collection_combo_ids)
	if pos is not None:
		w['collection'].set_active(int(pos))
	else:
		w['volume'].set_active(0)
	# tags
	for tag in self.am_tags:
		self.am_tags[tag].set_active(False)
	if item.has_key('tags'):
		for tag in item['tags']:
			i = gutils.findKey(tag.tag_id, self.tags_ids)
			self.am_tags[i].set_active(True)
	# languages
	w['lang_treeview'].get_model().clear()
	if item.has_key('languages') and len(item['languages'])>0:
		for i in item['languages']:
			self.create_language_row(i)
	# poster
	if item.has_key('image') and item['image']:
		image_path = os.path.join(self.locations['home'], 'posters', "m_%s.jpg"%item['image'])
	else:
		image_path = os.path.join(self.locations['images'], 'default.png')
	if not os.path.isfile(image_path):
		image_path = os.path.join(self.locations['images'], 'default.png')
	w['picture'].set_from_file(image_path)
	
	w['notebook'].set_current_page(0)
	w['source'].set_active(self.d_plugin)
	w['o_title'].grab_focus()
	from widgets import connect_add_signals
	connect_add_signals(self)
	#}}}

def get_details(self): #{{{
	w = self.widgets['add']
	
	cast_buffer  = w['cast'].get_buffer()
	notes_buffer = w['notes'].get_buffer()
	plot_buffer  = w['plot'].get_buffer()
	
	t_movies = {
		'classification' : w['classification'].get_text(),
		'color'          : w['color'].get_active(),
		'cond'           : w['color'].get_active(),
		'country'        : w['country'].get_text(),
		'director'       : w['director'].get_text(),
		'genre'          : w['genre'].get_text(),
		'layers'         : w['layers'].get_active(),
		'media_num'      : w['discs'].get_text(),
		'number'         : w['number'].get_value(),
		'o_site'         : w['o_site'].get_text(),
		'o_title'        : w['o_title'].get_text(),
		'rating'         : w['rating_slider'].get_value(),
		'region'         : w['region'].get_active(),
		'runtime'        : w['runtime'].get_text(),
		'site'           : w['site'].get_text(),
		'studio'         : w['studio'].get_text(),
		'title'          : w['title'].get_text(),
		'trailer'        : w['trailer'].get_text(),
		'year'           : w['year'].get_text(),
		'collection_id'  : self.collection_combo_ids[w['collection'].get_active()],
		'volume_id'      : self.volume_combo_ids[w['volume'].get_active()],
		'cast'           : cast_buffer.get_text(cast_buffer.get_start_iter(),cast_buffer.get_end_iter()),
		'notes'          : notes_buffer.get_text(notes_buffer.get_start_iter(),notes_buffer.get_end_iter()),
		'plot'           : plot_buffer.get_text(plot_buffer.get_start_iter(),plot_buffer.get_end_iter()),
	}
	if self._am_movie_id is not None:
		t_movies['movie_id'] = self._am_movie_id

	medium_id = w['media'].get_active()
	if medium_id>0:
		t_movies['medium_id'] = self.media_ids[medium_id]
	vcodec_id = w['vcodec'].get_active()
	if vcodec_id>0:
		t_movies['vcodec_id'] = self.vcodecs_ids[vcodec_id]
	if w['seen'].get_active():
		t_movies['seen'] = True
	else:
		t_movies['seen'] = False

	def get_id(model, text):
		for i in model:
			if i[1] == text:
				return i[0]
		return None
	# languages
	from sets import Set as set # for python2.3 compatibility
	t_movies['languages'] = set()
	for row in self.lang['model']:
		lang_id   = get_id(self.lang['lang'], row[0])
		lang_type = get_id(self.lang['type'], row[1])
		acodec    = get_id(self.lang['acodec'], row[2])
		achannel  = get_id(self.lang['achannel'], row[3])
		subformat = get_id(self.lang['subformat'], row[4])
		t_movies['languages'].add((lang_id, lang_type, acodec, achannel, subformat))

	# tags
	t_movies['tags'] = {}
	for i in self.tags_ids:
		if self.am_tags[i].get_active() == True:
			t_movies['tags'][self.tags_ids[i]] = 1
		
	# validate data -------------------------------------------------------
	for i in t_movies.keys():
		if t_movies[i] == '':
			t_movies[i] = None
	for i in ['color','cond','layers','region', 'media', 'vcodec']:
		if t_movies.has_key(i) and t_movies[i] == -1:
			t_movies[i]=None
	for i in ['volume_id','collection_id', 'runtime']:
		if t_movies.has_key(i) and (t_movies[i] is None or int(t_movies[i]) == 0):
			t_movies[i] = None
	if t_movies.has_key('year') and (t_movies['year'] is None or int(t_movies['year']) < 1886):
		t_movies['year'] = None

	return t_movies	#}}}

def add_movie_db(self, close):
	if  len(self.widgets['add']['o_title'].get_text()) or len(self.widgets['add']['title'].get_text()):
		plot_buffer = self.widgets['add']['plot'].get_buffer()
		cast_buffer = self.widgets['add']['cast'].get_buffer()
		notes_buffer = self.widgets['add']['notes'].get_buffer()
		number = self.widgets['add']['number'].get_text()
		(filepath, filename) = os.path.split(self.widgets['add']['picture_name'].get_text())
		t_movies = {
			'cast'           : gutils.gescape(cast_buffer.get_text(cast_buffer.get_start_iter(), cast_buffer.get_end_iter())),
			'classification' : gutils.gescape(self.widgets['add']['classification'].get_text()),
			'color'          : self.widgets['add']['color'].get_active(),
			'cond'           : self.widgets['add']['condition'].get_active(),
			'country'        : gutils.gescape(self.widgets['add']['country'].get_text()),
			'director'       : gutils.gescape(self.widgets['add']['director'].get_text()),
			'genre'          : gutils.gescape(self.widgets['add']['genre'].get_text()),
			'image'          : filename,
			'layers'         : self.widgets['add']['layers'].get_active(),
			'loaned'         : False,
			'media_num'      : self.widgets['add']['discs'].get_text(),
			'notes'          : gutils.gescape(notes_buffer.get_text(notes_buffer.get_start_iter(), notes_buffer.get_end_iter())),
			'number'         : number,
			'o_site'         : self.widgets['add']['o_site'].get_text(),
			'o_title'        : gutils.gescape(self.widgets['add']['o_title'].get_text()),
			'plot'           : gutils.gescape(plot_buffer.get_text(plot_buffer.get_start_iter(), plot_buffer.get_end_iter())),
			'rating'         : self.widgets['add']['rating_slider'].get_value(),
			'region'         : self.widgets['add']['region'].get_active(),
			'runtime'        : self.widgets['add']['runtime'].get_text(),
			'site'           : self.widgets['add']['site'].get_text(),
			'studio'         : gutils.gescape(self.widgets['add']['studio'].get_text()),
			'title'          : gutils.gescape(self.widgets['add']['title'].get_text()),
			'trailer'        : self.widgets['add']['trailer'].get_text(),
			'year'           : self.widgets['add']['year'].get_text()
		}
		vol_id = self.widgets['add']['volume'].get_active()
		if vol_id>0:
			t_movies['volume_id'] = self.volume_combo_ids[vol_id]
		col_id = self.widgets['add']['collection'].get_active()
		if col_id>0:
			t_movies['collection_id'] = self.collection_combo_ids[col_id]
		medium_id = self.widgets['add']['media'].get_active()
		if medium_id>0:
			t_movies['medium_id'] = self.media_ids[medium_id]
		vcodec_id = self.widgets['add']['vcodec'].get_active()
		if vcodec_id>0:
			t_movies['vcodec_id'] = self.vcodecs_ids[vcodec_id]
		seen = int(self.widgets['add']['seen'].get_active())
		if seen == 1:
			t_movies['seen'] = True
		else:
			t_movies['seen'] = False
		# languages
		t_languages = {}
		# tags
		t_tags = {}
		for i in self.tags_ids:
			if self.am_tags[i].get_active() == True:
				t_tags[self.tags_ids[i]] = 1

		# add movie data to database
		self.db.add_movie(t_movies, t_languages, t_tags)

		# lets move poster from tmp to posters dir
		tmp_dest = os.path.join(self.griffith_dir, "posters")

		if os.name == 'nt' or os.name == 'win32':
			temp_dir = tempfile.gettempdir()
			temp_dir = temp_dir + "\\"
		else:
			temp_dir = "/tmp/"

		pic = string.replace(self.widgets['add']['picture_name'].get_text()+".jpg",temp_dir,'')

		if len(self.widgets['add']['picture_name'].get_text()):
			if os.path.isfile(os.path.join(temp_dir, pic)):
				shutil.move(os.path.join(temp_dir, pic), tmp_dest)

		if int(self.widgets['add']['number'].get_text()) >= 2:
			# FIXME: what if number-2 doesn't exist? (TODO: search for nearest number)
			insert_after = self.treemodel.get_iter(int(self.widgets['add']['number'].get_text())-2)
		else:
			insert_after = None
		myiter = self.treemodel.insert_after(None, insert_after)

		if len(self.widgets['add']['picture_name'].get_text()):
			image_path = os.path.join(tmp_dest, pic)
			#lets make the thumbnail and medium image from poster for future use
			gutils.make_thumbnail(self, image_path)
			gutils.make_medium_image(self, image_path)
		else:
			image_path = os.path.join(self.locations['images'], "default.png")
		handler = self.Image.set_from_file(image_path)
		pixbuf = self.Image.get_pixbuf()
		self.treemodel.set_value(myiter, 0, '%004d' % int(self.widgets['add']['number'].get_text()))
		self.treemodel.set_value(myiter, 1, pixbuf.scale_simple(30,40,3))
		self.treemodel.set_value(myiter, 2, str(self.widgets['add']['o_title'].get_text()))
		self.treemodel.set_value(myiter, 3, str(self.widgets['add']['title'].get_text()))
		self.treemodel.set_value(myiter, 4, str(self.widgets['add']['director'].get_text()))
		#update statusbar
		self.total += 1
		self.total_filter = self.total
		self.count_statusbar()
		#select new entry from main treelist
		treeselection = self.widgets['treeview'].get_selection()
		treeselection.select_iter(myiter)
		self.widgets['treeview'].set_cursor(int(self.widgets['add']['number'].get_text())-1)
		self.treeview_clicked()
		next_number=gutils.find_next_available(self)
		clear(self)
		self.widgets['add']['number'].set_text(str(next_number))

		if close:
			self.hide_add_window()
	else:
		gutils.error(self.widgets['results']['window'], _("You should fill the original title\nor the movie title."))

def change_rating_from_slider(self):
	rating = int(self.widgets['add']['rating_slider'].get_value())
	self.widgets['add']['image_rating'].show()
	try:
		rimage = int(str(self.config.get('rating_image')))
	except:
		rimage = 0
	if rimage:
		prefix = ''
	else:
		prefix = "meter"
	rating_file = "%s/%s0%d.png" % (self.locations['images'], prefix, rating)
	handler = self.widgets['add']['image_rating'].set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(rating_file))

def populate_with_results(self):
	m_id = None
	if self.founded_results_id:
		self.debug.show("self.founded:results_id: %s" % self.founded_results_id)
		m_id = self.founded_results_id
	else:
		self.founded_results_id = 0
		treeselection = self.widgets['results']['treeview'].get_selection()
		(tmp_model, tmp_iter) = treeselection.get_selected()
		m_id = tmp_model.get_value(tmp_iter, 0)
	self.hide_results()

	try:
		self.debug.show("m_id: %s" % m_id)
	except:
		self.debug.show("m_id: Bad UNICODE character")

	plugin_name = 'PluginMovie' + self.active_plugin
	plugin = __import__(plugin_name)
	self.movie = plugin.Plugin(m_id)
	self.movie.open_page(self.widgets['add']['window'])
	self.movie.parse_movie(self.config)
	if self.config.get('s_o_title'):
		self.widgets['add']['o_title'].set_text(gutils.convert_entities(self.movie.original_title))
	if self.config.get('s_title'):
		self.widgets['add']['title'].set_text(gutils.convert_entities(self.movie.title))
	if self.config.get('s_director'):
		self.widgets['add']['director'].set_text(gutils.convert_entities(self.movie.director))
	if self.config.get('s_plot'):
		plot_buffer = self.widgets['add']['plot'].get_buffer()
		plot_buffer.set_text(gutils.convert_entities(self.movie.plot))
	if self.config.get('s_with'):
		cast_buffer = self.widgets['add']['cast'].get_buffer()
		cast_buffer.set_text(gutils.convert_entities(self.movie.with))
	if self.config.get('s_country'):
		self.widgets['add']['country'].set_text(gutils.convert_entities(self.movie.country))
	if self.config.get('s_genre'):
		self.widgets['add']['genre'].set_text(gutils.convert_entities(self.movie.genre))
	if self.config.get('s_classification'):
		self.widgets['add']['classification'].set_text(gutils.convert_entities(self.movie.classification))
	if self.config.get('s_studio'):
		self.widgets['add']['studio'].set_text(gutils.convert_entities(self.movie.studio))
	if self.config.get('s_o_site'):
		self.widgets['add']['o_site'].set_text(gutils.remove_accents(self.movie.site))
	if self.config.get('s_site'):
		self.widgets['add']['site'].set_text(gutils.remove_accents(self.movie.imdb))
	if self.config.get('s_trailer'):
		self.widgets['add']['trailer'].set_text(gutils.remove_accents(self.movie.trailer))
	if self.config.get('s_year'):
		self.widgets['add']['year'].set_text(self.movie.year)
	if self.config.get('s_notes'):
		notes_buffer = self.widgets['add']['notes'].get_buffer()
		notes_buffer.set_text(gutils.convert_entities(self.movie.notes))
	if self.config.get('s_runtime'):
		self.widgets['add']['runtime'].set_text(self.movie.running_time)
	if self.config.get('s_rating') and self.movie.rating:
		self.widgets['add']['rating_slider'].set_value(float(self.movie.rating))
	# poster
	if self.windows:
		temp_dir = "C:\\windows\\temp\\"
	else:
		temp_dir = "/tmp/"
	if self.config.get('s_image'):
		if self.movie.picture != '':
			image = os.path.join(temp_dir, self.movie.picture)
			try:
				handler = self.Image.set_from_file(image)
				pixbuf = self.Image.get_pixbuf()
				self.widgets['add']['picture'].set_from_pixbuf(pixbuf.scale_simple(100, 140, 3))
				self.widgets['add']['picture_name'].set_text(string.replace(self.movie.picture, ".jpg",''))
			except:
				image = os.path.join(self.locations['images'], "default.png")
				handler = self.Image.set_from_file(image)
				self.widgets['add']['picture'].set_from_pixbuf(self.Image.get_pixbuf())
		else:
			image = os.path.join(self.locations['images'], "default.png")
			handler = self.Image.set_from_file(image)
			Pixbuf = self.Image.get_pixbuf()
			self.widgets['add']['picture'].set_from_pixbuf(Pixbuf)

def show_websearch_results(self):
	total = self.founded_results_id = 0
	for g in self.search_movie.ids:
		if ( str(g) != '' ):
			total += 1
	if total > 1:
		self.widgets['results']['window'].show()
		self.widgets['results']['window'].set_keep_above(True)
		row = None	
		key = 0
		self.treemodel_results.clear()
		for row in self.search_movie.ids:
			if (str(row)!=''):
				title = str(self.search_movie.titles[key]).decode(self.search_movie.encode)
				myiter = self.treemodel_results.insert_before(None, None)
				self.treemodel_results.set_value(myiter, 0, str(row))
				self.treemodel_results.set_value(myiter, 1, title)
			key +=1
		self.widgets['results']['treeview'].show()
	elif total==1:
		self.widgets['results']['treeview'].set_cursor(total-1)
		for row in self.search_movie.ids:
			if ( str(row) != '' ):
				self.founded_results_id = str(row)
				populate_with_results(self)
	else:
		gutils.error(self.widgets['results']['window'], _("No results"), self.widgets['add']['window'])

def get_from_web(self):
	"""search the movie in web using the active plugin"""
	if len(self.widgets['add']['o_title'].get_text()) \
		or len(self.widgets['add']['title'].get_text()):
		option = gutils.on_combo_box_entry_changed_name(self.widgets['add']['source'])
		self.active_plugin = option
		plugin_name = 'PluginMovie%s' % option
		plugin = __import__(plugin_name)
		self.search_movie = plugin.SearchPlugin()
		if len(self.widgets['add']['o_title'].get_text()):
			self.search_movie.url = self.search_movie.original_url_search
			self.search_movie.title = \
				gutils.remove_accents(self.widgets['add']['o_title'].get_text(), 'utf-8')
		elif len(self.widgets['add']['title'].get_text()) \
			and not len(self.widgets['add']['o_title'].get_text()):
			self.search_movie.url = self.search_movie.translated_url_search
			self.search_movie.title = \
				gutils.remove_accents(self.widgets['add']['title'].get_text(), 'utf-8')
		self.search_movie.search(self.widgets['add']['window'])
		self.search_movie.get_searches()
		self.show_search_results(self.search_movie)
	else:
		gutils.error(self.widgets['results']['window'], \
			_("You should fill the original title\nor the movie title."))

def source_changed(self):
	option = gutils.on_combo_box_entry_changed_name(self.widgets['add']['source'])
	self.active_plugin = option
	plugin_name = 'PluginMovie' + option
	plugin = __import__(plugin_name)
	self.widgets['add']['plugin_desc'].set_text(plugin.plugin_name+"\n" \
		+plugin.plugin_description+"\n"+_("Url: ") \
		+plugin.plugin_url+"\n"+_("Language: ")+plugin.plugin_language)
	image = os.path.join(self.locations['images'], plugin_name + ".png")
	# if movie plugin logo exists lets use it
	if os.path.exists(image):
		handler = self.am_plugin_image.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(image))

def clone_movie(self):
	treeselection = self.widgets['treeview'].get_selection()
	(tmp_model, tmp_iter) = treeselection.get_selected()
	number = tmp_model.get_value(tmp_iter, 0)
	movie = self.db.Movie.get_by(number=number)

	if movie is None:
		return false

	next_number = gutils.find_next_available(self)
	new_image = str(movie.image) + '_' + str(next_number)
	
	# integer problem workaround
	if int(movie.seen)==1:
		seen = True
	else:
		seen = False
	new_movie = self.db.Movie()
	
	new_movie.cast = movie.cast
	new_movie.classification = movie.classification
	new_movie.color = movie.color
	new_movie.cond = movie.cond
	new_movie.country = movie.country
	new_movie.director = movie.director
	new_movie.genre = movie.genre
	new_movie.image = new_image
	new_movie.site = movie.site
	new_movie.layers = movie.layers
	new_movie.medium_id = movie.medium_id
	new_movie.number = next_number
	new_movie.media_num = movie.media_num
	new_movie.notes = movie.notes
	new_movie.o_title = movie.o_title
	new_movie.plot = movie.plot
	new_movie.rating = movie.rating
	new_movie.region = movie.region
	new_movie.runtime = movie.runtime
	new_movie.seen = seen
	new_movie.o_site = movie.o_site
	new_movie.studio = movie.studio
	new_movie.title = movie.title
	new_movie.trailer = movie.trailer
	new_movie.year = movie.year
	
	new_movie.tags = movie.tags
	new_movie.languages = movie.languages
	
	# save
	new_movie.save()
	new_movie.flush()

	# WARNING: loan problems (don't copy volume/collection data until resolved)

	tmp_dest = os.path.join(self.griffith_dir, "posters")
	if movie.image is not None:
		image_path = os.path.join(tmp_dest, str(movie.image)+".jpg")
		clone_path = os.path.join(tmp_dest, new_image+".jpg")
		# clone image
		shutil.copyfile(image_path, clone_path)
		image_path = clone_path
	else:
		if self.windows:
			image_path = "images/default.png"
		else:
			image_path = os.path.join(self.locations['images'], "default.png")
	handler = self.Image.set_from_file(image_path)

	#update statusbar
	self.total = self.total + 1
	self.total_filter = self.total
	self.count_statusbar()
	self.populate_treeview(self.db.Movie.select())
	self.widgets['treeview'].set_cursor(next_number-1)
	self.treeview_clicked()

# vim: fdm=marker
