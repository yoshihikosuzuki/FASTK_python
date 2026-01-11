from collections import Counter
from dataclasses import dataclass
from typing import List, Optional

import plotly_light as pl

from ._hist import Hist


@dataclass
class Pread:
    """Read with a count profile.

    positional arguments:
      @ id     : Read ID (1-indexed).
      @ K      : Of k-mers.
      @ counts : Count profile. `length(seq) == length(counts) == length(states) == self.length`

    optional arguments:
      @ _seq   : Nucleotide sequence of the entire read.
      @ states : Label (E/H/D/R) for each k-mer.
      @ name   : Read Name.

    instance variables:
      @ seq    : == `_seq[K - 1:]`. The length is same as the count profile.
      @ length : Length of the count profile (i.e. shorter than original read length).
    """

    id: int
    K: int
    counts: list[int]
    _seq: str | None = None
    states: list[str] | None = None
    name: str | None = None

    @property
    def seq(self) -> str:
        assert self._seq is not None, "`_seq` is None"
        return self._seq[self.K - 1 :]

    @property
    def length(self) -> int:
        return len(self.counts)

    @property
    def _length(self) -> int:
        return self.length + self.K - 1

    def __post_init__(self):
        assert self._seq is None or self.length == len(self.seq)
        assert self.states is None or self.length == len(self.states)

    def __repr__(self) -> str:
        var_names = ["id", "name", "K", "_seq", "counts", "states"]
        var_reprs = ", ".join(map(lambda x: f"{x}={repr(getattr(self, x))}", var_names))
        return f"{self.__class__.__name__}({var_reprs})"

    def to_hist(self, min_count: int = 1, max_count: int = 100) -> Hist:
        """Convert count profile to histogram.

        optional arguments:
          @ max_count : Maximum k-mer count.
                        Larger counts are capped to this value.
        """
        return Hist(
            Counter(
                self.counts
                if max_count is None
                else [min(count, max_count) for count in self.counts]
            ),
            min_count,
            max_count,
        )

    def show(
        self,
        # options for trace
        add_bases: bool = False,
        use_webgl: bool = True,
        # options for layout
        max_count: Optional[int] = None,
        max_count_zoom: Optional[int] = 100,
        width: Optional[int] = 1000,
        height: Optional[int] = 500,
        layout: Optional[pl.Layout] = None,
        # return options
        return_trace: bool = False,
        return_fig: bool = False,
    ) -> List[pl.BaseTraceType] | pl.Figure | None:
        """
        optional arguments:
          @ max_count      : Maximum k-mer count.
                             Larger counts are capped to this value.
          @ max_count_zoom : If not None, make a button zooming in to [0,`max_count_zoom`].
          @ layout         : Additional layout.
          @ return_fig     : If True, return a `go.Figure` object.
        """
        traces = []
        # Counts trace
        pos_list = list(range(self.length))
        capped_counts = [
            cnt if max_count is None else min(cnt, max_count) for cnt in self.counts
        ]
        texts = [
            f"pos = {i} (-(k-1)={i-self.K+1}, +(k-1)={i+self.K-1}), count = {c}<br>"
            f"k-mer = {self._seq[i:i + self.K] if self._seq is not None else '-'}"
            for i, c in enumerate(self.counts)
        ]
        traces.append(
            pl.scatter(
                x=pos_list,
                y=capped_counts,
                text=texts,
                mode="markers+lines",
                col="black",
                name="Counts",
                show_legend=False,
                use_webgl=use_webgl,
            )
        )
        # Bases trace
        if add_bases:
            traces.append(
                pl.scatter(
                    x=pos_list,
                    y=capped_counts,
                    text=list(self.seq),
                    text_col="black",
                    text_pos="top center",
                    mode="text",
                    name="Bases",
                    show_legend=True,
                    show_init=False,
                    use_webgl=use_webgl,
                )
            )
        if return_trace:
            return traces

        _layout = pl.layout(
            width=width,
            height=height,
            x_title="Position",
            y_title=(
                "K-mer count"
                if max_count is None
                else f"K-mer count (capped at {max_count})"
            ),
            xy_grid=True,
        )
        fig = pl.figure(traces, pl.merge_layout(_layout, layout))
        if max_count_zoom is not None and (
            max_count is None or max_count_zoom < max_count
        ):
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        x=0.01,
                        xanchor="left",
                        y=1.02,
                        yanchor="bottom",
                        # font={"size": 12},
                        # pad={"t": 0, "r": 0, "b": 0, "l": 0},
                        # borderwidth=1,
                        buttons=[
                            dict(
                                label=f"<{max_count_zoom}",
                                method="relayout",
                                args=[
                                    {
                                        "yaxis.range[0]": 0,
                                        "yaxis.range[1]": max_count_zoom + 1,
                                    }
                                ],
                            )
                        ],
                    )
                ]
            )
        return fig if return_fig else pl.show(fig)
