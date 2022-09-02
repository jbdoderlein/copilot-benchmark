

METADATA = {}


def check(candidate):
    assert candidate('') == True
    assert candidate('aba') == True
    assert candidate('aaaaa') == True
    assert candidate('zbcd') == False
    assert candidate('xywyx') == True
    assert candidate('xywyz') == False
    assert candidate('xywzx') == False



if __name__ == '__main__':
    try:
        check(is_palindrome)
        exit(0)
    except AssertionError:
        exit(1)

