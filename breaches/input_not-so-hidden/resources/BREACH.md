# not-so-hidden

Page: `/index.php?page=recover`  
Difficulty: 1/10

## Description

On the "forgot password" page, there is a form.

The flag is hidden behind it, but no input is visible, and clicking submit returns an error.

## Exploit

In the source code, there is a hidden input text field with an email address (`webmaster@borntosec.com`). Replacing `webmaster` with `admin` and clicking submit gives us the flag.
