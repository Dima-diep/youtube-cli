from bs4 import BeautifulSoup
import os
import requests
from pyfzf.pyfzf import FzfPrompt
import sys
from plumbum.commands import ProcessExecutionError

def parse(filename, channelname, channel):
        html_main = open(f".tmp/{filename}", 'r')
        bs = BeautifulSoup(html_main, features='lxml')
        names = bs.find_all('div', class_="pure-g")
        for name in names:
            for a in bs.find_all('a', href=True):
                watchlnk = a['href'][:6]
                if watchlnk == "/watch":
                    prlink = a.get('href')
                    if prlink[-8:] == "listen=1":
                        pass
                    else:
                        written = f"https://youtube.com{prlink}"
                        with open(".tmp/llist.txt", 'r') as wl:
                            filelink = wl.read()
                            if written not in filelink:
                                wl.close()
                                with open(".tmp/llist.txt", 'a') as lw:
                                    lw.write(f"{written}\n")
                                    lw.close()
            for p in bs.find_all('p', {'dir': 'auto'}):
                if p.text == channelname:
                    pass
                elif p.text[-5:] == 'views':
                    pass
                elif p.text[:6] == 'Shared':
                    pass
                elif p.text[-4:] == 'view':
                    pass
                else:
                    writtes = p.string
                    with open(".tmp/vlist.txt", 'r') as vl:
                        filechan = vl.read()
                        if str(writtes) not in filechan:
                            vl.close()
                            with open(".tmp/vlist.txt", 'a') as lv:
                                lv.write(f"{writtes}\n")
                                lv.close()

def main(linker, namer):
    try:
        if os.path.exists('config/.mirror'):
            try:
                global mirror
                with open('config/.mirror') as ff:
                    mirror = ff.read()
                responce = requests.get(f"https://{mirror}")
            except (TimeoutError, requests.ConnectionError):
                sys.exit(f"Internet isn't working or you can't connect to mirror: {mirror}")
        else:
            sys.exit("Please configure your mirror!")

        os.system("echo > .tmp/llist.txt && echo > .tmp/vlist.txt")
        fzf = FzfPrompt()
        channel = f"https://{mirror}{linker}"
        channelname = namer
        os.system(f"curl {channel} > .tmp/index.html")
        page = 2
        while page > 1:
            os.system(f"curl {channel}?page={page} > .tmp/index{page}.html")
            page += 1
            if page == 6:
                break
        filelist = ['index.html', 'index2.html', 'index3.html', 'index4.html', 'index5.html']
        for element in filelist:
            parse(element, channelname, channel)
        with open(".tmp/vlist.txt", 'rt') as sv:
            global num
            global e
            e = sv.read().splitlines()
        if e == "":
            print("There is an error or channel is blocked!")
        else:
            e.pop(2) # Remove None
            e.pop(0)
            selec = fzf.prompt(e)
            nsele = selec[0]
            num = e.index(nsele)
            with open(".tmp/llist.txt", 'rt') as sv:
                global link
                e = sv.read().splitlines()
                e.pop(0)
                link = e[num]
            menusel = ['Play it (Linux)', 'Download video', 'Download audio', 'Play audio in Termux', 'Play video in Termux VNC', 'Share Link']
            getvideo = fzf.prompt(menusel)
            getvid = ", ".join(getvideo)

            if getvid == "Play it (Linux)" or getvid == "Play audio in Termux":
                os.system(f"mpv {link}")
            elif getvid == "Download video":
                os.system(f"cd Video && yt-dlp {link} && cd ..")
            elif getvid == "Download audio":
                os.system(f"cd Audio && yt-dlp -x {link} && cd ..")
            elif getvid == "Play video in Termux VNC":
                print("Write DISPLAY. ex. :1")
                disp = input()
                os.system(f"env DISPLAY={disp} mpv -vo=x11 {vilink}")
            elif getvid == 'Share Link':
                os.system("clear")
                print(link)
    except ProcessExecutionError:
        os.system("python3 bin/channel.py")
