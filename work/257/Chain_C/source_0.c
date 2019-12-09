#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//
FILE *  openFile(const char *  fn)
{
  FILE *  f = fopen(fn, "w");
  if (f == 0) {
    exit(1);
  }
  return f;
}
void  closeFile(FILE *  f)
{
  int err = fclose(f);
  if (err) {
    exit(1);
  }
}
void plotMH(FILE * pf,
            double x_min, double y_min,
            double x_max, double y_max,
            int x_steps, int y_steps)
{
  double x_stepwidth = (x_max - x_min) / (x_steps - 1);
  double y_stepwidth = (y_max -y_min) / (y_steps -1);
  
  fprintf(pf, "Gridplot\n");
  fprintf(pf, "# x-range %f %f\n", x_min, x_max);
  fprintf(pf, "# y-range %f %f\n", y_min, y_max);
  fprintf(pf, "# x-count %d\n", x_steps);
  fprintf(pf, "# y-count %d\n", y_steps);
  fprintf(pf, "# scale 1 1 1\n");
  fprintf(pf, "# min-color 255 0 0\n");
  fprintf(pf, "# max-color 0 0 255\n");
  fprintf(pf, "# time 0\n");
  fprintf(pf, "# label piezometric head\n");
  for (int x_ix = 0; x_ix < x_steps; ++x_ix) {
    double x = x_min + x_ix * x_stepwidth;
    for (int y_ix = 0; y_ix < y_steps; ++y_ix) {
      double y = y_min + y_ix * y_stepwidth;
      double tmp = x*x + y*y;
      double z = tmp ? sin(tmp)/tmp : 1;
      fprintf(pf, "%f ", z);
    }
    fprintf(pf, "\n");
  } 
}

int main(int argc, char** argv)
{
  FILE * pf = openFile("vipplot.vgfc");
  double x_min = -3, x_max = +3;
  double y_min = -3, y_max = +3;
  int x_steps, y_steps;
  x_steps = y_steps = 100;
  
  plotMH(pf,
         x_min, y_min,
         x_max, y_max,
         x_steps, y_steps);
  closeFile(pf);
  return 0;
}
