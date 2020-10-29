#199801.txt
import re
import jieba
import logging
from tqdm import tqdm,trange
from threading import Thread
import time

dicts={} #记录单个词语的次数
dicts_group = {}#记录二元词组的次数

# 展示建模进度条
def showBar():
    for i in trange(50):
        time.sleep(0.001)
        pass

# 处理语料
def removeSymbol(data):
    #去除空白行
    try:
        while(1):
            del data[data.index('\n')]
    except ValueError:
        #print(len(data))
        pass
    #去除无关信息
    for x in range(len(data)):
        data[x] = re.sub(r"[/A-Za-z\s]"," ",data[x])
        data[x] = re.sub(' +', ' ', data[x])
        data[x] = re.sub('。 ', '', data[x])
        data[x] = data[x][19:]
        data[x]="BOS"+data[x]+"EOS"#添加起始符BOS和终止符EOS
        #print(data[x])

#统计词频
def wordCount(data):
    word_no_repeat = 0
    for x in range(len(data)):
        sentence = data[x].split(' ')
        for i in range(len(sentence)):
            word = sentence[i]
            if word not in dicts:
                word_no_repeat +=1
                dicts[word]=1
            else:
                dicts[word]+=1
            if word!='EOS':
                after = sentence[i+1]
                if word+after not in dicts_group:
                    dicts_group[word+after]=1
                else:
                    dicts_group[word+after]+=1
    return word_no_repeat

#分词
def segmentation(sentence):
    sentence = 'BOS'+sentence+'EOS'
    lists=[]
    sentence = jieba.cut(sentence,HMM=False)
    format_sentence=",".join(sentence)
    #将词按","分割后依次填入数组word_list[]
    lists=format_sentence.split(",")
    #print(lists)
    return lists

#计算句子概率
def calProbability(s_seg,singleCount,dicts,dicts_group):
    #概率值为p
    p=1

    for i in range(len(s_seg)):
        if(i==0):
            continue
        word = s_seg[i]
        pre = s_seg[i-1]

        fz = 0
        if pre+word in dicts_group:
            fz = dicts_group[pre+word]

        fm = 0
        if pre in dicts:
            fm = dicts[pre]

        #数据平滑处理：加1法
        p*=(float(fz+1)/float(fm+singleCount))
    return p

#模型训练初始化
def buildModel():
    print('Bi-gram模型训练中...')

    thread = Thread(target=showBar)
    thread.start()

    with open (file = "199801.txt",mode = "r") as f1:
        data = f1.readlines()

    removeSymbol(data)

    singleCount = wordCount(data)

    jieba.setLogLevel(logging.INFO) #关闭jieba的日志信息

    thread.join()

    print('Bi-gram模型训练完成!')

    return singleCount

#主程序入口
if __name__=='__main__':
    singleCount = buildModel()
    #暂未实现的想法: 模型构建好之后, 把模型数据写到json文件, 以后每次运行之前, 先读取json , if 有, 就不用再花时间构建
    while(1):
        s = input("请输入待预测的中文句子(输入'q'退出): ")
        if(s=='q'):
            print('Bye~')
            break
        s_seg = []
        s_seg = segmentation(s)

        p = calProbability(s_seg,singleCount,dicts,dicts_group)

        print(f'这句话出现的概率是: {p}')
