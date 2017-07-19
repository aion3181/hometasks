#!/user/bin/python
import psutil
import os
import datetime
import time
import json
f1 = open("settings.py", 'r')
dictset = f1.readlines()
fileext = str(dictset[0].split(' ')[2])
numb = int(dictset[1].split(' ')[2]) * 60
f1.close()
# filename = 'systemlog.txt'
filename = 'systemlog.'+fileext
i = 1
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H.%M.%S')
cpu = psutil.cpu_percent(interval=1)
mem = psutil.disk_usage('/').percent
vmem = psutil.virtual_memory().percent
ioread = psutil.disk_io_counters(perdisk=False).read_count
iowrite = psutil.disk_io_counters(perdisk=False).write_count
psutil.net_if_addrs().keys()
netsent = 0
netrecv = 0

while True:
    for en in psutil.net_if_addrs().keys():
        if psutil.net_io_counters(pernic=True)[en].bytes_sent is not 0:
            netsent += psutil.net_io_counters(pernic=True)[en].bytes_sent
        if psutil.net_io_counters(pernic=True)[en].bytes_recv is not 0:
            netrecv += psutil.net_io_counters(pernic=True)[en].bytes_recv
    if filename == 'systemlog.txt':
        f = open(filename, 'a+')
        if os.stat(filename).st_size > 0:
            f.seek(0, 0)
            i = int(f.readlines()[-1].split(':')[0].split(' ')[1]) + 1
        strfortxtfile = 'SNAPSHOT {}: {}: | cpu:{}% | mem:{}% | vmem:{}% | io(read/write):{}/{} | net(bites sent/recv):{}/{} |\n'.format(i, st, cpu, mem, vmem, ioread, iowrite, netsent, netrecv)
        f.write(strfortxtfile)
        f.close()
    elif filename == 'systemlog.json':
        net = str(netsent)+'/'+str(netrecv)
        io = str(ioread)+'/'+str(iowrite)
        snap = "SNAPSHOT {}".format(i)
        jsondictforjson= {snap: {'TIMESTAMP': st, 'cpu': cpu, 'mem': mem, 'vmem': vmem, 'io(read/write)': io, 'net(bites sent/recv)': net}}
        if os.path.isfile(filename) is True:
            if os.stat(filename).st_size == 0:
                f = open(filename, 'w')
                json.dump(jsondictforjson, f, indent=4)
                f.close()
            else:
                f = open(filename, 'r+')
                dictforjson=json.load(f)
                big = 1
                for x in dictforjson.keys():
                    if int(x.split(" ")[1]) > big:
                        big = int(x.split(" ")[1])
                i = big + 1
                snap = "SNAPSHOT {}".format(i)
                dictforjson[snap] = {'TIMESTAMP': st, 'cpu': cpu, 'mem': mem, 'vmem': vmem, 'io(read/write)': io, 'net(bites sent/recv)': net}
                f.seek(0, 0)
                json.dump(dictforjson, f, indent=4)
                f.close()
        else:
            f = open(filename, 'w')
            json.dump(jsondictforjson, f, indent=4)
            f.close()
    time.sleep(numb)