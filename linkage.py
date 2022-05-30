import os
from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt()

print("Write link:")
link = input()

menusel = ['Play it (Linux)', 'Download video', 'Download audio', 'Play audio in Termux', 'Play video in Termux VNC']
getvideo = fzf.prompt(menusel)
getvid = ", ".join(getvideo)

if getvid == "Play it (Linux)" or getvid == "Play audio in Termux":
    os.system(f"mpv {link}")
elif getvid == "Download video":
    os.system(f"cd Video && yt-dlp {link} && cd ..")
elif getvid == "Download audio":
    os.system(f"cd Audio && yt-dlp -x {link} && cd..")
elif getvid == "Play video in Termux VNC":
    print("Write DISPLAY. ex. :1")
    disp = input()
    os.system(f"env DISPLAY={disp} mpv -vo=x11 {link}")
