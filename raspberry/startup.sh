#!/usr/bin/env bash
nohup python3 Documents/gitRepos/freyr/s_adc.py -s 20  >> s_adc.log &
nohup python3 Documents/gitRepos/freyr/s_dht11.py -s 20 >> s_dht11.log &
nohup python3 Documents/gitRepos/freyr/s_camera.py -s 30 >> s_camera.log &

