"""Methods for calling did using rpy2."""

from rpy2 import robjects
from rpy2.robjects import packages
import pandas as pd
from nostocalean.functions import suppress

RegressionResult = robjects.vectors.ListVector

base = packages.importr("base")
did_base = packages.importr("did")


class DidResult:
    """Accessors for a did result."""

    def __init__(self, result: RegressionResult):
        self.result = result
        self.rx = self.result.rx

    def summary(self, **kwargs) -> str:
        """Return a string summary of a did result."""
        with suppress():
            return str(base.summary(self.result, **kwargs))  # pylint: disable=no-member

    def get_es(self) -> RegressionResult:
        """Return an aggregated event study of a did result."""
        return did_base.aggte(self.result, type="dynamic")  # pylint: disable=no-member

    def es_summary(self, **kwargs) -> str:
        """Return a string summary of an aggregated event study of a did result."""
        with suppress():
            # fmt: off
            return str(base.summary(self.get_es(), **kwargs))  # pylint: disable=no-member
            # fmt: on


def att_gt(y: str, d: str, g: str, t: str, data: pd.DataFrame, **kwargs) -> DidResult:
    """Wrapper for calling did::att_gt in R."""
    if "covariates" in kwargs:
        kwargs["covariates"] = robjects.Formula("~" + "+".join(kwargs["covariates"]))

    # fmt: off
    result = did_base.att_gt(yname=y, gname=d, idname=g, tname=t, data=data) # pylint: disable=no-member
    # fmt: on

    return DidResult(result)


def did(*args, **kwargs) -> str:
    """Estimate group-time treatment effects and return the summary."""
    return att_gt(*args, **kwargs).summary()


def pdid(*args, **kwargs) -> str:
    """Estimate group-time treatment effects and print the summary."""
    print(att_gt(*args, **kwargs).summary())


def es(*args, **kwargs) -> str:
    """Estimate dynamic effects and return the summary."""
    return att_gt(*args, **kwargs).es_summary()


def pes(*args, **kwargs) -> str:
    """Estimate dynamic effects and print the summary."""
    print(att_gt(*args, **kwargs).es_summary())
