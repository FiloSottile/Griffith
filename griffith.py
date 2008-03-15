#!/usr/bin/env python
# -*- coding: utf-8 -*-

__revision__ = '$Id: $'

# Copyright (c) 2005-2008 Vasco Nunes, Piotr Ożarowski

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

# ================================
# Note: indentations with 4 spaces. This is how wxGlade likes to generate files...
# ================================

# set the PATH
import sys, os.path

lib = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), 'lib'))
if os.path.isdir(lib):
    sys.path.append(lib)
del lib

# check dependencies
from gutils import get_dependencies
(required, extra) = get_dependencies()
missing = []
for i in required:
    if i['version'] is False or (i['version'] is not True and i['version'][0] == '-'):
        missing.append(i)
if len(missing) > 0:
    print 'Error: missing modules:'
    for i in missing:
        print "%(module)s" % i,
        if i.has_key('module_req'):
            print "\t:: required version: %(module_req)s" % i,
            if i['version'] is not False and i['version'][0] == '-':
                print "\t:: detected: %(version)s" % i
        print "\n",
    sys.exit(1)
del missing

# other imports
import wx
import MainFrame


# begin wxGlade: extracode
# end wxGlade

class GriffithApp(wx.App):
    def OnInit(self):
        # show a splashscreen
        image = wx.Image("images/splash.bmp", wx.BITMAP_TYPE_BMP)
        bmp = image.ConvertToBitmap()
        wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN |
            wx.SPLASH_TIMEOUT, 2000, None, -1)
        wx.Yield()
        wx.InitAllImageHandlers()
        main_frame = MainFrame.MainFrame(None, -1, "")
        self.SetTopWindow(main_frame)
        main_frame.Show()
        return 1

# end of class GriffithApp

if __name__ == "__main__":
    import gettext
    gettext.install("griffith") # replace with the appropriate catalog name
    griffith = GriffithApp(0)
    griffith.MainLoop()