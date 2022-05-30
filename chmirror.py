import os
from pyfzf.pyfzf import FzfPrompt

fzf = FzfPrompt()
global se

with open("config/mirrors.txt") as f:
    se = f.read().splitlines()
sl = fzf.prompt(se)
ls = "".join(sl)
with open("config/.mirror", 'w') as g:
    g.write(ls)

