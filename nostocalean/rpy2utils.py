from rpy2.robjects.packages import importr
from rpy2.robjects import Formula, pandas2ri
from rpy2.robjects import r as r_env
import rpy2
import numpy as np

pandas2ri.activate()


def _convert_vector(lv):
    """Convert an RPy2 object in reasonable ways"""
    if isinstance(lv, rpy2.robjects.vectors.ListVector):
        d = dict(lv.items())
        return d
    elif isinstance(lv, rpy2.robjects.vectors.Vector):
        return list(lv)
    elif isinstance(lv, rpy2.robjects.Formula):
        return lv.r_repr()
    elif isinstance(lv, np.ndarray):
        try:
            return lv.item()
        except ValueError:
            return lv
    else:
        return lv


def convert(lv):
    """Recursively convert a ListVector"""
    if isinstance(lv, rpy2.robjects.vectors.ListVector):
        top_level_dict = _convert_vector(lv)
        for key, val in list(top_level_dict.items()):
            if isinstance(lv, rpy2.robjects.vectors.ListVector):
                top_level_dict[key] = convert(val)
            else:
                top_level_dict[key] = _convert_vector(val)
        return top_level_dict
    else:
        return _convert_vector(lv)


def execute_r(
    r_code: str,
    packages: list,
    inputs: dict,
    outputs: list,
    overwrite=False,
    side_effect=False,
) -> dict:
    """
    Execute R code and return the result.
    """
    call = (
        r_env if side_effect else r_env.eval
    )  # Ignore print statements if side_effect is False
    for pkg in packages:
        call(f"library({pkg})")
    for k, val in inputs.items():
        if overwrite or not r_env.exists(k)[0]:
            r_env.assign(k, val)
    call(r_code)
    return {o: convert(r_env.get(o)) for o in outputs}

