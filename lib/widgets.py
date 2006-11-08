# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2006 Vasco Nunes
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
import edit
import gtk
import sys

def define_widgets(self, gladefile):
	self.e_movie_id = gladefile.get_widget('m_movie_id')
	#widgets
	self.main_window = gladefile.get_widget('main_window')
	self.toolbar     = gladefile.get_widget('toolbar1')
	# add movie window
	self.add_movie_window  = gladefile.get_widget('add_movie')
	self.am_original_title = gladefile.get_widget('am_original_title')
	self.am_title          = gladefile.get_widget('am_title')
	self.am_number         = gladefile.get_widget('am_number')
	self.am_director       = gladefile.get_widget('am_director')
	self.am_plot           = gladefile.get_widget('am_plot')
	self.am_picture        = gladefile.get_widget('am_image')
	self.am_picture_name   = gladefile.get_widget('am_hide_image_name')
	self.am_year           = gladefile.get_widget('am_year')
	self.am_runtime        = gladefile.get_widget('am_runtime')
	self.am_with           = gladefile.get_widget('am_with')
	self.am_country        = gladefile.get_widget('am_country')
	self.am_genre          = gladefile.get_widget('am_genre')
	self.am_media          = gladefile.get_widget('am_media')
	self.am_vcodec         = gladefile.get_widget('am_vcodec')
	self.am_classification = gladefile.get_widget('am_classification')
	self.am_studio         = gladefile.get_widget('am_studio')
	self.am_site           = gladefile.get_widget('am_site')
	self.am_imdb           = gladefile.get_widget('am_imdb')
	self.am_trailer        = gladefile.get_widget('am_trailer')
	self.am_discs          = gladefile.get_widget('am_discs')
	self.am_source         = gladefile.get_widget('am_source')
	self.am_obs            = gladefile.get_widget('am_obs')
	self.am_plugin_desc    = gladefile.get_widget('am_plugin_desc')
	self.am_plugin_image   = gladefile.get_widget('am_plugin_image')
	# main treeview
	self.main_treeview  = gladefile.get_widget('main_treeview')
	self.confirm_delete = gladefile.get_widget('confirm_delete')
	# main notebook
	self.cast           = gladefile.get_widget('m_cast')
	self.classification = gladefile.get_widget('m_classification')
	self.collection     = gladefile.get_widget('m_collection')
	self.color          = gladefile.get_widget('m_color')
	self.condition      = gladefile.get_widget('m_condition')
	self.country        = gladefile.get_widget('m_country')
	self.director       = gladefile.get_widget('m_director')
	self.genre          = gladefile.get_widget('m_genre')
	self.imdb           = gladefile.get_widget('m_imdb')
	self.layers         = gladefile.get_widget('m_layers')
	self.medium         = gladefile.get_widget('m_medium')
	self.notes          = gladefile.get_widget('m_notes')
	self.number         = gladefile.get_widget('m_number')
	self.o_title        = gladefile.get_widget('m_o_title')
	self.picture        = gladefile.get_widget('m_picture_image')
	self.picture_button = gladefile.get_widget('m_picture')
	self.plot           = gladefile.get_widget('m_plot')
	self.region         = gladefile.get_widget('m_region')
	self.runtime        = gladefile.get_widget('m_runtime')
	self.loan_info      = gladefile.get_widget('loan_information')
	self.site           = gladefile.get_widget('m_site')
	self.studio         = gladefile.get_widget('m_studio')
	self.title          = gladefile.get_widget('m_title')
	self.trailer        = gladefile.get_widget('m_trailer')
	self.vcodec         = gladefile.get_widget('m_vcodec')
	self.volume         = gladefile.get_widget('m_volume')
	self.year           = gladefile.get_widget('m_year')
	self.seen_icon      = gladefile.get_widget('m_seen_icon')
	self.loaned_icon    = gladefile.get_widget('m_loaned_icon')
	self.tags           = gladefile.get_widget('m_tags')
	self.show_volume_button     = gladefile.get_widget('m_show_volume_button')
	self.show_collection_button = gladefile.get_widget('m_show_collection_button')

	# volumes/collections tab
	self.am_volume_combo                = gladefile.get_widget('am_volume_combo')
	self.am_collection_combo            = gladefile.get_widget('am_collection_combo')
	# get from web
	self.b_get_from_web = gladefile.get_widget('get_from_web')
	self.c_web_source   = gladefile.get_widget('combo_source')
	self.progressbar    = gladefile.get_widget('w_progress')
	# results
	self.w_results        = gladefile.get_widget('results')
	self.results_treeview = gladefile.get_widget('results_treeview')
	#REMOVE:self.update_button    = gladefile.get_widget('update_button')
	# statusbar
	self.statusbar = gladefile.get_widget('statusbar')
	# preferences
	self.w_preferences = gladefile.get_widget('w_preferences')
	self.epdf_reader   = gladefile.get_widget('pdf_reader_entry')
	self.p_db_type     = gladefile.get_widget('p_db_type')
	self.p_db_host     = gladefile.get_widget('p_db_host')
	self.p_db_port     = gladefile.get_widget('p_db_port')
	self.p_db_name     = gladefile.get_widget('p_db_name')
	self.p_db_user     = gladefile.get_widget('p_db_user')
	self.p_db_passwd   = gladefile.get_widget('p_db_passwd')
	self.p_db_details  = gladefile.get_widget('p_db_details')
	self.p_s_classification = gladefile.get_widget('p_s_classification')
	self.p_s_country   = gladefile.get_widget('p_s_country')
	self.p_s_director  = gladefile.get_widget('p_s_director')
	self.p_s_genre     = gladefile.get_widget('p_s_genre')
	self.p_s_image     = gladefile.get_widget('p_s_image')
	self.p_s_notes     = gladefile.get_widget('p_s_notes')
	self.p_s_o_site    = gladefile.get_widget('p_s_o_site')
	self.p_s_o_title   = gladefile.get_widget('p_s_o_title')
	self.p_s_plot      = gladefile.get_widget('p_s_plot')
	self.p_s_rating    = gladefile.get_widget('p_s_rating')
	self.p_s_runtime   = gladefile.get_widget('p_s_runtime')
	self.p_s_site      = gladefile.get_widget('p_s_site')
	self.p_s_studio    = gladefile.get_widget('p_s_studio')
	self.p_s_title     = gladefile.get_widget('p_s_title')
	self.p_s_trailer   = gladefile.get_widget('p_s_trailer')
	self.p_s_with      = gladefile.get_widget('p_s_with')
	self.p_s_year      = gladefile.get_widget('p_s_year')
	# cover print
	self.w_print_cover_simple              = gladefile.get_widget('w_print_cover_simple')
	self.w_print_cover_image               = gladefile.get_widget('w_print_cover_image')
	self.cover_simple_size                 = gladefile.get_widget('cover_simple_size')
	self.cover_simple_include_movie_number = gladefile.get_widget('cover_simple_include_movie_number')
	self.cover_image_size                  = gladefile.get_widget('cover_image_size')
	self.cover_image_number                = gladefile.get_widget('cover_image_number')
	self.cover_simple_include_poster       = gladefile.get_widget('cover_simple_include_poster')
	#people
	self.w_people   = gladefile.get_widget('w_people')
	self.ap_name    = gladefile.get_widget('ap_name')
	self.ap_email   = gladefile.get_widget('ap_email')
	self.ap_phone   = gladefile.get_widget('ap_phone')
	self.ep_name    = gladefile.get_widget('ep_name')
	self.ep_email   = gladefile.get_widget('ep_email')
	self.ep_phone   = gladefile.get_widget('ep_phone')
	self.ep_id      = gladefile.get_widget('ep_id')
	self.p_treeview = gladefile.get_widget('p_treeview')
	#filter
	self.e_filter        = gladefile.get_widget('filter_txt')
	self.filter_criteria = gladefile.get_widget('filter_criteria')
	self.w_add_person    = gladefile.get_widget('w_add_person')
	self.w_edit_person   = gladefile.get_widget('w_edit_person')
	#loan
	self.w_loan_to     = gladefile.get_widget('w_loan_to')
	self.return_button = gladefile.get_widget('return_button')
	self.loan_button   = gladefile.get_widget('loan_button')
	self.loan_to       = gladefile.get_widget('loan_to')
	self.list_loaned   = gladefile.get_widget('list_loaned_movies')
	#prefs
	self.view_image    = gladefile.get_widget('view_image')
	self.view_otitle   = gladefile.get_widget('view_otitle')
	self.view_title    = gladefile.get_widget('view_title')
	self.view_director = gladefile.get_widget('view_director')
	self.p_media       = gladefile.get_widget('p_media')
	self.p_vcodec       = gladefile.get_widget('p_vcodec')
	self.p_color       = gladefile.get_widget('p_color')
	self.p_condition   = gladefile.get_widget('p_condition')
	self.p_region      = gladefile.get_widget('p_region')
	self.p_layers      = gladefile.get_widget('p_layers')
	self.p_font        = gladefile.get_widget('p_font')
	#buttons
	self.go_o_site_button   = gladefile.get_widget('go_o_site')
	self.go_site_button     = gladefile.get_widget('go_site')
	self.go_trailer_button  = gladefile.get_widget('go_trailer')
	self.new_db      = gladefile.get_widget('new_bt')
	#notebooks
	self.nb_add = gladefile.get_widget('notebook_add')
	#ratings
	self.image_rating      = gladefile.get_widget('image_rating')
	self.image_add_rating  = gladefile.get_widget('image_add_rating')
	self.menu_toolbar      = gladefile.get_widget('menu_toolbar')
	self.export_menu       = gladefile.get_widget('export_menu')

	self.rating_slider_add = gladefile.get_widget('rating_scale_add')

	#tech data
	self.am_condition = gladefile.get_widget('am_condition')
	self.am_color     = gladefile.get_widget('am_color')
	self.am_region    = gladefile.get_widget('am_region')
	self.am_layers    = gladefile.get_widget('am_layers')

	#spellchecker
	self.spellchecker = gladefile.get_widget('spellchecker_pref')
	self.spell_notes  = gladefile.get_widget('spell_notes')
	self.spell_plot   = gladefile.get_widget('spell_plot')
	self.spell_lang   = gladefile.get_widget('spell_lang')

	self.am_seen          = gladefile.get_widget('am_seen')
	self.b_email_reminder = gladefile.get_widget('b_email_reminder')
	self.loan_history     = gladefile.get_widget('loan_history')
	self.default_plugin   = gladefile.get_widget('default_plugin')
	self.rating_image     = gladefile.get_widget('rating_image')
	self.mail_smtp_server = gladefile.get_widget('mail_smtp_server')
	self.mail_use_auth    = gladefile.get_widget('mail_use_auth')
	self.mail_username    = gladefile.get_widget('mail_username')
	self.mail_password    = gladefile.get_widget('mail_password')
	self.mail_email       = gladefile.get_widget('mail_email')
	self.all_movies       = gladefile.get_widget('all_movies')
	self.results_select   = gladefile.get_widget('results_select')
	self.results_cancel   = gladefile.get_widget('results_cancel')

	# poster button related
	self.open_poster     = gladefile.get_widget('open_poster')
	self.fetch_poster    = gladefile.get_widget('fetch_poster')
	self.delete_poster   = gladefile.get_widget('delete_poster')
	self.t_delete_poster = gladefile.get_widget('t_delete_poster')

	self.poster_window = gladefile.get_widget('poster_window')
	self.big_poster    = gladefile.get_widget('big_poster')

	#main popup menu
	self.popup        = gladefile.get_widget('popup')
	self.popup_loan   = gladefile.get_widget('popup_loan')
	self.popup_return = gladefile.get_widget('popup_return')
	self.popup_email  = gladefile.get_widget('popup_email')
	self.f_col        = gladefile.get_widget('f_col')

	#add some tooltips
	self.tooltips = gtk.Tooltips()
	self.tooltips.set_tip(self.epdf_reader, _('Define here the PDF reader you want to use within Griffith. Popular choices are xpdf, gpdf, evince or kpdf. Make sure you have this program installed and working first.'))
	self.tooltips.set_tip(self.spell_lang, _("Here you can define the desired language to use while spell checking some fields. Use you locale setting. For example, to use european portuguese spell checking enter 'pt'"))
	self.tooltips.set_tip(self.mail_smtp_server, _("Use this entry to define the SMTP server you want to use to send e-mails. On *nix systems, 'localhost' should work. Alternatively, you can use your Internet Service Provider's SMTP server address."))
	self.tooltips.set_tip(self.mail_email, _("This is the from e-mail address that should be used to all outgoing e-mail. You want to include your own e-mail address here probably."))

	# add handlers for windows delete events
	self.add_movie_window.connect('delete_event', self.on_delete_event_am)
	self.w_results.connect('delete_event', self.on_delete_event_r)
	self.w_people.connect('delete_event', self.on_delete_event_wp)
	self.w_add_person.connect('delete_event', self.on_delete_event_ap)
	self.w_edit_person.connect('delete_event', self.on_delete_event_ep)
	self.w_loan_to.connect('delete_event', self.on_delete_event_lt)
	self.w_print_cover_simple.connect('delete_event', self.on_delete_event_pcs)
	self.w_print_cover_image.connect('delete_event', self.on_delete_event_pci)
	self.poster_window.connect('delete_event', self.on_delete_event_pw)
	self.w_preferences.connect('delete_event', self.on_delete_event_p)

	# languages
	self.lang_name_combo  = gladefile.get_widget('lang_name_combo')	# preferences window
	self.lang['menu'] = gladefile.get_widget('lang_menu')
	self.lang['treeview'] = gladefile.get_widget('lang_treeview')
	self.lang['treeview'].connect('button_press_event', self.on_lang_treeview_button_press_event)
	self.audio_vbox = gladefile.get_widget('m_audio_vbox')
	self.subtitle_vbox = gladefile.get_widget('m_subtitle_vbox')

	# tags
	self.tag_name_combo = gladefile.get_widget('tag_name_combo')	# preferences window
	self.am_tag_vbox    = gladefile.get_widget('am_tag_vbox')	# add window
	# audio codecs
	self.acodec_name_combo = gladefile.get_widget('acodec_name_combo')	# preferences window
	# audio channels
	self.achannel_name_combo = gladefile.get_widget('achannel_name_combo')	# preferences window
	# subtitle formats
	self.subformat_name_combo = gladefile.get_widget('subformat_name_combo')	# preferences window
	# media
	self.medium_name_combo = gladefile.get_widget('medium_name_combo')	# preferences window
	self.am_medium_vbox    = gladefile.get_widget('am_medium_vbox')	# add window
	# video codecs
	self.vcodec_name_combo = gladefile.get_widget('vcodec_name_combo')	# preferences window
	self.am_vcodec_vbox    = gladefile.get_widget('am_vcodec_vbox')	# add window

	self.main_window.connect('key_press_event', self.on_key_press_event)
	self.main_treeview.connect('button_press_event', self.on_maintree_button_press_event)
	self.p_treeview.connect('button_press_event', self.on_p_tree_button_press_event)

	# define handlers for general events

	dic = {
		'gtk_main_quit'                         : self.destroy,
		'on_about1_activate'                    : self.about_dialog,
		'on_quit1_activate'                     : self.destroy,
		'on_toolbar_quit_clicked'               : self.destroy,
		'on_toolbar_add_clicked'                : self.add_movie,
		'on_cancel_add_movie_clicked'           : self.hide_add_movie,
		'on_add1_activate'                      : self.add_movie,
		'on_add_movie_clicked'                  : self.add_movie_db,
		'on_add_movie_close_clicked'            : self.add_movie_close_db,
		'on_delete_movie_clicked'               : self.delete_movie,
		'on_delete1_movie_activate'             : self.delete_movie,
		'on_main_treeview_row_activated'        : self.treeview_clicked,
		'on_row_activated'                      : self.treeview_clicked,
		'on_get_from_web_clicked'               : self.get_from_web,
		'on_update_button_clicked'              : self.update_movie,
		# preferences
		'on_preferences1_activate'              : self.show_preferences,
		'on_cancel_preferences_clicked'         : self.hide_preferences,
		'on_save_preferences_clicked'           : self.save_preferences,
		'on_p_db_type_changed'                  : self.on_p_db_type_changed,
		'on_backup_activate'                    : self.backup,
		'on_restore_activate'                   : self.restore,
		'on_merge_activate'                     : self.merge,
		'on_cover_simple_activate'              : self.print_cover_simple_show,
		'on_cancel_print_cover_simple_clicked'  : self.print_cover_simple_hide,
		'on_b_print_cover_simple_clicked'       : self.print_cover_simple_process,
		'on_add_clear_clicked'                  : self.clear_add_dialog,
		'on_people_activate'                    : self.show_people_window,
		'on_cancel_people_clicked'              : self.hide_people_window,
		'on_filter_txt_changed'                 : self.filter_txt,
		'on_filter_criteria_changed'            : self.filter_txt,
		'on_clear_filter_clicked'               : self.clear_filter,
		'on_people_add_clicked'                 : self.add_person,
		'on_add_person_cancel_clicked'          : self.add_person_cancel,
		'on_add_person_db_clicked'              : self.add_person_db,
		'on_people_delete_clicked'              : self.delete_person,
		'on_people_edit_clicked'                : self.edit_person,
		'on_edit_person_cancel_clicked'         : self.edit_person_cancel,
		'on_update_person_clicked'              : self.update_person,
		'on_clone_activate'                     : self.clone_movie,
		'on_loan_button_clicked'                : self.loan_movie,
		'on_cancel_loan_clicked'                : self.cancel_loan,
		'on_loan_ok_clicked'                    : self.commit_loan,
		'on_return_button_clicked'              : self.return_loan,
		'on_list_loaned_movies_activate'        : self.filter_loaned,
		'on_cover_choose_image_activate'        : self.print_cover_image,
		'on_cancel_print_cover_image_clicked'   : self.print_cover_image_hide,
		'on_b_print_cover_image_clicked'        : self.print_cover_image_process,
		'on_combo_source_changed'               : self.source_changed,
		# toolbar
		'on_view_toolbar_activate'              : self.toggle_toolbar,
		'on_go_first_clicked'                   : self.go_first,
		'on_go_last_clicked'                    : self.go_last,
		'on_go_back_clicked'                    : self.go_prev,
		'on_go_forward_clicked'                 : self.go_next,
		'on_new_bt_clicked'                     : self.new_dbb,
		'on_new_activate'                       : self.new_dbb,
		# poster
		'on_e_picture_clicked'                  : self.change_poster,
		'on_open_poster_clicked'                : self.change_poster,
		'on_zoom_poster_clicked'                : self.z_poster,
		'on_delete_poster_clicked'              : self.del_poster,
		'on_fetch_poster_clicked'               : self.get_poster,
		# URLs
		'on_goto_homepage_activate'             : self.on_goto_homepage_activate,
		'on_goto_forum_activate'                : self.on_goto_forum_activate,
		'on_goto_report_bug_activate'           : self.on_goto_report_bug_activate,
		'on_go_o_site_clicked'                  : self.go_oficial_site,
		'on_go_site_clicked'                    : self.go_site,
		'on_go_trailer_clicked'                 : self.go_trailer_site,
		'on_seen_movies_activate'               : self.filter_not_seen,
		'on_all_movies_activate'                : self.filter_all,
		'on_rating_scale_value_changed'         : self.scale_rating_change,
		'on_rating_scale_add_value_changed'     : self.scale_rating_change_add,
		'on_sugest_activate'                    : self.sugest_movie,
		'on_popup_delete_activate'              : self.delete_movie,
		'on_popup_clone_activate'               : self.clone_movie,
		'on_popup_simple_activate'              : self.print_cover_simple_show,
		'on_popup_choose_image_activate'        : self.print_cover_image,
		# loans
		'on_popup_loan_activate'                : self.loan_movie,
		'on_popup_return_activate'              : self.return_loan,
		'on_popup_email_activate'               : self.email_reminder,
		'on_email_reminder_clicked'             : self.email_reminder,
		# volumes/collections
		'on_am_collection_combo_changed'        : self.on_am_collection_combo_changed,
		'on_am_volume_combo_changed'            : self.on_am_volume_combo_changed,
		'on_am_add_volume_button_clicked'       : self.add_volume,
		'on_am_add_collection_button_clicked'   : self.add_collection,
		'on_am_remove_volume_button_clicked'    : self.remove_volume,
		'on_am_remove_collection_button_clicked': self.remove_collection,
		'on_f_col_changed'                      : self.filter_collection,
		'on_results_cancel_clicked'		: self.results_cancel_ck,
		# languages
		'on_lang_add_clicked'			: self.on_lang_add_clicked,
		'on_lang_remove_clicked'		: self.on_lang_remove_clicked,
		'on_lang_rename_clicked'		: self.on_lang_rename_clicked,
		'on_lang_name_combo_changed'		: self.on_lang_name_combo_changed,
		# tags
		'on_tag_add_clicked'			: self.on_tag_add_clicked,
		'on_tag_remove_clicked'			: self.on_tag_remove_clicked,
		'on_tag_rename_clicked'			: self.on_tag_rename_clicked,
		'on_tag_name_combo_changed'		: self.on_tag_name_combo_changed,
		# audio codecs
		'on_acodec_add_clicked'			: self.on_acodec_add_clicked,
		'on_acodec_remove_clicked'		: self.on_acodec_remove_clicked,
		'on_acodec_rename_clicked'		: self.on_acodec_rename_clicked,
		'on_acodec_name_combo_changed'		: self.on_acodec_name_combo_changed,
		# audio channels
		'on_achannel_add_clicked'		: self.on_achannel_add_clicked,
		'on_achannel_remove_clicked'		: self.on_achannel_remove_clicked,
		'on_achannel_rename_clicked'		: self.on_achannel_rename_clicked,
		'on_achannel_name_combo_changed'	: self.on_achannel_name_combo_changed,
		# subtitle formats
		'on_subformat_add_clicked'		: self.on_subformat_add_clicked,
		'on_subformat_remove_clicked'		: self.on_subformat_remove_clicked,
		'on_subformat_rename_clicked'		: self.on_subformat_rename_clicked,
		'on_subformat_name_combo_changed'	: self.on_subformat_name_combo_changed,
		# media
		'on_medium_add_clicked'			: self.on_medium_add_clicked,
		'on_medium_remove_clicked'		: self.on_medium_remove_clicked,
		'on_medium_rename_clicked'		: self.on_medium_rename_clicked,
		'on_medium_name_combo_changed'		: self.on_medium_name_combo_changed,
		# video codecs
		'on_vcodec_add_clicked'			: self.on_vcodec_add_clicked,
		'on_vcodec_remove_clicked'		: self.on_vcodec_remove_clicked,
		'on_vcodec_rename_clicked'		: self.on_vcodec_rename_clicked,
		'on_vcodec_name_combo_changed'		: self.on_vcodec_name_combo_changed
	}
	gladefile.signal_autoconnect(dic)

def connect_add_signals(self):
	try:
		self.results_select.disconnect(self.poster_results_signal)
	except:
		pass

	try:
		self.results_treeview.disconnect(self.results_poster_double_click)
	except:
		pass

	try:
		self.results_select.disconnect(self.results_signal)
	except:
		pass

	try:
		self.results_treeview.disconnect(self.results_double_click)
	except:
		pass

	# connect signals

	self.results_signal = self.results_select.connect('clicked', \
			self.populate_dialog_with_results)
	self.results_double_click = self.results_treeview.connect('button_press_event', \
		self.on_results_button_press_event)

def connect_poster_signals(self, event, result, current_poster):
	import edit

	try:
		self.results_select.disconnect(self.poster_results_signal)
	except:
		pass

	try:
		self.results_treeview.disconnect(self.results_poster_double_click)
	except:
		pass

	try:
		self.results_select.disconnect(self.results_signal)
	except:
		pass

	try:
		self.results_treeview.disconnect(self.results_double_click)
	except:
		pass

	# connect signals

	self.results_poster_double_click = self.results_treeview.connect('button_press_event', \
		edit.get_poster_select_dc, self, result, current_poster)

	self.poster_results_signal = \
		self.results_select.connect('clicked', edit.get_poster_select, \
		self, result, current_poster)
