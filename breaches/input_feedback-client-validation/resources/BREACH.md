# feedback-client-validation 

Page: `/?page=feedback`  
Difficulty: bugged/10

## Description

There is a feedback form needing both a non-empty name and a non-empty message.

## Exploit 1?

The validation is only client-sided, so you can remove the JavaScript verification code?

## Exploit 2?

The site doesn't seem to do any HTML tag escaping, so you can name yourself `<i>Coucou</i>` and have an italic name???

## What.

honnête j'ai pas compris la

Putting `a`, `i`, `script` in the name field gives us the flag, which kinda makes sense if it was about HTML tag escaping, but then why doesn't it need the brackets `<>`????

Also `e` works too. Actually, let me test something.

Edit: `aceilprst` all work???????????????????????????????????????? 42 fix your shit plz.

## Fun fact of the day

Putting `<svg/onloa` in the name field gives the message a big ass forehead :D
