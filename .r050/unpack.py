"""unpack.py <main.py> <out.py>: write the lzma-decompressed source of a self-extracting main.py (no exec)."""
import sys, lzma, re
src = open(sys.argv[1], encoding='latin-1').read()
m = re.search(r"exec\(lzma\.decompress\((.*)\)\)", src, re.S)
data = eval(m.group(1)).encode('latin-1') if isinstance(eval(m.group(1)), str) else eval(m.group(1))
open(sys.argv[2], 'wb').write(lzma.decompress(data))
