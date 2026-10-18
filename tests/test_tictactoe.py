"""틱택토 테스트: 규칙 함수(순수 함수)와 play() 진행 흐름을 검사한다."""

import pytest

from games import tictactoe


def feed(monkeypatch, answers):
    """input()이 호출될 때마다 answers를 차례로 돌려주도록 바꾼다."""
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda _: next(it))


# ---------- 규칙 함수 ----------


def test_new_board_is_empty():
    board = tictactoe.new_board()
    assert len(board) == 9
    assert all(cell == tictactoe.EMPTY for cell in board)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("1", 0),
        ("9", 8),
        (" 5 ", 4),
        ("0", None),
        ("10", None),
        ("a", None),
        ("", None),
    ],
)
def test_parse_move(text, expected):
    assert tictactoe.parse_move(text) == expected


def test_place_mark_does_not_modify_original():
    board = tictactoe.new_board()
    new = tictactoe.place_mark(board, 4, "X")
    assert new[4] == "X"
    assert board[4] == tictactoe.EMPTY


def test_place_mark_on_taken_cell_raises():
    board = tictactoe.place_mark(tictactoe.new_board(), 0, "X")
    with pytest.raises(ValueError):
        tictactoe.place_mark(board, 0, "O")


def test_is_valid_move():
    board = tictactoe.place_mark(tictactoe.new_board(), 0, "X")
    assert tictactoe.is_valid_move(board, 1)
    assert not tictactoe.is_valid_move(board, 0)
    assert not tictactoe.is_valid_move(board, 9)
    assert not tictactoe.is_valid_move(board, -1)
    assert not tictactoe.is_valid_move(board, None)


@pytest.mark.parametrize("line", tictactoe.WIN_LINES)
def test_get_winner_all_lines(line):
    board = tictactoe.new_board()
    for i in line:
        board[i] = "O"
    assert tictactoe.get_winner(board) == "O"


def test_get_winner_none():
    assert tictactoe.get_winner(tictactoe.new_board()) is None


def test_draw():
    board = list("XOXXOOOXX")
    assert tictactoe.is_full(board)
    assert tictactoe.get_winner(board) is None
    assert tictactoe.is_draw(board)


def test_not_draw_when_winner_exists():
    board = list("XXXOO    ")
    assert tictactoe.get_winner(board) == "X"
    assert not tictactoe.is_draw(board)


def test_next_player():
    assert tictactoe.next_player("X") == "O"
    assert tictactoe.next_player("O") == "X"


def test_format_board_shows_numbers_for_empty_cells():
    text = tictactoe.format_board(tictactoe.place_mark(tictactoe.new_board(), 0, "X"))
    assert "X" in text
    assert "9" in text


# ---------- play() 진행 흐름 (input 흉내) ----------


def test_play_x_wins(monkeypatch, capsys):
    # X:1,2,3 / O:4,5 → X가 윗줄 완성
    feed(monkeypatch, ["1", "4", "2", "5", "3"])
    tictactoe.play()
    assert "X 승리" in capsys.readouterr().out


def test_play_draw(monkeypatch, capsys):
    feed(monkeypatch, ["1", "2", "3", "5", "4", "6", "8", "7", "9"])
    tictactoe.play()
    assert "무승부" in capsys.readouterr().out


def test_play_retries_on_invalid_input(monkeypatch, capsys):
    # 문자, 범위 밖 숫자 → 재입력 요구, 이후 정상 입력 뒤 q로 종료
    feed(monkeypatch, ["a", "0", "5", "q"])
    tictactoe.play()
    out = capsys.readouterr().out
    assert out.count("1~9 사이의 비어 있는 칸") == 2


def test_play_rejects_taken_cell(monkeypatch, capsys):
    feed(monkeypatch, ["1", "1", "q"])
    tictactoe.play()
    assert "1~9 사이의 비어 있는 칸" in capsys.readouterr().out


def test_play_quit(monkeypatch, capsys):
    feed(monkeypatch, ["q"])
    tictactoe.play()
    assert "메뉴로 돌아갑니다" in capsys.readouterr().out
