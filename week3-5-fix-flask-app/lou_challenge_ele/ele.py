# -*- coding: UTF-8 -*-

import re
import requests

def ele_red_packet(number):
    url = 'http://www.quanmama.com/quan/2362429.html'
    user_agent = 'User-Agent: Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36 MicroMessenger/6.5.13.1081 NetType/WIFI Language/zh_CN'
    headers = {'User-Agent': user_agent}
    s = r"group_sn=\w{32}"
    l = re.findall(s, requests.get(url, headers=headers).text)
    headers = {'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'text/plain;charset=UTF-8',
            "Host": "restapi.ele.me",
            "Origin": "https://h5.ele.me",
            "Pragma": "no-cache",
            "Referer": "https://h5.ele.me/baida/"
            }

    phone = number
    if not re.findall('^\d{11}$', phone):
        return '请输入正确的手机号，尽管正确也很可能领不到红包~'

    sn='10db3582b00f00a1'

    s_list = []
    for url in l:
        value = {
            "group_sn": url[9:],
            "phone": phone,
            "weixin_uid": '468015ki5tulqs9mbjmjvr6w83o45kh9'
        }
        s = requests.post("https://restapi.ele.me/marketing/hongbao/h5/grab",
                    json=value, headers=headers)

        s_list.append(s.status_code)

    if 200 in s_list:
        return "假装领取成功，{} 个红包已注入 {} 的饿了么账户!".format(len(s_list), phone)
    else:
        return "红包领取失败！"
