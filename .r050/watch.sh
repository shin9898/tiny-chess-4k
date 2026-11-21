#!/bin/zsh
# append a tally line to progress.txt each time 40 more games are done
cd "$(dirname $0)"; last=0
while sleep 60; do
  n=$(wc -l < h2h-c3.jsonl 2>/dev/null | tr -d ' '); n=${n:-0}
  if (( n - last >= 40 )); then last=$n
    echo "$(date '+%m-%d %H:%M') load=$(uptime | sed 's/.*averages: //') $(python3 tally.py h2h-c3.jsonl --prev 95 35 70 | grep -E '^(今回|合算|CPU/手 C3)' | tr '\n' '|')" >> progress.txt
  fi
  grep -q Traceback h2h.log && echo "TRACEBACK $(date '+%T')" >> progress.txt && exit
done
