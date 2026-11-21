"""genbook.py <n> <seed> <out.json>: make n new 8-ply openings, disjoint from starts.json (034's 100-opening book).
Each ply picks uniformly (seeded) among legal moves whose engine-v3 depth-3 score (srch depth 2 after the move,
root set up exactly as base.py root() does) is within 25 cp of the best, so openings are varied but sound.
Final position must score |v| <= 60 cp at the same depth.
Uses engine-v3 (base.py) move generator and evaluation only; no engine code is modified."""
import json, random, sys, os
sys.argv, args = sys.argv[:1], sys.argv[1:]
import h2h
n, seed, out = int(args[0]), int(args[1]), args[2]
rng = random.Random(seed)
R = h2h.load(os.path.join(h2h.HERE, 'base.py'))
def prep(R, S):
    # same setup as base.py root(): phase-specific tables and fresh score for S
    b = S[0]; MATE = R['MATE']
    ph = min(24, sum((0,1,1,2,4)['PNBRQ'.index(x)] for x in b.upper() if x in 'NBRQ'))
    TS = [R['tab'](ph, b), R['tab'](ph, b[::-1].swapcase())]; R['TS'] = TS
    s = 30*((b.count('B')>1)-(b.count('b')>1))
    for i, p in enumerate(b):
        if p.isupper(): s += TS[0][p][i]
        elif p.islower(): s -= TS[1][p.upper()][119-i]
    R.update(NN=0, HARD=10**9, KL=[[] for _ in range(200)], RD=3, H=set()); R['TT'].clear(); R['HI'].clear()
    return (b, s, S[2], S[3], 0)
def score(R, S, m):
    return -R['srch'](R['mk'](S, m), 2, -R['MATE'], R['MATE'], 1)
def final_key(R, opening):
    S = h2h.start(R); c = 0
    for u in opening:
        m = dict(h2h.legal(R, S, c))[u]; S = R['mk'](S, m); c ^= 1
    return S[0], S
seen = {final_key(R, o)[0] for _, o in h2h.BOOK}
book = []; tries = 0
while len(book) < n:
    tries += 1
    S = h2h.start(R); c = 0; seq = []; ok = True
    for ply in range(8):
        lg = h2h.legal(R, S, c)
        if not lg: ok = False; break
        P = prep(R, S)
        sc = [(score(R, P, m), u, m) for u, m in lg]
        best = max(s for s, _, _ in sc)
        u, m = rng.choice([(u, m) for s, u, m in sc if s >= best - 25])
        S = R['mk'](S, m); c ^= 1; seq.append(u)
    if not ok or not h2h.legal(R, S, c): continue
    P = prep(R, S)
    if abs(max(score(R, P, m) for _, m in h2h.legal(R, S, c))) > 60: continue
    if S[0] in seen: continue
    seen.add(S[0]); book.append([f"gen{seed}-{len(book):03d}", seq])
json.dump(book, open(out, 'w'))
print(len(book), 'openings from', tries, 'tries')
