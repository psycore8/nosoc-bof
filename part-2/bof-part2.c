/* Code https://blog.techorganic.com/2015/04/21/64-bit-linux-stack-smashing-tutorial-part-2/ */
/* Mod
/* Compile: gcc -fno-stack-protector -no-pie bof-part2.c -o bof-part2      */
/* Disable ASLR: echo 0 > /proc/sys/kernel/randomize_va_space     */

#include <stdio.h>
#include <unistd.h>

int gadg() {
 asm ("pop %rdi");
 asm ("ret");
 return 0;
}

int vuln() {
    char buf[80];
    int r;
    r = read(0, buf, 400);
    printf("\nRead %d bytes. buf is %s\n", r, buf);
    puts("No shell for you :(");
    return 0;
}

int main(int argc, char *argv[]) {
    setuid(0);
    seteuid(0);
    printf("Try to exec /bin/zsh --interactive");
    vuln();
    return 0;
}
