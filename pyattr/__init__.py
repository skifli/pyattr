"""
Copyright skifli under the MIT license. ALl rights reserved.
See '../LICENSE' for license information.
SPDX-License-Identifier: MIT License.
"""

from types import FrameType, TracebackType
from sys import _getframe
from typing import Any, final

__version__ = "1.4.5"


def _pyattr_stack() -> list[FrameType]:
    frame = _getframe().f_back
    frames = []

    while frame:
        frames.append(frame)
        frame = frame.f_back

    return frames


class PyattrError(Exception):
    pass


class _PyattrDict(dict):
    @final
    def __pyattr_check(self, __key: str, class_object: object, i: int = 3) -> str:
        caller = _pyattr_stack()[i].f_locals

        if "self" in caller:
            caller_class = caller["self"].__class__.__name__

            if __key.startswith(f"_{caller_class}"):
                __key = __key.removeprefix(f"_{caller_class}")

        try:
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
        except AttributeError as e:
            last_frame = _pyattr_stack()[3]

            raise AttributeError(*e.args, name=e.name, obj=e.obj).with_traceback(
                TracebackType(
                    tb_next=None,
                    tb_frame=last_frame,
                    tb_lasti=last_frame.f_lasti,
                    tb_lineno=last_frame.f_lineno,
                )
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
            self, "pyattr_class_object", _pyattr_stack()[1].f_locals["__class__"]
        )

        super().update(kwargs)

    @final
    def pyattr_get_class_object(self) -> object:
        try:
            return object.__getattribute__(self, "pyattr_class_object")
        except AttributeError:
            last_frame = _pyattr_stack()[2]

            raise PyattrError(
                "Did you forget to add 'super().__init__()' at the start of the '__init__' function of your class?"
            ).with_traceback(
                TracebackType(
                    tb_next=None,
                    tb_frame=last_frame,
                    tb_lasti=last_frame.f_lasti,
                    tb_lineno=last_frame.f_lineno,
                )
            )

    @final
    def __getattribute__(self, __name: str) -> Any:
        try:
            obj = object.__getattribute__(self, __name)

            return obj
        except AttributeError:
            pass

        return super().__getitem__(__name, self.pyattr_get_class_object())

    @final
    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setitem__(__name, __value, self.pyattr_get_class_object())
