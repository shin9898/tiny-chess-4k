"""selpos.py <seed> <out.json> <out-games.json>: pick bench positions (C3 to move) from 050's h2h-c3.jsonl and 034's scr-c3.jsonl.
  opening 40 (ply 8-20), middlegame 40 (ply 21+, phase >= 10), endgame 40 (phase <= 6),
  heavy 30 = the 30 highest in-game CPU moves of C3 in h2h-c3.jsonl (high-load measurement), one per game.
  Every position is a ply where C3 moved in the source game (so it is never terminal).
  Half of opening/middle/endgame come from each source. phase = base.py root() formula (N,B=1 R=2 Q=4, max 24).
Games file: the 10 games of 034 screening (BUD=10000) with the largest C3 max CPU, for full-game replay at BUD=30000."""
import json, random, sys, os
sys.argv, args = sys.argv[:1], sys.argv[1:]
import h2h
rng = random.Random(int(args[0]))
R = h2h.load(os.path.join(h2h.HERE, 'base.py'))
def boards(moves):
    S = h2h.start(R); c = 0; out = [S[0]]
    for u in moves: S = R['mk'](S, dict(h2h.legal(R, S, c))[u]); c ^= 1; out.append(S[0])
    return out
def phase(b): return min(24, sum((0, 1, 1, 2, 4)['PNBRQ'.index(x)] for x in b.upper() if x in 'NBRQ'))
new = [json.loads(l) for l in open('h2h-c3.jsonl')]
old = [json.loads(l) for l in open('../../034/.h2h/scr-c3.jsonl')]
cand = {'opening': [], 'middle': [], 'endgame': []}
for srcname, G in (('050', new), ('034', old)):
    for gi, g in enumerate(G):
        bs = boards(g['moves'])
        for q in range(8, len(g['moves'])):
            if (q % 2 == 0) != g['a_white']: continue
            b = bs[q]; ph = phase(b)
            cat = 'opening' if q <= 20 else 'middle' if ph >= 10 else 'endgame' if ph <= 6 else None
            if cat: cand[cat].append((srcname, gi, q))
pos = []
for cat, L in cand.items():
    for srcname in ('050', '034'):
        sub = [x for x in L if x[0] == srcname]; rng.shuffle(sub); used = set(); k = 0
        for s_, gi, q in sub:
            if gi in used: continue
            g = (new if s_ == '050' else old)[gi]
            mv = g['moves'][:q]
            used.add(gi); pos.append(dict(id=f'{cat}-{s_}-{k:02d}', cat=cat, src=f'{s_}:game{gi}:op{g["op"]}:{"w" if g["a_white"] else "b"}', moves=mv)); k += 1
            if k == 20: break
top = sorted(((x, gi, g['plyA'][j]) for gi, g in enumerate(new) for j, x in enumerate(g['cpuA'])), reverse=True)
used = set(); k = 0
for x, gi, q in top:
    if gi in used: continue
    used.add(gi); g = new[gi]
    pos.append(dict(id=f'heavy-{k:02d}', cat='heavy', src=f'050:game{gi}:op{g["op"]}:{"w" if g["a_white"] else "b"}:ingame{x}', moves=g['moves'][:q])); k += 1
    if k == 30: break
json.dump(pos, open(args[1], 'w'))
gm = sorted(range(len(old)), key=lambda i: -old[i]['maxA'])[:10]
json.dump([dict(id=f'game034-{i}', cat='game', src=f'034:game{i}:op{old[i]["op"]}:maxA{old[i]["maxA"]}', moves=old[i]['moves'], c3white=old[i]['a_white']) for i in gm], open(args[2], 'w'))
import collections; print(len(pos), collections.Counter(p['cat'] for p in pos))
