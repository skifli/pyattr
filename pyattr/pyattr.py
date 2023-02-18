from typing import Any
from inspect import stack


class ProtectedDict(dict):
    def pyattr_check(self, __key: str, class_object: object) -> str:
        try:
            caller_class = stack()[3][0].f_locals["self"].__class__.__name__

            if __key.startswith(f"_{caller_class}"):
                __key = __key.removeprefix(f"_{caller_class}")
        except KeyError:
            pass

        caller = stack()[3][0].f_locals

        if __key.startswith("__"):
            if "self" in caller:
                if caller["self"].__class__ != class_object:
                    raise AttributeError(
                        f"Attribute '{__key}' of '{class_object.__name__}' object is private."
                    )
            else:
                raise AttributeError(
                    f"Attribute '{__key}' of '{class_object.__name__}' object is private."
                )
        elif __key.startswith("_"):
            if "self" in caller:
                if class_object not in caller["self"].__class__.__mro__:
                    raise AttributeError(
                        f"Attribute '{__key}' of '{class_object.__name__}' object is protected."
                    )
            else:
                raise AttributeError(
                    f"Attribute '{__key}' of '{class_object.__name__}' object is protected."
                )

        return __key

    def __getitem__(self, __key: str, class_object: object) -> Any:
        return super().__getitem__(self.pyattr_check(__key, class_object))

    def __setitem__(self, __key: str, __value: str, class_object: object) -> None:
        super().__setitem__(self.pyattr_check(__key, class_object), __value)


class Protected(ProtectedDict):
    def __init__(self, **kwargs) -> None:
        object.__setattr__(
            self, "pyattr_class_object", stack()[1][0].f_locals["__class__"]
        )

        super().update(kwargs)

    def __getattribute__(self, __name: str) -> Any:
        try:
            return object.__getattribute__(self, __name)
        except AttributeError:
            pass

        return super().__getitem__(
            __name, object.__getattribute__(self, "pyattr_class_object")
        )

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setitem__(
            __name, __value, object.__getattribute__(self, "pyattr_class_object")
        )


class Example(Protected):
    def __init__(self) -> None:
        super().__init__()

        self.__name = "pyattr"


example = Example()
print(example.__name)  # Error - '__name' is a protected attribute.
