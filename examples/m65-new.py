import opk
import cadquery as cq
from cadquery import exporters
from random import choice

keys = {
    0: [
    { 'w': 1,'t':'⎋ `\n  ¬','fs':5},
    { 'w': 1,'t':'1\n!','fs':5 },
    { 'w': 1,'t':'2\n\"','fs':5 },
    { 'w': 1,'t':'3\n£','fs':5 },
    { 'w': 1,'t':'4\n$','fs':5 },
    { 'w': 1,'t':'5\n%','fs':5 },
    { 'w': 1,'t':'6\n^','fs':5 },
    { 'w': 1,'t':'7\n&','fs':5 },
    { 'w': 1,'t':'8\n*','fs':5 },
    { 'w': 1,'t':'9\n(','fs':5 },
    { 'w': 1,'t':'0\n)','fs':5 },
    { 'w': 1,'t':'-  ⌦\n_  ','fs':5 },
    { 'w': 1,'t':'⌫ =\n  +','fs':5 }
    ],
    1: [
    { 'w': 1,'t':'↹','fs':12},
    { 'w': 1,'t':'q' },
    { 'w': 1,'t':'w' },
    { 'w': 1,'t':'e' },
    { 'w': 1,'t':'r' },
    { 'w': 1,'t':'t' },
    { 'w': 1,'t':'y' },
    { 'w': 1,'t':'u' },
    { 'w': 1,'t':'i' },
    { 'w': 1,'t':'o' },
    { 'w': 1,'t':'p' },
    { 'w': 1,'t':'[\n{','fs':5 },
    { 'w': 1,'t':']\n}','fs':5 }
    ],
    2: [
    { 'w': 1,'t':'#\n~','fs':5 },
    { 'w': 1,'t':'a' },
    { 'w': 1,'t':'s' },
    { 'w': 1,'t':'d' },
    { 'w': 1,'t':'f','n': True },
    { 'w': 1,'t':'g' },
    { 'w': 1,'t':'h' },
    { 'w': 1,'t':'j','n': True },
    { 'w': 1,'t':'k' },
    { 'w': 1,'t':'l' },
    { 'w': 1,'t':';\n:','fs':5 },
    { 'w': 1,'t':'\'\n@','fs':5 },
    { 'w': 1,'t':'⊼','fs':12 },
    ],
    3: [
    { 'w': 1,'t':'⇧','fs':12 },
    { 'w': 1,'t':'\\\n|','fs':5 },
    { 'w': 1,'t':'z' },
    { 'w': 1,'t':'x' },
    { 'w': 1,'t':'c' },
    { 'w': 1,'t':'v' },
    { 'w': 1,'t':'b' },
    { 'w': 1,'t':'n' },
    { 'w': 1,'t':'m' },
    { 'w': 1,'t':',\n<','fs':5 },
    { 'w': 1,'t':'.\n>','fs':5 },
    { 'w': 1,'t':'↑','fs':12 },
    { 'w': 1,'t':'/\n?','fs':5 }
    ],
    4: [
    { 'w': 1,'t':'⎈','f':"DejaVu Sans Mono",'fs':12 },
    { 'w': 1,'t':'','f':"/usr/share/fonts/texlive-fontawesome5/FontAwesome5Brands-Regular-400.otf" },
    { 'w': 1,'t':'⇓','f':"DejaVu Sans Mono",'fs':12},
    { 'w': 1,'t':'⎇','f':"/usr/share/fonts/truetype/NotoSansSymbols-Black.ttf" },
    { 'w': 1,'t':'⇑','f':"DejaVu Sans Mono",'fs':12 },
    {'w':1,'convex':True},
    {'w':1,'t':'','convex':True,'f':"/usr/share/fonts/texlive-fontawesome5/FontAwesome5Brands-Regular-400.otf",'fs':9},
    {'w':1,'convex':True},
    { 'w': 1,'t':'⎇','f':"/usr/share/fonts/truetype/NotoSansSymbols-Black.ttf" },
    { 'w': 1,'t':'⇧','fs':12 },
    { 'w': 1,'t':'←','fs':12 },
    { 'w': 1,'t':'↓','fs':12 },
    { 'w': 1,'t':'→','fs':12 }

    ],
}
colours=["tomato2","springgreen3","slateblue2","sienna1","seagreen3","orangered2","orchid2","maroon2","limegreen","lightseagreen","lightcoral","magenta3","yellow"]

#rows = [
    #{'angle': 13, 'height': 16,   'keys': keys[0] },      # row 0, function row
    #{'angle': 9,  'height': 14,   'keys': keys[1] },      # row 1, numbers row
    #{'angle': 8,  'height': 12,   'keys': keys[2] },      # row 2, QWERT
    #{'angle': -6, 'height': 11.5, 'keys': keys[3] },      # row 3, ASDFG
    #{'angle': -8, 'height': 13,   'keys': keys[4] },      # row 4, ZXCVB
    #{'angle': 0,  'height': 12.5, 'keys': keys[5] },      # row 5, bottom row
#]
rows = [
    {'angle': 9,  'height': 14,   'keys': keys[0] },      # row 1, numbers row
    {'angle': 8,  'height': 12,   'keys': keys[1] },      # row 2, QWERT
    {'angle': -6, 'height': 11.5, 'keys': keys[2] },      # row 3, ASDFG
    {'angle': -8, 'height': 13,   'keys': keys[3] },      # row 4, ZXCVB
    {'angle': 0,  'height': 12.5, 'keys': keys[4] },      # row 5, bottom row
]

mainFont = "DejaVu Sans Mono"
mainSize = 9
assy = cq.Assembly()

y = 0
for i, r in enumerate(rows):
    x = 0
    for j,k in enumerate(r['keys']):
        name = "row{}_{}_U{}".format(i,j,k['w'])
        convex = False
        if 'convex' in k:
            convex = k['convex']
            name+= "_space"
        
        depth = 2.8
        if 'n' in k:
            if k['n']:
                name+= "_homing"
            depth = 3.6
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
        cap = opk.keycap(angle=r['angle'], height=r['height'], unitX=k['w'], 
                         convex=convex, depth=depth,
                         legend=legend, font=font,
                         fontsize=fontSize)
        # Export one key at the time
        #exporters.export(cap, './export/STEP/' + name + '.step')
        #exporters.export(cap, './export/STL/' + name + '.stl', tolerance=0.001, angularTolerance=0.05)
        w = 19.05 * k['w'] / 2
        x+= w
        assy.add(cap, name=name, color=cq.Color(choice(colours)),
                 loc=cq.Location(cq.Vector(x,y,0)))
        x+= w
    y -= 19.05

if 'show_object' in locals():
    show_object(assy)

# Export the whole assembly, very handy especially for STEP
#exporters.export(assy.toCompound(), 'keycaps.stl', tolerance=0.001, angularTolerance=0.05)
#exporters.export(assy.toCompound(), 'keycaps.step')
