from __future__ import annotations

from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "docs"
    files = sorted(root.glob("t*_methodology.md"))
    bt = chr(96)
    block = (
        "## Figure rendering\n\n"
        "Publication-ready static visuals are generated from the existing figure CSV\n"
        "outputs (no data-value changes) using:\n\n"
        f"{bt}{bt}{bt}bash\n"
        "python scripts/run_visuals_all.py\n"
        "python scripts/qa_visuals.py\n"
        f"{bt}{bt}{bt}\n\n"
        "Artifacts:\n\n"
        f"- {bt}visuals/png/*.png{bt}\n"
        f"- {bt}visuals/vector/*.pdf{bt}\n"
        f"- {bt}intermediate/visuals_run_manifest.json{bt}\n\n"
        f"Style and chart standards are documented in "
        f"{bt}docs/quality/README.md#visual-style-guide{bt}.\n"
    )

    for p in files:
        txt = p.read_text(encoding="utf-8", errors="replace")
        txt = txt.replace("\x08", "").replace("\x0b", "").replace("\r", "")
        if "## Figure rendering" in txt:
            txt = txt.split("## Figure rendering")[0].rstrip() + "\n\n" + block
        else:
            txt = txt.rstrip() + "\n\n" + block
        p.write_text(txt + "\n", encoding="utf-8")

    print(f"fixed {len(files)} files")


if __name__ == "__main__":
    main()
