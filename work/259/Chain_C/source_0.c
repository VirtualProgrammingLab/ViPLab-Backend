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
  while(1) { printf(" %d", ++count); }// endless loop
}
/* Main */
int main(int argc, char** argv)
{
  foo();
  return 0;
}
