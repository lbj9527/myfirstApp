##########################learning yield##########################
import random
import string

#gene 26+26 letters and 10 digits
forSelect = string.ascii_letters + string.digits

def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)



g = foo()
print(next(g))
print("*"*20)
print(next(g))
print(g.send(7))

###########输出#############
#starting...
#4
#********************
#res: None
#4
#res: 7
#4

###########yield 用法详解############
#1.yield的作用类似于return
#2.有yield的函数，不是函数，而是迭代器
#3.当使用带yield的函数时，遇到next(),循环,send(),则开始迭代
#4.迭代时，下一次迭代从上一次迭代的结束处开始
#5.send()具有向yield传参的功能
#6.使用yield的原因是，与数组相比，可以节省内存
