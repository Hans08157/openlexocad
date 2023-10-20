# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Topo, Draw
import traceback, math, collections

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

#=====================================================================================================================

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


def qstr(str):
   return Base.StringTool.toQString(lxstr(str))
#Base.Message().showMessageBoxWarning(qstr("Title"), qstr("Message"))

def clamp(val, minVal, maxVal):
    return max(minVal, min(val, maxVal))

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

class KranPortal(lx.Element):

    _lengthName = "Gesamtlänge"  # "Length"
    _widthName = "Gesamtbreite"  # "Width"
    _seatHeightName = "Fundamenthöhe"  # "Seat Height"
    _level1HeightName = "Erster Höhenstand" # First Level
    _seatSizeName = "Fundamentbreite"  # "Seat Size"
    _topPlateWidthName = "Ballastbreite"  # "Upper Beam Size"
    _topPlateSizeName = "Ballaststärke"  # "Upper Beam Thickness"
    _metallprofileTypeName1 = "Metallprofil Typ St1"  # "Metallprofile type"
    _metallprofileName1 = "Metallprofil Stand 1"  # "Metallprofile"
    _metallprofileTypeName21 = "Metallprofil Typ St21"  # "Metallprofile type"
    _metallprofileName21 = "Metallprofil St21"  # "Metallprofile"
    _metallprofileTypeName22 = "Metallprofil Typ St22"  # "Metallprofile type"
    _metallprofileName22 = "Metallprofil St22"  # "Metallprofile"
    _topPlateNumberName = "Anzahl Ballast"  # "Number of Upper Beams"
    _ankerAngleName = "Halterungwinkel"  # "Angle of anker"
    _ankerLengthName = "Halterunglänge"  # "Length of anker"

    _color_I_beam = Base.Color(255, 170, 0)
    _color_I_beam_up = Base.Color(255, 140, 0)
    _color_Seat_beam = Base.Color(255, 255, 0)
    _color_Top_beam = Base.Color(184, 184, 184)

    def getGlobalClassId(self):
        return Base.GlobalId("{ac0ef876-798f-4047-97f6-156691daf4de}")

    def __init__(self, aArg): 
        lx.Element.__init__(self, aArg)
        self.registerPythonClass("KranPortal", "OpenLxApp.Element")
        
        # Register properties 
        self.setPropertyHeader(lxstr("Kran Portal"), -1)
        self.setPropertyGroupName(lxstr("Kran Portal Parameter"), -1)
        self._length = self.registerPropertyDouble(self._lengthName, 8.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._width = self.registerPropertyDouble(self._widthName, 6.6, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        # self._seatHeight = self.registerPropertyDouble(self._seatHeightName, 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._seatSize = self.registerPropertyDouble(self._seatSizeName, 0.8, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._level1Height = self.registerPropertyDouble(self._level1HeightName, 6.0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._metallprofileType1 = self.registerPropertyEnum(self._metallprofileTypeName1, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._metallprofileType1.setEmpty()
        for i in range(len(types)):
            # print(types[i])
            self._metallprofileType1.addEntry(lxstr(types[i]), -1)

        self._metallprofile1 = self.registerPropertyEnum(self._metallprofileName1, 21, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._metallprofile1.setEmpty()
        for i in range(len(typ2)):
            if types[0] == typ2[i][0]:
                self._metallprofile1.addEntry(lxstr(typ2[i][1]), -1)

        self._metallprofileType21 = self.registerPropertyEnum(self._metallprofileTypeName21, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._metallprofileType21.setEmpty()
        for i in range(len(types)):
            # print(types[i])
            self._metallprofileType21.addEntry(lxstr(types[i]), -1)

        self._metallprofile21 = self.registerPropertyEnum(self._metallprofileName21, 23, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._metallprofile21.setEmpty()
        for i in range(len(typ2)):
            if types[0] == typ2[i][0]:
                self._metallprofile21.addEntry(lxstr(typ2[i][1]), -1)

        self._metallprofileType22 = self.registerPropertyEnum(self._metallprofileTypeName22, 0, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._metallprofileType22.setEmpty()
        for i in range(len(types)):
            # print(types[i])
            self._metallprofileType22.addEntry(lxstr(types[i]), -1)

        self._metallprofile22 = self.registerPropertyEnum(self._metallprofileName22, 21, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._metallprofile22.setEmpty()
        for i in range(len(typ2)):
            if types[0] == typ2[i][0]:
                self._metallprofile22.addEntry(lxstr(typ2[i][1]), -1)
        
        self._topPlateSize = self.registerPropertyDouble(self._topPlateSizeName, 0.25, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._topPlateWidth = self.registerPropertyDouble(self._topPlateWidthName, 1.8, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._ankerAngle = self.registerPropertyDouble(self._ankerAngleName, 45., lx.Property.VISIBLE, lx.Property.EDITABLE, -1)
        self._ankerLength = self.registerPropertyDouble(self._ankerLengthName, 4., lx.Property.VISIBLE, lx.Property.EDITABLE, -1)


        self._topPlateNumber = self.registerPropertyInteger(self._topPlateNumberName, 6, lx.Property.VISIBLE, lx.Property.EDITABLE, -1)

        self._setAllSteps()

        self._updateGeometry()

        self._insidePropUpdate = False

        
        
    def _setAllSteps(self):
        self._length.setSteps(0.1)
        self._width.setSteps(0.1)
        # self._seatHeight.setSteps(0.1)
        self._seatSize.setSteps(0.1)
        self._topPlateSize.setSteps(0.01)
        self._topPlateWidth.setSteps(0.1)
        self._ankerLength.setSteps(0.1)



    def _createSeat(self):
        """ Creating seat beams """
        # lenSeat = 6.6   # self._seatSize.getValue()
        seatSize = self._seatSize.getValue()
        # heigSeat = 0.8  # nself._seatHeight.getValue()
        length = self._length.getValue()
        width = self._width.getValue()
        lenSeat = width

        profiletyp = str(types[self._metallprofileType1.getValue()])
        profilesize = str(typ2[self._metallprofile1.getValue()][1])

        profile = lx.IShapeProfileDef.createIn(doc)
        profile.setValuesFromPredefinedSteelProfile(lxstr(profiletyp + ' ' + profilesize))
        # profile.setValuesFromPredefinedSteelProfile(lxstr('HEA 800'))
        # w = profile.getOverallDepth()
        # d = profile.getOverallWidth()
        # profile.setOverallDepth(d)
        # profile.setOverallWidth(w)
        h = profile.getOverallDepth()
        b = profile.getOverallWidth()

        block = lx.Block.createIn(doc)
        block.setYLength(seatSize)
        block.setZLength(seatSize)
        block.setXLength(1.05*lenSeat)

        # orig = Geom.Pnt(0, 0, 0)
        bl_st = Geom.Pnt(-(1.05*lenSeat)/2., -seatSize/2., 0)
        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)
        bl_pos = Geom.Ax2(bl_st, zDir)
        block.setPosition(bl_pos)

        element1 = lx.SubElement.createIn(doc)
        element1.setGeometry(block)
        axis1 = Geom.Ax2(Geom.Pnt((length-b)/2., 0, 0), zDir, yDir) # width/2., 0
        element1.setLocalPlacement(axis1)
        # element1.setDiffuseColor(self._color_Seat_beam)

        element2 = lx.SubElement.createIn(doc)
        element2.setGeometry(block)
        axis2 = Geom.Ax2(Geom.Pnt(-(length-b)/2., 0, 0), zDir, yDir)
        element2.setLocalPlacement(axis2)
        
        self.addSubElement(element1)
        self.addSubElement(element2)


    def _createLevel1(self):
        
        length = self._length.getValue()
        width  = self._width.getValue()
        seatSize = self._seatSize.getValue()
        level1Height = self._level1Height.getValue()
        # connecting beam sizes
        h_beam = 0.2
        b_beam = 0.05

        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)

        # I-beam profile
        profiletyp = str(types[self._metallprofileType1.getValue()])
        profilesize = str(typ2[self._metallprofile1.getValue()][1])

        profile = lx.IShapeProfileDef.createIn(doc)
        profile.setValuesFromPredefinedSteelProfile(lxstr(profiletyp + ' ' + profilesize))
        
        # w = profile.getOverallDepth()
        # d = profile.getOverallWidth()
        # profile.setOverallDepth(d)
        # profile.setOverallWidth(w)
        h = profile.getOverallDepth()
        b = profile.getOverallWidth()
 
        profLength = level1Height

        # creating I-beam geometry
        eas = lx.ExtrudedAreaSolid.createIn(doc)
        eas.setSweptArea(profile)
        ax2 = Geom.Ax2(Geom.Pnt(0, 0, seatSize), zDir, yDir, xDir)
        eas.setPosition(ax2)
        eas.setExtrudedDirection(zDir)
        eas.setDepth(profLength)
        # 
        # axes for setLocalPlacement  
        axis1 = Geom.Ax2(Geom.Pnt((length-b)/2., (width-h)/2., 0), zDir) # width/2., 0
        axis2 = Geom.Ax2(Geom.Pnt((length-b)/2., -(width-h)/2., 0), zDir) # width/2., 0
        axis3 = Geom.Ax2(Geom.Pnt(-(length-b)/2., -(width-h)/2., 0), zDir) # width/2., 0
        axis4 = Geom.Ax2(Geom.Pnt(-(length-b)/2., (width-h)/2., 0), zDir) # width/2., 0
        
        # adding elements with I-beam geometry
        element1 = lx.SubElement.createIn(doc)
        element1.setGeometry(eas)
        element1.setLocalPlacement(axis1)
        element1.setDiffuseColor(self._color_I_beam)
        
        element2 = lx.SubElement.createIn(doc)
        element2.setGeometry(eas)
        element2.setLocalPlacement(axis2)
        element2.setDiffuseColor(self._color_I_beam)
        
        element3 = lx.SubElement.createIn(doc)
        element3.setGeometry(eas)
        element3.setLocalPlacement(axis3)
        element3.setDiffuseColor(self._color_I_beam)

        element4 = lx.SubElement.createIn(doc)
        element4.setGeometry(eas)
        element4.setLocalPlacement(axis4)
        element4.setDiffuseColor(self._color_I_beam)

        # horizontal connecting beam with rectangle geometry
        block = lx.Block.createIn(doc)
        block.setYLength(b_beam)
        block.setZLength(h_beam)
        block.setXLength(width-2*h)

        bl_st = Geom.Pnt(-(width)/2.+h, -b_beam/2., seatSize+level1Height/2.-h_beam/2.)
        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)
        bl_pos = Geom.Ax2(bl_st, zDir)
        block.setPosition(bl_pos)

        # crossed connecting beam with rectangle geometry
        block_cr_length = (level1Height**2 + (width-2.*h)**2)**0.5
        block_cr = lx.Block.createIn(doc)
        block_cr.setYLength(b_beam)
        block_cr.setZLength(h_beam)
        block_cr.setXLength(block_cr_length)
        bl_st_cr = Geom.Pnt(-(block_cr_length)/2., -b_beam/2., seatSize+level1Height/2.-h_beam/2.)
        bl_pos_cr = Geom.Ax2(bl_st_cr, zDir)
        block_cr.setPosition(bl_pos_cr)

        # adding elements with horizontal connecting beam
        element5 = lx.SubElement.createIn(doc)
        element5.setGeometry(block)
        axis5 = Geom.Ax2(Geom.Pnt(-(length-b)/2., 0, 0), zDir, yDir) # width/2., 0
        element5.setLocalPlacement(axis5)
        element5.setDiffuseColor(self._color_I_beam)

        element6 = lx.SubElement.createIn(doc)
        element6.setGeometry(block)
        axis6 = Geom.Ax2(Geom.Pnt((length-b)/2., 0, 0), zDir, yDir) # width/2., 0
        element6.setLocalPlacement(axis6)
        element6.setDiffuseColor(self._color_I_beam)

        # angle for crossing beam
        orig = Geom.Pnt(0, 0, seatSize+level1Height/2.)  
        ax1 = Geom.Ax1(orig, xDir)
        angle = math.atan(level1Height/(width-2.*h))
        # print(angle*180.0/3.1415)

        # adding elements with  crossed connecting beam
        element7 = lx.SubElement.createIn(doc)
        element7.setGeometry(block_cr)
        axis7 = Geom.Ax2(Geom.Pnt(-(length-b)/2., 0, 0), zDir, yDir) # width/2., 0
        element7.setLocalPlacement(axis7)
        element7.setDiffuseColor(self._color_I_beam)
        element7.rotate(ax1, -angle)

        element8 = lx.SubElement.createIn(doc)
        element8.setGeometry(block_cr)
        axis8 = Geom.Ax2(Geom.Pnt(-(length-b)/2., 0, 0), zDir, yDir) # width/2., 0
        element8.setLocalPlacement(axis8)
        element8.setDiffuseColor(self._color_I_beam)
        element8.rotate(ax1, angle)

        element9 = lx.SubElement.createIn(doc)
        element9.setGeometry(block_cr)
        axis9 = Geom.Ax2(Geom.Pnt((length-b)/2., 0, 0), zDir, yDir) # width/2., 0
        element9.setLocalPlacement(axis9)
        element9.setDiffuseColor(self._color_I_beam)
        element9.rotate(ax1, -angle)

        element10 = lx.SubElement.createIn(doc)
        element10.setGeometry(block_cr)
        axis10 = Geom.Ax2(Geom.Pnt((length-b)/2., 0, 0), zDir, yDir) # width/2., 0
        element10.setLocalPlacement(axis10)
        element10.setDiffuseColor(self._color_I_beam)
        element10.rotate(ax1, angle)

        # I-beam profile
        profiletyp2 = str(types[self._metallprofileType21.getValue()])
        profilesize2 = str(typ2[self._metallprofile21.getValue()][1])

        profile2 = lx.IShapeProfileDef.createIn(doc)
        profile2.setValuesFromPredefinedSteelProfile(lxstr(profiletyp2 + ' ' + profilesize2))
        
        # w = profile2.getOverallDepth()
        # d = profile2.getOverallWidth()
        # profile2.setOverallDepth(d)
        # profile2.setOverallWidth(w)
        h = profile2.getOverallDepth()
        b = profile2.getOverallWidth()
        t = profile2.getFlangeThickness()

        # upper crossed connecting beam with rectangle geometry
        block_cr_up_len = ((length-b)**2 + (width-b)**2)**0.5
        block_cr_up = lx.Block.createIn(doc)
        block_cr_up.setYLength(h_beam)
        block_cr_up.setZLength(b_beam)
        block_cr_up.setXLength(block_cr_up_len)
        bl_st_cr_up = Geom.Pnt(-block_cr_up_len/2., -h_beam/2., seatSize+level1Height-b_beam+t)
        bl_pos_cr_up = Geom.Ax2(bl_st_cr_up, zDir)
        block_cr_up.setPosition(bl_pos_cr_up)

        # angle for upper crossing beam
        orig = Geom.Pnt(0, 0, seatSize+level1Height/2.)  
        ax1 = Geom.Ax1(orig, zDir)
        angle = math.atan((length-b)/(width-b))

        element11 = lx.SubElement.createIn(doc)
        element11.setGeometry(block_cr_up)
        axis11 = Geom.Ax2(Geom.Pnt(0, 0, 0), zDir, yDir) # width/2., 0
        element11.setLocalPlacement(axis11)
        element11.setDiffuseColor(self._color_I_beam)
        element11.rotate(ax1, -angle)

        element12 = lx.SubElement.createIn(doc)
        element12.setGeometry(block_cr_up)
        axis12 = Geom.Ax2(Geom.Pnt(0, 0, 0), zDir, yDir) # width/2., 0
        element12.setLocalPlacement(axis12)
        element12.setDiffuseColor(self._color_I_beam)
        element12.rotate(ax1, angle)


        self.addSubElement(element1)
        self.addSubElement(element2)
        self.addSubElement(element3)
        self.addSubElement(element4)
        self.addSubElement(element5)
        self.addSubElement(element6)
        self.addSubElement(element7)
        self.addSubElement(element8)
        self.addSubElement(element9)
        self.addSubElement(element10)
        self.addSubElement(element11)
        self.addSubElement(element12)


    def _createLevel2(self):

        length = self._length.getValue()
        width  = self._width.getValue()
        seatSize = self._seatSize.getValue()
        level1Height = self._level1Height.getValue()

        orig = Geom.Pnt(0, 0, 0)
        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)

        profiletyp1 = str(types[self._metallprofileType21.getValue()])
        profilesize1 = str(typ2[self._metallprofile21.getValue()][1])

        profile1 = lx.IShapeProfileDef.createIn(doc)
        profile1.setValuesFromPredefinedSteelProfile(lxstr(profiletyp1 + ' ' + profilesize1))
        # profile.setValuesFromPredefinedSteelProfile(lxstr('HEA 1000'))
        # w = profile1.getOverallDepth()
        # d = profile1.getOverallWidth()
        # profile1.setOverallDepth(d)
        # profile1.setOverallWidth(w)
        h = profile1.getOverallDepth()
        b = profile1.getOverallWidth()

        profiletyp2 = str(types[self._metallprofileType22.getValue()])
        profilesize2 = str(typ2[self._metallprofile22.getValue()][1])

        profile2 = lx.IShapeProfileDef.createIn(doc)
        profile2.setValuesFromPredefinedSteelProfile(lxstr(profiletyp2 + ' ' + profilesize2))
        # profile.setValuesFromPredefinedSteelProfile(lxstr('HEA 800'))
        # w2 = profile2.getOverallDepth()
        # d2 = profile2.getOverallWidth()
        # profile2.setOverallDepth(d2)
        # profile2.setOverallWidth(w2)
        h2 = profile2.getOverallDepth()
        b2 = profile2.getOverallWidth()
 
        profLength_x = length
        profLength_y = width

        ax2_x = Geom.Ax2(Geom.Pnt(-profLength_x/2., 0, level1Height+seatSize), xDir, zDir, yDir)
        ax2_y = Geom.Ax2(Geom.Pnt(-profLength_y/2., 0, level1Height+seatSize), xDir, zDir, yDir)

        # lower I-beam
        eas_x = lx.ExtrudedAreaSolid.createIn(doc)
        eas_x.setSweptArea(profile1)
        eas_y = lx.ExtrudedAreaSolid.createIn(doc)
        eas_y.setSweptArea(profile1)
        eas_x.setPosition(ax2_x)
        eas_x.setExtrudedDirection(zDir)
        eas_x.setDepth(profLength_x)
        eas_y.setPosition(ax2_y)
        eas_y.setExtrudedDirection(zDir)
        eas_y.setDepth(profLength_y)

        # upper I-beam
        eas_x2 = lx.ExtrudedAreaSolid.createIn(doc)
        eas_x2.setSweptArea(profile2)
        eas_x2.setPosition(ax2_x)
        eas_x2.setExtrudedDirection(zDir)
        eas_x2.setDepth(profLength_x - 2*b2)

        eas_y2 = lx.ExtrudedAreaSolid.createIn(doc)
        eas_y2.setSweptArea(profile2)
        eas_y2.setPosition(ax2_y)
        eas_y2.setExtrudedDirection(zDir)
        eas_y2.setDepth(profLength_y - 2*b2)

        # axes for setLocalPlacement  
        axis1 = Geom.Ax2(Geom.Pnt(0, (width-b)/2., h/2.), zDir, xDir) # width/2., 0
        axis2 = Geom.Ax2(Geom.Pnt(0, -(width-b)/2., h/2.), zDir, xDir) # width/2., 0
        axis3 = Geom.Ax2(Geom.Pnt(-(length-b)/2., 0, h/2.), zDir, yDir) # width/2., 0
        axis4 = Geom.Ax2(Geom.Pnt((length-b)/2., 0, h/2.), zDir, yDir) # width/2., 0
        
        axis5 = Geom.Ax2(Geom.Pnt(b2, (width-b2)/2., h+h2/2.), zDir, xDir) # width/2., 0
        axis6 = Geom.Ax2(Geom.Pnt(b2, -(width-b2)/2., h+h2/2.), zDir, xDir) # width/2., 0
        axis7 = Geom.Ax2(Geom.Pnt(-(length-b2)/2., b2, h+h2/2.), zDir, yDir) # width/2., 0
        axis8 = Geom.Ax2(Geom.Pnt((length-b2)/2., b2, h+h2/2.), zDir, yDir) # width/2., 0

        # adding elements with I-beam geometry beam
        element1 = lx.SubElement.createIn(doc)
        element1.setGeometry(eas_x)
        element1.setLocalPlacement(axis1)
        element1.setDiffuseColor(self._color_I_beam)
        
        element2 = lx.SubElement.createIn(doc)
        element2.setGeometry(eas_x)
        element2.setLocalPlacement(axis2)
        element2.setDiffuseColor(self._color_I_beam)
        
        element3 = lx.SubElement.createIn(doc)
        element3.setGeometry(eas_y)
        element3.setLocalPlacement(axis3)
        element3.setDiffuseColor(self._color_I_beam)

        element4 = lx.SubElement.createIn(doc)
        element4.setGeometry(eas_y)
        element4.setLocalPlacement(axis4)
        element4.setDiffuseColor(self._color_I_beam)

        element5 = lx.SubElement.createIn(doc)
        element5.setGeometry(eas_x2)
        element5.setLocalPlacement(axis5)
        element5.setDiffuseColor(self._color_I_beam_up)
        
        element6 = lx.SubElement.createIn(doc)
        element6.setGeometry(eas_x2)
        element6.setLocalPlacement(axis6)
        element6.setDiffuseColor(self._color_I_beam_up)
        
        element7 = lx.SubElement.createIn(doc)
        element7.setGeometry(eas_y2)
        element7.setLocalPlacement(axis7)
        element7.setDiffuseColor(self._color_I_beam_up)

        element8 = lx.SubElement.createIn(doc)
        element8.setGeometry(eas_y2)
        element8.setLocalPlacement(axis8)
        element8.setDiffuseColor(self._color_I_beam_up)

        self.addSubElement(element1)
        self.addSubElement(element2)
        self.addSubElement(element3)
        self.addSubElement(element4)
        self.addSubElement(element5)
        self.addSubElement(element6)
        self.addSubElement(element7)
        self.addSubElement(element8)


    @staticmethod
    def _createFacetedBrepSubElement(listPoint, heightStep, dir):
        wire = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(listPoint))
        extrudeFace = Topo.FaceTool.extrudedFace(wire, dir, heightStep)
        geom = lx.FacetedBrep.createIn(doc)
        geom.setShape(extrudeFace)
        subElem = lx.SubElement.createIn(doc)
        subElem.setGeometry(geom)
        return subElem
    
    def _createUpperLevel(self):
        profiletyp1 = str(types[self._metallprofileType21.getValue()])
        profilesize1 = str(typ2[self._metallprofile21.getValue()][1])

        profile1 = lx.IShapeProfileDef.createIn(doc)
        profile1.setValuesFromPredefinedSteelProfile(lxstr(profiletyp1 + ' ' + profilesize1))
        
        # w = profile1.getOverallDepth()
        # d = profile1.getOverallWidth()
        # profile1.setOverallDepth(d)
        # profile1.setOverallWidth(w)
        h = profile1.getOverallDepth()
        b = profile1.getOverallWidth()

        profiletyp2 = str(types[self._metallprofileType22.getValue()])
        profilesize2 = str(typ2[self._metallprofile22.getValue()][1])

        profile2 = lx.IShapeProfileDef.createIn(doc)
        profile2.setValuesFromPredefinedSteelProfile(lxstr(profiletyp2 + ' ' + profilesize2))
        
        # w2 = profile2.getOverallDepth()
        # d2 = profile2.getOverallWidth()
        # profile2.setOverallDepth(d2)
        # profile2.setOverallWidth(w2)
        h2 = profile2.getOverallDepth()
        b2 = profile2.getOverallWidth()

        plateHeight = self._topPlateSize.getValue()
        # plateCount = 5
        plateTopWidth = self._topPlateWidth.getValue()
        plateWidth = plateTopWidth + 0.3

        seatSize = self._seatSize.getValue()
        length = self._length.getValue()
        width = self._width.getValue()
        level1Height = self._level1Height.getValue()
        nPN = self._topPlateNumber.getValue()

        # topBeamSize = self._topBeamSize.getValue()
        # topBeamLengthX = length
        # topBeamLengthY = width
        # nBm = self._topBeamNumber.getValue()
        # height = self._height.getValue()

        listPoint = []
        pt1 = Geom.Pnt(length/2., width/2.-plateWidth, seatSize+level1Height+h+h2)
        pt2 = Geom.Pnt(length/2., width/2., seatSize+level1Height+h+h2)
        pt3 = Geom.Pnt(-length/2., width/2., seatSize+level1Height+h+h2)
        pt4 = Geom.Pnt(-length/2., width/2.-plateWidth, seatSize+level1Height+h+h2)
        listPoint += [pt1, pt2, pt3, pt4]

        zDir = Geom.Dir(0, 0, 1)
        plate1 = KranPortal._createFacetedBrepSubElement(listPoint, plateHeight, zDir)
        self.addSubElement(plate1)

        listPoint = []
        pt1 = Geom.Pnt(length/2., -(width/2.-plateWidth), seatSize+level1Height+h+h2)
        pt2 = Geom.Pnt(length/2., -width/2., seatSize+level1Height+h+h2)
        pt3 = Geom.Pnt(-length/2., -width/2., seatSize+level1Height+h+h2)
        pt4 = Geom.Pnt(-length/2., -(width/2.-plateWidth), seatSize+level1Height+h+h2)
        listPoint += [pt1, pt2, pt3, pt4]
        plate1 = KranPortal._createFacetedBrepSubElement(listPoint, plateHeight, zDir)
        self.addSubElement(plate1)

        delta = 0.1 # !!!!!
        edge = 0.2
        pt_pp = Geom.Pnt(length/2., width/2., seatSize+level1Height+h+h2+plateHeight)
        pt_mp = Geom.Pnt(-pt_pp.x(), pt_pp.y(), pt_pp.z())
        pt_mm = Geom.Pnt(-pt_pp.x(), -pt_pp.y(), pt_pp.z())
        pt_pm = Geom.Pnt(pt_pp.x(), -pt_pp.y(), pt_pp.z())

        diag_p = Geom.Vec(pt_mm, pt_pp).normalized()
        diag_m = Geom.Vec(pt_pm, pt_mp).normalized()
        k_p = diag_p.y()/diag_p.x()
        k_m = diag_m.y()/diag_m.x()
        y_0 = delta * (1+k_p**2)**0.5

        z_0 = seatSize+level1Height+h+h2+plateHeight

        # South balast
        x_1, x_2, x_3, x_4, x_5, x_6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        y_1, y_2, y_3, y_4, y_5, y_6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        y_4 = -(width/2. - plateTopWidth)
        y_3 = y_4
        x_3, x_4 = (y_3+y_0)/k_m, (y_4+y_0)/k_p
        y_2 = -(width/2. - edge)
        y_5 = y_2
        x_5 = (y_5+y_0)/k_p
        x_2 = (y_2+y_0)/k_m
        x_1, x_6  = x_2, x_5
        y_1 = -width/2
        y_6 = y_1
        
        listPoint = []
        pt1 = Geom.Pnt(x_1, y_1, z_0)
        pt2 = Geom.Pnt(x_2, y_2, z_0)
        pt3 = Geom.Pnt(x_3, y_3, z_0)
        pt4 = Geom.Pnt(x_4, y_4, z_0)
        pt5 = Geom.Pnt(x_5, y_5, z_0)
        pt6 = Geom.Pnt(x_6, y_6, z_0)
        listPoint += [pt1, pt2, pt3, pt4, pt5, pt6]

        plate_s = KranPortal._createFacetedBrepSubElement(listPoint, plateHeight, zDir)

        # East balast
        x_1, x_2, x_3, x_4, x_5, x_6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        y_1, y_2, y_3, y_4, y_5, y_6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        x_3 = x_4 = length/2. - plateTopWidth
        x_2 = x_5 = length/2. - edge
        x_1 = x_6 = length/2.
        y_1 = y_2 = x_2*k_p - y_0
        y_3 = x_3*k_p - y_0
        y_4 = x_4*k_m + y_0
        y_6 = y_5 = x_5*k_m + y_0
        
        listPoint = []
        pt1 = Geom.Pnt(x_1, y_1, z_0)
        pt2 = Geom.Pnt(x_2, y_2, z_0)
        pt3 = Geom.Pnt(x_3, y_3, z_0)
        pt4 = Geom.Pnt(x_4, y_4, z_0)
        pt5 = Geom.Pnt(x_5, y_5, z_0)
        pt6 = Geom.Pnt(x_6, y_6, z_0)
        listPoint += [pt1, pt2, pt3, pt4, pt5, pt6]

        plate_e = KranPortal._createFacetedBrepSubElement(listPoint, plateHeight, zDir)
        
        # North balast
        x_1, x_2, x_3, x_4, x_5, x_6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        y_1, y_2, y_3, y_4, y_5, y_6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        y_4 = y_3 = (width/2. - plateTopWidth)
        y_2 = y_5 = (width/2. - edge)
        y_1 = y_6  = width/2
        x_2 = (y_2-y_0)/k_p
        x_3, x_4 = (y_3-y_0)/k_p, (y_4-y_0)/k_m
        x_5 = (y_5-y_0)/k_m
        x_1, x_6  = x_2, x_5
        
        listPoint = []
        pt1 = Geom.Pnt(x_1, y_1, z_0)
        pt2 = Geom.Pnt(x_2, y_2, z_0)
        pt3 = Geom.Pnt(x_3, y_3, z_0)
        pt4 = Geom.Pnt(x_4, y_4, z_0)
        pt5 = Geom.Pnt(x_5, y_5, z_0)
        pt6 = Geom.Pnt(x_6, y_6, z_0)
        listPoint += [pt1, pt2, pt3, pt4, pt5, pt6]

        plate_n = KranPortal._createFacetedBrepSubElement(listPoint, plateHeight, zDir)

        # West balast
        x_1, x_2, x_3, x_4, x_5, x_6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        y_1, y_2, y_3, y_4, y_5, y_6 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        x_3 = -(length/2. - plateTopWidth)
        x_4 = x_3
        x_2 = -(length/2. - edge)
        x_5 = -(length/2. - edge)
        x_1 = -length/2.
        x_6 = -length/2.
        y_1 = x_2*k_m - y_0
        y_2 = x_2*k_m - y_0
        y_3 = x_3*k_m - y_0
        y_4 = x_4*k_p + y_0
        y_6 = x_6*k_p + y_0
        y_5 = x_5*k_p + y_0
        
        listPoint = []
        pt1 = Geom.Pnt(x_1, y_1, z_0)
        pt2 = Geom.Pnt(x_2, y_2, z_0)
        pt3 = Geom.Pnt(x_3, y_3, z_0)
        pt4 = Geom.Pnt(x_4, y_4, z_0)
        pt5 = Geom.Pnt(x_5, y_5, z_0)
        pt6 = Geom.Pnt(x_6, y_6, z_0)
        listPoint += [pt1, pt2, pt3, pt4, pt5, pt6]

        plate_w = KranPortal._createFacetedBrepSubElement(listPoint, plateHeight, zDir)

        plates = []
        for i in range(nPN):
            plate = plate_s.copy()
            plate.translate(Geom.Vec(0, 0, i*plateHeight), Geom.CoordSpace_LCS) #,Geom.CoordSpace_LCS
            plates.append(plate)
            plate = plate_e.copy()
            plate.translate(Geom.Vec(0, 0, i*plateHeight), Geom.CoordSpace_LCS) #,Geom.CoordSpace_LCS
            plates.append(plate)
            plate = plate_n.copy()
            plate.translate(Geom.Vec(0, 0, i*plateHeight), Geom.CoordSpace_LCS) #,Geom.CoordSpace_LCS
            plates.append(plate)
            plate = plate_w.copy()
            plate.translate(Geom.Vec(0, 0, i*plateHeight), Geom.CoordSpace_LCS) #,Geom.CoordSpace_LCS
            plates.append(plate)

        for el in plates:
            self.addSubElement(el)
        
        doc.removeObject(plate_s)
        doc.removeObject(plate_e)
        doc.removeObject(plate_n)
        doc.removeObject(plate_w)

        # self.addSubElement(plate_s)
        # self.addSubElement(plate_e)
        # self.addSubElement(plate_n)
        # self.addSubElement(plate_w)

        # supporting beam with rectangle geometry
        block_length = self._ankerLength.getValue()
        anker_ang = math.pi*self._ankerAngle.getValue()/180.0

        h_sp_beam = 0.2
        b_sp_beam = 0.08

        zDir = Geom.Dir(0, 0, 1)
        xDir = Geom.Dir(1, 0, 0)
        yDir = Geom.Dir(0, 1, 0)
        place_length = ((length/2.)**2+(width/2.)**2)**0.5-1.4*b
        block = lx.Block.createIn(doc)
        block.setYLength(b_sp_beam)
        block.setZLength(h_sp_beam)
        block.setXLength(block_length)

        bl_st = Geom.Pnt(-(block_length-place_length), -b_sp_beam/2., seatSize+level1Height+h+h2)
        
        bl_pos = Geom.Ax2(bl_st, zDir)
        block.setPosition(bl_pos)

        # adding elements with supporting beam
        orig_LCP = Geom.Pnt(place_length, 0, seatSize+level1Height+h+h2)
        ax1_LCP = Geom.Ax1(orig_LCP, yDir)

        orig = Geom.Pnt(0, 0, 0)
        ax1 = Geom.Ax1(orig, zDir)
        angle = math.atan(width/length)

        axis = Geom.Ax2(Geom.Pnt(0, 0, 0), zDir, xDir)
        angleList = [angle, 3.1415-angle, 3.1415+angle, -angle]
        for ang in angleList:
            element = lx.SubElement.createIn(doc)
            element.setGeometry(block)
            element.setLocalPlacement(axis)
            element.rotate(ax1_LCP, anker_ang)
            element.rotate(ax1, ang)
            element.setDiffuseColor(self._color_I_beam)
            self.addSubElement(element)

    # def _createUpperBalastPlate(self):

    def createCompound(self):
        self._createSeat()
        self._createLevel1()
        self._createLevel2()
        self._createUpperLevel()


    def setLength(self, p):
        # nBeam = self._topBeamNumber.getValue()
        topPlateWidth = self._topPlateWidth.getValue()
        # seatSize = self._seatSize.getValue()
        minV = 2*(topPlateWidth + 0.02)
        with EditMode(self.getDocument()):
            self._length.setValue(clamp(p, minV, 1e04))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
            # self._insidePropUpdate = True
            
            
    def setWidth(self, p):
        # nBeam = self._topBeamNumber.getValue()
        topPlateWidth = self._topPlateWidth.getValue()
        # seatSize = self._seatSize.getValue()
        minV = 2*(topPlateWidth + 0.31)
        # if not self._insidePropUpdate:
        with EditMode(self.getDocument()):
            self._width.setValue(clamp(p, minV, 1e04))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setLevel1Height(self, p):
        minV = 0.2
        with EditMode(self.getDocument()):
            self._level1Height.setValue(clamp(p, minV, 1e04))
            self._updateGeometry()
        # if p < minV:
        #     Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setSeatHeight(self, p):
        minV = 0.2
        with EditMode(self.getDocument()):
            self._seatHeight.setValue(clamp(p, minV, 1e04))
            self._updateGeometry()
        # if p < minV:
        #     Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setSeatSize(self, p):
        minV = 0.5
        maxV = min(self._length.getValue()-0.01, self._width.getValue()-0.01)
        # print(maxV)
        with EditMode(self.getDocument()):
            self._seatSize.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))


    def setMetallprofileType1(self, p):
        with EditMode(self.getDocument()):
            self._metallprofileType1.setValue(p)
            self._updateGeometry()
            
    def setMetallprofile1(self, p):
        with EditMode(self.getDocument()):
            self._metallprofile1.setValue(p)
            self._updateGeometry()

    def setMetallprofileType21(self, p):
        with EditMode(self.getDocument()):
            self._metallprofileType21.setValue(p)
            self._updateGeometry()
            
    def setMetallprofile21(self, p):
        with EditMode(self.getDocument()):
            self._metallprofile21.setValue(p)
            self._updateGeometry()
            
    def setMetallprofileType22(self, p):
        with EditMode(self.getDocument()):
            self._metallprofileType22.setValue(p)
            self._updateGeometry()
            
    def setMetallprofile22(self, p):
        with EditMode(self.getDocument()):
            self._metallprofile22.setValue(p)
            self._updateGeometry()



    def setTopPlateSize(self, p):
        # length = self._length.getValue()
        # width  = self._width.getValue()
        # nBeam = self._topPlateNumber.getValue()
        maxV = 1e2
        with EditMode(self.getDocument()):
            self._topPlateSize.setValue(clamp(p, 0.01, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setTopPlateWidth(self, p):
        length = self._length.getValue()
        width  = self._width.getValue()
        # nBeam = self._topPlateNumber.getValue()
        minV = 0.01
        maxV = min(length/2., width/2. - 0.32)
        with EditMode(self.getDocument()):
            self._topPlateWidth.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))

    def setTopPlateNumber(self, p):
        # length = self._length.getValue()
        # width  = self._width.getValue()
        # topBeamSize = self._topBeamSize.getValue() 
        # maxV = min(int(length/topBeamSize/2.), int(width/topBeamSize/2.))
        # print(maxV)
        with EditMode(self.getDocument()):
            self._topPlateNumber.setValue(clamp(p, 0, 1e3))
            self._updateGeometry()
        if p < 0:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
        # if p > maxV:
        #     Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))

    def setAnkerAngle(self, p):
        # nBeam = self._topPlateNumber.getValue()
        minV = 0
        maxV = 90
        with EditMode(self.getDocument()):
            self._ankerAngle.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
    
    def setAnkerLength(self, p):
        # nBeam = self._topPlateNumber.getValue()
        minV = 0
        maxV = 1000
        with EditMode(self.getDocument()):
            self._ankerLength.setValue(clamp(p, minV, maxV))
            self._updateGeometry()
        if p > maxV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too big"))
        if p < minV:
            Base.Message().showMessageBoxWarning(qstr("Warning"), qstr("Value is too small"))
    

    def removeBeams(self):
        #print "removeBeams"
        beams = self.getSubElements() # removeSubElements()
        for b in beams:
            self.removeSubElement(b)
            doc.removeObject(b)


    def _updateGeometry(self):
        doc = self.getDocument()
        with EditMode(doc):
            self.removeBeams()
            self.createCompound()

    def onPropertyChanged(self, aPropertyName):
        #doc.beginEditing()
        # self._topBeamNumber.setMinValue(1)
        if aPropertyName == self._lengthName:
            self.setLength(self._length.getValue())
        elif aPropertyName == self._widthName:
            self.setWidth(self._width.getValue())
        # elif aPropertyName == self._seatHeightName:
        #     self.setSeatHeight(self._seatHeight.getValue())
        elif aPropertyName == self._seatSizeName:
            self.setSeatSize(self._seatSize.getValue())
        elif aPropertyName == self._level1HeightName:
            self.setLevel1Height(self._level1Height.getValue())

        elif aPropertyName == self._metallprofileTypeName1:
            self.setMetallprofileType1(self._metallprofileType1.getValue())
        elif aPropertyName == self._metallprofileName1:
            self.setMetallprofile1(self._metallprofile1.getValue())
        elif aPropertyName == self._metallprofileTypeName21:
            self.setMetallprofileType21(self._metallprofileType21.getValue())
        elif aPropertyName == self._metallprofileName21:
            self.setMetallprofile21(self._metallprofile21.getValue())
        elif aPropertyName == self._metallprofileTypeName22:
            self.setMetallprofileType22(self._metallprofileType22.getValue())
        elif aPropertyName == self._metallprofileName22:
            self.setMetallprofile22(self._metallprofile22.getValue())

        elif aPropertyName == self._topPlateSizeName:
            self.setTopPlateSize(self._topPlateSize.getValue())
        elif aPropertyName == self._topPlateWidthName:
            self.setTopPlateWidth(self._topPlateWidth.getValue())
        elif aPropertyName == self._ankerAngleName:
            self.setAnkerAngle(self._ankerAngle.getValue())
        elif aPropertyName == self._ankerLengthName:
            self.setAnkerLength(self._ankerLength.getValue())

        elif aPropertyName == self._topPlateNumberName:
            self.setTopPlateNumber(self._topPlateNumber.getValue())
            
        
        # self._insidePropUpdate = False



    def onScaling(self, aVec, aScaleBasePnt):
        x = abs(aVec.x())
        y = abs(aVec.y())
        z = abs(aVec.z())

        with EditMode(self.getDocument()):
            if not Geom.GeomTools.isEqual(x, 1.):
                print("Scaling in X")
                old = self._width.getValue()
                self.setWidth(old * x)
            if not Geom.GeomTools.isEqual(y, 1.):
                print("Scaling in Y")
                old = self._length.getValue()
                self.setLength(old * y)
            if not Geom.GeomTools.isEqual(z, 1.):
                print("Scaling in Z")
                old = self._height.getValue()
                self.setHeight(old * z)

            self.translateAfterScaled(aVec, aScaleBasePnt)

def main():
    doc.registerPythonScript(Base.GlobalId("{4cafa721-f366-41be-babf-b30fc37a031f}"))

    try:
        kp = KranPortal(doc)
        thisScript = lx.Application.getInstance().getActiveScript()
        if thisScript.isDragAndDropped():
            pos = Geom.Ax2(thisScript.getInsertionPoint(), Geom.Dir(0, 0, 1))
            kp.setLocalPlacement(pos)
    except Exception as e:
        print("{}".format(e))
        traceback.print_exc()
    finally:
        doc.recompute()
    
if __name__ == "__main__":
    main()
    

