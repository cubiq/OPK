#!/usr/bin/env python3


import cadquery as cq
from opk import *

leg = [["⎋","1","2","3","4","5","6","7","8","9","0","-","⌫"],
["↹","q", "w", "e","r","t","y","u","i","o","p","[","]"],
["#","a","s","d","f","g","h","j","k","l",";","'","⌅"],
["⇧","\\","z","x","c","v","b","n","m",",",".","↑","/"],
["⎈","","⇓","⎇","⇑","","","","⎇","⇧","←","↓","→"]]
lay= [[1]*13 , [1]*13,[1]*13,[1]*13,[1]*13]
rows=len(leg)
fonts=[
        ["DejaVu Sans Mono"]+["Noto Sans"]*11+["DejaVu Sans Mono"],
        ["Noto Sans"]*13,
        ["Noto Sans"]*13,
        ["Noto Sans"]*13,
        ["DejaVu Sans Mono"]+["Font Awesome 5 Brands"]+["Noto Sans"]*11
        ]
s=19.05
m65 = cq.Assembly()
x = 0
i = -1
j = -1
angles=[9,8.5,-6,-7,0]

for row,ll,ff in zip(leg,lay,fonts):
    x -= s
    i += 1
    y = 0
    for k,l,f in zip(row,ll,ff):
        print(k,l)
        y += l*s
        j += 1
        convex=False
        if k == '':
            convex=True
        m65.add(keycap(legend=k,angle=angles[i],font=f,convex=convex),name="k{}{}".format(i,j),loc=cq.Location(cq.Vector(y,x,0)))

cq.exporters.export(m65.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
