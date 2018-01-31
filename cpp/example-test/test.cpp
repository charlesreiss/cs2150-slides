#include "test.h"
#include <iostream>
using std::cout;
using std::ostream;
using std::endl;

int test::idcount = 0;

test::test() : id (idcount++), value(0) {
    cout << "calling test(); object created is " << *this << endl;
}

test::test(int v) : id (idcount++), value(v) {
    cout << "calling test(" << v << "); object created is " << *this << endl;
}

test::test(const test& x) : id(x.id), value(x.value) {
    cout << "calling test(" << x <<"); object created is " << *this << endl;
}

test::~test() {
    cout << "calling ~test() on " << *this << endl;
}

test& test::operator=(const test& other) {
    cout << "calling operator=(" << other << ")" << endl;
    return *this;
}

ostream& operator<<(ostream& out, const test& f) {
    out << "test[id=" << f.id << ",v=" << f.value << "]@" << &f;
    return out;
}
