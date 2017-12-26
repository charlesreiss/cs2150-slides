#ifndef TEST_H
#define TEST_H

#include <iostream>

class test {
    static int idcount;
    const int id;
    int value;
public:
    test();
    test(int v);
    test(const test& x);
    ~test();
    test& operator=(const test& other);
    friend std::ostream& operator<<(std::ostream& out, const test& f);
};

#endif
