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

    // 011111011010010100000110101100111010011011100011100100001110111011100101101101111110010011101001011000101010100010111101000111100
}