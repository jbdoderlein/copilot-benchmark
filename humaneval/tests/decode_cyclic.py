

METADATA = {}


def check(candidate):
    from random import randint, choice
    import string

    letters = string.ascii_lowercase
    for _ in range(100):
        str = ''.join(choice(letters) for i in range(randint(10, 20)))
        encoded_str = encode_cyclic(str)
        assert candidate(encoded_str) == str



if __name__ == '__main__':
    try:
        check(decode_cyclic)
        exit(0)
    except AssertionError:
        exit(1)

