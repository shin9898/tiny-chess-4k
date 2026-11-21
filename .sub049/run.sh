#!/bin/zsh
# 049: C3 (b3d7f39 main.py) on practice trial pt0, twice in parallel (separate ports), to check determinism + completion
export PATH=/usr/local/bin:$PATH
cd "$(dirname $0)"
W=/Users/apple/dev/makefun-tiny-chess-work
echo "start $(date '+%F %T')" > progress.txt
for r in a b; do
  p=18490; [ $r = b ] && p=18590
  ( python3 $W/run_trial.py $PWD/c3-main.py $W/trials/pt0 $PWD/runs/c3-pt0$r $p > log-$r.txt 2>&1
    echo "$r done $(date '+%F %T') rc=$? $(tail -1 log-$r.txt)" >> progress.txt ) &
done
wait
shasum -a 256 runs/c3-pt0*/moves.json >> progress.txt
echo "all done $(date '+%F %T')" >> progress.txt
