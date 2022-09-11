from  opk import *
import cadquery as cq

cap = keycap(legend="",unitX=1,unitY=1.0, font="/usr/share/fonts/truetype/Font_Awesome_6_Brands-Regular-400.otf",convex=True)
cq.exporters.export(cap, 'space-penguin.stl', tolerance=0.001, angularTolerance=0.05)
cs = keycap(legend="",unitX=1,unitY=1.0, font="/usr/share/fonts/truetype/Font_Awesome_6_Brands-Regular-400.otf",convex=True)
cq.exporters.export(cs, 'space-cameleon.stl', tolerance=0.001, angularTolerance=0.05)

#exporters.export(cap, 'keycap.step')
