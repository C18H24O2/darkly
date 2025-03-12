#!/usr/bin/env bash

URL_ROOT="${URL_ROOT:-http://10.13.248.102}"
URL="$URL_ROOT/index.php?page=redirect&site=test"
curl $URL 2>/dev/null | grep "flag" --color=auto
