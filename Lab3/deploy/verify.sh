#!/bin/bash
set -e
sleep 5
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Accept: text/html" http://127.0.0.1/)
if [ "$HTTP_CODE" -ne 200 ] && [ "$HTTP_CODE" -ne 406 ]; then
    exit 1
fi
ALIVE_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health/alive)
if [ "$ALIVE_CODE" -ne 200 ]; then
    exit 1
fi