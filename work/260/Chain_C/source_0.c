#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// declaration of function to be called
void foo(void);
/* Template */

void foo(void)
{
  /* your code */
  /* endless recursion */ foo();
}
/* Main */
int main(int argc, char** argv)
{
  foo();
  return 0;
}
