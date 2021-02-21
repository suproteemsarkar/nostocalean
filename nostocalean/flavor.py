"""Custom pandas_flavor methods."""

import pandas as pd
import pandas_flavor as pf
from pandas._typing import FilePathOrBuffer


@pf.register_dataframe_method
def mem(df: pd.DataFrame) -> float:
    """Get the memory usage (in GB) of a dataframe."""
    return df.memory_usage().sum() / 1e9


@pf.register_dataframe_method
def write_parquet(df: pd.DataFrame, path: FilePathOrBuffer) -> None:
    """Write a dataframe to a path as a parquet."""
    try:
        df.to_parquet(
            path,
            engine="fastparquet",
            compression="snappy",
        )
    except OSError:
        df.to_parquet(
            path,
            engine="fastparquet",
            compression="snappy",
            row_group_offsets=100_000,
        )
