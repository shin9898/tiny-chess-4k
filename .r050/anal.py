"""anal.py: summarize 050 CPU sweep files (b-*.jsonl) by run and category."""
import json, glob, collections
def load(pat): return [json.loads(l) for f in sorted(glob.glob(pat)) for l in open(f)]
def q(c, f): return c[min(len(c)-1, int(f*len(c)))]
def summ(tag, R):
    c = sorted(r['cpu'] for r in R); w = max(R, key=lambda r: r['cpu'])
    print(f"{tag}: n={len(c)} 平均 {sum(c)/len(c):.3f} 中央 {q(c,.5):.3f} p90 {q(c,.9):.3f} p99 {q(c,.99):.3f} 最大 {c[-1]:.3f} s "
          f"(>2s {sum(x>2 for x in c)} >3s {sum(x>3 for x in c)} >5s {sum(x>5 for x in c)}) 最悪 {w['id']} ply{w['ply']} nn{w['nn']} load{w['load']:.1f}")
for tag, pat in (('cold-low', 'b-cold-low.jsonl'), ('cold-high(6並列×各1回)', 'b-cold-high*.jsonl'), ('warm-high', 'b-warm-high.*.jsonl'), ('game-low(034の10局再生)', 'b-game-low.jsonl')):
    R = load(pat)
    if not R: continue
    summ(tag, R)
    if 'game' not in tag:
        for cat in ('opening', 'middle', 'endgame', 'heavy'): summ('  ' + cat, [r for r in R if r['cat'] == cat])
# per-position max over the 6 cold-high copies; nodes identical across copies (determinism)
H = collections.defaultdict(list)
for r in load('b-cold-high*.jsonl'): H[r['id']].append((r['cpu'], r['nn'], r['move']))
print('cold-high 6回で nn/move が全一致した局面:', sum(len({(n, m) for _, n, m in v}) == 1 for v in H.values()), '/', len(H))
L = {r['id']: r for r in load('b-cold-low.jsonl')}
print('cold-low と cold-high の nn/move 一致:', sum((L[k]['nn'], L[k]['move']) == (v[0][1], v[0][2]) for k, v in H.items()), '/', len(H))
nn = sorted(r['nn'] for r in L.values()); print('cold-low nodes 最大', nn[-1], '>=54000:', sum(x >= 54000 for x in nn))
