# Start Here

This page is the fastest way to use the repo regardless of background.

## 1) Choose your goal

- **Run one analysis quickly**: use the `quick-start` profile.
- **Rebuild main paper outputs**: use the `core-paper` profile.
- **Run full strict replication**: use `full-replication` or `release-signoff`.
- **Explore sources only**: use `ot list-sources`, `ot btos`, `ot jolts`.

## 2) Install and run

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

### Profile-driven run

```bash
ot run --profile config/profiles/quick-start.toml
```

### CLI-driven run

```bash
ot run --bundle core-paper --source-selection-mode latest_mode
```

## 3) Discover options

```bash
ot list-analyses
ot list-sources
```

## 4) Pick source policy

- `latest_mode`: monitor current data and rolling updates.
- `freeze_mode`: enforce comparability for release-grade replication.

See [source_selection.md](source_selection.md) for details.

## 5) Understand outputs

- Main analysis outputs: `figures/`
- Rebuild metadata and logs: `intermediate/`
- Methods and assumptions: `docs/methodology/`
