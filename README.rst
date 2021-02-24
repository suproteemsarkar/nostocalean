===========
Nostocalean
===========

Custom utility functions.

This package contains a collection of utility functions for empirical work in Python.
It's in progress and the API may change often.

Nostocalean includes wrappers for ``fixest::feglm`` and ``fixest::feols``,
which are accessible by running ``est.feglm`` and ``est.feols``. 

There are additional utility methods for OLS: 
``est.reg``, which returns a string regression summary,
and ``est.treg``, which returns a coefficient table.

Example: Given a dataframe ``df`` with columns ``x, y, group_a, group_b`` 
run a regression of ``y`` on ``x`` with group fixed effects, and double cluster:

.. code-block:: python

    from nostocalean import est
    
    summary = est.reg("y ~ x | group_a + group_b", data=df, se="twoway")
    print(summary)

Nostocalean also includes several utility functions, including CES and HARA

Example: To sample a utility function, run:

.. code-block:: python

    from nostocalean.utility_functions import get_utility_function
    get_utility_function()
