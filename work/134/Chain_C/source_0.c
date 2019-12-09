#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// declaration of function to be called
void foo(void);
/* Template */

void foo(void)
{
  /* your code */
  int count=0;
  printf(" M%crz ", (char)0xe4); // illegal UTF8 char
}
/* Main */
int main(int argc, char** argv)
{
  foo();
  return 0;
}
