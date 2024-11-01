run_py: build_so
    source ./.venv/bin/activate && python setup.py build && python ./build/lib.linux-x86_64-cpython-312/main.py

run_c:
    clang main.c -o main -DENABLE_LOG=1 -lm && ./main

run_py_test: build_so
    source ./.venv/bin/activate && python ./algorithm.py

build_so:
    clang -shared -o lib.so -fPIC -DENABLE_LOG=0 $(pkg-config --cflags python3) main.c

build_so_py:
    clang -shared -o lib.so -fPIC -DENABLE_LOG=0 $(pkg-config --cflags python3) des_lib.c
