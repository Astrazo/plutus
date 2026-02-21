from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Game:
    """Represents a single game with a known outcome in simulation."""

    game_id: str
    sport: str
    start_time: datetime
    home_team: str
    away_team: str
    home_win: bool
    data_ready: bool = False


@dataclass(frozen=True)
class Bet:
    """Represents a bet placed on a game."""

    bet_id: str
    game_id: str
    selection: str
    stake: float
    odds_multiplier: float
    placed_at: datetime
    settled_at: Optional[datetime] = None
    result: Optional[str] = None  # "win" or "loss"
    payout: Optional[float] = None


@dataclass(frozen=True)
class BankrollState:
    """Tracks bankroll, in-play money, and profit."""

    bank_roll: float
    in_play: float
    profit: float
