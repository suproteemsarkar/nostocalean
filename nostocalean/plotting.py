"""Custom pyplot style and palette."""

import matplotlib.pyplot as plt
import colorcet as cc
import seaborn as sns

plt.rcParams.update(
    {
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "figure.figsize": (7, 4.33),
        "lines.linewidth": 2,
        "axes.spines.bottom": False,
        "axes.spines.top": False,
        "axes.spines.left": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "ytick.left": False,
        "grid.linewidth": 0.8,
        "grid.alpha": 0.8,
        "font.family": "Lato",
        "font.weight": "regular",
    }
)

cmap = cc.cm.glasbey_bw
sns.set_palette([cmap(i) for i in range(cmap.N)])
palette = sns.color_palette()
