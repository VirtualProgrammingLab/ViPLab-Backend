#include <stdio.h>
void foo()
{
  int i; // unused var -> compile warning
  printf("Hello World!\n");
}
