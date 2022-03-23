#!/bin/bash
python3 /init.py
/bin/bash /data/run.sh >> /data/proxy.log &
tail -f /data/proxy.log
