===========
Nostocalean
===========

Custom utility functions.

This package contains a collection of utility functions for empirical work in Python.
It's in progress and the API may change often. In addition to custom utility methods,
the package includes wrappers for `fixest <https://github.com/lrberge/fixest>`_ 
and `did <https://github.com/bcallaway11/did>`_.

Example: Given a dataframe ``df`` with columns ``x, y, group_a, group_b`` 
run a regression of ``y`` on ``x`` with group fixed effects, and double cluster:

.. code-block:: python

    from nostocalean import est
    
    summary = est.reg("y ~ x | group_a + group_b", data=df, se="twoway")
    print(summary)

Example: Given a dataframe ``df`` with columns ``y, first_treat, group, time``
report event study (aggregated group-time) estimates:

.. code-block:: python

    from nostocalean import est

    summary = est.es(y="y", d="first_treat", g="group", t="time", data=df)
    print(summary)

Nostocalean also includes several utility functions, including CES and HARA

Example: To sample a utility function, run:

.. code-block:: python

    from nostocalean.utility_functions import get_utility_function
    get_utility_function()
