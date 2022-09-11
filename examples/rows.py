#!/usr/bin/env python3


import cadquery as cq
from opk import *
import os

leg = [["⎋"],["⎋"],
["↹"],
["⇪","d","f","g"],
["⇧"],
["⎈"],
["",""]]
lay= [[1],[1],[1.5],[1.75]+[1]*3,[2.25],[1.25],[2,1]]
fonts=[
        ["/usr/share/fonts/truetype/NotoSansSymbols-Medium.ttf"],
        ["/usr/share/fonts/truetype/NotoSansSymbols-Medium.ttf"],
        ["Noto Sans Mono"],
        ["Noto Sans Mono"]*4,
        ["Noto Sans Mono"],
        ["/usr/share/fonts/truetype/NotoSansSymbols-Medium.ttf"],
        ["Noto Sans Mono"]+["/usr/share/fonts/texlive-fontawesome5/FontAwesome5Brands-Regular-400.otf"]
        ]
sx = 19.05
sy = 19.05
rows = cq.Assembly()
y = 0
i = -1
j = -1
angles = [13.5,9,8.5,-6,-7,0,0]
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
        convex = False
        if k in ["",""]:
            convex = True
        scoop = 2.5
        if k in ['f','F','j','J']:
            scoop = 2.5*1.2
        fs=3
        if len(k)<=5:
            fs=vfs[len(k)]
        if (len(k.split("\n"))==2):
            fs = 4.5

        rows.add(keycap(legend=k,
                        angle=angles[i],
                        font=f,
                        convex=convex,
                        depth = scoop,
                        unitX=l),
                 name="k{}{}".format(i,j),
                 loc=cq.Location(cq.Vector(x,y,0)))
        x += w
cq.exporters.export(rows.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
#show_object(rows, name="rows", options={"alpha": 0})
