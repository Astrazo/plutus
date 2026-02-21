# plutus
Paper Trader (sports game paper-betting simulation)

## Current Status (as of 2026-02-21)
- A minimal simulation loop exists and persists state in `data/state.json`.
- CLI supports one-shot runs or continuous live-style polling.
- Bets are placed only on games marked `data_ready=True` (placeholder for model data readiness).
- Upcoming-game filtering is enforced for games starting within the next 60 minutes.
- Tests exist for core simulation functions and storage reset.

## How To Run
Use the venv Python:
```bash
.venv/bin/python -m plutus.cli
```

### Useful Flags
- `--live` run continuously until interrupted
- `--interval-seconds N` set loop interval (default 30)
- `--show-details` print full games/bets lists
- `--open-only` show only open bets in detailed output
- `--reset-state` clear `data/state.json` then run
- `--reset-only` clear `data/state.json` and exit

### Example
```bash
.venv/bin/python -m plutus.cli --live --interval-seconds 30 --show-details --open-only
```

## Project Notes for New Contributors
- `plutus/runner.py` is the coordinator. It loads state, settles bets, generates games, places new bets, and saves state.
- `plutus/simulation.py` contains the dummy-game generator, bet placement, and settlement logic.
- `plutus/storage.py` handles JSON persistence.
- `plutus/models.py` defines `Game`, `Bet`, and `BankrollState`.
- `plutus/cli.py` is the entry point (argparse-based).

## Tests
```bash
.venv/bin/pytest -q
```

## Known Gaps / Next Steps
- Replace dummy game generator with real game provider APIs.
- Replace `data_ready` placeholder with real readiness checks (lineups, weather, etc.).
- Add model inference (currently selects home team by default).
- Add sportsbook odds integration (currently uses fixed 1.90 multiplier).
- Consider long-running state growth (rotation/archival of `data/state.json`).

## Simulation
A minimal simulation runner is available for testing the bankroll lifecycle before APIs and models are integrated.

### Run a single cycle
```bash
python -m plutus.cli
```

### Run continuously (every 30 seconds)
```bash
python -m plutus.cli --live --interval-seconds 30
```

### Show detailed games and bets
```bash
python -m plutus.cli --show-details
```

### Show only open bets with details
```bash
python -m plutus.cli --show-details --open-only
```

### Reset state before running
```bash
python -m plutus.cli --reset-state
```

### Reset state and exit
```bash
python -m plutus.cli --reset-only
```

### Notes
- State persists to `data/state.json` to allow resume between runs.
- Defaults: $100 starting bankroll, $10 stake per bet, 1.90 odds, 4 concurrent games.
