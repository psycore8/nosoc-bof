// code from https://blog.techorganic.com/2015/04/10/64-bit-linux-stack-smashing-tutorial-part-1/
 
#include <stdio.h>
#include <unistd.h>
 
int vuln() {
    char buf[80];
    int r;
    r = read(0, buf, 400);
    printf("\nRead %d bytes. buf is %s\n", r, buf);
    puts("No shell for you :(");
    return 0;
}
 
int main(int argc, char *argv[]) {
    printf("Try to exec /bin/sh");
    vuln();
    return 0;
}