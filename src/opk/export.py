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

from defaults import *
from keycap import KeyCap
import cadquery as cq
from enum import Enum
from typing import List


class ExportType(Enum):
    STEP = '.step'
    STL = '.stl'


def export_key_rows(rows: List[List[KeyCap]], export_type: ExportType, path='./', name='keycaps'):
    """Exports full rows. Expects a grid i.e. a list of lists of KeyCaps"""
    assy = cq.Assembly()
    y = 0
    for i, row in rows:
        x = 0
        for keycap in row:
            w = U1_MM * keycap.unitX / 2
            x += w
            assy.add(keycap.cad(), name=keycap.name, loc=cq.Location(cq.Vector(x, y, 0)))
            x += w
        y -= U1_MM
    if export_type == ExportType.STEP:
        cq.exporters.export(assy.toCombine(), path + name + export_type.value)
    elif export_type == ExportType.STL:
        cq.exporters.export(assy.toCombine(), path + name + export_type.value, tolerance=0.001, angularTolerance=0.05)
    else:
        raise ValueError(f'Invalid export type')


def export_individual_keys(key_caps: List[KeyCap], export_type: ExportType, path='./', prefix='', suffix=''):
    """Takes a list of KeyCaps and exports each into individual files"""
    for key_cap in key_caps:
        filepath = path + prefix + key_cap.name + suffix + export_type.value
        if export_type == ExportType.STEP:
            cq.exporters.export(key_cap.cad(), filepath)
        elif export_type == ExportType.STL:
            cq.exporters.export(key_cap.cad(), filepath, tolerance=0.001, angularTolerance=0.05)
    else:
        raise ValueError(f'Invalid export type')
