from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from plutus.models import Bet, BankrollState, Game


def _encode_datetime(value: datetime) -> str:
    return value.isoformat()


def _decode_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _serialize_game(game: Game) -> Dict[str, object]:
    data = asdict(game)
    data["start_time"] = _encode_datetime(game.start_time)
    return data


def _deserialize_game(data: Dict[str, object]) -> Game:
    return Game(
        game_id=str(data["game_id"]),
        sport=str(data["sport"]),
        start_time=_decode_datetime(str(data["start_time"])),
        home_team=str(data["home_team"]),
        away_team=str(data["away_team"]),
        home_win=bool(data["home_win"]),
        data_ready=bool(data.get("data_ready", False)),
    )


def _serialize_bet(bet: Bet) -> Dict[str, object]:
    data = asdict(bet)
    data["placed_at"] = _encode_datetime(bet.placed_at)
    if bet.settled_at is not None:
        data["settled_at"] = _encode_datetime(bet.settled_at)
    return data


def _deserialize_bet(data: Dict[str, object]) -> Bet:
    settled_value = data.get("settled_at")
    return Bet(
        bet_id=str(data["bet_id"]),
        game_id=str(data["game_id"]),
        selection=str(data["selection"]),
        stake=float(data["stake"]),
        odds_multiplier=float(data["odds_multiplier"]),
        placed_at=_decode_datetime(str(data["placed_at"])),
        settled_at=_decode_datetime(str(settled_value)) if settled_value else None,
        result=str(data["result"]) if data.get("result") else None,
        payout=float(data["payout"]) if data.get("payout") is not None else None,
    )


def _serialize_bankroll(bankroll: BankrollState) -> Dict[str, float]:
    return asdict(bankroll)


def _deserialize_bankroll(data: Dict[str, object]) -> BankrollState:
    return BankrollState(
        bank_roll=float(data["bank_roll"]),
        in_play=float(data["in_play"]),
        profit=float(data["profit"]),
    )


def load_state(path: Path) -> Dict[str, object]:
    """Load persisted simulation state from disk."""
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)
    games = [_deserialize_game(item) for item in raw.get("games", [])]
    bets = [_deserialize_bet(item) for item in raw.get("bets", [])]
    bankroll = raw.get("bankroll")
    return {
        "games": games,
        "bets": bets,
        "bankroll": _deserialize_bankroll(bankroll) if bankroll else None,
    }


def save_state(
    path: Path, games: List[Game], bets: List[Bet], bankroll: BankrollState
) -> None:
    """Persist simulation state to disk."""
    payload = {
        "games": [_serialize_game(game) for game in games],
        "bets": [_serialize_bet(bet) for bet in bets],
        "bankroll": _serialize_bankroll(bankroll),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def reset_state(path: Path) -> None:
    """Delete persisted simulation state from disk."""
    if path.exists():
        path.unlink()
