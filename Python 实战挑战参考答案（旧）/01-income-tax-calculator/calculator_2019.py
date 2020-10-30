import sys

def main():
    # 检查命令行参数合法性，并转换为正确类型
    if len(sys.argv) != 2:
        print('Parameter Error')
        exit()
    try:
        income = int(sys.argv[1])
    except ValueError:
        print('Parameter Error')
        exit()

    # 扣除起征点
    value = income - 5000
    # 依据落入的税率区间，按照相应的税率参数计算税费
    if value <= 0:
        result = 0
    elif value <= 3000:
        result = value * 0.03 - 0
    elif value <= 12000:
        result = value * 0.1 - 210
    elif value <= 25000:
        result = value * 0.2 - 1410
    elif value <= 35000:
        result = value * 0.25 - 2660
    elif value <= 55000:
        result = value * 0.3 - 4410
    elif value <= 80000:
        result = value * 0.35 - 7160
    else:
        result = income * 0.45 - 15160

    # 打印结果
    print('{:.2f}'.format(result))


if __name__ == '__main__':
    main()
