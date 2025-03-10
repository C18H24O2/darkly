#!/usr/bin/env bash

if [ ! -f password ]; then
  echo "password file not found"
  exit 1
fi
URL_ROOT="${1:-http://10.13.248.102}"
curl "$URL_ROOT/index.php?page=signin&username=admin&password=$(cat password)&Login=Login#" 2>/dev/null | grep "flag" --color=auto
