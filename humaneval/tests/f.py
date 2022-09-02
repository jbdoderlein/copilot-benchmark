def check(candidate):

    assert candidate(5) == [1, 2, 6, 24, 15]
    assert candidate(7) == [1, 2, 6, 24, 15, 720, 28]
    assert candidate(1) == [1]
    assert candidate(3) == [1, 2, 6]


if __name__ == '__main__':
    try:
        check(f)
        exit(0)
    except AssertionError:
        exit(1)

