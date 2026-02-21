from pathlib import Path

from plutus.storage import load_state, reset_state


def test_reset_state_deletes_file(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    state_path.write_text("{}", encoding="utf-8")

    reset_state(state_path)

    assert not state_path.exists()
    assert load_state(state_path) == {}
