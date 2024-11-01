from setuptools import Extension, setup


def main():
    setup(
        name="des",
        version="1.0.0",
        description="This is a des package",
        ext_modules=[
            Extension(
                "des",
                ["./des_lib.c"],
                extra_compile_args=["-fPIC"],
            )
        ],
    )


if __name__ == "__main__":
    main()
