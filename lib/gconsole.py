# -*- coding: ISO-8859-1 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2006 Vasco Nunes
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
import getopt
import sys
import gutils

def check_args(self):
	if len(sys.argv)>1:
		try:
			opts, args = getopt.getopt(sys.argv[1:], "hDco:s:d:w:y:",
					['help', 'debug', 'sqlecho', 'clean', 'fix-db', 'search_original=', 'search_title=', 'director=', 'with=', 'year='])
		except getopt.GetoptError:
			# print help information and exit:
			con_usage()
			sys.exit(2)

		where = {}
		for o, a in opts:
			if o in ('-h', '--help'):
				con_usage()
				sys.exit()
			if o in ('-D', '--debug'):
				self.debug.set_debug()
			if o in ('-c', '--clean'):
				gutils.clean_posters_dir(self)
				sys.exit()
			if o == '--fix-db':
				self.db.fix_old_data()
			if o == '--sqlecho':
				self.db.metadata.engine.echo = True
			if o in ('-o', '--search_original'):
				where['original_title'] = a
			if o in ('-s', '--search_title'):
				where['title'] = a
			if o in ('-d', '--director'):
				where['director'] = a
			if o in ('-w', '--with'):
				where['actors'] = a
			if o in ('-y', '--year'):
				where['year'] = str(int(a))
		if len(where)>0:
			con_search_movie(self, where)

def con_search_movie(self, where): # FIXME
	query = ''
	for i in where:
		query += i + " LIKE '%" + where[i] + "%' AND "
	query = query[:len(query)-5] # cut last " AND "

	cursor = self.db.get_all_data(table_name="movies", order_by="number ASC", where=query,
			what='number, title, original_title, year, director')
	if cursor.EOF:
		print _("No movie found")
	while not cursor.EOF:
		row = cursor.GetRowAssoc(0)
		print "\033[31;1m[%s]\033[0m\t\033[38m%s\033[0m (%s), %s - \033[32m%s\033[0m"%(row['number'],row['title'], \
			row['original_title'], row['year'], row['director'])
		cursor.MoveNext()
	sys.exit()

def con_usage():
	print "USAGE:", sys.argv[0], "[OPTIONS] [HOMEDIR]"
	print "\nHOMEDIR is optional home directory (if different than ~/.griffith)"
	print "\nOPTION:"
	print "-h, --help\tprints this screen"
	print "-D, --debug\trun with more debug info"
	print "-c, --clean\tfind and delete orphan files in poster's directory"
	print "--fix-db\tfix old database"
	print "--sqlecho\tprint SQL queries"
	print "\n printing movie list:"
	print "-d <expr>, --director=<expr>"
	print "-o <expr>, --original_title=<expr>"
	print "-s <expr>, --search_title=<expr>"
	print "-w <expr>, --with=<expr>"
	print "-y <expr>, --year=<expr>"

