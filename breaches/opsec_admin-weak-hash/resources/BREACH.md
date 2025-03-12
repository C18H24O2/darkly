# weak-hash 

Page: `/admin/`  
Difficulty: 3/10

## Description

By doing some wordlist attack, we find that `/admin/` exists, and is a password-protected page.

## Exploit

In `robots.txt`, we find the `whatever/` directory, which contains a `htpasswd` file with a `user:pass` combo.

The user is `root` and the password is md5-hashed. We can reverse the hash to be `qwerty123@`, and use those credentials to log in and get the flag.
