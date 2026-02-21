from dataclasses import replace
from datetime import datetime, timezone

from plutus.config import SimulationConfig
from plutus.models import BankrollState
from datetime import timedelta

from plutus.simulation import (
    filter_upcoming_games,
    generate_dummy_games,
    place_bets,
    settle_bets,
)


def test_generate_dummy_games_count_and_uniqueness() -> None:
    now = datetime.now(timezone.utc)
    games = generate_dummy_games(now, 4)
    assert len(games) == 4
    assert len({game.game_id for game in games}) == 4


def test_place_bets_respects_bankroll() -> None:
    config = SimulationConfig(starting_cash=100.0, bet_amount=10.0, max_open_bets=4)
    bankroll = BankrollState(bank_roll=15.0, in_play=0.0, profit=0.0)
    games = generate_dummy_games(datetime.now(timezone.utc), 4)

    bets, updated = place_bets(games, bankroll, config, datetime.now(timezone.utc))

    assert len(bets) == 1
    assert updated.bank_roll == 5.0
    assert updated.in_play == 10.0


def test_place_bets_skips_unready_games() -> None:
    config = SimulationConfig(starting_cash=100.0, bet_amount=10.0, max_open_bets=4)
    bankroll = BankrollState(bank_roll=50.0, in_play=0.0, profit=0.0)
    now = datetime.now(timezone.utc)
    games = generate_dummy_games(now, 2)
    games = [
        replace(games[0], data_ready=False),
        replace(games[1], data_ready=True),
    ]

    bets, updated = place_bets(games, bankroll, config, now)

    assert len(bets) == 1
    assert updated.in_play == config.bet_amount


def test_settle_bets_updates_bankroll_and_profit() -> None:
    config = SimulationConfig(
        starting_cash=100.0, bet_amount=10.0, odds_multiplier=1.90
    )
    now = datetime.now(timezone.utc)
    games = generate_dummy_games(now, 1)
    game = games[0]
    games[0] = game.__class__(
        game_id=game.game_id,
        sport=game.sport,
        start_time=game.start_time,
        home_team=game.home_team,
        away_team=game.away_team,
        home_win=True,
        data_ready=True,
    )
    bankroll = BankrollState(bank_roll=90.0, in_play=10.0, profit=-10.0)

    bets, _ = place_bets(games, bankroll, config, now)
    settled, updated = settle_bets(bets, games, bankroll, now, config)

    assert settled[0].result == "win"
    assert updated.in_play == 0.0
    assert updated.bank_roll == 90.0 + 19.0
    assert updated.profit == (updated.bank_roll - config.starting_cash)


def test_filter_upcoming_games_limits_window() -> None:
    now = datetime.now(timezone.utc)
    games = [
        generate_dummy_games(now - timedelta(minutes=5), 1)[0],
        generate_dummy_games(now + timedelta(minutes=10), 1)[0],
        generate_dummy_games(now + timedelta(hours=2), 1)[0],
    ]

    upcoming = filter_upcoming_games(games, now, 60)

    assert len(upcoming) == 1
    assert upcoming[0].start_time >= now
