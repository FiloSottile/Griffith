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

import sys
import os
import string
import wx
import gutils
import platform
import re
import gettext
from locale import getdefaultlocale

# for now, spell support will not be implemented
spell_support = 0

def locations(self):
    defaultLang, defaultEnc = getdefaultlocale()
    if defaultEnc is None:
        defaultEnc = 'UTF-8'
    locations = {}
    locations['exec'] = os.path.abspath(os.path.dirname(sys.argv[0])) # deprecated
    locations['lib']  = os.path.dirname(__file__)
    
    self.debug.show("running on %s - %s" % (os.name, platform.system()))
    if os.name == 'nt' or os.name.startswith('win'):
        self.windows = True
    else:
        self.windows = False
        
    if platform.system() == 'Darwin':
        self.mac = True
    else:
        self.mac = False
        
    if self.windows: # win32, win64
        import winshell
        from win32com.shell import shellcon, shell
        import shutil
        
        mydocs = winshell.my_documents()
        locations['movie_plugins']  = "%s\\lib\\plugins\\movie" % locations['exec']
        locations['export_plugins'] = "%s\\lib\\plugins\\export" % locations['exec']
        locations['images']         = "%s\\images" % locations['exec']
        locations['share']          = locations['images']
        locations['desktop']        = ''
        locations['i18n']           = "%s\\i18n" % locations['exec']
        os.environ['PATH'] += ";lib;"
        
        # griffith dir location should point to 'Application Data'
        # this is changed on 0.9.5+svn so we need to make it backward compatible
        if os.path.exists(os.path.join(mydocs, 'griffith').decode(defaultEnc)):
            shutil.move(os.path.join(mydocs, 'griffith').decode(defaultEnc),os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0), 'griffith').decode(defaultEnc))
        locations['home'] = os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0), 'griffith').decode(defaultEnc)
        
        # windows hack for locale setting
        lang = os.getenv('LANG')
        if lang is None:
            if defaultLang:
                lang = defaultLang
        if lang:
            os.environ['LANG'] = lang

    elif os.name == 'posix':
        locations['home']  = os.path.join(os.path.expanduser('~'), '.griffith').decode(defaultEnc)
        locations['share'] = os.path.abspath(os.path.join(locations['lib'], '..'))
        locations['i18n']  = os.path.abspath(os.path.join(locations['share'], '..', 'locale'))
        if not os.path.isdir(locations['i18n']):
            locations['i18n'] = os.path.join(locations['share'], 'i18n')
        #some locations
        locations['movie_plugins']  = os.path.join(locations['lib'], 'plugins', 'movie')
        locations['export_plugins'] = os.path.join(locations['lib'], 'plugins', 'export')
        locations['images']  = os.path.join(locations['share'], 'images')
        locations['desktop'] = os.path.join(os.path.expanduser('~'), 'Desktop').decode(defaultEnc)
    else:
        print 'Operating system not supported'
        sys.exit()
    
    from tempfile import gettempdir
    locations['temp'] = gettempdir()
    
    if self._tmp_home is not None: # see gconsole.check_args
        locations['home'] = self._tmp_home.decode(defaultEnc)
        del self._tmp_home

    try:
        if not os.path.exists(locations['home']):
            self.debug.show('Creating %s' % locations['home'])
            os.makedirs(locations['home'])
        else:
            self.debug.show("Using Griffith directory: %s" % locations['home'])
    except OSError:
        self.debug.show('Unable to create griffith directory.')
        raise
        sys.exit()

    if not os.access(locations['home'], os.W_OK):
        self.debug.show('Cannot write to griffith directory, %s' % locations['home'])
        sys.exit()

    # includes plugins in system path for easier importing
    sys.path.append(locations['lib'])
    sys.path.append(locations['movie_plugins'])
    sys.path.append(locations['export_plugins'])
    
    self.locations = locations
    return locations

def location_posters(locations, config):
    if config.get('posters', None) is not None:
        locations['posters']  = os.path.join(locations['home'], config.get('posters'))
    elif config.get('type', 'sqlite', section='database') == 'sqlite':
        dbname = config.get('name', 'griffith', section='database')
        if dbname != 'griffith':
            config['posters'] = 'posters_sqlite_' + dbname
        else:
            config['posters'] = 'posters'
        locations['posters'] = os.path.join(locations['home'], config.get('posters'))
        config.save()
    else:
        config['posters'] = "posters_%(type)s_%(host)s_%(port)s_%(name)s_%(user)s" % config.toDict('database')
        locations['posters'] = os.path.join(locations['home'], config.get('posters'))
        config.save()
    # check if posters dir exists
    if not os.path.isdir(locations['posters']):
        os.makedirs(locations['posters'])

def locations_misc(self):
    self._ = None

    # add default folders to some select widgets
    if self.windows:
        fonts_dir = os.path.join(os.environ['SYSTEMROOT'],'fonts')
        #self.widgets['preferences']['font'].set_current_folder(fonts_dir)
    elif self.mac:
       pass
        #self.widgets['preferences']['font'].set_current_folder("/System/Library/Fonts/")
    else:
       pass
        #self.widgets['preferences']['font'].set_current_folder("/usr/share/fonts/")
            
    self.griffith_dir = self.locations['home']	# deprecated

    self.pdf_reader = self.config.get('pdf_reader')

def i18n(self, location):
    gettext.bindtextdomain('griffith', location)
    gettext.textdomain('griffith')

def toolbar(self):
    """if toolbar is hide in config lets hide the widget"""
    if not self.config.get('view_toolbar', 'True', section='window'):
        pass

def treeview(self):
    self.main_listcontrol.InsertColumn(0, _('N.'), format=wx.LIST_FORMAT_LEFT, width=-1)
    self.main_listcontrol.InsertColumn(1, _('Original Title'), format=wx.LIST_FORMAT_LEFT, width=-1)
    self.main_listcontrol.InsertColumn(2, _('Title'), format=wx.LIST_FORMAT_LEFT, width=-1)
    self.main_listcontrol.InsertColumn(3, _('Director'), format=wx.LIST_FORMAT_LEFT, width=-1)
    self.main_listcontrol.InsertColumn(4, _('Genre'), format=wx.LIST_FORMAT_LEFT, width=-1)
    self.main_listcontrol.InsertColumn(5, _('Seen it'), format=wx.LIST_FORMAT_LEFT, width=-1)
    self.main_listcontrol.InsertColumn(6, _('Year'), format=wx.LIST_FORMAT_LEFT, width=-1)
    self.main_listcontrol.InsertColumn(7, _('Runtime'), format=wx.LIST_FORMAT_LEFT, width=-1)
    
def combos(self):
    i = 0
    pos_to_activate = 0
    selected_criteria = self.config.get('criteria', None, section='mainlist')
    for criteria in self.search_criteria:
        new_criteria = self.field_names[criteria]
        self.cb_criteria.Insert(new_criteria, i)
        if selected_criteria == new_criteria:
            pos_to_activate = i
        i += 1
    self.cb_criteria.SetSelection(pos_to_activate)
    i = 0
    for field in self.sort_criteria:
        if field != 'movie_id':
            #self.widgets['preferences']['sortby'].insert_text(i, self.field_names[field])
            pass
        else:
            #self.widgets['preferences']['sortby'].insert_text(i, _('Last added'))
            pass
        i += 1
    #self.widgets['preferences']['sortby'].set_wrap_width(3)
    #self.widgets['preferences']['sortby'].set_active(0) # Number

def dictionaries(self):
    """initializes data filled dynamically by users"""
    import update
    self.am_tags = {} # dictionary for tag CheckBoxes
    #update.update_volume_combo_ids(self)
    #update.update_collection_combo_ids(self)
    #fill_volumes_combo(self)
    #fill_collections_combo(self)
    #fill_preferences_tags_combo(self)
    #language_combos(self)
    #acodec_combos(self)
    #achannel_combos(self)
    #subformat_combos(self)
    #vcodec_combos(self)
    #media_combos(self)
    #create_tag_vbox(self, widget=self.widgets['add']['tag_vbox'], tab=self.am_tags)
    self.sort_criteria = [ # "[]" because of index() 
        'number', 'o_title', 'title', 'director', 'year', 'runtime', 'country',
        'genre', 'studio', 'media_num', 'rating', 'classification', 'collection_id',
        'volume_id', 'cond', 'layers', 'region', 'movie_id']
    self.search_criteria = (
        'o_title', 'title', 'number', 'director', 'plot', 'cast', 'notes', 'year',
        'runtime', 'country', 'genre', 'studio', 'media_num', 'rating')
    self.field_names = {
        'cast'           : _('Cast'),
        'classification' : _('Classification'),
        'collection_id'  : _('Collection'),
        'color'          : _('Color'),
        'cond'           : _('Condition'),
        'country'        : _('Country'),
        'director'       : _('Director'),
        'genre'          : _('Genre'),
        'image'          : _('Image'),
        'layers'         : _('Layers'),
        'loaned'         : _('Loaned'),
        'media_num'      : _('Discs'),
        'medium_id'      : _('Medium'),
        'notes'          : _('Notes'),
        'number'         : _('Number'),
        'o_site'         : _('Official site'),
        'o_title'        : _('Original Title'),
        'plot'           : _('Plot'),
        'rating'         : _('Rating'),
        'region'         : _('Region'),
        'runtime'        : _('Runtime'),
        'seen'           : _('Seen it'),
        'site'           : _('Site'),
        'studio'         : _('Studio'),
        'title'          : _('Title'),
        'trailer'        : _('Trailer'),
        'vcodec_id'      : _('Video codec'),
        'volume_id'      : _('Volume'),
        'year'           : _('Year')}
    self._conditions = (_('N/A'), _('Damaged'), _('Poor'),  _('Fair'), _('Good'), _('Excellent'))
    self._colors = (_('N/A'), _('Color'), _('Black and White'), _('Mixed'))
    self._lang_types = ('', _('lector'), _('dubbing'), _('subtitles'), _('commentary'))
    self._layers = (_('N/A'), _('Single Side, Single Layer'), _('Single Side, Dual Layer'), _('Dual Side, Single Layer'), _('Dual Side, Dual Layer'))
    self._regions = (
        _('Region 0 (No Region Coding)'),
        _('Region 1 (United States of America, Canada)'),
        _('Region 2 (Europe,including France, Greece, Turkey, Egypt, Arabia, Japan and South Africa)'),
        _('Region 3 (Korea, Thailand, Vietnam, Borneo and Indonesia)'),
        _('Region 4 (Australia and New Zealand, Mexico, the Caribbean, and South America)'),
        _('Region 5 (India, Africa, Russia and former USSR countries)'),
        _('Region 6 (Popular Republic of China)'),
        _('Region 7 (Reserved for Unspecified Special Use)'),
        _('Region 8 (Airlines/Cruise Ships)'),
    )

def web_results(self):
    self.treemodel_results = gtk.TreeStore(str, str)
    self.widgets['results']['treeview'].set_model(self.treemodel_results)
    self.widgets['results']['treeview'].set_headers_visible(False)
    # column ids
    renderer=gtk.CellRendererText()
    self.column1=gtk.TreeViewColumn(None, renderer, text=0)
    self.column1.set_visible(False)
    self.widgets['results']['treeview'].append_column(self.column1)
    # column titles
    renderer=gtk.CellRendererText()
    self.column2=gtk.TreeViewColumn(None, renderer, text=1)
    self.column2.set_resizable(True)
    self.column2.set_sort_column_id(1)
    self.widgets['results']['treeview'].append_column(self.column2)

def gtkspell(self):
    global spell_support
    spell_error = False
    if self.posix and spell_support:
        if self.config.get('gtkspell', False, section='spell') == True:
            if self.config.get('notes', True, section='spell') == True and self.config.get('lang', section='spell') != '':
                try:
                    self.notes_spell = gtkspell.Spell(self.widgets['add']['cast'], self.config.get('lang', section='spell'))
                except:
                    spell_error = True
            if self.config.get('plot', True, section='spell')==True and self.config.get('lang', section='spell') != '':
                try:
                    self.plot_spell = gtkspell.Spell(self.widgets['add']['plot'], self.config.get('lang', section='spell'))
                except:
                    spell_error = True
            if spell_error:
                self.debug.show('Dictionary not available. Spellcheck will be disabled.')
                if not self.config.get('notified', False, section='spell'):
                    gutils.info(self, _("Dictionary not available. Spellcheck will be disabled. \n" + \
                        "Please install the aspell-%s package or adjust the spellchekcer preferences.")%self.config.get('lang', section='spell'), \
                        self.widgets['preferences']['window'])
                    self.config.set('notified', True, section='spell')
                    self.config.save()
    else:
        self.debug.show('Spellchecker is not available')

def preferences(self):
    self.widgets['preferences']['db_type'].insert_text(0,'SQLite3 (internal)')
    self.widgets['preferences']['db_type'].insert_text(1,'PostgreSQL')
    self.widgets['preferences']['db_type'].insert_text(2,'MySQL')
    self.widgets['preferences']['db_type'].insert_text(3,'Microsoft SQL')
    self.widgets['preferences']['db_host'].set_text(self.config.get('host', '', section='database'))
    self.widgets['preferences']['db_port'].set_value(int(self.config.get('port', 0, section='database')))
    self.widgets['preferences']['db_user'].set_text(self.config.get('user', '', section='database'))
    self.widgets['preferences']['db_passwd'].set_text(self.config.get('passwd', '', section='database'))
    self.widgets['preferences']['db_name'].set_text(self.config.get('name', '', section='database'))
    db_type = self.config.get('type', 'sqlite', section='database')
    if db_type == 'postgres':
        self.widgets['preferences']['db_type'].set_active(1)
    elif db_type == 'mysql':
        self.widgets['preferences']['db_type'].set_active(2)
    elif db_type == 'mssql':
        self.widgets['preferences']['db_type'].set_active(3)
    else:
        self.widgets['preferences']['db_type'].set_active(0)

def fill_volumes_combo(self, default=0):
    self.widgets['add']['volume'].get_model().clear()
    self.widgets['filter']['volume'].get_model().clear()
    for i in self.volume_combo_ids:
        vol_id = self.volume_combo_ids[i]
        if vol_id>0:
            name = self.db.Volume.query.filter_by(volume_id=vol_id).first().name
        else:
            name = ''
        self.widgets['add']['volume'].insert_text(int(i), str(name))
        self.widgets['filter']['volume'].insert_text(int(i), str(name))
    self.widgets['add']['volume'].show_all()
    self.widgets['filter']['volume'].show_all()
    self.widgets['filter']['volume'].set_active(0)
    i = gutils.findKey(default, self.volume_combo_ids)
    if i is not None:
        self.widgets['add']['volume'].set_active(int(i))
    self.widgets['add']['volume'].set_wrap_width(3)

def fill_collections_combo(self, default=0):
    self.widgets['add']['collection'].get_model().clear()
    self.widgets['filter']['collection'].get_model().clear()
    for i in self.collection_combo_ids:
        col_id = self.collection_combo_ids[i]
        if col_id>0:
            name = self.db.Collection.query.filter_by(collection_id=col_id).first().name
        else:
            name = ''
        self.widgets['add']['collection'].insert_text(int(i), str(name))
        self.widgets['filter']['collection'].insert_text(int(i), str(name))
    self.widgets['add']['collection'].show_all()
    self.widgets['filter']['collection'].show_all()
    self.widgets['filter']['collection'].set_active(0)
    i = gutils.findKey(default, self.collection_combo_ids)
    if i is not None:
        self.widgets['add']['collection'].set_active(int(i))
    self.widgets['add']['collection'].set_wrap_width(2)

def fill_preferences_tags_combo(self):
    self.widgets['preferences']['tag_name'].get_model().clear()
    self.tags_ids = {}
    i = 0
    for tag in self.db.Tag.query.all():
        self.tags_ids[i] = tag.tag_id
        self.widgets['preferences']['tag_name'].insert_text(int(i), str(tag.name))
        i += 1
    self.widgets['preferences']['tag_name'].show_all()

def language_combos(self):
    self.widgets['preferences']['lang_name'].get_model().clear()
    self.languages_ids = {}
    self.languages_ids[0] = 0	# empty one
    self.widgets['preferences']['lang_name'].insert_text(0, '')
    i = 1
    for lang in self.db.Lang.query.all():
        self.languages_ids[i] = lang.lang_id
        self.widgets['preferences']['lang_name'].insert_text(int(i), str(lang.name))
        i += 1
    self.widgets['preferences']['lang_name'].show_all()
    # add movie languages treeview
    self.lang['lang'].clear()
    for i in self.db.Lang.query.all():
        self.lang['lang'].append([i.lang_id, i.name])
def acodec_combos(self):
    self.widgets['preferences']['acodec_name'].get_model().clear()
    self.acodecs_ids = {}
    self.acodecs_ids[0] = 0	# empty one
    self.widgets['preferences']['acodec_name'].insert_text(0, '')
    i = 1
    for acodec in self.db.ACodec.query.all():
        self.acodecs_ids[i] = acodec.acodec_id
        self.widgets['preferences']['acodec_name'].insert_text(int(i), str(acodec.name))
        i += 1
    self.widgets['preferences']['acodec_name'].show_all()
    # add movie languages treeview
    self.lang['acodec'].clear()
    for i in self.db.ACodec.query.all():
        self.lang['acodec'].append([i.acodec_id, i.name])
def achannel_combos(self):
    self.widgets['preferences']['achannel_name'].get_model().clear()
    self.achannels_ids = {}
    self.achannels_ids[0] = 0	# empty one
    self.widgets['preferences']['achannel_name'].insert_text(0, '')
    i = 1
    for achannel in self.db.AChannel.query.all():
        self.achannels_ids[i] = achannel.achannel_id
        self.widgets['preferences']['achannel_name'].insert_text(int(i), str(achannel.name))
        i += 1
    self.widgets['preferences']['achannel_name'].show_all()
    # add movie languages treeview
    self.lang['achannel'].clear()
    for i in self.db.AChannel.query.all():
        self.lang['achannel'].append([i.achannel_id, i.name])
def subformat_combos(self):
    self.widgets['preferences']['subformat_name'].get_model().clear()
    self.subformats_ids = {}
    self.subformats_ids[0] = 0	# empty one
    self.widgets['preferences']['subformat_name'].insert_text(0, '')
    i = 1
    for subformat in self.db.SubFormat.query.all():
        self.subformats_ids[i] = subformat.subformat_id
        self.widgets['preferences']['subformat_name'].insert_text(int(i), str(subformat.name))
        i += 1
    self.widgets['preferences']['subformat_name'].show_all()
    # add movie languages treeview
    self.lang['subformat'].clear()
    for i in self.db.SubFormat.query.all():
        self.lang['subformat'].append([i.subformat_id, i.name])

def media_combos(self):
    # clear data
    self.widgets['preferences']['medium_name'].get_model().clear()
    self.widgets['preferences']['media'].get_model().clear()
    self.widgets['add']['media'].get_model().clear()
    
    self.media_ids = {}

    self.media_ids[0] = None
    self.widgets['preferences']['medium_name'].insert_text(0, '')
    self.widgets['add']['media'].insert_text(0, _('N/A'))
    self.widgets['preferences']['media'].insert_text(0, _('N/A'))
    i = 1
    for medium in self.db.Medium.query.all():
        self.media_ids[i] = medium.medium_id
        self.widgets['preferences']['medium_name'].insert_text(int(i), str(medium.name))
        self.widgets['add']['media'].insert_text(int(i), str(medium.name))
        self.widgets['preferences']['media'].insert_text(int(i), str(medium.name))
        i += 1

    self.widgets['preferences']['medium_name'].show_all()
    self.widgets['add']['media'].show_all()
    self.widgets['preferences']['media'].show_all()
    if self.config.has_key('media', section='defaults'):
        pos = gutils.findKey(self.config.get('media', section='defaults'), self.media_ids)
        if pos  is not None:
            self.widgets['preferences']['media'].set_active(int(pos))
        else:
            self.widgets['preferences']['media'].set_active(0)
    else:
        self.widgets['preferences']['media'].set_active(0)

def vcodec_combos(self):
    # clear data
    self.widgets['preferences']['vcodec_name'].get_model().clear()
    self.widgets['preferences']['vcodec'].get_model().clear()
    self.widgets['add']['vcodec'].get_model().clear()
    
    self.vcodecs_ids = {}
    
    self.vcodecs_ids[0] = None
    self.widgets['preferences']['vcodec_name'].insert_text(0, '')
    self.widgets['add']['vcodec'].insert_text(0, _('N/A'))
    self.widgets['preferences']['vcodec'].insert_text(0, _('N/A'))
    i = 1
    for vcodec in self.db.VCodec.query.all():
        self.vcodecs_ids[i] = vcodec.vcodec_id
        self.widgets['preferences']['vcodec_name'].insert_text(int(i), str(vcodec.name))
        self.widgets['add']['vcodec'].insert_text(int(i), str(vcodec.name))
        self.widgets['preferences']['vcodec'].insert_text(int(i), str(vcodec.name))
        i += 1

    self.widgets['preferences']['vcodec_name'].show_all()
    self.widgets['add']['vcodec'].show_all()
    self.widgets['preferences']['vcodec'].show_all()
    
    pos = gutils.findKey(self.config.get('vcodec', 0, section='defaults'), self.vcodecs_ids)
    if pos is not None:
        self.widgets['preferences']['vcodec'].set_active(int(pos))
    else:
        self.widgets['preferences']['vcodec'].set_active(0)

def create_tag_vbox(self, widget, tab):
    for i in widget.get_children():
        i.destroy()
    for i in self.tags_ids:
        tag_id = self.tags_ids[i]
        tag_name = self.db.Tag.query.filter_by(tag_id=tag_id).first().name
        tab[i] = gtk.CheckButton(str(tag_name))
        tab[i].set_active(False)
        widget.pack_start(tab[i])
    widget.show_all()

def remove_hbox(self, widget, tab):
    number = len(widget.get_children())-1	# last box number
    try:
        tab.pop()
        widget.remove(widget.get_children().pop())
    except:
        self.debug.show('List is empty')
    widget.show_all()

