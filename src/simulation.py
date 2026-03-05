from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import List, Tuple
from uuid import uuid4

from src.config import SimulationConfig, calculate_profit
from src.models import BankrollState, Bet, Game


def generate_dummy_games(start_time: datetime, count: int) -> List[Game]:
    """Generate dummy games with random outcomes."""
    games: List[Game] = []
    for index in range(count):
        game_id = f"GAME-{uuid4().hex[:8]}"
        games.append(
            Game(
                game_id=game_id,
                sport="NBA",
                start_time=start_time + timedelta(minutes=index * 15),
                home_team=f"HOME-{index + 1}",
                away_team=f"AWAY-{index + 1}",
                home_win=random.choice([True, False]),
                data_ready=random.choice([True, False]),
            )
        )
    return games


def filter_upcoming_games(
    games: List[Game], now: datetime, window_minutes: int
) -> List[Game]:
    """Filter games to those starting within the upcoming window."""
    window_end = now + timedelta(minutes=window_minutes)
    return [game for game in games if now <= game.start_time <= window_end]


def place_bets(
    games: List[Game],
    bankroll: BankrollState,
    config: SimulationConfig,
    placed_at: datetime,
) -> Tuple[List[Bet], BankrollState]:
    """Place bets on a list of games while bankroll permits."""
    bets: List[Bet] = []
    available = bankroll.bank_roll
    for game in games:
        if not game.data_ready:
            continue
        if available < config.bet_amount:
            break
        selection = game.home_team
        bet = Bet(
            bet_id=f"BET-{uuid4().hex[:8]}",
            game_id=game.game_id,
            selection=selection,
            stake=config.bet_amount,
            odds_multiplier=config.odds_multiplier,
            placed_at=placed_at,
        )
        bets.append(bet)
        available -= config.bet_amount
    updated = BankrollState(
        bank_roll=bankroll.bank_roll - len(bets) * config.bet_amount,
        in_play=bankroll.in_play + len(bets) * config.bet_amount,
        profit=bankroll.profit,
    )
    return bets, updated


def settle_bets(
    bets: List[Bet],
    games: List[Game],
    bankroll: BankrollState,
    settled_at: datetime,
    config: SimulationConfig,
) -> Tuple[List[Bet], BankrollState]:
    """Settle all open bets using game outcomes."""
    game_lookup = {game.game_id: game for game in games}
    settled_bets: List[Bet] = []
    bank_roll = bankroll.bank_roll
    in_play = bankroll.in_play

    for bet in bets:
        game = game_lookup.get(bet.game_id)
        if game is None:
            settled_bets.append(bet)
            continue
        win = game.home_win and bet.selection == game.home_team
        payout = bet.stake * bet.odds_multiplier if win else 0.0
        bank_roll += payout
        in_play -= bet.stake
        settled_bets.append(
            Bet(
                bet_id=bet.bet_id,
                game_id=bet.game_id,
                selection=bet.selection,
                stake=bet.stake,
                odds_multiplier=bet.odds_multiplier,
                placed_at=bet.placed_at,
                settled_at=settled_at,
                result="win" if win else "loss",
                payout=payout,
            )
        )

    updated = BankrollState(
        bank_roll=bank_roll,
        in_play=in_play,
        profit=calculate_profit(bank_roll, config.starting_cash),
    )
    return settled_bets, updated
