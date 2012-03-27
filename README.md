#Griffith 0.13.0 README

This document was last updated on Thu Jun 10 2009.  
Please see the file COPYING for licensing and warranty information.  
The latest version of this software is available at the following URL:  
http://www.griffith.cc/  


##Table of Contents

* Introduction
* System Requirements
* Installation
* Reporting Bugs
* TODO list
* About the Authors


##Introduction

Griffith is a film collection manager, released under the GNU/GPL License.


##System Requirements

<table>
  <thead><tr><td>Name</td><td>Minimum version</td><td>NOTE</td></tr></thead>
  <tr><td><a href="http://www.python.org/">Python</a></td><td>2.5 or higher</td><td></td></tr>
  <tr><td><a href="http://www.gtk.org/">GTK+</a></td><td>tested on 2.8.6</td><td></td></tr>
  <tr><td><a href="http://www.pygtk.org/">PyGTK (with glade3)</a></td><td>2.6.8</td><td></td></tr>
  <tr><td><a href="http://www.sqlalchemy.org/">SQLAlchemy</a></td><td>0.5</td><td></td></tr>
  <tr><td><a href="http://initd.org/tracker/pysqlite">pysqlite2</a></td><td>2</td><td>Python 2.5's sqlite3 module will be used if available</td></tr>
  <tr><td><a href="http://www.pythonware.com/products/pil/">PIL</a></td><td></td><td></td></tr>
  <tr><td><a href="http://www.reportlab.org">ReportLab</a></td><td>1.19</td><td></td></tr>
</table>

##Other (optional) dependencies:

<table>
  <tr><td>PostgreSQL support</td><td><a href="http://initd.org/tracker/psycopg/wiki/PsycopgTwo">Psycopg2</a></td><td>2</td></tr>
  <tr><td>MySQL support</td><td><a href="http://sourceforge.net/projects/mysql-python">MySQLDb</a></td><td></td></tr>
  <tr><td>Upgrading from Griffith &lt;= 0.6.2<br />(only if pysqlite 1.0 was used before, 1.1 is not needed)</td><td>pysqlite</td><td>1.0 </td></tr>
  <tr><td>Encoding detection of imported CSV file support</td><td><a href="http://chardet.feedparser.org/">chardet</a></td><td></td></tr>
  <tr><td>Gtkspell</td><td>python-gnome-extras</td><td></td></tr>
  <tr><td>Covers and reports support</td><td>PDF reader</td><td></td></tr>
</table>

##To check dependencies:

    $ ./griffith --check-dep

##To show detected Python modules versions:

    $ ./griffith --show-dep

Windows installer includes all the needed requirements.  
A GTK+ runtime is not necessary when using this installer.  


##External databases

You need to prepare a new database and a new user by yourself

###PostgreSQL

	CREATE USER griffith UNENCRYPTED PASSWORD 'gRiFiTh' NOCREATEDB NOCREATEUSER;
	CREATE DATABASE griffith WITH OWNER = griffith ENCODING = 'UNICODE';
	GRANT ALL ON DATABASE griffith TO griffith;

###MySQL

	CREATE DATABASE `griffith` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
	CREATE USER 'griffith'@'localhost' IDENTIFIED BY 'gRiFiTh';
	CREATE USER 'griffith'@'%' IDENTIFIED BY 'gRiFiTh';
	GRANT ALL ON `griffith` . * TO 'griffith'@'localhost';
	GRANT ALL ON `griffith` . * TO 'griffith'@'%';

###Microsoft SQL Server
	CREATE DATABASE griffith
	EXEC sp_addlogin @loginame='griffith', @passwd='gRiFiTh', @defdb='griffith'
	GO
	USE griffith
	EXEC sp_changedbowner @loginame='griffith'


##Installation

See INSTALL file


##Reporting Bugs
	
If you want to help or report any bugs founded please visit:  
  http://www.griffith.cc/  
or  
  https://bugs.launchpad.net/griffith/


##TODO

See TODO file


##About the Authors

See AUTHORS file
