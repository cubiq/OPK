import opk
import cadquery as cq
from cadquery import exporters
from kb_render import *

keys = {
    0: [
    { 't':'Num','fs':7},
    { 't':'/'},
    { 't':'*' },
    { 't':'-'}
    ],
    1: [
    { 't':'7\nHome','fs':4.5 },
    { 't':'8\n↑','fs':4.5 },
    { 't':'9\nPgUp','fs':4.5 },
    { 't':'+','h':2,'oy':-0.5 }
    ],
    2: [
    { 't':'4\n←','fs':4.5 },
    { 't':'5','n':True },
    { 't':'6\n→','fs':4.5 }
    ],
    3: [
    { 't':'1\nEnd','fs':4.5 },
    { 't':'2\n↓','fs':4.5 },
    { 't':'3\nPgDn','fs':4.5 },
    { 't':'⊼','h':2,'oy':-0.5 },
    ],
    4: [
    { 'w': 2,'t':'0\nIns','fs':6 },
    { 't':'.\nDel', 'fs':5 }
    ],
}

#rows = [
    #{'angle': 13, 'height': 16,   'keys': keys[0] },      # row 0, function row
    #{'angle': 9,  'height': 14,   'keys': keys[1] },      # row 1, numbers row
    #{'angle': 8,  'height': 12,   'keys': keys[2] },      # row 2, QWERT
    #{'angle': -6, 'height': 11.5, 'keys': keys[3] },      # row 3, ASDFG
    #{'angle': -8, 'height': 13,   'keys': keys[4] },      # row 4, ZXCVB
    #{'angle': 0,  'height': 12.5, 'keys': keys[5] },      # row 5, bottom row
#]
rows = [
    {'angle': 9,  'height': 14,   'keys': keys[0] },      # row 1, numbers row
    {'angle': 8,  'height': 12,   'keys': keys[1] },      # row 2, QWERT
    {'angle': -6, 'height': 11.5, 'keys': keys[2] },      # row 3, ASDFG
    {'angle': -8, 'height': 13,   'keys': keys[3] },      # row 4, ZXCVB
    {'angle': 0,  'height': 12.5, 'keys': keys[4] },      # row 5, bottom row
]

mainFont = "DejaVu Sans Mono"
mainSize = 9

sx = 19.05
sy = 19.05

assy = render_kb(rows, mainFont=mainFont, mainSize = mainSize, sx = sx, sy = sy, export=True)

if 'show_object' in locals():
    show_object(assy)

# Export the whole assembly, very handy especially for STEP
#exporters.export(assy.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(assy.toCompound(), 'keycaps.step')
