from rpy2.robjects import pandas2ri

from nostocalean.est.fixest import feols, feglm, reg, treg, preg
from nostocalean.est.did import att_gt, did, es, pdid, pes

pandas2ri.activate()