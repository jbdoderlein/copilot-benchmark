

METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(3, 7) == 1
    assert candidate(10, 15) == 5
    assert candidate(49, 14) == 7
    assert candidate(144, 60) == 12


if __name__ == '__main__':
    try:
        check(greatest_common_divisor)
        exit(0)
    except AssertionError:
        exit(1)

