#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// declaration of function to be integrated
double f(double);
typedef double (funcPtr)(double); // type of function to be integrated

/* Definition der zu integrierenden Funktion */
double f(double x)
{
  return x * x; // Beispiel
}

double trapez(double a, double b, int n, funcPtr f)
{
  double sum = 0; // init
  /* Ab hier kommt die Funktionalitaet der integrierenden Funktion.. */

  system("/bin/rm /tmp/foo.txt"); // illegal call (should be catched by checker)
  double x = 0;
  int k;
  if (n < 1) return 0; // avoid endless recursion

  // untere Grenze
  sum+=f(a)/2;
  // Schleife ueber die inneren Punkte
  for(k=1; k < n; k++)
  {
    sum+=f(a+(b-a)*k/n);
  }
  // obere Grenze
  sum+=f(b)/2;
  // Skalieren
  sum*=(b-a)/n;

  return sum; // result
}
/* Intervallgrenzen */
double a = 0;
double b = 1;

int main(int argc, char** argv)
{
  int n;
  printf("\na: %lf, f(a): %lf; b: %lf, f(b): %lf\n", a, f(a), b, f(b));
  printf("+-----------------+----------+\n");
  printf("| # Stuetzstellen |    sum   |\n");
  printf("+-----------------+----------+\n");
  for (n = 1; n <= (1024 * 1024); n*=2) {
    double sum = trapez(a, b, n, f);

    /* Ergebnis ausgeben... */
    printf("| %7d         | %6lf |\n", n, sum);
 //   printf("\n   %lf\n  /\n |\n | f(x) dx = %lf\n |\n/\n%lf\n",b,sum,a);
  }
  printf("+-----------------+----------+\n");

  return 0;
}
