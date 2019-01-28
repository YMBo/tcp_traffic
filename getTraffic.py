# !/usr/bin/env python
# -*- coding: UTF-8 -*-
'''统计跨机房服务调用'''
import sys
rootPath = ['', '/usr/local/ymb/traffic/venv/lib64/python27.zip', '/usr/local/ymb/traffic/venv/lib64/python2.7', '/usr/local/ymb/traffic/venv/lib64/python2.7/plat-linux2', '/usr/local/ymb/traffic/venv/lib64/python2.7/lib-tk', '/usr/local/ymb/traffic/venv/lib64/python2.7/lib-old', '/usr/local/ymb/traffic/venv/lib64/python2.7/lib-dynload', '/usr/lib64/python2.7', '/usr/lib/python2.7', '/usr/local/ymb/traffic/venv/lib/python2.7/site-packages']
sys.path+=rootPath
reload(sys)
import pcap
import dpkt
from log import logger
import threading
from dao import dataBase
from conf import TIME, NAME
# 列出所有网络接口
# pcap.findalldevs()

# name接口名，
# promisc为真代表打开混杂模式，
# immediate代表立即模式，启用将不缓存数据包
# timeout_ms代表接收数据包的超时时间
# pcap.pcap对象pc是个动态数据，通常结合for循环或是while循环不断读取数据包，数据包会返回时间戳及报文数据．
# data = pcap.pcap(name='en0', promisc=True, immediate=True)
# setfilter用来设置数据包过滤器，比如只想抓http的包，那就通过setfilter(tcp port 80)实现

results = {}
# 记录程序执行次数
num = 0
error = False


# 开始抓包
def getIp():
    # 取默认网卡
    global error
    # name = pcap.findalldevs()
    try:
        dataPack = pcap.pcap(name=NAME, promisc=True, immediate=True)
        # dataPack.setfilter('udp port 6343')
        logger.info('连接网卡->%s，开始抓包', NAME)
    except Exception as e:
        logger.error('连接网卡->%s失败，强制退出，错误信息->%s', NAME, e)
        error = True
        sys.exit(1)
    else:
        for ptime, pdata in dataPack:
            # 解包，获得数据链路层包
            Ethernet_pack = dpkt.ethernet.Ethernet(pdata)
            # 判断是否含有网络层ip包，和传输层tcp包（端口号用）
            if type(Ethernet_pack.data) == dpkt.ip.IP and type(
                    Ethernet_pack.data.data) == dpkt.tcp.TCP:
                srcIp = '%d.%d.%d.%d' % tuple(
                    map(ord, list(Ethernet_pack.data.src)))
                dstIp = '%d.%d.%d.%d' % tuple(
                    map(ord, list(Ethernet_pack.data.dst)))
                sport = Ethernet_pack.data.data.sport
                dport = Ethernet_pack.data.data.dport
                obj = {
                    'srcIp': srcIp,
                    'dstIp': dstIp,
                    'sport': sport,
                    'dport': dport,
                    'count': 1
                }
                head = str(srcIp) + '=>' + str(dstIp)
                try:
                    currentObj = results[head]
                except KeyError:
                    results[head] = obj
                else:
                    currentObj['count'] = currentObj['count'] + 1
        dataPack.close()


# 定时器
def setInterval(fun, time=TIME):
    if error:
        logger.error('连接网卡失败，强制退出')
        sys.exit(1)
    timer = threading.Timer(time, setInterval, (fun, time))
    fun()
    timer.start()


# 格式化数据，入库格式
def formatData():
    global results
    return [(results[x]['srcIp'], results[x]['dstIp'], results[x]['sport'],
             results[x]['dport'], results[x]['count']) for x in results]


# 清空results
def clearResult():
    global results, num
    num += 1
    logger.info('--------------------------第%s次-----------------------------',
                num)
    data = formatData()
    dataBase.clearTable()
    if len(data) != 0:
        dataBase.insert(data)
        results = {}
        logger.info('%ss 清除result', TIME)


def main():
    setInterval(clearResult)
    getIp()


if __name__ == "__main__":
    main()
