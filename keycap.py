import opk
from cadquery import exporters
try:
    from cq_server.ui import UI, show_object
except ModuleNotFoundError:
    pass

cap = opk.keycap()
show_object(cap)

#exporters.export(cap, 'keycap.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(cap, 'keycap.step')