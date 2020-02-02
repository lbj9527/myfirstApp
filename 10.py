"""
如何使用 salt 加 hash 来单向转换密码明文
"""

import os
from hashlib import sha256  #hashlib提供了常见的摘要算法,如MD5,SHA1,HA256等
from hmac import HMAC       #hmac算法模块，提供了带salt的哈希算法

#加密
def encrypt_password(password, salt = None):
    if salt is None:
        salt = os.urandom(8)   #返回一个有n个byte那么长的一个随机string

    if isinstance(salt, str):    #返回salt是否为str的子类
        salt = salt.encode('utf-8')

    result = password.encode('utf-8')
    for i in range(10):
        result = HMAC(result, salt, sha256).digest()
    return salt + result

#验证
def validate_password(hashed, input_password):
    return hashed == encrypt_password(input_password, 'a')

if __name__ == "__main__":

    hashed = encrypt_password('123456','a')
    isRight = validate_password(hashed, '123456')
    print(isRight)



#####################备注#####################
# 1.密码原文（或经过 hash 后的值）和随机生成的 salt 字符串混淆，然后再进行 hash，最后把 hash 值和 salt 值一起存储。
#   验证密码的时候只要用 salt 再与密码原文做一次相同步骤的运算，比较结果与存储的 hash 值就可以了。
#   这样一来哪怕是简单的密码，在进过 salt 混淆后产生的也是很不常见的字符串，根本不会出现在彩虹字典中。salt 越长暴力破解的难度越大

    
      


