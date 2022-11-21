"""Methods for calling fixest using rpy2."""

import re
from typing import Optional

from rpy2 import robjects
from rpy2.robjects import packages
import pandas as pd
from nostocalean.functions import suppress

RegressionResult = robjects.vectors.ListVector

base = packages.importr("base")
fixest = packages.importr("fixest")


class FixestResult:
    """Accessors for a fixest result."""

    def __init__(self, result: robjects.vectors.ListVector, **kwargs):
        self.result = result
        self.rx = self.result.rx
        if "vcov" in kwargs:
            self.mode = "vcov"
            self.vcov = kwargs["vcov"]
        else:
            self.mode = "cluster"
            self.cluster = kwargs["cluster"]

    def summary(self, **kwargs) -> str:
        """Return a string summary of a feols result."""
        if "vcov" not in kwargs and "cluster" not in kwargs:
            if self.mode == "vcov":
                kwargs["vcov"] = self.vcov
            else:
                kwargs["cluster"] = self.cluster

        with suppress():
            return str(base.summary(self.result, **kwargs))  # pylint: disable=no-member

    def get_table(self, **kwargs) -> pd.DataFrame:
        """Return the coefficient table from a feols regression result."""
        coeftable = pd.DataFrame(
            self.rx["coeftable"][0], columns=["coef", "se", "t", "p"]
        )
        summary = self.summary()
        coeftable.index = map(
            lambda s: s.split(f" ")[0],
            summary[summary.find("Standard-errors") : summary.find("\n---")].split(
                "\n"
            )[2:],
        )  # Get coefficient names from fixest summary
        return coeftable


def feols(
    fml: str,
    data: pd.DataFrame,
    **kwargs,
) -> FixestResult:
    """Wrapper for calling fixest::feols in R."""

    if "vcov" not in kwargs and "cluster" not in kwargs:
        kwargs["vcov"] = "hetero"

    columns = set(re.findall(r"[\w']+", fml))
    columns = [column for column in columns if column != "1"]

    for key in ["cluster", "panel_id"]:
        if key in kwargs:
            columns = list(set(columns + re.findall(r"[\w']+", kwargs[key])))
            if kwargs[key][0] == "~":
                kwargs[key] = robjects.Formula(kwargs[key])

    result = fixest.feols(  # pylint: disable=no-member
        robjects.Formula(fml),
        data=data[columns].dropna(subset=columns),
        **kwargs,
    )

    return FixestResult(result, **kwargs)


def feglm(
    fml: str,
    data: pd.DataFrame,
    **kwargs,
) -> FixestResult:
    """Wrapper for calling fixest::feglm in R."""

    if "vcov" not in kwargs and "cluster" not in kwargs:
        kwargs["vcov"] = "hetero"

    columns = set(re.findall(r"[\w']+", fml))
    columns = [column for column in columns if column != "1"]

    for key in ["cluster", "panel_id"]:
        if key in kwargs:
            columns = list(set(columns + re.findall(r"[\w']+", kwargs[key])))
            if kwargs[key][0] == "~":
                kwargs[key] = robjects.Formula(kwargs[key])

    result = fixest.feglm(  # pylint: disable=no-member
        robjects.Formula(fml),
        data=data[columns].dropna(subset=columns),
        **kwargs,
    )

    return FixestResult(result, **kwargs)


def reg(*args, **kwargs) -> str:
    """Run a feols regression and return the summary."""
    return feols(*args, **kwargs).summary()


def preg(*args, **kwargs) -> None:
    """Run a feols regression and print the summary."""
    print(feols(*args, **kwargs).summary())


def treg(*args, **kwargs) -> pd.DataFrame:
    """Run a feols regression and return the coefficient table."""
    return feols(*args, **kwargs).get_table()
