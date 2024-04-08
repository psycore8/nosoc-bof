https://www.nosociety.de/it-security:blog:buffer_overflow_x64

Im zweiten Teil aktivieren wir das NX-Bit, welches uns vor Buffer Overflows schützen soll. Damit es spaßig bleibt, hebeln wir diesen Schutz natürlich direkt aus. Dies erreichen wir, indem der auszuführende Befehl an die libc-Funktion system() weitergeleitet wird
