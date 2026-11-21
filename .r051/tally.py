"""tally.py <games.jsonl> [--prev W D L]: score of A (C3) with 95% CI; optionally pooled with earlier W/D/L counts.
CI: normal approx, per-game SE from the W/D/L sample variance; pair SE uses colour pairs (same opening) when present."""
import json, sys, math, collections
a = sys.argv[1:]; prev = None
if '--prev' in a:
    i = a.index('--prev'); prev = tuple(int(x) for x in a[i+1:i+4]); del a[i:i+4]
G = [json.loads(l) for l in open(a[0])]
def ci(w, d, l):
    n = w + d + l; p = (w + d/2) / n
    var = (w*(1-p)**2 + d*(0.5-p)**2 + l*(0-p)**2) / (n - 1)
    se = math.sqrt(var / n); return n, p, se, p - 1.96*se, p + 1.96*se
def line(tag, w, d, l):
    n, p, se, lo, hi = ci(w, d, l)
    return f"{tag}: {n}局 勝{w} 分{d} 敗{l} スコア率 {p:.4f} SE {se:.4f} 95%CI {lo:.3f}〜{hi:.3f}"
w = sum(g['res'] == 1 for g in G); d = sum(g['res'] == .5 for g in G); l = sum(g['res'] == 0 for g in G)
print(line('今回', w, d, l))
pairs = collections.defaultdict(list)
for g in G: pairs[g['op']].append(g['res'])
full = [sum(v)/2 for v in pairs.values() if len(v) == 2]
if len(full) > 1:
    m = sum(full)/len(full); se = math.sqrt(sum((x-m)**2 for x in full)/(len(full)-1)/len(full))
    print(f"今回 先後ペア単位: {len(full)}ペア 平均 {m:.4f} SE {se:.4f} 95%CI {m-1.96*se:.3f}〜{m+1.96*se:.3f}")
for aw, tag in ((True, 'C3白'), (False, 'C3黒')):
    s = [g['res'] for g in G if g['a_white'] == aw]
    if s: print(f"{tag}: {len(s)}局 {sum(s)/len(s):.3f}")
print('終局理由', dict(collections.Counter(g['reason'] for g in G)))
if prev: print(line('合算(038+今回)', w+prev[0], d+prev[1], l+prev[2]))
for k, tag in (('A', 'C3'), ('B', 'v3')):
    c = sorted(x for g in G for x in g.get('cpu'+k, []))
    if c:
        q = lambda f: c[min(len(c)-1, int(f*len(c)))]
        print(f"CPU/手 {tag}: n={len(c)} 平均 {sum(c)/len(c):.3f} 中央 {q(.5):.3f} p90 {q(.9):.3f} p99 {q(.99):.3f} p99.9 {q(.999):.3f} 最大 {c[-1]:.3f} s | >2s {sum(x>2 for x in c)} >3s {sum(x>3 for x in c)} >4s {sum(x>4 for x in c)} >5s {sum(x>5 for x in c)}")
