import opk
import cadquery as cq
from cadquery import exporters
from kb_render import *

keys = {
    0: [
    { 't':'⎋ `\n  ¬','fs':5},
    { 't':'1\n!','fs':5 },
    { 't':'2\n\"','fs':5 },
    { 't':'3\n£','fs':5 },
    { 't':'4\n$','fs':5 },
    { 't':'5\n%','fs':5 },
    { 't':'6\n^','fs':5 },
    { 't':'7\n&','fs':5 },
    { 't':'8\n*','fs':5 },
    { 't':'9\n(','fs':5 },
    { 't':'0\n)','fs':5 },
    { 't':'-  ⌦\n_  ','fs':5 },
    { 't':'⌫ =\n  +','fs':5 }
    ],
    1: [
    { 't':'↹','fs':12},
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
    { 't':']\n}','fs':5 }
    ],
    2: [
    { 't':'#\n~','fs':5 },
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
    { 't':'⊼','fs':12 },
    ],
    3: [
    { 't':'⇧','fs':12 },
    { 't':'\\\n|','fs':5 },
    { 't':'z' },
    { 't':'x' },
    { 't':'c' },
    { 't':'v' },
    { 't':'b' },
    { 't':'n' },
    { 't':'m' },
    { 't':',\n<','fs':5 },
    { 't':'.\n>','fs':5 },
    { 't':'↑','fs':12 },
    { 't':'/\n?','fs':5 }
    ],
    4: [
    { 't':'⎈','f':"DejaVu Sans Mono",'fs':12 },
    { 't':'','f':"/usr/share/fonts/texlive-fontawesome5/FontAwesome5Brands-Regular-400.otf" },
    { 't':'⇓','f':"DejaVu Sans Mono",'fs':12},
    { 't':'⎇','f':"/usr/share/fonts/truetype/NotoSansSymbols-Black.ttf" },
    { 't':'⇑','f':"DejaVu Sans Mono",'fs':12 },
    { 'convex':True},
    { 't':'','convex':True,'f':"/usr/share/fonts/texlive-fontawesome5/FontAwesome5Brands-Regular-400.otf",'fs':9},
    { 'convex':True},
    { 't':'⎇','f':"/usr/share/fonts/truetype/NotoSansSymbols-Black.ttf" },
    { 't':'⇧','fs':12 },
    { 't':'←','fs':12 },
    { 't':'↓','fs':12 },
    { 't':'→','fs':12 }

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

assy = render_kb(rows, mainFont=mainFont, mainSize = mainSize, sx = sx, sy = sy)

if 'show_object' in locals():
    show_object(assy)

# Export the whole assembly, very handy especially for STEP
#exporters.export(assy.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(assy.toCompound(), 'keycaps.step')
