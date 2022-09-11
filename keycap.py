from  opk import *
import cadquery as cq

rows = [
    {'angle': 13, 'height': 16},      # row 0, function row
    {'angle': 9,  'height': 14},      # row 1, numbers row
    {'angle': 8,  'height': 12},      # row 2, QWERT
    {'angle': -6, 'height': 11.5},      # row 3, ASDFG
    {'angle': -8, 'height': 13},      # row 4, ZXCVB
    {'angle': 0,  'height': 12.5},      # row 5, bottom row
]

legend = [
        {'t':'⎋','ox':-9.0,'oy':2.5,'fs':12,'f':"DejaVu Sans Mono"},
        {'t':'α','ox':8.8,'oy':3.0,'fs':2,'f':"DejaVu Sans Mono"},
        {'t':'ă','ox':-5.8,'oy':-3.0,'fs':8,'f':"DejaVu Sans Mono"},
        {'t':'x','ox':7.8,'oy':-3.0,'fs':5,'f':"DejaVu Sans Mono"},
        {'t':'o','fs':10}
          ]

cap = keycap(angle=rows[5]['angle'], height=rows[5]['height'],
             unitX=2, unitY=1,
             convex=False, depth=2.8,
             legend=legend)
cq.exporters.export(cap, 'space-penguin.stl', tolerance=0.001, angularTolerance=0.05)
if 'show_object' in locals():
    show_object(cap)

