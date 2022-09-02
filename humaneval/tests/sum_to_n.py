

METADATA = {}


def check(candidate):
    assert candidate(1) == 1
    assert candidate(6) == 21
    assert candidate(11) == 66
    assert candidate(30) == 465
    assert candidate(100) == 5050



if __name__ == '__main__':
    try:
        check(sum_to_n)
        exit(0)
    except AssertionError:
        exit(1)

