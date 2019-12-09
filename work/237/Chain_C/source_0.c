#include <stdio.h>

int
main(int argc, char* argv[])
{
  fputc('$', stdout);
  putc('#', stdout);
  printf("\n");
  return 0;
}
