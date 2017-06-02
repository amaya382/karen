import sys
import fontforge as ff

def overwrite_os2(src):
    font = ff.open(src)
    font.os2_unicoderanges = (-520090881, 2059927039, 100663350, 67108864)
    font.os2_codepages = (-535690817, -537460736)
    font.generate(src)

overwrite_os2(sys.argv[1])
