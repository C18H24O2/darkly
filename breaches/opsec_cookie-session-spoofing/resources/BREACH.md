# cookie-session-spoofing

Page: `<any>`  
Difficulty: 2/10

## Description

The site uses a cookie (`I_am_admin`) to store whether the user is an administrator or not.

## Exploit

The value of the cookie is just the md5 hash of a boolean value (`true` or `false` md5'd).

We can just put `true` (`b326b5062b2f0e69046810717534cb09`) and get the flag.
