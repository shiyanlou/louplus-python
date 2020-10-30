# -*- coding: utf-8 -*-
import sys
import csv
import configparser
from getopt import getopt, GetoptError
from datetime import datetime
from collections import namedtuple
import queue
from multiprocessing import Queue, Process

# 税率表条目类，该类由 namedtuple 动态创建，代表一个命名元组
IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

# 起征点常量
INCOME_TAX_START_POINT = 5000

# 税率表，里面的元素类型为前面创建的 IncomeTaxQuickLookupItem
INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 15160),
    IncomeTaxQuickLookupItem(55000, 0.35, 7160),
    IncomeTaxQuickLookupItem(35000, 0.30, 4410),
    IncomeTaxQuickLookupItem(25000, 0.25, 2660),
    IncomeTaxQuickLookupItem(12000, 0.2, 1410),
    IncomeTaxQuickLookupItem(3000, 0.1, 210),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

class Args(object):
    """
    命令行参数处理类
    """

    def __init__(self):
        # 解析命令行选项
        self.options = self._options()

    def _options(self):
        """
        内部函数，用来解析命令行选项，返回保存了所有选项及其取值的字典
        """

        try:
            # 解析命令行选项和参数，本程序只支持选项，因此忽略返回结果里的参数列表
            opts, _ = getopt(sys.argv[1:], 'hC:c:d:o:', ['help'])
        except GetoptError:
            print('Parameter Error')
            exit()
        options = dict(opts)

        # 处理 -h 或 --help 选项
        if len(options) == 1 and ('-h' in options or '--help' in options):
            print(
                'Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            exit()

        return options

    def _value_after_option(self, option):
        """
        内部函数，用来获取跟在选项后面的值
        """

        value = self.options.get(option)

        # 城市参数可选，其它参数必须提供
        if value is None and option != '-C':
            print('Parameter Error')
            exit()

        return value

    @property
    def city(self):
        """
        城市
        """

        return self._value_after_option('-C')

    @property
    def config_path(self):
        """
        配置文件路径
        """

        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        """
        用户工资文件路径
        """

        return self._value_after_option('-d')

    @property
    def export_path(self):
        """
        税后工资文件路径
        """

        return self._value_after_option('-o')


# 创建一个全局参数类对象供后续使用
args = Args()


class Config(object):
    """
    配置文件处理类
    """

    def __init__(self):
        # 读取配置文件
        self.config = self._read_config()

    def _read_config(self):
        """
        内部函数，用来读取配置文件中指定城市的配置
        """

        config = configparser.ConfigParser()
        config.read(args.config_path)
        # 如果指定了城市并且该城市在配置文件中，返回该城市的配置，否则返回默认的配置
        if args.city and args.city.upper() in config.sections():
            return config[args.city.upper()]
        else:
            return config['DEFAULT']

    def _get_config(self, key):
        """
        内部函数，用来获得配置项的值
        """

        try:
            return float(self.config[key])
        except (ValueError, KeyError):
            print('Parameter Error')
            exit()

    @property
    def social_insurance_baseline_low(self):
        """
        获取社保基数下限
        """

        return self._get_config('JiShuL')

    @property
    def social_insurance_baseline_high(self):
        """
        获取社保基数上限
        """

        return self._get_config('JiShuH')

    @property
    def social_insurance_total_rate(self):
        """
        获取社保总费率
        """

        return sum([
            self._get_config('YangLao'),
            self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('GongShang'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin')
        ])


# 创建一个全局的配置文件处理对象供后续使用
config = Config()


class UserData(Process):
    """
    用户工资文件处理进程
    """

    def __init__(self, userdata_queue):
        super().__init__()

        # 用户数据队列
        self.userdata_queue = userdata_queue

    def _read_users_data(self):
        """
        内部函数，用来读取用户工资文件
        """

        userdata = []
        with open(args.userdata_path) as f:
            # 依次读取用户工资文件中的每一行并解析得到用户 ID 和工资
            for line in f.readlines():
                employee_id, income_string = line.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print('Parameter Error')
                    exit()
                userdata.append((employee_id, income))

        return userdata

    def run(self):
        """
        进程入口方法
        """

        # 从用户数据文件依次读取每条用户数据并写入到队列
        for item in self._read_users_data():
            self.userdata_queue.put(item)


class IncomeTaxCalculator(Process):
    """
    税后工资计算进程
    """

    def __init__(self, userdata_queue, export_queue):
        super().__init__()

        # 用户数据队列
        self.userdata_queue = userdata_queue
        # 导出数据队列
        self.export_queue = export_queue

    @staticmethod
    def calc_social_insurance_money(income):
        """
        计算应纳税额
        """

        if income < config.social_insurance_baseline_low:
            return config.social_insurance_baseline_low * \
                config.social_insurance_total_rate
        elif income > config.social_insurance_baseline_high:
            return config.social_insurance_baseline_high * \
                config.social_insurance_total_rate
        else:
            return income * config.social_insurance_total_rate

    @classmethod
    def calc_income_tax_and_remain(cls, income):
        """
        计算税后工资
        """

        # 计算社保金额
        social_insurance_money = cls.calc_social_insurance_money(income)

        # 计算应纳税额
        real_income = income - social_insurance_money
        taxable_part = real_income - INCOME_TAX_START_POINT

        # 从高到低判断落入的税率区间，如果找到则用该区间的参数计算纳税额并返回结果
        for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
            if taxable_part > item.start_point:
                tax = taxable_part * item.tax_rate - item.quick_subtractor
                return '{:.2f}'.format(tax), '{:.2f}'.format(real_income - tax)

        # 如果没有落入任何区间，则返回 0
        return '0.00', '{:.2f}'.format(real_income)

    def calculate(self, employee_id, income):
        """
        计算单个用户的税后工资
        """

        # 计算社保金额
        social_insurance_money = '{:.2f}'.format(
            self.calc_social_insurance_money(income))

        # 计算税后工资
        tax, remain = self.calc_income_tax_and_remain(income)

        return [employee_id, income, social_insurance_money, tax, remain,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')]

    def run(self):
        """
        进程入口方法
        """

        # 从用户数据队列读取用户数据，计算用户税后工资，然后写入到导出数据队列
        while True:
            # 获取下一个用户数据
            try:
                # 超时时间为 1 秒，如果超时则认为没有需要处理的数据，退出进程
                employee_id, income = self.userdata_queue.get(timeout=1)
            except queue.Empty:
                return

            # 计算税后工资
            result = self.calculate(employee_id, income)

            # 将结果写入到导出数据队列
            self.export_queue.put(result)


class IncomeTaxExporter(Process):
    """
    税后工资导出进程
    """

    def __init__(self, export_queue):
        super().__init__()

        # 导出数据队列
        self.export_queue = export_queue

        # 创建 CSV 写入器
        self.file = open(args.export_path, 'w', newline='')
        self.writer = csv.writer(self.file)

    def run(self):
        """
        进程入口方法
        """

        # 从导出数据队列读取导出数据，写入到导出文件中
        while True:
            # 获取下一个导出数据
            try:
                # 超时时间为 1 秒，如果超时则认为没有需要处理的数据，退出进程
                item = self.export_queue.get(timeout=1)
            except queue.Empty:
                # 退出时关闭文件
                self.file.close()
                return

            # 写入到导出文件
            self.writer.writerow(item)


if __name__ == '__main__':
    # 创建进程之间通信的队列
    userdata_queue = Queue()
    export_queue = Queue()

    # 用户数据进程
    userdata = UserData(userdata_queue)
    # 税后工资计算进程
    calculator = IncomeTaxCalculator(userdata_queue, export_queue)
    # 税后工资导出进程
    exporter = IncomeTaxExporter(export_queue)

    # 启动进程
    userdata.start()
    calculator.start()
    exporter.start()

    # 等待所有进程结束
    userdata.join()
    calculator.join()
    exporter.join()
