"""
_funcs.py
05. February 2023

a few generic useful functions

Author:
Nilusink
"""
import typing as tp


def arg_or_default(value: tp.Any, default_value: tp.Any, check_if: tp.Any = ...) -> tp.Any:
    """
    :param value: the value to check
    :param default_value: what the value should be if it equals `check_if`
    :param check_if: what to check for
    """
    return default_value if value is check_if else value
