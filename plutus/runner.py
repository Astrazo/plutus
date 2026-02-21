from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from plutus.config import SimulationConfig
from plutus.models import BankrollState, Bet, Game
from plutus.simulation import (
    filter_upcoming_games,
    generate_dummy_games,
    place_bets,
    settle_bets,
)
from plutus.storage import load_state, save_state

STATE_PATH = Path("data/state.json")


@dataclass
class SimulationState:
    """Runtime state for the simulation run."""

    games: List[Game]
    bets: List[Bet]
    bankroll: BankrollState


class SimulationRunner:
    """Coordinates a single simulation cycle."""

    def __init__(self, config: Optional[SimulationConfig] = None) -> None:
        self.config = config or SimulationConfig()

    def load_or_initialize(self) -> SimulationState:
        """Load state from disk or initialize a fresh run."""
        loaded = load_state(STATE_PATH)
        games = loaded.get("games", [])
        bets = loaded.get("bets", [])
        bankroll = loaded.get("bankroll") or BankrollState(
            bank_roll=self.config.starting_cash,
            in_play=0.0,
            profit=0.0,
        )
        return SimulationState(games=games, bets=bets, bankroll=bankroll)

    def run_cycle(self, now: Optional[datetime] = None) -> SimulationState:
        """Run a single place/settle cycle and persist results."""
        current_time = now or datetime.utcnow()
        state = self.load_or_initialize()

        if state.bets:
            state.bets, state.bankroll = settle_bets(
                state.bets, state.games, state.bankroll, current_time, self.config
            )

        new_games = generate_dummy_games(current_time, self.config.max_open_bets)
        new_games = filter_upcoming_games(
            new_games, current_time, self.config.upcoming_window_minutes
        )
        existing_ids = {game.game_id for game in state.games}
        new_games = [game for game in new_games if game.game_id not in existing_ids]
        new_bets, updated_bankroll = place_bets(
            new_games, state.bankroll, self.config, current_time
        )

        combined_games = state.games + new_games
        combined_bets = state.bets + new_bets
        bankroll = updated_bankroll

        save_state(STATE_PATH, combined_games, combined_bets, bankroll)
        return SimulationState(
            games=combined_games, bets=combined_bets, bankroll=bankroll
        )
