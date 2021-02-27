"""Hacky methods for calling fixest on an R container."""

import os
import subprocess
import re
import tempfile
from pathlib import Path

import pandas as pd


class ContainerConfig:
    """Container location and cache path config."""

    def __init__(self):
        self.container_path = None
        self.cache_path = None
        try:
            self.container_path = Path(os.environ["R_CONTAINER_PATH"]).resolve()
            self.cache_path = Path(os.environ["R_DATASET_PATH"]).resolve()
        except KeyError:
            pass


config = ContainerConfig()


def reg(fml: str, data: pd.DataFrame, se: str = "hetero", no_cache: bool = False):
    """Run a feols regression on a container and return the summary."""
    if config.container_path is None:
        raise RuntimeError("No R container specified.")

    cache_dir = None
    if config.cache_path is None or no_cache:
        cache_dir = tempfile.TemporaryDirectory()
        cache_path = Path(cache_dir.name)
    else:
        cache_path = config.cache_path

    columns = list(set(re.findall(r"[\w']+", fml)))
    df = data[columns]
    df_hash = "_".join(pd.util.hash_pandas_object(df).astype(str))

    out_path = cache_path / f"{df_hash}.csv"
    if not out_path.exists():
        df.to_csv(out_path)

    r_string = f'library(fixest); frame <- read.csv("/cache/{df_hash}.csv"); feols({fml}, frame, se="{se}")'
    feols_result = subprocess.check_output(
        [
            "singularity",
            "exec",
            "--bind",
            f"{cache_path}:/cache",
            config.container_path,
            "Rscript",
            "-e",
            r_string,
        ]
    ).decode()

    if cache_dir is not None:
        cache_dir.cleanup()

    return feols_result


def preg(*args, **kwargs):
    """Run a feols regression on a container and print the summary."""
    print(reg(*args, **kwargs))
