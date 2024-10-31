#include "stdio.h"
#include "string.h"
#include "stdint.h"
#include <stdatomic.h>
#include <stdint.h>

#define ENABLE_LOG 1

union data {
    char word[8];
    uint64_t bytes;
};

const uint8_t IP[] = {58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64,
    56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13,
    5, 63, 55, 47, 39, 31, 23, 15, 7};

const uint8_t FP[] = {40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5,
    45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25};

const uint8_t PC_1[] = {57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60,
    52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12,
    4};

const uint8_t PC_2[] = { 14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34,
    53, 46, 42, 50, 36, 29, 32};

const uint8_t shifts[] = { 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1};


const uint8_t E[] = { 32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13,
    14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28,
    29, 28, 29, 30, 31, 32, 1 };

const uint8_t S[8][4][16] = {
    {
        {14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7},
        {0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8},
        {4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0},
        {15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13},
    },
    {
        {15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10},
        {3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5},
        {0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15},
        {13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9},
    },
    {
        {10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8},
        {13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1},
        {13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7},
        {1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12},
    },
    {
        {7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15},
        {13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9},
        {10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4},
        {3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14},
    },
    {
        {2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9},
        {14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6},
        {4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14},
        {11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3},
    },
    {
        {12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11},
        {10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8},
        {9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6},
        {4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13},
    },
    {
        {4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1},
        {13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6},
        {1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2},
        {6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12},
    },
    {
        {13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7},
        {1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2},
        {7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8},
        {2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11},
    },
};

const uint8_t P[] = { 16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24,
    14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25};


#if ENABLE_LOG  
    #include "math.h"
    double calculate_entropy(uint64_t data) {
        double one_count = 0;
        for (uint8_t i = 0; i < 64; ++i) {
            one_count += data >> i & 1;
        }
        double zero_p = (64 - one_count) / 64;
        double one_p = one_count / 64;

        double entropy = 0;
        if (zero_p != 0) {
            entropy -= zero_p * log2(zero_p);
        }
        if (one_p != 0) {
            entropy -= one_p * log2(one_p);
        }
        return entropy;
    }
#endif

union data change_position(union data d, uint8_t* new_pos, uint8_t len) {
    union data new_d;    
    new_d.bytes = 0;

    for (int i = 0; i < len; ++i) {
        uint8_t bit_position = 63 - (new_pos[i] - 1);  // Позиція біта у 64-бітовому числі
        uint8_t bit = (d.bytes >> bit_position) & 1;   // Отримати біт
        new_d.bytes |= ((uint64_t)bit << (63 - i));    // Встановити біт у новій позиції
    }
    return new_d;
}

uint32_t shift_left(uint32_t data, uint8_t shift) {
    return (data << shift) | (data >> (32 - shift));
}

uint32_t substitution(uint64_t expanded) {
    uint32_t result = 0;
    for (int i = 0; i < 8; i++) {
        int six_bits = (expanded >> (42 - 6 * i)) & 0x3F; 
        int row = ((six_bits & 0x20) >> 4) | (six_bits & 0x01);  
        int col = (six_bits >> 1) & 0x0F;                        
        result = (result << 4) | S[i][row][col];
    }
    return result;
}

uint32_t F(uint32_t right, uint64_t round_key) {
    union data new_right;
    new_right.bytes = right;
    union data expanded_right = change_position(new_right, (uint8_t*) E, 48);
    expanded_right.bytes ^= round_key;
    expanded_right.bytes = substitution(expanded_right.bytes);
    return change_position(expanded_right, (uint8_t*) P, 32).bytes;
}


union data encrypt(union data to_encrypt, union data key) {
    union data new_data = change_position(to_encrypt, (uint8_t*) IP, 64);

    uint32_t right_data = new_data.bytes;
    uint32_t left_data = new_data.bytes >> 32;

    union data round_key = change_position(key, (uint8_t*) PC_1, 56);
    uint32_t left_key = (round_key.bytes >> 28) & 0x0FFF;
    uint32_t right_key = round_key.bytes & 0x0FFF;

    uint32_t new_left;

    for (int i = 0; i < 16; ++i) {
        left_key = shift_left(left_key, shifts[i]);
        right_key = shift_left(right_key, shifts[i]);

        union data combined_key;
        combined_key.bytes = ((uint64_t)right_key << 28) | left_key;
        round_key = change_position(combined_key, (uint8_t*) PC_2, 32);

        new_left = right_data; 
        right_data = left_data ^ F(right_data, round_key.bytes);

        left_data = new_left;

#if ENABLE_LOG
        float entropy = calculate_entropy((uint64_t) right_data << 32 | left_data);
        printf("Entropy: %f\n", entropy);
#endif
    }

    new_data.bytes = ((uint64_t)right_data << 32) | left_data;
    new_data = change_position(new_data, (uint8_t*) FP, 64);

    return new_data; 
}


union data decrypt(union data to_decrypt, union data key) {
    union data new_data = change_position(to_decrypt, (uint8_t*) IP, 64);

    uint32_t right_data = new_data.bytes;
    uint32_t left_data = new_data.bytes >> 32;

    union data round_key = change_position(key, (uint8_t*) PC_1, 56);
    uint32_t left_key = (round_key.bytes >> 28) & 0x0FFF;
    uint32_t right_key = round_key.bytes & 0x0FFF;

    union data round_keys[16];
    for (int i = 0; i < 16; ++i){
        uint32_t left_key = shift_left(left_key, shifts[i]);
        uint32_t right_key = shift_left(right_key, shifts[i]);

        union data combined_key;
        combined_key.bytes = ((uint64_t)right_key << 28) | left_key;
        round_key = change_position(combined_key, (uint8_t*) PC_2, 32);
        round_keys[i] = round_key;
    }


    for (int i = 15; i >= 0; --i) {
        uint32_t new_left = right_data; 
        right_data = left_data ^ F(right_data, round_keys[i].bytes);

        left_data = new_left;
    }

    new_data.bytes = ((uint64_t)right_data << 32) | left_data;
    new_data = change_position(new_data, (uint8_t*) FP, 64);
    return new_data;
}



int main(int argc, char *argv[]) {
    union data to_encrypt;
    union data key;
    
    strcpy(to_encrypt.word, "Haello");
    strcpy(key.word, "worlds");

    printf("Before: %s, as bytes: %lu\n", to_encrypt.word, to_encrypt.bytes);

    union data encrypted = encrypt(to_encrypt, key);
    printf("Encrypted: %s, as bytes: %lu\n", encrypted.word, encrypted.bytes);

    union data decrypted = decrypt(encrypted, key);
    printf("Decrypted: %s, as bytes: %lu\n", decrypted.word, decrypted.bytes);

    return 0;
}
