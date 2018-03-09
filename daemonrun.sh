#!/bin/bash
# This is our first script.
source ../venv/bin/activate
echo 'entering venv...\n'
gunicorn -w 3 startserver:application -b unix:/tmp/gunicorn.sock -D 
echo 'Starting server successfully\n'
