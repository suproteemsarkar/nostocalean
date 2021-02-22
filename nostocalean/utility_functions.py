"""Some *real* utility functions."""

import random

utility_functions = [
    "Quasilinear",
    "Leontief",
    "Stone-Geary",
    "Cobb-Douglas",
    "Homothetic",
    "HARA",
    "Exponential (CARA)",
    "Power (CRRA)",
    "Epstein-Zin",
    "Quadratic",
    "CES",
]


def get_utility_function() -> str:
    """Return a utility function."""
    return random.choice(utility_functions)
