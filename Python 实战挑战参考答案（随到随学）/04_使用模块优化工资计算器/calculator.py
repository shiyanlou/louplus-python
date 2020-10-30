import sys, csv, getopt, datetime, queue
from configparser import ConfigParser
from multiprocessing import Process, Queue as q

class Args:
    def __init__(self):
        l = sys.argv[1:]
        # 选项有“短选项”和“长选项”两种，短选项格式：一个减号一个字母；长选项格式：俩减号多个字母
        # getopt.getopt 方法有仨参数：要处理的对象列表、短选项组、长选项组
        # 短选项组为字符串，若选项有参数，后面加冒号；长选项组为列表，若选项有参数，后面加等号
        # 该方法返回值为二元元组，每个元素都是列表，一个是选项解析结果，另一个是其余参数
        options, args = getopt.getopt(l, 'hC:c:d:o:', ['help'])
        d = dict(options)
        if len(options) == 1 and list(d.keys())[0] in ['-h', '--help']:
            print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            exit()
        if d.get('-C'):
            self.C = d['-C'].upper()
        else:
            self.C = 'DEFAULT'
        self.c = d['-c']
        self.d = d['-d']
        self.o = d['-o']


class Config:
    def __init__(self):
        self.config = self._a()
    def _a(self):
        d = {'s':0}
        # 生成配置文件解析类的实例
        cfg = ConfigParser()
        # 解析配置文件
        cfg.read(args.c)
        # 获取某个配置组下的所有键值对，items 方法的返回值为列表，其中每个元素都是二元元组
        # 注意，每个元素的 key 都是全小写的字符串，不论配置文件里是什么样
        for m, n in cfg.items(args.C):
            if m == 'jishul' or m == 'jishuh':
                d[m] = float(n)
            else:
                d['s'] += float(n)
        return d


def compute(salary):
    # 社保金额计算
    social_insurance_salary = salary * config['s']
    if salary < config['jishul']:
        social_insurance_salary = config['jishul'] * config['s']
    if salary > config['jishuh']:
        social_insurance_salary = config['jishuh'] * config['s']
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

class Data:
    def __init__(self):
        with open(args.d) as f:
            l = list(csv.reader(f))
        self.value = l

args = Args()
config = Config().config
data = Data().value


q1, q2 = q(), q()

def f1():
    for i in data:
        q1.put(i)

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

def f3():
    with open(args.o, 'a') as f:
        while True:
            try:
                csv.writer(f).writerow(q2.get(timeout=0.1))
            except queue.Empty:
                return

Process(target=f1).start()
Process(target=f2).start()
Process(target=f3).start()
