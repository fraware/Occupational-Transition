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


def save_dual(
    fig: plt.Figure,
    stem: str,
    *,
    visual_root: Path | None = None,
    tight_layout: bool = True,
) -> tuple[Path, Path]:
    """Write PNG + PDF.

    Default: ``visuals/png`` and ``visuals/vector`` under repo root.
    Pass ``visual_root`` (e.g. ``docs/states/virginia/visuals``) to write under
    ``<visual_root>/png`` and ``<visual_root>/vector`` instead.

    Set ``tight_layout=False`` when the figure uses fixed axes positions (for example
    ``Figure.add_axes``) and should not be auto-adjusted before save.
    """
    if visual_root is not None:
        pdir = visual_root / "png"
        vdir = visual_root / "vector"
        pdir.mkdir(parents=True, exist_ok=True)
        vdir.mkdir(parents=True, exist_ok=True)
    else:
        ensure_visual_dirs()
        pdir = PNG_DIR
        vdir = VECTOR_DIR
    png = pdir / f"{stem}.png"
    pdf = vdir / f"{stem}.pdf"
    # Keep exported file metadata aligned with the displayed figure title.
    title = ""
    if getattr(fig, "_suptitle", None) is not None:
        title = (fig._suptitle.get_text() or "").strip()
    if not title:
        for ax in fig.axes:
            t = (ax.get_title() or "").strip()
            if t:
                title = t
                break
    if not title:
        title = stem.replace("_", " ")
    if tight_layout:
        fig.tight_layout()
    fig.savefig(png, bbox_inches="tight", metadata={"Title": title})
    fig.savefig(pdf, bbox_inches="tight", metadata={"Title": title})
    plt.close(fig)
    return png, pdf
