#!/bin/bash -e
cd /home/dietpi/security
. env/bin/activate

while true; do
    DISPLAY=:0 ./desktop_qt.py
done
