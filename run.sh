#!/bin/bash

pkill -9 python3
pkill -9 python

sleep 2

bash -c 'find ./logs/ -name "*.log" -type f -delete'

python3 -m neural_networks.DarknetServer -m './neural_networks/models/gate' &

python3 -m camera_server.serverXavier &
sleep 1 && python3 -m camera_server.saveCameraClient &
sleep 5 && python3 main.py 
