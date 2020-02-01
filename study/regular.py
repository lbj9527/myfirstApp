##########################learning regular expression##########################
import re


#example1
def example1():
    line = "Cats are smarter than dogs"

    matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
    if matchObj:
        print ("matchObj.group(): ",matchObj.group())
        print ("matchObj.group(1): ",matchObj.group(1))
        print ("matchObj.group(2): ",matchObj.group(2))
    else:
        print("no match!")

#example2
def example2():
    s = '1102231990xxxxxxxx'
    res = re.search(r'(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{4})',s)
    print(res.groupdict())

if __name__ == "__main__":
    example1()
    example2()



#########################正则表达式 用法详解#########################
#example1
#1.正则表达式：r'(.*) are (.*?) .*'
#2.r表示字符串为非转义的原始字符串，让编译器忽略反斜杠
#3.(.*)第一个匹配分组，.代表匹配除换行符之外的单个字符，*表示匹配多个字符
#4.(.*?)第二个匹配分组，.*? 后面多个问号，代表非贪婪模式，也就是说只匹配符合条件的最少字符
#5.后面的一个 .* 没有括号包围，所以不是分组，匹配效果和第一个一样，但是不计入匹配结果中，所以matchObj.group(3)会报错
#6.matchObj.group() 等同于 matchObj.group(0)，表示匹配到的完整文本字符
#  matchObj.group(1) 得到第一组匹配结果，也就是(.*)匹配到的
#  matchObj.group(2) 得到第二组匹配结果，也就是(.*?)匹配到的


#example2
# 1.(?p<name>)这个正则的意思是，给匹配到的数字命名一个组名name，同一正则表达式中这个组名必须是唯一的
# 2.\d表示匹配一个数字，等于[0-9]
# 3.{3}表示匹配3次,所以\d{3}表示匹配3个数字
# 4.直接将匹配结果直接转为字典模式，方便使用