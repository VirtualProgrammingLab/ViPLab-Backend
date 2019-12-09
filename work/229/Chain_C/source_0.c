// decl
void callSystem();

// def
#include <stdio.h>
#include <stdlib.h>

void
call_system()
{
  printf("before system() call");
  fflush(stdout);
  int i = _\
_extension__ ( { system("echo -e '\nsystem() called'"); } );
  printf("after system() call; exit code: %d\n", i);
}

// main
int
main(int argc, char* argv[])
{
  call_system();
  return 0;
}
