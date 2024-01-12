from project import main, is_valid, mode_1

def main():
    test_is_valid()
    #test_main()
    test_mode_1()
 #   test_longest_words()

#def test_main():
#    user_choice = "4"
#    assert main(user_choice) == valid()
    #assert not is_valid()


def test_mode_1():
    letters = "xskbtmv"
    assert mode_1(letters) == "tsk" is True

def test_is_valid():

    assert is_valid("corn")
    assert not is_valid("cron")


#def test_longest_words():
#    assert longest_words("act") == ["act", "cat"]
#    assert longest_words("abcd") == ["abcd"]
#    assert longest_words("xyz") == "No valid word found."


if __name__ == "__main__":
    main()
