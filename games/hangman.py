
"""행맨 게임."""

import random

GAME_NAME = "행맨"

WORDS = [
    "apple",
    "banana",
    "python",
    "computer",
    "hangman",
    "guitar",
    "orange",
]

MAX_MISTAKES = 6


def mask_word(word: str, guessed: set[str]) -> str:
    """맞힌 글자만 보여 주고 나머지는 밑줄로 표시한다."""
    return "".join(
        char if char in guessed else "_"
        for char in word
    )


def is_solved(word: str, guessed: set[str]) -> bool:
    """단어의 모든 글자를 맞혔는지 확인한다."""
    return all(char in guessed for char in word)


def play() -> None:
    """행맨 게임을 진행한다."""
    print(f"\n=== {GAME_NAME} ===")
    print("숨겨진 영어 단어를 맞혀 보세요!")
    print(f"틀릴 수 있는 횟수: {MAX_MISTAKES}회")

    while True:
        word = random.choice(WORDS)
        guessed: set[str] = set()
        wrong_guesses: set[str] = set()

        while (
            len(wrong_guesses) < MAX_MISTAKES
            and not is_solved(word, guessed)
        ):
            print(f"\n단어: {mask_word(word, guessed)}")
            print(f"틀린 글자: {', '.join(sorted(wrong_guesses)) or '없음'}")
            print(
                f"남은 기회: "
                f"{MAX_MISTAKES - len(wrong_guesses)}회"
            )

            guess = input("알파벳 한 글자를 입력하세요: ").strip().lower()

            if len(guess) != 1 or not guess.isalpha() or not guess.isascii():
                print("영어 알파벳 한 글자만 입력하세요.")
                continue

            if guess in guessed or guess in wrong_guesses:
                print("이미 입력한 글자입니다. 다른 글자를 입력하세요.")
                continue

            if guess in word:
                guessed.add(guess)
                print("정답에 포함된 글자입니다!")
            else:
                wrong_guesses.add(guess)
                print("틀렸습니다!")

        if is_solved(word, guessed):
            print(f"\n정답입니다! 단어는 '{word}'입니다.")
        else:
            print(f"\n기회를 모두 사용했습니다. 정답은 '{word}'입니다.")

        answer = input("한 판 더 하시겠습니까? (y/n): ").strip().lower()

        if answer in {"n", "no"}:
            print("행맨 게임을 종료합니다.")
            return

        while answer not in {"y", "yes", "n", "no"}:
            answer = input("y 또는 n을 입력하세요: ").strip().lower()

            if answer in {"n", "no"}:
                print("행맨 게임을 종료합니다.")
                return
