#!/usr/bin/env python3

import cadquery as cq
from opk import *
leg = [ ["⎋","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12", "Prn\nScr","Scr\nLock","Pause"],
        ["¬\n`","!\n1","\"\n2","£\n3","$\n4","%\n5","^\n6","&\n7","*\n8","(\n9",")\n0","_\n-","=\n+","⌫","Ins","Home","Pg\nUp"],
["↹","q","w","e","r","t","y","u","i","o","p","[","]","|\n\\","Del","End","Pg\nDn"],
["⇪","a","s","d","f","g","h","j","k","l",";","'","enter"],
["⇧","z","x","c","v","b","n","m",",",".","/","⇧","↑"],
["⎈","","Alt","","Alt","Fn","Mnu","Ctrl","←","↓","→"]]
lay= [[1]*16,
      [1]*13+[2]+[1]*3,
      [1.5]+[1]*12+[1.5]+[1]*3,
      [1.75]+[1]*11+[2.25],
      [2.25]+[1]*10+[2.75]+[1],
      [1.25,1.25,1.25,6.25,1.25,1.25,1.25,1.25,1,1,1]]
fonts=[
        ["DejaVu Sans Mono"]*16,
        ["DejaVu Sans Mono"]*17,
        ["DejaVu Sans Mono"]*17,
        ["DejaVu Sans Mono"]*13,
        ["DejaVu Sans Mono"]*13,
        ["DejaVu Sans Mono"]+["Font Awesome 6 Brands"]+["Noto Sans"]*6+["DejaVu Sans Mono"]*3
        ]

offx=[[0,1,0,0,0]+[0.5,0,0,0]+[0.5,0,0,0]+[0.5,0,0],
      [0.0]*14+[0.5,0,0],
      [0.0]*14+[0.5,0,0],
      [0.0]*13,
      [0.0]*12+[1.5],
      [0.0]*8+[0.5,0,0]
      ]
offy=[[0.5]+[0]*15,
      [0]*17,
      [0]*17,
      [0]*13,
      [0]*13,
      [0]*11
      ]

sx=19.05
sy=19.05

m65 = cq.Assembly()

y = 0
i = -1
j = -1

angles=[13.5,9,8.5,-6,-7,0]
vfs=[0,9,7,6,4.5,4.5]

for row,ll,ff,ofx,ofy in zip(leg,lay,fonts,offx,offy):

    i += 1
    y = -(i+1)*sy

    x = 0
    for k,l,f,ox,oy in zip(row,ll,ff,ofx,ofy):
        print(k,len(k),l,f)
        w = l*sx/2.0
        j += 1
        x += w + ox*sx
        y += oy*sy
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
                       fontsize=fs,
                       unitX=l),
                name="k{}{}".format(i,j),
                loc=cq.Location(cq.Vector(x,y,0))
                )
        x += w

#cq.exporters.export(m65.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
show_object(m65, name="legend", options={'color': 'red', 'alpha': 0})
