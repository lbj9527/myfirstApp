"""
你有一个目录，装了很多照片，把它们的尺寸变成都不大于 iPhone5 分辨率的大小。
"""

from PIL import Image
import os

path = 'pic'
resultPath = 'result_05py'

if not os.path.isdir(resultPath):
    os.mkdir(resultPath)

for picName in os.listdir(path):
    picPath = os.path.join(path, picName)
    print(picPath)
    with Image.open(picPath) as im:
        w, h = im.size
        n = w / 1366 if (w / 1366) >= (h / 640) else h / 640
        im.thumbnail((w // n, h // n))
        im.save(resultPath+'/finish_' + picName.split('.')[0] + '.jpg', 'jpeg')


#######################备注##########################
# 1.with用法
#   紧跟with后面的语句会被求值，返回对象的__enter__()方法被调用，这个方法的返回值将被赋值给as关键字后面的变量，当with后面的代码块全部被执行完之后，将调用前面返回对象的__exit__()方法。
#   with语句最关键的地方在于被求值对象必须有__enter__()和__exit__()这两个方法
# 2.os.path.join(path1,path2,path3)用法
#   拼接path1，path2等的路径，若无/，则自动加上/