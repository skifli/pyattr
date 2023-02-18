# pyattr

![PyPI](https://img.shields.io/pypi/v/pyattr)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyattr)
![Lines of Code](https://img.shields.io/github/languages/code-size/skifli/pyattr)

- [pyattr](#pyattr)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Example](#example)

While Python does have name mangling, it is not nearly as powerful as access modifiers found in languages such as C++. **pyattr** provides an easy-to-use API for access modifiers in Python, and is actively developed.

## Installation

Installation via **pip**:

```
pip install pyattr
```

## Usage

All you have to do is make your class inherit from the **`pyattr.Protected`** class, and add **`super().__init__()`** as the first line in the **`__init__`** function of your class. And that's it! **pyattr** will handle the magic to make sure variables cannot be accessed / set where the shouldn't be. It also provides useful error messages to users.

## Example

```python
from pyattr import Protected

class Example(Protected):
    def __init__(self) -> None:
        super().__init__()

        self.__name = "pyattr"

example = Example()
print(example.__name) # Error - '__name' is a protected attribute of 'Example'.
```