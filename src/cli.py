from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone

from src.config import SimulationConfig
from src.runner import STATE_PATH, SimulationRunner, SimulationState
from src.storage import reset_state


def _print_state_summary(
    state: SimulationState, show_details: bool, open_only: bool
) -> None:
    """Print the simulation summary and optional detail sections.

    Args:
        state: Simulation state returned by the runner.
        show_details: Whether to print detailed games and bets.
    """
    print("Simulation cycle complete")
    print(f"Bankroll: ${state.bankroll.bank_roll:.2f}")
    print(f"In-play: ${state.bankroll.in_play:.2f}")
    print(f"Profit: ${state.bankroll.profit:.2f}")
    print(f"Total games tracked: {len(state.games)}")
    print(f"Total bets tracked: {len(state.bets)}")
    if show_details:
        print("\nGames:")
        for game in state.games:
            print(
                " - "
                f"{game.game_id} | {game.sport} | {game.start_time.isoformat()} | "
                f"{game.away_team} @ {game.home_team} | home_win={game.home_win} | "
                f"data_ready={game.data_ready}"
            )
        print("\nBets:")
        bets = state.bets
        if open_only:
            bets = [bet for bet in bets if bet.result is None]
        for bet in bets:
            payout = f"{bet.payout:.2f}" if bet.payout is not None else "--"
            print(
                " - "
                f"{bet.bet_id} | game={bet.game_id} | selection={bet.selection} | "
                f"stake={bet.stake:.2f} | odds={bet.odds_multiplier:.2f} | "
                f"placed_at={bet.placed_at.isoformat()} | "
                f"settled_at={bet.settled_at.isoformat() if bet.settled_at else 'open'} | "
                f"result={bet.result or 'open'} | "
                f"payout={payout}"
            )


def main() -> None:
    """Entry point for running a simulation cycle."""
    parser = argparse.ArgumentParser(description="Run a simulation cycle.")
    parser.add_argument(
        "--show-details",
        action="store_true",
        help="Print detailed games and bets after the cycle.",
    )
    parser.add_argument(
        "--open-only",
        action="store_true",
        help="Show only open bets in detailed output.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run continuously until interrupted.",
    )
    parser.add_argument(
        "--interval-seconds",
        type=int,
        default=SimulationConfig().poll_interval_seconds,
        help="Seconds to wait between cycles in live mode.",
    )
    parser.add_argument(
        "--reset-state",
        action="store_true",
        help="Clear persisted state before running.",
    )
    parser.add_argument(
        "--reset-only",
        action="store_true",
        help="Clear persisted state and exit without running a cycle.",
    )
    args = parser.parse_args()

    runner = SimulationRunner()
    if args.reset_state or args.reset_only:
        reset_state(STATE_PATH)
        print(f"State reset: {STATE_PATH}")
        if args.reset_only:
            return

    if args.live:
        try:
            while True:
                state = runner.run_cycle(datetime.now(timezone.utc))
                _print_state_summary(state, args.show_details, args.open_only)
                time.sleep(args.interval_seconds)
        except KeyboardInterrupt:
            print("\nLive run interrupted. Exiting.")
    else:
        state = runner.run_cycle(datetime.now(timezone.utc))
        _print_state_summary(state, args.show_details, args.open_only)


if __name__ == "__main__":
    main()
