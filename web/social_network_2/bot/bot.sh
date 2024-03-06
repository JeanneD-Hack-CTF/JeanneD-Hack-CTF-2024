#!/bin/bash

/opt/bitnami/python/bin/python3 /app/bot/bot.py --host "127.0.0.1" --port 80 --delay 3 --headless >>/var/log/admin-bot.log
pkill firefox-esr
