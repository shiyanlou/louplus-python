import sys
import csv
from collections import namedtuple

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
        # 保存命令行参数列表
        self.args = sys.argv[1:]

    def _value_after_option(self, option):
        """
        内部函数，用来获取跟在选项后面的值
        """

        try:
            # 获得选项位置
            index = self.args.index(option)
            # 下一位置即为选项值
            return self.args[index + 1]
        except (ValueError, IndexError):
            print('Parameter Error')
            exit()

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
        内部函数，用来读取配置文件中的配置项
        """

        config = {}
        with open(args.config_path) as f:
            # 依次读取配置文件里的每一行并解析得到配置项名称和值
            for line in f.readlines():
                key, value = line.strip().split('=')
                try:
                    # 去掉前后可能出现的空格
                    config[key.strip()] = float(value.strip())
                except ValueError:
                    print('Parameter Error')
                    exit()

        return config

    def _get_config(self, key):
        """
        内部函数，用来获得配置项的值
        """

        try:
            return self.config[key]
        except KeyError:
            print('Config Error')
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

class UserData(object):
    """
    用户工资文件处理类
    """

    def __init__(self):
        # 读取用户工资文件
        self.userlist = self._read_users_data()

    def _read_users_data(self):
        """
        内部函数，用来读取用户工资文件
        """

        userlist = []
        with open(args.userdata_path) as f:
            # 依次读取用户工资文件中的每一行并解析得到用户 ID 和工资
            for line in f.readlines():
                employee_id, income_string = line.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print('Parameter Error')
                    exit()
                userlist.append((employee_id, income))

        return userlist

    def get_userlist(self):
        """
        获取用户数据列表
        """

        # 直接返回属性 userlist 列表对象
        return self.userlist

class IncomeTaxCalculator(object):
    """
    税后工资计算类
    """

    def __init__(self, userdata):
        # 初始化时接收一个 UserData 对象
        self.userdata = userdata

    @classmethod
    def calc_social_insurance_money(cls, income):
        """
        计算社保金额
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

    def calc_for_all_userdata(self):
        """
        计算所有用户的税后工资
        """

        result = []
        # 循环计算每一个用户的税后工资，并将结果汇总到结果集中
        for employee_id, income in self.userdata.get_userlist():
            # 计算社保金额
            social_insurance_money = '{:.2f}'.format(
                self.calc_social_insurance_money(income))

            # 计算税后工资
            tax, remain = self.calc_income_tax_and_remain(income)

            # 添加到结果集
            result.append(
                [employee_id, income, social_insurance_money, tax, remain])

        return result

    def export(self):
        """
        导出所有用户的税后工资到文件
        """

        # 计算所有用户的税后工资
        result = self.calc_for_all_userdata()

        with open(args.export_path, 'w', newline='') as f:
            # 创建 csv 文件写入对象
            writer = csv.writer(f)
            # 写入多行数据
            writer.writerows(result)


if __name__ == '__main__':
    # 创建税后工资计算器
    calculator = IncomeTaxCalculator(UserData())

    # 调用 export 方法导出税后工资到文件
    calculator.export()
