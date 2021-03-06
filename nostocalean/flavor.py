"""Custom pandas_flavor methods."""

from typing import List, Optional, TypeVar, Union

import pandas as pd
import pandas_flavor as pf
import numpy as np
import matplotlib as mpl
import seaborn as sns

FrameOrSeries = TypeVar("FrameOrSeries", pd.DataFrame, pd.Series)


@pf.register_dataframe_method
@pf.register_series_method
def mem(df: FrameOrSeries, deep: bool = True) -> float:
    """Get the memory usage (in GB) of a dataframe or series."""
    if isinstance(df, pd.DataFrame):
        return df.memory_usage(deep=deep).sum() / 1e9
    return df.memory_usage(deep=deep) / 1e9


@pf.register_dataframe_method
@pf.register_series_method
def desc(df: FrameOrSeries, increment: float = 0.1) -> FrameOrSeries:
    """Calls pandas describe with a specified percentile increment."""
    return df.describe(percentiles=np.arange(increment, 1, increment))


@pf.register_series_method
def normalize(series: pd.Series) -> pd.Series:
    """Normalizes a series."""
    return (series - series.mean()) / series.std()


@pf.register_series_method
def rescale(series: pd.Series, upper: float = 0, lower: float = 1) -> pd.Series:
    """Rescales a series."""
    return lower + (upper - lower) * (
        (series - series.min()) / (series.max() - series.min())
    )


@pf.register_series_method
def winsorize(series: pd.Series, left: float = 1, right: float = 1) -> pd.Series:
    """Winsorizes a series at the provided percentiles."""
    values = series.dropna()
    left_cutoff = np.percentile(values, left)
    right_cutoff = np.percentile(values, 100 - right)

    series = series.copy()
    series[series < left_cutoff] = left_cutoff
    series[series > right_cutoff] = right_cutoff
    return series


@pf.register_dataframe_method
def left_merge(
    df: pd.DataFrame,
    other: Union[pd.DataFrame, pd.Series],
    on: Union[List[str], str],
    right_columns: Union[List[str], str, None] = None,
) -> pd.DataFrame:
    """Convenience in-place method for left merge that avoids copying irrelevant columns."""
    if isinstance(on, str):
        on = [on]

    if isinstance(other, pd.DataFrame):
        addition = df[on].merge(other, on=on, how="left")
    else:
        addition = df[on].merge(other, left_on=on, right_index=True, how="left")

    if right_columns is None:
        right_columns = addition.columns
    elif isinstance(right_columns, str):
        right_columns = [right_columns]
    for column in addition.columns:
        if column not in on and column in right_columns:
            df[column] = addition[column].values


@pf.register_dataframe_method
def tsg(
    df: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    agg: str = "sum",
    i: int = 1,
    e: int = 1,
) -> pd.Series:
    """Return a grouped time series given an outcome variable and aggregation function."""
    series = df.groupby([x, group])[y].agg(agg).reset_index()
    T = series[x].nunique()
    series = series.groupby(group).head(T - i).groupby(group).tail(T - i - e)
    return series


@pf.register_dataframe_method
def tsgr(
    df: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    agg: str = "sum",
    resample: str = "4W",
    i: int = 1,
    e: int = 1,
) -> pd.Series:
    """Return a grouped time series given an outcome variable, resample window, and aggregation function."""
    series = df.set_index(x).groupby(group)[y].resample(resample).agg(agg).reset_index()
    T = series[x].nunique()
    series = series.groupby(group).head(T - i).groupby(group).tail(T - i - e)
    return series


@pf.register_dataframe_method
def ts(
    df: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    agg: str = "sum",
    i: int = 1,
    e: int = 1,
    **kwargs,
) -> mpl.axes.Axes:
    """Return a time series plot given an outcome variable and aggregation function."""
    series = df.tsg(x=x, y=y, group=group, agg=agg, i=i, e=e)
    return sns.lineplot(data=series, x=x, y=y, hue=group, **kwargs)


@pf.register_dataframe_method
def tsr(
    df: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    agg: str = "sum",
    resample: str = "4W",
    i: int = 1,
    e: int = 1,
    **kwargs,
) -> mpl.axes.Axes:
    """Return a time series plot given an outcome variable, resample window, and aggregation function."""
    series = df.tsgr(x=x, y=y, group=group, agg=agg, resample=resample, i=i, e=e)
    return sns.lineplot(data=series, x=x, y=y, hue=group, **kwargs)


@pf.register_dataframe_method
def write_parquet(df: pd.DataFrame, path: str) -> None:
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
