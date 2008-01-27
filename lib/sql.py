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
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.exceptions import *
import os.path
import gutils
import gtk

class DBTable(object):#{{{
	def __repr__(self):
		return "%s:%s" % (self.__class__.__name__, self.name)
	def add_to_db(self):
		if self.name is None or len(self.name)==0:
			debug.show("%s: name can't be empty" % self.__class__.__name__)
			return False
		# check if achannel already exists
		if self.query.filter_by(name=self.name).first() is not None:
			debug.show("%s: '%s' already exists" % (self.__class__.__name__, self.name))
			return False
		debug.show("%s: adding '%s' to database..." % (self.__class__.__name__, self.name))
		self.save()
		try:
			self.flush()
		except exceptions.SQLError, e:
			debug.show("%s: add_to_db: %s" % (self.__class__.__name__, e))
			return False
		self.refresh()
		return True
	def remove_from_db(self):
		dbtable_id = self.__dict__[self.__class__.__name__.lower() + '_id']
		if dbtable_id<1:
			debug.show("%s: none selected => none removed" % self.__class__.__name__)
			return False
		tmp = None
		if hasattr(self,'movies'):
			tmp = getattr(self,'movies')
		elif hasattr(self,'movielangs'):
			tmp = getattr(self,'movielangs')
		if tmp and len(tmp)>0:
			gutils.warning(self, msg=_("This item is in use.\nOperation aborted!"))
			return False
		debug.show("%s: removing '%s' (id=%s) from database..."%(self.__class__.__name__, self.name, dbtable_id))
		self.delete()
		try:
			self.flush()
		except exceptions.SQLError, e:
			debug.show("%s: remove_from_db: %s" % (self.__class__.__name__, e))
			return False
		#self.refresh()
		return True
	def update_in_db(self):
		dbtable_id = self.__dict__[self.__class__.__name__.lower() + '_id']
		if dbtable_id<1:
			debug.show("%s: none selected => none updated" % self.__class__.__name__)
			return False
		if self.name is None or len(self.name)==0:
			debug.show("%s: name can't be empty" % self.__class__.__name__)
			return False
		tmp = self.query.filter_by(name=self.name).first()
		if tmp is not None and tmp is not self:
			gutils.warning(self, msg=_("This name is already in use!"))
			return False
		self.update()
		try:
			self.flush()
		except exceptions.SQLError, e:
			debug.show("%s: update_in_db: %s" % (self.__class__.__name__, e))
			return False
		self.refresh()
		return True#}}}

class GriffithSQL:
	version = 2	# database format version, incrase after any changes in data structures
	metadata = None
	class Configuration(object):
		def __repr__(self):
			return "Config:%s=%s" % (self.param, self.value)
	class AChannel(DBTable):
		pass
	class ACodec(DBTable):
		pass
	class Collection(DBTable):
		pass
	class Lang(DBTable):
		pass
	class Medium(DBTable):
		pass
	class MovieLang(object):
		def __repr__(self):
			return "MovieLang:%s-%s (Type:%s ACodec:%s AChannel:%s SubFormat:%s)" % \
				(self.movie_id, self.lang_id, self.type, self.acodec_id, self.achannel_id, self.subformat_id)
	class MovieTag(object):
		def __repr__(self):
			return "MovieTag:%s-%s" % (self.movie_id, self.tag_id)
	class Person(DBTable):
		pass
	class SubFormat(DBTable):
		pass
	class Tag(DBTable):
		def remove_from_db(self):
			if len(self.movietags) > 0:
				gutils.warning(self, msg=_("This item is in use.\nOperation aborted!"))
				return False
			return DBTable.remove_from_db(self)
	class VCodec(DBTable):
		pass
	class Volume(DBTable):
		pass
	class Loan(object):#{{{
		def __repr__(self):
			return "Loan:%s (movie:%s person:%s)" % (self.loan_id, self.movie_id, self.person_id)
		def __setitem__(self, key, value):
			if key == 'movie_id' and value:
				if GriffithSQL.Movie.query.filter_by(movie_id=value).first() is None:
					raise ValueError('wrong movie_id')
			elif key == 'person_id' and value:
				if GriffithSQL.Person.query.filter_by(person_id=value).first() is None:
					raise ValueError('wrong movie_id')
			self[key] = value
		def _validate(self):
			if self.movie_id is None:
				raise ValueError('movie_id is not set')
			if self.person_id is None:
				raise ValueError('person_id is not set')
			if self.movie is None:
				self.movie = GriffithSQL.Movie.query.filter_by(movie_id=self.movie_id).first()
				if self.movie is None:
					raise ValueError('wrong movie_id')
			if self.person is None:
				self.person = GriffithSQL.Person.query.filter_by(person_id=self.person_id).first()
				if self.person is None:
					raise ValueError('wrong person_id')
			if self.collection_id>0 and self.collection is None:
				self.collection = GriffithSQL.Collection.query.filter_by(collection_id=self.collection_id).first()
				if self.collection is None:
					raise ValueError('wrong collection_id')
			if self.volume_id>0 and self.volume is None:
				self.volume = GriffithSQL.Volume.query.filter_by(volume_id=self.volume_id).first()
				if self.volume is None:
					raise ValueError('wrong volume_id')
			return True
		def set_loaned(self):
			"""
			Set loaned=True for all movies in volume/collection and for movie itself
			Set loan's date to today's date
			"""
			self._validate()

			if self.collection is not None:
				self.movie.mapper.mapped_table.update(self.movie.c.collection_id==self.collection_id).execute(loaned=True)
				self.collection.loaned = True
				self.collection.update()
			if self.volume is not None:
				self.movie.mapper.mapped_table.update(self.movie.c.volume_id==self.volume_id).execute(loaned=True)
				self.volume.loaned = True
				self.volume.update()
			if self.movie is None:
				self.movie = Movie.query.filter_by(movie_id=self.movie_id).first()
			self.movie.loaned = True
			self.movie.update()
			if self.date is None:
				self.date = func.current_date()	# update loan date
			self.return_date = None
			self.save_or_update()
			try:
				self.mapper.get_session().flush()
				self.refresh()
			except exceptions.SQLError, e:
				debug.show("set_loaned: %s" % e)
				return False
			return True
		def set_returned(self):
			"""
			Set loaned=False for all movies in volume/collection and for movie itself.
			Set return_date to today's date
			"""
			self._validate()
			if self.collection is not None:
				self.movie.mapper.mapped_table.update(self.movie.c.collection_id==self.collection_id).execute(loaned=False)
				self.collection.loaned = False
				self.collection.update()
			if self.volume_id is not None:
				self.movie.mapper.mapped_table.update(self.movie.c.volume_id==self.volume_id).execute(loaned=False)
				self.volume.loaned = False
				self.volume.update()
			self.movie.loaned = False
			self.movie.update()
			if self.return_date is None:
				self.return_date = func.current_date()
			self.save_or_update()
			try:
				self.mapper.get_session().flush()
				self.refresh()
			except exceptions.SQLError, e:
				debug.show("set_returned: %s" % e)
				return False
			return True
			#}}}
	class Movie(object):#{{{
		def __repr__(self):
			return "Movie:%s (number=%s)" % (self.movie_id, self.number)
		def __setitem__(self, key, value):
			setattr(self,key,value)
		def __getitem__(self, key):
			return getattr(self,key)
		def has_key(self, key):
			if key in ('volume','collection','medium','vcodec','loans','tags','languages','lectors','dubbings','subtitles'):
				return True
			else:
				return self.c.has_key(key)
		def remove_from_db(self):
			if self.loaned == True:
				debug.show("You can't remove loaned movie!")
				return False
			self.delete()
			try:
				self.flush()
			except exceptions.SQLError, e:
				debug.show("remove_from_db: %s" % e)
				return False
			return True
		def update_in_db(self, t_movies=None):
			if self.movie_id < 1:
				raise ValueError('movie_id is not set')
			if t_movies is not None:
				self.languages.clear()
				self.tags.clear()
				#self.mapper.mapped_table.update(self.c.movie_id==t_movies['movie_id']).execute(t_movies)
			return self.add_to_db(t_movies)
		def add_to_db(self, t_movies=None):
			if t_movies is not None:
				t_tags = t_languages = None
				if t_movies.has_key('tags'):
					t_tags = t_movies.pop('tags')
				if t_movies.has_key('languages'):
					t_languages = t_movies.pop('languages')
				for i in self.c.keys():
					if t_movies.has_key(i):
						self[i] = t_movies[i]
				# languages
				if t_languages is not None:
					for lang in t_languages:
						if lang[0]>0:
							ml = GriffithSQL.MovieLang(lang_id=lang[0], type=lang[1],
								acodec_id=lang[2], achannel_id=lang[3], subformat_id=lang[4])
							self.languages.append(ml)
				# tags
				if t_tags is not None:
					for tag in t_tags.keys():
						self.tags.append(GriffithSQL.Tag(tag_id=tag))
			self.update()
			try:
				self.flush()
			except exceptions.SQLError, e:
				debug.show("add_to_db: %s" % e)
				if e.args[0][:16] == '(IntegrityError)':
					gutils.error(None, _('Column "%s" is not unique') % _('Number'))
				return False
			self.refresh()
			return True
		#}}}

	def __init__(self, config, gdebug, griffith_dir):
		from sqlalchemy.orm import scoped_session, sessionmaker
		Session = scoped_session(sessionmaker(autoflush=True, transactional=True))
		mapper = Session.mapper
		global debug
		debug = gdebug
		if config.get('type', None, section='database') is None:
			config.set('type', 'sqlite', section='database')

		if config.get('type', 'sqlite', section='database') != 'sqlite':
			if config.get('host', None, section='database') is None:
				config.set('host', '127.0.0.1', section='database')
			if config.get('user', None, section='database') is None:
				config.set('user', 'griffith', section='database')
			if config.get('passwd', None, section='database') is None:
				config.set('passwd', 'gRiFiTh', section='database')
			if config.get('name', None, section='database') is None:
				config.set('name', 'griffith', section='database')

		# connect to database --------------------------------------{{{
		if config.get('type', section='database') == 'sqlite':
			url = "sqlite:///%s" % os.path.join(griffith_dir, config.get('name', 'griffith', section='database') + '.db')
		elif config.get('type', section='database') == 'postgres':
			if config.get('port', 0, section='database')==0:
				config.set('port', 5432, section='database')
			url = "postgres://%s:%s@%s:%d/%s" % (
				config.get('user', section='database'),
				config.get('passwd', section='database'),
				config.get('host', section='database'),
				int(config.get('port', section='database')),
				config.get('name', section='database'))
		elif config.get('type', section='database') == 'mysql':
			if config.get('port', 0, section='database')==0:
				config.set('port', 3306, section='database')
			url = "mysql://%s:%s@%s:%d/%s" % (
				config.get('user', section='database'),
				config.get('passwd', section='database'),
				config.get('host', section='database'),
				int(config.get('port', section='database')),
				config.get('name', section='database'))
		elif config.get('type', section='database') == 'mssql':
			if config.get('port', 0, section='database')==0:
				config.set('port', 1433, section='database')
			# use_scope_identity=0 have to be set as workaround for a sqlalchemy bug
			# but it is not guaranteed that the right identity value will be selected
			# because the select @@identity statement selects the very last id which
			# also can be a id from a trigger-insert or another user
			# sqlalchemy uses a wrong syntax. It has to select the id within the insert
			# statement: insert <table> (<columns>) values (<values>) select scope_identity()
			# (one statement !) After preparing and executing there should be a fetch
			# If it is executed as two separate statements the scope is lost after insert.
			url = "mssql://%s:%s@%s:%d/%s?use_scope_identity=0" % (
				config.get('user', section='database'),
				config.get('passwd', section='database'),
				config.get('host', section='database'),
				int(config.get('port', section='database')),
				config.get('name', section='database'))
		else:
			config.set('type', 'sqlite', section='database')
			url = "sqlite:///%s" % os.path.join(griffith_dir, config.get('name', 'griffith', section='database') + '.db')
		try:
			self.metadata = MetaData(url)
		except Exception, e:	# InvalidRequestError, ImportError
			debug.show("MetaData: %s" % e)
			config.set('type', 'sqlite', section='database')
			gutils.warning(self, "%s\n\n%s" % (_('Cannot connect to database.\nFalling back to SQLite.'), _('Please check debug output for more informations.')))
			self.metadata = MetaData("sqlite:///%s" % os.path.join(griffith_dir, config.get('name', 'griffith', section='database') + '.db'))

		# try to establish a db connection
		try:
			self.metadata.bind.connect()
		except Exception, e:
			debug.show("engine connection: %s" % e)
			gutils.error(self, _('Database connection failed.'))
			config.set('type', 'sqlite', section='database')
			url = "sqlite:///%s" % os.path.join(griffith_dir, 'griffith.db')
			self.metadata = MetaData(url)
			self.metadata.bind.connect()
		#}}}

		# prepare tables interface ---------------------------------{{{
		movies = Table('movies', self.metadata,
			Column('movie_id', Integer, primary_key = True),
			Column('number', Integer, nullable=False, unique=True),
			Column('collection_id', Integer, ForeignKey('collections.collection_id')),
			Column('volume_id', Integer, ForeignKey('volumes.volume_id')),
			Column('medium_id', Integer, ForeignKey('media.medium_id')),
			Column('vcodec_id', Integer, ForeignKey('vcodecs.vcodec_id')),
			Column('loaned', Boolean, nullable=False, default=False),
			Column('seen', Boolean, nullable=False, default=False),
			Column('rating', SmallInteger(2)),
			Column('color', SmallInteger),
			Column('cond', SmallInteger),	# MySQL will not accept name "condition"
			Column('layers', SmallInteger),
			Column('region', SmallInteger),
			Column('media_num', SmallInteger),
			Column('runtime', Integer),
			Column('year', Integer),
			Column('o_title', VARCHAR(255)),
			Column('title', VARCHAR(255)),
			Column('director', VARCHAR(255)),
			Column('o_site', VARCHAR(255)),
			Column('site', VARCHAR(255)),
			Column('trailer', VARCHAR(256)),
			Column('country', VARCHAR(128)),
			Column('genre', VARCHAR(128)),
			Column('image', VARCHAR(128)),
			Column('studio', VARCHAR(128)),
			Column('classification', VARCHAR(128)),
			Column('cast', TEXT),
			Column('plot', TEXT),
			Column('notes', TEXT))
		loans = Table('loans', self.metadata,
			Column('loan_id', Integer, primary_key=True),
			Column('person_id', Integer, ForeignKey('people.person_id'), nullable=False),
			Column('movie_id', Integer, ForeignKey('movies.movie_id'), nullable=False),
			Column('volume_id', Integer, ForeignKey('volumes.volume_id')),
			Column('collection_id', Integer, ForeignKey('collections.collection_id')),
			Column('date', Date, nullable=False, default=func.current_date()),
			Column('return_date', Date, nullable=True))
		people = Table('people', self.metadata,
			Column('person_id', Integer, primary_key=True),
			Column('name', VARCHAR(255), nullable=False, unique=True),
			Column('email', VARCHAR(128)),
			Column('phone', VARCHAR(64)))
		volumes = Table('volumes', self.metadata,
			Column('volume_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True),
			Column('loaned', Boolean, nullable=False, default=False))
		collections = Table('collections', self.metadata,
			Column('collection_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True),
			Column('loaned', Boolean, nullable=False, default=False))
		media = Table('media', self.metadata,
			Column('medium_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True))
		languages = Table('languages', self.metadata,
			Column('lang_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True))
		vcodecs = Table('vcodecs', self.metadata,
			Column('vcodec_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True))
		acodecs = Table('acodecs', self.metadata,
			Column('acodec_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True))
		achannels = Table('achannels', self.metadata,
			Column('achannel_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True))
		subformats = Table('subformats', self.metadata,
			Column('subformat_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True))
		tags = Table('tags', self.metadata,
			Column('tag_id', Integer, primary_key=True),
			Column('name', VARCHAR(64), nullable=False, unique=True))
		movie_lang = Table('movie_lang', self.metadata,
			Column('ml_id', Integer, primary_key=True),
			Column('type', SmallInteger), # 0: Original, 1:lector, 2:dubbing, 3:subtitle 
			Column('movie_id', Integer, ForeignKey('movies.movie_id'), nullable=False),
			Column('lang_id', Integer, ForeignKey('languages.lang_id'), nullable=False),
			Column('acodec_id', Integer, ForeignKey('acodecs.acodec_id')),
			Column('achannel_id', Integer, ForeignKey('achannels.achannel_id')),
			Column('subformat_id', Integer, ForeignKey('subformats.subformat_id')))
		movie_tag = Table('movie_tag', self.metadata,
			Column('mt_id', Integer, primary_key=True),
			Column('movie_id', Integer, ForeignKey('movies.movie_id')),
			Column('tag_id', Integer, ForeignKey('tags.tag_id')))
		configuration = Table('configuration', self.metadata,
			Column('param', VARCHAR(16), primary_key=True),
			Column('value', VARCHAR(128), nullable=False))#}}}

		# mappers -------------------------------------------------#{{{
		mapper(self.Configuration, configuration)
		mapper(self.Volume,volumes, properties={
			'movies': relation(self.Movie, backref='volume')})
		mapper(self.Collection, collections, properties={
			'movies': relation(self.Movie, backref='collection')})
		mapper(self.Medium, media, properties={
			'movies': relation(self.Movie, backref='medium')})
		mapper(self.VCodec, vcodecs, properties={
			'movies': relation(self.Movie, backref='vcodec')})
		mapper(self.Person, people, properties = {
			'loans'    : relation(self.Loan, backref='person', cascade='all, delete-orphan')})
		mapper(self.MovieLang, movie_lang, primary_key=[movie_lang.c.ml_id], properties = {
			'movie'    : relation(self.Movie, lazy=False),
			'language' : relation(self.Lang, lazy=False),
			'achannel' : relation(self.AChannel),
			'acodec'   : relation(self.ACodec),
			'subformat': relation(self.SubFormat)})
		mapper(self.ACodec, acodecs, properties={
			'movielangs': relation(self.MovieLang, lazy=False)})
		mapper(self.AChannel, achannels, properties={
			'movielangs': relation(self.MovieLang, lazy=False)})
		mapper(self.SubFormat, subformats, properties={
			'movielangs': relation(self.MovieLang, lazy=False)})
		mapper(self.Lang, languages, properties={
			'movielangs': relation(self.MovieLang, lazy=False)})
		mapper(self.MovieTag, movie_tag)
		mapper(self.Tag, tags, properties={'movietags': relation(self.MovieTag, backref='tag')})
		mapper(self.Loan, loans, properties = {
			'volume'    : relation(self.Volume),
			'collection': relation(self.Collection)})
		mapper(self.Movie, movies, order_by=movies.c.number , properties = {
			'loans'     : relation(self.Loan, backref='movie', cascade='all, delete-orphan'),
			#'tags'       : relation(self.Tag, cascade='all, delete-orphan', secondary=movie_tag,
			'tags'      : relation(self.Tag, secondary=movie_tag,
					primaryjoin=movies.c.movie_id==movie_tag.c.movie_id,
					secondaryjoin=movie_tag.c.tag_id==tags.c.tag_id),
			'languages' : relation(self.MovieLang, cascade='all, delete-orphan')})#}}}
		
		self.metadata.create_all()
		# check if database needs upgrade
		try:
			v = self.Configuration.query.filter_by(param='version').one()	# returns None if table exists && param ISNULL
		except SQLError, e:	# table doesn't exist
			debug.show("DB version: %s" % e)
			v = 0

		if v is not None and v>1:
			v = int(v.value)
		# FIXME:
#		if v < self.version:
#			from dbupgrade import upgrade_database
#			upgrade_database(self, v)

# for debugging (run: ipython sql.py)
if __name__ == '__main__':
	import sys
	import config, gdebug
	from initialize import locations, location_posters
	from gconsole import check_args, check_args_with_db
	
	class Tmp:
		def __init__(self):
			self.debug = gdebug.GriffithDebug(True)
	tmp = Tmp()
	check_args(tmp)
	locations(tmp)
	tmp.config = config.Config(os.path.join(tmp.locations['home'], 'griffith.cfg'))
	location_posters(tmp.locations, tmp.config)
	
	db = GriffithSQL(tmp.config, tmp.debug, tmp.locations['home'])
	check_args_with_db(tmp)
	
	print '\nGriffithSQL test drive\n======================'
	print "Engine: %s" % (db.metadata.bind.name)
	print 'Database object name: db\n'

# vim: fdm=marker
