#!/bin/zsh
# check run: C3 pt0 again (determinism) + engine-v3 (58bb1ce) pt0..2 under the same conditions
export PATH=/usr/local/bin:$PATH
cd "$(dirname $0)"
W=~/dev/makefun-tiny-chess-work
echo "start $(date '+%F %T') load=$(uptime | sed 's/.*averages: //')" > progress2.txt
( CPU_LOG=$PWD/cpu-c3-pt0b.tsv python3 $W/run_trial.py $PWD/cpuwrap.py $W/trials/pt0 $PWD/runs/c3-pt0b 18480 > log-c3-pt0b.txt 2>&1; echo "c3-pt0b done $(tail -1 log-c3-pt0b.txt)" >> progress2.txt ) &
i=0
for t in pt0 pt1 pt2; do
  ( ENGINE=$PWD/v3-main.py CPU_LOG=$PWD/cpu-v3-$t.tsv python3 $W/run_trial.py $PWD/cpuwrap.py $W/trials/$t $PWD/runs/v3-$t $((18580+i*100)) > log-v3-$t.txt 2>&1; echo "v3-$t done $(tail -1 log-v3-$t.txt)" >> progress2.txt ) &
  i=$((i+1))
done
wait
echo "all done $(date '+%F %T')" >> progress2.txt
