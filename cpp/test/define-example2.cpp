#ifndef FOO
if shown after preprocessing:
foo not defined first time
#endif
#define FOO
#ifndef FOO
if shown after preprocessing:
foo not defined second time
#endif
