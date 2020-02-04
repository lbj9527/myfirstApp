import os, time, random
from multiprocessing import Process,Pool,Queue
import subprocess

print('Process (%s) start...' % os.getpid())        #返回进程ID

####################例1.启动一个子进程#####################
def testSubProc():                #此函数说明，当子进程调用函数时，该函数也处于子线程中
    print('random count' , random.random())
    time.sleep(random.random())
    print('subpoc after subproc, id:',os.getpid())

def run_proc(name):
    testSubProc()
    print('Run child process %s (%s)...' % (name, os.getpid()))

def startSubProc():
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()

    #join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
    p.join()

    print('Child process end.')

#################例2.使用线程池管理4个子进程################
def long_time_task(name):
    print('Run task %s (%s)' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, end - start))

def startProcssPool():
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocess done...')
    p.close()
    p.join()
    print('All subprocesses done.')

###代码解读
#1.对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，
#  调用close()之后就不能继续添加新的Process了。
#2.请注意输出的结果，task 0，1，2，3是立刻执行的，而task 4要等待前面某个task完成后才执行，
#  这是因为Pool的默认大小在我的电脑上是4，因此，最多同时执行4个进程。
#  这是Pool有意设计的限制，并不是操作系统的限制。如果改成：
#      p = Pool(5)
#  就可以同时跑5个进程。

#####################例3.使用subProcess管理子进程######################
##待输入





#################例4.进程通信：mutilprocessing子模块queue###############
def writeQueue(q):
    print('write process %s' % os.getpid())
    words = ['A','B','C']
    for word in words:
        print('put %s to queue' % word)
        q.put(word)
        time.sleep(random.random())

def readQueue(q):
    print('read process %s' % os.getpid())
    while True:
        word = q.get(True)
        print('get %s from queue' % word)

def readAndWrite():
    #父进程创建Queue,并传给各个子进程
    print('Parent process %s' % os.getpid())
    q = Queue()
    pw = Process(target=writeQueue, args=(q,))
    pr = Process(target=readQueue, args=(q,))

    #启动子进程pw，写入
    pw.start()

    #启动子进程pr，读取
    pr.start()

    #等待pw结束
    pw.join()

    #pr进程里是死循环，无法等待其结果，只能强行终止
    pr.terminate()




if __name__ == '__main__':
    #startSubProc()
    startProcssPool()
    #readAndWrite()