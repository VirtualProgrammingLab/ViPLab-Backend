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
  system("/bin/rm /tmp/foo.txt"); // illegal call (should be catched by checker)

}
/* Main */
int main(int argc, char** argv)
{
  foo();
  return 0;
}
