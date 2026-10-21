from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_cumulative(dates: list[datetime], totals: list[float], out: str | Path) -> Figure:
    figure, axes = plt.subplots()
    axes.plot(dates, totals)
    axes.set_xlabel("Year")
    axes.set_ylabel("Cumulative EVA duration (hours)")
    figure.tight_layout()
    figure.savefig(out)
    return figure
