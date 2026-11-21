"""[051: engine file from $BENCH_ENG (default c3.py)] bench.py <positions.json> <out.jsonl> <cold|warm> [i0-i1]: per-move CPU (process_time) and nodes of C3 (c3.py) per position.
cold: fresh engine globals (empty TT), one think() at the position.
warm: fresh globals, then think() at every earlier ply >= 8 with the same side to move along the recorded history
      (as in a game: TT/history kept between moves), timing only the last one.
game: replay a whole recorded game; C3 thinks at every ply >= 8 of its colour ("c3white") with TT kept, each one timed
      and written as its own row (moves of the record are applied, not C3's choice).
Positions: [{"id","cat","src","moves":[uci...]}] -- the engine is to move after "moves". Engine code unchanged."""
import json, os, sys, time
sys.argv, args = sys.argv[:1], sys.argv[1:]
import h2h
P = json.load(open(args[0])); out = args[1]; mode = args[2]
lo, hi = map(int, (args[3] if len(args) > 3 else f'0-{len(P)-1}').split('-'))
R = h2h.load(os.path.join(h2h.HERE, 'base.py'))
def legal_after(moves):
    S = h2h.start(R); c = 0
    for u in moves: S = R['mk'](S, dict(h2h.legal(R, S, c))[u]); c ^= 1
    return [u for u, _ in h2h.legal(R, S, c)]
def think(E, moves):
    lg = legal_after(moves); E['NN'] = 0
    t = time.process_time(); u = E['think']({'start_fen': h2h.SF, 'moves': list(moves), 'legal_moves': lg})
    return time.process_time() - t, E['NN'], u, len(lg)
with open(out, 'a') as f:
    for k in range(lo, hi + 1):
        p = P[k]; mv = p['moves']; E = h2h.load(os.path.join(h2h.HERE, os.environ.get('BENCH_ENG', 'c3.py')))
        if mode == 'game':
            for q in range(8, len(mv)):
                if (q % 2 == 0) != p['c3white']: continue
                cpu, nn, u, nl = think(E, mv[:q])
                f.write(json.dumps(dict(id=p['id'], cat='game', src=p['src'], ply=q, mode=mode, cpu=round(cpu, 4), nn=nn, move=u,
                                        nlegal=nl, load=os.getloadavg()[0])) + '\n'); f.flush()
            print(k, 'game done', flush=True); continue
        if mode == 'warm':
            for q in range(8, len(mv)):
                if (len(mv) - q) % 2 == 0: think(E, mv[:q])
        cpu, nn, u, nl = think(E, mv)
        r = dict(id=p['id'], cat=p['cat'], src=p['src'], ply=len(mv), mode=mode, cpu=round(cpu, 4), nn=nn, move=u, nlegal=nl,
                 load=os.getloadavg()[0])
        f.write(json.dumps(r) + '\n'); f.flush(); print(k, r['cat'], r['ply'], r['cpu'], nn, flush=True)
