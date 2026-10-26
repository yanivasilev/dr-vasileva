import sys, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

f = TTFont(sys.argv[1])
if 'fvar' in f:
    from fontTools.varLib.instancer import instantiateVariableFont
    f = instantiateVariableFont(f, {"wght": 600})
gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
hmtx = f['hmtx']

def outline(text, tracking_em):
    pen = SVGPathPen(gs); bp = BoundsPen(gs)
    x = 0; track = tracking_em * upm
    for i, ch in enumerate(text):
        if ch == ' ':
            x += hmtx['space'][0] + track; continue
        g = cmap[ord(ch)]
        t = (1, 0, 0, -1, x, 0)           # flip y for SVG
        gs[g].draw(TransformPen(pen, t)); gs[g].draw(TransformPen(bp, t))
        x += hmtx[g][0] + (track if i < len(text) - 1 else 0)
    return pen.getCommands(), bp.bounds

out = {}
for key, text, tr in [("logo", "DR VASILEVA", .34), ("mono", "DV", .04)]:
    d, (x0, y0, x1, y1) = outline(text, tr)
    out[key] = {"d": d, "box": [round(x0), round(y0), round(x1 - x0), round(y1 - y0)]}
json.dump(out, open("glyphs.json", "w"))
print({k: v["box"] for k, v in out.items()}, len(out["logo"]["d"]))
