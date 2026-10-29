#!/bin/bash
cd "$(dirname "$(readlink -f "$0")")"
for v in syn udp icmp lowrate flashcrowd; do
  mn -c > /dev/null 2>&1
  /usr/bin/python3 topo_loop.py --scenario loop --rounds 3 --variant $v --out_dir v2_$v > v2_$v.log 2>&1
done
echo VARIANTS2 DONE
