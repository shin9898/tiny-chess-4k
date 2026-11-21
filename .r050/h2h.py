"""Head-to-head referee: two unpacked engine sources play the 40-opening book with both colours.

usage: h2h.py <engineA.py> <engineB.py> <out.jsonl> [procs] [openings e.g. 0-39]
Each game runs in its own process with fresh engine globals (empty TT) so games are independent
and deterministic. Rules follow RULES.txt: mate, stalemate, insufficient material, threefold,
50-move (100 plies), ply cap 200 adjudicated by material margin >= 5.
Result lines: {"op","a_white","res"(A's points),"reason","plies","cpuA","cpuB" (max per move),"sumA","nA",...}
"""
import json, os, sys, time
from multiprocessing import Pool
os.environ.setdefault('MAKEFUN_ENV_URL', 'http://x')
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = json.load(open(os.path.join(HERE, 'starts.json')))
SF = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
MV = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}


def load(path):
    src = open(path).read()
    if '\nwhile 1:' in src: src = src[:src.index('\nwhile 1:')]
    g = {'__name__': 'eng'}
    exec(compile(src, path, 'exec'), g)
    if os.environ.get('H2H_BUD'): g['BUD'] = int(os.environ['H2H_BUD'])  # same reduced budget for both sides
    return g


def start(R):
    fen = SF.split()[0]
    for k in '2345678': fen = fen.replace(k, '.' * int(k))
    fen = fen.replace('1', '.').replace('/', '  ')
    b = ' ' * 21 + fen + ' ' * 21
    R['TS'] = [R['tab'](24, b)] * 2
    return (b, 0, 15, 0, 0)


def legal(R, S, c):
    out = []
    for m in R['gen'](S):
        C = R['mk'](S, m)
        if R['att'](C[0], C[0].find('k'), 1): continue
        u = R['nm'](m[0], c) + R['nm'](m[1], c) + m[2].lower()
        out.append((u, m))
        if m[2] == 'N':
            for p in 'RB':
                out.append((u[:4] + p.lower(), (m[0], m[1], p)))
    return out


def insufficient(b):
    pcs = [p for p in b if p.isalpha() and p.upper() != 'K']
    if any(p.upper() in 'PRQ' for p in pcs): return False
    if len(pcs) <= 1: return True
    if all(p.upper() == 'B' for p in pcs):
        cols = {((i // 10) + (i % 10)) % 2 for i, p in enumerate(b) if p.upper() == 'B'}
        return len(cols) == 1
    return False


def material(b):  # side to move minus opponent
    return sum(MV[p] for p in b if p.isupper()) - sum(MV[p.upper()] for p in b if p.islower())


def play(args):
    pa, pb, op, a_white = args
    R = load(os.path.join(HERE, 'base.py'))
    EA, EB = load(pa), load(pb)
    name, opening = BOOK[op]
    S = start(R); c = 0; hist = []; reps = {}; hm = 0
    cpu = {0: [], 1: []}  # 0: A, 1: B
    reason = None; res = None
    while True:
        lg = legal(R, S, c)
        ep = S[3] if S[3] and any(m[1] == S[3] and S[0][m[0]] == 'P' for _, m in lg) else 0
        key = (S[0], c, S[2], ep)
        reps[key] = reps.get(key, 0) + 1
        if not lg:
            inchk = R['att'](S[0], S[0].find('K'), 0)
            reason = 'checkmate' if inchk else 'stalemate'
            res = (0 if inchk else .5, c)  # points for side to move
            break
        if reps[key] >= 3: reason = 'threefold'; res = (.5, c); break
        if hm >= 100: reason = 'fifty'; res = (.5, c); break
        if insufficient(S[0]): reason = 'insufficient'; res = (.5, c); break
        if len(hist) >= 200:
            d = material(S[0]); reason = 'adjudicated'
            res = (1 if d >= 5 else 0 if d <= -5 else .5, c); break
        if len(hist) < len(opening):
            u = opening[len(hist)]
        else:
            white_to_move = c == 0
            who = 0 if white_to_move == a_white else 1
            E = EA if who == 0 else EB
            t0 = time.process_time()
            u = E['think']({'start_fen': SF, 'moves': list(hist), 'legal_moves': [x for x, _ in lg]})
            cpu[who].append(time.process_time() - t0)
        mm = dict(lg)
        if u not in mm:
            reason = 'illegal'; res = (0, c); break
        m = mm[u]
        cap = S[0][m[1]] != '.' or (S[0][m[0]] == 'P' and m[1] == S[3])
        hm = 0 if cap or S[0][m[0]] == 'P' else hm + 1
        S = R['mk'](S, m); c ^= 1; hist.append(u)
    pts_stm, stm = res
    # side to move stm (0 white); A is white iff a_white
    a_is_stm = (stm == 0) == a_white
    ra = pts_stm if a_is_stm else 1 - pts_stm
    return {'op': op, 'name': name, 'a_white': a_white, 'res': ra, 'reason': reason, 'plies': len(hist),
            'maxA': round(max(cpu[0] or [0]), 3), 'maxB': round(max(cpu[1] or [0]), 3),
            'sumA': round(sum(cpu[0]), 2), 'nA': len(cpu[0]), 'sumB': round(sum(cpu[1]), 2), 'nB': len(cpu[1]),
            'moves': hist}


def main():
    pa, pb, out = sys.argv[1:4]
    procs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    lo, hi = map(int, (sys.argv[5] if len(sys.argv) > 5 else '0-99').split('-'))
    done = set()
    if os.path.exists(out):
        for l in open(out):
            j = json.loads(l); done.add((j['op'], j['a_white']))
    tasks = [(os.path.abspath(pa), os.path.abspath(pb), op, aw) for op in range(lo, hi + 1) for aw in (True, False)
             if (op, aw) not in done]
    with Pool(procs) as p, open(out, 'a') as f:
        for r in p.imap_unordered(play, tasks):
            f.write(json.dumps(r) + '\n'); f.flush()
            print(r['op'], 'Awhite' if r['a_white'] else 'Ablack', r['res'], r['reason'], r['plies'], r['maxA'], r['maxB'], flush=True)


if __name__ == '__main__':
    main()
