void foo(); /* decl */

int main(int argc, char* argv[])
{
  foo();
  return 0 // missing ';' -> compile error
}
