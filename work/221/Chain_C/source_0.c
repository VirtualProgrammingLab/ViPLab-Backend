#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// declaration of function to be called
void foo(void);
void writeVGF(const char *  fn, const char *  str)
{
  FILE *  f = fopen(fn, "w");
  int err = 0;
  if (f == 0) {
    exit(1);
  }
  fprintf(f, "%s", str);
  err = fclose(f);
  if (err) {
    exit(1);
  }
}

/* Template */

void foo(void)
{
  /* foo code */
  printf("foo()");
writeVGF("./vipplot.vgf", "# first\n");
writeVGF("./vipplot.vgf3", "# second\n");
writeVGF("./vipplot.vgfc", "# third\n");
}
/* Main */
int main(int argc, char** argv)
{
  foo();
  return 0;
}
