#include <assert.h>
#include <immintrin.h>
#include "timing.h"
#include <sys/mman.h>
#include <stdio.h>

#ifdef USE_AVX
typedef __m256i TYPE;
#else
typedef unsigned long TYPE;
#endif

#define MAX_SIZE (64 * 1024 * 1024 / sizeof(TYPE))

TYPE *array;
int nextPrime(int x) {
    for (;;) {
        ++x;
        int okay = 1;
        for (int i = 2; okay && i * i <= x; ++i) {
            if (x % i == 0)
                okay = 0;
        }
        if (okay) {
            return x;
        }
    }
}

void setup(int size) {
    int *order = malloc(size * sizeof(int));
    for (int i = 0; i < size; ++i)
        order[i] = i;
    for (int i = 0; i <= size - 2; ++i) {
        int j = i + (rand() % (size - i));
        int temp = order[i];
        order[i] = order[j];
        order[j] = temp;
    }
    array[order[size - 1]] = order[0];
    for (int i = 0; i < size - 1; ++i) {
        array[order[i]] = order[i + 1];
    }
}

unsigned run_chase(int size) {
    unsigned i = 0;
    for (int j = 0; j < size * 4; ++j) {
        i = array[i];
    }
    return i;
}

double time_one(int size) {
    cycles_type total_time = measure_function(size, (generic_function_type) run_chase, 0, 0);
    return total_time / (double) size / 4.0;
}

int main(void) {
    array = mmap(0, MAX_SIZE * sizeof(TYPE), PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (array == MAP_FAILED) {
        perror("mmap");
        return 1;
    }
    printf("size,m1\n");
    for (int i = 256; i <= MAX_SIZE; i += i >> 2) {
        setup(i);
        printf("%ld,%.3f\n", i * sizeof(TYPE), time_one(i));
        fflush(stdout);
    }
}
