#include "stdio.h"

union data {
    char word[8];
    unsigned long long int bytes;
};

int main(int argc, char *argv[])
{
    union data d;
    d.bytes = "Hello \n";
    unsigned long long int mask = 1;
    mask = mask << 58;
    size_t size = sizeof(mask);
    printf("Size: %zu\n", size);
    printf("Mask: %llu\n", mask);
    return 0;
}
