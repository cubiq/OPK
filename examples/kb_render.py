import cadquery as cq
from random import choice
import opk

def render_kb(rows, mainFont="DejaVu Sans Mono", mainSize = 9, sx = 19.05, sy = 19.05, depth = 2.8, export = False ):

    assy = cq.Assembly()
    colours=["tomato2","springgreen3","slateblue2","sienna1","seagreen3","orangered2","orchid2","maroon2","limegreen","lightseagreen","lightcoral","magenta3","yellow"]

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

            cdepth = depth
            if 'n' in k:
                if k['n']:
                    name+= "_homing"
                cdepth = depth + 0.8
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
                            convex=convex, depth=cdepth,
                            legend=legend, font=font,
                            fontsize=fontSize)
            # Export one key at the time
            if export:
                cq.exporters.export(cap, './export/STEP/' + name + '.step')
                cq.exporters.export(cap, './export/STL/' + name + '.stl', tolerance=0.001, angularTolerance=0.05)
            w = sx * kw / 2
            ox = 0.0
            if 'ox' in k:
                ox = k['ox']
            x += w + ox*sx
            oy = 0.0
            if 'oy' in k:
                oy = k['oy']
            y += oy*sy
            assy.add(cap, name=name, color=cq.Color(choice(colours)),
                    loc=cq.Location(cq.Vector(x,y,0)))
            x += w
        y = -(i+1)*sy
    return assy
