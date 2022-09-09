import opk
import cadquery as cq
from cadquery import exporters

keys = {
    0: [
    { 'unitX': 1 },
    ],
    1: [
    { 'unitX': 1 },
    { 'unitX': 2 }
    ],
    2: [
    { 'unitX': 1 },
    { 'unitX': 1.5 }
    ],
    3: [
    { 'unitX': 1 },
    { 'unitX': 1, 'depth': 3.6 },
    { 'unitX': 1.75 },
    { 'unitX': 2.25 }
    ],
    4: [
    { 'unitX': 1 },
    { 'unitX': 1.25 },
    { 'unitX': 1.75 },
    { 'unitX': 2.25 },
    { 'unitX': 2.75 },
    ],
    5: [
    { 'unitX': 1 },
    { 'unitX': 1.25 },
    { 'unitX': 1.5 },
    { 'unitX': 6.25, 'convex': True }
    ]
}

rows = [
    {'angle': 13, 'height': 16,   'keys': keys[0] },      # row 0, function row
    {'angle': 9,  'height': 14,   'keys': keys[1] },      # row 1, numbers row
    {'angle': 8,  'height': 12,   'keys': keys[2] },      # row 2, QWERT
    {'angle': -6, 'height': 11.5, 'keys': keys[3] },      # row 3, ASDFG
    {'angle': -8, 'height': 13,   'keys': keys[4] },      # row 4, ZXCVB
    {'angle': 0,  'height': 12.5, 'keys': keys[5] },      # row 5, bottom row
]

assy = cq.Assembly()

y = 0
for i, r in enumerate(rows):
    x = 0
    for k in r['keys']:
        name = "row{}_U{}".format(i,k['unitX'])
        convex = False
        if 'convex' in k:
            convex = k['convex']
            name+= "_space"
        
        depth = 2.8
        if 'depth' in k:
            if k['depth'] > depth: name+= "_homing"
            depth = k['depth']

        print("Generating: ", name)
        cap = opk.keycap(angle=r['angle'], height=r['height'], unitX=k['unitX'], convex=convex, depth=depth)
        # Export one key at the time
        #exporters.export(cap, './export/STEP/' + name + '.step')
        #exporters.export(cap, './export/STL/' + name + '.stl', tolerance=0.001, angularTolerance=0.05)
        w = 19.05 * k['unitX'] / 2
        x+= w
        assy.add(cap, name=name, loc=cq.Location(cq.Vector(x,y,0)))
        x+= w
    y -= 19.05

if 'show_object' in locals():
    show_object(assy)

# Export the whole assembly, very handy especially for STEP
#exporters.export(assy.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(assy.toCompound(), 'keycaps.step')