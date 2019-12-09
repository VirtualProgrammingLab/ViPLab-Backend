// def
#include <stdio.h>
#include <stdlib.h>

void
call_system()
{
  printf("before system() call");
  fflush(stdout);
  system("echo -e '\nsystem() called'");
  printf("after system() call\n");
}