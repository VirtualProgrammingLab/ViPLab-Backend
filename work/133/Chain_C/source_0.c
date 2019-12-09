#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// declaration of function to be called
void foo(void);
void foo(void)
{
  const char *  fn = "../foo.txt";
  FILE *  f = fopen(fn, "w");
  if (f == NULL) { exit(1); }
  printf("foo()");
  fclose(f);
}
/* Main */
int main(int argc, char** argv)
{
  foo();
  return 0;
}
