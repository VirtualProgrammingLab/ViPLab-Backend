#include "header.h"

static const double pi = 3.1415926;
int main(int argc,char **argv)
{
int i;

	for(i = 0;i<256;i++) {
		double arg = i * pi / 256.0;
		PRINT("%g\t:\t%g\n",arg,error(arg));
	}
	return 0;
}
