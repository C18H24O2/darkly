# value-validation

Page: `/index.php?page=survey`  
Difficulty: 2/10

## Description

The survey page has a form from which we can submit user ratings and update them.

## Exploit

The issue is that those ratings are provided by the client-side page data, and not by the server.

This means we can replace the `10` points with `10000` and force the server to accept it. 

## Side note

To mess with the results, since there is no rate limiting, we can spam the page with whatever we want, even taking in public, and since there is no rate limiting, this will also get us the flag.
