#include "test.h"
using std::cout;
using std::endl;
int main() {
    test *c = new test(2);
    test *d = new test;
    delete c;
    return 0;
}
