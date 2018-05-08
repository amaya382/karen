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

GG_FILE = "GenEiGothicM-Regular.ttf"
UM_FILE = "UbuntuMono-R.ttf"
HK_FILE = "Hack-Regular.ttf"
NE_FILE = "NotoEmoji-Regular.ttf"
KAREN_FILE = KAREN_FONTNAME + ".ttf"

SRC_GG_FILE = path.join(SRC, GG_FILE)
SRC_UM_FILE = path.join(SRC, UM_FILE)
SRC_HK_FILE = path.join(SRC, HK_FILE)
SRC_NE_FILE = path.join(SRC, NE_FILE)
OUT_KAREN_FILE = path.join(OUT, KAREN_FILE)

base = ff.open(SRC_GG_FILE)
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
        base.selection.select(glyph.unicode)
        base.paste()

# Merge Hack
hk.em = EM
for glyph in hk.glyphs():
    if glyph.isWorthOutputting() and 0xa1 <= glyph.unicode and \
            len(list(base.selection.select(glyph.unicode).byGlyphs)) > 0 and \
            list(base.selection.byGlyphs)[0].width == FULL_WIDTH:
        glyph.transform(HK_SCALE_MAT)
        glyph.width = HALF_WIDTH
        hk.selection.select(glyph.unicode)
        hk.copy()
        base.selection.select(glyph.unicode)
        base.paste()

# Merge Noto Emoji
ne.em = EM
for glyph in ne.glyphs():
    if glyph.isWorthOutputting() and 0x20e0 <= glyph.unicode:
        glyph.transform(NE_SCALE_MAT)
        glyph.width = FULL_WIDTH
        ne.selection.select(glyph.encoding)
        ne.copy()
        base.selection.select(glyph.unicode)
        base.paste()


# Customize several glyphs
## No-break space
base.selection.select(0xa0)
list(base.selection.byGlyphs)[0].width = HALF_WIDTH

## Half-width space
base.selection.select(0x20)
list(base.selection.byGlyphs)[0].width = HALF_WIDTH

## |
um.selection.select(0xa6); um.copy()
base.selection.select(0x7c); base.paste()


# Set font info
base.ascent = ASCENT
base.descent = DESCENT
base.os2_winascent = ASCENT
base.os2_windescent = DESCENT
base.os2_typoascent = TYPO_ASCENT
base.os2_typodescent = TYPO_DESCENT
base.os2_typolinegap = 0
base.hhea_ascent = ASCENT
base.hhea_descent = -DESCENT
base.hhea_linegap = 0
base.vhea_linegap = 0
base.upos = 45

## Copyright
def generate_copyright(font):
    s = "\n\n"
    s += "* " + font.fontname
    s += "\n"
    s += font.copyright
    return s
karen_copyright = "Karen is based on the following products:"
karen_copyright += generate_copyright(base)
karen_copyright += generate_copyright(um)
karen_copyright += generate_copyright(hk)
karen_copyright += generate_copyright(ne)
base.copyright = karen_copyright
base.sfnt_names = \
    tuple((row[0], row[1], karen_copyright if row[1] == "Copyright" else row[2]) \
        for row in base.sfnt_names)

base.fontname = KAREN_FONTNAME
base.familyname = KAREN_FAMILYNAME
base.fullname = KAREN_FONTNAME
base.weight = KAREN_WEIGHT
base.os2_vendor = ""
base.sfntRevision = KAREN_VERSION
base.appendSFNTName("English (US)", "Trademark", "")
base.appendSFNTName("English (US)", "Designer", "")
base.appendSFNTName("English (US)", "Descriptor", "")
base.appendSFNTName("English (US)", "License", "")
base.appendSFNTName("English (US)", "License URL", "")
base.appendSFNTName("English (US)", "Vendor URL", "")
base.appendSFNTName("English (US)", "Copyright", karen_copyright)
base.appendSFNTName("English (US)", "Version", KAREN_VERSION_STR)
base.appendSFNTName("English (US)", "UniqueID", KAREN_FONTNAME + " " + KAREN_VERSION_STR)
base.appendSFNTName("English (US)", "Preferred Family", KAREN_FAMILYNAME)
base.appendSFNTName("English (US)", "Preferred Styles", KAREN_WEIGHT)
base.appendSFNTName("Japanese", "Family", KAREN_FAMILYNAME_JA)
base.appendSFNTName("Japanese", "Fullname", KAREN_FONTNAME_JA)
base.appendSFNTName("Japanese", "Preferred Family", KAREN_FAMILYNAME_JA)
base.appendSFNTName("Japanese", "Preferred Styles", KAREN_WEIGHT)

# Generate Karen
base.generate(OUT_KAREN_FILE)
