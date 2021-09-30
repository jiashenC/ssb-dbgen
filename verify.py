from sys import argv
from collections import defaultdict


def test_order_line(text_entry):
    order_count = defaultdict(lambda: 0)
    for col in text_entry:
        o_key, l_num = int(col[0]), int(col[1])
        order_count[o_key] += 1

    for i in range(1, 6):
        assert(order_count[i] == 300003)

    for o_key in order_count:
        if o_key in list(range(1, 6)):
            continue
        assert(order_count[o_key] == 3)


def test_customer(text_entry):
    customer_count = defaultdict(lambda: set())
    for col in text_entry:
        o_key, cust_key = int(col[0]), int(col[2])
        customer_count[cust_key].add(o_key)

    for cust_key in range(5):
        cust_key = cust_key * (30000 // 5) + 1
        assert(0.04 <= len(customer_count[cust_key]) / 1500000 <= 0.06)

def test_date(text_entry):
    date_count = defaultdict(lambda: 0)
    for col in text_entry:
        date_txt = col[5]
        date_txt = date_txt[1:-1]
        date_without_year = '-'.join(date_txt.split('-')[1:])
        date_count[date_without_year] += 1

    assert(0.51 <= date_count['05-29'] / 6000000 <= 0.53)


def main():
    path = argv[1]

    text_entry = []
    with open(path) as f:
        for i, line in enumerate(f.read().splitlines()):
            text_entry.append(line.split(','))

    test_order_line(text_entry)
    test_customer(text_entry)
    test_date(text_entry)


if __name__ == '__main__':
    main()
