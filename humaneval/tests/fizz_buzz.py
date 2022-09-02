

METADATA = {}


def check(candidate):
    assert candidate(50) == 0
    assert candidate(78) == 2
    assert candidate(79) == 3
    assert candidate(100) == 3
    assert candidate(200) == 6
    assert candidate(4000) == 192
    assert candidate(10000) == 639
    assert candidate(100000) == 8026



if __name__ == '__main__':
    try:
        check(fizz_buzz)
        exit(0)
    except AssertionError:
        exit(1)

