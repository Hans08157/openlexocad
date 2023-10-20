# coding=utf-8
# OpenLexocad libraries

"""
version 3.0	16.03.2020

attributes
version 2.0
add profiles and red line

version 2.1
    add face extrusion

version 2.2
    add cutting by line

version 3.0
    remaking cutting by top line, now work more correctly,
    and takes less time for it. Change element to PythonElement

version 4.0
    added posibility to build cut line now only with Z coordinates
    We need to added two new functions to stretch or cut the
    metal profiles. The same for the bored piles (concrete cylinder).
    Нам потрібно додати дві нові функції для розтягування або різання
    металевих профілів. Те саме для буронабивних паль (бетонний циліндр).

version 5.0
    reference line
    set depth for profile

version 6.0
    add IFC type for each elements:
    - ifcColumn
    - ifcPipe
    - ifcWall
version 7.0
    - Transparency" only additional property for columns
    - Adjust order of the parameters
    - For "show main line" translations don`t work(81th row)
version 8.0
    - remake assembly in to multigeo
    - adjust order of the parameters
    - transparency only for columns and wall
version 9.0
    - change from ElementAssembly to Element(with SubElements)
version 10.0
    - new cutting algorithm with local transform
    - main line element stay is scene


========================================
====  Supported by Roman Davydiuk   ====
====  Mail: davydjukroman@gmail.com ====
====  Skype: live:davydjukroman     ====
========================================
"""

import math
import collections
import OpenLxApp as lx
import OpenLxUI as ui
import Base, Core, Geom, Topo
import pdb

lxStr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

st = Topo.ShapeTool

doc = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel = uidoc.getSelection()

epsilon = 0.0001
pi2 = math.pi * 0.5

GUID_CLASS = Base.GlobalId("{1072EB78-8445-4DB5-BE8C-4A54BDAFEA33}")
GUID_SCRPT = Base.GlobalId("{ACD50C5A-B8F5-4CAD-A4D3-D3C74471DA98}")

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


# =====================================================================================================================

def qStr(str):
    return Base.StringTool.toQString(lxStr(str))


def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))


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


class Arc3Pnt:
    def __init__(self, p1, p2, p3):
        self._startPt = Geom.Pnt(p1)
        self._endPt = Geom.Pnt(p3)

        self._centerPt = Arc3Pnt._calcCenterPt(p1, p2, p3)

        self._startVec = Geom.Vec(self._centerPt, self._startPt)
        middleVec = Geom.Vec(self._centerPt, p2)
        endVec = Geom.Vec(self._centerPt, self._endPt)

        self._normVec = self._startVec.crossed(endVec)
        if self._normVec.squareMagnitude() < epsilon:
            self._normVec = self._startVec.crossed(middleVec)
        self._normVec.normalize()

        self._angle = Arc3Pnt._calcAngle(self._startVec, middleVec, endVec, self._normVec)

        self._axis = Geom.Ax1(self._centerPt, Geom.Dir(self._normVec))

    def copy(self):
        return Arc3Pnt(self._startPt, self.paramPt(0.5), self._endPt)

    @staticmethod
    def _calcBaryCenter(w1, p1, w2, p2, w3, p3):
        x = w1 * p1.x() + w2 * p2.x() + w3 * p3.x()
        y = w1 * p1.y() + w2 * p2.y() + w3 * p3.y()
        z = w1 * p1.z() + w2 * p2.z() + w3 * p3.z()

        return Geom.Pnt(x, y, z)

    @staticmethod
    def _calcCenterPt(p1, p2, p3):
        # For the formulas, please look at https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_from_cross-_and_dot-products

        v12 = Geom.Vec(p2, p1)
        v13 = Geom.Vec(p3, p1)
        v21 = Geom.Vec(p1, p2)
        v23 = Geom.Vec(p3, p2)
        v31 = Geom.Vec(p1, p3)
        v32 = Geom.Vec(p2, p3)

        v12Len = v12.magnitude()
        v13Len = v13.magnitude()
        v23Len = v23.magnitude()

        vCross = v12.crossed(v23)
        vCrossLen = vCross.magnitude()

        invDen = 1.0 / (2.0 * vCrossLen * vCrossLen)  # Inverted denominator

        # Weights
        w1 = v23Len * v23Len * v12.dot(v13) * invDen
        w2 = v13Len * v13Len * v21.dot(v23) * invDen
        w3 = v12Len * v12Len * v31.dot(v32) * invDen

        return Arc3Pnt._calcBaryCenter(w1, p1, w2, p2, w3, p3)

    @staticmethod
    def _basisAngle(vec, u, v):
        # All 3 vectors must be normalized

        uAngle = math.acos(u.dot(vec))
        vAngleCos = v.dot(vec)

        if vAngleCos > 0.0:
            uAngle = (2.0 * math.pi) - uAngle

        return uAngle

    @staticmethod
    def _calcAngle(v1, v2, v3, vNorm):
        nv1 = v1.normalized()
        nv2 = v2.normalized()
        nv3 = v3.normalized()
        # vNorm must be already normalized

        pnv1 = vNorm.crossed(nv1)

        angle2 = Arc3Pnt._basisAngle(nv2, nv1, pnv1)
        angle3 = Arc3Pnt._basisAngle(nv3, nv1, pnv1)

        if (angle2 + epsilon) > angle3:
            return v1.angle(v3)
        else:
            return - ((2.0 * math.pi) - v1.angle(v3))

    def angle(self):
        return self._angle

    def radius(self):
        return self._centerPt.distance(self._startPt)

    def length(self):
        return math.fabs(self.radius() * self._angle)

    def paramRatio(self):
        return 1.0 / self.length()

    def partLength(self, dt):
        return self.radius() * self._angle * dt

    def startPt(self):
        return self._startPt

    def endPt(self):
        return self._endPt

    def centerPt(self):
        return self._centerPt

    def paramPt(self, t):
        if t < epsilon:
            return self._startPt
        if (t + epsilon) > 1.0:
            return self._endPt

        paramVec = self._startVec.rotated(self._axis, self._angle * t)
        return self._centerPt.translated(paramVec)

    def startTangent(self):
        return self.paramTangent(0.0)

    def endTangent(self):
        return self.paramTangent(1.0)

    def paramTangent(self, t):
        if t < epsilon:
            t = 0.0
        if (t + epsilon) > 1.0:
            t = 1.0

        dt = 0.001

        dArc = None
        if (1.0 - t) < dt:
            pt1 = self.paramPt(t - dt)
            pt2 = self.paramPt(t)

            dArc = Geom.Vec(pt1, pt2)
        elif (t - 0.0) < dt:
            pt1 = self.paramPt(t)
            pt2 = self.paramPt(t + dt)

            dArc = Geom.Vec(pt1, pt2)
        else:
            pt1 = self.paramPt(t - dt)
            pt2 = self.paramPt(t + dt)

            dArc = Geom.Vec(pt1, pt2)
        dArc.normalize()

        return dArc


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

    def getPntList(self):
        return self._ptList

    @staticmethod
    def fromElement(lineElem):
        newPD = PolylineData()

        firstEdge = True
        startIndex = 0
        for edgeIndex in range(len(lineElem)):
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

        # i_n = len(lineElem[len(lineElem) - 1]) - 1
        # newPD._closed = lineElem[len(lineElem) - 1][i_n]
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


class Line2D:
    def __init__(self, pt, dir):
        self._pt = Geom.Pnt2d(pt.x(), pt.y())
        self._dir = dir.normalized()

    @staticmethod
    def from2Points(pt1, pt2):
        dir = Geom.Vec2d(pt2.x() - pt1.x(), pt2.y() - pt1.y())
        return Line2D(pt1, dir)

    def point(self):
        return self._pt

    def paramPoint(self, t):
        x = self._pt.x() + t * self._dir.x()
        y = self._pt.y() + t * self._dir.y()

        return Geom.Pnt2d(x, y)

    def direction(self):
        return self._dir

    def normal(self):
        return Geom.Vec2d(-self._dir.y(), self._dir.x())  # Direction is already normalized

    def offset(self, dVec):
        return Line2D(self._pt.translated(dVec), self._dir)

    def normalOffset(self, offs):
        normVec = self.normal()
        normVec.scale(offs)

        return self.offset(normVec)

    def findY(self, x):
        xDir = self._dir.x()
        if math.fabs(xDir) < epsilon:
            raise ZeroDivisionError("Line is parallel to X axis.")

        t = (x - self._pt.x()) / xDir
        return self._pt.y() + t * self._dir.y()

    def classifyPoint(self, pt):
        normVec = self.normal()
        ptDir = Geom.Vec2d(self._pt, pt)

        return math.copysign(1.0, normVec * ptDir)

    @staticmethod
    def collinear(l1, l2):
        if math.fabs(l2._dir.x()) < epsilon:
            return bool(math.fabs(l1._dir.x()) < epsilon)
        if math.fabs(l2._dir.y()) < epsilon:
            return bool(math.fabs(l1._dir.y()) < epsilon)

        return bool(math.fabs((l1._dir.x() / l2._dir.x()) - (l1._dir.y() / l2._dir.y())) < epsilon)

    @staticmethod
    def intersect(l1, l2):
        if Line2D.collinear(l1, l2):
            return None

        dx = l2._pt.x() - l1._pt.x()
        dy = l2._pt.y() - l1._pt.y()

        if math.fabs(l2._dir.y()) > epsilon:
            t = (dx * l2._dir.y() - dy * l2._dir.x()) / (l1._dir.x() * l2._dir.y() - l1._dir.y() * l2._dir.x())
            return l1.paramPoint(t)
        else:
            t = (dy * l1._dir.x() - dx * l1._dir.y()) / (l1._dir.y() * l2._dir.x())
            return l2.paramPoint(t)


class PolylineReader:
    def __init__(self, polyLine):
        self.polyline = polyLine
        self.segmCount = polyLine.segmentCount()
        self.e = 0.0001
        self.pointListWithDistance = []
        self.segmentsList = []

        if self.segmCount <= 0:
            # print("There are no segments")
            return

        for segmId in range(self.segmCount):
            segmType = self.polyline.segmentType(segmId)

            if segmType == PolylineData.SegmType_Line:
                startPt = self.polyline.segmStartPt(segmId)
                endPt = self.polyline.segmEndPt(segmId)
                lineSegment = self.SegmLine(startPt, endPt)
                self.segmentsList.append(lineSegment)

            elif segmType == PolylineData.SegmType_Arc:
                arc = PolylineData.segmArc(self.polyline, segmId)
                # print("Radius = ", arc.radius(), ", angle = ", arc.angle(), arc.angle() * 180.0 / math.pi)
                n = int(math.fabs(arc.angle() / (math.acos(((arc.radius() - self.e) / arc.radius())) * 2.0)))
                for i in range(n):
                    pnt0 = arc.paramPt(float(i) / float(n))
                    pnt1 = arc.paramPt((float(float(i) + 1.0) / float(n)))
                    if float(float(i) + 1.0) / float(n) <= 1.0:
                        lineSegment = self.SegmLine(pnt0, pnt1)
                        self.segmentsList.append(lineSegment)
                # print("ARC")
            else:
                # print("Unknown segment")
                return

    def getListPointWithDistanceOnPolyline(self, dist, radius, withLast):
        listPoint = []
        for segm in self.segmentsList:
            endPoint = self.segmentsList[len(self.segmentsList) - 1].p1
            if segm == self.segmentsList[len(self.segmentsList) - 1]:
                ifLast = True
            else:
                ifLast = False
            if len(listPoint) >= 1:
                distToPrev = segm.getDistanceToFirstPnt(listPoint[len(listPoint) - 1], dist)
            else:
                distToPrev = segm.getDistanceToFirstPnt(self.segmentsList[0].p0, radius)
            listSegmentPoint = segm.getListPointWithDistance(dist, ifLast, radius, distToPrev)
            if listSegmentPoint is not None:
                for pnt in listSegmentPoint:
                    if withLast is False:
                        pntPro1 = Geom.Pnt(pnt.x(), pnt.y(), 0.0)
                        pntPro2 = Geom.Pnt(endPoint.x(), endPoint.y(), 0.0)
                        if pntPro1.distance(pntPro2) < radius:
                            pass
                        else:
                            listPoint.append(pnt)
                    else:
                        listPoint.append(pnt)
        return listPoint

    class SegmLine:
        def __init__(self, startPnt, endPnt):
            self.p0 = startPnt
            self.p1 = endPnt
            self.p0x = startPnt.x()
            self.p0y = startPnt.y()
            self.p1x = endPnt.x()
            self.p1y = endPnt.y()
            self.vecSegm = Geom.Vec(startPnt, endPnt)
            self.len = self.vecSegm.magnitude()

        def getNumberOfParts(self, dist):
            n = self.vecSegm.magnitude() / dist
            return n

        def getPntByCoef(self, t):
            if t == 0:
                return self.p0
            elif t == 1:
                return self.p1
            elif 0 < t < 1:
                return self.p0.translated(self.vecSegm.scaled(t))
            else:
                # print("COEFICIENT T OUT OF RANGE!!!")
                return None

        def getPntByDist(self, dist):
            if dist == 0:
                return self.p0
            elif dist == self.len:
                return self.p1
            else:
                normalVec = self.vecSegm.normalized()
                resPnt = self.p0.translated(normalVec.multiplied(dist))
                return resPnt

        def getDistanceToFirstPnt(self, q, dist):
            qx = q.x()
            qy = q.y()
            len = 4.0 * math.pow(dist * 0.5, 2)
            p0x = self.p0x
            p0y = self.p0y
            dirVec = self.vecSegm.normalized()
            dx = dirVec.x()
            dy = dirVec.y()
            a = math.pow(dx, 2.0) + math.pow(dy, 2.0)
            b = (-2. * dx * qx) + (p0x * dx) + (dx * p0x) - (2.0 * dy * qy) + (p0y * dy) + (dy * p0y)
            c = (math.pow(qx, 2)) - (2.0 * qx * p0x) + (math.pow(p0x, 2)) + (math.pow(qy, 2)) - (2.0 * qy * p0y) + (
                math.pow(p0y, 2)) - len
            D = math.pow(b, 2) - (4.0 * a * c)
            if D > 0.0:
                t1 = (-b + math.sqrt(D)) / (2.0 * a)
                t2 = (-b - math.sqrt(D)) / (2.0 * a)
                if t1 >= t2:
                    resPnt = self.getPntByDist(math.fabs(t1))
                    vecDist = Geom.Vec(self.p0, resPnt)
                    return vecDist.magnitude()
                elif t1 < t2:
                    resPnt = self.getPntByDist(math.fabs(t2))
                    vecDist = Geom.Vec(self.p0, resPnt)
                    return vecDist.magnitude()
            elif D == 0:
                t = - b / (2.0 * a)
                resPnt = self.getPntByDist(t)
                vecDist = Geom.Vec(self.p0, resPnt)
                return vecDist.magnitude()
            elif D < 0:
                # print("D", D)
                # print("WRONG DISCRIMINANT")
                return None

        def getListPointWithDistance(self, distance, ifLast, rad, startDistance):
            pointList = []

            vecForAngle = Geom.Vec(Geom.Pnt(self.p0.x(), self.p0.y(), self.p0.z()),
                                   Geom.Pnt(self.p1.x(), self.p1.y(), self.p0.z()))
            angle = self.vecSegm.angle(vecForAngle)
            len = self.len
            dist = distance
            radius = rad
            startDist = startDistance
            if angle == 0.5 * math.pi:
                return pointList
            elif angle < 0.00001:
                dist = distance / math.cos(angle)
            if ifLast:
                segmN = int(((len - startDist) / dist) + 1.0)
            elif startDist is not None:
                segmN = int(((len - startDist) / dist) + 1.0)
            else:
                segmN = int(((len - radius) / dist) + 1.0)

            for i in range(segmN):
                resPnt = self.getPntByDist(startDist + (dist * float(i)))
                pointList.append(resPnt)
            return pointList


class Bohrpfahlwand(lx.Wall):
    _heightParamName = "Columns height"
    _diameterParamName = "Columns diameter"
    _typeParamName = "Type of structure"
    _columnDistanceParamName = "Distance between columns"

    _ifProfilesParamName = "Availability of profiles"
    _profilesTypeParamName = "Profiles type"
    _profilesSizeParamName = "Profiles size"
    _profilesHeightParamName = "Profiles height"
    _profilesAngleParamName = "Profiles angle"

    _mainLineParamName = "Show main line"

    _ifExtrudeFacesParamName = "Extruded faces"
    _thicknessParamName = "Thickness"
    _wall_retreat_param_name = "Wall retreat"

    _cutColumnsWithLineParamName = "Column height line"
    _depthColumnsWithLineParamName = "Columns depth line"
    _columnTransparencyParamName = "Columns transparency"
    _cutProfilesWithLineParamName = "Profiles height line"
    _representationPropName = "_representation"

    _polylineParamName = "Polyline"
    _polylineIDPropName = "PolylineID"

    def __init__(self, aArg):
        lx.Wall.__init__(self, aArg)
        self.registerPythonClass("Bohrpfahlwand", "OpenLxApp.ElementAssembly")
        # Register properties
        self.setPropertyHeader(lxStr("Bohrpfahlwand creator"), -1)
        self.setPropertyGroupName(lxStr("Bohrpfahlwand creator parameters"), -1)

        self._type = self.registerPropertyEnum(self._typeParamName, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, 73)
        self._type.setEmpty()
        self._type.addEntry(lxStr("Tangierend"), -1)
        self._type.addEntry(lxStr("Überschnitten"), -1)
        self._type.addEntry(lxStr("Aufgelöst"), -1)

        self._height = self.registerPropertyDouble(self._heightParamName, 10.0, lx.Property.VISIBLE,
                                                   lx.Property.EDITABLE, 71)

        self._diameter = self.registerPropertyDouble(self._diameterParamName, 0.5, lx.Property.VISIBLE,
                                                     lx.Property.EDITABLE, 72)

        self._columnDistance = self.registerPropertyDouble(self._columnDistanceParamName, 1.0, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 74)

        self._ifProfiles = self.registerPropertyEnum(self._ifProfilesParamName, 0, lx.Property.VISIBLE,
                                                     lx.Property.EDITABLE, 76)
        self._ifProfiles.setEmpty()
        self._ifProfiles.addEntry(lxStr("No"), -1)
        self._ifProfiles.addEntry(lxStr("Yes"), -1)

        self._profilesType = self.registerPropertyEnum(self._profilesTypeParamName, 0, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 77)
        self._profilesType.setEmpty()
        for i in range(len(types)):
            self._profilesType.addEntry(lxStr(types[i]), -1)

        self._profilesSize = self.registerPropertyEnum(self._profilesSizeParamName, 0, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 78)
        self._profilesSize.setEmpty()
        for i in range(len(typ2)):
            if types[0] == typ2[i][0]:
                self._profilesSize.addEntry(lxStr(typ2[i][1]), -1)

        self._profilesHeight = self.registerPropertyDouble(self._profilesHeightParamName, 10.0, lx.Property.VISIBLE,
                                                           lx.Property.EDITABLE, 79)

        self._profilesAngle = self.registerPropertyDouble(self._profilesAngleParamName, 0.0, lx.Property.VISIBLE,
                                                          lx.Property.EDITABLE, 80)

        # =============================================

        self._ifExtrudeFaces = self.registerPropertyEnum(self._ifExtrudeFacesParamName, 0, lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, 82)
        self._ifExtrudeFaces.setEmpty()
        self._ifExtrudeFaces.addEntry(lxStr("No"), -1)
        self._ifExtrudeFaces.addEntry(lxStr("Yes"), -1)

        self._thickness = self.registerPropertyDouble(self._thicknessParamName, 0.01, lx.Property.VISIBLE,
                                                      lx.Property.EDITABLE, 84)
        self._wall_retreat = self.registerPropertyDouble(self._wall_retreat_param_name, 0.0, lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, 85)

        if self._ifProfiles.getValue is 0:
            self._profilesType.setVisible(False)
            self._profilesSize.setVisible(False)
            self._profilesHeight.setVisible(False)
        else:
            self._profilesType.setVisible(True)
            self._profilesSize.setVisible(True)
            self._profilesHeight.setVisible(True)

        # ====================================================================

        self._cutColumnsWithLineBtn = self.registerPropertyButton(self._cutColumnsWithLineParamName,
                                                                  lx.Property.VISIBLE, lx.Property.EDITABLE, 483)

        # ====================================================================
        self._cutProfilesWithLineBtn = self.registerPropertyButton(self._cutProfilesWithLineParamName,
                                                                   lx.Property.VISIBLE, lx.Property.EDITABLE, 485)

        # =====================================================================
        self._depthColumnsWithLineBtn = self.registerPropertyButton(self._depthColumnsWithLineParamName,
                                                                    lx.Property.VISIBLE, lx.Property.EDITABLE, 484)

        # =====================================================================
        self._columnTransparency = self.registerPropertyInteger(self._columnTransparencyParamName, 0,
                                                                lx.Property.VISIBLE, lx.Property.EDITABLE, 75)
        # =====================================================================

        self._showMainLine = self.registerPropertyEnum(self._mainLineParamName, 0, lx.Property.VISIBLE,
                                                       lx.Property.EDITABLE, 81)
        self._showMainLine.setEmpty()
        self._showMainLine.addEntry(lxStr("No"), -1)
        self._showMainLine.addEntry(lxStr("Yes"), -1)

        self._representation = self.registerPropertyEnum(self._representationPropName, 1, lx.Property.VISIBLE,
                                                         lx.Property.EDITABLE, 506)
        self._representation.setEmpty()
        self._representation.addEntry(lxStr("Axis"), 509)  # Index 0
        self._representation.addEntry(lxStr("SolidModel"), 508)  # Index 1

        # Additional not visible parameters
        self._modules = self.registerPropertyDouble("Modules", 0.0, lx.Property.NOT_VISIBLE, lx.Property.NOT_EDITABLE,
                                                    -1)

        self._set_steps()

        # ===== MAIN LINE =====
        self._polyline = self.registerPropertyString(self._polylineParamName, lxStr(""), lx.Property.NOT_VISIBLE,
                                                     lx.Property.NOT_EDITABLE, -1)
        self._polylineID = self.registerPropertyString(self._polylineIDPropName, lxStr(""), lx.Property.NOT_VISIBLE,
                                                       lx.Property.NOT_EDITABLE, -1)

        # ===== CUT COLUMNS LINE =====
        self._cutColumnsPolyline = self.registerPropertyString("_cutColumnsPolyline", lxStr(""),
                                                               lx.Property.NOT_VISIBLE, lx.Property.NOT_EDITABLE, -1)
        self._cutColumnsLineBaseData = None
        cutColumnsLineDataStr = cstr(self._cutColumnsPolyline.getValue())
        if cutColumnsLineDataStr:
            self._cutColumnsLineBaseData = self.read_from_string(cutColumnsLineDataStr)

        

        # ===== DEPTH COLUMNS LINE =====
        self._depthColumnsPolyline = self.registerPropertyString("_depthColumnsPolyline", lxStr(""),
                                                                 lx.Property.NOT_VISIBLE, lx.Property.NOT_EDITABLE, -1)
        self._depthColumnsLineBaseData = None
        depthColumnsLineDataStr = cstr(self._depthColumnsPolyline.getValue())
        if depthColumnsLineDataStr:
            self._depthColumnsLineBaseData = self.read_from_string(depthColumnsLineDataStr)

        # ===== CUT PROFILES LINE =====
        self._cutProfilesPolyline = self.registerPropertyString("_cutProfilesPolyline", lxStr(""),
                                                                lx.Property.NOT_VISIBLE, lx.Property.NOT_EDITABLE, -1)
        self._cutProfilesLineBaseData = None
        cutProfilesLineDataStr = cstr(self._cutProfilesPolyline.getValue())
        if cutProfilesLineDataStr:
            self._cutProfilesLineBaseData = self.read_from_string(cutProfilesLineDataStr)

        self.setBoundingBoxEnabled(False)
        

    def _set_steps(self):
        self._height.setSteps(0.05)
        self._diameter.setSteps(0.01)
        self._columnDistance.setSteps(0.01)
        self._profilesHeight.setSteps(0.05)
        self._profilesAngle.setSteps(5.0)
        self._thickness.setSteps(0.01)
        self._wall_retreat.setSteps(0.01)

    @staticmethod
    def _create_sub_element_face(point_list):
        edgeList = Topo.vector_Edge(4)
        edgeList[0] = Topo.EdgeTool.makeEdge(point_list[0], point_list[1])
        edgeList[1] = Topo.EdgeTool.makeEdge(point_list[1], point_list[2])
        edgeList[2] = Topo.EdgeTool.makeEdge(point_list[2], point_list[3])
        edgeList[3] = Topo.EdgeTool.makeEdge(point_list[3], point_list[0])
        wire = Topo.WireTool.makeWire(edgeList, Geom.Precision.linear_Resolution())
        face = Topo.FaceTool.makeFace(wire, Geom.Precision.linear_Resolution())
        geom = lx.createCurveBoundedPlaneFromFace(doc, face)
        elem = lx.SubElement.createIn(doc)
        elem.setGeometry(geom)
        return elem

    @staticmethod
    def _calculate_trimming(points, base_data):
        height_list = []
        polyline_elem = PolylineData.fromElement(base_data)
        trfs = pickedElement.getTransform()
        print("Polyline transform", trfs)
        cut_points_list = polyline_elem.getPntList()

        segments_list = []
        for k in range(len(cut_points_list) - 1):
            first_segment_pnt = cut_points_list[k]
            second_segment_pnt = cut_points_list[k + 1]
            segments_list.append([first_segment_pnt, second_segment_pnt])

        for i in range(len(points)):
            res_pnt = None
            if i == 0:
                main_pnt = Geom.Pnt2d(points[i].x(), points[i].y())
                second_pnt = Geom.Pnt2d(points[i + 1].x(), points[i + 1].y())
                angle = math.radians(90)
            elif i == len(points) - 1:
                main_pnt = Geom.Pnt2d(points[i].x(), points[i].y())
                second_pnt = Geom.Pnt2d(points[i - 1].x(), points[i - 1].y())
                angle = math.radians(90)
            else:
                second_pnt = Geom.Pnt2d(points[i - 1].x(), points[i - 1].y())
                main_pnt = Geom.Pnt2d(points[i].x(), points[i].y())
                next_pnt = Geom.Pnt2d(points[i + 1].x(), points[i + 1].y())
                angle = Geom.Vec2d.angle(
                    Geom.Vec2d(main_pnt, second_pnt),
                    Geom.Vec2d(main_pnt, next_pnt)) * 0.5

            pnt_for_vec_1 = main_pnt
            pnt_for_vec_2 = second_pnt.rotated(main_pnt, angle)
            check_line = Line2D.from2Points(pnt_for_vec_1, pnt_for_vec_2)
            for s in segments_list:

                x1 = s[0].x()
                y1 = s[0].y()
                z1 = s[0].z()

                x2 = s[1].x()
                y2 = s[1].y()
                z2 = s[1].z()

                segment_line = Line2D.from2Points(Geom.Pnt2d(x1, y1), Geom.Pnt2d(x2, y2))

                intersect_pnt = Line2D.intersect(check_line, segment_line)
                if intersect_pnt:
                    x = intersect_pnt.x()
                    y = intersect_pnt.y()

                    if x1 <= x <= x2 or x1 >= x >= x2 and y1 <= y <= y2 or y1 >= y >= y2:
                        a = (x - x1) / (x2 - x1) if (x2 - x1) != 0.0 else 0.0
                        b = (y - y1) / (y2 - y1) if (y2 - y1) != 0.0 else 0.0

                        if -0.001 < a - b < 0.001:
                            z = a * (z2 - z1) + z1
                            res_pnt = z
                            print("Z = ", z)
                            break

            height_list.append(res_pnt)
        return height_list

    @staticmethod
    def _create_sub_element_extruded_face(points_list, height, direction):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(points_list))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, direction, height)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        wall_elem = lx.SubElement.createIn(doc)
        wall_elem.setGeometry(geom)
        return wall_elem

    def create_profile(self, direction, profile_type, profile_size, pnt, height):
        profile = lx.IShapeProfileDef.createIn(doc)
        profile.setValuesFromPredefinedSteelProfile(lxStr(profile_type + ' ' + profile_size))
        eas2 = lx.ExtrudedAreaSolid.createIn(doc)
        eas2.setSweptArea(profile)
        eas2.setExtrudedDirection(Geom.Dir(0, 0, 1))
        eas2.setDepth(height)
        print("Profile depth: ", height)
        axis = Geom.Ax2(pnt, Geom.Dir(0, 0, 1), direction)
        column_element = lx.SubElement.createIn(doc)
        column_element.setGeometry(eas2)
        column_element.setLocalPlacement(axis)
        rotDir = Geom.Ax1(pnt, Geom.Dir(0, 0, -1))
        if self._profilesAngle.getValue() != 0.0:
            column_element.rotate(rotDir, math.radians(self._profilesAngle.getValue()))
        self.addSubElement(column_element)

    def _placeSegmentsAccLine(self, polyline):
        # Make transform for main points
        print("Place segment")
        type = self._type.getValue()
        diameter = self._diameter.getValue()
        if_face = False
        if type is 0:
            distance = diameter
        elif type is 1:
            distance = self._columnDistance.getValue()
        else:
            if_face = True
            distance = diameter + self._columnDistance.getValue()

        main_polyline = PolylineReader(polyline)

        raw_columns_point_list = main_polyline.getListPointWithDistanceOnPolyline(distance, diameter * 0.5, False)
        columns_point_list = []
        print("testttttygghnhnhnhht", len(raw_columns_point_list))
        for column_pnt in raw_columns_point_list:
            print("Add new pnt:")
            print()
            columns_point_list.append(column_pnt)
            print("New point added:", columns_point_list[-1])

        # calculate cut lines
        height_list = self._calculate_trimming(columns_point_list,
                                               self._cutColumnsLineBaseData) if self._cutColumnsLineBaseData else None
        depth_list = self._calculate_trimming(columns_point_list,
                                              self._depthColumnsLineBaseData) if self._depthColumnsLineBaseData else None
        profiles_height_list = self._calculate_trimming(columns_point_list,
                                                        self._cutProfilesLineBaseData) if self._cutProfilesLineBaseData and self._ifProfiles.getValue() == 1 else None
        print("testttttt")
        prev_column_pnt = None
        prev_column_height = None

        for j in range(len(columns_point_list)):
            pnt = columns_point_list[j]

            if height_list and depth_list:
                depth = depth_list[j] if depth_list[j] else pnt.z()
                height = height_list[j] - depth if height_list[j] else self._height.getValue()
            elif height_list and not depth_list:
                depth = pnt.z()
                height = height_list[j] - pnt.z() if height_list[j] else self._height.getValue()
            elif not height_list and depth_list:
                depth = depth_list[j] if depth_list[j] else pnt.z()
                height = pnt.z() - depth + self._height.getValue()
            else:
                height = self._height.getValue()
                depth = pnt.z()

            cylinder_geometry = lx.RightCircularCylinder.createIn(doc)
            cylinder_geometry.setHeight(height)
            cylinder_geometry.setRadius(diameter * 0.5)

            cylinder = lx.SubElement.createIn(doc)
            cylinder.setGeometry(cylinder_geometry)
            axis = Geom.Ax2(Geom.Pnt(pnt.x(), pnt.y(), depth), Geom.Dir(0, 0, 1))
            cylinder.setLocalPlacement(axis)
            cylinder.setTransparency(self._columnTransparency.getValue())
            self.addSubElement(cylinder)

            if self._ifProfiles.getValue() is 1:
                if j == 0:
                    direction = Geom.Dir(Geom.Vec(columns_point_list[0], columns_point_list[1]))
                elif j == len(columns_point_list) - 1:
                    direction = Geom.Dir(Geom.Vec(columns_point_list[len(columns_point_list) - 2],
                                                  columns_point_list[len(columns_point_list) - 1]))
                else:
                    direction = Geom.Dir(Geom.Vec(columns_point_list[j - 1], columns_point_list[j + 1]))

                self.create_profile(direction, str(types[self._profilesType.getValue()]),
                                    str(typ2[self._profilesSize.getValue()][1]),
                                    Geom.Pnt(pnt.x(), pnt.y(), depth),
                                    profiles_height_list[j] - depth if profiles_height_list
                                                                       and profiles_height_list[
                                                                           j] else self._profilesHeight.getValue())
            # Build faces
            if if_face:
                if prev_column_pnt:
                    face_points_list = [Geom.Pnt(
                        prev_column_pnt.x(),
                        prev_column_pnt.y(),
                        prev_column_height),
                        Geom.Pnt(pnt.x(), pnt.y(), depth + height),
                        pnt, prev_column_pnt]

                    thickness = self._thickness.getValue()
                    dir_vec = Geom.Vec(face_points_list[2], face_points_list[3]).rotated(
                        Geom.Ax1(face_points_list[2], Geom.Dir(0, 0, 1)), math.radians(90))
                    build_dir = Geom.Dir(dir_vec)
                    move_vec = dir_vec.normalized().scaled(-thickness * 0.5 + self._wall_retreat.getValue())
                    moved_face_points_list = []
                    for k in range(len(face_points_list)):
                        moved_face_points_list.append(face_points_list[k].translated(move_vec))

                    if self._ifExtrudeFaces.getValue() is 1:
                        face_elem = self._create_sub_element_extruded_face(moved_face_points_list, thickness, build_dir)
                        face_elem.setTransparency(self._columnTransparency.getValue())
                        self.addSubElement(face_elem)
                    else:
                        face_elem = self._create_sub_element_face(moved_face_points_list)
                        face_elem.setTransparency(self._columnTransparency.getValue())
                        self.addSubElement(face_elem)

                prev_column_pnt = pnt
                prev_column_height = depth + height



    def create_compound(self):
        axisCurve = self.getAxisRepresentation()
        polyLine = PolylineData.fromElement(get_polyline_data(axisCurve))
        if self._showMainLine.getValue() == 1:
            show_main_line = lx.SubElement.createIn(doc)
            show_main_line.setGeometry(axisCurve)
            show_main_line.setDiffuseColor(main_line_color)
            self.addSubElement(show_main_line)
        self._placeSegmentsAccLine(polyLine)

    def _updateGeometry(self):
        with EditMode(self.getDocument()):
            self.removeSubElements_exceptLine()
            self.create_compound()

    def removeSubElements_exceptLine(self):
        sub_elems = self.getSubElements()
        lineGlobID = Base.GlobalId(self._polylineID.getValue())
        for i in range(len(sub_elems)):
            if sub_elems[i].getGlobalId() != lineGlobID:
                self.removeSubElement(sub_elems[i])

    def set_height(self, height):
        with EditMode(self.getDocument()):
            self._height.setValue(clamp(height, 0.001, 100000.0))
            self._updateGeometry()

    def set_column_diameter(self, diameter):
        with EditMode(self.getDocument()):
            self._diameter.setValue(clamp(diameter, 0.01, 100.0))
            self._updateGeometry()

    ########TYPE########
    def set_type(self, type):
        with EditMode(self.getDocument()):
            self._type.setValue(type)
            if type is 0:
                self._columnDistance.setVisible(False)
            elif type is 1:
                self._columnDistance.setVisible(True)
            elif type is 2:
                self._columnDistance.setVisible(True)
            ui.UIApplication.getInstance().getUIDocument(doc).getSelection().forceUpdate()
            self._updateGeometry()

    def set_columns_distance(self, columnDistance):
        with EditMode(self.getDocument()):
            self._columnDistance.setValue(clamp(columnDistance, self._diameter.getValue(), 100.0))
            self._updateGeometry()
        if columnDistance < self._diameter.getValue():
            Base.Message().showMessageBoxWarning(qStr("Warning"), qStr("Value is too small"))
        elif columnDistance > 100.0:
            Base.Message().showMessageBoxWarning(qStr("Warning"), qStr("Value is too big"))

    def setProfiles(self, param):
        with EditMode(self.getDocument()):
            self._ifProfiles.setValue(param)
            if self._ifProfiles.getValue() is 0:
                self._profilesType.setVisible(False)
                self._profilesSize.setVisible(False)
                self._profilesHeight.setVisible(False)
                self._profilesAngle.setVisible(False)
            else:
                self._profilesType.setVisible(True)
                self._profilesSize.setVisible(True)
                self._profilesHeight.setVisible(True)
                self._profilesAngle.setVisible(True)
            ui.UIApplication.getInstance().getUIDocument(doc).getSelection().forceUpdate()
            self._updateGeometry()

    def setProfilesType(self, param):
        with EditMode(self.getDocument()):
            self._profilesType.setValue(param)
            self._updateGeometry()

    def setProfilesSize(self, param):
        with EditMode(self.getDocument()):
            self._profilesSize.setValue(param)
            self._updateGeometry()

    def setProfilesHeight(self, param):
        with EditMode(self.getDocument()):
            self._profilesHeight.setValue(clamp(param, self._height.getValue(), 100000.0))
            self._updateGeometry()

    def setProfilesAngle(self, param):
        with EditMode(self.getDocument()):
            self._profilesAngle.setValue(clamp(param, 0.0, 180.0))
            self._updateGeometry()

    def setExtrudedFaces(self, param):
        with EditMode(self.getDocument()):
            self._ifExtrudeFaces.setValue(param)
            if self._ifExtrudeFaces.getValue() is 0:
                self._thickness.setVisible(False)
            else:
                self._thickness.setVisible(True)
            ui.UIApplication.getInstance().getUIDocument(doc).getSelection().forceUpdate()
            self._updateGeometry()

    def setFaceThickness(self, param):
        with EditMode(self.getDocument()):
            self._thickness.setValue(clamp(param, 0.001, self._diameter.getValue() * 0.5))
            self._updateGeometry()

    def set_wall_retreat(self, param):
        with EditMode(self.getDocument()):
            self._wall_retreat.setValue(clamp(param, -100, 100))
            self._updateGeometry()

    def set_columns_height_line(self):
        with EditMode(self.getDocument()):
            selected_line = pickPolyline(uidoc)
            if selected_line is not None:
                self.setColumnsCutPolylineData(selected_line)  # !!!!!!!!!!!!!

    def set_columns_depth_line(self):
        with EditMode(self.getDocument()):
            selected_line = pickPolyline(uidoc)
            if selected_line is not None:
                self.setColumnsDepthPolylineData(selected_line)  # !!!!!!!!!!!!!

    def set_profiles_height_line(self):
        with EditMode(self.getDocument()):
            if_profiles = self._ifProfiles.getValue()
            print(if_profiles)
            if if_profiles is 0:
                add_profile = Base.Message().showMessageBoxQuestionYesNo(qStr("Warning"), qStr(
                    "Profiles were not added\nto the model. Add them?"))
                if add_profile:
                    self._ifProfiles.setValue(1)

            selected_line = pickPolyline(uidoc)
            if selected_line is not None:
                self.setProfilesCutPolylineData(selected_line)  # !!!!!!!!!!!!!

    def set_column_transparency(self, param):
        with EditMode(self.getDocument()):
            self._columnTransparency.setValue(clamp(param, 0, 100))
            self._updateGeometry()

    def set_main_line_visibility(self, param):
        with EditMode(self.getDocument()):
            self._showMainLine.setValue(param)
            self._updateGeometry()

    def setColumnsCutPolylineData(self, polylineData):
        if lxStr(self.write_to_string(polylineData)) is self._modules.getValue():
            return
        self._insidePropUpdate = True
        self._cutColumnsLineBaseData = polylineData
        self._cutColumnsPolyline.setValue(lxStr(self.write_to_string(polylineData)))
        self._updateGeometry()

    def setColumnsDepthPolylineData(self, polylineData):
        if lxStr(self.write_to_string(polylineData)) is self._modules.getValue():
            return
        self._insidePropUpdate = True
        self._depthColumnsLineBaseData = polylineData
        self._depthColumnsPolyline.setValue(lxStr(self.write_to_string(polylineData)))
        self._updateGeometry()

    def setProfilesCutPolylineData(self, polylineData):
        if lxStr(self.write_to_string(polylineData)) is self._modules.getValue():
            return
        self._insidePropUpdate = True
        self._cutProfilesLineBaseData = polylineData
        self._cutProfilesPolyline.setValue(lxStr(self.write_to_string(polylineData)))
        self._updateGeometry()

    @staticmethod
    def write_to_string(line_data):
        strn = ""
        strn += "{};".format(len(line_data))
        for i in range(len(line_data)):
            if line_data[i][0] == PolylineData.SegmType_Line:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};".format(line_data[i][0], \
                                                                                      line_data[i][1].x(),
                                                                                      line_data[i][1].y(),
                                                                                      line_data[i][1].z(), \
                                                                                      line_data[i][2].x(),
                                                                                      line_data[i][2].y(),
                                                                                      line_data[i][2].z())
            elif line_data[i][0] == PolylineData.SegmType_Arc:
                strn += "{0};{1:.5f};{2:.5f};{3:.5f};{4:.5f};{5:.5f};{6:.5f};{7:.5f};{8:.5f};{9:.5f};".format(
                    line_data[i][0], \
                    line_data[i][1].x(), line_data[i][1].y(), line_data[i][1].z(), \
                    line_data[i][2].x(), line_data[i][2].y(), line_data[i][2].z(), \
                    line_data[i][3].x(), line_data[i][3].y(), line_data[i][3].z())
            # if i != len(lineData)-1:
            #     strn += ";"
        i_n = len(line_data[len(line_data) - 1]) - 1
        strn += "{}".format(line_data[len(line_data) - 1][i_n])
        return strn

    @staticmethod
    def read_from_string(value):
        lineData = []
        st = value.split(";")
        # lenList = int(st[0])
        index = 0
        for i in range(int(st[0])):
            if int(st[index + 1]) == PolylineData.SegmType_Line:
                lineData.append(
                    [int(st[index + 1]), Geom.Pnt(float(st[index + 2]), float(st[index + 3]), float(st[index + 4])), \
                     Geom.Pnt(float(st[index + 5]), float(st[index + 6]), float(st[index + 7]))])
                index += 7
            elif int(st[index + 1]) == PolylineData.SegmType_Arc:
                lineData.append(
                    [int(st[index + 1]), Geom.Pnt(float(st[index + 2]), float(st[index + 3]), float(st[index + 4])), \
                     Geom.Pnt(float(st[index + 5]), float(st[index + 6]), float(st[index + 7])), \
                     Geom.Pnt(float(st[index + 8]), float(st[index + 9]), float(st[index + 10]))])
                index += 10

        i_n = len(lineData[int(st[0]) - 1])
        if st[len(st) - 1] == "True":
            bl = True
        else:
            bl = False
        lineData[int(st[0]) - 1].append(bl)

        return lineData

    def polyline(self):
        return self._polyline.getValue()

    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())
        with EditMode(doc):
            if not Geom.GeomTools.isEqual(x, 1.):
                pass
            if not Geom.GeomTools.isEqual(y, 1.):
                pass
            if not Geom.GeomTools.isEqual(z, 1.):
                old = self._height.getValue()
                self.set_height(old * z)

            self.translateAfterScaled(aVec, aScaleBasePnt)

    def _switchRepresentations(self, index):
        with EditMode(self.getDocument()):
            if index == 0:  # Index 0
                self.showAxisRepresentation()
                self.removeSubElements_exceptLine()
            else:
                self.showSolidModelRepresentation()

                """
                Recreate the "MultiGeo" based on the Axis
                """
                self._updateGeometry()

    def getGlobalClassId(self):
        return GUID_CLASS

    def onPropertyChanged(self, aPropertyName):
        print(aPropertyName)

        if aPropertyName == Bohrpfahlwand._heightParamName:
            self.set_height(self._height.getValue())
        elif aPropertyName == Bohrpfahlwand._diameterParamName:
            self.set_column_diameter(self._diameter.getValue())
        elif aPropertyName == Bohrpfahlwand._typeParamName:
            self.set_type(self._type.getValue())
        elif aPropertyName == Bohrpfahlwand._columnDistanceParamName:
            self.set_columns_distance(self._columnDistance.getValue())
        elif aPropertyName == Bohrpfahlwand._ifProfilesParamName:
            self.setProfiles(self._ifProfiles.getValue())
        elif aPropertyName == Bohrpfahlwand._profilesTypeParamName:
            self.setProfilesType(self._profilesType.getValue())
        elif aPropertyName == Bohrpfahlwand._profilesSizeParamName:
            self.setProfilesSize(self._profilesSize.getValue())
        elif aPropertyName == Bohrpfahlwand._profilesHeightParamName:
            self.setProfilesHeight(self._profilesHeight.getValue())
        elif aPropertyName == Bohrpfahlwand._profilesAngleParamName:
            self.setProfilesAngle(self._profilesAngle.getValue())

        elif aPropertyName == Bohrpfahlwand._ifExtrudeFacesParamName:
            self.setExtrudedFaces(self._ifExtrudeFaces.getValue())

        elif aPropertyName == self._thickness.getName():
            self.setFaceThickness(self._thickness.getValue())
        elif aPropertyName == self._wall_retreat.getName():
            self.set_wall_retreat(self._wall_retreat.getValue())
        elif aPropertyName == Bohrpfahlwand._cutColumnsWithLineParamName:
            self.set_columns_height_line()
        elif aPropertyName == Bohrpfahlwand._depthColumnsWithLineParamName:
            self.set_columns_depth_line()
        elif aPropertyName == Bohrpfahlwand._cutProfilesWithLineParamName:
            self.set_profiles_height_line()
        elif aPropertyName == Bohrpfahlwand._columnTransparencyParamName:
            self.set_column_transparency(self._columnTransparency.getValue())

        elif aPropertyName == Bohrpfahlwand._mainLineParamName:
            self.set_main_line_visibility(self._showMainLine.getValue())

        if aPropertyName == self._representation.getName():
            self._switchRepresentations(self._representation.getValue())

    def setAxisCurve(self, axisCurve):
        with EditMode(self.getDocument()):
            """
            Here we set the Axis
            """
            doc = self.getDocument()
            polyLine = PolylineData.fromElement(get_polyline_data(axisCurve))
            segmCount = polyLine.segmentCount()
            new_axis_geometry = lx.CompositeCurve.createIn(doc)

            main_point = Geom.Pnt(0.0, 0.0, 0.0)
            for segmId in range(segmCount):
                segmType = polyLine.segmentType(segmId)
                if segmType == PolylineData.SegmType_Line:
                    start_pnt = polyLine.segmStartPt(segmId)
                    end_pnt = polyLine.segmEndPt(segmId)

                    first_pnt = main_point.rotated(
                        Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0.0, 0.0, 1.0)),
                        Geom.Vec.angle(
                            Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(1.0, 0.0, 0.0)),
                            Geom.Vec(start_pnt, end_pnt))
                    ).translated(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), start_pnt))

                    second_pnt = main_point.rotated(
                        Geom.Ax1(Geom.Pnt(0.0, 0.0, 0.0), Geom.Dir(0.0, 0.0, 1.0)),
                        Geom.Vec.angle(
                            Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), Geom.Pnt(1.0, 0.0, 0.0)),
                            Geom.Vec(start_pnt, end_pnt))
                    ).translated(Geom.Vec(Geom.Pnt(0.0, 0.0, 0.0), end_pnt))

                    first_pnt.transformed(global_transform)
                    second_pnt.transformed(global_transform)

                    new_axis_geometry.addSegment(lx.createLineSegment(doc, first_pnt, second_pnt))
                    print("=====Line segment=====")
                    print(first_pnt.x(), first_pnt.y(), first_pnt.z())
                    print(second_pnt.x(), second_pnt.y(), second_pnt.z())

                elif segmType == PolylineData.SegmType_Arc:
                    arc_segment = polyLine.segmArc(segmId)
                    start_pnt = arc_segment.paramPt(0.0)
                    middle_pnt = arc_segment.paramPt(0.5)
                    end_pnt = arc_segment.paramPt(1.0)
                    arc = Arc3Pnt(start_pnt, middle_pnt, end_pnt)
                    arc_center = arc.centerPt()
                    arc_angle = arc.angle()

                    first_pnt = start_pnt.translated(
                        Geom.Vec(start_pnt, middle_pnt).normalized().scaled(main_point.y()))
                    first_pnt.setZ(start_pnt.z() + main_point.z())
                    second_pnt = first_pnt.rotated(
                        Geom.Ax1(arc_center, Geom.Dir(0.0, 0.0, 1.0)), arc_angle * 0.5)
                    second_pnt.setZ(middle_pnt.z() + main_point.z())
                    third_pnt = first_pnt.rotated(
                        Geom.Ax1(arc_center, Geom.Dir(0.0, 0.0, 1.0)), arc_angle)
                    third_pnt.setZ(end_pnt.z() + main_point.z())

                    first_pnt.transformed(global_transform)
                    second_pnt.transformed(global_transform)
                    third_pnt.transformed(global_transform)

                    new_axis_geometry.addSegment(lx.createArc3PointsSegment(doc, first_pnt, second_pnt, third_pnt))
                    print("=====Line segment=====")
                    print(first_pnt.x(), first_pnt.y(), first_pnt.z())
                    print(second_pnt.x(), second_pnt.y(), second_pnt.z())
                    print(second_pnt.x(), second_pnt.y(), second_pnt.z())

            ok = self.setAxisRepresentation(new_axis_geometry)

            """
            Recreate the "MultiGeo" based on the Axis
            """
            self._updateGeometry()
            return ok


def selectPolyline(uidoc):
    uidoc.highlightByShapeType(Topo.ShapeType_WIRE)
    ok = uidoc.pickPoint()
    uidoc.stopHighlightByShapeType()
    if ok:
        return uidoc.getPickedElement()
    else:
        return None


def get_polyline_data(line_set):
    lineData = []
    wire = Topo.ShapeTool.isSingleWire(line_set.getShape())
    if Topo.WireTool.isClosed(wire):
        edges = Topo.WireTool.getEdges(Topo.WireTool.reversed(wire))
    else:
        edges = Topo.WireTool.getEdges(wire)

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
        else:
            raise RuntimeError("Unsupported edge type")

    print("Line data len:", len(lineData))
    return lineData


def pickPolyline(uidoc):
    ui.showStatusBarMessage(lxStr("[L] Select base line [Esc] Cancel"))
    lineSet = selectPolyline(uidoc)
    ui.showStatusBarMessage(lxStr(""))

    if lineSet is not None:
        return get_polyline_data(lineSet)
    else:
        return None


if __name__ == "__main__":
    doc = lx.Application.getInstance().getActiveDocument()
    droppedOnElement = None
    pickedElement = None
    if doc:
        doc.registerPythonScript(GUID_SCRPT)
        bohrpfahlwand = Bohrpfahlwand(doc)
        bohrpfahlwand.setDiffuseColor(Base.Color_fromCdwkColor(4))
        geometry = None

        """
        If the script is dropped on an Element take the Geometry and delete Element
        """
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            droppedOnElement = thisScript.getDroppedOnElement()
            if droppedOnElement:
                geometry = droppedOnElement.getGeometry()
                main_line_color = Base.Color(droppedOnElement.getOglMaterial().getDiffuseColor())
                global_transform = droppedOnElement.getTransform()
                if bohrpfahlwand.setAxisCurve(droppedOnElement):
                    doc.removeObject(droppedOnElement)
                    bohrpfahlwand._updateGeometry()

        """
        Ask the user to pick a Line, take the Geometry and delete Element
        """
        if geometry is None:
            ui.showStatusBarMessage(5944)
            uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
            uidoc.highlightByShapeType(Topo.ShapeType_WIRE)
            ok = uidoc.pickPoint()
            uidoc.stopHighlightByShapeType()
            ui.showStatusBarMessage(lxStr(""))
            if ok:
                pickedElement = uidoc.getPickedElement()
                geometry = pickedElement.getGeometry()
                main_line_color = Base.Color(pickedElement.getOglMaterial().getDiffuseColor())
                global_transform = pickedElement.getTransform()
                if bohrpfahlwand.setAxisCurve(pickedElement):
                    doc.removeObject(pickedElement)
                    bohrpfahlwand._updateGeometry()
