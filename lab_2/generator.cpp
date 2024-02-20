#include <iostream>
#include <random>
#include <ctime>

#define MAX_BIT 128

using namespace std;

int generator()
{
    srand(time(0));
    for (int i = 0; i < MAX_BIT; ++i)
    {
        unsigned long long rand_num = rand() % 32767;
        bool binary_num = rand_num % 2;
        cout << binary_num;
    }
    return 0;
}

int main()
{
    cout << generator();
}