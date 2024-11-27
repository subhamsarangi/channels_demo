## LINUX

daphne backend.asgi:application --bind 0.0.0.0 --port 8001 > access_$(date +%Y%m%d).log 2> log_$(date +%Y%m%d).log

jobs

fg %1

## WINDOWS

for /f %i in ('powershell -Command "Get-Date -Format yyyyMMdd"') do set DATE=%i
daphne backend.asgi:application --bind 0.0.0.0 --port 8001 > access_%DATE%.log 2> log_%DATE%.log

ws://127.0.0.1:8001/ws/chat/<room_name>/
