#!/usr/bin/env python3
import cadquery as cq
from opk import *

leg = [["⎋","1"],
["↹","q"],
["#","a"],
["⇧","\\"],
[""," "]]
lay= [[1]*2 , [1]*2,[1]*2,[1]*2,[1,1.25]]
fonts=[
        ["DejaVu Sans Mono"]+["Noto Sans"],
        ["Noto Sans"]*2,
        ["Noto Sans"]*2,
        ["Noto Sans"]*2,
        ["DejaVu Sans Mono"]+["Font Awesome 5 Brands Regular"]
        ]

i = -1
j = -1
angles=[9,8.5,-6,-7,0]

for row,ll,ff in zip(leg,lay,fonts):
    i += 1
    for k,l,f in zip(row,ll,ff):
        print(k,l)
        j += 1
        convex=False
        if k == '':
            convex=True
        key = keycap(legend=k,angle=angles[i],font=f,convex=convex,unitX=l)
        name="k{}{}{}u".format(i,j,l)
        cq.exporters.export(key, name+".step")
        cq.exporters.export(key, name+".stl", tolerance=0.001, angularTolerance=0.05)
