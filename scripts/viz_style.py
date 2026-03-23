"""Shared visual style for publication-ready static figures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
VIS_ROOT = ROOT / "visuals"
PNG_DIR = VIS_ROOT / "png"
VECTOR_DIR = VIS_ROOT / "vector"


@dataclass(frozen=True)
class VizStyle:
    dpi: int = 220
    title_size: int = 12
    axis_size: int = 10
    tick_size: int = 9
    legend_size: int = 9
    line_width: float = 2.0
    marker_size: float = 5.0
    grid_alpha: float = 0.28
    facecolor: str = "white"
    high_color: str = "#1f77b4"
    middle_color: str = "#ff7f0e"
    low_color: str = "#2ca02c"
    neutral_color: str = "#4d4d4d"
    palette_sector: tuple[str, ...] = (
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
    )


STYLE = VizStyle()


def apply_matplotlib_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": STYLE.dpi,
            "savefig.dpi": STYLE.dpi,
            "figure.facecolor": STYLE.facecolor,
            "axes.facecolor": STYLE.facecolor,
            "axes.titlesize": STYLE.title_size,
            "axes.labelsize": STYLE.axis_size,
            "xtick.labelsize": STYLE.tick_size,
            "ytick.labelsize": STYLE.tick_size,
            "legend.fontsize": STYLE.legend_size,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": STYLE.grid_alpha,
            "grid.linestyle": "--",
            "font.family": "DejaVu Sans",
        }
    )


def ensure_visual_dirs() -> None:
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)


def save_dual(fig: plt.Figure, stem: str) -> tuple[Path, Path]:
    ensure_visual_dirs()
    png = PNG_DIR / f"{stem}.png"
    pdf = VECTOR_DIR / f"{stem}.pdf"
    fig.tight_layout()
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    return png, pdf
