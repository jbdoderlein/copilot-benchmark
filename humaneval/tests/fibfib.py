

METADATA = {}


def check(candidate):
    assert candidate(2) == 1
    assert candidate(1) == 0
    assert candidate(5) == 4
    assert candidate(8) == 24
    assert candidate(10) == 81
    assert candidate(12) == 274
    assert candidate(14) == 927



if __name__ == '__main__':
    try:
        check(fibfib)
        exit(0)
    except AssertionError:
        exit(1)

