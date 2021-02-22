"""Methods for calling fixest using rpy2."""

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
    """Accessors for a feols result."""

    def __init__(self, result: FixestResult):
        self.result = result

    def summary(self, se: Optional[str] = None) -> str:
        """Return a string summary of a feols result."""
        with suppress():
            if se is None:
                return str(base.summary(self.result))  # pylint: disable=no-member
            return str(base.summary(self.result, se=se))  # pylint: disable=no-member

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
    cluster: Optional[str] = None,
) -> RegressionResult:
    """Wrapper for calling fixest::feols in R."""
    # fmt: off
    if cluster is not None and se is not None:
        result = fixest.feols(Formula(fml), data=data, se=se, cluster=cluster)  # pylint: disable=no-member
    elif cluster is not None:
        result = fixest.feols(Formula(fml), data=data, se="cluster", cluster=cluster)  # pylint: disable=no-member
    elif se is not None:
        result = fixest.feols(Formula(fml), data=data, se=se)  # pylint: disable=no-member
    else:
        result = fixest.feols(Formula(fml), data=data, se="hetero")  # pylint: disable=no-member
    # fmt: on
    return RegressionResult(result)


def reg(
    fml: str,
    data: pd.DataFrame,
    se: Optional[str] = "hetero",
    cluster: Optional[str] = None,
) -> str:
    """Run a feols regression and return the summary."""
    return feols(fml, data, se=se, cluster=cluster).summary(se)


def treg(
    fml: str,
    data: pd.DataFrame,
    se: Optional[str] = "hetero",
    cluster: Optional[str] = None,
) -> pd.DataFrame:
    """Run a feols regression and return the coefficient table."""
    return feols(fml, data, se=se, cluster=cluster).get_table()
