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
plugin_author = "Christian Sagmueller"
plugin_author_email = ""
plugin_version = "0.2"

class Plugin(movie.Movie):
    def __init__(self, id):
        self.encode='iso-8859-1'
        self.movie_id = id
        print id
        self.url = "http://www.ofdb.de/view.php?page=film&fid=" + str(self.movie_id)
        
    def picture(self):
        self.picture_url = "http://www.ofdb.de/images/film/" + gutils.trim( self.page, "<img src=\"images/film/", "\"" )
#        self.picture_url = "http://www.ofdb.de/" + gutils.trim(self.page,"""<td><!-- Linke Spalte -->
#	<table border="0" cellspacing="0" cellpadding="0">
#	<tr valign="top">
#	<td>
#	  <img src=\"""","\"")
    def original_title(self):
        self.original_title = string.capwords(gutils.trim(self.page,"""Originaltitel:</font></td>
            <td>&nbsp;&nbsp;</td>
            <td width="99%"><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b>""","<") )
    
    def title(self):
        self.title = self.original_title
        
    def director(self):
        
        self.director = gutils.trim(self.page,"""Regie: 
              </font></td>
            <td>&nbsp;&nbsp;</td>
            <td><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b><a href="view.php?page=liste&Name=""","</a><br>")
        self.director = string.capwords(gutils.after(self.director,">"))
        
    def plot(self):
        self.plot = gutils.trim(self.page,"<b>Inhalt:</b>", "<")
        
    def year(self):
        self.year = gutils.trim(self.page,"""Erscheinungsjahr: 
              </font></td>
            <td>&nbsp;&nbsp;</td>
            <td><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b><a href="view.php?page=blaettern&Kat=Jahr&Text=""","</a></b></font></td>")
        self.year = string.capwords(gutils.after(self.year,"\">"))
        
    def running_time(self):
        self.running_time = string.capwords(gutils.trim(self.page,"<b class=\"ch\">Runtime:</b>"," min") )
        
    def genre(self):
        self.genre = gutils.trim(self.page,"""Genre(s):</font></td>
            <td>&nbsp;&nbsp;</td>
            <td nowrap><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b>""","</b></font></td>")
        self.genre = string.replace( self.genre, "<br>", ", " )
        self.genre = string.replace( self.genre, "/", ", " )
        self.genre = string.capwords(self.genre)
        
    def with(self):
        self.with = ""
        self.with = gutils.trim(self.page,"""Darsteller: 
              </font></td>
            <td>&nbsp;&nbsp;</td>
            <td><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b>""","</b></font></td>")
        self.with = string.replace(self.with,"</a><br>", ", ")
        self.with = string.strip(gutils.strip_tags(self.with))
        
    def classification(self):
        self.classification = gutils.trim(self.page,"MPAA</a>:</b> ",".<br>")
        self.classification = ""
        
    def studio(self):
        self.studio = ""
        
    def site(self):
        self.site = ""
        
    def imdb(self):
        self.imdb = "http://www.ofdb.de/view.php?page=film&fid=" + str(self.movie_id)
        
    def trailer(self):
        self.trailer = ""
        
    def country(self):
        self.country = gutils.trim(self.page,"""Herstellungsland: 
              </font></td>
            <td>&nbsp;&nbsp;</td>
            <td><font face="Arial,Helvetica,sans-serif" size="2" class="Daten"><b><a href="view.php?page=blaettern&Kat=Land&Text=""","</a>")
        self.country = string.capwords(gutils.after(self.country,"\">"))
        
    def rating(self):
        self.rating = gutils.trim(self.page,"<br>Note: ","&nbsp;")
        if self.rating == '':
            self.rating = "0"
        self.rating = str(float(self.rating))
        
class SearchPlugin(movie.SearchMovie):

    def __init__(self):
        self.original_url_search    = "http://www.ofdb.de/view.php?page=erwblaettern&Kat=Film&Land=-&Alter=-&Titel="
        self.translated_url_search    = "http://www.ofdb.de/view.php?page=erwblaettern&Kat=Film&Land=-&Alter=-&Titel="
        
    def search(self,parent_window):
        self.open_search(parent_window)
        self.sub_search()
        return self.page
        
    def sub_search(self):
        self.page = gutils.trim(self.page,"</font><br><br><br>", "<br></font></p>");
        
    def get_searches(self):
        self.elements = string.split(self.page,"<br>")
        
        if (self.elements[0]<>''):
            for element in self.elements:
                self.ids.append(gutils.trim(element,"<a href='view.php?page=film&fid=","'>"))
                self.titles.append(gutils.trim(element,">","</a>"))
        else:
            pass
