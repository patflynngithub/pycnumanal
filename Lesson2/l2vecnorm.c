/* Compute l2 vector norm */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main( int argc, char *argv[]) {

    // get vector (array) size from command line argument
    int n = atoi(argv[1]);

    double u[n]; // create the vector (array)

    // initialize vector (array) by incrementing by 1 from 0
    for (int i = 0; i < n; ++i) {
        u[i] = i;
    }

    // compute l2-norm of vector (array)
    double accum = 0.;
    for (int i = 0; i < n; ++i) {
        accum += u[i] * u[i];
    }
    double norm = sqrt(accum);

    printf("%f\n", norm);
}

