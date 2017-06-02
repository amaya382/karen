import sys
import fontforge as ff

def overwrite_unicoderanges(src):
    font = ff.open(src)
    font.os2_unicoderanges = (-520090881, 2059927039, 100663350, 67108864)
    font.generate(src)

overwrite_unicoderanges(sys.argv[1])
