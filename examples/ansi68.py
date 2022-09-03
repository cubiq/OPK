#!/usr/bin/env python3

import cadquery as cq
from opk import *
leg = [["⎋","!\n1","\"\n2","£\n3","$\n4","%\n5","^\n6","&\n7","*\n8","(\n9",")\n0","_\n-","=\n+","⌫","¬\n`"],
["↹","q","w","e","r","t","y","u","i","o","p","[","]","|\n\\","⌦"],
["⇪","a","s","d","f","g","h","j","k","l",":\n;","@\n'","enter","Pg\nUp"],
["⇧","z","x","c","v","b","n","m","<\n,",">\n.","?\n/","⇧","↑","Pg\nDn"],
["⎈","","⎇","","⎇","Fn","⎈","←","↓","→"]]
lay= [[1]*13+[2,1],
      [1.5]+[1]*12+[1.5]+[1],
      [1.75]+[1]*11+[2.25]+[1],
      [2.25]+[1]*10+[1.75]+[1,1],
      [1.25,1.25,1.25,6.25,1,1,1,1,1,1]]
fonts=[
        ["DejaVu Sans Mono"]*15,
        ["DejaVu Sans Mono"]*15,
        ["DejaVu Sans Mono"]*14,
        ["DejaVu Sans Mono"]*14,
        ["DejaVu Sans Mono"]+["Font Awesome 6 Brands"]+["DejaVu Sans Mono"]*8
        ]
sx=19.05
sy=19.05
m65 = cq.Assembly()
y = 0
i = -1
j = -1
angles=[9,8.5,-6,-7,0]
vfs=[0,9,7,6,4.5,4.5]

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
            scoop = 2.5*1.2
        fs=3
        if len(k)<=5:
            fs=vfs[len(k)]
        if (len(k.split("\n"))==2):
            fs = 4.5
        m65.add(keycap(legend=k,
                       angle=angles[i],
                       font=f,
                       convex=convex,
                       depth = scoop,
                       fontsize = fs,
                       unitX=l),
                name="k{}{}".format(i,j),
                loc=cq.Location(cq.Vector(x,y,0))
                )
        x += w

#cq.exporters.export(m65.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
show_object(m65, name="legend", options={'color': 'red', 'alpha': 0})
