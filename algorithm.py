S_BOX = [
    # Таблиця S-Box (заповнена для прикладу)
]

MIX_COLUMNS_MATRIX = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
]

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = S_BOX[state[i][j]]
    return state

def shift_rows(state):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state

def galois_multiply(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= 0x1b
        b >>= 1
    return p % 256

def mix_columns(state):
    for i in range(4):
        col = state[i]
        state[i] = [
            galois_multiply(MIX_COLUMNS_MATRIX[0][0], col[0]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[0][1], col[1]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[0][2], col[2]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[0][3], col[3]),
            galois_multiply(MIX_COLUMNS_MATRIX[1][0], col[0]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[1][1], col[1]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[1][2], col[2]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[1][3], col[3]),
            galois_multiply(MIX_COLUMNS_MATRIX[2][0], col[0]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[2][1], col[1]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[2][2], col[2]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[2][3], col[3]),
            galois_multiply(MIX_COLUMNS_MATRIX[3][0], col[0]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[3][1], col[1]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[3][2], col[2]) ^
            galois_multiply(MIX_COLUMNS_MATRIX[3][3], col[3])
        ]
    return state

def add_round_key_mod_256(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] = (state[i][j] + round_key[i][j]) % 256
    return state

def initial_state(block):
    state = [[0] * 4 for _ in range(4)]
    for i in range(16):
        state[i % 4][i // 4] = block[i]
    return state

def state_to_block(state):
    block = [0] * 16
    for i in range(16):
        block[i] = state[i % 4][i // 4]
    return block

def key_expansion(key):
    round_keys = [key[i:i+4] for i in range(0, len(key), 4)]
    for i in range(10):
        new_key = [((round_keys[-1][j] + round_keys[i][j]) % 256) for j in range(4)]
        round_keys.append(new_key)
    return round_keys

def aes_encrypt_mod_256(block, round_keys):
    state = initial_state(block)
    state = add_round_key_mod_256(state, round_keys[0])
    for round_key in round_keys[1:-1]:
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key_mod_256(state, round_key)
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key_mod_256(state, round_keys[-1])
    return state_to_block(state)