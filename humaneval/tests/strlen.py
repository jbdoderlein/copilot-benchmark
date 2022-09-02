

METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == 0
    assert candidate('x') == 1
    assert candidate('asdasnakj') == 9


if __name__ == '__main__':
    try:
        check(strlen)
        exit(0)
    except AssertionError:
        exit(1)

