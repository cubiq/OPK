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

import cadquery as cq
from cadquery import exporters

# Prevent error when running from cli
if 'show_object' not in globals():
    def show_object(*args, **kwargs):
        pass

def keycap(
    unitX: float = 1,           # keycap size in unit. Standard sizes: 1, 1.25, 1.5, ...
    unitY: float = 1,
    base: float = 18.2,         # 1-unit size in mm at the base
    top: float = 14.2,          # 1-unit size in mm at the top, actual hitting area will be slightly bigger
    curv: float = 1.3,          # Top side curvature. Higher value makes the top rounder (use small increments)
    bFillet: float = 0.5,       # Fillet at the base
    tFillet: float = 4,         # Fillet at the top
    height: float = 13,         # Height of the keycap before cutting the scoop (final height is lower)
    angle: float = 7,           # Angle of the top surface
    depth: float = 2.5,         # Scoop depth
    thickness: float = 1.5,     # Keycap sides thickness
    convex: bool = False,       # Is this a spacebar?
    legend: str = "",           # Legend
    font: str = "sans serif",
    fontsize: float = 10,
    sep: float = 19.05          # separation between keys
):
    top_diff = base - top

    curv = min(curv, 1.9)

    bx = sep * unitX - (sep - base)
    by = sep * unitY - (sep - base)

    tx = bx - top_diff
    ty = by - top_diff

    # if spacebar make the top less round-y
    tension = .4 if convex else 1

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
                    mid.moved(cq.Location(cq.Vector(0, 0, height/4), (1,0,0), angle/4)),
                    top.moved(cq.Location(cq.Vector(0, 0, height), (1,0,0), angle))
                    )
        .loft()
    )

    # Create a body that will be carved from the main shape to create the shape
    if convex:
        tool = (
            cq.Workplane("YZ").transformed(offset=cq.Vector(0, height-2.1, -bx/2), rotate=cq.Vector(0, 0, angle))
            .moveTo(-by/2, -1)
            .threePointArc((0, 2), (by/2, -1))
            .lineTo(by/2, 10)
            .lineTo(-by/2, 10)
            .close()
            .extrude(bx, combine=False)
        )
    else:
        tool = (
            cq.Workplane("YZ").transformed(offset=cq.Vector(0, height+1, bx/2), rotate=cq.Vector(0, 0, angle))
            .moveTo(-by/2+2,0)
            .threePointArc((0, min(-0.1, -depth+1)), (by/2-2, 0))
            .lineTo(by/2-2, 10)
            .lineTo(-by/2+2, 10)
            .close()
            .workplane(offset=-bx/2)
            .moveTo(-by/2, -1)
            .threePointArc((0, -depth), (by/2, -1))
            .lineTo(by/2, 10)
            .lineTo(-by/2, 10)
            .close()
            .workplane(offset=-bx/2)
            .moveTo(-by/2+2, 0)
            .threePointArc((0, min(-0.1, -depth+1)), (by/2-2, 0))
            .lineTo(by/2-2, 10)
            .lineTo(-by/2+2, 10)
            .close()
            .loft(combine=False)
        )

    #show_object(tool, options={'alpha': 0.4})
    keycap = keycap - tool

    # Top edge fillet
    keycap = keycap.edges(">Z").fillet(0.5)

    # Since the shell() function is not able to deal with complex shapes
    # we need to subtract a smaller keycap from the main shape
    shell = (
        cq.Workplane("XY").rect(bx-thickness*2, by-thickness*2)
        .workplane(offset=height/5).rect(bx-thickness*2.3, by-thickness*2.3)
        .workplane().transformed(offset=cq.Vector(0, 0, height-height/5-4), rotate=cq.Vector(angle, 0, 0)).rect(tx-thickness*2, ty-thickness*2)
        .loft()
    )
    keycap = keycap - shell

    # Build the stem and the keycap guts
    if unitX < 2:
        stem_pts = [(0,0)]
    elif unitX < 3:
        dist = 2.25 / 2 * sep - sep / 2
        stem_pts = [(0,0), (dist, 0), (-dist,0)]
    else:
        dist = unitX / 2 * sep - sep / 2
        stem_pts = [(0,0), (dist, 0), (-dist,0)]

    stem1 = (
        cq.Sketch()
        .rect(tx, 0.8)
        .push(stem_pts)
        .rect(0.8, ty)
        .circle(2.75)
        .clean()
    )

    stem2 = (
        cq.Sketch()
        .push(stem_pts)
        .rect(4.1, 1.25)
        .rect(1.1, 4.1)
        .clean()
    )

    keycap = (
        keycap.faces("<Z").transformed(offset=cq.Vector(0, 0, 4.5))
        .placeSketch(stem1)
        .extrude("next")
        .faces("<Z").workplane(offset=-0.6)
        .pushPoints(stem_pts)
        .circle(2.75)
        .extrude("next")
        .faces("<Z")
        .placeSketch(stem2)
        .cutBlind(-4.6)
        .faces(">Z[1]").edges("|X or |Y")
        .chamfer(0.2)
    )

    # Add the legend if present
    if legend:
        legend = (
            cq.Workplane("XY").transformed(offset=cq.Vector(0, 0, height+1), rotate=cq.Vector(angle, 0, 0))
            .text(legend, fontsize, -4, font=font, halign="center")
        )
        bb = legend.val().BoundingBox()
        # try to center the legend horizontally
        legend = legend.translate((-bb.center.x, 0, 0))

        legend = legend - keycap
        legend = legend.translate((0,0,-1))
        keycap = keycap - legend
        legend = legend - tool      # this can be used to export the legend for 2 colors 3D printing

        #show_object(legend, name="legend", options={'color': 'blue', 'alpha': 0})

    """
    # Example to cut a DXF logo out of the keycap
    logo = (
        cq.importers
        .importDXF('logo.dxf')
        .wires().toPending()
        .extrude(-2)
        .translate((-5,-4.6,height)) # needs centering
        .rotateAboucurventer((1,0,0), angle)
    )
    keycap = keycap - logo
    """

    return keycap
