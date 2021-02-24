===========
Nostocalean
===========

Custom utility functions.

Nostocalean includes a wrapper for ``fixest::feols``. 

Example: Given a dataframe ``df`` with columns ``x, y, group, time`` 
run a regression of ``y`` on ``x`` with group and time fixed effects, and double cluster:

.. code-block:: python

    from nostocalean import ols
    
    summary = ols.reg("y ~ x | group + time", data=df, se="twoway")
    print(summary)

To sample a utility function, run:

.. code-block:: python

    from nostocalean.utility_functions import get_utility_function
    get_utility_function()
