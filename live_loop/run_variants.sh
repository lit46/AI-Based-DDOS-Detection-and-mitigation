#!/bin/bash
cd ~/sdn_floodlight_dataset/sdn_loop
for v in udp icmp lowrate flashcrowd; do
  mn -c >/dev/null 2>&1
  /usr/bin/python3 topo_loop.py --scenario loop --rounds 3 --variant $v --out_dir var_$v > var_$v.log 2>&1
done
echo VARIANTS DONE
