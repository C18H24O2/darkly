#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import argparse
import atexit
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, Future
from html.parser import HTMLParser
import mimetypes
import os
import threading
import urllib
import urllib.request

verbose = False


def log(msg: str) -> None:
    print(f"({threading.current_thread().name}) {msg}")


def debug(msg: str) -> None:
    if verbose:
        log(f"[debug] {msg}")


def print_path(path: list[str]) -> None:
    log("Path:")
    for i, p in enumerate(path):
        if i == 0:
            log(f"  {p}")
        else:
            log(("  " * (i)) + f"-> {p}")


target_tags = ['a', 'img', 'source', 'link', 'iframe', 'script', 'video', 'audio', 'track', 'embed']
target_protocols = ['http', 'https', 'ftp', 'file']
class LinkExtractor(HTMLParser):
    __links: set[str]
    __orig_url: str

    def __init__(self, orig_url: str) -> None:
        super().__init__()
        self.__links = set()
        self.__orig_url = orig_url

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == 'a':
            for (name, value) in attrs:
                if name == 'href':
                    self.__links.add(value)
                    break
        elif tag in target_tags:
            for (name, value) in attrs:
                if name == 'src':
                    self.__links.add(value)
                    break
        super().handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        for proto in target_protocols:
            if data.startswith(proto + '://'):
                self.__links.add(data)
        super().handle_data(data)

    def get_links(self) -> list[str]:
        return [urllib.parse.urljoin(self.__orig_url, link) for link in self.__links]


def get_links(html: str, orig: str) -> list[str]:
    parser = LinkExtractor(orig)
    parser.feed(html)
    return parser.get_links()


user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'
html_types = ['text/html', 'application/xhtml+xml', 'application/xml']
target_types = [] # populated in main

def crawl(url: str, level: int, extensions: list, output_path: str, exec_pool: ThreadPoolExecutor, futures: list[Future], visited_urls: set[str] = set(), path: list[str] = []) -> None:
    #DARKLY: hook
    if "/" not in url:
        return
    if ".hidden/" not in url:
        return
    #DARKLY: end hook

    if url in visited_urls:
        debug(f"Already visited {url}, skipping")
        return
    visited_urls.add(url)

    try:
        debug(f"Making request to {url}")
        req = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as response:
            debug(f"Got response from {url}")

            headers = response.getheaders()
            charset = ''
            state = 0 # 0 -> unknown, 1 -> html, 2 -> downloadable

            for (name, value) in headers:
                if name.lower() == 'content-type':
                    options = [x.strip() for x in value.split(';')]
                    mime_type = options[0]
                    if mime_type in html_types:
                        state = 1
                    for opt in options:
                        if '=' not in opt: continue
                        (key, val) = opt.split('=')
                        if key.lower() == 'charset':
                            charset = val
                            break
                    else:
                        continue
                    break

            #DARKLY: hook
            if mime_type == "application/octet-stream":
                data = response.read()
                if charset == '':
                    charset = 'utf-8'
                decoded = data.decode(charset)
                if "voisin" in decoded or "aide" in decoded or "oujours" in decoded: #bordel
                    return
                path.append(url)
                print_path(path)
                path.pop()
                print(f"Got data:", decoded.strip())
                exit(1)
                return
            #DARKLY: end hook

            data: bytes = b''
            if state == 0:
                try:
                    debug(f"No content-type found in headers, trying to detect via external library")
                    import magic
                    data = response.read()
                    if data is None or len(data) == 0:
                        raise ValueError("No data received")
                    mime_type = magic.from_buffer(data, mime=True)
                    if mime_type is None:
                        raise ValueError("No mime type found")
                    if mime_type in html_types:
                        debug(f"Got content-type '{mime_type}', assuming downloadable")
                        state = 2
                except Exception as e:
                    log(f"Failed to detect mime type: {e}")
                except ImportError:
                    debug(f"Failed to import magic library, erroring out")
                if state == 0:
                    debug(f"No content-type found in headers, skipping...")
                    return

            if state == 1 and level == 0:
                debug("Found HTML but crawling is at the maximum depth, skipping...")
                return

            if len(data) == 0:
                data = response.read()
            if data is None or len(data) == 0:
                raise ValueError("No data received")

            if state == 2:
                log(f"Downloaded {url}")
                path.append(url)
                print_path(path)
                path.pop()
                name = os.path.basename(url)
                if name is None or len(name) == 0:
                    ext = mimetypes.guess_extension(mime_type)
                    if ext is None or len(ext) == 0:
                        ext = ''
                    else:
                        ext = '.' + ext
                    name = f"download-{str(uuid.uuid4())}{ext}"
                target_path = os.path.join(output_path, name)
                os.makedirs(output_path, exist_ok=True)
                debug(f"Writing to {target_path}")
                try:
                    with open(target_path, 'wb') as f:
                        f.write(data)
                except Exception as e:
                    log(f"Failed to write file '{name}': {e}")
                return

            if charset == '':
                charset = 'utf-8'
                debug(f"No charset found in headers, using default {charset}")
                
            debug(f"Got HTML response from {url}")
            
            debug(f"Decoding data with charset '{charset}'")
            html: str = data.decode(charset)

            links: list[str] = []
            try:
                links = get_links(html, url)
                debug(f"Got {len(links)} links: {links}")
            except Exception as e:
                raise ValueError(f"Failed to parse links: {e}")
            for link in links:
                for proto in target_protocols:
                    if link.startswith(proto + '://'):
                        if level != 0:
                            debug("CRAWLING???")
                            debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(type(futures)))
                            path.append(url)
                            futures.append(exec_pool.submit(crawl, link, level - 1, extensions, output_path, exec_pool, futures, visited_urls, [*path]))
                            path.pop()
                            debug("CRAWLING!!!")
                        break
    except Exception as e:
        pass
        #log(f"Error while crawling {url}: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='spider', description='A little web crawling program, fetches images from a given website.')
    parser.add_argument('url', help='the url to crawl')
    parser.add_argument('-e', '--extension', default=['jpg', 'png', 'jpeg', 'gif', 'bmp'], help='the extensions to look for', action='append')
    parser.add_argument('-l', '--level', type=int, default=5, help='the depth of the crawl, -1 for infinite')
    parser.add_argument('-p', '--path', default='data', help='the path to store the images')
    parser.add_argument('-r', '--recursive', action='store_true', help='crawl recursively')
    parser.add_argument('-t', '--threads', type=int, default=4, help='the number of threads to use')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')

    args = parser.parse_args()

    extensions = args.extension
    url = args.url
    recursive = args.recursive
    level = args.level
    if not recursive:
        level = 1
    elif level >= 0:
        level += 1 # add one for the initial crawl
    output_path = args.path
    threads = args.threads
    verbose = args.verbose

    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            raise ValueError("Invalid URL scheme, must be http or https")
        if parsed.netloc == '':
            raise ValueError("Invalid URL, must contain a domain name")
        debug(f"Parsed URL {url} into {parsed}")
    except ValueError as e:
        log(f"Provided URL ({url}) is invalid", e)
        exit(1)

    debug(f"Populating target types (from {extensions})")
    target_types = [mimetypes.guess_type(f"test.{ext}")[0] for ext in extensions]
    debug(f"Target types: {target_types}")

    debug(f"Launching ThreadPoolExecutor with {threads} threads")
    with ThreadPoolExecutor(max_workers=threads) as exec_pool:
        futures = []
        futures.append(exec_pool.submit(crawl, url, level, extensions, output_path, exec_pool, futures))

        time.sleep(10000)
        while len(futures) > 0:
            done, _ = wait(futures, return_when=FIRST_COMPLETED)
            futures = [f for f in futures if not f.done()]
    log("Done")
