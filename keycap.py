import opk
from cadquery import exporters

cap = keycap()
show_object(cap, name="keycap", options={"alpha": 0.4})

#exporters.export(cap, 'keycap.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(cap, 'keycap.step')