"""
姓名:
    段贤维
学号:
    20182294
班级:
    计科卓越班

"""

# 加载词库, 数据预处理
def loadLib(path):
    maxLen = 0 # 记录最长词语的长度
    with open (file = path,mode = "r") as f:
        data = f.readlines()
    #去除 开头的数字 和 末尾的'\n'
    for i in range(len(data)):
        if(len(data[i])==2):
            try:
                if(0<int(data[i])<10):
                    del data[i]
            except ValueError:
                data[i]=data[i][:-1]
                if(len(data[i])>maxLen):
                    maxLen = len(data[i])
        else:
            data[i] = data[i][2:-1]
            if(len(data[i])>maxLen):
                maxLen = len(data[i])
    return data,maxLen # 处理后的词库 和 最长词语的长度

# 前向最大匹配算法
def FMM(s,lib,maxLen):
    result = [] # 分词结果
    while s:
        if len(s) >= maxLen:
                temp = s[:maxLen] # 截取最长的词
        else:
            temp = s
        while len(temp) > 1: # 判断当前的词总长度是否大于1
            if temp in lib: # 判断当前词是否在词库中
                result.append(temp)
                break
            temp = temp[:-1] # 不在词库中，从后向前移动一个字

        if len(temp) == 1: # 当前词长度为1，单字成词
            result.append(temp)
        s = s[len(temp) :] # 在原句中删掉分出的词
    return result

# 后向最大匹配算法
def BMM(s,lib,maxLen):
    result = []
    while s:
        if len(s) > maxLen:
            temp = s[len(s) - maxLen :]  # 截取最长的词
        else:
            temp = s
        while len(temp) > 1:  # 判断当前的词总长度是否大于1
            if temp in lib:  # 判断当前词是否在词库中
                result.append(temp)
                break
            temp = temp[1:]  # 不在词库中，从前向后移动一个字

        if len(temp) == 1:  # 当前词长度为1，单字成词
            result.append(temp)
        s = s[: len(s) - len(temp)]  # 在原句中删掉分出的词

    result.reverse()
    return result

# 展示分词结果
def show(ans,method):
    if(method=='FMM'):
        print('FMM分词结果: ',end='')
    if(method=='BMM'):
        print('BMM分词结果: ',end='')
    l = len(ans)
    for i in range(l-1):
        print(ans[i],end=' / ')
    print(ans[l-1])


#主程序入口
if __name__=='__main__':
    lib,maxLen = loadLib("百度分词词库.txt")

    while(True):
        s = input("请输入待分词的中文句子(输入'q'退出): ")
        if(s=='q'):
            print('Bye~')
            break

        s1 = FMM(s,lib,maxLen)
        s2 = BMM(s,lib,maxLen)

        show(s1,"FMM")
        show(s2,"BMM")
# 测试样例:
# 王公子说的确实在理
# 市场中国有企业才能发展
