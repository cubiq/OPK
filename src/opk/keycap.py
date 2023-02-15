from defaults import *
import math
import cadquery as cq

class KeyCap:
    """KeyCap object defines the shape and generator"""

    # Default initializer generates the default key cap with no legend
    def __init__(self,
                 unit=1,  # keycap size in unit. Standard sizes: 1 1.25 1.5 ...
                 unit_y=1,
                 base=BASE_U1_MM,  # 1-unit size in mm at the base
                 top=TOP_U1_MM,  # 1-unit size in mm at the top actual hitting area will be slightly bigger
                 curve=TOP_CURVE,  # Top side curvature. Higher value makes the top round use small increments
                 b_fillet=BASE_FILLET,  # Fillet at the base
                 t_fillet=TOP_FILLET,  # Fillet at the top
                 height=HEIGHT,  # Height of the keycap before cutting the scoop (final height is lower)
                 angle=TOP_ANGLE,  # Angle of the top surface
                 scoop_depth=SCOOP_DEPTH,  # Scoop depth
                 wall_thickness=THICKNESS,  # Keycap sides thickness
                 is_spacebar=False,  # Is this a spacebar?
                 legend='',  # Legend
                 legend_depth=LEGEND_DEPTH,  # How deep to carve the legend positive value makes the legend embossed
                 legend_font=FONT,  # font name use a font name including extension to use a local file
                 legend_font_size=FONT_SIZE,  # the font size is in units
                 is_pos=False  # use POS style stabilizers
                 ):
        self.unitX: float = unit
        self.unitY: float = unit_y
        self.base: float = base
        self.top: float = top
        self.curv: float = curve
        self.bFillet: float = b_fillet
        self.tFillet: float = t_fillet
        self.height: float = height
        self.angle: float = angle
        self.depth: float = scoop_depth
        self.thickness: float = wall_thickness
        self.convex: bool = is_spacebar
        self.legend: str = legend
        self.legendDepth: float = legend_depth
        self.font: str = legend_font
        self.fontsize: float = legend_font_size
        self.pos: bool = is_pos
        self.shape = None
        self.name = f'SPACEBAR_U{self.unitX}' if is_spacebar else f'{self.legend}_U{self.unitX}'

    def __str__(self):
        key_type = ''
        if self.legend:
            key_type = f' {self.legend}'
        elif self.convex:
            key_type = ' SPACEBAR'
        return f'U{self.unitX}{key_type}'

    def override_name(self, name):
        self.name = name

    def generate_shape(self):
        top_diff = self.base - self.top

        curv = min(self.curv, 1.9)

        bx = U1_MM * self.unitX - (U1_MM - self.base)
        by = U1_MM * self.unitY - (U1_MM - self.base)

        tx = bx - top_diff
        ty = by - top_diff

        # if spacebar make the top less round-y
        tension = .4 if self.convex else 1

        if self.unitX < 2 and self.unitY < 2:
            pos = False

        # Three-section loft of rounded rectangles. Can't find a better way to do variable fillet
        base = (
            cq.Sketch()
                .rect(bx, by)
                .vertices()
                .fillet(self.bFillet)
        )

        mid = (
            cq.Sketch()
                .rect(bx, by)
                .vertices()
                .fillet((self.tFillet - self.bFillet) / 3)
        )

        top = (
            cq.Sketch()
                .arc((curv, curv * tension), (0, ty / 2), (curv, ty - curv * tension))
                .arc((curv, ty - curv * tension), (tx / 2, ty), (tx - curv, ty - curv * tension))
                .arc((tx - curv, ty - curv * tension), (tx, ty / 2), (tx - curv, curv * tension))
                .arc((tx - curv, curv * tension), (tx / 2, 0), (curv, curv * tension))
                .assemble()
                .vertices()
                .fillet(self.tFillet)
                .moved(cq.Location(cq.Vector(-tx / 2, -ty / 2, 0)))
        )

        # Main shape
        keycap = (
            cq.Workplane('XY')
                .placeSketch(base,
                             mid.moved(
                                 cq.Location(cq.Vector(0, 0, self.height / 4), cq.Vector(1, 0, 0), self.angle / 4)),
                             top.moved(cq.Location(cq.Vector(0, 0, self.height), cq.Vector(1, 0, 0), self.angle))
                             )
                .loft()
        )

        # Create a body that will be carved from the main shape to create the top scoop
        if self.convex:
            scoop = (
                cq.Workplane('YZ').transformed(offset=cq.Vector(0, self.height - 2.1, -bx / 2),
                                               rotate=cq.Vector(0, 0, self.angle))
                    .moveTo(-by / 2, -1)
                    .threePointArc((0, 2), (by / 2, -1))
                    .lineTo(by / 2, 10)
                    .lineTo(-by / 2, 10)
                    .close()
                    .extrude(bx, combine=False)
            )
        else:
            scoop = (
                cq.Workplane('YZ')
                    .transformed(offset=cq.Vector(0, self.height, bx / 2), rotate=cq.Vector(0, 0, self.angle))
                    .moveTo(-by / 2 + 2, 0)
                    .threePointArc((0, min(-0.1, -self.depth + 1.5)), (by / 2 - 2, 0))
                    .lineTo(by / 2, self.height)
                    .lineTo(-by / 2, self.height)
                    .close()
                    .workplane(offset=-bx / 2)
                    .moveTo(-by / 2 - 2, -0.5)
                    .threePointArc((0, -self.depth), (by / 2 + 2, -0.5))
                    .lineTo(by / 2, self.height)
                    .lineTo(-by / 2, self.height)
                    .close()
                    .workplane(offset=-bx / 2)
                    .moveTo(-by / 2 + 2, 0)
                    .threePointArc((0, min(-0.1, -self.depth + 1.5)), (by / 2 - 2, 0))
                    .lineTo(by / 2, self.height)
                    .lineTo(-by / 2, self.height)
                    .close()
                    .loft(combine=False)
            )

        # show_object(tool, options={'alpha': 0.4})
        keycap = keycap - scoop

        # Top edge fillet
        keycap = keycap.edges('>Z').fillet(0.6)

        # Since the shell() function is not able to deal with complex shapes
        # we need to subtract a smaller keycap from the main shape
        shell = (
            cq.Workplane('XY').rect(bx - self.thickness * 2, by - self.thickness * 2)
                .workplane(offset=self.height / 4).rect(bx - self.thickness * 3, by - self.thickness * 3)
                .workplane().transformed(offset=cq.Vector(0, 0, self.height - self.height / 4 - 4.5),
                                         rotate=cq.Vector(self.angle, 0, 0)).rect(tx - self.thickness * 2 + .5,
                                                                                  ty - self.thickness * 2 + .5)
                .loft()
        )
        keycap = keycap - shell

        # create a temporary surface that will be used to project the stems to
        # this is needed because extrude(face) needs the entire extruded outline to be contained inside the destination face
        tmpface = shell.faces('>Z').workplane().rect(bx * 2, by * 2).val()
        tmpface = cq.Face.makeFromWires(tmpface)

        # Build the stem and the keycap guts

        if self.pos:  # POS-like stems
            stem_pts = []
            ribh_pts = []
            ribv_pts = []

            stem_num_x = math.floor(self.unitX)
            stem_num_y = math.floor(self.unitY)
            stem_start_x = round(-U1_MM * (stem_num_x / 2) + U1_MM / 2, 6)
            stem_start_y = round(-U1_MM * (stem_num_y / 2) + U1_MM / 2, 6)

            for i in range(stem_num_y):
                ribh_pts.extend([(0, stem_start_y + i * U1_MM)])
                for l in range(stem_num_x):
                    if i == 0:
                        ribv_pts.extend([(stem_start_x + l * U1_MM, 0)])
                    stem_pts.extend([(stem_start_x + l * U1_MM, stem_start_y + i * U1_MM)])

        else:  # standard stems
            stem_pts = [(0, 0)]

            if (self.unitY > self.unitX):
                if self.unitY > 2.75:
                    dist = self.unitY / 2 * U1_MM - U1_MM / 2
                    stem_pts.extend([(0, dist), (0, -dist)])
                elif self.unitY > 1.75:
                    dist = 2.25 / 2 * U1_MM - U1_MM / 2
                    stem_pts.extend([(0, -dist), (0, dist)])

                ribh_pts = stem_pts
                ribv_pts = [(0, 0)]
            else:
                if self.unitX > 2.75:
                    dist = self.unitX / 2 * U1_MM - U1_MM / 2
                    stem_pts.extend([(dist, 0), (-dist, 0)])
                elif self.unitX > 1.75:  # keycaps smaller than 3unit all have 2.25 stabilizers
                    dist = 2.25 / 2 * U1_MM - U1_MM / 2
                    stem_pts.extend([(dist, 0), (-dist, 0)])

                ribh_pts = [(0, 0)]
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
            keycap.faces('<Z').transformed(offset=cq.Vector(0, 0, 4.5)).workplane()
                .pushPoints(stem_pts)
                .circle(2.75)
                .extrude(tmpface)
                .pushPoints(ribh_pts)
                .rect(tx, 0.8)
                .extrude(tmpface)
                .pushPoints(ribv_pts)
                .rect(0.8, ty)
                .extrude(tmpface)
                .faces('<Z').workplane(offset=-0.6)
                .pushPoints(stem_pts)
                .circle(2.75)
                .extrude('next')
                .faces('<Z')
                .placeSketch(stem2)
                .extrude(-4.6, combine='cut')
                .faces('>Z[1]').edges('|X or |Y')
                .chamfer(0.2)
        )

        # Add the legend if present
        if self.legend and self.legendDepth != 0:
            fontPath = ''
            if self.font.endswith(('.otf', '.ttf', '.ttc')):
                fontPath = self.font
                font = ''

            if self.legend.endswith('.dxf'):
                legend = (
                    cq.importers
                        .importDXF(self.legend)
                        .wires().toPending()
                        .extrude(-4)
                        .translate((0, 0, self.height + 1))
                        .rotateAboutCenter((1, 0, 0), self.angle)
                )
                # center the legend
                bb = legend.val().BoundingBox()
                legend = legend.translate((-bb.center.x, -bb.center.y, 0))
            else:
                legend = (
                    cq.Workplane('XY').transformed(offset=cq.Vector(0, 0, self.height + 1),
                                                   rotate=cq.Vector(self.angle, 0, 0))
                        .text(self.legend, self.fontsize, -4, font=self.font, fontPath=fontPath, halign='center',
                              valign='center')
                )
                bb = legend.val().BoundingBox()
                # only center horizontally to keep the baseline
                legend = legend.translate((-bb.center.x, 0, 0))

            if self.legendDepth < 0:
                legend = legend - keycap
                legend = legend.translate((0, 0, self.legendDepth))
                keycap = keycap - legend
                legend = legend - scoop  # this can be used to export the legend for 2 colors 3D printing
            else:
                scoop = scoop.translate((0, 0, self.legendDepth))
                legend = legend - scoop
                legend = legend - keycap  # use this for multi-color 3D printing
                keycap = keycap + legend

            # show_object(legend, name='legend', options={'color': 'blue', 'alpha': 0})
        self.shape = keycap
        return keycap
