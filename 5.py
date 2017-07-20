#!/user/bin/python
import psutil
import os
import datetime
import time
import json
# settings from settings.py
class stngs(object):
    def filenames(self):
        f1 = open("settings.py", 'r')
        dictset = f1.readlines()
        fileext = str(dictset[0].split(' ')[2])
        f1.close()
        self.filename = 'systemlog.'+fileext
        return self.filename
    def numbs(self):
        f1 = open("settings.py", 'r')
        dictset = f1.readlines()
        self.numb = int(dictset[1].split(' ')[2]) * 60
        f1.close()
        return self.numb
# system parameters for snapshot
class stts(object):
    def st(self):
        ts = time.time()
        self.st1 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H.%M.%S')
        return self.st1
    def cpu(self):
        self.cpu1 = psutil.cpu_percent(interval=1)
        return self.cpu1
    def mem(self):
        self.mem1 = psutil.disk_usage('/').percent
        return self.mem1
    def vmem(self):
        self.vmem1 = psutil.virtual_memory().percent
        return self.vmem1
    def io(self):
        ioread = psutil.disk_io_counters(perdisk=False).read_count
        iowrite = psutil.disk_io_counters(perdisk=False).write_count
        self.io1 = str(ioread) + '/' + str(iowrite)
        return self.io1
    def net(self):
        psutil.net_if_addrs().keys()
        netsent = 0
        netrecv = 0
        for en in psutil.net_if_addrs().keys():
            if psutil.net_io_counters(pernic=True)[en].bytes_sent is not 0:
                netsent += psutil.net_io_counters(pernic=True)[en].bytes_sent
            if psutil.net_io_counters(pernic=True)[en].bytes_recv is not 0:
                netrecv += psutil.net_io_counters(pernic=True)[en].bytes_recv
        self.net1 = str(netsent) + '/' + str(netrecv)
        return self.net1
# create dict for json file
class jsoncnt(object):
    def jsdict(self, cnt):
        snap1 = "SNAPSHOT {}".format(cnt)
        self.jsondict= {snap1: {'TIMESTAMP': stts().st(), 'cpu': stts().cpu(), 'mem': stts().mem(), 'vmem': stts().vmem(), 'io(read/write)': stts().io(), 'net(bites sent/recv)': stts().net()}}
        return self.jsondict
fl1 = stngs().filenames()
n1 = stngs().numbs()
i = 1
while True:

    if fl1 == 'systemlog.txt':
        f = open(fl1, 'a+')
        if os.stat(fl1).st_size > 0:
            f.seek(0, 0)
            i = int(f.readlines()[-1].split(':')[0].split(' ')[1]) + 1
        strfortxtfile = 'SNAPSHOT {}: {}: | cpu:{}% | mem:{}% | vmem:{}% | io(read/write):{} | net(bites sent/recv):{} |\n'.format(i, stts().st(), stts().cpu(), stts().mem(), stts().vmem(), stts().io(), stts().net())
        f.write(strfortxtfile)
        f.close()
    elif fl1 == 'systemlog.json':
        jsondictforjson = jsoncnt().jsdict(i)
        if os.path.isfile(fl1) is True:
            if os.stat(fl1).st_size == 0:
                f = open(fl1, 'w')
                json.dump(jsondictforjson, f, indent=4)
                f.close()
            else:
                f = open(fl1, 'r+')
                dictforjson=json.load(f)
                big = 1
                for x in dictforjson.keys():
                    if int(x.split(" ")[1]) > big:
                        big = int(x.split(" ")[1])
                i = big + 1
                snap = "SNAPSHOT {}".format(i)
                dictforjson[snap] = jsoncnt().jsdict(i)
                f.seek(0, 0)
                json.dump(dictforjson, f, indent=4)
                f.close()
        else:
            f = open(fl1, 'w')
            json.dump(jsondictforjson, f, indent=4)
            f.close()
    time.sleep(n1)