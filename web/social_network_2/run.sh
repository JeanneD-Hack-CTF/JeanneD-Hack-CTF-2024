#!/bin/bash

# Listen at every connection on port 80
gunicorn "app:app" -w 1 --threads 4 -b 0.0.0.0:80
