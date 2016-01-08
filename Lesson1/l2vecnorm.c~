/* l2 vector norm */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main( int argc, char *argv[]) {

    // get vector size from command line argument
    int n = atoi(argv[1]);

    double u[n];

    // initialize array
    for (int i = 0; i < n; ++i) {
        u[i] = i;
    }

    clock_t startTime = clock();

    // compute l2-norm of vector (array)
    double accum = 0.;
    for (int i = 0; i < n; ++i) {
        accum += u[i] * u[i];
    }
    double norm = sqrt(accum);

    clock_t endTime = clock();
    clock_t cpuTime = endTime - startTime;

    printf("%ld", cpuTime);
}

