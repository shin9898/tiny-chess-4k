#!/bin/zsh
# 050: C3 (b3d7f39) vs engine-v3 (58bb1ce), BUD=30000 both (HARD=60000), 200 new openings (starts050.json) x both colours = 400 games, 6 procs.
# Resumable: h2h050.py skips (op, colour) already in the jsonl. Start detached: nohup ./run.sh > run.log 2>&1 &
cd "$(dirname $0)"
export H2H_BUD=30000 H2H_BOOK=starts050.json
echo "start $(date '+%F %T') load=$(uptime | sed 's/.*averages: //')" >> progress.txt
./watch.sh &
WP=$!
python3 h2h050.py c3.py base.py h2h-c3.jsonl 6 0-199 > h2h.log 2>&1
echo "h2h exit rc=$? $(date '+%F %T')" >> progress.txt
kill $WP 2>/dev/null
echo "終了 $(date '+%m-%d %H:%M') $(python3 tally.py h2h-c3.jsonl --prev 95 35 70 | tr '\n' '|')" >> progress.txt
