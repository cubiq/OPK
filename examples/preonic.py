#!/usr/bin/env python3

import cadquery as cq
from opk import *

leg = [
    ["⎋","!\n1","\"\n2","£\n3","$\n4","%\n5","^\n6","&\n7","*\n8","(\n9",")\n0","⌫"],
    ["q", "w", "e","r","t","y","u","i","o","p","{\n[","}\n]"],
    ["↹","a","s","d","f","g","h","j","k","l",":\n;","@\n'"],
    ["⇧","z","x","c","v","b","n","m","<\n,",">\n.","?\n/","⌅"],
    ["⎈","⎇","","⎇","⇓","","⇑","←","↓","↑","→"]]
lay= [[1]*12, [1]*12,[1]*12,[1]*12,[1]*5+[2]+[1]*5]
fonts=[
        ["DejaVu Sans Mono"]*12,
        ["DejaVu Sans Mono"]*12,
        ["DejaVu Sans Mono"]*12,
        ["DejaVu Sans Mono"]*12,
        ["DejaVu Sans Mono"]*11
        ]
sx=19.05
sy=19.05
pre = cq.Assembly()
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
        pre.add(keycap(legend=k,
                       angle=angles[i],
                       font=f,
                       depth = scoop,
                       convex=convex,
                       fontsize =fs,
                       unitX=l),
                name="k{}{}".format(i,j),
                loc=cq.Location(cq.Vector(x,y,0)))
        x += w
#cq.exporters.export(pre.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
show_object(pre, name="pre", options={"alpha": 0})
