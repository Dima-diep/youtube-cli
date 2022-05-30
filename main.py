import os
from pyfzf.pyfzf import FzfPrompt
import requests
from plumbum.commands.processes import ProcessExecutionError
import sys

fzf = FzfPrompt()

def main():
    sl = ['Channels', 'Search', 'Add Channel', 'Delete Channel', 'Change Mirror', 'Get Current Mirror', 'Add custom mirror', 'Backup subscribes', 'Restore subscribes', 'Play by link', 'Update script']
    sel = fzf.prompt(sl)
    ls = ", ".join(sel)
    run = 'python3 bin/'

    if ls == 'Channels':
        os.system(f"{run}channel.py")
    elif ls == 'Search':
        os.system(f"{run}search.py")
    elif ls == 'Add Channel':
        os.system(f"{run}search-channel.py")
    elif ls == 'Delete Channel':
        os.system(f"{run}delchan.py")
    elif ls == 'Change Mirror':
        os.system(f"{run}chmirror.py")
    elif ls == 'Get Current Mirror':
        try:
            print(f"Current mirror is: {mirror}")
        except (FileNotFoundError, NameError):
            print("There is no any mirror!")
    elif ls == 'Add custom mirror':
        print("Write mirror - without https://:")
        mirrorin = input()
        with open("config/mirrors.txt", 'a') as f:
            f.write(mirrorin)
            f.close()
    elif ls == 'Backup subscribes':
        os.system("bash bin/backup.sh")
    elif ls == 'Restore subscribes':
        os.system("bash bin/restore.sh")
    elif ls == 'Play by link':
        os.system(f"{run}linkage.py")
    elif ls == 'Update script':
        os.system("bash bin/backup.sh && mv backup.tar.gz .. && cd .. && rm -rf youtube-cli && git clone https://notabug.org/StalinKali/youtube-cli && cd youtube-cli && bash install.sh && mv ../backup.tar.gz . && echo \"Write backup.tar.gz\" && bash bin/restore.sh")

try:
    global mirror
    with open('config/.mirror') as ff:
        mirror = ff.read()
    response = requests.get(f"https://{mirror}")
    main()
except (FileNotFoundError, requests.ConnectionError, TimeoutError):
    main()
except ProcessExecutionError:
    sys.exit()
