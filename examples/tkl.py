import opk
import cadquery as cq
from cadquery import exporters
from kb_render import *

keys = {
    0: [
        {'t':'⎋'},
        {'t':'F1','ox':1.0,'fs':6},
        {'t':'F2','fs':6},
        {'t':'F3','fs':6},
        {'t':'F4','fs':6},
        {'t':'F5','ox':0.5,'fs':6},
        {'t':'F6','fs':6},
        {'t':'F7','fs':6},
        {'t':'F8','fs':6},
        {'t':'F9','ox':0.5,'fs':6},
        {'t':'F10','fs':6},
        {'t':'F11','fs':6},
        {'t':'F12','fs':6},
        {'t':'Print\nScreen','ox':0.5,'fs':3},
        {'t':'Screen\nLock','fs':3},
        {'t':'Pause','fs':3}
        ],
    1: [
        { 't':'`\n¬','fs':5, 'oy':-0.5},
        { 't':'!\n1','fs':5},
        { 't':'"\n2','fs':5},
        { 't':'£\n3','fs':5},
        { 't':'$\n4','fs':5},
        { 't':'%\n5','fs':5},
        { 't':'^\n6','fs':5},
        { 't':'&\n7','fs':5},
        { 't':'*\n8','fs':5},
        { 't':'(\n9','fs':5},
        { 't':')\n0','fs':5},
        { 't':'-\n_','fs':5},
        { 't':'+\n=','fs':5},
        { 'w':2,'t':'⌫','fs':12},
        { 't':'Ins','fs':5,'ox':0.5},
        { 't':'Home','fs':5},
        { 't':'Pg\nUp','fs':5},
    ],
    2: [
        { 'w':1.5,'t':'↹','fs':12,'oy':-0.5},
        { 't':'q' },
        { 't':'w' },
        { 't':'e' },
        { 't':'r' },
        { 't':'t' },
        { 't':'y' },
        { 't':'u' },
        { 't':'i' },
        { 't':'o' },
        { 't':'p' },
        { 't':'[\n{','fs':5 },
        { 't':']\n}','fs':5 },
        { 'w':1.5,'t':'|\n\\','fs':5 },
        { 't':'Del','ox':0.5,'fs':5 },
        { 't':'End','fs':5 },
        { 't':'Pg\nDn','fs':5}
    ],
    3: [
        { 'w':1.75,'t':'⇪','oy':-0.5 },
        { 't':'a' },
        { 't':'s' },
        { 't':'d' },
        { 't':'f','n': True },
        { 't':'g' },
        { 't':'h' },
        { 't':'j','n': True },
        { 't':'k' },
        { 't':'l' },
        { 't':';\n:','fs':5 },
        { 't':'\'\n@','fs':5 },
        { 'w':2.25,'t':'⊼','fs':12 }
    ],
    4: [
        { 'w':2.25,'t':'⇧','oy':-0.5 },
        { 't':'z' },
        { 't':'x' },
        { 't':'c' },
        { 't':'v' },
        { 't':'b' },
        { 't':'n' },
        { 't':'m' },
        { 't':',\n<','fs':5 },
        { 't':'.\n>','fs':5 },
        { 't':'/\n?','fs':5 },
        { 'w':2.75,'t':'⇧'},
        { 't':'↑','fs':12,'ox':1.5}
    ],
    5: [
        { 'w': 1.25,'t':'⎈','oy':-0.5 },
        { 'w': 1.25,'t':'','f':"/usr/share/fonts/texlive-fontawesome5/FontAwesome5Brands-Regular-400.otf"},
        { 'w': 1.25,'t':'⎇','f':"/usr/share/fonts/truetype/NotoSansSymbols-Black.ttf"},
        { 'w': 6.25, 'convex':True},
        { 'w':1.25, 't':'⎇','f':"/usr/share/fonts/truetype/NotoSansSymbols-Black.ttf" },
        {'w':1.25, 't':'Fn'},
        { 'w': 1.25,'t':'','f':"/usr/share/fonts/texlive-fontawesome5/FontAwesome5Brands-Regular-400.otf" },
        { 'w': 1.25,'t':'⎈'},
        { 't':'←','fs':12,'ox': 0.5},
        { 't':'↓','fs':12 },
        { 't':'→','fs':12 }
    ],
}

rows = [
    {'angle': 13, 'height': 16,   'keys': keys[0] },      # row 0, function row
    {'angle': 9,  'height': 14,   'keys': keys[1] },      # row 1, numbers row
    {'angle': 8,  'height': 12,   'keys': keys[2] },      # row 2, QWERT
    {'angle': -6, 'height': 11.5, 'keys': keys[3] },      # row 3, ASDFG
    {'angle': -8, 'height': 13,   'keys': keys[4] },      # row 4, ZXCVB
    {'angle': 0,  'height': 12.5, 'keys': keys[5] },      # row 5, bottom row
]

mainFont = "DejaVu Sans Mono"
mainSize = 9

sx = 19.05
sy = 19.05

assy = render_kb(rows, mainFont=mainFont, mainSize = mainSize, sx = sx, sy = sy)

if 'show_object' in locals():
    show_object(assy)

# Export the whole assembly, very handy especially for STEP
#exporters.export(assy.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(assy.toCompound(), 'keycaps.step')
