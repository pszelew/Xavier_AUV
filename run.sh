#!/bin/bash

pkill -9 python3
pkill -9 python

python3 -m camera_server.serverXavier.py &
sleep 2 && python3 main.py 
