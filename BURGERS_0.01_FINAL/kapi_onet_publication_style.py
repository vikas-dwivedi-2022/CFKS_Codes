"""Frozen plotting template for KAPI-ELM publication figures.

The dimensions and typography are defined at final printed size. Panel
labels are intentionally omitted. Keep this module beside experiment
notebooks when a shared external style module is preferred.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib as mpl
import numpy as np
from matplotlib.colors import LogNorm

MM_TO_INCH = 1.0 / 25.4

SINGLE_COLUMN_WIDTH = 88.0 * MM_TO_INCH
DOUBLE_COLUMN_WIDTH = 180.0 * MM_TO_INCH

BLACK = "#222222"
GRAY = "#6E6E6E"
LIGHT_GRAY = "#D9D9D9"
GRID_GRAY = "#E6E6E6"
BLUE = "#0072B2"
SKY_BLUE = "#56B4E9"
GREEN = "#009E73"
ORANGE = "#E69F00"
VERMILLION = "#D55E00"
PURPLE = "#CC79A7"

CMAP_SOLUTION = "viridis"
CMAP_MAGNITUDE = "magma"
CMAP_COEFFICIENT = "RdBu_r"


def apply_publication_style() -> None:
    """Apply the frozen final-size KAPI-ELM style without requiring LaTeX."""
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": [
                "STIX Two Text",
                "STIXGeneral",
                "DejaVu Serif",
            ],
            "mathtext.fontset": "stix",
            "font.size": 8.0,
            "axes.labelsize": 8.5,
            "axes.titlesize": 8.5,
            "axes.titlepad": 3.0,
            "axes.linewidth": 0.7,
            "axes.edgecolor": BLACK,
            "axes.labelcolor": BLACK,
            "axes.facecolor": "white",
            "figure.facecolor": "white",
            "figure.titlesize": 9.0,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "xtick.color": BLACK,
            "ytick.color": BLACK,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "xtick.minor.size": 1.5,
            "ytick.minor.size": 1.5,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.minor.width": 0.55,
            "ytick.minor.width": 0.55,
            "legend.fontsize": 7.0,
            "legend.title_fontsize": 7.0,
            "legend.frameon": False,
            "legend.handlelength": 1.8,
            "legend.handletextpad": 0.5,
            "legend.columnspacing": 1.0,
            "lines.linewidth": 1.35,
            "lines.markersize": 3.5,
            "patch.linewidth": 0.7,
            "grid.color": GRID_GRAY,
            "grid.linewidth": 0.5,
            "grid.alpha": 0.8,
            "figure.dpi": 120,
            "savefig.dpi": 600,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
            "savefig.facecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def add_major_y_grid(ax) -> None:
    """Use a light horizontal grid for line plots only."""
    ax.grid(True, axis="y", which="major")
    ax.grid(False, axis="x")


def format_colorbar(colorbar, label: str | None = None) -> None:
    """Apply consistent colorbar typography and outline width."""
    colorbar.outline.set_linewidth(0.6)
    colorbar.ax.tick_params(
        labelsize=7.0,
        width=0.6,
        length=2.5,
    )
    if label is not None:
        colorbar.set_label(label, fontsize=8.0, labelpad=4.0)


def positive_lognorm(
    array,
    *,
    floor: float = 1.0e-12,
    lower_percentile: float = 2.0,
    upper_percentile: float = 99.5,
) -> LogNorm:
    """Robust logarithmic normalization for nonnegative error magnitudes."""
    values = np.asarray(array, dtype=float)
    positive = values[np.isfinite(values) & (values > floor)]
    if positive.size == 0:
        return LogNorm(vmin=floor, vmax=10.0 * floor)

    vmin = max(
        floor,
        float(np.percentile(positive, lower_percentile)),
    )
    vmax = max(
        10.0 * vmin,
        float(np.percentile(positive, upper_percentile)),
    )
    return LogNorm(vmin=vmin, vmax=vmax)


def save_figure(
    fig,
    stem: str | Path,
    *,
    formats: Iterable[str] = ("pdf", "png"),
    png_dpi: int = 600,
) -> list[Path]:
    """Save vector PDF plus a high-resolution PNG preview."""
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)

    saved_paths: list[Path] = []
    for extension in formats:
        extension = extension.lower().lstrip(".")
        path = stem.with_suffix(f".{extension}")
        kwargs = {
            "bbox_inches": "tight",
            "pad_inches": 0.02,
            "facecolor": "white",
        }
        if extension == "png":
            kwargs["dpi"] = png_dpi
        fig.savefig(path, **kwargs)
        saved_paths.append(path)
    return saved_paths


apply_publication_style()

__all__ = [
    "SINGLE_COLUMN_WIDTH",
    "DOUBLE_COLUMN_WIDTH",
    "BLACK",
    "GRAY",
    "LIGHT_GRAY",
    "GRID_GRAY",
    "BLUE",
    "SKY_BLUE",
    "GREEN",
    "ORANGE",
    "VERMILLION",
    "PURPLE",
    "CMAP_SOLUTION",
    "CMAP_MAGNITUDE",
    "CMAP_COEFFICIENT",
    "apply_publication_style",
    "add_major_y_grid",
    "format_colorbar",
    "positive_lognorm",
    "save_figure",
]
