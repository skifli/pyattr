from typing import Any, final
from inspect import stack

__version__ = "1.2.1"


class _PyattrDict(dict):
    @final
    def __pyattr_check(self, __key: str, class_object: object, i: int = 3) -> str:
        try:
            caller_class = stack()[i][0].f_locals["self"].__class__.__name__

            if __key.startswith(f"_{caller_class}"):
                __key = __key.removeprefix(f"_{caller_class}")
        except KeyError:
            pass

        caller = stack()[i][0].f_locals

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

    @final
    def __getitem__(self, __key: str, class_object: object) -> Any:
        return super().__getitem__(self.__pyattr_check(__key, class_object))

    @final
    def __setitem__(self, __key: str, __value: str, class_object: object) -> None:
        super().__setitem__(self.__pyattr_check(__key, class_object), __value)


class Pyattr(_PyattrDict):
    def __init__(self, **kwargs) -> None:
        object.__setattr__(
            self, "pyattr_class_object", stack()[1][0].f_locals["__class__"]
        )

        super().update(kwargs)

    @final
    def __getattribute__(self, __name: str) -> Any:
        try:
            obj = object.__getattribute__(self, __name)

            if __name in ["__class__", "_PyattrDict__pyattr_check"]:
                return obj
        except AttributeError:
            pass

        return super().__getitem__(
            __name, object.__getattribute__(self, "pyattr_class_object")
        )

    @final
    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setitem__(
            __name, __value, object.__getattribute__(self, "pyattr_class_object")
        )
