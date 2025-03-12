# find-me

Page: `/.hidden/`  
Difficulty: 3/10

## Description

In `robots.txt`, we find the `.hidden/` directory, which has a lot of folders in which the flag must be hidden.

## Exploit

Check everything. that's it. :3

Ideally the target file must have a reference to `"flag"`, so we search for that recursively with a script. For instance, I've used a modified version of `spider.py` from [Cybersecurity - arachnida](https://projects.intra.42.fr/projects/cybersecurity-arachnida-web).

We can just run the script with the url and a shit ton of threads, and wait.
```bash
./bourrin.py -r -t 32 http://10.13.248.94/.hidden/
```
