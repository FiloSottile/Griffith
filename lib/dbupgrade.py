# -*- coding: UTF-8 -*-
# vim: fdm=marker

__revision__ = '$Id$'

# Copyright (c) 2005-2009 Vasco Nunes, Piotr Ożarowski
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

import logging
import os.path

from sqlalchemy import *
from sqlalchemy.exc import *

import db
import gutils

log = logging.getLogger("Griffith")


@gutils.popup_message(_('Upgrading database...'))
def upgrade_database(self, version, config):
    """Create new db or update existing one to current format"""
    b = self.engine
    if version == 0 or version is None:
        log.info('Creating new database...')
        # version is 0 or none only for new databases
        db.metadata.create_all(b)
        db.tables.configuration.insert(bind=b).execute(param=u'version', value=unicode(self.version))
        db.tables.media.insert(bind=b).execute(name=u'DVD')
        db.tables.media.insert(bind=b).execute(name=u'DVD-R')
        db.tables.media.insert(bind=b).execute(name=u'DVD-RW')
        db.tables.media.insert(bind=b).execute(name=u'DVD+R')
        db.tables.media.insert(bind=b).execute(name=u'DVD+RW')
        db.tables.media.insert(bind=b).execute(name=u'DVD-RAM')
        db.tables.media.insert(bind=b).execute(name=u'CD')
        db.tables.media.insert(bind=b).execute(name=u'CD-RW')
        db.tables.media.insert(bind=b).execute(name=u'VCD')
        db.tables.media.insert(bind=b).execute(name=u'SVCD')
        db.tables.media.insert(bind=b).execute(name=u'VHS')
        db.tables.media.insert(bind=b).execute(name=u'BETACAM')
        db.tables.media.insert(bind=b).execute(name=u'LaserDisc')
        db.tables.media.insert(bind=b).execute(name=u'HD DVD')
        db.tables.media.insert(bind=b).execute(name=u'Blu-ray')
        db.tables.ratios.insert(bind=b).execute(name=u'16:9')
        db.tables.ratios.insert(bind=b).execute(name=u'16:10')
        db.tables.ratios.insert(bind=b).execute(name=u'4:3')
        db.tables.acodecs.insert(bind=b).execute(name=u'AC-3 Dolby audio')
        db.tables.acodecs.insert(bind=b).execute(name=u'OGG')
        db.tables.acodecs.insert(bind=b).execute(name=u'MP3')
        db.tables.acodecs.insert(bind=b).execute(name=u'MPEG-1')
        db.tables.acodecs.insert(bind=b).execute(name=u'MPEG-2')
        db.tables.acodecs.insert(bind=b).execute(name=u'AAC')
        db.tables.acodecs.insert(bind=b).execute(name=u'Windows Media Audio')
        db.tables.vcodecs.insert(bind=b).execute(name=u'MPEG-1')
        db.tables.vcodecs.insert(bind=b).execute(name=u'MPEG-2')
        db.tables.vcodecs.insert(bind=b).execute(name=u'XviD')
        db.tables.vcodecs.insert(bind=b).execute(name=u'DivX')
        db.tables.vcodecs.insert(bind=b).execute(name=u'H.264')
        db.tables.vcodecs.insert(bind=b).execute(name=u'RealVideo')
        db.tables.vcodecs.insert(bind=b).execute(name=u'QuickTime')
        db.tables.vcodecs.insert(bind=b).execute(name=u'Windows Media Video')
        db.tables.achannels.insert(bind=b).execute(name=u'mono')
        db.tables.achannels.insert(bind=b).execute(name=u'stereo')
        db.tables.achannels.insert(bind=b).execute(name=u'5.1')
        db.tables.achannels.insert(bind=b).execute(name=u'7.1')
        db.tables.subformats.insert(bind=b).execute(name=u'DVD VOB')
        db.tables.subformats.insert(bind=b).execute(name=u'MPL2 (.txt)')
        db.tables.subformats.insert(bind=b).execute(name=u'MicroDVD (.sub)')
        db.tables.subformats.insert(bind=b).execute(name=u'SubRip (.srt)')
        db.tables.subformats.insert(bind=b).execute(name=u'SubViewer2 (.sub)')
        db.tables.subformats.insert(bind=b).execute(name=u'Sub Station Alpha (.ssa)')
        db.tables.subformats.insert(bind=b).execute(name=u'Advanced Sub Station Alpha (.ssa)')
        db.tables.languages.insert(bind=b).execute(name=_('Brazilian Portuguese'))
        db.tables.languages.insert(bind=b).execute(name=_('Bulgarian'))
        db.tables.languages.insert(bind=b).execute(name=_('Catalan'))
        db.tables.languages.insert(bind=b).execute(name=_('Czech'))
        db.tables.languages.insert(bind=b).execute(name=_('Danish'))
        db.tables.languages.insert(bind=b).execute(name=_('Dutch'))
        db.tables.languages.insert(bind=b).execute(name=_('English'))
        db.tables.languages.insert(bind=b).execute(name=_('Estonian'))
        db.tables.languages.insert(bind=b).execute(name=_('French'))
        db.tables.languages.insert(bind=b).execute(name=_('German'))
        db.tables.languages.insert(bind=b).execute(name=_('Greek'))
        db.tables.languages.insert(bind=b).execute(name=_('Hungarian'))
        db.tables.languages.insert(bind=b).execute(name=_('Indonesian'))
        db.tables.languages.insert(bind=b).execute(name=_('Italian'))
        db.tables.languages.insert(bind=b).execute(name=_('Japanese'))
        db.tables.languages.insert(bind=b).execute(name=_('Korean'))
        db.tables.languages.insert(bind=b).execute(name=_('Norwegian Bokmal'))
        db.tables.languages.insert(bind=b).execute(name=_('Occitan'))
        db.tables.languages.insert(bind=b).execute(name=_('Pashto'))
        db.tables.languages.insert(bind=b).execute(name=_('Polish'))
        db.tables.languages.insert(bind=b).execute(name=_('Portuguese'))
        db.tables.languages.insert(bind=b).execute(name=_('Russian'))
        db.tables.languages.insert(bind=b).execute(name=_('Simplified Chinese'))
        db.tables.languages.insert(bind=b).execute(name=_('Slovak'))
        db.tables.languages.insert(bind=b).execute(name=_('Spanish'))
        db.tables.languages.insert(bind=b).execute(name=_('Swedish'))
        db.tables.languages.insert(bind=b).execute(name=_('Turkish'))
        db.tables.tags.insert(bind=b).execute(name=_('Favourite'))
        db.tables.tags.insert(bind=b).execute(name=_('Buy me'))
        return True # upgrade process finished
    #
    # next steps are only for existing databases with an outdated structure
    # not for new created databases
    #
    if version == 1: # fix changes between v1 and v2
        version += 1
        log.info("Upgrading database to version %d...", version)
        b.execute("UPDATE loans SET return_date='2007-01-01' WHERE return_date='None';")
        db_version = self.session.query(db.Configuration).filter_by(param=u'version').one()
        db_version.value = unicode(version)
        self.session.add(db_version)
        self.session.commit()
    if version == 2:    # fix changes between v2 and v3
        #e_type = self.session.bind.engine.dialect.name
        e_type = self.session.bind.name
        version += 1
        log.info("Upgrading database to version %d...", version)

        # create new table
        db.tables.posters.create(checkfirst=True, bind=b)
        db.tables.filters.create(checkfirst=True, bind=b)
        db.tables.ratios.create(checkfirst=True, bind=b)
        try:
            db.tables.ratios.insert(bind=b).execute(name=u'16:9')
            db.tables.ratios.insert(bind=b).execute(name=u'4:3')
        except IntegrityError, e:
            # if the following conversion of the posters takes to long and the user
            # kills the application the database is in a undefined state which throughs that exception
            log.warn("Cannot add values because they exist already: %s", e)

        log.info('... adding new columns')
        # common SQL statements
        queries = {'poster_md5': 'ALTER TABLE movies ADD poster_md5 VARCHAR(32) NULL REFERENCES posters(md5sum);',
                   'ratio_id': 'ALTER TABLE movies ADD ratio_id INTEGER NULL REFERENCES ratios(ratio_id);',
                   'screenplay': 'ALTER TABLE movies ADD screenplay VARCHAR(256) NULL;',
                   'cameraman': 'ALTER TABLE movies ADD cameraman VARCHAR(256) NULL;'}
        # if needed some db specific SQL statements
        if e_type == 'mysql':
            pass
        elif e_type == 'mssql':
            pass
        for key, query in queries.items():
            try:
                self.session.bind.execute(query)
            except OperationalError, e:
                if e.message.find(b'(OperationalError) duplicate column name:') > -1:
                    log.warn("Cannot add '%s' column because it exists already: %s", key, e)
                    continue
                else:
                    log.error("Cannot add '%s' column: %s", key, e)
                    return False
            except Exception, e:
                log.error("Cannot add '%s' column: %s", key, e)
                return False

        log.info('... saving posters in database')
        posters_dir = get_old_posters_location(self.data_dir, config, clean_config=True)
        updated = {}
        movies_table = db.metadata.tables['movies']
        for movie in self.session.query(db.Movie.image).all():
            poster_file_name = os.path.join(posters_dir, "%s.jpg" % movie.image)
            if poster_file_name in updated:
                continue
            if os.path.isfile(poster_file_name):
                poster_md5 = gutils.md5sum(file(poster_file_name, 'rb'))
                poster = self.session.query(db.Poster).filter_by(md5sum=poster_md5).first()
                if not poster:
                    poster = db.Poster(md5sum=poster_md5, data=file(poster_file_name, 'rb').read())
                    self.session.add(poster)

                update_query = movies_table.update(movies_table.c.image == movie.image, {'poster_md5': poster_md5, 'image': None}, bind=b)
                # deactivating a 0.12 feature
                save_update_onupdated = movies_table.c['updated'].onupdate
                movies_table.c['updated'].onupdate = None

                try:
                    # yeah, we're commiting inside the loop,
                    # it slows down the process a lot, but at least we can skip buggy posters
                    update_query.execute()
                    self.session.commit()
                except Exception, e:
                    self.session.rollback()
                    log.error(e)
                else:
                    updated[poster_file_name] = True
                    try:
                        os.remove(poster_file_name)
                    except:
                        log.warn("cannot remove %s", poster_file_name)
                finally:
                    movies_table.c['updated'].onupdate = save_update_onupdated
            else:
                log.warn("file not found: %s", movie.image)
                update_query = movies_table.update(movies_table.c.image == movie.image, {'image': None}, bind=b)
                # deactivating a 0.12 feature
                save_update_onupdated = movies_table.c['updated'].onupdate
                movies_table.c['updated'].onupdate = None
                try:
                    update_query.execute()
                finally:
                    movies_table.c['updated'].onupdate = save_update_onupdated
                updated[poster_file_name] = True
        del updated

        db_version = self.session.query(db.Configuration).filter_by(param=u'version').one()
        db_version.value = unicode(version)
        self.session.add(db_version)
        self.session.commit()

    if version == 3:    # fix changes between v3 and v4
        version += 1
        log.info("Upgrading database to version %d...", version)

        log.info('... adding new columns')
        # common SQL statements
        queries = {'barcode': 'ALTER TABLE movies ADD barcode VARCHAR(32) NULL;',
                   'width': 'ALTER TABLE movies ADD width SMALLINT NULL;',
                   'height': 'ALTER TABLE movies ADD height SMALLINT NULL;'}

        for key, query in queries.items():
            try:
                self.session.bind.execute(query)
            except Exception, e:
                log.error("Cannot add '%s' column: %s", key, e)
                return False

        db_version = self.session.query(db.Configuration).filter_by(param=u'version').one()
        db_version.value = unicode(version)
        self.session.add(db_version)
        self.session.commit()

    if version == 4:    # fix changes between v4 and v5
        version += 1
        log.info("Upgrading database to version %d...", version)

        log.info('... deleting old filters')
        # new format, filters were introduced in -beta so we'll free to delete them without warning
        query = 'DELETE FROM filters;'
        self.session.bind.execute(query)

        db_version = self.session.query(db.Configuration).filter_by(param=u'version').one()
        db_version.value = unicode(version)
        self.session.add(db_version)
        self.session.commit()

    if version == 5:    # fix changes between v5 and v6
        version += 1
        log.info("Upgrading database to version %d...", version)
        
        # common SQL statements
        queries = {'created': 'ALTER TABLE movies ADD created DATETIME;',
                   'updated': 'ALTER TABLE movies ADD updated DATETIME;'}
        for key, query in queries.items():
            try:
                self.session.bind.execute(query)
            except Exception, e:
                log.error("Cannot add '%s' column: %s", key, e)
                return False

        db_version = self.session.query(db.Configuration).filter_by(param=u'version').one()
        db_version.value = unicode(version)
        self.session.add(db_version)
        self.session.commit()

    return True


# ---------------------------------------------------
# for Griffith <= 0.6.2 compatibility
# ---------------------------------------------------


def convert_from_old_db(config, source_file, destination_file, locations):    #{{{
    """
    convert .gri database into .bd one
    """

    log.info('Converting old database - it can take several minutes...')
    log.debug("Source file: %s", source_file)
    gutils.info(_("Griffith will now convert your database to the new format. This can take several minutes if you have a large database."))
    from sql import GriffithSQL
    from gutils import digits_only
    import os

    if not os.path.isfile(source_file):
        return False

    if 'home' not in locations:
        log.error("locations doesn't contain home path, cannot convert old database")
        return False

    if open(source_file).readline()[:47] == '** This file contains an SQLite 2.1 database **':
        log.debug('SQLite 2.1 detected')
        try:
            import sqlite
        except ImportError:
            log.error('Old DB conversion: please install pysqlite legacy (v1.0)')
            gutils.warning(_("Old DB conversion: please install pysqlite legacy (v1.0)"))
            return False
    else:
        try:    # Python 2.5
            from sqlite3 import dbapi2 as sqlite
        except ImportError: # Python < 2.5 - try to use pysqlite2
            from pysqlite2 import dbapi2 as sqlite

    if os.path.isfile(destination_file):
        # rename destination_file if it already exist
        i = 1
        while True:
            if os.path.isfile("%s_%s" % (destination_file, i)):
                i += 1
            else:
                break
        os.rename(destination_file, "%s_%s" % (destination_file, i))

    try:
        old_db = sqlite.connect(source_file)
    except sqlite.DatabaseError, e:
        if str(e) == 'file is encrypted or is not a database':
            print 'Your database is most probably in SQLite2 format, please convert it to SQLite3:'
            print '$ sqlite ~/.griffith/griffith.gri .dump | sqlite3 ~/.griffith/griffith.gri3'
            print '$ mv ~/.griffith/griffith.gri{,2}'
            print '$ mv ~/.griffith/griffith.gri{3,}'
            print 'or install pysqlite in version 1.0'
            gutils.warning(_("Your database is most probably in SQLite2 format, please convert it to SQLite3"))
        else:
            raise
        return False

    old_cursor = old_db.cursor()

    # fix old database
    old_cursor.execute('PRAGMA encoding = "UTF-8";')
    old_cursor.execute("UPDATE movies SET media = '1' WHERE media = 'DVD';")
    old_cursor.execute("UPDATE movies SET media = '2' WHERE media = 'DVD-R';")
    old_cursor.execute("UPDATE movies SET media = '3' WHERE media = 'DVD-RW';")
    old_cursor.execute("UPDATE movies SET media = '4' WHERE media = 'DVD+R';")
    old_cursor.execute("UPDATE movies SET media = '5' WHERE media = 'DVD+RW';")
    old_cursor.execute("UPDATE movies SET media = '6' WHERE media = 'DVD-RAM';")
    old_cursor.execute("UPDATE movies SET media = '7' WHERE media = 'DivX';")
    old_cursor.execute("UPDATE movies SET media = '7' WHERE media = 'DIVX';")
    old_cursor.execute("UPDATE movies SET media = '7' WHERE media = 'XviD';")
    old_cursor.execute("UPDATE movies SET media = '7' WHERE media = 'XVID';")
    old_cursor.execute("UPDATE movies SET media = '7' WHERE media = 'WMV';")
    old_cursor.execute("UPDATE movies SET media = '9' WHERE media = 'VCD';")
    old_cursor.execute("UPDATE movies SET media = '10' WHERE media = 'SVCD';     ")
    old_cursor.execute("UPDATE movies SET media = '11' WHERE media = 'VHS';")
    old_cursor.execute("UPDATE movies SET media = '12' WHERE media = 'BETACAM';")
    old_cursor.execute("UPDATE movies SET collection_id=0 WHERE collection_id<1")
    old_cursor.execute("UPDATE movies SET volume_id=0 WHERE volume_id<1")
    old_cursor.execute("UPDATE movies SET color=NULL WHERE color<1 OR color='' OR color>3")
    old_cursor.execute("UPDATE movies SET condition=NULL WHERE condition<0 OR condition='' OR condition>5")
    old_cursor.execute("UPDATE movies SET layers=NULL WHERE layers<0 OR layers='' OR layers>4")
    old_cursor.execute("UPDATE movies SET region=NULL WHERE region='' OR region=2 OR region<0 OR region>8")
    old_cursor.execute("UPDATE movies SET year=NULL WHERE year<1900 or year>2007")
    old_cursor.execute("UPDATE movies SET rating = 0 WHERE rating NOT IN (0,1,2,3,4,5,6,7,8,9,10);") # rating>10 doesn't work with some DB
    old_cursor.execute("UPDATE movies SET runtime = NULL WHERE runtime > 10000;") # remove strings
    old_cursor.execute("UPDATE loans SET return_date=NULL WHERE return_date=''")
    old_cursor.execute("UPDATE loans SET return_date=NULL WHERE return_date='None'")
    old_cursor.execute("DELETE FROM loans WHERE date='' OR date ISNULL")
    old_cursor.execute("DELETE FROM volumes WHERE name = ''")
    old_cursor.execute("DELETE FROM volumes WHERE name = 'None'")
    old_cursor.execute("DELETE FROM collections WHERE name = ''")
    old_cursor.execute("DELETE FROM collections WHERE name = 'None'")
    old_cursor.execute("DELETE FROM languages WHERE name = ''")

    config.set('type', 'sqlite', section='database')
    config.set('file', 'griffith.db', section='database')
    config['posters'] = 'posters'
    config.set('color', 0, section='defaults')
    config.set('condition', 0, section='defaults')
    config.set('layers', 0, section='defaults')
    config.set('media', 0, section='defaults')
    config.set('region', 0, section='defaults')
    config.set('vcodec', 0, section='defaults')
    locations['posters'] = os.path.join(locations['home'], 'posters')
    new_db = GriffithSQL(config, locations['home'], fallback=False)

    # collections
    collection_mapper = {'': None, u'': None, 0: None, '0': None, -1: None, '-1': None}
    old_cursor.execute("SELECT id, name FROM collections;") # loaned status will be set later - buggy databases :-(
    for i in old_cursor.fetchall():
        o = db.Collection(name=i[1])
        try:
            new_db.session.add(o)
            new_db.session.commit()
        except Exception, e:
            log.error(e)
            continue
        collection_mapper[i[0]] = o.collection_id

    # volumes
    volume_mapper = {'': None, u'': None, 0: None, '0': None, -1: None, '-1': None}
    old_cursor.execute("SELECT id, name FROM volumes;") # loaned status will be set later - buggy databases :-(
    for i in old_cursor.fetchall():
        o = db.Volume(name=i[1])
        try:
            new_db.session.add(o)
            new_db.session.commit()
        except Exception, e:
            log.error(e)
            continue
        volume_mapper[i[0]] = o.volume_id

    # people
    person_mapper = {}
    old_cursor.execute("SELECT id, name, email, phone FROM people;")
    for i in old_cursor.fetchall():
        o = db.Person(name=i[1], email=i[2], phone=i[3])
        try:
            new_db.session.add(o)
            new_db.session.commit()
        except Exception, e:
            log.error(e)
            continue
        person_mapper[i[0]] = o.person_id

    # languages
    language_mapper = {'': None, u'': None, 0: None, '0': None, -1: None, '-1': None}
    old_cursor.execute("SELECT id, name FROM languages;")
    for i in old_cursor.fetchall():
        o = new_db.session.query(db.Lang).filter_by(name=i[1]).first()
        if o is not None:
            language_mapper[i[0]] = o.lang_id
        else:
            o = db.Lang(name=i[1])
            try:
                new_db.session.add(o)
                new_db.session.commit()
            except Exception, e:
                log.error(e)
                continue
            language_mapper[i[0]] = o.lang_id

    # media
    medium_mapper = {'': None, u'': None, 0: None, '0': None, -1: None, '-1': None}
    old_cursor.execute("SELECT id, name FROM media;")
    for i in old_cursor.fetchall():
        o = new_db.session.query(db.Medium).filter_by(name=i[1]).first()
        if o is not None:
            medium_mapper[i[0]] = o.medium_id
        else:
            o = db.Medium(name=i[1])
            try:
                new_db.session.add(o)
                new_db.session.commit()
            except Exception, e:
                log.error(e)
                continue
            medium_mapper[i[0]] = o.medium_id

    # tags
    tag_mapper = {}
    old_cursor.execute("SELECT id, name FROM tags;")
    for i in old_cursor.fetchall():
        o = new_db.session.query(db.Tag).filter_by(name=i[1]).first()
        if o is not None:
            tag_mapper[i[0]] = o.tag_id
        else:
            o = db.Tag(name=i[1])
            try:
                new_db.session.add(o)
                new_db.session.commit()
            except Exception, e:
                log.error(e)
                continue
            tag_mapper[i[0]] = o.tag_id

    # movies
    movie_mapper = {}
    old_cursor.execute("""
        SELECT id, volume_id, collection_id, original_title, title, director,
            number, image, plot, country, year, runtime, classification,
            genre, studio, site, imdb, actors, trailer, rating, loaned,
            media, num_media, obs, seen, region, condition, color, layers
        FROM movies ORDER BY number;""")
    for i in old_cursor.fetchall():
        o = db.Movie()
        o.number = digits_only(i[6])
        if i[1] in volume_mapper:
            o.volume_id = volume_mapper[i[1]]
        if i[2] in collection_mapper:
            o.collection_id = collection_mapper[i[2]]
        o.o_title = i[3][:255]
        o.title = i[4][:255]
        o.director = i[5][:255]
        o.image = i[7][:128]
        o.plot = i[8]
        o.country = i[9][:128]
        o.year = digits_only(i[10])
        o.runtime = digits_only(i[11])
        o.classification = i[12][:128]
        o.genre = i[13][:128]
        o.studio = i[14][:128]
        o.o_site = i[15][:255]
        o.site = i[16][:255]
        o.cast = i[17]
        o.trailer = i[18][:255]
        o.rating = digits_only(i[19])
        #o.loaned = bool(i[20]) # updated later
        if int(i[21]) in medium_mapper:
            o.medium_id = medium_mapper[int(i[21])]
        o.media_num = digits_only(i[22])
        o.notes = i[23]
        o.seen = bool(i[24])
        o.region = digits_only(i[25])
        o.cond = digits_only(i[26], 5)
        o.color = digits_only(i[27], 3)
        o.layers = digits_only(i[28], 4)

        try:
            new_db.session.add(o)
            new_db.session.commit()
        except Exception, e:
            log.error(e)
            continue
        movie_mapper[i[0]] = o.movie_id

    # movie tag
    old_cursor.execute("SELECT movie_id, tag_id FROM movie_tag WHERE movie_id IN (SELECT id FROM movies);")
    for i in old_cursor.fetchall():
        o = new_db.session.query(db.MovieTag).filter_by(movie_id=movie_mapper[i[0]], tag_id=tag_mapper[i[1]]).first()
        if o is None:
            m = new_db.session.query(db.Movie).filter_by(movie_id=movie_mapper[i[0]]).one()
            t = new_db.session.query(db.Tag).filter_by(tag_id=tag_mapper[i[1]]).one()
            m.tags.append(t)
            try:
                new_db.session.add(m)
                new_db.session.commit()
            except Exception, e:
                log.error(e)
                continue

    # movie lang
    old_cursor.execute("SELECT movie_id, lang_id, type FROM movie_lang WHERE movie_id IN (SELECT id FROM movies);")
    for i in old_cursor.fetchall():
        o = new_db.session.query(db.MovieLang).filter_by(movie_id=movie_mapper[i[0]], lang_id=language_mapper[i[1]], type=i[2]).first()
        if o is None:
            m = new_db.session.query(db.Movie).filter_by(movie_id=movie_mapper[i[0]]).one()
            l = db.MovieLang(lang_id=language_mapper[i[1]], type=i[2])
            m.languages.append(l)
            try:
                new_db.session.add(m)
                new_db.session.commit()
            except Exception, e:
                log.error(e)
                continue

    # loans
    old_cursor.execute("SELECT person_id, movie_id, volume_id, collection_id, date, return_date FROM loans;")
    for i in old_cursor.fetchall():
        vol = col = None
        not_returned = i[5] is None

        if int(i[2]) > 0:
            try:
                vol = new_db.session.query(db.Volume).filter_by(volume_id=volume_mapper[i[2]]).one()
            except Exception, e:
                log.error(e)
                continue
        if int(i[3]) > 0:
            try:
                col = new_db.session.query(db.Collection).filter_by(collection_id=collection_mapper[i[3]]).one()
            except Exception, e:
                log.error(e)
                continue
        if int(i[1]) == 0:
            if vol is not None and len(vol.movies) > 0:
                m = vol.movies[0]
            elif col is not None and len(col.movies) > 0:
                m = col.movies[0]
            else:
                log.warn("Cannot find associated movie for this loan (%s)" % i)
                continue
        else:
            try:
                m = new_db.session.query(db.Movie).filter_by(movie_id=movie_mapper[i[1]]).one()
            except Exception, e:
                log.error(e)
                continue

        l = db.Loan()
        l.person_id = person_mapper[i[0]]
        l.date = str(i[4])[:10]
        if not_returned:
            m.loaned = True
            l.return_date = None
        else:
            l.return_date = str(i[5])[:10]

        # update volume / collection status
        if int(i[2]) > 0:
            l.volume_id = volume_mapper[i[2]]
            if not_returned:
                vol.loaned = True
                vol.save()
        if int(i[3]) > 0:
            l.collection_id = collection_mapper[i[3]]
            if not_returned:
                col.loaned = True
                col.save()
        l.save()
        m.loans.append(l)
        try:
            new_db.session.add(m)
            new_db.session.commit()
        except Exception, e:
            log.error(e)
            continue
    #clear_mappers()
    return new_db
#}}}


def get_old_posters_location(home_dir, config, clean_config=False):
    if config.get('posters', None) is not None:
        dirname = config.get('posters')
    elif config.get('type', 'sqlite', section='database') == 'sqlite':
        dbname = config.get('name', 'griffith', section='database')
        if dbname != 'griffith':
            dirname = "posters_sqlite_%s" % dbname
        else:
            dirname = 'posters'
    else:
        dirname = "posters_%(type)s_%(host)s_%(port)s_%(name)s_%(user)s" % config.to_dict('database')
    if clean_config:
        config.remove_option('posters')
        config.save()
    return os.path.join(home_dir, dirname)
