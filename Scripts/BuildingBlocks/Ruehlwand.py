# OpenLexocad libraries
# version 2.0   07.05.2020

# attributes
#   version 2.0
#   - innovations applied

# ========================================
# ====  Supported by Roman Davydiuk   ====
# ====  Mail: davydjukroman@gmail.com ====
# ====  Skype: live:davydjukroman     ====
# ========================================
# Script GUID : {sjds2394s92fs032jjrl}

import collections
import os
import math
import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd
import Base, Core, Draw, Geom, Topo, PartCommands

cstr  = Base.StringTool.toStlString
lxstr = Base.StringTool.toString

app = lx.Application.getInstance()
doc = app.getActiveDocument()
uiapp = ui.UIApplication.getInstance()
uidoc = uiapp.getUIDocument(doc)
sel = uidoc.getSelection()

epsilon = 0.0001
pi2 = math.pi * 0.5

# Python dictionary of all profiles listed in Lexocad...
profiles = collections.OrderedDict()

profiles.update({'HEA 100': {'h': 96E-03, 'b': 100E-03, 's': 5.0E-03, 't': 8.0E-03, 'r': 12.0E-03}})
profiles.update({'HEA 120': {'h': 114E-03, 'b': 120E-03, 's': 5.0E-03, 't': 8.0E-03, 'r': 12.0E-03}})
profiles.update({'HEA 140': {'h': 133E-03, 'b': 140E-03, 's': 5.5E-03, 't': 8.5E-03, 'r': 12.0E-03}})
profiles.update({'HEA 160': {'h': 152E-03, 'b': 160E-03, 's': 6.0E-03, 't': 9.0E-03, 'r': 15.0E-03}})
profiles.update({'HEA 180': {'h': 171E-03, 'b': 180E-03, 's': 6.0E-03, 't': 9.5E-03, 'r': 15.0E-03}})
profiles.update({'HEA 200': {'h': 190E-03, 'b': 200E-03, 's': 6.5E-03, 't': 10.0E-03, 'r': 18.0E-03}})
profiles.update({'HEA 220': {'h': 210E-03, 'b': 220E-03, 's': 7.0E-03, 't': 11.0E-03, 'r': 18.0E-03}})
profiles.update({'HEA 240': {'h': 230E-03, 'b': 240E-03, 's': 7.5E-03, 't': 12.0E-03, 'r': 21.0E-03}})
profiles.update({'HEA 260': {'h': 250E-03, 'b': 260E-03, 's': 7.5E-03, 't': 12.5E-03, 'r': 24.0E-03}})
profiles.update({'HEA 280': {'h': 270E-03, 'b': 280E-03, 's': 8.0E-03, 't': 13.0E-03, 'r': 24.0E-03}})
profiles.update({'HEA 300': {'h': 290E-03, 'b': 300E-03, 's': 8.5E-03, 't': 14.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 320': {'h': 310E-03, 'b': 300E-03, 's': 9.0E-03, 't': 15.5E-03, 'r': 27.0E-03}})
profiles.update({'HEA 340': {'h': 330E-03, 'b': 300E-03, 's': 9.5E-03, 't': 16.5E-03, 'r': 27.0E-03}})
profiles.update({'HEA 360': {'h': 350E-03, 'b': 300E-03, 's': 10.0E-03, 't': 17.5E-03, 'r': 27.0E-03}})
profiles.update({'HEA 400': {'h': 390E-03, 'b': 300E-03, 's': 11.0E-03, 't': 19.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 450': {'h': 440E-03, 'b': 300E-03, 's': 11.5E-03, 't': 21.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 500': {'h': 490E-03, 'b': 300E-03, 's': 12.0E-03, 't': 23.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 550': {'h': 540E-03, 'b': 300E-03, 's': 12.5E-03, 't': 24.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 600': {'h': 590E-03, 'b': 300E-03, 's': 13.0E-03, 't': 25.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 650': {'h': 640E-03, 'b': 300E-03, 's': 13.5E-03, 't': 26.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 700': {'h': 690E-03, 'b': 300E-03, 's': 14.5E-03, 't': 27.0E-03, 'r': 27.0E-03}})
profiles.update({'HEA 800': {'h': 790E-03, 'b': 300E-03, 's': 15.0E-03, 't': 28.0E-03, 'r': 30.0E-03}})
profiles.update({'HEA 900': {'h': 890E-03, 'b': 300E-03, 's': 16.0E-03, 't': 30.0E-03, 'r': 30.0E-03}})
profiles.update({'HEA 1000': {'h': 990E-03, 'b': 300E-03, 's': 16.5E-03, 't': 31.0E-03, 'r': 30.0E-03}})
profiles.update({'HEAA 100': {'h': 91E-03, 'b': 100E-03, 's': 4.2E-03, 't': 5.5E-03, 'r': 12.0E-03}})
profiles.update({'HEAA 120': {'h': 109E-03, 'b': 120E-03, 's': 4.2E-03, 't': 5.5E-03, 'r': 12.0E-03}})
profiles.update({'HEAA 140': {'h': 128E-03, 'b': 140E-03, 's': 4.3E-03, 't': 6.0E-03, 'r': 12.0E-03}})
profiles.update({'HEAA 160': {'h': 148E-03, 'b': 160E-03, 's': 4.5E-03, 't': 7.0E-03, 'r': 15.0E-03}})
profiles.update({'HEAA 180': {'h': 167E-03, 'b': 180E-03, 's': 5.0E-03, 't': 7.5E-03, 'r': 15.0E-03}})
profiles.update({'HEAA 200': {'h': 186E-03, 'b': 200E-03, 's': 5.5E-03, 't': 8.0E-03, 'r': 18.0E-03}})
profiles.update({'HEAA 220': {'h': 205E-03, 'b': 220E-03, 's': 6.0E-03, 't': 8.5E-03, 'r': 18.0E-03}})
profiles.update({'HEAA 240': {'h': 224E-03, 'b': 240E-03, 's': 6.5E-03, 't': 9.0E-03, 'r': 21.0E-03}})
profiles.update({'HEAA 260': {'h': 244E-03, 'b': 260E-03, 's': 6.5E-03, 't': 9.5E-03, 'r': 24.0E-03}})
profiles.update({'HEAA 280': {'h': 264E-03, 'b': 280E-03, 's': 7.0E-03, 't': 10.0E-03, 'r': 24.0E-03}})
profiles.update({'HEAA 300': {'h': 283E-03, 'b': 300E-03, 's': 7.5E-03, 't': 10.5E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 320': {'h': 301E-03, 'b': 300E-03, 's': 8.0E-03, 't': 11.0E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 340': {'h': 320E-03, 'b': 300E-03, 's': 8.5E-03, 't': 11.5E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 360': {'h': 339E-03, 'b': 300E-03, 's': 9.0E-03, 't': 12.0E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 400': {'h': 378E-03, 'b': 300E-03, 's': 9.5E-03, 't': 13.0E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 450': {'h': 425E-03, 'b': 300E-03, 's': 10.0E-03, 't': 13.5E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 500': {'h': 472E-03, 'b': 300E-03, 's': 10.5E-03, 't': 14.0E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 550': {'h': 522E-03, 'b': 300E-03, 's': 11.5E-03, 't': 15.0E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 600': {'h': 571E-03, 'b': 300E-03, 's': 12.0E-03, 't': 15.5E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 650': {'h': 620E-03, 'b': 300E-03, 's': 12.5E-03, 't': 16.0E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 700': {'h': 670E-03, 'b': 300E-03, 's': 13.0E-03, 't': 17.0E-03, 'r': 27.0E-03}})
profiles.update({'HEAA 800': {'h': 770E-03, 'b': 300E-03, 's': 14.0E-03, 't': 18.0E-03, 'r': 30.0E-03}})
profiles.update({'HEAA 900': {'h': 870E-03, 'b': 300E-03, 's': 15.0E-03, 't': 20.0E-03, 'r': 30.0E-03}})
profiles.update({'HEAA 1000': {'h': 970E-03, 'b': 300E-03, 's': 16.0E-03, 't': 21.0E-03, 'r': 30.0E-03}})
profiles.update({'HEB 100': {'h': 100E-03, 'b': 100E-03, 's': 6.0E-03, 't': 10.0E-03, 'r': 12.0E-03}})
profiles.update({'HEB 120': {'h': 120E-03, 'b': 120E-03, 's': 6.5E-03, 't': 11.0E-03, 'r': 12.0E-03}})
profiles.update({'HEB 140': {'h': 140E-03, 'b': 140E-03, 's': 7.0E-03, 't': 12.0E-03, 'r': 12.0E-03}})
profiles.update({'HEB 160': {'h': 160E-03, 'b': 160E-03, 's': 8.0E-03, 't': 13.0E-03, 'r': 15.0E-03}})
profiles.update({'HEB 180': {'h': 180E-03, 'b': 180E-03, 's': 8.5E-03, 't': 14.0E-03, 'r': 15.0E-03}})
profiles.update({'HEB 200': {'h': 200E-03, 'b': 200E-03, 's': 9.0E-03, 't': 15.0E-03, 'r': 18.0E-03}})
profiles.update({'HEB 220': {'h': 220E-03, 'b': 220E-03, 's': 9.5E-03, 't': 16.0E-03, 'r': 18.0E-03}})
profiles.update({'HEB 240': {'h': 240E-03, 'b': 240E-03, 's': 10.0E-03, 't': 17.0E-03, 'r': 21.0E-03}})
profiles.update({'HEB 260': {'h': 260E-03, 'b': 260E-03, 's': 10.0E-03, 't': 17.5E-03, 'r': 24.0E-03}})
profiles.update({'HEB 280': {'h': 280E-03, 'b': 280E-03, 's': 10.5E-03, 't': 18.0E-03, 'r': 24.0E-03}})
profiles.update({'HEB 300': {'h': 300E-03, 'b': 300E-03, 's': 11.0E-03, 't': 19.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 320': {'h': 320E-03, 'b': 300E-03, 's': 11.5E-03, 't': 20.5E-03, 'r': 27.0E-03}})
profiles.update({'HEB 340': {'h': 340E-03, 'b': 300E-03, 's': 12.0E-03, 't': 21.5E-03, 'r': 27.0E-03}})
profiles.update({'HEB 360': {'h': 360E-03, 'b': 300E-03, 's': 12.5E-03, 't': 22.5E-03, 'r': 27.0E-03}})
profiles.update({'HEB 400': {'h': 400E-03, 'b': 300E-03, 's': 13.5E-03, 't': 24.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 450': {'h': 450E-03, 'b': 300E-03, 's': 14.0E-03, 't': 26.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 500': {'h': 500E-03, 'b': 300E-03, 's': 14.5E-03, 't': 28.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 550': {'h': 550E-03, 'b': 300E-03, 's': 15.0E-03, 't': 29.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 600': {'h': 600E-03, 'b': 300E-03, 's': 15.5E-03, 't': 30.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 650': {'h': 650E-03, 'b': 300E-03, 's': 16.0E-03, 't': 31.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 700': {'h': 700E-03, 'b': 300E-03, 's': 17.0E-03, 't': 32.0E-03, 'r': 27.0E-03}})
profiles.update({'HEB 800': {'h': 800E-03, 'b': 300E-03, 's': 17.5E-03, 't': 33.0E-03, 'r': 30.0E-03}})
profiles.update({'HEB 900': {'h': 900E-03, 'b': 300E-03, 's': 18.5E-03, 't': 35.0E-03, 'r': 30.0E-03}})
profiles.update({'HEB 1000': {'h': 1000E-03, 'b': 300E-03, 's': 19.0E-03, 't': 36.0E-03, 'r': 30.0E-03}})
profiles.update({'HEM 100': {'h': 120E-03, 'b': 106E-03, 's': 12.0E-03, 't': 20.0E-03, 'r': 12.0E-03}})
profiles.update({'HEM 120': {'h': 140E-03, 'b': 126E-03, 's': 12.5E-03, 't': 21.0E-03, 'r': 12.0E-03}})
profiles.update({'HEM 140': {'h': 160E-03, 'b': 146E-03, 's': 13.0E-03, 't': 22.0E-03, 'r': 12.0E-03}})
profiles.update({'HEM 160': {'h': 180E-03, 'b': 166E-03, 's': 14.0E-03, 't': 23.0E-03, 'r': 15.0E-03}})
profiles.update({'HEM 180': {'h': 200E-03, 'b': 186E-03, 's': 14.5E-03, 't': 24.0E-03, 'r': 15.0E-03}})
profiles.update({'HEM 200': {'h': 220E-03, 'b': 206E-03, 's': 15.0E-03, 't': 25.0E-03, 'r': 18.0E-03}})
profiles.update({'HEM 220': {'h': 240E-03, 'b': 226E-03, 's': 15.5E-03, 't': 26.0E-03, 'r': 18.0E-03}})
profiles.update({'HEM 240': {'h': 270E-03, 'b': 248E-03, 's': 18.0E-03, 't': 32.0E-03, 'r': 21.0E-03}})
profiles.update({'HEM 260': {'h': 290E-03, 'b': 268E-03, 's': 18.0E-03, 't': 32.5E-03, 'r': 24.0E-03}})
profiles.update({'HEM 280': {'h': 310E-03, 'b': 288E-03, 's': 18.5E-03, 't': 33.0E-03, 'r': 24.0E-03}})
profiles.update({'HEM 300': {'h': 340E-03, 'b': 310E-03, 's': 21.0E-03, 't': 39.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 320': {'h': 359E-03, 'b': 309E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 340': {'h': 377E-03, 'b': 309E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 360': {'h': 395E-03, 'b': 308E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 400': {'h': 432E-03, 'b': 307E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 450': {'h': 478E-03, 'b': 307E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 500': {'h': 524E-03, 'b': 306E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 550': {'h': 572E-03, 'b': 306E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 600': {'h': 620E-03, 'b': 305E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 650': {'h': 668E-03, 'b': 305E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 700': {'h': 716E-03, 'b': 304E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 27.0E-03}})
profiles.update({'HEM 800': {'h': 814E-03, 'b': 303E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 30.0E-03}})
profiles.update({'HEM 900': {'h': 910E-03, 'b': 302E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 30.0E-03}})
profiles.update({'HEM 1000': {'h': 1008E-03, 'b': 302E-03, 's': 21.0E-03, 't': 40.0E-03, 'r': 30.0E-03}})
profiles.update({'HHD 60': {'h': 248E-03, 'b': 253E-03, 's': 7.0E-03, 't': 11.0E-03, 'r': 24E-03}})
profiles.update({'HHD 78': {'h': 255E-03, 'b': 255E-03, 's': 9.0E-03, 't': 14.5E-03, 'r': 24E-03}})
profiles.update({'HHD 94': {'h': 306E-03, 'b': 305E-03, 's': 9.0E-03, 't': 14.5E-03, 'r': 27E-03}})
profiles.update({'HHD 104': {'h': 265E-03, 'b': 258E-03, 's': 12.0E-03, 't': 19.5E-03, 'r': 24E-03}})
profiles.update({'HHD 118': {'h': 314E-03, 'b': 307E-03, 's': 11.0E-03, 't': 18.5E-03, 'r': 27E-03}})
profiles.update({'HHD 135': {'h': 355E-03, 'b': 369E-03, 's': 11.5E-03, 't': 17.5E-03, 'r': 27E-03}})
profiles.update({'HHD 141': {'h': 278E-03, 'b': 262E-03, 's': 16.0E-03, 't': 26.0E-03, 'r': 24E-03}})
profiles.update({'HHD 152': {'h': 360E-03, 'b': 370E-03, 's': 12.5E-03, 't': 20.0E-03, 'r': 27E-03}})
profiles.update({'HHD 155': {'h': 325E-03, 'b': 311E-03, 's': 15.0E-03, 't': 24.0E-03, 'r': 27E-03}})
profiles.update({'HHD 176': {'h': 366E-03, 'b': 372E-03, 's': 14.5E-03, 't': 23.0E-03, 'r': 27E-03}})
profiles.update({'HHD 184': {'h': 294E-03, 'b': 267E-03, 's': 21.0E-03, 't': 34.0E-03, 'r': 24E-03}})
profiles.update({'HHD 190': {'h': 369E-03, 'b': 391E-03, 's': 15.0E-03, 't': 24.0E-03, 'r': 27E-03}})
profiles.update({'HHD 199': {'h': 372E-03, 'b': 374E-03, 's': 16.5E-03, 't': 26.0E-03, 'r': 27E-03}})
profiles.update({'HHD 207': {'h': 341E-03, 'b': 316E-03, 's': 20.0E-03, 't': 32.0E-03, 'r': 27E-03}})
profiles.update({'HHD 214': {'h': 375E-03, 'b': 393E-03, 's': 17.0E-03, 't': 27.0E-03, 'r': 27E-03}})
profiles.update({'HHD 237': {'h': 381E-03, 'b': 394E-03, 's': 18.5E-03, 't': 30.0E-03, 'r': 27E-03}})
profiles.update({'HHD 240': {'h': 314E-03, 'b': 273E-03, 's': 27.0E-03, 't': 44.0E-03, 'r': 24E-03}})
profiles.update({'HHD 262': {'h': 387E-03, 'b': 396E-03, 's': 20.5E-03, 't': 33.0E-03, 'r': 27E-03}})
profiles.update({'HHD 274': {'h': 361E-03, 'b': 322E-03, 's': 26.0E-03, 't': 42.0E-03, 'r': 27E-03}})
profiles.update({'HHD 287': {'h': 393E-03, 'b': 398E-03, 's': 22.5E-03, 't': 36.0E-03, 'r': 27E-03}})
profiles.update({'HHD 308': {'h': 371E-03, 'b': 325E-03, 's': 29.0E-03, 't': 47.0E-03, 'r': 27E-03}})
profiles.update({'HHD 312': {'h': 399E-03, 'b': 400E-03, 's': 24.5E-03, 't': 39.0E-03, 'r': 27E-03}})
profiles.update({'HHD 333': {'h': 346E-03, 'b': 282E-03, 's': 36.0E-03, 't': 60.0E-03, 'r': 24E-03}})
profiles.update({'HHD 337': {'h': 405E-03, 'b': 402E-03, 's': 26.5E-03, 't': 42.0E-03, 'r': 27E-03}})
profiles.update({'HHD 350': {'h': 383E-03, 'b': 329E-03, 's': 33.0E-03, 't': 53.0E-03, 'r': 27E-03}})
profiles.update({'HHD 370': {'h': 413E-03, 'b': 405E-03, 's': 29.0E-03, 't': 46.0E-03, 'r': 27E-03}})
profiles.update({'HHD 404': {'h': 421E-03, 'b': 407E-03, 's': 31.5E-03, 't': 50.0E-03, 'r': 27E-03}})
profiles.update({'HHD 435': {'h': 407E-03, 'b': 336E-03, 's': 40.0E-03, 't': 65.0E-03, 'r': 27E-03}})
profiles.update({'HHD 446': {'h': 431E-03, 'b': 410E-03, 's': 34.5E-03, 't': 55.0E-03, 'r': 27E-03}})
profiles.update({'HHD 488': {'h': 441E-03, 'b': 413E-03, 's': 37.5E-03, 't': 60.0E-03, 'r': 27E-03}})
profiles.update({'HHD 531': {'h': 451E-03, 'b': 416E-03, 's': 40.5E-03, 't': 65.0E-03, 'r': 27E-03}})
profiles.update({'HHD 577': {'h': 461E-03, 'b': 420E-03, 's': 44.0E-03, 't': 70.0E-03, 'r': 27E-03}})
profiles.update({'HHD 621': {'h': 471E-03, 'b': 423E-03, 's': 47.0E-03, 't': 75.0E-03, 'r': 27E-03}})
profiles.update({'HHD 685': {'h': 481E-03, 'b': 431E-03, 's': 55.0E-03, 't': 80.0E-03, 'r': 27E-03}})

# Für die erweiterung der Liste kann profiles upgedatet werden und types müsssen angepasst werden, falls ein neuer Typ entsteht.
# Zudem muss bei den Leerzeichen aufgepasst werden => Bsp LARSSEN 22_10  !!!!!
types = ['HEA', 'HEAA', 'HEB', 'HEM', 'HHD']

typ2 = []

list1 = list(profiles.keys())

for i in range(0, len(list1)):
    list2 = list1[i].split(' ')
    for j in range(0, len(types)):
        if list2[0] == types[j]:
            typ2.append([list2[0], list2[1]])

#=====================================================================================================================
def vecsAreSame(v1, v2, tolerance=epsilon):
    if math.fabs(v1.x() - v2.x()) > tolerance:
        return False

    if math.fabs(v1.y() - v2.y()) > tolerance:
        return False

    return bool(math.fabs(v1.z() - v2.z()) <= tolerance)


def qstr(str):
    return Base.StringTool.toQString(lxstr(str))

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

def baseVecTranslate(pt, baseVec, dist):
    return Geom.Pnt(
        pt.x() + (baseVec.x() * dist),
        pt.y() + (baseVec.y() * dist),
        pt.z() + (baseVec.z() * dist)
    )

def printVal(name, val):
    print("{} = {}".format(name, val))

def printVec(name, val):
    print("{}: ({}, {}, {})".format(name, val.x(), val.y(), val.z()))

def printPolyline(name, ptList):
    print("{}:".format(name))

    for pt in ptList:
        print("    ({}, {}, {})".format(pt.x(), pt.y(), pt.z()))

def printElemHierarchy(name, rootElem):
    outStr = name + ":\n  "
    outStr += rootElem + "\n"

    subElemList = rootElem.getSubElements()
    for subElem in subElemList:
        outStr += "  |-" + subElem + "\n"

    print(outStr)

# Helper functions for easier model assembly
def vecHAngle(xCoord, yCoord):
    if yCoord > epsilon:
        if xCoord > epsilon:
            return math.atan(yCoord / xCoord)
        elif xCoord < -epsilon:
            return math.pi + math.atan(yCoord / xCoord)
        else:
            return pi2
    elif yCoord < -epsilon:
        if xCoord > epsilon:
            return math.atan(yCoord / xCoord)
        elif xCoord < -epsilon:
            return -math.pi + math.atan(yCoord / xCoord)
        else:
            return -pi2
    else:
        if xCoord > -epsilon:
            return 0.0
        else:
            return math.pi

def vecVAngle(length, zCoord):
    if length < epsilon:
        return 0.0

    return math.asin(zCoord / length)

def angleVec(vec):
    vecLen = vec.magnitude()

    angleH = vecHAngle(vec.x(), vec.y())
    angleV = vecVAngle(vecLen, vec.z())

    return angleH, -angleV

def vecMagnitude2D(vec):
    return math.sqrt(vec.x() * vec.x() + vec.y() * vec.y())

def vecHExpandXZ(unitVec, hLength):
    if math.fabs(unitVec.z()) > epsilon:
        z = (hLength * unitVec.z()) / unitVec.x()
        return Geom.Vec(hLength, 0.0, z)
    else:
        return Geom.Vec(hLength, 0.0, 0.0)

class PolylineData:
    SegmType_Line = 0
    SegmType_Arc = 1

    _closedSuffix = "_closed"
    _ptListSuffix = "_points"
    _edgeListSuffix = "_edges"

    class _Segment:
        def __init__(self, type, data):
            self.type = type
            self.data = data

    class _LineSegmData:
        def __init__(self, startIndex, closeSegm=False):
            self.startIndex = startIndex

            if not closeSegm:
                self.endIndex = startIndex + 1
            else:
                self.endIndex = 0

    class _ArcSegmData:
        def __init__(self, ptList, p1Index, closeSegm=False):
            self.p1Index = p1Index
            self.p2Index = p1Index + 1
            if not closeSegm:
                self.p3Index = p1Index + 2
            else:
                self.p3Index = 0

            self.arc = Arc3Pnt(ptList[self.p1Index], ptList[self.p2Index], ptList[self.p3Index])

    def __init__(self):
        self._closed = False

        self._ptList = []
        self._segmList = []

    @staticmethod
    def fromElement(lineElem):
        newPD = PolylineData()

        firstEdge = True
        startIndex = 0
        for edgeIndex in range(len(lineElem)):
            # edge = edges[edgeIndex]
            #
            # edgeTypeRes = Topo.EdgeTool.getGeomCurveType(edge)
            # if not edgeTypeRes.ok:
            #     raise RuntimeError("Can't get edge type")

            if lineElem[edgeIndex][0] == PolylineData.SegmType_Line:
                p1Res = lineElem[edgeIndex][1]
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res))
                    firstEdge = False

                p2Res = lineElem[edgeIndex][2]
                newPD._ptList.append(Geom.Pnt(p2Res))

                segmData = PolylineData._LineSegmData(startIndex, False)
                newPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

                startIndex += 1
            elif lineElem[edgeIndex][0] == PolylineData.SegmType_Arc:
                p1Res = lineElem[edgeIndex][1]
                if firstEdge:
                    newPD._ptList.append(Geom.Pnt(p1Res))
                    firstEdge = False

                p2Res = lineElem[edgeIndex][2]
                newPD._ptList.append(Geom.Pnt(p2Res))

                p3Res = lineElem[edgeIndex][3]
                newPD._ptList.append(Geom.Pnt(p3Res))

                segmData = PolylineData._ArcSegmData(newPD._ptList, startIndex, False)
                newPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

                startIndex += 2
            else:
                raise RuntimeError("Unsupported edge type")


        i_n = len(lineElem[len(lineElem) - 1]) - 1
        newPD._closed = lineElem[len(lineElem) - 1][i_n]
        return newPD

    def isClosed(self):
        return self._closed

    def pointCount(self):
        return len(self._ptList)

    def point(self, id):
        return self._ptList[id]

    def segmentCount(self):
        return len(self._segmList)

    def segmentType(self, id):
        return self._segmList[id].type

    def segmStartPt(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
        else:
            startPtId = self._segmList[id].data.p1Index

        return self._ptList[startPtId]

    def segmStartTangent(self, id, normalize=False):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
            endPtId = self._segmList[id].data.endIndex

            tangVec = Geom.Vec(self._ptList[startPtId], self._ptList[endPtId])
            if normalize:
                tangVec.normalize()

            return tangVec
        else:
            return self._segmList[id].data.arc.startTangent()

    def segmStartBisector(self, id, normalize=False):
        if id <= 0:
            return self.segmStartTangent(id, normalize)
        else:
            prevTang = self.segmEndTangent(id - 1, True)
            currTang = self.segmStartTangent(id, True)

            bisect = prevTang + currTang
            if normalize:
                bisect.normalize()

            return bisect

    def segmEndPt(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.endIndex
        else:
            startPtId = self._segmList[id].data.p3Index

        return self._ptList[startPtId]

    def segmEndTangent(self, id, normalize=False):
        if self._segmList[id].type == PolylineData.SegmType_Line:
            startPtId = self._segmList[id].data.startIndex
            endPtId = self._segmList[id].data.endIndex

            tangVec = Geom.Vec(self._ptList[endPtId], self._ptList[startPtId])
            if normalize:
                tangVec.normalize()

            return tangVec
        else:
            return -self._segmList[id].data.arc.endTangent()

    def segmEndBisector(self, id, normalize=False):
        lastSegmId = len(self._segmList)
        if id >= lastSegmId:
            return self.segmEndTangent(id, normalize)
        else:
            currTang = self.segmEndTangent(id, True)
            nextTang = self.segmStartTangent(id + 1, True)

            bisect = currTang + nextTang
            if normalize:
                bisect.normalize()

            return bisect

    def segmArc(self, id):
        if self._segmList[id].type == PolylineData.SegmType_Arc:
            return self._segmList[id].data.arc
        else:
            raise TypeError("Segment is not of arc type")

    def _buildEdgeList(self):
        edgeList = []

        for edge in self._segmList:
            edgeList.append(int(edge.type))

        return edgeList

    def _buildSegmentList(self, edgeList):
        self._segmList = []

        segmCount = len(edgeList)
        lastSegmId = segmCount

        startIndex = 0
        for edge in range(lastSegmId):
            edgeType = edgeList[edge]

            if edgeType == PolylineData.SegmType_Line:
                segmData = PolylineData._LineSegmData(startIndex, False)
                self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))

                startIndex += 1
            elif edgeType == PolylineData.SegmType_Arc:
                segmData = PolylineData._ArcSegmData(self._ptList, startIndex, False)
                self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))

                startIndex += 2
            else:
                self._segmList = None
                return

        # Last edge
        edgeType = edgeList[lastSegmId]

        if edgeType == PolylineData.SegmType_Line:
            segmData = PolylineData._LineSegmData(startIndex, self._closed)
            self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, segmData))
        elif edgeType == PolylineData.SegmType_Arc:
            segmData = PolylineData._ArcSegmData(self._ptList, startIndex, self._closed)
            self._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, segmData))
        else:
            self._segmList = None
            return

    @staticmethod
    def prepareParamSet(paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        paramSet.setParameter(closedParamName, False)
        paramSet.setParameter(ptListParamName, None)
        paramSet.setParameter(edgeListParamName, None)

    def writeIntoParamSet(self, paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        paramSet.setParameter(closedParamName, self._closed, False)
        paramSet.setParameter(ptListParamName, self._ptList, False)
        paramSet.setParameter(edgeListParamName, self._buildEdgeList(), False)

    @staticmethod
    def fromParamSet(paramSet, name):
        closedParamName = name + PolylineData._closedSuffix
        ptListParamName = name + PolylineData._ptListSuffix
        edgeListParamName = name + PolylineData._edgeListSuffix

        if not paramSet.hasParameter(closedParamName) or \
                not paramSet.hasParameter(ptListParamName) or \
                not paramSet.hasParameter(edgeListParamName):
            return None

        newPD = PolylineData()

        newPD._closed = paramSet.getBoolParameter(closedParamName)

        newPD._ptList = paramSet.getPointListParameter(ptListParamName)
        if newPD._ptList is None:
            return None

        newPD._buildSegmentList(paramSet.getIntListParameter(edgeListParamName))
        if newPD._segmList is None:
            return None

        return newPD

    def makeCopy(self):
        copyPD = PolylineData()

        copyPD._closed = self._closed

        for pt in self._ptList:
            copyPD._ptList.append(Geom.Pnt(pt))

        for segm in self._segmList:
            if segm.type == PolylineData.SegmType_Line:
                closeSegm = bool(segm.data.endIndex == 0)
                lineData = PolylineData._LineSegmData(segm.data.startIndex, closeSegm)

                copyPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Line, lineData))
            elif segm.type == PolylineData.SegmType_Arc:
                closeSegm = bool(segm.data.p3Index == 0)
                arcData = PolylineData._ArcSegmData(copyPD._ptList, segm.data.p1Index, closeSegm)

                copyPD._segmList.append(PolylineData._Segment(PolylineData.SegmType_Arc, arcData))

        return copyPD

class EditMode:
    def __init__(self, doc):
        if doc is None:
            raise RuntimeError("Document is None.")

        self._doc = doc
        self._exitEditing = False

    def __enter__(self):
        if not self._doc.isEditing():
            self._doc.beginEditing()
            self._exitEditing = True
        else:
            self._exitEditing = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._exitEditing:
            self._doc.endEditing()
            self._doc.recompute()

class ModelAssembler:
    # Beam types
    BT_Square = 0
    BT_Circle = 1

    # Beam type names
    _squareBTypeName = "square"
    _circleBTypeName = "circle"
    @staticmethod
    def correctBeamType(beamType):
        return bool(beamType == ModelAssembler.BT_Square or beamType == ModelAssembler.BT_Circle)

    @staticmethod
    def writeBeamType(bt):
        if bt == ModelAssembler.BT_Square:
            return ModelAssembler._squareBTypeName
        elif bt == ModelAssembler.BT_Circle:
            return ModelAssembler._circleBTypeName
        else:
            raise RuntimeError("Invalid beam type")

    @staticmethod
    def parseBeamType(bt):
        if bt == ModelAssembler._squareBTypeName:
            return ModelAssembler.BT_Square
        elif bt == ModelAssembler._circleBTypeName:
            return ModelAssembler.BT_Circle
        else:
            raise RuntimeError("Invalid beam type string")

    def __init__(self, doc):
        self._doc = doc
        self._modelGr = None
        self._color = None

    def beginModel(self, modelGr):
        if self._modelGr is not None:
            raise RuntimeError("beginModel() called twice")

        self._modelGr = modelGr
        if modelGr is None:
            raise RuntimeError("modelGr is NULL")

    def setColor(self, color):
        self._color = color

    def endModel(self):
        if self._modelGr is None:
            raise RuntimeError("Called endModel() before beginModel()")

        finishedModel = self._modelGr
        self._modelGr = None

        return finishedModel

    def _createBaseBeam_Square(self, length, radiusH, radiusV, angle):
        diameterH = radiusH * 2.0
        diameterV = radiusV * 2.0

        beamGeom = lx.Block.createIn(self._doc)
        beamGeom.setLength(length)
        beamGeom.setWidth(diameterH)
        beamGeom.setHeight(diameterV)

        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(beamGeom)
        if self._color is not None:
            beam.setDiffuseColor(self._color)

        beam.translate(Geom.Vec(0.0, -radiusH, -radiusV), Geom.CoordSpace_WCS)

        if math.fabs(angle) > epsilon:
            angleAxis = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(1.0, 0.0, 0.0))
            beam.rotate(angleAxis, angle, Geom.CoordSpace_WCS)

        return beam

    def _createBaseBeam_Circle(self, length, radius):
        beamGeom = lx.RightCircularCylinder .createIn(self._doc)
        beamGeom.setHeight(length)
        beamGeom.setRadius(radius)

        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(beamGeom)
        if self._color is not None:
            beam.setDiffuseColor(self._color)
        rotAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxis, math.radians(90), Geom.CoordSpace_WCS)

        return beam

    def _createBaseBeam(self, beamType, length, radiusH, radiusV, angle):
        if not ModelAssembler.correctBeamType(beamType):
            raise RuntimeError("Invalid beam type")

        if beamType == ModelAssembler.BT_Square:
            return self._createBaseBeam_Square(length, radiusH, radiusV, angle)
        else:
            if abs(radiusH - radiusV) > epsilon:
                raise RuntimeError("Radii must be equal")

            return self._createBaseBeam_Circle(length, radiusH)

    def addXBeam(self, beamType, startPt, length, radiusH, radiusV, angle=0.0):
        if self._modelGr is None:
            raise RuntimeError("Called addXBeam() before beginModel()")

        beam = self._createBaseBeam(beamType, length, radiusH, radiusV, angle)
        beam.translate(Geom.Vec(startPt.x(),
                                          startPt.y(),
                                          startPt.z()),
                                 Geom.CoordSpace_WCS)

        self._modelGr.addSubElement(beam)

    def addXBeamUniform(self, beamType, startPt, length, radius, angle=0.0):
        self.addXBeam(beamType, startPt, length, radius, radius, angle)

    def addYBeam(self, beamType, startPt, length, radiusH, radiusV, angle):
        if self._modelGr is None:
            raise RuntimeError("Called addYBeam() before beginModel()")

        beam = self._createBaseBeam(beamType, length, radiusH, radiusV, angle)

        rotAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 0, 1))
        beam.rotate(rotAxis, math.radians(90), Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(),
                                          startPt.y(),
                                          startPt.z()),
                                 Geom.CoordSpace_WCS)

        self._modelGr.addSubElement(beam)

    def addYBeamUniform(self, beamType, startPt, length, radius, angle=0.0):
        self.addYBeam(beamType, startPt, length, radius, radius, angle)

    def addZBeam(self, beamType, startPt, length, radiusH, radiusV, angle=0.0):
        if self._modelGr is None:
            raise RuntimeError("Called addZBeam() before beginModel()")

        beam = self._createBaseBeam(beamType, length, radiusH, radiusV, angle)

        rotAxis = Geom.Ax1(Geom.Pnt(0, 0, 0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxis, math.radians(-90), Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(),
                                          startPt.y(),
                                          startPt.z()),
                                 Geom.CoordSpace_WCS)

        self._modelGr.addSubElement(beam)

    def addZBeamUniform(self, beamType, startPt, length, radius, angle=0.0):
        self.addZBeam(beamType, startPt, length, radius, radius, angle)

    def addBeam(self, beamType, startPt, endPt, radiusH, radiusV, angle=0.0):
        beamVec = Geom.Vec(startPt, endPt)
        # print "beamVec = ({}, {}, {})".format(beamVec.x(), beamVec.y(), beamVec.z())
        beamLen = beamVec.magnitude()
        # myBeamLen = math.sqrt(beamVec.x() * beamVec.x() + beamVec.y() * beamVec.y() + beamVec.z() * beamVec.z())
        # print "beamLen = {}, myBeamLen = {}".format(beamLen, myBeamLen)
        beamAngleH, beamAngleV = angleVec(beamVec)
        # print "beamAngleH = {}, beamAngleV = {}".format(beamAngleH, beamAngleV)

        beam = self._createBaseBeam(beamType, beamLen, radiusH, radiusV, angle)

        rotAxisV = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxisV, beamAngleV, Geom.CoordSpace_WCS)

        rotAxisH = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1))
        beam.rotate(rotAxisH, beamAngleH, Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(),
                                          startPt.y(),
                                          startPt.z()),
                                 Geom.CoordSpace_WCS)

        self._modelGr.addSubElement(beam)

    def addBeamUniform(self, beamType, startPt, endPt, radius, angle=0.0):
        self.addBeam(beamType, startPt, endPt, radius, radius, angle)

    def addCutBeam(self, beamType, startPt, endPt, radiusH, radiusV, startVec, endVec, angle=0.0):
        beamVec = Geom.Vec(startPt, endPt)
        dir = beamVec.normalized()
        # print "beamVec = ({}, {}, {})".format(beamVec.x(), beamVec.y(), beamVec.z())
        beamLen = beamVec.magnitude()
        # myBeamLen = math.sqrt(beamVec.x() * beamVec.x() + beamVec.y() * beamVec.y() + beamVec.z() * beamVec.z())
        # print "beamLen = {}, myBeamLen = {}".format(beamLen, myBeamLen)
        beamAngleH, beamAngleV = angleVec(beamVec)
        # print "beamAngleH = {}, beamAngleV = {}".format(beamAngleH, beamAngleV)

        beam = self._createBaseBeam(beamType, beamLen+4.*radiusV, radiusH, radiusV, angle)

        rotAxisV = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 1, 0))
        beam.rotate(rotAxisV, beamAngleV, Geom.CoordSpace_WCS)

        rotAxisH = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1))
        beam.rotate(rotAxisH, beamAngleH, Geom.CoordSpace_WCS)

        beam.translate(Geom.Vec(startPt.x(), startPt.y(), startPt.z()), Geom.CoordSpace_WCS)
        trans = Geom.Vec(0.0 - 2.*radiusV*dir.x(), 0.0 - 2.*radiusV*dir.y(), 0.0 - 2.*radiusV*dir.z())
        #print()
        beam.translate(trans, Geom.CoordSpace_WCS)

        startNorm = Geom.Vec(-startVec.y(), startVec.x(), startVec.z())
        endNorm = Geom.Vec(endVec.y(), -endVec.x(), endVec.z())
        startDir = Geom.Dir(startNorm.x(), startNorm.y(), 0.0)
        endDir = Geom.Dir(endNorm)
        startPln = Geom.Pln(Geom.Pnt(startPt.x(), startPt.y(), startPt.z()), startDir)
        endPln = Geom.Pln(endPt, endDir)
        beam2 = lx.Element.createIn(self._doc)
        # beam2 = beam.getElement()
        geom = beam.getGeometry()
        beam2.setGeometry(geom)
        t = beam.getTransform()
        beam2.setTransform(t)
        doc.removeObject(beam)

        beam_start = lx.vector_Element()
        beam_end = lx.vector_Element()

        if lx.bop_splitByPlane(beam2, startPln, beam_start) != 0:
            print("Error in cut")
        doc.removeObject(beam_start[1])
        doc.removeObject(beam2)

        if lx.bop_splitByPlane(beam_start[0], endPln, beam_end) != 0:
            print("Error in cut")
        doc.removeObject(beam_start[0])
        doc.removeObject(beam_end[1])

        t = beam_end[0].getTransform()
        geom = beam_end[0].getGeometry()
        beam = lx.SubElement.createIn(self._doc)
        beam.setGeometry(geom)
        beam.setTransform(t)
        doc.removeObject(beam_end[0])
        #doc.recompute()

        self._modelGr.addSubElement(beam)

    def addHorCutBeam(self, firstPntA, secondPntA, vRadius, hRadius, firstVec, secondVec):
        firstPnt = Geom.Pnt(firstPntA.x(), firstPntA.y(), firstPntA.z() - vRadius)
        secondPnt = Geom.Pnt(secondPntA.x(), secondPntA.y(), secondPntA.z() - vRadius)
        mainVec = Geom.Vec(firstPnt, secondPnt)

        firstAngle = Geom.Vec.angle(firstVec, Geom.Vec(mainVec.x(), mainVec.y(), 0.0))
        secondAngle = Geom.Vec.angle(secondVec, Geom.Vec(mainVec.x(), mainVec.y(), 0.0))

        firstStep = hRadius / math.sin(firstAngle)
        secondStep = hRadius / math.sin(secondAngle)

        firVec = firstVec.normalized()
        secVec = secondVec.normalized()
        firVec.scale(firstStep)
        secVec.scale(secondStep)
        listPoint = []
        listPoint.append(firstPnt.translated(firVec))
        listPoint.append(firstPnt.translated(firVec.reversed()))
        listPoint.append(secondPnt.translated(secVec.reversed()))
        listPoint.append(secondPnt.translated(secVec))

        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, Geom.Dir(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(0.0, 0.0, 1.0))), vRadius * 2.0)
        geom = lx.FacetedBrep.createIn(self._doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(self._doc)
        subElem.setGeometry(geom)
        self._modelGr.addSubElement(subElem)

    @staticmethod
    def _preapareRotTransf(angle):
        angleAxis = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(1.0, 0.0, 0.0))

        rotTr = Geom.Trsf()
        if math.fabs(angle) > epsilon:
            rotTr.setRotation(angleAxis, angle)

        return rotTr

    @staticmethod
    def _addProfilePoints_Square(radiusH, radiusV, angle, vtxList):
        rotTr = ModelAssembler._preapareRotTransf(angle)

        vtx = Geom.Pnt(0.0, radiusH, radiusV)
        vtx.transform(rotTr)
        vtxList.append(vtx)

        vtx = Geom.Pnt(0.0, radiusH, -radiusV)
        vtx.transform(rotTr)
        vtxList.append(vtx)

        vtx = Geom.Pnt(0.0, -radiusH, -radiusV)
        vtx.transform(rotTr)
        vtxList.append(vtx)

        vtx = Geom.Pnt(0.0, -radiusH, radiusV)
        vtx.transform(rotTr)
        vtxList.append(vtx)

    @staticmethod
    def _findCircleDivAngle(radius, perfAngle, minEdgeLen, minVtxCount):
        twoPi = 2.0 * math.pi

        perfDivAngle = math.pi - perfAngle
        perfDivCount = math.ceil(twoPi / perfDivAngle)

        divAngle = twoPi / perfDivCount

        radiusSq = radius * radius
        minEdgeLenSq = minEdgeLen * minEdgeLen
        edgeLenSq = radiusSq + radiusSq + 2.0 * radiusSq * math.cos(divAngle)
        if (edgeLenSq + epsilon) < minEdgeLenSq:
            twoRadiusSq = radiusSq + radiusSq
            edgeDivAngleCos = (twoRadiusSq - edgeLenSq) / twoRadiusSq
            edgeDivAngle = math.acos(edgeDivAngleCos)

            edgeDivCount = math.floor(twoPi / edgeDivAngle)
            divAngle = twoPi / edgeDivCount

        divCount = int(twoPi / divAngle)
        if divCount < minVtxCount:
            divAngle = twoPi / minVtxCount

        return divAngle

    @staticmethod
    def _addProfilePoints_Circle(radius, vtxList):
        perfAngle = 0.94 * math.pi
        minEdgeLen = min(0.1, radius / 8)
        divAngle = ModelAssembler._findCircleDivAngle(radius, perfAngle, minEdgeLen, 8)

        srcVtx = Geom.Pnt(0.0, 0.0, radius)
        twoPi = 2.0 * math.pi
        angleAxis = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(1.0, 0.0, 0.0))
        currAngle = twoPi
        while currAngle > epsilon:
            vtxList.append(srcVtx.rotated(angleAxis, currAngle))
            currAngle -= divAngle

    @staticmethod
    def _addProfilePoints(beamType, radiusH, radiusV, angle, vtxList):
        if beamType == ModelAssembler.BT_Square:
            ModelAssembler._addProfilePoints_Square(radiusH, radiusV, angle, vtxList)
        else:
            if abs(radiusH - radiusV) > epsilon:
                raise RuntimeError("Radii must be equal")

            ModelAssembler._addProfilePoints_Circle(radiusH, vtxList)

    @staticmethod
    def _appenExtrusionSegm(extrPos, extrTangent, vtxList, indexList, profVtxList):
        profVtxCount = len(profVtxList)
        extrStartId = len(vtxList) - profVtxCount

        # Generate new vertices
        extrTrsf = ModelAssembler._calcTransfByTangent(extrTangent)
        extrTrVec = Geom.Vec(extrPos.x(), extrPos.y(), extrPos.z())
        for profVtx in profVtxList:
            trProfVtx = profVtx.transformed(extrTrsf)
            trProfVtx.translate(extrTrVec)

            vtxList.append(trProfVtx)

        # Generate bridge faces
        for profVtxId in range(profVtxCount):
            startVtxId = extrStartId + profVtxId
            endVtxId = extrStartId + ((profVtxId + 1) % profVtxCount)

            indexList.append(endVtxId)
            indexList.append(startVtxId)
            indexList.append(startVtxId + profVtxCount)
            indexList.append(-2)
            indexList.append(-1)

            indexList.append(endVtxId)
            indexList.append(startVtxId + profVtxCount)
            indexList.append(endVtxId + profVtxCount)
            indexList.append(-2)
            indexList.append(-1)

    @staticmethod
    def _calcTransfByTangent(tangent):
        angleH, angleV = angleVec(tangent)

        rotAxisV = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 1, 0))
        trsfV = Geom.Trsf()
        trsfV.setRotation(rotAxisV, angleV)

        rotAxisH = Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0, 0, 1))
        trsfH = Geom.Trsf()
        trsfH.setRotation(rotAxisH, angleH)

        return trsfH * trsfV

    @staticmethod
    def _calcExtrusionStep(arc):
        arcRadius = arc.radius()

        perfAngle = 0.96 * math.pi
        minEdgeLen = min(0.1, arcRadius / 8)
        divAngle = ModelAssembler._findCircleDivAngle(arcRadius, perfAngle, minEdgeLen, 8)

        arcAngle = math.fabs(arc.angle())
        divNum = int(arcAngle // divAngle)
        if (math.fabs(arcAngle % divAngle) > epsilon) or (divNum == 0):
            divNum += 1

        return 1.0 / float(divNum)

    def addSubElem(self, subElem):
        self._modelGr.addSubElement(subElem)

    def addSubmodel(self, subMdl, transform=None):
        beamList = subMdl.getSubElements()
        for beam in beamList:
            if transform is not None:
                beamTr = beam.getTransform()
                newTr = transform * beamTr
                beam.setTransform(newTr)

            self._modelGr.addSubElement(beam)


class FacetedModelAssembler:
    def __init__(self, doc):
        self._doc = doc
        if doc is None:
            raise ValueError("doc is None")

        self._pointList = None
        self._indexList = None

        self._insideFaceCreation = False

    def _insertPoint(self, pt):
        pointListLen = len(self._pointList)

        # Try to find this point in the list
        for index in range(pointListLen):
            if vecsAreSame(pt, self._pointList[index]):
                # print "[{}, {}, {}]: Found existing index - {}".format(pt.x(), pt.y(), pt.z(), index)
                return index

        # print "[{}, {}, {}]: Inserted new index - {}".format(pt.x(), pt.y(), pt.z(), pointListLen)

        # This point is not yet in the list
        self._pointList.append(Geom.Pnt(pt))
        return pointListLen

    def beginModel(self):
        if self._pointList is not None:
            raise RuntimeError("FacetedModelAssembler.beginModel() is called twice")

        self._pointList = Geom.vector_Pnt()
        self._indexList = []

    def endModel(self):
        if self._pointList is None:
            raise RuntimeError(
                "FacetedModelAssembler.endModel() must be called after FacetedModelAssembler.beginModel()")

        if self._insideFaceCreation:
            raise RuntimeError("Face must be closed before calling FacetedModelAssembler.endModel()")

        geom = lx.FacetedBrep.createIn(self._doc)
        geom.setPoints(self._pointList)
        geom.setModel(self._indexList)

        self._pointList = None
        self._indexList = None

        return geom

    def beginFace(self):
        if self._pointList is None:
            raise RuntimeError(
                "FacetedModelAssembler.beginFace() must be called between FacetedModelAssembler.beginModel() and FacetedModelAssembler.endModel()")

        if self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.beginFace() is called twice")

        self._insideFaceCreation = True

    def addVertex(self, pos):
        if not self._insideFaceCreation:
            raise RuntimeError(
                "FacetedModelAssembler.addVertex() must be called between FacetedModelAssembler.beginFace() and FacetedModelAssembler.endFace()")

        ptIndex = self._insertPoint(pos)
        self._indexList.append(ptIndex)

    def addVertexList(self, posList):
        if not self._insideFaceCreation:
            raise RuntimeError(
                "FacetedModelAssembler.addVertexList() must be called between FacetedModelAssembler.beginFace() and FacetedModelAssembler.endFace()")

        for pos in posList:
            ptIndex = self._insertPoint(pos)
            self._indexList.append(ptIndex)

    def endLoop(self):
        self._indexList.append(-2)

    def endFace(self):
        if not self._insideFaceCreation:
            raise RuntimeError("FacetedModelAssembler.endFace() must be called after FacetedModelAssembler.beginFace()")

        self._indexList.append(-2)
        self._indexList.append(-1)

        self._insideFaceCreation = False

    def addExtrusionBridgeNeg(self, startEdge, endEdge, closed):
        if self._insideFaceCreation:
            raise RuntimeError(
                "FacetedModelAssembler.addExtrusionBridgeNeg() must be called outside of face assembly process")

        vtxCount = len(startEdge)
        if len(endEdge) != vtxCount:
            raise RuntimeError("Edge numbers must be equal.")

        if closed:
            minClearEdgeCount = 2
        else:
            minClearEdgeCount = 1

        clearEdgeCount = vtxCount - 1
        if clearEdgeCount < minClearEdgeCount:
            raise RuntimeError("There are too few edges.")

        for edge in range(clearEdgeCount):
            self.beginFace()

            self.addVertex(startEdge[edge])
            self.addVertex(endEdge[edge])
            self.addVertex(endEdge[edge + 1])
            self.addVertex(startEdge[edge + 1])

            self.endFace()

        if closed:
            self.beginFace()

            self.addVertex(startEdge[clearEdgeCount])
            self.addVertex(endEdge[clearEdgeCount])
            self.addVertex(endEdge[0])
            self.addVertex(startEdge[0])

            self.endFace()

    def addExtrusionBridgePos(self, startEdge, endEdge, closed):
        if self._insideFaceCreation:
            raise RuntimeError(
                "FacetedModelAssembler.addExtrusionBridgePos() must be called outside of face assembly process")

        vtxCount = len(startEdge)
        if len(endEdge) != vtxCount:
            raise RuntimeError("Edge numbers must be equal.")

        if closed:
            minClearEdgeCount = 2
        else:
            minClearEdgeCount = 1

        clearEdgeCount = vtxCount - 1
        if clearEdgeCount < minClearEdgeCount:
            raise RuntimeError("There are too few edges.")

        for edge in range(clearEdgeCount):
            self.beginFace()

            self.addVertex(startEdge[edge])
            self.addVertex(startEdge[edge + 1])
            self.addVertex(endEdge[edge + 1])
            self.addVertex(endEdge[edge])

            self.endFace()

        if closed:
            self.beginFace()

            self.addVertex(startEdge[clearEdgeCount])
            self.addVertex(startEdge[0])
            self.addVertex(endEdge[0])
            self.addVertex(endEdge[clearEdgeCount])

            self.endFace()


class Ruehlwand(lx.Element):
    _baugrubentiefeParamName = "Baugrubentiefe"
    _einbindetiefeParamName = "Einbindetiefe"
    _metallprofileTypeParamName = "Metallprofile type"
    _metallprofileParamName = "Metallprofile"
    _abstandProfileParamName = "Abstand profile"
    _hoheGelanderParamName = "Höhe geländer"
    _netzhoheParamName = "Netzhöhe"

    _ankerParamName = "Anker"

    _ankerlangeTotalParamName = "Ankerlänge total"
    _verankerungslangeParamName = "Verankerungslänge"
    _winkelZuHorizontalenParamName = "Winkel zu horizontalen"
    _radiusParamName = "Radius"
    _verankerungskopfradiusParamName = "Verankerungskopfradius"
    _ankerhoheUnterTerrainParamName = "Ankerhöhe unter Terrain"
    _ankerhoheUnterTerrainLage2ParamName = "Ankerhöhe unter Terrain Lage 2"
    _ankerhoheUnterTerrainLage3ParamName = "Ankerhöhe unter Terrain Lage 3"
    _ankerhoheUnterTerrainLage4ParamName = "Ankerhöhe unter Terrain Lage 4"
    _distanceBetweenParamName = "Distance anchor-bar"
    _ifHorizontalBeamsParamName = "Horizontal beams"
    _distanceToHorizontalBeamsParamName = "Distance to beams"
    _numberHorizontalBeamsParamName = "Number horizontal beams"
    _distanceBetweenHorizontalBeamsParamName = "Distance between horizontal beams"
    _polylineParamName = "Polyline"

    def getGlobalClassId(self):
        return Base.GlobalId("{E6BCD138-950E-49AF-8A43-F22E89C4D719}")

    def __init__(self, aArg):
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("Ruehlwand", "OpenLxApp.Element")
        # Register properties
        self.setPropertyHeader(lxstr("Ruehlwand creator"), -1)
        self.setPropertyGroupName(lxstr("Ruehlwand creator"), -1)

        self._baugrubentiefe = self.registerPropertyDouble(self._baugrubentiefeParamName, 10.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._einbindetiefe = self.registerPropertyDouble(self._einbindetiefeParamName, 2.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._metallprofileType = self.registerPropertyEnum(self._metallprofileTypeParamName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._metallprofileType.setEmpty()
        for i in range(len(types)):
            print(types[i])
            self._metallprofileType.addEntry(lxstr(types[i]), -1)

        self._metallprofile = self.registerPropertyEnum(self._metallprofileParamName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._metallprofile.setEmpty()
        for i in range(len(typ2)):
            if types[0] == typ2[i][0]:
                self._metallprofile.addEntry(lxstr(typ2[i][1]), -1)

        self._abstandProfile = self.registerPropertyDouble(self._abstandProfileParamName, 3.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._distanceBetween = self.registerPropertyDouble(self._distanceBetweenParamName, 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._hoheGelander = self.registerPropertyDouble(self._hoheGelanderParamName, 1.2, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._netzhohe = self.registerPropertyDouble(self._netzhoheParamName, 3.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._anker = self.registerPropertyBool(self._ankerParamName, True, lx.Property.VISIBLE,
                                                     lx.Property.EDITABLE, -1)

        #propertise for anker
        self._ankerlangeTotal = self.registerPropertyDouble(self._ankerlangeTotalParamName, 15.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._verankerungslange = self.registerPropertyDouble(self._verankerungslangeParamName, 3.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._winkelZuHorizontalen = self.registerPropertyDouble(self._winkelZuHorizontalenParamName, 45.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._radius = self.registerPropertyDouble(self._radiusParamName, 0.1, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._verankerungskopfradius = self.registerPropertyDouble(self._verankerungskopfradiusParamName, 0.5, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._ankerhoheUnterTerrain = self.registerPropertyDouble(self._ankerhoheUnterTerrainParamName, 2.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._ankerhoheUnterTerrainLage2 = self.registerPropertyDouble(self._ankerhoheUnterTerrainLage2ParamName, 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._ankerhoheUnterTerrainLage3 = self.registerPropertyDouble(self._ankerhoheUnterTerrainLage3ParamName, 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._ankerhoheUnterTerrainLage4 = self.registerPropertyDouble(self._ankerhoheUnterTerrainLage4ParamName, 0.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)



        self._ifHorizontalBeams = self.registerPropertyBool(self._ifHorizontalBeamsParamName, True, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._distanceToHorizontal = self.registerPropertyDouble(self._distanceToHorizontalBeamsParamName, 1.7, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._numberHorizontalBeams = self.registerPropertyInteger(self._numberHorizontalBeamsParamName, 8, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._distanceBetweenHorizontalBeams = self.registerPropertyDouble(self._distanceBetweenHorizontalBeamsParamName, 1.5, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)



        self._reverse = self.registerPropertyBool("Reversed", False, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._modules = self.registerPropertyDouble("Modules", 0.0, lx.Property.NOT_VISIBLE,
                                                    lx.Property.NOT_EDITABLE, -1)

        self._polyline = self.registerPropertyString(self._polylineParamName, lxstr(""), lx.Property.NOT_VISIBLE,
                                                     lx.Property.NOT_EDITABLE, -1)  # NOT_VISIBLE
        self._baseData = None
        dataStr = cstr(self._polyline.getValue())
        if dataStr:
            self._baseData = self.readFromString(dataStr)

        self._baugrubentiefe.setSteps(0.1)
        self._einbindetiefe.setSteps(0.1)
        self._abstandProfile.setSteps(0.1)
        self._distanceBetween.setSteps(0.1)
        self._hoheGelander.setSteps(0.1)
        self._netzhohe.setSteps(0.1)
        self._ankerlangeTotal.setSteps(0.1)
        self._verankerungslange.setSteps(0.1)
        self._radius.setSteps(0.01)
        self._verankerungskopfradius.setSteps(0.01)
        self._ankerhoheUnterTerrain.setSteps(0.1)
        self._ankerhoheUnterTerrainLage2.setSteps(0.1)
        self._ankerhoheUnterTerrainLage3.setSteps(0.1)
        self._ankerhoheUnterTerrainLage4.setSteps(0.1)
        self._distanceToHorizontal.setSteps(0.1)
        self._distanceBetweenHorizontalBeams.setSteps(0.1)

        

    @staticmethod
    def setKoord(elem, xdirekt, ydirekt, pnt):
        xkoord = pnt.x()
        ykoord = pnt.y()
        zkoord = pnt.z()

        origin1 = Geom.Pnt(0, 0, 0)
        zDir1 = Geom.Dir(0, 0, 1)
        elem.setLocalPlacement(Geom.Ax2(origin1, zDir1, Geom.Dir(-ydirekt, xdirekt, 0)))
        elem.translate(Geom.Vec(xkoord, ykoord, zkoord), Geom.CoordSpace_WCS)
        return elem

    @staticmethod
    def setanker(element, xdirekt, ydirekt, pnt, angle, length, ankerlength, headlength, radius, origin1, xDir1, zDir1, headradius):
        if element:
            cylinder = lx.RightCircularCylinder.createIn(doc)
            ankelem = lx.SubElement.createIn(doc)
            cylinder.setHeight(ankerlength - headlength)
            cylinder.setRadius(radius)
            ankelem.setGeometry(cylinder)
            axis2 = Geom.Ax2(origin1, xDir1, zDir1)
            ankelem.setLocalPlacement(axis2)
        else:
            # Erstellung Ankerkopf
            cylinder = lx.RightCircularCylinder.createIn(doc)
            ankelem = lx.SubElement.createIn(doc)
            cylinder.setHeight(headlength)
            cylinder.setRadius(headradius)
            ankelem.setGeometry(cylinder)
            origin2 = Geom.Pnt(ankerlength - headlength, 0, 0)
            axis2 = Geom.Ax2(origin2, xDir1, zDir1)
            ankelem.setLocalPlacement(axis2)

        xkoord = pnt.x()
        ykoord = pnt.y()
        zkoord = pnt.z()
        origin1 = Geom.Pnt(0, 0, 0)
        zDir1 = Geom.Dir(0, 0, 1)

        ankelem.setLocalPlacement(Geom.Ax2(origin1, Geom.Dir(xdirekt, ydirekt, 0), zDir1))
        normvector = Geom.Vec(xdirekt, ydirekt, 0).normalized()
        normvector = normvector.multiplied(-length)

        ankelem.translate(Geom.Vec(xkoord + normvector.x(), ykoord + normvector.y(), zkoord), Geom.CoordSpace_WCS)

        ang = math.radians(angle)
        rotationPoint = Geom.Pnt(xkoord, ykoord, zkoord)

        yAxis = Geom.Ax1(rotationPoint, Geom.Dir(ydirekt, -xdirekt, 0))
        ankelem.rotate(yAxis, ang, Geom.CoordSpace_WCS)

        return ankelem

    @staticmethod
    def setvectorhight(vec, length):
        n = Geom.Vec(vec.x(), vec.y(), 0)
        n = n.normalized()
        nz = vec.normalized()

        if abs(n.x()) > 0.001:
            nz = nz.multiplied(n.x() / nz.x())
        else:
            if abs(n.y()) > 0.001:
                nz = nz.multiplied(n.y() / nz.y())
            else:
                print("I think we have at least a serious z-problem here.")
                return -1

        n = Geom.Vec(n.x(), n.y(), nz.z())

        n = n.multiplied(length)

        return n

    @staticmethod
    def _createSubElementFace(listPoint, colour, texture):
        model = FacetedModelAssembler(doc)

        model.beginModel()
        model.beginFace()
        model.addVertexList(listPoint)
        model.endFace()

        geom = model.endModel()
        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(geom)

        if colour is not None:
            elem.setDiffuseColor(colour)

        if texture is not None:
            elem.setTexture(texture, -1)

        return elem

    def _placeSegmentsAccLine(self, polyLine, model):
        Highttot = self._baugrubentiefe.getValue()
        depth = self._einbindetiefe.getValue()
        profiletyp = str(types[self._metallprofileType.getValue()])

        profilesize = str(typ2[self._metallprofile.getValue()][1])

        a = self._abstandProfile.getValue()  # Abstand Metallprofile
        distanceBetween = self._distanceBetween.getValue() # Abstand Metallprofile

        railingheight = self._hoheGelander.getValue()
        netzheight = self._netzhohe.getValue()

        ifAnker = self._anker.getValue()

        ankerlength = self._ankerlangeTotal.getValue()
        headlength = self._verankerungslange.getValue()
        angle = self._winkelZuHorizontalen.getValue()
        radius = self._radius.getValue()
        headradius = self._verankerungskopfradius.getValue()
        zanker = []
        zanker.append(self._ankerhoheUnterTerrain.getValue())
        zanker.append(self._ankerhoheUnterTerrainLage2.getValue())
        zanker.append(self._ankerhoheUnterTerrainLage3.getValue())
        zanker.append(self._ankerhoheUnterTerrainLage4.getValue())


        ifHorizontalBeams = self._ifHorizontalBeams.getValue()
        distanceToHorizontalBeams = self._distanceToHorizontal.getValue()
        numberHorizontalBeams = self._numberHorizontalBeams.getValue()
        distanceBetweenHorizontalBeams = self._distanceBetweenHorizontalBeams.getValue()


        points = []
        for i in range(polyLine.segmentCount() + 1):
            #print("Add point")
            points.append(Geom.Pnt(polyLine.point(i).x(), polyLine.point(i).y(), polyLine.point(i).z() - self._einbindetiefe.getValue()))

        if self._reverse.getValue():
            points.reverse()
        # Import Points of Path

        # create Vectors
        pathvec = []
        for j in range(len(points)-1):
            pathvec.append(Geom.Vec(points[j], points[j + 1]))

        for t in range(len(pathvec)):
            # Kopieren Wall 2
            listPntForWall2 = []
            listPntForWall2.append(points[t].translated(Geom.Vec(0.0, 0.0, depth)))
            listPntForWall2.append(points[t].translated(Geom.Vec(0.0, 0.0, Highttot)))
            listPntForWall2.append(points[t+1].translated(Geom.Vec(0.0, 0.0, Highttot)))
            listPntForWall2.append(points[t+1].translated(Geom.Vec(0.0, 0.0, depth)))

            model.addSubElem(self._createSubElementFace(listPntForWall2, None, None))



            # Kopieren Wall 3
            listPntForWall3 = []
            listPntForWall3.append(points[t])
            listPntForWall3.append(points[t].translated(Geom.Vec(0.0, 0.0, depth)))
            listPntForWall3.append(points[t + 1].translated(Geom.Vec(0.0, 0.0, depth)))
            listPntForWall3.append(points[t + 1])

            model.addSubElem(self._createSubElementFace(listPntForWall3, Base.Color(102, 102, 102), None))

            # Kopieren Wall 4
            listPntForWall4 = []
            listPntForWall4.append(points[t].translated(Geom.Vec(0.0, 0.0, Highttot)))
            listPntForWall4.append(points[t].translated(Geom.Vec(0.0, 0.0, railingheight + Highttot)))
            listPntForWall4.append(points[t + 1].translated(Geom.Vec(0.0, 0.0, railingheight + Highttot)))
            listPntForWall4.append(points[t + 1].translated(Geom.Vec(0.0, 0.0, Highttot)))

            model.addSubElem(self._createSubElementFace(listPntForWall4, Base.Color(126, 65, 0), None))

            # Kopieren Netze
            kopierenNetze = []
            kopierenNetze.append(points[t].translated(Geom.Vec(0.0, 0.0, Highttot + railingheight)))
            kopierenNetze.append(points[t].translated(Geom.Vec(0.0, 0.0, Highttot + railingheight + netzheight)))
            kopierenNetze.append(points[t + 1].translated(Geom.Vec(0.0, 0.0, Highttot + railingheight + netzheight)))
            kopierenNetze.append(points[t + 1].translated(Geom.Vec(0.0, 0.0, Highttot + railingheight)))
            texture = Draw.Texture2()
            texture.setTextureFileName(lxstr('materials/629b.png'))
            model.addSubElem(self._createSubElementFace(kopierenNetze, None, texture))

            origin1 = Geom.Pnt(0, 0, 0)
            zDir1 = Geom.Dir(0, 0, 1)
            xDir1 = Geom.Dir(1, 0, 0)
            normvec = self.setvectorhight(pathvec[t], (a))
            normvecStart = self.setvectorhight(pathvec[t], (distanceBetween))
            nprojektiert = Geom.Vec(pathvec[t].x(), pathvec[t].y(), 0)

            if ifAnker:
                aneu = self.setanker(True, -pathvec[t].y(), pathvec[t].x(), points[t], angle, ankerlength - headlength, ankerlength, headlength, radius, origin1, xDir1, zDir1, headradius)
                aneu.translate(Geom.Vec(0, 0, Highttot-zanker[0]), Geom.CoordSpace_WCS)
                aneu.translate(normvecStart, Geom.CoordSpace_WCS)
                aneu2 = self.setanker(False, -pathvec[t].y(), pathvec[t].x(), points[t], angle, ankerlength, ankerlength, headlength, radius, origin1, xDir1, zDir1, headradius)
                aneu2.translate(Geom.Vec(0, 0, Highttot-zanker[0]), Geom.CoordSpace_WCS)
                aneu2.translate(normvecStart, Geom.CoordSpace_WCS)
                aneu2.setDiffuseColor(Base.Color(102, 102, 102))
                model.addSubElem(aneu)
                model.addSubElem(aneu2)

                for s in range(1, 4):
                    if zanker[s] == 0:
                        pass
                    else:
                        aneus = aneu.copy()
                        aneus.translate(Geom.Vec(0,0,zanker[0]-zanker[s]),Geom.CoordSpace_WCS)
                        aneus2 = aneu2.copy()
                        aneus2.translate(Geom.Vec(0,0,zanker[0]-zanker[s]),Geom.CoordSpace_WCS)
                        model.addSubElem(aneus)
                        model.addSubElem(aneus2)

                for i in range(1,int((nprojektiert.magnitude() - distanceBetween)/(a))+1):
                    aneu = aneu.copy()
                    aneu.translate(normvec, Geom.CoordSpace_WCS)
                    aneu2 = aneu2.copy()
                    aneu2.translate(normvec, Geom.CoordSpace_WCS)

                    model.addSubElem(aneu)
                    model.addSubElem(aneu2)
                    for j in range(1,4):
                        if zanker[j] == 0:
                            pass
                        else:
                            aneui = aneu.copy()
                            aneui.translate(Geom.Vec(0, 0, zanker[0]-zanker[j]), Geom.CoordSpace_WCS)
                            aneu2i = aneu2.copy()
                            aneu2i.translate(Geom.Vec(0, 0, zanker[0]-zanker[j]), Geom.CoordSpace_WCS)
                            model.addSubElem(aneui)
                            model.addSubElem(aneu2i)

            if ifHorizontalBeams:

                profile = lx.IShapeProfileDef.createIn(doc)
                profile.setValuesFromPredefinedSteelProfile(lxstr(profiletyp + ' ' + profilesize))
                eas2 = lx.ExtrudedAreaSolid.createIn(doc)
                eas2.setSweptArea(profile)
                eas2.setExtrudedDirection(Geom.Dir(0, 0, 1))
                eas2.setDepth(pathvec[t].magnitude())

                normDirVec = Geom.Dir(points[t+1].x() - points[t].x(), points[t+1].y() - points[t].y(), points[t+1].z() - points[t].z())

                for k in range(int(numberHorizontalBeams)):
                    element = lx.SubElement.createIn(doc)
                    element.setGeometry(eas2)
                    axis1 = Geom.Ax2(Geom.Pnt(points[t].x(), points[t].y(), points[t].z() + distanceToHorizontalBeams + depth + (float(k) * distanceBetweenHorizontalBeams)), normDirVec)

                    element.setLocalPlacement(axis1)

                    element.setUserName(lxstr("Metallprofil"))
                    element.setDiffuseColor(Base.Color(0, 250, 250))

                    model.addSubElem(element)


        for t in range(len(pathvec)):

            profile = lx.IShapeProfileDef.createIn(doc)
            profile.setValuesFromPredefinedSteelProfile(lxstr(profiletyp + ' ' + profilesize))
            eas2 = lx.ExtrudedAreaSolid.createIn(doc)
            eas2.setSweptArea(profile)
            eas2.setExtrudedDirection(Geom.Dir(0, 0, 1))
            eas2.setDepth(Highttot + railingheight + netzheight)

            element = lx.SubElement.createIn(doc)
            element.setGeometry(eas2)

            origin1 = Geom.Pnt(0, 0, 0)
            zDir1 = Geom.Dir(0, 0, 1)
            xDir1 = Geom.Dir(1, 0, 0)
            yDir1 = Geom.Dir(0, 1, 0)
            axis1 = Geom.Ax2(origin1, zDir1, xDir1)

            element.setLocalPlacement(axis1)

            element.setUserName(lxstr("Metallprofil"))
            element.setDiffuseColor(Base.Color(0, 250, 250))

            normvec = self.setvectorhight(pathvec[t], a)
            nprojektiert = Geom.Vec(pathvec[t].x(), pathvec[t].y(), 0)

            # Kopieren Metallprofile und Anker

            elem = self.setKoord(element, -pathvec[t].y(), pathvec[t].x(), points[t])
            model.addSubElem(elem)
            for i in range(1, int(nprojektiert.magnitude() / a) + 1):
                elem = elem.copy()
                elem.translate(normvec, Geom.CoordSpace_WCS)
                model.addSubElem(elem)


    def printPolyline(self, name, ptList):
        print("{}:".format(name))

        for pt in ptList:
            print("    ({}, {}, {})".format(pt.x(), pt.y(), pt.z()))

    def fixPolyline(self, pntList):
        self._pntList = pntList
        self.printPolyline("pntList", pntList)
        self.printPolyline("self._pntList", self._pntList)

    def createCompound(self):
        with EditMode(self.getDocument()):
            self.removeSubElements()
            model = ModelAssembler(doc)
            model.beginModel(self)
            polyLine = PolylineData.fromElement(self._baseData)
            self._placeSegmentsAccLine(polyLine, model)
            model.endModel()

    def printPolylineTest(self, strn):
        print(":{}".format(strn))

        # for pt in ptList:
        #     print "    ({}, {}, {})".format(pt.x(), pt.y(), pt.z())

    def setPolylineData(self, polylineData):
        if lxstr(self.writeToString(polylineData)) is self._modules.getValue():
            print("Select another polyline")
            return

        #if not self._insidePropUpdate:
        self._insidePropUpdate = True

        self._baseData = polylineData
        self._polyline.setValue(lxstr(self.writeToString(polylineData)))
        #self.printPolylineTest(cstr(self._polyline.getValue()))

        self.createCompound()

    @staticmethod
    def writeToString(lineData):
        strn = ""
        strn += "{};".format(len(lineData))
        for i in range(len(lineData)):
            if lineData[i][0] == PolylineData.SegmType_Line:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};".format(lineData[i][0],\
                                                             lineData[i][1].x(), lineData[i][1].y(), lineData[i][1].z(),\
                                                             lineData[i][2].x(), lineData[i][2].y(), lineData[i][2].z())
            elif lineData[i][0] == PolylineData.SegmType_Arc:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};{7:.5f};{8:.5f};{9:.5f};".format(lineData[i][0],\
                                                             lineData[i][1].x(), lineData[i][1].y(), lineData[i][1].z(),\
                                                             lineData[i][2].x(), lineData[i][2].y(), lineData[i][2].z(),\
                                                             lineData[i][3].x(), lineData[i][3].y(), lineData[i][3].z())
            # if i != len(lineData)-1:
            #     strn += ";"
        i_n = len(lineData[len(lineData)-1])-1
        strn += "{}".format(lineData[len(lineData)-1][i_n])
        return strn

    @staticmethod
    def readFromString(strn):
        lineData = []
        st = strn.split(";")
        #lenList = int(st[0])
        index = 0
        for i in range(int(st[0])):
            if int(st[index+1]) == PolylineData.SegmType_Line:
                lineData.append([int(st[index+1]), Geom.Pnt(float(st[index+2]), float(st[index+3]), float(st[index+4])),\
                                Geom.Pnt(float(st[index+5]), float(st[index+6]), float(st[index+7]))])
                index += 7
            elif int(st[index+1]) == PolylineData.SegmType_Arc:
                lineData.append([int(st[index + 1]), Geom.Pnt(float(st[index + 2]), float(st[index + 3]), float(st[index + 4])), \
                                Geom.Pnt(float(st[index + 5]), float(st[index + 6]), float(st[index + 7])), \
                                Geom.Pnt(float(st[index + 8]), float(st[index + 9]), float(st[index + 10]))])
                index += 10

        i_n = len(lineData[int(st[0])-1])
        if st[len(st)-1] == "True":
            bl = True
        else:
            bl = False
        lineData[int(st[0])-1].append(bl)
        #print "i_n={} , st[last]={}".format(i_n, lineData[int(st[0])-1][i_n])

        return lineData

    def polyline(self):
        return self._polyline.getValue()

    def setBaugrubentiefe(self, param):
        with EditMode(self.getDocument()):
            self._baugrubentiefe.setValue((clamp(param, self._einbindetiefe.getValue() + epsilon, 10000.0)))
            self.createCompound()

    def setEinbindetiefe(self, param):
        with EditMode(self.getDocument()):
            self._einbindetiefe.setValue((clamp(param, epsilon, self._baugrubentiefe.getValue() - epsilon)))
            self.createCompound()

    def setMetallprofileType(self, param):
        with EditMode(self.getDocument()):
            self._metallprofileType.setValue(param)
            self.createCompound()

    def setMetallprofile(self, param):
        with EditMode(self.getDocument()):
            self._metallprofile.setValue(param)
            self.createCompound()

    def setAbstandProfile(self, param):
        with EditMode(self.getDocument()):
            self._abstandProfile.setValue((clamp(param, epsilon, 10000.0)))
            self.createCompound()

    def setDistanceBetween(self, param):
        with EditMode(self.getDocument()):
            self._distanceBetween.setValue((clamp(param, 0.0, 10000.0)))
            self.createCompound()

    def setHoheGelander(self, param):
        with EditMode(self.getDocument()):
            self._hoheGelander.setValue((clamp(param, epsilon, 10000.0)))
            self.createCompound()

    def setNetzhohe(self, param):
        with EditMode(self.getDocument()):
            self._netzhohe.setValue((clamp(param, epsilon, 10000.0)))
            self.createCompound()


    def setAnker(self, param):
        with EditMode(self.getDocument()):
            self._anker.setValue(param)
            self.createCompound()

    def setAnkerlangeTotal(self, param):
        with EditMode(self.getDocument()):
            self._ankerlangeTotal.setValue((clamp(param, self._verankerungslange.getValue(), 10000.0)))
            self.createCompound()


    def setVerankerungslange(self, param):
        with EditMode(self.getDocument()):
            self._verankerungslange.setValue((clamp(param, epsilon, self._ankerlangeTotal.getValue() - epsilon)))
            self.createCompound()

    def setWinkelZuHorizontalen(self, param):
        with EditMode(self.getDocument()):
            self._winkelZuHorizontalen.setValue((clamp(param, 0, 90)))
            self.createCompound()


    def setRadius(self, param):
        with EditMode(self.getDocument()):
            self._radius.setValue((clamp(param, epsilon, self._verankerungskopfradius.getValue())))
            self.createCompound()

    def setVerankerungskopfradius(self, param):
        with EditMode(self.getDocument()):
            self._verankerungskopfradius.setValue((clamp(param, self._radius.getValue(), 10000.0)))
            self.createCompound()

    def setAnkerhoheUnterTerrain(self, param):
        with EditMode(self.getDocument()):
            self._ankerhoheUnterTerrain.setValue((clamp(param, 0.0, 1000.0)))
            self.createCompound()

    def setAnkerhoheUnterTerrainLage2(self, param):
        with EditMode(self.getDocument()):
            self._ankerhoheUnterTerrainLage2.setValue((clamp(param, 0.0, 1000.0)))
            self.createCompound()


    def setAnkerhoheUnterTerrainLage3(self, param):
        with EditMode(self.getDocument()):
            self._ankerhoheUnterTerrainLage3.setValue((clamp(param, 0.0, 1000.0)))
            self.createCompound()

    def setAnkerhoheUnterTerrainLage4(self, param):
        with EditMode(self.getDocument()):
            self._ankerhoheUnterTerrainLage4.setValue((clamp(param, 0.0, 1000.0)))
            self.createCompound()

    def setReverseBtn(self, param):
        with EditMode(self.getDocument()):
            self._reverse.setValue(param)
            self.createCompound()


    def setIfHorizontalBeams(self, param):
        with EditMode(self.getDocument()):
            self._ifHorizontalBeams.setValue(param)
            self.createCompound()
    def setDistanceToHorizontal(self, param):
        with EditMode(self.getDocument()):
            self._distanceToHorizontal.setValue(clamp(param, 0.0, 1000.0))
            self.createCompound()
    def setNumberHorizontalBeams(self, param):
        with EditMode(self.getDocument()):
            maxBeams = int(((self._baugrubentiefe.getValue() + self._netzhohe.getValue() - self._distanceToHorizontal.getValue()) / self._distanceBetweenHorizontalBeams.getValue()))
            self._numberHorizontalBeams.setValue(clamp(param, 1, maxBeams))
            self.createCompound()
    def setDistanceBetweenHorizontalBeams(self, param):
        with EditMode(self.getDocument()):
            maxValue = (self._baugrubentiefe.getValue() + self._netzhohe.getValue() - self._distanceToHorizontal.getValue()) / float(self._numberHorizontalBeams.getValue())
            self._distanceBetweenHorizontalBeams.setValue(clamp(param, 0.0, maxValue))
            self.createCompound()



    def onPropertyChanged(self, aPropertyName):
        if aPropertyName == Ruehlwand._baugrubentiefeParamName:
            self.setBaugrubentiefe(self._baugrubentiefe.getValue())
        elif aPropertyName == Ruehlwand._einbindetiefeParamName:
            self.setEinbindetiefe(self._einbindetiefe.getValue())
        elif aPropertyName == Ruehlwand._metallprofileTypeParamName:
            self.setMetallprofileType(self._metallprofileType.getValue())
        elif aPropertyName == Ruehlwand._metallprofileParamName:
            self.setMetallprofile(self._metallprofile.getValue())
        elif aPropertyName == Ruehlwand._abstandProfileParamName:
            self.setAbstandProfile(self._abstandProfile.getValue())
        elif aPropertyName == Ruehlwand._distanceBetweenParamName:
            self.setDistanceBetween(self._distanceBetween.getValue())
        elif aPropertyName == Ruehlwand._hoheGelanderParamName:
            self.setHoheGelander(self._hoheGelander.getValue())
        elif aPropertyName == Ruehlwand._netzhoheParamName:
            self.setNetzhohe(self._netzhohe.getValue())

        elif aPropertyName == Ruehlwand._ankerParamName:
            self.setAnker(self._anker.getValue())

        elif aPropertyName == Ruehlwand._ankerlangeTotalParamName:
            self.setAnkerlangeTotal(self._ankerlangeTotal.getValue())
        elif aPropertyName == Ruehlwand._verankerungslangeParamName:
            self.setVerankerungslange(self._verankerungslange.getValue())
        elif aPropertyName == Ruehlwand._winkelZuHorizontalenParamName:
            self.setWinkelZuHorizontalen(self._winkelZuHorizontalen.getValue())
        elif aPropertyName == Ruehlwand._radiusParamName:
            self.setRadius(self._radius.getValue())
        elif aPropertyName == Ruehlwand._verankerungskopfradiusParamName:
            self.setVerankerungskopfradius(self._verankerungskopfradius.getValue())
        elif aPropertyName == Ruehlwand._ankerhoheUnterTerrainParamName:
            self.setAnkerhoheUnterTerrain(self._ankerhoheUnterTerrain.getValue())
        elif aPropertyName == Ruehlwand._ankerhoheUnterTerrainLage2ParamName:
            self.setAnkerhoheUnterTerrainLage2(self._ankerhoheUnterTerrainLage2.getValue())
        elif aPropertyName == Ruehlwand._ankerhoheUnterTerrainLage3ParamName:
            self.setAnkerhoheUnterTerrainLage3(self._ankerhoheUnterTerrainLage3.getValue())
        elif aPropertyName == Ruehlwand._ankerhoheUnterTerrainLage4ParamName:
            self.setAnkerhoheUnterTerrainLage4(self._ankerhoheUnterTerrainLage4.getValue())

        elif aPropertyName == Ruehlwand._ifHorizontalBeamsParamName:
            self.setIfHorizontalBeams(self._ifHorizontalBeams.getValue())

        elif aPropertyName == Ruehlwand._distanceToHorizontalBeamsParamName:
            self.setDistanceToHorizontal(self._distanceToHorizontal.getValue())

        elif aPropertyName == Ruehlwand._numberHorizontalBeamsParamName:
            self.setNumberHorizontalBeams(self._numberHorizontalBeams.getValue())

        elif aPropertyName == Ruehlwand._distanceBetweenHorizontalBeamsParamName:
            self.setDistanceBetweenHorizontalBeams(self._distanceBetweenHorizontalBeams.getValue())

        elif aPropertyName == "Reversed":
            self.setReverseBtn(self._reverse.getValue())

def getPolylineData(lineSet):
    lineData = []
    #edges = Topo.ShapeTool.getEdges(lineSet.getShape())
    wire = Topo.ShapeTool.isSingleWire(lineSet.getShape())
    # print("Is Wire Closed?", Topo.WireTool.isClosed(wire))
    # print("Is Wire SelfIntersecting?", Topo.WireTool.isSelfIntersecting(wire))
    # print("Fix Reorder in Wire !", Topo.WireTool.fixReorder(wire))
    if Topo.WireTool.isClosed(wire):
       edges = Topo.WireTool.getEdges(Topo.WireTool.reversed(wire))
    else:
       edges = Topo.WireTool.getEdges(wire)
    #edges = Topo.WireTool.getEdges(wire)

    for edgeIndex in range(len(edges)):
        edge = edges[edgeIndex]

        edgeTypeRes = Topo.EdgeTool.getGeomCurveType(edge)
        if not edgeTypeRes.ok:
            raise RuntimeError("Can't get edge type")

        if edgeTypeRes.type == Geom.CurveType_LINE:
            lineParamRes = Topo.EdgeTool.getLineParameters(edge)
            if not lineParamRes.ok:
                raise RuntimeError("Can't get line parameters")
            p1Res = Topo.EdgeTool.d0(edge, lineParamRes.startParam)
            p2Res = Topo.EdgeTool.d0(edge, lineParamRes.endParam)
            if (not p1Res.ok) or (not p2Res.ok):
                raise RuntimeError("Can't get line start or end point")
            lineData.append([PolylineData.SegmType_Line, Geom.Pnt(p1Res.p), Geom.Pnt(p2Res.p)])

            # print "LineNumb[{}] has type {}: startPt ({}, {}, {}), " \
            #       "\n endPt ({}, {}, {})".format(edgeIndex, lineData[edgeIndex][0],
            #                                      lineData[edgeIndex][1].x(), lineData[edgeIndex][1].y(), lineData[edgeIndex][1].z(),
            #                                      lineData[edgeIndex][2].x(), lineData[edgeIndex][2].y(), lineData[edgeIndex][2].z())

        elif edgeTypeRes.type == Geom.CurveType_CIRCLE:
            arcParamsRes = Topo.EdgeTool.getArcParameters(edge)
            if not arcParamsRes.ok:
                raise RuntimeError("Can't get arc parameters")
            p1Res = Topo.EdgeTool.d0(edge, arcParamsRes.startParam)
            middleParam = (arcParamsRes.startParam + arcParamsRes.endParam) * 0.5
            p2Res = Topo.EdgeTool.d0(edge, middleParam)
            p3Res = Topo.EdgeTool.d0(edge, arcParamsRes.endParam)
            if (not p1Res.ok) or (not p2Res.ok) or (not p3Res.ok):
                raise RuntimeError("Can't get arc start or middle or end point")
            lineData.append([PolylineData.SegmType_Arc, Geom.Pnt(p1Res.p), Geom.Pnt(p2Res.p), Geom.Pnt(p3Res.p)])

            # print "LineNumb[{}] has type {}: startPt ({}, {}, {}), " \
            #       "\n endPt ({}, {}, {})".format(edgeIndex, lineData[edgeIndex][0],
            #                                      lineData[edgeIndex][1].x(), lineData[edgeIndex][1].y(), lineData[edgeIndex][1].z(),
            #                                      lineData[edgeIndex][2].x(), lineData[edgeIndex][2].y(), lineData[edgeIndex][2].z(),
            #                                      lineData[edgeIndex][3].x(), lineData[edgeIndex][3].y(), lineData[edgeIndex][3].z())
        else:
            raise RuntimeError("Unsupported edge type")
    lineData[len(edges)-1].append(Topo.WireTool.isClosed(wire))
    #print(lineData[len(edges)-1])
    return lineData

def selectPolyline(uidoc):
    uidoc.highlightByShapeType(Topo.ShapeType_WIRE)
    ok = uidoc.pickPoint()
    uidoc.stopHighlightByShapeType()
    if ok:
        return uidoc.getPickedElement()
    else:
        return None

def pickPolyline(uidoc):
    ui.showStatusBarMessage(lxstr("[L] Select base line [Esc] Cancel"))
    lineSet = selectPolyline(uidoc)
    ui.showStatusBarMessage(lxstr(""))

    if lineSet is not None:
        return getPolylineData(lineSet)
    else:
        return None
if __name__ == "__main__":
    # Register this Python Script
    doc.registerPythonScript(Base.GlobalId("{4AB544F7-4F99-4F65-AC43-3BC15C91BE9A}"))


    # Begin creating the Element
    with EditMode(doc):
        polylineData = pickPolyline(uidoc)
        if polylineData is not None:

            comp = Ruehlwand(doc)
            comp.setDiffuseColor(Base.Color_fromCdwkColor(25))
            comp.setPolylineData(polylineData)  # !!!!!!!!!!!!!

        doc.recompute()
