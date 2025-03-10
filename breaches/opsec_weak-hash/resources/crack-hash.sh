#!/usr/bin/env bash

if [ ! -f "hash.txt" ]; then
    echo "hash.txt not found"
    exit 1
fi

if [ ! -f "wordlist.txt" ]; then
	wget https://github.com/danielmiessler/SecLists/raw/refs/heads/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt -O wordlist.txt
fi

hashcat -D 1 -o cracked.txt hash.txt wordlist.txt --force
