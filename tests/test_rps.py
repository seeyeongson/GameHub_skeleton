"""Test round outcomes, input validation, scoring, draws, and returning to the hub."""

import pytest

from games import rps


@pytest.mark.parametrize(
    "player, computer, expected",
    [
        ("1", "1", "draw"),
        ("1", "2", "lose"),
        ("1", "3", "win"),
        ("2", "1", "win"),
        ("2", "2", "draw"),
        ("2", "3", "lose"),
        ("3", "1", "lose"),
        ("3", "2", "win"),
        ("3", "3", "draw"),
    ],
)
def test_decide(player, computer, expected):
    assert rps.decide(player, computer) == expected


@pytest.mark.parametrize(
    "player, computer", [("abc", "1"), ("1", "9"), ("0", "2"), ("", "3")]
)
def test_decide_rejects_invalid_choices(player, computer):
    with pytest.raises(ValueError):
        rps.decide(player, computer)


def test_play_player_wins_and_returns(monkeypatch, capsys):
    answers = iter(["2", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(rps.random, "choice", lambda _: "1")
    assert rps.play() is None
    output = capsys.readouterr().out
    assert "점수: 나 2 - 컴퓨터 0" in output
    assert "최종 결과: 승리!" in output


def test_play_computer_wins_and_returns(monkeypatch, capsys):
    answers = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(rps.random, "choice", lambda _: "2")
    assert rps.play() is None
    output = capsys.readouterr().out
    assert "점수: 나 0 - 컴퓨터 2" in output
    assert "최종 결과: 패배!" in output


def test_play_retries_invalid_input_and_draw(monkeypatch, capsys):
    answers = iter(["abc", "9", "--3", "1", " 2 ", "2"])
    computers = iter(["1", "1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(rps.random, "choice", lambda _: next(computers))
    assert rps.play() is None
    output = capsys.readouterr().out
    assert output.count("0, 1, 2, 3 중 하나를 입력하세요.") == 3
    assert "무승부입니다!" in output
    assert "점수: 나 2 - 컴퓨터 0" in output


def test_play_zero_returns_to_menu(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "0")
    assert rps.play() is None
    assert "메인 메뉴로 돌아갑니다." in capsys.readouterr().out
