#!/bin/zsh
# 051 screening: <cand>.py vs engine-v3 (base.py), H2H_BUD=10000 both, 034 starts.json 100 openings x both colours = 200 games (same as 034 screening).
# usage: nohup ./run-scr.sh d1 4 > scr-d1.log 2>&1 &   (resumable)
cd "$(dirname $0)"
export H2H_BUD=10000
echo "start $1 $(date '+%F %T') load=$(uptime | sed 's/.*averages: //')" >> progress.txt
python3 h2h.py $1.py base.py scr-$1.jsonl ${2:-4} 0-99
echo "end $1 rc=$? $(date '+%F %T') $(python3 tally.py scr-$1.jsonl | head -1)" >> progress.txt
