from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.image as mpimg

from viz_style import PNG_DIR, VECTOR_DIR
from viz_utils import ROOT, sha256_file

EXPECTED_STEMS = [
    "occupation_share_barh",
    "task_heatmap",
    "hours_timeseries",
    "transition_counts_heatmap_latest",
    "transition_summary_metrics",
    # Manuscript-ready stack of Figure 2 Panel A + Panel B summary grid.
    "figure2_redesigned_composite",
    "btos_ai_trends",
    "btos_workforce_effects_barh",
    # Manuscript-ready stack of Figure 3 panels (PIL composite; same CSV contract).
    "figure3_redesigned_composite",
    "jolts_openings_rate",
    "ces_payroll_index",
    "figure4_redesigned_composite",
    "capability_matrix_heatmap",
    "policy_roadmap",
    "asec_mean_income",
    "sipp_event_employment",
    "cps_supp_mobility_share",
    "abs_measure_shares",
    "ces_payroll_index_mean",
    "bed_gross_job_gains",
    "qcew_top20_state_employment",
    "lehd_benchmark_rate",
    "top30_puma_high_ai_share",
    "nls_occupation_switch_rate",
]

SOURCE_CSVS = sorted((ROOT / "figures").glob("*.csv"))
MANIFEST = ROOT / "intermediate" / "visuals_run_manifest.json"


def _check_png_readable(path: Path) -> None:
    arr = mpimg.imread(path)
    if arr.size == 0:
        raise ValueError(f"empty image array: {path}")


def main() -> int:
    errors: list[str] = []
    outputs: list[dict[str, str | int]] = []
    for stem in EXPECTED_STEMS:
        png = PNG_DIR / f"{stem}.png"
        pdf = VECTOR_DIR / f"{stem}.pdf"
        for p in (png, pdf):
            if not p.is_file():
                errors.append(f"missing visual output: {p}")
                continue
            if p.stat().st_size <= 0:
                errors.append(f"empty visual output: {p}")
        if png.is_file():
            try:
                _check_png_readable(png)
            except Exception as exc:
                errors.append(f"unreadable PNG {png}: {exc}")
        if png.is_file() and pdf.is_file():
            outputs.append(
                {
                    "stem": stem,
                    "png_path": str(png.relative_to(ROOT)).replace("\\", "/"),
                    "pdf_path": str(pdf.relative_to(ROOT)).replace("\\", "/"),
                    "png_sha256": sha256_file(png),
                    "pdf_sha256": sha256_file(pdf),
                    "png_bytes": int(png.stat().st_size),
                    "pdf_bytes": int(pdf.stat().st_size),
                }
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_csv_sha256": [
            {
                "path": str(p.relative_to(ROOT)).replace("\\", "/"),
                "sha256": sha256_file(p),
            }
            for p in SOURCE_CSVS
        ],
        "outputs": outputs,
    }
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"QA OK: visuals ({len(outputs)} stems). Manifest: {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
