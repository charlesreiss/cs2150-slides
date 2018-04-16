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

void setup(int size) {
    for (unsigned i = 0; i < size; ++i) {
#ifdef USE_AVX
        array[i] = _mm256_set1_epi32(((i + 1) * 103) % size);
#else
        array[i] = ((i + 1) * 103) % size;
#endif
    }
}

unsigned run_chase(int size) {
    unsigned i = 0;
    for (int j = 0; j < size * 4; ++j) {
#ifdef USE_AVX
        i = _mm256_extract_epi32(array[i], 0);
#else
        i = array[i];
#endif
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
    for (int i = 256; i <= MAX_SIZE; i *= 2) {
        setup(i);
        printf("%ld,%.3f,%.3f,%.3f\n", i * sizeof(TYPE), time_one(i), time_one(i), time_one(i));
    }
}
