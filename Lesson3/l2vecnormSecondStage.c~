/* Compute l2 vector norm */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main( int argc, char *argv[]) {

    // get vector (array) size from command line argument
    int n = atoi(argv[1]);

    // create the vector (array)
    double u[n];

    // initialize the vector (array) by setting first entry to 0
    // and incrementing by 1 from there
    for (int i = 0; i < n; ++i) {
        u[i] = i;
    }

    /*
    // for testing: display vector (array) contents
    for (int i = 0; i < n; ++i) {
        printf("%f  ", u[i]);
    }
    printf("\n");
    */

    // compute l2-norm of vector (array)
    double accum = 0.;
    for (int i = 0; i < n; ++i) {
        accum += u[i] * u[i];
    }
    double norm = sqrt(accum);

    // output l2-norm
    printf("%f\n", norm);

}

