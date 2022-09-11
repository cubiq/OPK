import opk
import cadquery as cq
from cadquery import exporters
from random import choice

keys = {
    0: [
    { 't':'Num','fs':7},
    { 't':'/'},
    { 't':'*' },
    { 't':'-'}
    ],
    1: [
    { 't':'7' },
    { 't':'8' },
    { 't':'9' },
    { 't':'+','h':2,'oy':-0.5 }
    ],
    2: [
    { 't':'4' },
    { 't':'5','n':True },
    { 't':'6' }
    ],
    3: [
    { 't':'1' },
    { 't':'2' },
    { 't':'3' },
    { 't':'⊼','h':2,'oy':-0.5 },
    ],
    4: [
    { 'w': 2,'t':'0' },
    { 't':'.' }
    ],
}
colours=["tomato2","springgreen3","slateblue2","sienna1","seagreen3","orangered2","orchid2","maroon2","limegreen","lightseagreen","lightcoral","magenta3","yellow"]

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
assy = cq.Assembly()

y = 0
for i, r in enumerate(rows):
    x = 0
    for j,k in enumerate(r['keys']):
        kh = 1
        if 'h' in k:
            kh = k['h']
        kw = 1
        if 'w' in k:
            kw = k['w']
        name = "row{}_{}_U{}".format(i,j,kw)
        convex = False
        if 'convex' in k:
            convex = k['convex']
            name+= "_space"

        depth = 2.8
        if 'n' in k:
            if k['n']:
                name+= "_homing"
            depth = 3.6
        legend = ''
        if 't' in k:
            legend = k['t']
        font = mainFont
        if 'f' in k:
            font = k['f']
        fontSize=mainSize
        if 'fs' in k:
            fontSize = k['fs']

        print("Generating: {} {}".format(name, legend))
        cap = opk.keycap(angle=r['angle'], height=r['height'],
                         unitX=kw, unitY=kh,
                         convex=convex, depth=depth,
                         legend=legend, font=font,
                         fontsize=fontSize)
        # Export one key at the time
        #exporters.export(cap, './export/STEP/' + name + '.step')
        #exporters.export(cap, './export/STL/' + name + '.stl', tolerance=0.001, angularTolerance=0.05)
        w = 19.05 * kw / 2
        x+= w
        oy = 0.0
        if 'oy' in k:
            oy = k['oy']
        y += oy*19.05
        assy.add(cap, name=name, color=cq.Color(choice(colours)),
                 loc=cq.Location(cq.Vector(x,y,0)))
        x+= w
    y = -(i+1)*19.05

if 'show_object' in locals():
    show_object(assy)

# Export the whole assembly, very handy especially for STEP
#exporters.export(assy.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(assy.toCompound(), 'keycaps.step')
