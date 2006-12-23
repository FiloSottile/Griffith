# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2006 Vasco Nunes, Piotr Ożarowski
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

def clear(self):
	"""clears all fields in dialog"""
	set_details(self, {})
	self.widgets['add']['cb_only_empty'].set_active(False)

def add_movie(self, details={}):
	set_details(self, details)
	
	self.active_plugin = ''
	self.widgets['add']['add_button'].show()
	self.widgets['add']['add_close_button'].show()
	self.widgets['add']['clear_button'].show()
	self.widgets['add']['save_button'].hide()
	self.widgets['add']['window'].set_title(_('Add a new movie'))
	self.widgets['add']['window'].show()

def edit_movie(self, details={}):
	if not details.has_key('number'):
		details['number'] = gutils.find_next_available(self.db)
	set_details(self, details)
	self.widgets['add']['add_button'].hide()
	self.widgets['add']['add_close_button'].hide()
	self.widgets['add']['clear_button'].hide()
	self.widgets['add']['save_button'].show()
	self.widgets['add']['window'].set_title(_('Edit movie'))
	self.widgets['add']['window'].show()

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
		w['number'].set_value(int(gutils.find_next_available(self.db)))
	if item.has_key('title') and item['title']:
		w['title'].set_text(item['title'])
	if item.has_key('year') and item['year']:
		w['year'].set_value( gutils.digits_only(item['year'], 2100))
	else:
		w['year'].set_value(0)
	if item.has_key('runtime') and item['runtime']:
		w['runtime'].set_value( gutils.digits_only(item['runtime']))
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
	if item.has_key('genre') and item['genre']:
		w['genre'].set_text(item['genre'])
	else:
		w['genre'].set_text('')
	if item.has_key('color') and item['color']:
		w['color'].set_active( gutils.digits_only(item['color'], 3))
	else:
		w['color'].set_active( gutils.digits_only(self.config.get('color', 0), 3))
	if item.has_key('layers') and item['layers']:
		w['layers'].set_active( gutils.digits_only(item['layers'], 4))
	else:
		w['layers'].set_active( gutils.digits_only(self.config.get('layers', 0), 4))
	if item.has_key('region') and item['region']>=0:
			w['region'].set_active( gutils.digits_only(item['region'], 8))
	else:
		w['region'].set_active( gutils.digits_only(self.config.get('region', 0), 8))
	if item.has_key('cond') and item['cond']>=0:
		w['condition'].set_active( gutils.digits_only( item['cond'], 5) )
	else:
		w['condition'].set_active( gutils.digits_only( self.config.get('condition', 0), 5))
	if item.has_key('media_num') and item['media_num']:
		w['discs'].set_value( gutils.digits_only(item['media_num']))
	else:
		w['discs'].set_value(1)
	if item.has_key('rating') and item['rating']:
		w['rating_slider'].set_value( gutils.digits_only(item['rating'], 10) )
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
	else:
		pos = gutils.findKey(self.config.get('media', 0), self.media_ids)
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
		w['image'].set_text(item['image'])
		image_path = os.path.join(self.locations['posters'], "m_%s.jpg" % item['image'])
	else:
		w['image'].set_text('')
		image_path = os.path.join(self.locations['images'], 'default.png')
	if not os.path.isfile(image_path):
		image_path = os.path.join(self.locations['images'], 'default.png')
	w['picture'].set_from_file(image_path)
	
	w['notebook'].set_current_page(0)
	w['source'].set_active(self.d_plugin)
	w['o_title'].grab_focus()
	#}}}

def get_details(self): #{{{
	w = self.widgets['add']
	
	cast_buffer  = w['cast'].get_buffer()
	notes_buffer = w['notes'].get_buffer()
	plot_buffer  = w['plot'].get_buffer()
	
	t_movies = {
		'classification' : w['classification'].get_text(),
		'color'          : w['color'].get_active(),
		'cond'           : w['condition'].get_active(),
		'country'        : w['country'].get_text(),
		'director'       : w['director'].get_text(),
		'genre'          : w['genre'].get_text(),
		'image'          : w['image'].get_text(),
		'layers'         : w['layers'].get_active(),
		'media_num'      : w['discs'].get_value(),
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
		'year'           : w['year'].get_value(),
		'collection_id'  : w['collection'].get_active(),
		'medium_id'      : w['media'].get_active(),
		'volume_id'      : w['volume'].get_active(),
		'vcodec_id'      : w['vcodec'].get_active(),
		'cast'           : cast_buffer.get_text(cast_buffer.get_start_iter(),cast_buffer.get_end_iter()),
		'notes'          : notes_buffer.get_text(notes_buffer.get_start_iter(),notes_buffer.get_end_iter()),
		'plot'           : plot_buffer.get_text(plot_buffer.get_start_iter(),plot_buffer.get_end_iter()),
	}
	if self._am_movie_id is not None:
		t_movies['movie_id'] = self._am_movie_id
	
	if t_movies['collection_id'] > 0:
		t_movies['collection_id'] = self.collection_combo_ids[t_movies['collection_id']]
	else:
		t_movies['collection_id'] = None
	if t_movies['volume_id'] > 0:
		t_movies['volume_id'] = self.volume_combo_ids[t_movies['volume_id']]
	else:
		t_movies['volume_id'] = None
	if t_movies['medium_id'] > 0:
		t_movies['medium_id'] = self.media_ids[t_movies['medium_id']]
	else:
		t_movies['medium_id'] = None
	if t_movies['vcodec_id'] > 0:
		t_movies['vcodec_id'] = self.vcodecs_ids[t_movies['vcodec_id']]
	else:
		t_movies['vcodec_id'] = None
	
	if w['seen'].get_active():
		t_movies['seen'] = True
	else:
		t_movies['seen'] = False
	if t_movies['year'] < 1900:
		t_movies['year'] = None

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
	
	validate_details(t_movies)

	return t_movies	#}}}

def validate_details(t_movies, allow_only=None):
	for i in t_movies.keys():
		if t_movies[i] == '':
			t_movies[i] = None
	for i in ['color','cond','layers','region', 'media', 'vcodec', 'rating']:
		if t_movies.has_key(i) and t_movies[i] < 1:
			t_movies[i] = None
	for i in ['volume_id','collection_id', 'runtime']:
		if t_movies.has_key(i) and (t_movies[i] is None or int(t_movies[i]) == 0):
			t_movies[i] = None
	if allow_only is not None:
		for i in t_movies:
			if not i in allow_only:
				t_movies.pop(i)

def update_movie(self):
	movie = self.db.Movie.get_by(movie_id=self._movie_id)
	if movie is None: # movie was deleted in the meantime
		return add_movie_db(self, True)
	old_image = movie.image
	details = get_details(self)
	if movie.update_in_db(details):
		treeselection = self.widgets['treeview'].get_selection()
		(tmp_model, tmp_iter) = treeselection.get_selected()
		
		if details['image'] and details['image'] != old_image:
			# TODO: fetch poster from amazon / load from disk
			image_path = os.path.join(self.locations['temp'], "poster_%s.jpg" % details['image'])
			if os.path.isfile(image_path):
				# delete old image
				import delete
				delete.delete_poster(self, old_image)
				new_image_path = os.path.join(self.locations['posters'], "%s.jpg" % details['image'])
				shutil.move(image_path, new_image_path)
				#lets make the thumbnail and medium image from poster for future use
				gutils.make_thumbnail(self, "%s.jpg"%details['image'])
				gutils.make_medium_image(self, "%s.jpg"%details['image'])
				# update thumbnail in main list
				handler = self.Image.set_from_file(new_image_path)
				pixbuf = self.Image.get_pixbuf()
				tmp_model.set_value(tmp_iter,1, pixbuf.scale_simple(30,40,3))
		# update main treelist
		tmp_model.set_value(tmp_iter,0,'%004d' % int(movie.number))
		tmp_model.set_value(tmp_iter,2, movie.o_title)
		tmp_model.set_value(tmp_iter,3,	movie.title)
		tmp_model.set_value(tmp_iter,4, movie.director)
		# close add window
		self.widgets['add']['window'].hide()
		# refresh
		self.treeview_clicked()
		self.update_statusbar(_('Movie information has been updated'))

def add_movie_db(self, close):
	details = get_details(self)
	if not details['o_title'] and not details['title']:
		gutils.error(self.widgets['results']['window'], _("You should fill the original title\nor the movie title."), parent=self.widgets['add']['window'])
		return False

	if details['o_title']:
		tmp_movie = self.db.Movie.get_by(o_title=details['o_title'])
		if tmp_movie is not None:
			response = gutils.question(self, msg=_('Movie with that title already exists, are you sure you want to add?'), cancel=0, parent=self.widgets['add']['window'])
			if response == gtk.RESPONSE_NO:
				return False
	if details['title']:
		tmp_movie = self.db.Movie.get_by(title=details['title'])
		if tmp_movie is not None:
			response = gutils.question(self, msg=_('Movie with that title already exists, are you sure you want to add?'), cancel=0, parent=self.widgets['add']['window'])
			if response == gtk.RESPONSE_NO:
				return False

	movie = self.db.Movie()
	if not movie.add_to_db(details):
		return False

	# lets move poster from tmp to posters dir
	tmp_dest = self.locations['posters']

	image_path = ''
	if details['image']:
		tmp_image_path = os.path.join(self.locations['temp'], "poster_%s.jpg" % details['image'])
		if os.path.isfile(tmp_image_path):
			image_path = os.path.join(tmp_dest, "%s.jpg" % details['image'])
			shutil.move(tmp_image_path, image_path)
			#lets make the thumbnail and medium image from poster for future use
			gutils.make_thumbnail(self, "%s.jpg"%details['image'])
			gutils.make_medium_image(self, "%s.jpg"%details['image'])

	rows = len(self.treemodel)
	if rows>0:
		insert_after = self.treemodel.get_iter(rows-1)	# last
	else:
		insert_after = None
	myiter = self.treemodel.insert_after(None, insert_after)

	if not os.path.isfile(image_path):
		image_path = os.path.join(self.locations['images'], 'default.png')
	handler = self.Image.set_from_file(image_path)
	pixbuf = self.Image.get_pixbuf()
	self.treemodel.set_value(myiter, 0, '%004d' % details['number'])
	self.treemodel.set_value(myiter, 1, pixbuf.scale_simple(30,40,3))
	self.treemodel.set_value(myiter, 2, details['o_title'])
	self.treemodel.set_value(myiter, 3, details['title'])
	self.treemodel.set_value(myiter, 4, details['director'])
	#update statusbar
	self.total += 1
	self.count_statusbar()
	#select new entry from main treelist
	self.widgets['treeview'].get_selection().select_iter(myiter)
	self.treeview_clicked()
	clear(self)

	if close:
		self.hide_add_window()

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
	w = self.widgets['add']
	m_id = None
	if self.founded_results_id:
		self.debug.show("self.founded:results_id: %s" % self.founded_results_id)
		m_id = self.founded_results_id
	else:
		self.founded_results_id = 0
		treeselection = self.widgets['results']['treeview'].get_selection()
		(tmp_model, tmp_iter) = treeselection.get_selected()
		m_id = tmp_model.get_value(tmp_iter, 0)
	
	self.treemodel_results.clear()
	self.widgets['results']['window'].hide()

	plugin_name = 'PluginMovie' + self.active_plugin
	plugin = __import__(plugin_name)
	self.movie = plugin.Plugin(m_id)
	self.movie.locations = self.locations
	
	fields_to_fetch = ['o_title', 'title', 'director', 'plot', 'cast', 'country', 'genre',
				'classification', 'studio', 'o_site', 'site', 'trailer', 'year',
				'notes', 'runtime', 'image', 'rating']
	# remove fields that user doesn't want to fetch: (see preferences window)
	fields_to_fetch = [ i for i in fields_to_fetch if self.config.get("s_%s" % i, True) ]

	if w['cb_only_empty'].get_active(): # only empty fields
		details = get_details(self)
		fields_to_fetch = [ i for i in fields_to_fetch if details[i] is None ]
	self.movie.fields_to_fetch = fields_to_fetch
	
	self.movie.open_page(w['window'])
	self.movie.parse_movie()

	if 'year' in fields_to_fetch:
		w['year'].set_value(int(self.movie.year))
		fields_to_fetch.pop(fields_to_fetch.index('year'))
	if 'runtime' in fields_to_fetch:
		w['runtime'].set_value(int(self.movie.runtime))
		fields_to_fetch.pop(fields_to_fetch.index('runtime'))
	if 'cast' in fields_to_fetch:
		cast_buffer = w['cast'].get_buffer()
		cast_buffer.set_text(gutils.convert_entities(self.movie.cast))
		fields_to_fetch.pop(fields_to_fetch.index('cast'))
	if 'plot' in fields_to_fetch:
		plot_buffer = w['plot'].get_buffer()
		plot_buffer.set_text(gutils.convert_entities(self.movie.plot))
		fields_to_fetch.pop(fields_to_fetch.index('plot'))
	if 'notes' in fields_to_fetch:
		notes_buffer = w['notes'].get_buffer()
		notes_buffer.set_text(gutils.convert_entities(self.movie.notes))
		fields_to_fetch.pop(fields_to_fetch.index('notes'))
	if 'rating' in fields_to_fetch:
		if self.movie.rating:
			w['rating_slider'].set_value(float(self.movie.rating))
		fields_to_fetch.pop(fields_to_fetch.index('rating'))
	# poster
	if 'image' in fields_to_fetch:
		if self.movie.image:
			image = os.path.join(self.locations['temp'], "poster_%s.jpg" % self.movie.image)
			try:
				handler = self.Image.set_from_file(image)
				pixbuf = self.Image.get_pixbuf()
				w['picture'].set_from_pixbuf(pixbuf.scale_simple(100, 140, 3))
				w['image'].set_text(self.movie.image)
			except:
				image = os.path.join(self.locations['images'], 'default.png')
				handler = self.Image.set_from_file(image)
				w['picture'].set_from_pixbuf(self.Image.get_pixbuf())
		else:
			image = os.path.join(self.locations['images'], 'default.png')
			handler = self.Image.set_from_file(image)
			Pixbuf = self.Image.get_pixbuf()
			w['picture'].set_from_pixbuf(Pixbuf)
		fields_to_fetch.pop(fields_to_fetch.index('image'))
	# other fields
	for i in fields_to_fetch:
		w[i].set_text(gutils.convert_entities(self.movie[i]))

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
	title = self.widgets['add']['title'].get_text()
	o_title = self.widgets['add']['o_title'].get_text()

	if o_title or title:
		option = gutils.on_combo_box_entry_changed_name(self.widgets['add']['source'])
		self.active_plugin = option
		plugin_name = 'PluginMovie%s' % option
		plugin = __import__(plugin_name)
		self.search_movie = plugin.SearchPlugin()
		if o_title:
			self.search_movie.url = self.search_movie.original_url_search
			self.search_movie.title = gutils.remove_accents(o_title, 'utf-8')
		elif title:
			self.search_movie.url = self.search_movie.translated_url_search
			self.search_movie.title = gutils.remove_accents(title, 'utf-8')
		self.search_movie.search(self.widgets['add']['window'])
		self.search_movie.get_searches()
		if len(self.search_movie.ids) == 1 and o_title and title:
			self.search_movie.url = self.search_movie.translated_url_search
			self.search_movie.title = gutils.remove_accents(title, 'utf-8')
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
	if tmp_iter is None:
		return False
	number = tmp_model.get_value(tmp_iter, 0)
	movie = self.db.Movie.get_by(number=number)

	if movie is None:
		return False

	next_number = gutils.find_next_available(self.db)
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

	tmp_dest = self.locations['posters']
	if movie.image is not None:
		image_path = os.path.join(tmp_dest, str(movie.image)+".jpg")
		clone_path = os.path.join(tmp_dest, new_image+".jpg")
		# clone image
		shutil.copyfile(image_path, clone_path)
		image_path = clone_path
	else:
		image_path = os.path.join(self.locations['images'], "default.png")
	handler = self.Image.set_from_file(image_path)

	#update statusbar
	self.total = self.total + 1
	self.count_statusbar()
	self.populate_treeview()
	self.widgets['treeview'].set_cursor(next_number-1)
	self.treeview_clicked()

# vim: fdm=marker
