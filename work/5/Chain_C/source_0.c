/* This program creates childs. */
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  int child_id;
  int childCount = 0;
  fprintf(stderr, "Starting forks...\n");

  for (int i = 0; i < 10; ++i) {
    child_id = fork();
    if (child_id < 0) {
      fprintf(stderr, "Parent %d: fork failed! Sleeping awhile...\n", getpid());
      sleep(3);
      fprintf(stderr, "Parent %d: ...exiting.\n", getpid());
      exit(1);
    } else if (child_id) {
      ++childCount;
      fprintf(stderr, "Parent %d with created child %d, childCount %d.\n", getpid(), child_id, childCount);
    } else {
      fprintf(stderr, "Child %d: sleeping awhile...\n", getpid());
      sleep(300);
      fprintf(stderr, "Child %d: ...exiting.\n", getpid());
      exit(0);
    }
  }
  fprintf(stderr, "...finishing forks; sleeping awhile...\n");
  sleep(3);
  fprintf(stderr, "Parent %d: ...exiting.\n", getpid());
  return 0;
}
