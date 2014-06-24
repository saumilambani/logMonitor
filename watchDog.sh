#!/bin/bash
echo $1
if [ $# -eq 0 ]; then
  python logMonitor/watchdog.py
else
  TAIL="--dur $1"
  python logMonitor/watchdog.py $TAIL
fi
