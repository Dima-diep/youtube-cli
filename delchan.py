import os
from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt()
global se
global scr

with open('config/channels.txt') as f:
    se = f.read().splitlines()
sl = fzf.prompt(se)
ls = "".join(sl)
ind = se.index(ls)
os.system("touch config/channels.txt.new && touch config/scripts.txt.new")
with open('config/scripts.txt') as i:
    es = i.read().splitlines()
    script = es[int(ind)]
    scr = "".join(script)
with open('config/scripts.txt', 'r+') as j:
    with open('config/scripts.txt.new', 'w') as k:
        for line in j:
            if line != f"{scr}":
                k.write(f"{line}")
with open('config/channels.txt', 'r+') as g:
    with open('config/channels.txt.new', 'w') as h:
        for line in g:
            if line != f"{ls}":
                h.write(f"{line}")
os.system("rm -rf config/channels.txt config/scripts.txt && mv config/channels.txt.new config/channels.txt && mv config/scripts.txt.new config/scripts.txt")
os.system(f"rm -rf channels/{scr}")
