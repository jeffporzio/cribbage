#include <iostream>
#include <experimental/generator>
 
using namespace std::experimental; 
using namespace std; 
 
generator<int> fib() 
{ 
 &n
bsp;  int a = 0; 
    int b = 1; 
    for (;;) { 
        __yield_value a; 
        auto next = a + b; 
        a = b; 
        b = next; 
    } 
} 
 
int _tmain(int argc, _TCHAR* argv[]) 
{ 
    for (v : fib()) { 
        if (v > 50) 
            break; 
        cout << v << endl; 
    } 
}