#include "timing.h"
#include <stdio.h>

#define N 1024

#define MEMORY_BARRIER // asm("":::"memory")

unsigned array[N][N];

unsigned goodLocalityVersion() {
    for ( int i = 0; i < N; i++ )
        for ( int j = 0; j < N; j++ ) {
            MEMORY_BARRIER;
            array[i][j] = 0;
        }
    for ( int c = 0; c < N; c++ )
        for ( int i = 0; i < N; i++ )
            for ( int j = 0; j < N; j++ ) {
                MEMORY_BARRIER;
                array[i][j]++;
            }
    unsigned sum = 0;
    for ( int i = 0; i < N; i++ )
        for ( int j = 0; j < N; j++ ){
            MEMORY_BARRIER;
            sum += array[i][j];
        }
    return sum;
}

unsigned badLocalityVersion() {
    for ( int j = 0; j < N; j++ )
        for ( int i = 0; i < N; i++ ) {
            MEMORY_BARRIER;
            array[i][j] = 0;
        }
    for ( int c = 0; c < N; c++ )
        for ( int j = 0; j < N; j++ )
            for ( int i = 0; i < N; i++ ) {
                MEMORY_BARRIER;
                array[i][j]++;
            }
    unsigned sum = 0;
    for ( int j = 0; j < N; j++ )
        for ( int i = 0; i < N; i++ ) {
            MEMORY_BARRIER;
            sum += array[i][j];
        }

    return sum;
}

double time_one(unsigned (*func)(void)) {
    cycles_type total_time = measure_function(0, (generic_function_type) func, 0, 0);
    return total_time / (double) (2.6e9);
}

int main() {
    printf("good locality: %6.2f\n", time_one(goodLocalityVersion));
    printf("bad locality:  %6.2f\n", time_one(badLocalityVersion));
}

