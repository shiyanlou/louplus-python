# 同上一个挑战一样，本挑战可以分解为 4 步：
# 1、处理命令行参数；2、处理配置文件和员工数据文件
# 3、计算数据；4、使用多进程进行计算并将计算结果写入文件
# 前三步无变化，创建各个类、函数
import sys, csv, queue
from multiprocessing import Process, Queue

class Args:  # 处理命令行参数
    def __init__(self):
        self.c = sys.argv[sys.argv.index('-c')+1]
        self.d = sys.argv[sys.argv.index('-d')+1]
        self.o = sys.argv[sys.argv.index('-o')+1]

class Config:  # 处理配置文件
    def __init__(self, f):
        self.config = self._read_conf(f)
    def _read_conf(self, f):
        d = {'s': 0}
        with open(f) as f:
            for i in f:
                name, value = i.split(' = ')
                # 如果 value < 1 则说明该项为社保比例项
                if float(value) < 1:
                    d['s'] += float(value)
                else:
                    d[name] = float(value)
        return d

class UserData:  # 处理员工数据文件
    def __init__(self, f):
        with open(f) as f:
            self.data = list(csv.reader(f))

def compute(salary):
    # 社保金额计算
    social_insurance_salary = salary * config['s']
    if salary < config['JiShuL']:
        social_insurance_salary = config['JiShuL'] * config['s']
    if salary > config['JiShuH']:
        social_insurance_salary = config['JiShuH'] * config['s']
    start_point = 5000  # 起征点
    # 需要缴税的那部分工资
    tax_part_salary = salary - social_insurance_salary - start_point
    if tax_part_salary <= 0:
        tax = 0 
    elif tax_part_salary <= 3000:
        tax = tax_part_salary * 0.03
    elif tax_part_salary <= 12000:
        tax = tax_part_salary * 0.1 - 210 
    elif tax_part_salary <= 25000:
        tax = tax_part_salary * 0.2 - 1410
    elif tax_part_salary <= 35000:
        tax = tax_part_salary * 0.25 - 2660
    elif tax_part_salary <= 55000:
        tax = tax_part_salary * 0.3 - 4410
    elif tax_part_salary <= 80000:
        tax = tax_part_salary * 0.35 - 7160
    else:
        tax = tax_part_salary * 0.45 - 15160
    # 税后工资
    after_tax_salary = salary - social_insurance_salary - tax
    return [salary, format(social_insurance_salary, '.2f'), format(tax, '.2f'),
            format(after_tax_salary, '.2f')]


if __name__ == '__main__':
    args = Args()
    config = Config(args.c).config
    userdata = UserData(args.d).data
    q1, q2 = Queue(), Queue()  # 创建两个队列，分别传送员工数据和计算结果

    # 推送员工数据的任务
    def f1():
        for i in userdata:
            q1.put(i)

    # 接收员工数据，计算并推送计算结果
    def f2():
        def haha():
            while True:
                try:
                    a, b = q1.get(timeout=0.1)
                    x = compute(int(b))
                    x.insert(0, a)
                    yield x
                except queue.Empty:
                    return
        for i in haha():
            q2.put(i)

    # 接收计算结果并写入文件
    def f3():
        with open(args.o, 'w') as f:
            while True:
                try:
                    csv.writer(f).writerow(q2.get(timeout=0.1))
                except queue.Empty:
                    return

    Process(target=f1).start()
    Process(target=f2).start()
    Process(target=f3).start()
