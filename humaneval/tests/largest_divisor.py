

METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(3) == 1
    assert candidate(7) == 1
    assert candidate(10) == 5
    assert candidate(100) == 50
    assert candidate(49) == 7


if __name__ == '__main__':
    try:
        check(largest_divisor)
        exit(0)
    except AssertionError:
        exit(1)

