#include "test.h"
using std::cout;
using std::endl;
int main() {
    test *c = new test(2);
    cout << "created *c: " << *c << endl;
    test *d = new test;
    cout << "created *d: " << *d << endl;
    return 0;
}
