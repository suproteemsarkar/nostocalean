"""Utility functions."""

import os
import re
import unicodedata
from contextlib import redirect_stderr, contextmanager
from typing import Any, Callable, Iterable, List

import numpy as np


def lmap(func: Callable, *iterables: Iterable) -> List:
    """Returns a list of the result of mapping a function to one or more iterables."""
    return list(map(func, *iterables))


@contextmanager
def suppress() -> None:
    """Suppress output within context."""
    with open(os.devnull, "w") as null:
        with redirect_stderr(null):
            yield


def skipna(func: Callable, return_val: Any = np.nan) -> Callable:
    """Skip NaN values when evaluating a function. Adapted from jiafengkevinchen/pandas_tools."""

    def _wrapped(x, *args, **kwargs):
        if (isinstance(x, float) and np.isnan(x)) or x is None:
            return return_val
        return func(x, *args, **kwargs)

    return _wrapped


def clean_name(col_name: str) -> str:
    """Clean column name. Adapted from ericmjl/pyjanitor."""
    col_name = str(col_name).lower()
    fixes = [(r"[ /:,?()\.-]", "_"), (r"['’]", "")]
    for search, replace in fixes:
        col_name = re.sub(search, replace, col_name)
    col_name = "".join(c for c in col_name if c.isalnum() or "_" in c)
    col_name = "".join(
        letter
        for letter in unicodedata.normalize("NFD", col_name)
        if not unicodedata.combining(letter)
    )
    col_name = col_name.strip("_")
    return col_name
