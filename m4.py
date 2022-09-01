#!/usr/bin/env python3


import cadquery as cq
from opk import *

leg = [["⎋","1"],
["↹","q"],
["#","a"],
["⇧","\\"],
["","⇓"]]
lay= [[1]*2 , [1]*2,[1]*2,[1]*2,[1,1.25]]

i = -1
j = -1
angles=[9,8.5,-6,-7,0]

for row,ll in zip(leg,lay):
    i += 1
    for k,l in zip(row,ll):
        print(k,l)
        j += 1
        convex=False
        if k == '':
            convex=True
        key = keycap(legend=k,angle=angles[i],font="Noto Sans",convex=convex,unitX=l)
        name="k{}{}{}u".format(i,j,l)
        cq.exporters.export(key, name+".step")
        cq.exporters.export(key, name+".stl", tolerance=0.001, angularTolerance=0.05)
