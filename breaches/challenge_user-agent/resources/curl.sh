#!/usr/bin/env bash

URL_ROOT="${1:-http://10.13.248.102}"
URL="$URL_ROOT/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f"
curl -A "ft_bornToSec" -e "https://www.nsa.gov/" $URL 2>/dev/null | grep "flag" --color=auto
