#!/bin/zsh
# 051 step 3: D1 vs C3 at full budget (H2H_BUD=30000 both, HARD=60000), 034 starts.json 100 openings x both colours = 200 games, 6 procs.
# Then D1 determinism + CPU sweep over pos050.json (150 positions from 050): det r1-r3 (3 separate processes at once, cold),
# cold-low (1 process), warm-high (6 chunks at once). Resumable h2h. Start: nohup ./run-h2h.sh > run-h2h.log 2>&1 &
cd "$(dirname $0)"
st() { echo "$1 $(date '+%F %T') load=$(uptime | sed 's/.*averages: //')" >> progress.txt; }
st "h2h d1-vs-c3 start"
H2H_BUD=30000 python3 h2h050.py d1.py c3.py h2h-d1c3.jsonl 6 0-99 > h2h-d1c3.log 2>&1
st "h2h end rc=$? $(python3 tally.py h2h-d1c3.jsonl | head -1)"
export BENCH_ENG=d1.py
st "det start"; for i in 1 2 3; do python3 bench.py pos050.json b-det-r$i.jsonl cold > /dev/null & done; wait; st "det done"
st "cold-low start"; python3 bench.py pos050.json b-cold-low.jsonl cold > /dev/null; st "cold-low done"
st "warm-high start"; for r in 0-24 25-49 50-74 75-99 100-124 125-149; do python3 bench.py pos050.json b-warm-high.$r.jsonl warm $r > /dev/null & done; wait; st "warm-high done"
st "all done"
