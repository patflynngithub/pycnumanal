/* Gives O(nlogn) timing */

/*
   - used gcc compiler

         gcc -o nlogn_timing nlogn_timing.c -std=gnu99 -lm
*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main( int argc, char *argv[]) {

    // get vector (array) size from command line argument
    int n = atoi(argv[1]);

    float timing = n*log(n);  // nlogn timing

    printf("%f\n", timing);
}

