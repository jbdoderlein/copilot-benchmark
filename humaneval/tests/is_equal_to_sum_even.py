def check(candidate):
    assert candidate(4) == False
    assert candidate(6) == False
    assert candidate(8) == True
    assert candidate(10) == True
    assert candidate(11) == False
    assert candidate(12) == True
    assert candidate(13) == False
    assert candidate(16) == True


if __name__ == '__main__':
    try:
        check(is_equal_to_sum_even)
        exit(0)
    except AssertionError:
        exit(1)

