run_py: build_so
    source ./.venv/bin/activate && python ./main.py

run_c:
    clang main.c -o main -DENABLE_LOG=1 -lm && ./main

run_py_test: build_so
    source ./.venv/bin/activate && python ./algorithm.py

build_so:
    clang -shared -o lib.so -fPIC -DENABLE_LOG=0 main.c
