#ifndef HEADER_H
#define HEADER_H

#include <stdio.h>

#define PRINT printf

extern double sin(double arg);
extern double cos(double arg);

double inline error(double arg)
{
	return 1.0 - sin(arg)*sin(arg) - cos(arg) * cos(arg);
}
#endif 
