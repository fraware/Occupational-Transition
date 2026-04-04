# Local scheduling for catalog refresh

Use `ot refresh` to batch-download rows from [docs/data_registry.csv](../data_registry.csv) into `raw/` (or `OT_RAW_DIR`). This is intended for **your machine** (Task Scheduler, cron, or a user-level job runner), not for required CI.

## Behavior

- **Targets:** pass `--cadence rolling` (or `static`, `annual`) and/or repeat `--dataset-id`.
- **Freeze mode:** if the environment has `SOURCE_SELECTION_MODE=freeze_mode` (see [source_selection.md](../source_selection.md)), refresh **does nothing** unless you pass `--allow-in-freeze-mode`.
- **Logs:** by default, append JSON lines under `intermediate/refresh_<UTC>.jsonl` (gitignored). Override with `--log path`.

## Examples

From the repository root, after `pip install -e .`:

```bash
ot catalog --cadence rolling
ot refresh --cadence rolling --dry-run
ot refresh --cadence rolling
ot refresh --dataset-id bls_jt_industry --dataset-id bls_ce_supersector
```

## Windows Task Scheduler

1. Action: **Start a program** — `python` (or full path to your venv `python.exe`).
2. Arguments: `-m occupational_transition.cli refresh --cadence rolling` (add `--raw-dir D:\data\ot_raw` if you use a non-default cache).
3. **Start in:** your clone root (the directory that contains `docs/` and `src/`).
4. Optional: set a user-level environment variable `OT_RAW_DIR` to a dedicated cache disk.

## cron (Unix)

```cron
15 6 * * 1 cd /path/to/Occupational-Transition && /path/to/venv/bin/python -m occupational_transition.cli refresh --cadence rolling >> /var/log/ot_refresh.log 2>&1
```

## Related

- `ot fetch --program BLS_JOLTS` — full JOLTS LABSTAT provenance bundle plus per-row registry fetches.
- [Replication README](../replication/README.md) — full pipeline from raw.
