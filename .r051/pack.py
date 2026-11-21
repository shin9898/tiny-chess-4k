"""pack.py <src.py> <out main.py>: lzma-pack source into a #coding:l1 self-extracting main.py (smallest of several settings)."""
import ast, lzma, sys

src = open(sys.argv[1]).read().encode()


def lit(data):
    s = data.decode('l1')
    best = None
    for q in ("'", '"'):
        o = []
        for ch in s:
            if ch == '\\': o.append('\\\\')
            elif ch == q: o.append('\\' + q)
            elif ch == '\n': o.append('\\n')
            elif ch == '\r': o.append('\\r')
            elif ch == '\0': o.append('\\0')
            else: o.append(ch)
        r = q + ''.join(o) + q
        # '\0' followed by a digit would read as octal
        r = r.replace('\\0', '\\x00') if any(r[i:i+2] == '\\0' and r[i+2:i+3].isdigit() for i in range(len(r))) else r
        if best is None or len(r.encode('l1')) < len(best.encode('l1')): best = r
    return best


best = None
for fmt, filt in [(lzma.FORMAT_ALONE, None)] + [(lzma.FORMAT_RAW, None)] * 0:
    for preset in (9, 9 | lzma.PRESET_EXTREME):
        for lc in range(0, 5):
            for lp in range(0, 3):
                for pb in range(0, 3):
                  for mf in (lzma.MF_BT4, lzma.MF_BT3, lzma.MF_BT2, lzma.MF_HC4):
                   for nl in (32, 64, 128, 273):
                    try:
                        d = lzma.compress(src, format=lzma.FORMAT_ALONE, filters=[{'id': lzma.FILTER_LZMA1, 'preset': preset, 'lc': lc, 'lp': lp, 'pb': pb, 'dict_size': 8192, 'mf': mf, 'nice_len': nl, 'depth': 0}])
                    except Exception:
                        continue
                    out = "#coding:l1\nimport lzma;exec(lzma.decompress(" + lit(d) + ".encode('l1')))"
                    b = out.encode('l1')
                    if best is None or len(b) < len(best): best = b
open(sys.argv[2], 'wb').write(best)
assert lzma.decompress(ast.literal_eval(best.decode('l1').split('decompress(', 1)[1].rsplit(".encode", 1)[0]).encode('l1')) == src
print(len(best))
