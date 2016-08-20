/* Gives O(nlogn) timing */

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

