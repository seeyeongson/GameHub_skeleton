from games.baseball import judge, is_valid_guess


def test_judge_win():
    assert judge("731", "731") == (3, 0)


def test_judge_strike_ball():
    assert judge("731", "712") == (1, 1)


def test_judge_all_ball():
    assert judge("731", "317") == (0, 3)


def test_valid_guess():
    assert is_valid_guess("123")


def test_invalid_duplicate():
    assert not is_valid_guess("111")


def test_invalid_zero():
    assert not is_valid_guess("107")
