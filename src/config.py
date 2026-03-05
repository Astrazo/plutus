from dataclasses import dataclass


def calculate_profit(current_bankroll: float, starting_cash: float) -> float:
    """Calculate profit relative to starting cash."""
    return current_bankroll - starting_cash


@dataclass(frozen=True)
class SimulationConfig:
    """Configuration values for simulation runs."""

    starting_cash: float = 100.0
    bet_amount: float = 10.0
    odds_multiplier: float = 1.90
    max_open_bets: int = 4
    poll_interval_seconds: int = 30
    upcoming_window_minutes: int = 60
