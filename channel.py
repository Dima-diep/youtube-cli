import os
from pyfzf.pyfzf import FzfPrompt
import sys

fzf = FzfPrompt()
global se

with open('config/channels.txt') as f:
    se = f.read().splitlines()
sl = fzf.prompt(se)
ls = "".join(sl)
ind = se.index(ls)
with open('config/scripts.txt') as g:
    es = g.read().splitlines()
    script = es[int(ind)]
    os.system(f"python3 channels/{script}")
