# pyattr

[![PyPI](https://img.shields.io/pypi/v/pyattr)](https://pypi.org/project/pyattr)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyattr)](https://pypi.org/project/pyattr/#files)
![Lines of Code](https://img.shields.io/github/languages/code-size/skifli/pyattr)

- [pyattr](#pyattr)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Example](#example)
  - [How it works](#how-it-works)
  - [Benchmarks](#benchmarks)

While Python does have name mangling, it is not nearly as powerful as access modifiers found in languages such as C++. **pyattr** provides an easy-to-use API for access modifiers in Python.

## Installation

Installation via **pip**:

```
pip install pyattr
```

## Usage

All you have to do is make your class inherit from the *`pyattr.Pyattr`* class, and add *`super().__init__()`* as the first line in the *`__init__`* function of your class. And that's it! **pyattr** will handle the magic to make sure variables cannot be accessed / set where the shouldn't be. It also provides useful error messages to users.

## Example

Here is a simple example involving a *private* variable.

```python
from pyattr import Pyattr

class Example(Pyattr):
    def __init__(self) -> None:
        super().__init__()

        self.__name = "pyattr"

example = Example()
print(example.__name) # Error - '__name' is a private attribute of 'Example'.
```

As well as variables, **pyattr** also supports access control of *functions*!

```python
from pyattr import Pyattr

class Example(Pyattr):
    def __init__(self) -> None:
        super().__init__()

    def __example(self) -> None:
        pass


example = Example()
print(example.__example())  # Error - '__example' is a private attribute of 'Example'.
```

## How it works

**pyattr** overrides the default *set* and *get* functions of your class. The overridden functions defined by **pyattr** are merged into your class when you inherit from the *`pyattr.Pyattr`* class. As well as this, the *`pyattr.Pyattr`* class inherits from the *`pyattr._PyattrDict`* class, which provides a custom dictionary implementation. This is because you can change the variables in a class using *`class.__dict__["var"] = "val"`*, meaning a custom dictionary would be the best way to prevent the access system being circumvented.

The overriden *set* and *get* functions of your class call the respective *set* and *get* functions of the custom dictionary. This dictionary, using *`sys._getframe()`*, works out the caller's function, and the caller's class (if any). It uses this data to work out if the caller should be allowed to access the specified variables. If it shouldn't, an *`AttributeError`* is raised, with an error message explaining the cause.

## Benchmarks

The code for the benchmarks can be found in the [benchmark](https://github.com/skifli/pyattr/blob/main/benchmark/) folder.

[![Benchmark Output](https://raw.githubusercontent.com/skifli/pyattr/main/benchmark/output.png)](https://github.com/skifli/pyattr/blob/main/benchmark/bench_test.py)
