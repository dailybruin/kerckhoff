#!/bin/sh
gunicorn -b 0.0.0.0:5000 -w 4 -k gthread --threads 2 kerckhoff.wsgi --log-file -