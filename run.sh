#!/bin/bash
python3 -m create_port.py &
sleep 1
pkill -9 python3
pkill -9 python

python3 -m definitions.py &

sleep 2

bash -c 'find ./logs/ -name "*.log" -type f -delete'

python3 -m camera_server.serverXavier &
sleep 2
python3 -m neural_networks.DarknetServer &

sleep 10 #&& python3 -m camera_server.saveCameraClient &

python3 main.py
