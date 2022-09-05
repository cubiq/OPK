import opk
from cadquery import exporters

cap = opk.keycap()
show_object(cap, name="keycap", options={"alpha": 0})

#exporters.export(cap, 'keycap.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(cap, 'keycap.step')