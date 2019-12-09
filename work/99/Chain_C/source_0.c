#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//
// expects filename arg
int main(int argc, char** argv)
{
  if (argc < 2) {
    exit(1);
  }
  printf(argv[1]);
  FILE *  f = fopen(argv[1], "r");
  if (f == NULL) {
    return 1;
  }
  fclose(f);
  return 0;
}
/* Main could be here. */
