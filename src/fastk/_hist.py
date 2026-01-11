from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import plotly_light as pl


@dataclass
class Hist:
    """K-mer histogram object with plotting functions."""

    freq: list[tuple[int, int]] | Counter
    min_count: int
    max_count: int
    unique: bool = False

    def __post_init__(self):
        if isinstance(self.freq, list):
            self.freq = Counter({k: v for k, v in self.freq})

    @property
    def rel_freq(self):
        tot = sum(self.freq.values())
        return Counter({k: v / tot * 100 for k, v in self.freq.items()})

    def show(
        self,
        # options for trace
        relative: bool = False,
        bin_size: int = 1,
        name: str | None = None,
        col: str | None = None,
        opacity: float = 1,
        show_legend: bool = False,
        use_histogram: bool = False,
        # options for layout
        width: int = 500,
        height: int = 500,
        layout: pl.Layout | None = None,
        barmode: str = "overlay",
        # return options
        return_trace: bool = False,
        return_fig: bool = False,
    ) -> pl.BaseTraceType | pl.Figure | None:
        trace = pl.hist(
            self.freq if not relative else self.rel_freq,
            bin_size=bin_size,
            col=col,
            opacity=opacity,
            name=name,
            show_legend=show_legend,
            use_histogram=use_histogram,
        )
        if return_trace:
            return trace
        _layout = pl.layout(
            width=width,
            height=height,
            x_title="K-mer count",
            y_title=("Frequency" if not relative else "Relative frequency [%]"),
            xy_grid=True,
            barmode=barmode,
        )
        fig = pl.figure(trace, pl.merge_layout(_layout, layout))
        return fig if return_fig else pl.show(fig)
