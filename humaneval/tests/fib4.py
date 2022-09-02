

METADATA = {}


def check(candidate):
    assert candidate(5) == 4
    assert candidate(8) == 28
    assert candidate(10) == 104
    assert candidate(12) == 386



if __name__ == '__main__':
    try:
        check(fib4)
        exit(0)
    except AssertionError:
        exit(1)

