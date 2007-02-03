# Written by Christian Sagmueller <christian@sagmueller.net>
# based on PluginMovieIMDB.py, Copyright (c) 2005 Vasco Nunes
# You may use and distribute this software under the terms of the
# GNU General Public License, version 2 or later

from gettext import gettext as _
import gutils
import movie,string

plugin_name = "OFDb"
plugin_description = "Online-Filmdatenbank"
plugin_url = "www.ofdb.de"
plugin_language = _("German")
plugin_author = "Christian Sagmueller, Jessica Katharina Parth"
plugin_author_email = "Jessica.K.P@women-at-work.org"
plugin_version = "0.7"

class Plugin(movie.Movie):
	def __init__(self, id):
		self.encode='iso-8859-1'
		self.movie_id = id
		self.url = "http://www.ofdb.de/view.php?page=film&fid=%s" % str(self.movie_id)

	def get_image(self):
		self.image_url = "http://www.ofdb.de/images/film/" + gutils.trim( self.page, "<img src=\"images/film/", "\"" )
		
	def get_o_title(self):
		self.o_title = gutils.trim(self.page,"""Originaltitel:</font></td>
            <td>&nbsp;&nbsp;</td>
            <td width="99%"><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b>""","<")

	def get_title(self):
		self.title = gutils.trim(self.page,'size="3"><b>','<')

	def get_director(self):
		self.director = gutils.trim(self.page,"""Regie: 
              </font></td>
            <td>&nbsp;&nbsp;</td>
            <td><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b><a href="view.php?page=liste&Name=""","</a><br>")
		self.director = string.capwords(gutils.after(self.director,">"))

	def get_plot(self):
		storyid = gutils.trim(self.page, 'sid=', '">')
		story_page = self.open_page(url="http://www.ofdb.de/view.php?page=inhalt&fid=%s&sid=%s" % (str(self.movie_id),storyid))
		self.plot = gutils.trim(story_page, "</b><br><br>","</")

	def get_year(self):
		self.year = gutils.trim(self.page,"""Erscheinungsjahr: 
              </font></td>
            <td>&nbsp;&nbsp;</td>
            <td><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b><a href="view.php?page=blaettern&Kat=Jahr&Text=""","</a></b></font></td>")
		self.year = string.capwords(gutils.after(self.year,"\">"))

	def get_runtime(self):
		self.runtime = string.capwords(gutils.trim(self.page,"<b class=\"ch\">Runtime:</b>"," min") )

	def get_genre(self):
		self.genre = gutils.trim(self.page,"""Genre(s):</font></td>
            <td>&nbsp;&nbsp;</td>
            <td nowrap><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b>""","</b></font></td>")
		self.genre = string.replace( self.genre, "<br>", ", " )
		self.genre = string.replace( self.genre, "/", ", " )
		self.genre = self.genre[0:-2]

	def get_cast(self):
		cast_page = self.open_page(url="http://www.ofdb.de/view.php?page=film_detail&fid=%s" % str(self.movie_id) )
		self.cast = ""
		self.cast = gutils.trim(cast_page,"Darsteller</i>","<td></td>\n</tr>\n</table>\n<br>")
		self.cast = string.strip(gutils.strip_tags(self.cast))
		self.cast = string.replace(self.cast,"&nbsp;", "")
		self.cast = string.replace(self.cast, "  ", "")
		self.cast = string.replace(self.cast, "\t", "")
		self.cast = string.replace(self.cast, "\n\n", "\n")
		self.cast = string.replace(self.cast, "\n\n", "")

	def get_classification(self):
		# ofdb.de got no classification
		self.classification = ""

	def get_studio(self):
		self.studio = ""

	def get_o_site(self):
		self.o_site = ""

	def get_site(self):
		self.site = "http://www.ofdb.de/view.php?page=film&fid=" + str(self.movie_id)

	def get_trailer(self):
		self.trailer = ""

	def get_country(self):
		self.country = gutils.trim(self.page,"""Herstellungsland: 
              </font></td>
            <td>&nbsp;&nbsp;</td>
            <td><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b><a href="view.php?page=blaettern&Kat=Land&Text=""","</a>")
		self.country = gutils.after(self.country,"\">")

	def get_rating(self):
		self.rating = gutils.trim(self.page,"<br>Note: ","&nbsp;")
		if self.rating == '':
			self.rating = "0"
		self.rating = str(round(float(self.rating)))

class SearchPlugin(movie.SearchMovie):
	def __init__(self):
		self.original_url_search    = "http://www.ofdb.de/view.php?page=suchergebnis&Kat=Titel&SText="
		self.translated_url_search    = "http://www.ofdb.de/view.php?page=suchergebnis&Kat=Titel&SText="
		self.encode='iso-8859-1'

	def search(self,parent_window):
		self.open_search(parent_window)
		self.page = gutils.trim(self.page,"</b><br><br>", "<br><br><br>");
		self.page = string.replace( self.page, "'", '"' )
		self.page = string.replace( self.page, '<font size="1">', '' )
		self.page = string.replace( self.page, '</font>', '' )
		return self.page

	def get_searches(self):
		elements = string.split(self.page,"<br>")

		if (elements[0]<>''):
			for element in elements:
				elementid = gutils.digits_only( gutils.trim(element,'<a href="view.php?page=film&fid=','">') )
				if elementid != 0:
					self.ids.append(elementid)
					self.titles.append(gutils.trim(element,">","</a>"))

