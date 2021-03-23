import warnings
from rpy2.robjects import pandas2ri

from nostocalean.est.fixest import feols, feglm, reg, treg, preg

try:
    from nostocalean.est.did import att_gt, did, es, pdid, pes
except:
    warnings.warn("Failed to load did methods")

pandas2ri.activate()