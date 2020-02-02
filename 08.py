"""
敏感词文本文件 filtered_words.txt，里面的内容 和 07.py一样，
当用户输入敏感词语，则用 星号 * 替换，例如当用户输入「北京是个好城市」，则变成「**是个好城市」
"""

word_filter = set()
with open('file/filtered_words.txt', 'r', encoding = 'UTF-8') as f:
    for w in f.readlines():
        word_filter.add(w.strip())


while True:
    s = input()
    if s == 'exit':
        break
    for w in word_filter:
        if w in s:
            s = s.replace(w, '*'*len(w))
    print(s)



    