

METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('', 'x') == 0
    assert candidate('xyxyxyx', 'x') == 4
    assert candidate('cacacacac', 'cac') == 4
    assert candidate('john doe', 'john') == 1


if __name__ == '__main__':
    try:
        check(how_many_times)
        exit(0)
    except AssertionError:
        exit(1)

