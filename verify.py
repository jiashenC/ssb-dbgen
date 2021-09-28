from sys import argv
from collections import defaultdict


def test_order_line():
    path = argv[1]
    order_count = defaultdict(lambda: 0)
    with open(path) as f:
        for i, line in enumerate(f.read().splitlines()):
            col = line.split(',')
            o_key, l_num = int(col[0]), int(col[1])
            order_count[o_key] += 1

    for i in range(5):
        assert(order_count[i], 300003)

    for i in range(5, 1500000):
        assert(order_count[i], 3)


def main():
    test_order_line()


if __name__ == '__main__':
    main()
