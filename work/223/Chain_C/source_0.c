#include <complex.h>
#include <stdio.h>
int main(void)
{
  double complex c = 5 + 3*I;
  printf("%g + %gi\n", creal(c), cimag(c));
  complex * cP = &c;
  printf("%g + %gi\n", creal(*cP), cimag(*cP));

  return 0;
}
