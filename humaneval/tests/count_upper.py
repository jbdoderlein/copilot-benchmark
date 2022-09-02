def check(candidate):

    # Check some simple cases
    assert candidate('aBCdEf')  == 1
    assert candidate('abcdefg') == 0
    assert candidate('dBBE') == 0
    assert candidate('B')  == 0
    assert candidate('U')  == 1
    assert candidate('') == 0
    assert candidate('EEEE') == 2

    # Check some edge cases that are easy to work out by hand.
    assert True



if __name__ == '__main__':
    try:
        check(count_upper)
        exit(0)
    except AssertionError:
        exit(1)

