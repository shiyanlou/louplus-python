# -*- coding: utf-8 -*-
import sys
import csv
from collections import namedtuple

# 使用 nametuple 的方式来存储个税计算表
# 优势是避免了使用索引来获取个税阶梯和税率造成代码难以维护的状态
IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

# 个税起征点 3500
INCOME_TAX_START_POINT = 3500

# 个税计算表，列表存储，每一行都是一个 namedtuple
# 每个 namedtuple 包含该计算阶梯的起始薪资、税率、速算扣除数
INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.2, 555),
    IncomeTaxQuickLookupItem(1500, 0.1, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

# 命令行参数处理类
class Args(object):

    # 初始化的时候读取命令行中输入的所有参数到 self.args 列表
    def __init__(self):
        self.args = sys.argv[1:]

    # 内部函数，用来提取参数 -c/-d/-o 后面的值
    def _value_after_option(self, option):
        try:
            # 首先获得参数 -c/-d/-o 所在位置在列表 sys.args 中的索引值
            index = self.args.index(option)
            # 获取 -c/-d/-o 所在位置的下一个位置的字符串就是对应的值
            return self.args[index + 1]
        except (ValueError, IndexError):
            # 如果获取出错，则打印错误信息并退出
            print('Parameter Error')
            exit()

    # 获取 -c 参数对应的值，即配置文件的路径
    @property
    def config_path(self):
        return self._value_after_option('-c')

    # 获取 -d 参数对应的值，即用户工资数据文件的路径
    @property
    def userdata_path(self):
        return self._value_after_option('-d')

    # 获取 -o 参数对应的值，即输出的用户工资单文件的路径
    @property
    def export_path(self):
        return self._value_after_option('-o')

# 创建命令行参数处理的对象 args
# 在此处创建的原因是后续的 class Config 的代码定义中需要用到这个对象
args = Args()

# 配置文件读取处理类
class Config(object):

    # 初始化的时候调用内部接口 self._read_config() 读取配置文件中的所有内容
    # 读取的配置项和值都存入字典 self.config 中
    def __init__(self):
        self.config = self._read_config()

    # 内部函数，用来读取配置文件中的配置项
    def _read_config(self):
        # 从 args 对象中获得配置文件路径
        config_path = args.config_path
        # 初始化存储配置项和值的字典
        config = {}
        # 打开配置文件读取数据
        with open(config_path) as f:
            # 读取每一行数据
            for line in f.readlines():
                # 使用 = 分割每一行的内容，注意需要去掉每行两边的空格
                key, value = line.strip().split(' = ')
                try:
                    # 将配置项和对应的值存入到字典中，注意需要去除字符串两边的空格
                    config[key.strip()] = float(value.strip())
                except ValueError:
                    # 如果配置值不能转成 float，则报错退出
                    print('Parameter Error')
                    exit()
        # 返回存储配置项和值的字典
        return config

    # 内部函数，用来使用配置项获得配置的值
    def _get_config(self, key):
        try:
            return self.config[key]
        except KeyError:
            # 如果配置项不存在则打印错误并退出
            print('Config Error')
            exit()

    # 获取社保基数下限
    @property
    def social_insurance_baseline_low(self):
        return self._get_config('JiShuL')

    # 获取社保基数上限
    @property
    def social_insurance_baseline_high(self):
        return self._get_config('JiShuH')

    # 获取社保总费率，分别获取每一项的费率后再使用 sum 计算列表中每一项的和
    @property
    def social_insurance_total_rate(self):
        return sum([
            self._get_config('YangLao'),
            self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('GongShang'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin')
        ])

# 创建配置文件处理的对象 config
# 在此处创建的原因是后续的 class IncomeTaxCalculator
# 的代码定义中需要用到这个对象
config = Config()

# 用户工资文件处理类
class UserData(object):

    # 初始化过程，读取用户工资文件并将数据存入到 userdata 列表中
    def __init__(self):
        self.userdata = self._read_users_data()

    # 内部函数，用来读取用户工资文件
    def _read_users_data(self):
        # 从 args 中获取用户工资文件路径
        userdata_path = args.userdata_path
        # 初始化存储的列表
        userdata = []
        # 打开用户工资文件
        with open(userdata_path) as f:
            # 读取用户工资文件中的每一行内容类似：101,3500
            for line in f.readlines():
                # 使用逗号分割每一行的字符串，得到工号和工资
                employee_id, income_string = line.strip().split(',')
                try:
                    # 将工资字符串转为整数
                    income = int(income_string)
                except ValueError:
                    # 如果工资无法转为整数则报错退出
                    print('Parameter Error')
                    exit()
                # 将每一行的数据转成二元组后添加到 userdata 列表
                userdata.append((employee_id, income))
        # 返回用户工资数据列表
        return userdata

    # 添加 __iter__ 将 UserData 对象成为可迭代对象，
    # 即可以用 for 循环获取中间的 userdata 列表里的数据
    def __iter__(self):
        return iter(self.userdata)

# 税后工资计算类
class IncomeTaxCalculator(object):

    # 初始化的时候传入 UserData 对象，传进来后赋值给 self.userdata
    def __init__(self, userdata):
        self.userdata = userdata

    # 静态成员方法：完全可以单独实现的方法，仅仅是因为与工资计算类有一些关联才放进入类中
    # 计算需要缴纳的社保金额，传入的参数为工资金额
    @staticmethod
    def calc_social_insurance_money(income):
        # 如果工资小于社保基数下限，则用社保基数下限计算社保
        if income < config.social_insurance_baseline_low:
            return config.social_insurance_baseline_low * \
                config.social_insurance_total_rate
        # 如果工资大于社保基数上限，则用社保基数上限计算社保
        if income > config.social_insurance_baseline_high:
            return config.social_insurance_baseline_high * \
                config.social_insurance_total_rate
        # 其他情况，则用工资计算社保
        return income * config.social_insurance_total_rate

    # 类方法：不需要实例化类也能够调用的方法，需要传入代表类的 cls
    # 计算个税和税后工资，传入的参数为工资金额
    @classmethod
    def calc_income_tax_and_remain(cls, income):
        # 计算社保金额
        social_insurance_money = cls.calc_social_insurance_money(income)
        # 获得应纳税所得额
        real_income = income - social_insurance_money
        taxable_part = real_income - INCOME_TAX_START_POINT
        # 如果应纳税所得额小于0，则交税0，税后工资为工资减去社保
        if taxable_part <= 0:
            return '0.00', '{:.2f}'.format(real_income)
        # 使用个税计算表计算个税
        for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
            # 循环遍历个税计算表，直到找到应纳税所得额所在的区间
            if taxable_part > item.start_point:
                # 使用公式计算个税
                tax = taxable_part * item.tax_rate - item.quick_subtractor
                # 返回个税及税后工资，注意需要保留两位小数
                return '{:.2f}'.format(tax), '{:.2f}'.format(real_income - tax)

    # 计算所有用户工资
    # 直接使用 self.userdata 对象计算其中的每一个数据
    def calc_for_all_userdata(self):
        # 初始化返回结果
        result = []
        # 循环获取 userdata 中的用户工号和税前工资
        for employee_id, income in self.userdata:
            # 初始化返回的数据结果，包含工号和税前工资
            data = [employee_id, income]
            # 计算需要缴纳的社保，注意需要保留两位小数
            social_insurance_money = '{:.2f}'.format(self.calc_social_insurance_money(income))
            # 计算个税及税后工资，注意需要保留两位小数
            tax, remain = self.calc_income_tax_and_remain(income)
            # 将社保、个税及税后工资补充到返回的数据列表中
            data += [social_insurance_money, tax, remain]
            result.append(data)
        # 返回所有用户的工资数据
        return result

    # 导出到工资数据文件，传入的参数用来指定导出的文件类型，此处用来未来扩展
    def export(self, file_type='csv'):
        # 计算并获得所有用户的工资数据
        result = self.calc_for_all_userdata()
        # 打开导出的文件，并写入
        with open(args.export_path, 'w', newline='') as f:
            # 使用 csv 模块创建 writer 对象
            writer = csv.writer(f)
            # 向文件中以 csv 格式写入列表
            writer.writerows(result)


if __name__ == '__main__':
    # 创建 UserData 对象并使用该对象初始化工资计算器
    calculator = IncomeTaxCalculator(UserData())
    # 调用工资计算器对象 calculator 中的 export 方法导出结果数据到文件
    calculator.export()
