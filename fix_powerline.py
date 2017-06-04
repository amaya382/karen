from os import path
import fontforge as ff
import psMat

OUT = "out"
KAREN_FILE = "Karen-Regular.ttf"
OUT_KAREN_FILE = path.join(OUT, KAREN_FILE)

FULL_WIDTH = 1024
HALF_WIDTH = FULL_WIDTH / 2
SHRINK_MAT = psMat.scale(0.5, 1.0)

karen = ff.open(OUT_KAREN_FILE)
karen.selection.select(("ranges", None), 0xe0a0, 0xe0a2)
for glyph in list(karen.selection.byGlyphs):
    glyph.transform(SHRINK_MAT)
    glyph.width = HALF_WIDTH
karen.selection.select(("ranges", None), 0xe0b0, 0xe0b3)
for glyph in list(karen.selection.byGlyphs):
    glyph.transform(SHRINK_MAT)
    glyph.width = HALF_WIDTH

karen.generate(OUT_KAREN_FILE)
