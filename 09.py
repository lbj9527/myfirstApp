# 1.collections是Python内建的一个集合模块，
#  提供了许多有用的集合类,如dict,list,set,tuple
# 2.OrderedDict是有序的dict,按照插入顺序
#   它还可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key
from collections import OrderedDict
import xlwt, json     #xlwt写入excel文件的扩展包,xlrd读取excel的扩展包


def writeExcel():
    #打开文件
    with open('file/student.txt', 'r', encoding='utf-8-sig') as f:

        #转化为json
        data = json.load(f, object_pairs_hook=OrderedDict)

        workbook = xlwt.Workbook()
        sheet1 = workbook.add_sheet('student', cell_overwrite_ok=True)
        for index, (key, values) in enumerate(data.items()):
            sheet1.write(index, 0, key)    #参数对应 行, 列, 值
            for i, value in enumerate(values):
                sheet1.write(index, i+1, value)
        workbook.save('file/studet.xls')

if __name__ == "__main__":
    writeExcel()


###########################备注############################
#1.txt文件包含BOM信息,需要添加'utf-8-sig',否则会报错
