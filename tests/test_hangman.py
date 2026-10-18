from games.hangman import mask_word, is_solved


def test_mask_word():
    assert mask_word("apple", {"a", "p"}) == "app__"


def test_mask_word_all_guessed():
    assert mask_word("apple", {"a", "p", "l", "e"}) == "apple"


def test_is_solved_true():
    assert is_solved("apple", {"a", "p", "l", "e"})


def test_is_solved_false():
    assert not is_solved("apple", {"a", "p"})
