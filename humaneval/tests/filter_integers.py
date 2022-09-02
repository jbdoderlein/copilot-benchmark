

METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate([]) == []
    assert candidate([4, {}, [], 23.2, 9, 'adasd']) == [4, 9]
    assert candidate([3, 'c', 3, 3, 'a', 'b']) == [3, 3, 3]


if __name__ == '__main__':
    try:
        check(filter_integers)
        exit(0)
    except AssertionError:
        exit(1)

