# user-controlled-redirect

Page: `/index.php?page=redirect&site=test`  
Difficulty: 2/10

## Description

This page is a redirection page, and the "target" is controlled by the user.

## Exploit

The user can control the target and replace it via whatever they want. If it's not handled, this could reveal information or allow for other attacks like XSS.

## Side note

This... looks like a well secured page... Why is that a flag??? It's not as if the entire redirection url was in the params, it's server-controlled. i don't get you 42
