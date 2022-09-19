"""
==========================
  ██████  ██████  ██   ██
 ██    ██ ██   ██ ██  ██
 ██    ██ ██████  █████ 
 ██    ██ ██      ██  ██ 
  ██████  ██      ██   ██
==========================
 Open Programmatic Keycap
==========================

OPK is a spherical top keycap profile developed in CadQuery
(https://github.com/CadQuery/cadquery) and released under the very permissive
Apache License 2.0. It's especially suited for creating high/medium profile,
spherical top keycaps.

!!! The profile is still highly experimental and very alpha stage. ¡¡¡

If you use the code please give credit, if you do modifications consider 
releasing them back to the public under a permissive open source license.

Copyright (c) 2022 Matteo "Matt3o" Spinelli
https://matt3o.com
"""

import math
import cadquery as cq

def keycap(
    unitX: float = 1,           # keycap size in unit. Standard sizes: 1, 1.25, 1.5, ...
    unitY: float = 1,
    base: float = 18.2,         # 1-unit size in mm at the base
    top: float = 13.2,          # 1-unit size in mm at the top, actual hitting area will be slightly bigger
    curv: float = 1.7,          # Top side curvature. Higher value makes the top rounder (use small increments)
    bFillet: float = 0.5,       # Fillet at the base
    tFillet: float = 5,         # Fillet at the top
    height: float = 13,         # Height of the keycap before cutting the scoop (final height is lower)
    angle: float = 7,           # Angle of the top surface
    depth: float = 2.8,         # Scoop depth
    thickness: float = 1.5,     # Keycap sides thickness
    convex: bool = False,       # Is this a spacebar?
    legend: str = "",           # Legend
    legendDepth: float = -1.0,  # How deep to carve the legend, positive value makes the legend embossed
    font: str = "sans-serif",   # font name, use a font name including extension to use a local file
    fontsize: float = 10,       # the font size is in units
    pos: bool = False           # use POS style stabilizers
):

    top_diff = base - top

    curv = min(curv, 1.9)

    bx = 19.05 * unitX - (19.05 - base)
    by = 19.05 * unitY - (19.05 - base)

    tx = bx - top_diff
    ty = by - top_diff

    # if spacebar make the top less round-y
    tension = .4 if convex else 1

    if unitX < 2 and unitY < 2:
        pos = False

    # Three-section loft of rounded rectangles. Can't find a better way to do variable fillet
    base = (
        cq.Sketch()
        .rect(bx, by)
        .vertices()
        .fillet(bFillet)
    )

    mid = (
        cq.Sketch()
        .rect(bx, by)
        .vertices()
        .fillet((tFillet-bFillet)/3)
    )

    top = (
        cq.Sketch()
        .arc((curv, curv*tension), (0, ty/2), (curv, ty-curv*tension))
        .arc((curv, ty-curv*tension), (tx/2, ty), (tx-curv, ty-curv*tension))
        .arc((tx-curv, ty-curv*tension), (tx, ty/2), (tx-curv, curv*tension))
        .arc((tx-curv, curv*tension), (tx/2, 0), (curv, curv*tension))
        .assemble()
        .vertices()
        .fillet(tFillet)
        .moved(cq.Location(cq.Vector(-tx/2, -ty/2, 0)))
    )

    # Main shape
    keycap = (
        cq.Workplane("XY")
        .placeSketch(base,
                    mid.moved(cq.Location(cq.Vector(0, 0, height/4), cq.Vector(1,0,0), angle/4)),
                    top.moved(cq.Location(cq.Vector(0, 0, height), cq.Vector(1,0,0), angle))
                    )
        .loft()
    )

    # Create a body that will be carved from the main shape to create the top scoop
    if convex:
        scoop = (
            cq.Workplane("YZ").transformed(offset=cq.Vector(0, height-2.1, -bx/2), rotate=cq.Vector(0, 0, angle))
            .moveTo(-by/2, -1)
            .threePointArc((0, 2), (by/2, -1))
            .lineTo(by/2, 10)
            .lineTo(-by/2, 10)
            .close()
            .extrude(bx, combine=False)
        )
    else:
        scoop = (
            cq.Workplane("YZ").transformed(offset=cq.Vector(0, height, bx/2), rotate=cq.Vector(0, 0, angle))
            .moveTo(-by/2+2,0)
            .threePointArc((0, min(-0.1, -depth+1.5)), (by/2-2, 0))
            .lineTo(by/2, height)
            .lineTo(-by/2, height)
            .close()
            .workplane(offset=-bx/2)
            .moveTo(-by/2-2, -0.5)
            .threePointArc((0, -depth), (by/2+2, -0.5))
            .lineTo(by/2, height)
            .lineTo(-by/2, height)
            .close()
            .workplane(offset=-bx/2)
            .moveTo(-by/2+2, 0)
            .threePointArc((0, min(-0.1, -depth+1.5)), (by/2-2, 0))
            .lineTo(by/2, height)
            .lineTo(-by/2, height)
            .close()
            .loft(combine=False)
        )

    #show_object(tool, options={'alpha': 0.4})
    keycap = keycap - scoop
    
    # Top edge fillet
    keycap = keycap.edges(">Z").fillet(0.6)

    # Since the shell() function is not able to deal with complex shapes
    # we need to subtract a smaller keycap from the main shape
    shell = (
        cq.Workplane("XY").rect(bx-thickness*2, by-thickness*2)
        .workplane(offset=height/4).rect(bx-thickness*3, by-thickness*3)
        .workplane().transformed(offset=cq.Vector(0, 0, height-height/4-4.5), rotate=cq.Vector(angle, 0, 0)).rect(tx-thickness*2+.5, ty-thickness*2+.5)
        .loft()
    )
    keycap = keycap - shell

    # create a temporary surface that will be used to project the stems to
    # this is needed because extrude(face) needs the entire extruded outline to be contained inside the destination face
    tmpface = shell.faces('>Z').workplane().rect(bx*2, by*2).val()
    tmpface = cq.Face.makeFromWires(tmpface)

    # Build the stem and the keycap guts

    if pos:     # POS-like stems
        stem_pts = []
        ribh_pts = []
        ribv_pts = []

        stem_num_x = math.floor(unitX)
        stem_num_y = math.floor(unitY)
        stem_start_x = round(-19.05 * (stem_num_x / 2) + 19.05 / 2, 6)
        stem_start_y = round(-19.05 * (stem_num_y / 2) + 19.05 / 2, 6)

        for i in range(0, stem_num_y):
            ribh_pts.extend([(0, stem_start_y+i*19.05)])
            for l in range(0, stem_num_x):
                if i == 0:
                    ribv_pts.extend([(stem_start_x+l*19.05, 0)])
                stem_pts.extend([(stem_start_x+l*19.05, stem_start_y+i*19.05)])

    else:       # standard stems
        stem_pts = [(0,0)]

        if ( unitY > unitX ):
            if unitY > 2.75:
                dist = unitY / 2 * 19.05 - 19.05 / 2
                stem_pts.extend([(0, dist), (0, -dist)])
            elif unitY > 1.75:
                dist = 2.25 / 2 * 19.05 - 19.05 / 2
                stem_pts.extend([(0, -dist), (0, dist)])
            
            ribh_pts = stem_pts
            ribv_pts = [(0,0)]
        else:
            if unitX > 2.75:
                dist = unitX / 2 * 19.05 - 19.05 / 2
                stem_pts.extend([(dist, 0), (-dist,0)])
            elif unitX > 1.75:      # keycaps smaller than 3unit all have 2.25 stabilizers
                dist = 2.25 / 2 * 19.05 - 19.05 / 2
                stem_pts.extend([(dist, 0), (-dist,0)])
            
            ribh_pts = [(0,0)]
            ribv_pts = stem_pts

    # this is the stem +
    stem2 = (
        cq.Sketch()
        .push(stem_pts)
        .rect(4.15, 1.27)
        .rect(1.12, 4.15)
        .clean()
    )

    keycap = (
        keycap.faces("<Z").transformed(offset=cq.Vector(0, 0, 4.5)).workplane()
        .pushPoints(stem_pts)
        .circle(2.75)
        .extrude(tmpface)
        .pushPoints(ribh_pts)
        .rect(tx, 0.8)
        .extrude(tmpface)
        .pushPoints(ribv_pts)
        .rect(0.8, ty)
        .extrude(tmpface)
        .faces("<Z").workplane(offset=-0.6)
        .pushPoints(stem_pts)
        .circle(2.75)
        .extrude("next")
        .faces("<Z")
        .placeSketch(stem2)
        .extrude(-4.6, combine="cut")
        .faces(">Z[1]").edges("|X or |Y")
        .chamfer(0.2)
    )

    # Add the legend if present
    if legend and legendDepth != 0:
        fontPath = ''
        if font.endswith((".otf", ".ttf", ".ttc")):
            fontPath = font
            font = ''

        if legend.endswith('.dxf'):
            legend = (
                cq.importers
                .importDXF(legend)
                .wires().toPending()
                .extrude(-4)
                .translate((0,0,height+1))
                .rotateAboutCenter((1,0,0), angle)
            )
            # center the legend
            bb = legend.val().BoundingBox()
            legend = legend.translate((-bb.center.x, -bb.center.y, 0))
        else:
            legend = (
                cq.Workplane("XY").transformed(offset=cq.Vector(0, 0, height+1), rotate=cq.Vector(angle, 0, 0))
                .text(legend, fontsize, -4, font=font, fontPath=fontPath, halign="center", valign="center")
            )
            bb = legend.val().BoundingBox()
            # only center horizontally to keep the baseline
            legend = legend.translate((-bb.center.x, 0, 0))
        
        if legendDepth < 0:
            legend = legend - keycap
            legend = legend.translate((0,0,legendDepth))
            keycap = keycap - legend
            legend = legend - scoop      # this can be used to export the legend for 2 colors 3D printing
        else:
            scoop = scoop.translate((0,0,legendDepth))
            legend = legend - scoop
            legend = legend - keycap    # use this for multi-color 3D printing
            keycap = keycap + legend

        #show_object(legend, name="legend", options={'color': 'blue', 'alpha': 0})

    return keycap
