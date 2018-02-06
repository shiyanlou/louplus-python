""" 计算社保和个人所得税（多进程方式）

步骤：解析参数 -> 读取社保配置文件 -> 读取员工数据 -> 计算 -> 输出

其中，读取员工数据，计算 和输出三个过程可以在独立的进程中完成。整个应用启动时，
会首先解析参数，并通过参数读取社保配置文件，配置文件读取完成后，会启动三个进程
分别用于读取员工数据，计算税额，输出结果。

读取员工数据进程每读取一项员工数据就会将其放到队列 Q1 当中，而计算税额进程则会
从队列 Q1 中获取相应的员工数据项，然后计算税额，计算完成后将结果放到队列 Q2 中，
输出进程则从 Q2 进程中获取计算结果，并将结果输出到文件当中。工作流程图如下:


    读取员工数据进程

          ||
          \/

        队列 Q1

          ||
          \/

      税额计算进程

          ||
          \/

        队列 Q2

          ||
          \/

        输出进程

执行方式:

    python3 calculator_multiprocess.py  -c test.cfg -d user.csv -o gongzi.csv
"""

import sys
import queue
from multiprocessing import Queue, Process


class ArgError(Exception):
    pass


class Args:
    """命令行参数解析类
    """
    def __init__(self, args):
        """
        Args:
            args (list): 参数列表
        """
        self.args = args

    def __parse_arg(self, arg):
        try:
            # 通过索引获取相应的参数的值
            value = self.args[self.args.index(arg) + 1]
        except (ValueError, IndexError):
            value = None
        return value

    def get_arg(self, arg):
        """获取指定参数的值
        """
        value = self.__parse_arg(arg)
        if value is None:
            raise ArgError('not found arg %s' % arg)
        return value


class SheBaoConfig:
    """社保配置文件类
    """
    def __init__(self, file):
        """
        Args:
            file (str): 社保配置文件
        """

        self.jishu_low, self.jishu_high, self.total_rate = self.__parse_config(file)

    def __parse_config(self, file):
        """解析社保参数配置文件
        """
        rate = 0
        jishu_low = 0
        jishu_high = 0

        with open(file) as f:
            for line in f:
                key,  value = line.split('=')
                key = key.strip()
                try:
                    value = float(value.strip())
                except ValueError:
                    continue
                if key == 'JiShuL':
                    jishu_low = value
                elif key == 'JiShuH':
                    jishu_high = value
                else:
                    rate += value
        return jishu_low, jishu_high, rate


class EmployeeData(Process):
    """员工数据实现类，多进程方式

    通过继承 Process 类，并实现 run 方法使其可以像一个进程一样启动执行。
    """
    def __init__(self, file, output_queue):
        """
        Args:
            file (str): 员工数据文件
            output_queue (object): multiprocessing.Queue 队列实例
        """
        self.file = file
        self.output_q = output_queue

        # 继承 Process 时，必须手动调用 Process.__init__ 方法
        super().__init__()

    def __parse(self):
        """ 解析员工数据，每次返回一行数据
        """
        # 每次解析一行数据
        for line in open(self.file):
            employee_id, gongzi = line.split(',')
            yield (int(employee_id), int(gongzi))

    def run(self):
        """进程启动后真正执行代码的方法
        """
        # 将解析出的每一行数据放到队列中
        for item in self.__parse():
            self.output_q.put(item)


class Calculator(Process):
    """社保，个人所得税计算实现类

    计算方法:

    应纳税所得额 = 工资金额 － 各项社会保险费 - 起征点(3500元)
    应纳税额 = 应纳税所得额 × 税率 － 速算扣除数
    最终工资 = 工资金额 - 各项社会保险费 - 应纳税额

    个人所得税税率因应纳税所得额不同而不同，具体可以查询税率速查表得知。
    """

    # 个人所得税起征点
    tax_start = 3500

    # 个人所得税税率速查表
    # 列表中每一项为元组，包含三项数据: (应纳税额, 税率，速算扣除数)
    tax_table = [
        (80000, 0.45, 13505),
        (55000, 0.35, 5505),
        (35000, 0.3, 2755),
        (9000, 0.25, 1005),
        (4500, 0.2, 555),
        (1500, 0.1, 105),
        (0, 0.03, 0),
    ]

    def __init__(self, config, input_queue, out_queue):
        """
        Args:
            config (object): SheBaoConfig 实例
            input_queue (object): 多进程队列，计算器将从这个队列中获取员工数据
            output_queue (object): 多进程队列，计算器将从计算结果放到这个队列中
        """

        self.config = config
        self.input_q = input_queue
        self.output_q = out_queue
        # 继承 Process 时，必须手动调用 Process.__init__ 方法
        super().__init__()

    def calculate(self, data_item):
        """
        Args:
            data_item (tuple):  有员工号和工资组成的元组，如 (101, 5000)
        """

        employee_id, gongzi = data_item

        # 计算社保金额
        if gongzi < self.config.jishu_low:
            shebao = self.config.jishu_low * self.config.total_rate
        elif gongzi > self.config.jishu_high:
            shebao = self.config.jishu_high * self.config.total_rate
        else:
            shebao = gongzi * self.config.total_rate

        # 工资减去社保后的剩余金额
        left_gongzi = gongzi - shebao

        # 应纳税所得额 = 工资 - 社保 - 起征点
        tax_gongzi = left_gongzi - self.tax_start

        # 如果应纳税所得额 小于 0，那么就不用缴纳个人所得税
        if tax_gongzi < 0:
            tax = 0
        else:
            # 否则查询税率速查表计算应该缴纳的个人所得税税额
            # item 包含三项数据，(应纳税额, 税率，速算扣除数)
            for item in self.tax_table:
                if tax_gongzi > item[0]:
                    tax = tax_gongzi * item[1] - item[2]
                    break

        # 最终工资 = 工资 - 社保 - 个人所得税
        last_gongzi = left_gongzi - tax

        return str(employee_id), str(gongzi), '{:.2f}'.format(shebao), '{:.2f}'.format(tax), '{:.2f}'.format(last_gongzi)

    def run(self):
        """进程启动后真正执行代码的方法
        """

        # 循环从输入队列中获取员工数据
        while True:
            try:
                # 指定获取超时时间为 1 秒，如果超时则认为没有需要处理的数据，退出进程
                item = self.input_q.get(timeout=1)
            except queue.Empty:
                return
            # 计算机结果
            result = self.calculate(item)
            # 将结果放到输出队列中
            self.output_q.put(result)


class Exporter(Process):
    """导出类实现
    """

    def __init__(self, file, input_queue):
        """
        Args:
            file (str): 需要导出的目标文件
            input_queue (object): 输入队列，从该队列中需要导出的数据项
        """
        self.file = open(file, 'w')
        self.input_q = input_queue
        # 继承 Process 时，必须手动调用 Process.__init__ 方法
        super().__init__()

    def export(self, item):
        line = ','.join(item) + '\n'
        self.file.write(line)

    def close(self):
        """关闭整个导出实例
        """
        # 关闭打开的文件
        self.file.close()

    def run(self):
        while True:
            try:
                # 指定获取超时时间为 1 秒，如果超时则认为没有需要处理的数据，退出进程
                item = self.input_q.get(timeout=1)
            except queue.Empty:
                # 退出进程前需要关闭整个导出实例
                self.close()
                return
            self.export(item)


if __name__ == '__main__':

    # 参数实例
    args = Args(sys.argv[1:])
    # 社保配置实例
    config = SheBaoConfig(args.get_arg('-c'))

    q1 = Queue()
    q2 = Queue()

    # 员工数据进程
    employee_data = EmployeeData(args.get_arg('-d'), q1)
    # 计算进程
    calculator = Calculator(config, q1, q2)
    # 导出进程
    exporter = Exporter(args.get_arg('-o'), q2)

    # 启动进程
    employee_data.start()
    calculator.start()
    exporter.start()

    # 通过 join 方法等待所有的进程结束
    employee_data.join()
    calculator.join()
    exporter.join()
