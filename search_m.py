import os
import re
import sys
import requests
from urllib.parse import quote

def clean():
    os.system("echo > .tmp/list.txt && echo > .tmp/chanlist.txt && echo > .tmp/video.txt && echo > .tmp/links.txt")

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def start_search():
    print("Search")
    search = input()
    rusfix = has_cyrillic(search)

    if rusfix:
        search = quote(search)
    else:
        for letter in search:
            if letter == ' ':
                search = search.replace(' ', '+')
    global site
    with open("config/.mirror") as conf:
        site = conf.read()
    os.system(f"curl https://{site}/search?q={search} > .tmp/index.html")

def check_mirror():
    if os.path.exists('config/.mirror'):
        with open('config/.mirror') as f:
            mirror = f.read()
            try:
                responce = requests.get(f'https://{mirror}')
            except (TimeoutError, requests.ConnectionError):
                sys.exit(f"Internet isnt working or you can't connect to mirror: {mirror}")
    else:
        sys.exit("Please, configure your mirror!")
