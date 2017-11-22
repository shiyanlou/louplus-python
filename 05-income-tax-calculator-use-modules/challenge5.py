# -*- coding: utf-8 -*-
import sys
import csv
import queue
import configparser
from getopt import getopt, GetoptError
from datetime import datetime
from multiprocessing import Process, Queue
from collections import namedtuple


IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

INCOME_TAX_START_POINT = 3500

INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.2, 555),
    IncomeTaxQuickLookupItem(1500, 0.1, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

q_user = Queue()
q_result = Queue()


class Args(object):

    def __init__(self):
        self.options = self._options()

    def _options(self):
        try:
            opts, _ = getopt(sys.argv[1:], 'hC:c:d:o:', ['help'])
        except GetoptError:
            print('Parameter Error')
            exit()
        options = dict(opts)
        if len(options) == 1 and ('-h' in options or '--help' in options):
            print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            exit()
        return options

    def _value_after_option(self, option):
        value = self.options.get(option)
        if value is None and option != '-C':
            print('Parameter Error')
            exit()
        return value

    @property
    def city(self):
        return self._value_after_option('-C')

    @property
    def config_path(self):
        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        return self._value_after_option('-d')

    @property
    def export_path(self):
        return self._value_after_option('-o')


args = Args()


class Config(object):

    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = configparser.ConfigParser()
        config.read(args.config_path)
        if args.city and args.city.upper() in config.sections():
            return config[args.city.upper()]
        else:
            return config['DEFAULT']

    def _get_config(self, name):
        try:
            return float(self.config[name])
        except (ValueError, KeyError):
            print('Parameter Error')
            exit()

    @property
    def social_insurance_baseline_low(self):
        return self._get_config('JiShuL')

    @property
    def social_insurance_baseline_high(self):
        return self._get_config('JiShuH')

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


config = Config()


class UserData(Process):

    def _read_users_data(self):
        with open(args.userdata_path) as f:
            for line in f.readlines():
                employee_id, income_string = line.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print('Parameter Error')
                    exit()
                yield (employee_id, income)

    def run(self):
        for data in self._read_users_data():
            q_user.put(data)


class IncomeTaxCalculator(Process):

    @staticmethod
    def calc_social_insurance_money(income):
        if income < config.social_insurance_baseline_low:
            return config.social_insurance_baseline_low * \
                config.social_insurance_total_rate
        if income > config.social_insurance_baseline_high:
            return config.social_insurance_baseline_high * \
                config.social_insurance_total_rate
        return income * config.social_insurance_total_rate

    @classmethod
    def calc_income_tax_and_remain(cls, income):
        social_insurance_money = cls.calc_social_insurance_money(income)
        real_income = income - social_insurance_money
        taxable_part = real_income - INCOME_TAX_START_POINT
        if taxable_part <= 0:
            return '0.00', '{:.2f}'.format(real_income)
        for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
            if taxable_part > item.start_point:
                tax = taxable_part * item.tax_rate - item.quick_subtractor
                return '{:.2f}'.format(tax), '{:.2f}'.format(real_income - tax)

    def calc_for_all_userdata(self):
        while True:
            try:
                employee_id, income = q_user.get(timeout=1)
            except queue.Empty:
                return
            data = [employee_id, income]
            social_insurance_money = '{:.2f}'.format(self.calc_social_insurance_money(income))
            tax, remain = self.calc_income_tax_and_remain(income)
            data.extend([social_insurance_money, tax, remain])
            data.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            yield data

    def run(self):
        for data in self.calc_for_all_userdata():
            q_result.put(data)


class Exporter(Process):

    def run(self):
        with open(args.export_path, 'w', newline='') as f:
            while True:
                writer = csv.writer(f)
                try:
                    item = q_result.get(timeout=1)
                except queue.Empty:
                    return
                writer.writerow(item)


if __name__ == '__main__':
    workers = [
        UserData(),
        IncomeTaxCalculator(),
        Exporter()
    ]
    for worker in workers:
        worker.run()
