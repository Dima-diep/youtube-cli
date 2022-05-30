import search_m
from bs4 import BeautifulSoup
from pyfzf.pyfzf import FzfPrompt
import os
from plumbum.commands import ProcessExecutionError

try:
    stc = 0

    fzf = FzfPrompt()
    search_m.clean()
    search_m.check_mirror()
    search_m.start_search()
    html_main = open(".tmp/index.html", 'r')
    bs = BeautifulSoup(html_main, features='lxml')
    names = bs.find_all('div', class_="h-box")
    for name in names:
        for a in bs.find_all('a'):
            watchlnk = a['href']
            if watchlnk[:6] == '/watch' and watchlnk[-8:] != 'listen=1':
                lnklst = open(".tmp/links.txt", 'a')
                lnklst.write(f'https://youtube.com{watchlnk}\n')
            else:
                pass
        for p in bs.find_all('p', {'dir': 'auto'}):
            if p.text[-5:] == 'views':
                pass
            elif p.text[:6] == 'Shared':
                pass
            elif p.text[-4:] == 'view':
                pass
            else:
                with open('.tmp/list.txt', 'a') as sea:
                    sea.write(f"{p.string}\n")
                    sea.close()
    
        for p in bs.find_all('p', {'class': 'channel-name', 'dir': 'auto'}):
            with open('.tmp/chanlist.txt', 'a') as chn:
                chn.write(f"{p.string}\n")
                chn.close()
    with open('.tmp/chanlist.txt', 'r') as f:
        bad_lines = set(f.readlines())

    with open('.tmp/list.txt', 'r') as f:
        for line in f.readlines():
            if not line in bad_lines:
                wrt = open('.tmp/video.txt', 'a')
                wrt.write(line)
    with open('.tmp/video.txt', 'r') as selection:
        global num
        gsc = selection.read().splitlines()
        selec = fzf.prompt(gsc)
        nsele = selec[0]
        num = gsc.index(nsele)
    with open('.tmp/links.txt', 'r') as linkd:
        global vilink
        lkd = linkd.read().splitlines()
        vilink = lkd[num]
    menusel = ['Play it (Linux)', 'Download video', 'Download audio', 'Play audio in Termux', 'Play video in Termux VNC', 'Share Link']
    getvideo = fzf.prompt(menusel)
    getvid = ", ".join(getvideo)

    if getvid == "Play it (Linux)" or getvid == "Play audio in Termux":
        os.system(f"mpv {vilink}")
    elif getvid == "Download video":
        os.system(f"cd Video && yt-dlp {vilink} && cd ..")
    elif getvid == "Download audio":
        os.system(f"cd Audio && yt-dlp -x {vilink} && cd ..")
    elif getvid == "Play video in Termux VNC":
        print("Write DISPLAY. ex. :1")
        disp = input()
        os.system(f"env DISPLAY={disp} mpv -vo=x11 {vilink}")
    elif getvid == 'Share Link':
        os.system("clear")
        print(vilink)
except ProcessExecutionError:
    os.system('python3 bin/search.py')
