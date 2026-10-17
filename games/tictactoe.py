"""틱택토 (2인용 콘솔 게임).

보드는 길이 9의 리스트이며 칸 번호는 화면에서 1~9로 보여 준다.

 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
"""

GAME_NAME = "틱택토"
EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"

WIN_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def new_board():
    """빈 보드를 만든다."""
    return [EMPTY] * 9


def parse_move(text):
    """사용자 입력(1~9)을 보드 인덱스(0~8)로 바꾼다. 잘못된 입력이면 None."""
    text = text.strip()
    if not text.isdigit():
        return None
    number = int(text)
    if not 1 <= number <= 9:
        return None
    return number - 1


def is_valid_move(board, index):
    """index가 0~8 범위이고 빈 칸인지 확인한다."""
    if index is None or not 0 <= index < 9:
        return False
    return board[index] == EMPTY


def place_mark(board, index, mark):
    """말을 놓은 새 보드를 반환한다. (원본 보드는 바꾸지 않는다)"""
    if not is_valid_move(board, index):
        raise ValueError("둘 수 없는 칸입니다.")
    new = list(board)
    new[index] = mark
    return new


def get_winner(board):
    """이긴 쪽의 말('X' 또는 'O')을 반환한다. 없으면 None."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    """보드가 가득 찼는지 확인한다."""
    return EMPTY not in board


def is_draw(board):
    """무승부인지 확인한다."""
    return is_full(board) and get_winner(board) is None


def next_player(mark):
    """다음 차례의 말을 반환한다."""
    return PLAYER_O if mark == PLAYER_X else PLAYER_X


def format_board(board):
    """보드를 출력용 문자열로 만든다. 빈 칸에는 칸 번호를 보여 준다."""
    cells = [board[i] if board[i] != EMPTY else str(i + 1) for i in range(9)]
    rows = []
    for r in range(3):
        start = r * 3
        end = start + 3
        row = cells[start:end]
        rows.append(" " + " | ".join(row))
    return "\n---+---+---\n".join(rows)


def play():
    """틱택토 한 판을 진행한다. (main.py 메뉴에서 호출)"""
    board = new_board()
    current = PLAYER_X
    print("\n=== 틱택토 ===")
    print("칸 번호(1~9)를 입력해 말을 놓으세요. 종료: q")

    while True:
        print()
        print(format_board(board))
        raw = input(f"\n[{current}] 차례 > ")

        if raw.strip().lower() == "q":
            print("게임을 종료하고 메뉴로 돌아갑니다.")
            return

        index = parse_move(raw)
        if not is_valid_move(board, index):
            print("1~9 사이의 비어 있는 칸을 입력하세요.")
            continue

        board = place_mark(board, index, current)

        winner = get_winner(board)
        if winner:
            print()
            print(format_board(board))
            print(f"\n{winner} 승리!")
            return
        if is_draw(board):
            print()
            print(format_board(board))
            print("\n무승부입니다.")
            return

        current = next_player(current)


if __name__ == "__main__":
    play()
