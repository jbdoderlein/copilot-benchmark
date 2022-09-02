

METADATA = {}


def check(candidate):
    assert candidate([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [0, 2, 3, 5, 9, 123]



if __name__ == '__main__':
    try:
        check(unique)
        exit(0)
    except AssertionError:
        exit(1)

