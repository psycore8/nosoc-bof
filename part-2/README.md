# Buffer Overflow im 64-Bit Stack - Teil 2

Im zweiten Teil aktivieren wir das NX-Bit, welches uns vor Buffer Overflows schützen soll. Damit es spaßig bleibt, hebeln wir diesen Schutz natürlich direkt aus. Dies erreichen wir, indem der auszuführende Befehl an die libc-Funktion system() weitergeleitet wird.

https://www.nosociety.de/it-security:blog:buffer_overflow_x64-2

![alt text](https://www.nosociety.de/_media/it-security:blog:bof64-2.jpg "Logo Title Text 1")
