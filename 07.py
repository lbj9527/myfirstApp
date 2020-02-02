"""
敏感词文本文件 filtered_words.txt，里面的内容为以下内容，
当用户输入敏感词语时，则打印出 Freedom，否则打印出 Human Rights。
北京
程序员
公务员
领导
牛比
牛逼
你娘
你妈
love
sex
jiangge
"""

word_filter = set()
with open('file/filtered_words.txt','r', encoding='UTF-8') as f:
    for w in f.readlines():
        print(w)
        word_filter.add(w.strip())   #strip()在头尾删除参数中指定的字符;无参数代表删除空格

while True:
    s = input()
    if s== 'exit':
        break
    if s in word_filter:
        print('Freeom')
    else:
        print('Human Rights')