#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// declaration of function to be called
void foo(void);
/* Template */

void foo(void)
{
  /* your code */
  printf("foo()");
  exit(2);
}
/* Main */
int main(int argc, char** argv)
{
  foo();
  return 0;
}
