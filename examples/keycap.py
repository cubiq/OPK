import opk
import cadquery as cq
cap = opk.keycap(legend="",unitX=1,unitY=1,fontPath="./FontAwesome5Brands-Regular-400.otf")
#show_object(cap, name="keycap", options={"alpha": 0})

cq.exporters.export(cap, 'keycap.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(cap, 'keycap.step')
