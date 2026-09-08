# AGENTS.md

## Role

Act as a senior software and ML engineer contributing to this project.

Before making substantial changes, understand how the proposed solution fits
into the wider architecture. Prefer incremental changes and clearly explain
important design decisions, trade-offs, and assumptions.

## Project

Plutus is a paper-trading system for sports markets.

The initial goal is to simulate sports betting using machine-learning models
without placing real-money bets.

The system will track:

- Available bankroll
- Capital currently in play
- Profit/loss relative to starting capital

The intended workflow is:

1. Retrieve upcoming games from external sports APIs.
2. Build model features for each game.
3. Run inference to predict the winner.
4. Apply configurable criteria to decide whether to place a simulated bet.
5. Move the stake from bankroll to in-play capital.
6. Record the simulated bet and game identifier.
7. Retrieve the final result when the game completes.
8. Settle the simulated bet and update bankroll and profit/loss.
9. Repeat across supported games and models.

For early development, assume decimal odds of `1.90`.

Future work may include live-game monitoring and simulated cash-out logic.

The backend is written in Python. The frontend may use JavaScript, HTML, and
CSS and will initially run locally.

## Conventions

- Prefer the simplest solution that satisfies the requirement.
- Prioritize core functionality over unnecessary abstraction.
- Use type hints for Python code.
- Use Google-style docstrings for functions.
- Place tests in `tests/` and use `pytest`.
- Format and lint Python consistently using tools such as Black and Pylint.
- Use a project virtual environment.
- Prefer pandas DataFrames for model-oriented tabular processing where appropriate.
- Implement sensible error handling for expected failure modes.
- Record dependencies in `requirements.txt`.
- Do not remove dependencies without first explaining why the change is needed.

## Verification

For new functions or modules:

- Add appropriate unit tests.
- Test integration with affected components where practical.
- Review the implementation after tests pass.
- Consider whether the solution can be simplified.
- For larger changes, work incrementally and validate each stage.

## Safety

- Never expose API keys or other secrets.
- Store secrets in `.env` and load them through environment variables.
- Do not commit or push changes unless explicitly instructed.

## Development Philosophy

Keep the project simple, understandable, and enjoyable to work on.