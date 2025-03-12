# bruteforce

Page: `/index.php?page=signin`  
Difficulty: 4/10

## Description

This is a simple password guessing game. Try? Fail. Try? Fail again. You get the picture.

## Exploit

The password for `admin` is `shadow`, it was bruteforced via a wordlist in a few seconds.

## How to fix

Don't use a shitty password. That's it. That's all it takes.

## Sidenote

This is maybe for the purposes of the exercise, but the password is sent in a GET request param, fully visible in the URL. Not a good idea.
