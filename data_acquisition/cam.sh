#!/bin/bash
# will be run as cron job+ (see crontab -e):
# 0 */2 * * * /home/pi/smartfridge_cam/cam.sh

DATE=$(date "+%Y-%m-%d-%H%M")
raspistill -vf -hf -o /home/pi/smartfridge_cam/$DATE.jpg