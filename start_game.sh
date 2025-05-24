#!/bin/bash -e
cd /home/dietpi/security
. env/bin/activate

while true; do
    ./desktop_qt.py
done
