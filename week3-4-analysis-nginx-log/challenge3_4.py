import re
from datetime import datetime
from collections import Counter


def open_parser(filename):
    with open(filename) as logfile:
        # 使用正则表达式解析日志文件
        pattern = (r''
                   '(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP 地址
                   '\[(.+)\]\s'  # 时间
                   '"GET\s(.+)\s\w+/.+"\s'  # 请求路径
                   '(\d+)\s'  # 状态码
                   '(\d+)\s'  # 数据大小
                   '"(.+)"\s'  # 请求头
                   '"(.+)"'  # 客户端信息
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers


def logs_count():
    logs = open_parser('nginx.log')

    # 存放统计后的 IP 和请求地址
    ip_list = []
    request404_list = []

    # 统计题目要求的信息
    for log in logs:
        # 转换原时间格式
        dt = datetime.strptime(log[1][:-6], "%d/%b/%Y:%H:%M:%S")
        # 获取 11 日当天的数据，返回满足条件的 IP 地址
        if int(dt.strftime("%d")) == 11:
            ip_list.append(log[0])
        # 获取状态码为 404 的数据，返回满足条件的请求地址
        if int(log[3]) == 404:
            request404_list.append(log[2])
    return ip_list, request404_list


def main():

    ip_counts = Counter(logs_count()[0])
    request404_counts = Counter(logs_count()[1])

    # 将字典按 Values 排序
    sorted_ip = sorted(ip_counts.items(), key=lambda x: x[1])
    sorted_request404 = sorted(request404_counts.items(), key=lambda x: x[1])

    # 排序后的最后一项 Values 最大, 并处理成字典返回
    ip_dict = dict([sorted_ip[-1]])
    url_dict = dict([sorted_request404[-1]])

    return ip_dict, url_dict


if __name__ == '__main__':
    print(main())
