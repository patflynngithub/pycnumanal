/* Gives O(n^2) timing */

/*
   - used gcc compiler

         gcc -o nsquared_timing nsquared_timing.c -std=gnu99 -lm
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main( int argc, char *argv[]) {

    // get vector (array) size from command line argument
    int n = atoi(argv[1]);

    float timing = n*n;  // n^2 timing

    printf("%f\n", timing);
}

