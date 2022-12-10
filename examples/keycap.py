"""
Simplest OPK Example to generate one key

Uncomment the exporters to save the model locally
"""
import opk
from cadquery import exporters

try:
    from cq_server.ui import ui, show_object
except ModuleNotFoundError:
    pass

cap = opk.keycap()

if 'show_object' in locals():
    show_object(cap)

#exporters.export(cap, 'keycap.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(cap, 'keycap.step')