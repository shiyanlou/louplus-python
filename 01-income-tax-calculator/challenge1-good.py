# -*- coding: utf-8 -*-


def calc_income_tax(income):
    taxable_part = income - 3500
    if taxable_part <= 0:
        return '0.00'
    income_tax_quick_lookup_table = [
        (80000, 0.45, 13505),
        (55000, 0.35, 5505),
        (35000, 0.30, 2755),
        (9000, 0.25, 1005),
        (4500, 0.2, 555),
        (1500, 0.1, 105),
        (0, 0.03, 0)
    ]
    for item in income_tax_quick_lookup_table:
        if taxable_part > item[0]:
            result = taxable_part * item[1] - item[2]
            return '{:.2f}'.format(result)


def main():
    import sys
    if len(sys.argv) != 2:
        print('Parameter Error')
        exit()
    try:
        income = int(sys.argv[1])
    except ValueError:
        print('Parameter Error')
        exit()
    print(calc_income_tax(income))


if __name__ == '__main__':
    main()
