# image-upload-sanitization

Page: `/index.php?page=upload`  
Difficulty: 8/10

## Description

A file upload form allows us to upload an image, but the server seems to only accept `jpg` files.

## Exploit

We can custom craft an upload POST request with `curl` to upload any file we want, and spoof its `content-type` to be `image/jpeg`, which the server will trust and accept.
