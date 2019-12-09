#include <iostream>
void foo()
{
  int i; // unused var -> compile warning
  std::cout << "Hello World!" << std::endl;
}
