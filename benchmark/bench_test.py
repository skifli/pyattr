from pyattr import Pyattr


class Example:
    def __init__(self) -> None:
        self.__age = 1

    def get_age(self) -> int:
        return self.__age


class PyAttrExample(Pyattr):
    def __init__(self) -> None:
        super().__init__()

        self.__age = 1

    def get_age(self) -> int:
        return self.__age


def bench_example() -> None:
    example = Example()

    for _ in range(1000):
        example.get_age()


def bench_pyattrexample() -> None:
    example = PyAttrExample()

    for _ in range(1000):
        example.get_age()


__benchmarks__ = [(bench_example, bench_pyattrexample, "Default class vs Pyattr class")]
