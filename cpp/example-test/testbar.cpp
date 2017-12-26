#include "test.h"
using std::cout;
using std::endl;

test bar(test param) {
  return test(10);
}
int main() {
    test *c = new test(2);
    cout << "about to call bar" << endl;
    test e = bar(*c);
    cout << "done calling bar" << endl;
}
