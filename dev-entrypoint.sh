#!/bin/sh
set -e

rsync -arv --progress /usr/src/cache/node_modules/. /kerckhoff/node_modules/
cmd="nohup npm run watch";
$cmd &
python3.7 kerckhoff/manage.py makemigrations
python3.7 kerckhoff/manage.py migrate
exec "$@"
