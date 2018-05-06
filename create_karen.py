#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import fontforge as ff
import psMat

SRC = "src"
OUT = "out"

KAREN_VERSION = 0.1
KAREN_VERSION_STR = str(KAREN_VERSION)
KAREN_WEIGHT = "Regular"
KAREN_FAMILYNAME = "Karen"
KAREN_FAMILYNAME_JA = "可憐"
KAREN_FONTNAME = KAREN_FAMILYNAME + "-" + KAREN_WEIGHT
KAREN_FONTNAME_JA = KAREN_FAMILYNAME_JA + "-" + KAREN_WEIGHT

GGM_FILE = "GenShinGothic-Monospace-Regular.ttf"
UM_FILE = "UbuntuMono-R.ttf"
HK_FILE = "Hack-Regular.ttf"
NE_FILE = "NotoEmoji-Regular.ttf"
KAREN_FILE = KAREN_FONTNAME + ".ttf"

SRC_GGM_FILE = path.join(SRC, GGM_FILE)
SRC_UM_FILE = path.join(SRC, UM_FILE)
SRC_HK_FILE = path.join(SRC, HK_FILE)
SRC_NE_FILE = path.join(SRC, NE_FILE)
OUT_KAREN_FILE = path.join(OUT, KAREN_FILE)

ggm = ff.open(SRC_GGM_FILE)
um = ff.open(SRC_UM_FILE)
hk = ff.open(SRC_HK_FILE)
ne = ff.open(SRC_NE_FILE)

EM = 1024
ASCENT = round(um.ascent * (EM / um.em))
DESCENT = round(um.descent * (EM / um.em))
TYPO_ASCENT = round(ASCENT * 0.9)
TYPO_DESCENT = -round(DESCENT * 0.75)
FULL_WIDTH = 1024
HALF_WIDTH = FULL_WIDTH / 2
HK_SCALE = 0.83
NE_SCALE = 0.79
HK_SCALE_MAT = psMat.scale(HK_SCALE)
NE_SCALE_MAT = psMat.scale(NE_SCALE)


# Merge Ubuntu Mono
um.em = EM
for glyph in um.glyphs():
    if glyph.isWorthOutputting() and 0 < glyph.unicode and glyph.unicode <= 0x2265:
        um.selection.select(glyph.encoding)
        um.copy()
        ggm.selection.select(glyph.unicode)
        ggm.paste()

# Merge Hack
hk.em = EM
for glyph in hk.glyphs():
    if glyph.isWorthOutputting() and 0xa1 <= glyph.unicode and \
            len(list(ggm.selection.select(glyph.unicode).byGlyphs)) > 0 and \
            list(ggm.selection.byGlyphs)[0].width == FULL_WIDTH:
        glyph.transform(HK_SCALE_MAT)
        glyph.width = HALF_WIDTH
        hk.selection.select(glyph.unicode)
        hk.copy()
        ggm.selection.select(glyph.unicode)
        ggm.paste()

# Merge Noto Emoji
ne.em = EM
for glyph in ne.glyphs():
    if glyph.isWorthOutputting() and 0x20e0 <= glyph.unicode:
        glyph.transform(NE_SCALE_MAT)
        glyph.width = FULL_WIDTH
        ne.selection.select(glyph.encoding)
        ne.copy()
        ggm.selection.select(glyph.unicode)
        ggm.paste()


# Customize several glyphs
## No-break space
ggm.selection.select(0xa0)
list(ggm.selection.byGlyphs)[0].width = HALF_WIDTH

## Half-width space
ggm.selection.select(0x20)
list(ggm.selection.byGlyphs)[0].width = HALF_WIDTH

## |
um.selection.select(0xa6); um.copy()
ggm.selection.select(0x7c); ggm.paste()


# Set font info
ggm.ascent = ASCENT
ggm.descent = DESCENT
ggm.os2_winascent = ASCENT
ggm.os2_windescent = DESCENT
ggm.os2_typoascent = TYPO_ASCENT
ggm.os2_typodescent = TYPO_DESCENT
ggm.os2_typolinegap = 0
ggm.hhea_ascent = ASCENT
ggm.hhea_descent = -DESCENT
ggm.hhea_linegap = 0
ggm.vhea_linegap = 0
ggm.upos = 45

## Copyright
def generate_copyright(font):
    s = "\n\n"
    s += "* " + font.fontname
    s += "\n"
    s += font.copyright
    return s
karen_copyright = "Karen is based on the following products:"
karen_copyright += generate_copyright(ggm)
karen_copyright += generate_copyright(um)
karen_copyright += generate_copyright(hk)
karen_copyright += generate_copyright(ne)
ggm.copyright = karen_copyright
ggm.sfnt_names = \
    tuple((row[0], row[1], karen_copyright if row[1] == "Copyright" else row[2]) \
        for row in ggm.sfnt_names)

ggm.fontname = KAREN_FONTNAME
ggm.familyname = KAREN_FAMILYNAME
ggm.fullname = KAREN_FONTNAME
ggm.weight = KAREN_WEIGHT
ggm.os2_vendor = ""
ggm.sfntRevision = KAREN_VERSION
ggm.appendSFNTName("English (US)", "Trademark", "")
ggm.appendSFNTName("English (US)", "Designer", "")
ggm.appendSFNTName("English (US)", "Descriptor", "")
ggm.appendSFNTName("English (US)", "License", "")
ggm.appendSFNTName("English (US)", "License URL", "")
ggm.appendSFNTName("English (US)", "Vendor URL", "")
ggm.appendSFNTName("English (US)", "Copyright", karen_copyright)
ggm.appendSFNTName("English (US)", "Version", KAREN_VERSION_STR)
ggm.appendSFNTName("English (US)", "UniqueID", KAREN_FONTNAME + " " + KAREN_VERSION_STR)
ggm.appendSFNTName("English (US)", "Preferred Family", KAREN_FAMILYNAME)
ggm.appendSFNTName("English (US)", "Preferred Styles", KAREN_WEIGHT)
ggm.appendSFNTName("Japanese", "Family", KAREN_FAMILYNAME_JA)
ggm.appendSFNTName("Japanese", "Fullname", KAREN_FONTNAME_JA)
ggm.appendSFNTName("Japanese", "Preferred Family", KAREN_FAMILYNAME_JA)
ggm.appendSFNTName("Japanese", "Preferred Styles", KAREN_WEIGHT)

# Generate Karen
ggm.generate(OUT_KAREN_FILE)
