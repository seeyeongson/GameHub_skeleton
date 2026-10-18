import random

GAME_NAME = "숫자 야구"


def make_answer() -> str:
    # 1~9 사이의 서로 다른 숫자 3개 생성#
    return "".join(random.sample("123456789", 3))


def judge(answer: str, guess: str) -> tuple[int, int]:
    # 스트라이크, 볼 판정#
    strike = sum(a == g for a, g in zip(answer, guess))
    ball = sum(num in answer for num in guess) - strike

    return strike, ball


def is_valid_guess(guess: str) -> bool:
    # 입력 검증#
    return (
        len(guess) == 3
        and guess.isdigit()
        and len(set(guess)) == 3
        and all(ch in "123456789" for ch in guess)
    )


def play() -> None:
    # 한 판 진행#

    answer = make_answer()

    print(f"\n[{GAME_NAME}]")
    print("서로 다른 숫자 3개를 맞혀 보세요.")
    print("모든 자리수는 1~9입니다.")
    print("최대 9번의 기회가 주어집니다.")

    for attempt in range(1, 10):
        while True:
            guess = input(f"\n[{attempt}/9] 추측: ").strip()

            if is_valid_guess(guess):
                break

            print("잘못된 입력입니다.")
            print("3자리 숫자, 중복 없음, 모든 숫자는 1~9만 가능")

        strike, ball = judge(answer, guess)

        # 승리 조건:
        # 3개의 숫자와 위치를 모두 맞춰 3S가 되면 승리
        if strike == 3:
            print(f"\n정답! {attempt}번 만에 맞혔습니다!")
            return

        print(f"{strike}S {ball}B")

    print(f"\n실패! 정답은 {answer}였습니다.")


if __name__ == "__main__":
    play()
