#!/usr/bin/env python

"""
Usage:
	% python setup.py py2app
"""

import sys,os
from distutils.core import setup

if sys.platform == 'darwin':
	
	# macosx needs latest macholib from svn trunk for this to work
	# see http://svn.pythonmac.org/macholib/macholib/trunk/macholib/

	import py2app
		
	# Build the .app file
	
	from setuptools import setup

	APP = ['griffith.py']
	DATA_FILES = ['lib/add.py',
	 'lib/config.py',
	 'lib/dbupgrade.py',
	 'lib/delete.py',
	 'lib/gconsole.py',
	 'lib/gdebug.py',
	 'lib/gutils.py',
	 'lib/initialize.py',
	 'lib/main_treeview.py',
	 'lib/quick_filter.py',
	 'lib/sql.py',
	 'lib/version.py'
	]
	OPTIONS = {'argv_emulation': True,
	'includes': "cgi,PIL,tempfile,csv,threading,htmlentitydefs,sqlalchemy,sqlalchemy.*,sqlalchemy.mods.*,sqlalchemy.databases.*,sqlalchemy.engine.*,sqlalchemy.ext.*,sqlalchemy.orm.*,zipfile,webbrowser,shutil,reportlab,reportlab.pdfgen,reportlab.pdfgen.canvas,reportlab.platypus,reportlab.pdfbase.ttfonts,smtplib,platform,gzip,commands,encodings,encodings.*",
	'iconfile': './images/griffith.icns',
	"optimize": 2
	}

	setup(
	    app=APP,
	    data_files=DATA_FILES,
	    options={'py2app': OPTIONS},
	    setup_requires=['py2app'],
	)
	
elif os.name == 'nt' or os.name.startswith('win'):

	import py2exe
	import time
	import sys
		
	# ModuleFinder can't handle runtime changes to __path__, but win32com uses them

	try:
		import modulefinder
		import win32com
		for p in win32com.__path__[1:]:
			modulefinder.AddPackagePath("win32com", p)
		for extra in ["win32com.shell"]: #,"win32com.mapi"
			__import__(extra)
			m = sys.modules[extra]
			for p in m.__path__[1:]:
				modulefinder.AddPackagePath(extra, p)
	except ImportError:
		# no build path setup, no worries.
		pass

	from distutils.core import setup
	import glob
	import py2exe

	opts = {
		"py2exe": {
			"includes": "cgi,PIL,pysqlite2,pysqlite2.*,tempfile,csv,threading,htmlentitydefs,sqlalchemy,sqlalchemy.*,sqlalchemy.mods.*,sqlalchemy.databases.*,sqlalchemy.engine.*,sqlalchemy.ext.*,sqlalchemy.orm.*,zipfile,webbrowser,shutil,reportlab,reportlab.pdfgen,reportlab.pdfgen.canvas,reportlab.platypus,reportlab.pdfbase.ttfonts,smtplib,win32com,platform,winshell,gzip,commands,encodings,encodings.*",
			"optimize": 2,
			"dist_dir": "dist",
		}
	}

	setup(
		name = "Griffith",
		version = "0.10dev",
		description = 'Griffith - A media collection manager',
		author = 'Vasco Nunes/Piotr Ozarowski',
		author_email = 'griffith-private@lists.berlios.de',
		url = 'http://www.griffith.cc/',
		license = 'GPL',
		windows = [
			{
				"script": "griffith.py",
				"icon_resources": [(1, "images\griffith.ico")]
			}],
		options = opts,
			data_files=[
			("i18n/bg/LC_MESSAGES", glob.glob("i18n\\bg\\LC_MESSAGES\\*.mo")),
			("i18n/ca/LC_MESSAGES",	glob.glob("i18n\\ca\\LC_MESSAGES\\*.mo")),
			("i18n/cs/LC_MESSAGES",	glob.glob("i18n\\cs\\LC_MESSAGES\\*.mo")),
			("i18n/da/LC_MESSAGES",	glob.glob("i18n\\da\\LC_MESSAGES\\*.mo")),
			("i18n/de/LC_MESSAGES",	glob.glob("i18n\\de\\LC_MESSAGES\\*.mo")),
			("i18n/el/LC_MESSAGES",	glob.glob("i18n\\el\\LC_MESSAGES\\*.mo")),
			("i18n/es/LC_MESSAGES",	glob.glob("i18n\\es\\LC_MESSAGES\\*.mo")),
			("i18n/ja/LC_MESSAGES",	glob.glob("i18n\\ja\\LC_MESSAGES\\*.mo")),
			("i18n/fr/LC_MESSAGES",	glob.glob("i18n\\fr\\LC_MESSAGES\\*.mo")),
			("i18n/nb/LC_MESSAGES",	glob.glob("i18n\\nb\\LC_MESSAGES\\*.mo")),
			("i18n/pl/LC_MESSAGES",	glob.glob("i18n\\pl\\LC_MESSAGES\\*.mo")),
			("i18n/pt/LC_MESSAGES",	glob.glob("i18n\\pt\\LC_MESSAGES\\*.mo")),
			("i18n/ru/LC_MESSAGES",	glob.glob("i18n\\ru\\LC_MESSAGES\\*.mo")),
			("i18n/it/LC_MESSAGES",	glob.glob("i18n\\it\\LC_MESSAGES\\*.mo")),
			("i18n/nl/LC_MESSAGES",	glob.glob("i18n\\nl\\LC_MESSAGES\\*.mo")),
			("i18n/sv/LC_MESSAGES",	glob.glob("i18n\\sv\\LC_MESSAGES\\*.mo")),
			("i18n/tr/LC_MESSAGES",	glob.glob("i18n\\tr\\LC_MESSAGES\\*.mo")),
			("i18n/pt_BR/LC_MESSAGES", glob.glob("i18n\\pt_BR\\LC_MESSAGES\\*.mo")),
			("i18n/zh_CN/LC_MESSAGES", glob.glob("i18n\\zh_CN\\LC_MESSAGES\\*.mo")),
			("images", glob.glob("images\\*.png")),
			("lib", glob.glob("lib\\*.*"))],
	)