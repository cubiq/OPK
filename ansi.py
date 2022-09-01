#!/usr/bin/env python3

import cadquery as cq
from opk import *
leg = [["⎋","1","2","3","4","5","6","7","8","9","0","-","+","⌫"],
["↹","q","w","e","r","t","y","u","i","o","p","[","]","\\"],
["Caps","a","s","d","f","g","h","j","k","l",";","'","enter"],
["⇧","z","x","c","v","b","n","m",",",".","/","shift"],
["⎈","","Alt","","Alt","Fn","Menu","Ctrl"]]
lay= [[1]*13+[2],
      [1.5]+[1]*12+[1.5],
      [1.75]+[1]*11+[2.25],
      [2.25]+[1]*10+[2.75],
      [1.25,1.25,1.25,6.25,1.25,1.25,1.25,1.25]]
fonts=[
        ["DejaVu Sans Mono"]+["Noto Sans"]*13,
        ["DejaVu Sans Mono"]+["Noto Sans"]*13,
        ["DejaVu Sans Mono"]+["Noto Sans"]*12,
        ["DejaVu Sans Mono"]+["Noto Sans"]*10+["DejaVu Sans Mono"],
        ["DejaVu Sans Mono"]+["Font Awesome 6 Brands"]+["Noto Sans"]*6
        ]
sx=19.05
sy=19.05
m65 = cq.Assembly()
y = 0
i = -1
j = -1
angles=[9,8.5,-6,-7,0]

for row,ll,ff in zip(leg,lay,fonts):
    y -= sy
    i += 1
    x = 0
    for k,l,f in zip(row,ll,ff):
        print(k,l)
        w = l*sx/2.0
        j += 1
        x += w
        convex=False
        if k == '':
            convex=True
        scoop = 2.5
        if k in ['f','F','j','J']:
            scoop = 3.5
        m65.add(keycap(legend=k,
                       angle=angles[i],
                       font=f,
                       convex=convex,
                       depth = scoop,
                       unitX=l),
                name="k{}{}".format(i,j),
                loc=cq.Location(cq.Vector(x,y,0))
                )
        x += w

cq.exporters.export(m65.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
show_object(m65, name="legend", options={'color': 'red', 'alpha': 0})
