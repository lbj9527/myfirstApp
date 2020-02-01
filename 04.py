import re     #正则表达式模块


#任一个英文的纯文本文件，统计其中的单词出现的个数
def statistic_words():
    fin = open('file/english.txt','r')
    str = fin.read()

    words = re.findall('([a-z]+)\b?', str, re.IGNORECASE)

    wordDict = dict()

    for word in words:
        if word in wordDict:
            wordDict[word] += 1  #若wordDict中有word,则value加一
        else:
            wordDict[word] = 1   #若woedDict中无word,则新增一对key,value

    for key, value in wordDict.items():
        print('%s: %s' % (key, value))



if __name__ == "__main__":
    statistic_words()


###########################备注#################################
#1.[a-z],匹配一个小写字母
#2.[a-z]+,匹配多个小写字母
#3.\b?表示搜索单词边界,非贪婪模式



