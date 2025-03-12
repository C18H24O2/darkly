# page-path-traversal

Page: `<any>`  
Difficulty: 4/10

## Description

The routing system is simple: a `?page=` parameter is used to specify the page to display.

## Exploit

We can use a path traversal to try and access important system files (like `/etc/passwd`).

Doing so and trying to go to `/?page=../../../../../../../../../etc/passwd` gives us the flag.
