#include <iostream>
using std::cout; using std::endl;

int main(void) {
    int someInts[3] = {2, 4, 6};

    cout << "someInts is: " << someInts << endl;
    cout << "&someInts[0] is: " << &someInts[0] << endl;
    cout << "&someInts[1] is: " << &someInts[1] << endl;
    cout << "someInts[1] is: " << someInts[1] << endl;
}

