# -*- coding: UTF-8 -*-

__revision__ = '$Id$'

# Copyright (c) 2005-2008 Vasco Nunes, Piotr Ożarowski
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

# these are the only to be "true" cross-platform
# other like license, icon, homepage...
# have different behaviors under different platforms

import version, wx

def display_about():
	info = wx.AboutDialogInfo()
	info.SetName(version.pname)
	info.SetVersion(version.pversion)
	info.SetDescription(version.pdescription)
	info.SetCopyright(u"\u00A9" + version.pyear + "\n" + version.pauthor)
	info.AddDeveloper("Vasco Nunes")
	info.AddDeveloper("Piotr Ozarowski")
	info.AddDeveloper("Jessica Katharina Parth")
	info.AddDeveloper("Michael Jahn")
	info.AddArtist('Paulo Bruckmann')
	info.AddArtist('dragonskulle')
	info.AddTranslator(_("See TRANSLATORS file"))
	wx.AboutBox(info)