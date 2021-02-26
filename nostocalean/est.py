"""Methods for calling fixest using rpy2."""

import re
from typing import Optional, TypeVar

from rpy2.robjects import Formula, pandas2ri
from rpy2.robjects.packages import importr
import pandas as pd
from .functions import clean_name, suppress

FixestResult = TypeVar("FixestResult")

base = importr("base")
fixest = importr("fixest")
pandas2ri.activate()


class RegressionResult:
    """Accessors for a fixest result."""

    def __init__(self, result: FixestResult, se: str):
        self.result = result
        self.rx = self.result.rx
        self.se = se

    def summary(self, **kwargs) -> str:
        """Return a string summary of a feols result."""
        if "se" not in kwargs:
            kwargs["se"] = self.se

        with suppress():
            return str(base.summary(self.result, **kwargs))  # pylint: disable=no-member

    def get_table(self) -> pd.DataFrame:
        """Return the coefficient table from a feols regression result."""
        return (
            self.result.rx["coeftable"][0]
            .rename(columns=clean_name)
            .rename(columns={"pr_t": "p_value"})
        )


def feols(
    fml: str,
    data: pd.DataFrame,
    se: Optional[str] = None,
    **kwargs,
) -> RegressionResult:
    """Wrapper for calling fixest::feols in R."""

    if se is None:
        se = "cluster" if "cluster" in kwargs else "hetero"

    columns = re.findall(r"[\w']+", fml)

    # fmt: off
    result  = fixest.feols(Formula(fml), data=data[columns], se=se, **kwargs) # pylint: disable=no-member
    # fmt: on

    return RegressionResult(result, se=se)


def feglm(
    fml: str,
    data: pd.DataFrame,
    se: Optional[str] = None,
    **kwargs,
) -> RegressionResult:
    """Wrapper for calling fixest::feglm in R."""

    if se is None:
        se = "cluster" if "cluster" in kwargs else "hetero"

    columns = re.findall(r"[\w']+", fml)

    # fmt: off
    result  = fixest.feglm(Formula(fml), data=data[columns], se=se, **kwargs) # pylint: disable=no-member
    # fmt: on

    return RegressionResult(result, se=se)


def reg(*args, **kwargs) -> str:
    """Run a feols regression and return the summary."""
    return feols(*args, **kwargs).summary()


def preg(*args, **kwargs) -> None:
    """Run a feols regression and print the summary."""
    print(feols(*args, **kwargs).summary())


def treg(*args, **kwargs) -> pd.DataFrame:
    """Run a feols regression and return the coefficient table."""
    return feols(*args, **kwargs).get_table()
