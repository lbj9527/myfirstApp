from multiprocessing import Process
import json
import time
from multiprocessing import  Lock

def show(i):
    with open('file/ticket.txt') as f:
        dic = json.load(f)#load直接打开文件, 不用read, loads操作字符串,需要read
    print('余票: %s' % dic['ticket'])

def buy_ticket(i,lock):
    lock.acquire() ##拿到钥匙进门,其他进程阻塞, acqurie和release之间的代码只能被一个进程执行
    with open('file/ticket.txt') as f:
        dic = json.load(f)#load直接打开文件, 不用read, loads操作字符串,需要read
        time.sleep(0.1)
    if  dic['ticket'] > 0 :
        dic['ticket'] -=1
        print('%s买到票了'%i) #console改为绿色
    else:
        print('%s没有买到票了'%i) #console改为红色
    time.sleep(0.1)
    with open('file/ticket.txt', 'w') as f:
        json.dump(dic,f) #修改json文件,减去被买去的票
    lock.release() #释放钥匙



if __name__ == '__main__':
    for i in range(10):
        p = Process(target=show, args=(i,))
        p.start()
    lock = Lock() #产生钥匙
    for i in range(10):
        p = Process(target=buy_ticket, args=(i,lock))
        p.start()