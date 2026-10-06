"""Play rock-paper-scissors against the computer; the first to two wins wins."""

import random

GAME_NAME = "가위바위보"

# Map each input number to its displayed choice.
CHOICES = {"1": "가위", "2": "바위", "3": "보"}


def decide(player: str, computer: str) -> str:
    """Return win, lose, or draw. Choices: 1=scissors, 2=rock, 3=paper."""

    # Reject invalid choices before comparing them.
    if player not in CHOICES or computer not in CHOICES:
        raise ValueError("선택은 1, 2, 3 중 하나여야 합니다.")

    # Identical choices produce a draw.
    if player == computer:
        return "draw"

    # Each pair lists the player's choice first and the computer's second.
    # Scissors beat paper, rock beats scissors, and paper beats rock.
    winning_pairs = {("1", "3"), ("2", "1"), ("3", "2")}

    if (player, computer) in winning_pairs:
        return "win"

    return "lose"


def play() -> None:
    """Run one match. Draws do not count; return to the hub when finished."""

    # Keep separate win counts for the player and the computer.
    player_wins = 0
    computer_wins = 0

    print(f"\n[{GAME_NAME}] 먼저 2승을 하면 승리합니다.")
    print("무승부는 다시 진행합니다. 0을 입력하면 메뉴로 돌아갑니다.")

    # Continue until either side has won two rounds.
    while player_wins < 2 and computer_wins < 2:
        player = input("1: 가위 / 2: 바위 / 3: 보 / 0: 메뉴 > ").strip()

        # Exit this function so the hub can display its menu again.
        if player == "0":
            print("메인 메뉴로 돌아갑니다.")
            return

        # Invalid input does not change the score or start a round.
        if player not in CHOICES:
            print("0, 1, 2, 3 중 하나를 입력하세요.")
            continue

        # Randomly select a valid choice for the computer.
        computer = random.choice(list(CHOICES))

        print(f"나: {CHOICES[player]} / 컴퓨터: {CHOICES[computer]}")
        result = decide(player, computer)

        # Update only the winner's score; draws leave both scores unchanged.
        if result == "win":
            player_wins += 1
            print("이번 판은 이겼어요!")
        elif result == "lose":
            computer_wins += 1
            print("이번 판은 졌어요!")
        else:
            print("무승부입니다!")

        print(f"점수: 나 {player_wins} - 컴퓨터 {computer_wins}")

    # Report the match winner after the loop finishes.
    if player_wins == 2:
        print("최종 결과: 승리!")
    else:
        print("최종 결과: 패배!")
