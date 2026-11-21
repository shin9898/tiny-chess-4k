#!/bin/zsh
# 050 CPU sweep of C3 over pos050.json (150 positions) + games034.json (10 full-game replays). Start: nohup ./bench.sh > bench.log 2>&1 &
# 1 cold-low: 1 process (low load)      2 cold-high: 6 identical processes at once (load ~6-7, like the h2h run)
# 3 warm-high: TT warmed along the game, 6 chunks at once   4 game-low: 034's 10 heaviest screening games replayed, 1 process
cd "$(dirname $0)"
st() { echo "$1 $(date '+%F %T') load=$(uptime | sed 's/.*averages: //')" >> bprogress.txt; }
st "1 cold-low start";  python3 bench.py pos050.json b-cold-low.jsonl cold > /dev/null; st "1 done"
st "2 cold-high start"; for i in 1 2 3 4 5 6; do python3 bench.py pos050.json b-cold-high$i.jsonl cold > /dev/null & done; wait; st "2 done"
st "3 warm-high start"; for r in 0-24 25-49 50-74 75-99 100-124 125-149; do python3 bench.py pos050.json b-warm-high.$r.jsonl warm $r > /dev/null & done; wait; st "3 done"
st "4 game-low start";  python3 bench.py games034.json b-game-low.jsonl game > /dev/null; st "4 done"
st "all done"
