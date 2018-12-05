# -*- coding=utf-8 -*-
from datetime import datetime
from tools.push_tools import PushTool
import requests
import sys
from configparser import ConfigParser

success_count = 0
failure_count = 0
start_time = datetime.now()
cookie = PushTool.get_cookies()
config = ConfigParser()
config.read('config.ini', 'utf-8')
target = int(config.get('bd_push', 'target'))


class BDPing:

    @staticmethod
    def bd_ping_one(domain):
        global success_count
        global failure_count
        xml = """
            <?xml version="1.0"?>
            <methodCall>
            <methodName>weblogUpdates.ping</methodName>
            <params>
            <param>
            <value><string>%s</string></value>
            </param><param><value><string>%s</string></value>
            </param>
            </params>
            </methodCall>
            """
        while True:
            url = PushTool.get_url(domain)
            xml = xml.replace('%s', url)
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Content-Type': 'text/xml',
                'Connection': 'keep-alive',
                'User-Agent': PushTool.user_agent(),
                'Content-Length': str(len(xml)),
                'Host': 'ping.baidu.com',
                'Origin': 'http://ping.baidu.com',
                'Referer': 'http://ping.baidu.com/ping.html'
            }
            conn = requests.Session()
            conn.headers = headers
            # print(headers)
            # 将cookiesJar赋值给会话
            cookiesJar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
            conn.cookies = cookiesJar
            code = 404
            try:
                res = conn.post('http://ping.baidu.com/ping/RPC2', headers=headers, json=xml, timeout=3.0)
                code = res.status_code
                if code == 200:
                    success_count += 1
                    if '<int>0</int>' in res.text:
                        print('成功 ping: %s status: %s' % (url, code))
                    else:
                        print('失败 ping: %s status: %s' % (url, code))
                else:
                    failure_count += 1
            except:
                failure_count += 1
            print('----------------------')
            print('success:%d  failure:%d' % (success_count, failure_count))

    @staticmethod
    def bd_ping_two():
        global success_count
        global failure_count
        global start_time
        global target
        xml = """
            <?xml version="1.0"?>
            <methodCall>
            <methodName>weblogUpdates.ping</methodName>
            <params>
            <param>
            <value><string>%s</string></value>
            </param><param><value><string>%s</string></value>
            </param>
            </params>
            </methodCall>
            """
        while True:
            url = PushTool.rand_all(target)
            xml = xml.replace('%s', url)
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Content-Type': 'text/xml',
                'Connection': 'keep-alive',
                'User-Agent': PushTool.user_agent(),
                'Content-Length': str(len(xml)),
                'Host': 'ping.baidu.com',
                'Origin': 'http://ping.baidu.com',
                'Referer': 'http://ping.baidu.com/ping.html'
            }
            conn = requests.Session()
            conn.headers = headers
            # print(headers)
            # 将cookiesJar赋值给会话
            cookiesJar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
            conn.cookies = cookiesJar
            code = 404
            try:
                res = conn.post('http://ping.baidu.com/ping/RPC2', headers=headers, json=xml, timeout=3.0)
                code = res.status_code
                if code == 200:
                    if '<int>0</int>' in res.text:
                        success_count += 1
                    else:
                        failure_count += 1
                else:
                    failure_count += 1
            except:
                failure_count += 1
            this_time = datetime.now()
            spend = this_time - start_time
            if int(spend.seconds) == 0:
                speed_sec = success_count / 1
            else:
                speed_sec = success_count / int(spend.seconds)
            speed_day = float('%.2f' % ((speed_sec * 60 * 60 * 24) / 10000000))
            percent = success_count / (failure_count + success_count) * 100
            sys.stdout.write(' ' * 100 + '\r')
            sys.stdout.flush()
            print(url)
            sys.stdout.write(
                '%s 成功%s 预计(day/千万):%s M 成功率:%.2f%% 状态码:%s\r' % (datetime.now(), success_count, speed_day, percent, code))
            sys.stdout.flush()

