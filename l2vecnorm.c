/* l2 vector norm */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main( int argc, char *argv[]) {

    int n = atoi(argv[1]);
    double u[n];

    // initialize
    for (int i = 0; i < n; ++i) {
        u[i] = i;
    }

    // l2-norm
    double accum = 0.;
    for (int i = 0; i < n; ++i) {
        accum += u[i] * u[i];
    }
    double norm = sqrt(accum);

    printf("%f\n", norm);
}

