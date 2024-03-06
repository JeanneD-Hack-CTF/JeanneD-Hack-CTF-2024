#!/bin/bash

# Listen at every connection on port 80 and running as nobody
gunicorn "app:app" -w 4 --threads 4 -u nobody -g nogroup -b 0.0.0.0:80

