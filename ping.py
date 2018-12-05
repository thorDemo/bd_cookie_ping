from threadpool import ThreadPool, makeRequests
from configparser import ConfigParser
from myLibs.ping_with_cookie import BDPing


config = ConfigParser()
config.read('config.ini', 'utf-8')
https = int(config.get('bd_push', 'https'))
thread_num = int(config.get('bd_push', 'thread'))
target = config.get('bd_push', 'target')
pool = ThreadPool(thread_num)
arg = []
for x in range(0, thread_num):
    arg.append(target)
request = makeRequests(BDPing.bd_ping, arg)
[pool.putRequest(req) for req in request]
pool.wait()
