#!/bin/bash

pkill -9 python3
pkill -9 python

bash -c 'find ./logs/ -name "*.log" -type f -delete'

python3 -m camera_server.serverXavier.py &
sleep 1 && python3 -m camera_serve.saveCameraClient &
sleep 2 && python3 main.py &
