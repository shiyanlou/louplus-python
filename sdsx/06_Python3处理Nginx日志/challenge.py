import re
from collections import Counter

def open_parser(a):
    with open(a) as f:
        data = f.read()
    pattern = ('(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP 地址
               '\[(.+)\]\s'                 # 时间
               '"GET\s(.+)\s\w+/.+"\s'      # 请求路径
               '(\d+)\s.*\s'                # 状态码
    )
    return re.findall(pattern, data)

def main():
    l = open_parser('nginx.log')
    ip_list, url_list = [], []
    for t in l:
        ip, date, url, st = t
        if st == '404':
            url_list.append(url)
        if date[:11] == '11/Jan/2017':
            ip_list.append(ip)
    a, b = sorted(Counter(ip_list).items(), key=lambda x: -x[1])[0]
    c, d = sorted(Counter(url_list).items(), key=lambda x: -x[1])[0]
    return {a: b}, {c: d}

if __name__ == '__main__':
    print(main())
