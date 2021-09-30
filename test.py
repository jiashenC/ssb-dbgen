from sys import argv
from collections import defaultdict


SCALE = 1


def test_order_line(line_order_text_entry):
    order_count = defaultdict(lambda: 0)
    for col in line_order_text_entry:
        o_key, l_num = int(col[0]), int(col[1])
        order_count[o_key] += 1

    for i in range(1, 6):
        assert 0.04 <= (order_count[i] / (6000000 * SCALE)) <= 0.06, order_count[i]

    for o_key in order_count:
        if o_key in list(range(1, 6)):
            continue
        assert order_count[o_key] == 3, order_count[o_key]


def test_customer(line_order_text_entry):
    customer_count = defaultdict(lambda: set())
    for col in line_order_text_entry:
        o_key, cust_key = int(col[0]), int(col[2])
        customer_count[cust_key].add(o_key)

    for cust_key in range(5):
        cust_key = cust_key * (30000 // 5 * SCALE) + 1
        assert 0.04 <= (len(
            customer_count[cust_key]) / (1500000 * SCALE)) <= 0.06, customer_count[cust_key]


def test_date(line_order_text_entry):
    date_count = defaultdict(lambda: 0)
    for col in line_order_text_entry:
        date_txt = col[5]
        date_txt = date_txt[1:-1]
        date_without_year = '-'.join(date_txt.split('-')[1:])
        date_count[date_without_year] += 1

    assert 0.51 <= (date_count['05-29'] /
                    (6000000 * SCALE)) <= 0.53, date_count['05-29']


def test_supplier(line_order_text_entry, supplier_text_entry):
    supp_key_to_region = defaultdict(lambda: 'WRONG')
    for col in supplier_text_entry:
        supp_key, region = int(col[0]), col[-3]
        supp_key_to_region[supp_key] = region

    supplier_count = defaultdict(lambda: defaultdict(lambda: 0))
    for col in line_order_text_entry:
        supp_key = int(col[4])
        region = supp_key_to_region[supp_key]
        supplier_count[region][supp_key] += 1

    total_supp_count = 0
    for region in supplier_count:
        total_supp_count += max(supplier_count[region].values())

    assert 0.49 <= (total_supp_count / (6000000 * SCALE)
                    ) <= 0.51, total_supp_count


def main():
    global SCALE

    SCALE = int(argv[1]) if len(argv) > 1 else 1

    line_order_path = 'lineorder.tbl'
    line_order_text_entry = []
    with open(line_order_path) as f:
        for i, line in enumerate(f.read().splitlines()):
            line_order_text_entry.append(line.split(','))

    test_order_line(line_order_text_entry)
    test_customer(line_order_text_entry)
    test_date(line_order_text_entry)

    supplier_path = 'supplier.tbl'
    supplier_text_entry = []
    with open(supplier_path) as f:
        for i, line in enumerate(f.read().splitlines()):
            supplier_text_entry.append(line.split(','))

    test_supplier(line_order_text_entry, supplier_text_entry)


if __name__ == '__main__':
    main()
