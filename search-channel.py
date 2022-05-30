import search_m
from random import randint
from bs4 import BeautifulSoup
from pyfzf.pyfzf import FzfPrompt
import os
from transliterate import slugify
from plumbum.commands import ProcessExecutionError

try:
    search_m.clean()

    global endfile
    global sel
    global nsel
    global num
    global vilink
    stc = 0

    fzf = FzfPrompt()
    search_m.check_mirror()
    search_m.start_search()

    html_main = open(".tmp/index.html", 'r')
    bs = BeautifulSoup(html_main, features='lxml')
    names = bs.find_all('div', class_="flex-left")
    for name in names:
        for a in bs.find_all('a'):
            watchlnk = a['href']
            if watchlnk[:7] == 'channel' or watchlnk[:8] == '/channel':
                lnklst = open(".tmp/links.txt", 'a')
                lnklst.write(f'{watchlnk}\n')
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
    with open('.tmp/chanlist.txt', 'r') as chs:
        global num
        shc = chs.read().splitlines()
        sel = fzf.prompt(shc)
        nsel = sel[0]
        num = shc.index(nsel)
    with open('.tmp/links.txt', 'r') as chan:
        nch = chan.read().splitlines()
        vilink = nch[num]
    vilink = vilink.strip('\n')
    vilink = "".join(vilink)

    if search_m.has_cyrillic(nsel):
        namefile = slugify(nsel)
    else:
        namefile = nsel

    selectt = ['Share link', 'Add Channel']
    lse = fzf.prompt(selectt)
    lsw = ", ".join(lse)

    if lsw == 'Add Channel':
        if os.path.exists(f"channel/{namefile}.py"):
            while true:
                randum = randint(10, 99)
                finame = namefile + str(randum) + ".py"
                if not os.path.exists(f"channels/{finame}"):
                    os.system(f"touch channels/{finame}")
                    endfile = finame
                    break
                else:
                    continue
        else:
            os.system(f"touch channels/{namefile}.py")

        os.system(f"echo \"import excode\" > channels/{namefile}.py")
        os.system(f"echo \"\nexcode.main(\'{vilink}\', \'{nsel}\')\" >> channels/{namefile}.py")
        if not os.path.exists("config/channels.txt"):
            os.system("touch config/channels.txt")
        if not os.path.exists("config/scripts.txt"):
            os.system("touch config/scripts.txt")
        with open("config/channels.txt", 'a') as wrt:
            wrt.write(f"\n{nsel}")
            wrt.close()
        with open("config/scripts.txt", 'a') as trw:
            trw.write(f'\n{namefile}.py')
            trw.close()
        os.system("rm -rf channels/\{namefile\}.py")
    elif lsw == 'Share link':
        os.system("clear")
        print(vilink)
except ProcessExecutionError:
    os.system('python3 bin/search-channel.py')
