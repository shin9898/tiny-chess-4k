#!/bin/zsh
# 3 practice trials of C3 (b3d7f39 main.py) in parallel, same runner/trials as engine-v3 (ticket 021)
export PATH=/usr/local/bin:$PATH
cd "$(dirname $0)"
echo "start $(date '+%F %T') load=$(uptime | sed 's/.*averages: //')" > progress.txt
i=0
for t in pt0 pt1 pt2; do
  ( CPU_LOG=$PWD/cpu-$t.tsv python3 /Users/apple/dev/makefun-tiny-chess-work/run_trial.py $PWD/cpuwrap.py /Users/apple/dev/makefun-tiny-chess-work/trials/$t $PWD/runs/c3-$t $((18180+i*100)) > log-$t.txt 2>&1
    echo "$t done $(date '+%F %T') rc=$? $(tail -1 log-$t.txt)" >> progress.txt ) &
  i=$((i+1))
done
wait
echo "all done $(date '+%F %T')" >> progress.txt
