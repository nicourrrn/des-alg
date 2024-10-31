run_c:
    clang main.c -o main -lm && ./main

run:
    source ./.venv/bin/activate && python ./algorithm.py
