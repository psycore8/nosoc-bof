# Buffer Overflow im 64-Bit Stack - Part 2

In the second part, we activate the NX bit, which is intended to protect us from buffer overflows. To keep things fun, we will of course override this protection directly. We achieve this by passing the command to be executed to the libc-Funktion system() is forwarded. 

🇩🇪 https://www.nosociety.de/it-security:blog:buffer_overflow_x64-2

🇺🇸 https://www.nosociety.de/en:it-security:blog:buffer_overflow_x64-2

![alt Debugger](https://www.nosociety.de/_media/it-security:blog:bof64-2.jpg "Logo Title Part 1")
